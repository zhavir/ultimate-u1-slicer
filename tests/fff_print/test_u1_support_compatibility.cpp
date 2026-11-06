#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>
#include <catch2/catch_message.hpp>
#include <catch2/generators/catch_generators.hpp>
#include <limits>
#include "test_helpers.hpp"
#include "test_utils.hpp"
#include "libslic3r/Format/bbs_3mf.hpp"
#include "libslic3r/Preset.hpp"
#include "libslic3r/ClipperUtils.hpp"
#include "libslic3r/Support/SupportCommon.hpp"

using namespace Slic3r;

TEST_CASE("Snapmaker support stability expansion uses footprint moments", "[U1SupportCompatibility]")
{
    const ExPolygon square(Polygon({Point(0., 0.), Point(scale_(10.), 0.), Point(scale_(10.), scale_(10.)), Point(0., scale_(10.))}));
    // Square Ixx=Iyy=10^4/12 mm^4. This case is inside the upstream 1..10 mm clamps.
    const double expected = (100. / (10000. / 12.) * 10.) * 100. / 1920. * 70.;
    CHECK(snapmaker_support_auto_expansion(square, 70., 100.) == Catch::Approx(expected));
    CHECK(snapmaker_support_auto_expansion(square, 1., 1.) == Catch::Approx(1.));
    CHECK(snapmaker_support_auto_expansion(square, 1000., 1000.) == Catch::Approx(10.));
    CHECK(snapmaker_support_auto_expansion(square, 0., 100.) == 0.);
    CHECK(snapmaker_support_auto_expansion(square, 70., 0.) == 0.);
    CHECK(snapmaker_support_auto_expansion(square, std::numeric_limits<double>::quiet_NaN(), 100.) == 0.);
    CHECK(snapmaker_support_auto_expansion(ExPolygon{}, 70., 100.) == 0.);
}

TEST_CASE("Snapmaker stepped support growth cannot cross a thin collision wall", "[U1SupportCompatibility]")
{
    const ExPolygons island{
        ExPolygon(Polygon({Point(0., 0.), Point(scale_(1.), 0.), Point(scale_(1.), scale_(1.)), Point(0., scale_(1.))}))};
    const ExPolygons wall{ExPolygon(Polygon({Point(scale_(2.), scale_(-10.)), Point(scale_(2.5), scale_(-10.)),
                                             Point(scale_(2.5), scale_(10.)), Point(scale_(2.), scale_(10.))}))};
    const ExPolygons grown = snapmaker_support_offset(island, scale_(4.), wall, scale_(0.2));
    REQUIRE_FALSE(grown.empty());
    CHECK(intersection_ex(grown, wall).empty());
    CHECK(get_extents(grown).max.x() <= scale_(2.) + SCALED_EPSILON);
    CHECK(area(grown) > area(island));
    CHECK(area(snapmaker_support_offset(island, scale_(4.), wall, 0)) == Catch::Approx(area(island)));
}

TEST_CASE("Normal support automatic expansion has the Snapmaker two millimeter footprint", "[U1SupportCompatibility]")
{
    Print automatic, explicit_width;
    Test::init_and_process_print({Test::TestMesh::overhang}, automatic,
                                 {{"enable_support", true},
                                  {"support_type", "normal(auto)"},
                                  {"support_style", "grid"},
                                  {"raft_first_layer_expansion", -1.0}});
    Test::init_and_process_print({Test::TestMesh::overhang}, explicit_width,
                                 {{"enable_support", true},
                                  {"support_type", "normal(auto)"},
                                  {"support_style", "grid"},
                                  {"raft_first_layer_expansion", 2.0}});
    const auto& a = automatic.objects().front()->support_layers();
    const auto& b = explicit_width.objects().front()->support_layers();
    REQUIRE_FALSE(a.empty());
    REQUIRE(a.size() == b.size());
    REQUIRE_FALSE(a.front()->support_islands.empty());
    CHECK(diff_ex(a.front()->support_islands, b.front()->support_islands).empty());
    CHECK(diff_ex(b.front()->support_islands, a.front()->support_islands).empty());
}

TEST_CASE("Original Snapmaker v2.4.1 projects slice with their retained machine macros", "[U1SupportCompatibility][U1OriginalProject]")
{
    const bool four_tools  = GENERATE(false, true);
    const std::string path = std::string(TEST_DATA_DIR) + "/u1/snapmaker-v2.4.1/" + (four_tools ? "four-tool.3mf" : "single-tool.3mf");
    ScopedTemporaryDir backup("u1_original_slice");
    Model model;
    model.set_backup_path(backup.string());
    DynamicPrintConfig config = DynamicPrintConfig::full_print_config();
    ConfigSubstitutionContext substitutions{ForwardCompatibilitySubstitutionRule::Enable};
    PlateDataPtrs plates;
    std::vector<Preset*> presets;
    bool is_bambu = false, is_orca = false;
    Semver version;
    const bool loaded = load_bbs_3mf(path.c_str(), &config, &substitutions, &model, &plates, &presets, &is_bambu, &is_orca, &version,
                                     nullptr, LoadStrategy::LoadModel | LoadStrategy::LoadConfig);
    release_PlateData_list(plates);
    for (Preset* preset : presets)
        delete preset;
    REQUIRE(loaded);
    config.normalize_fdm();
    REQUIRE(config.opt_float("raft_first_layer_expansion") == -1.);
    REQUIRE(config.option<ConfigOptionBool>("snapmaker_support_expansion")->value);
    Print print;
    for (ModelObject* object : model.objects)
        print.auto_assign_extruders(object);
    print.apply(model, config);
    const auto validation = print.validate();
    INFO(validation.string);
    REQUIRE(validation.string.empty());
    print.set_status_silent();
    const std::string output = Test::gcode(print);
    CHECK_FALSE(output.empty());
    CHECK(print.objects().size() == (four_tools ? 4 : 1));
    CHECK(print.extruders().size() == (four_tools ? 4 : 1));
}

TEST_CASE("Snapmaker chamber cooling follows material softening thresholds and high temperature overrides",
          "[U1SupportCompatibility][U1ChamberCooling]")
{
    const int scenario        = GENERATE(0, 1, 2, 3);
    const int vitrification[] = {50, 70, 71, 50};
    const int expected[]      = {2, 1, 0, 0};
    auto config               = Test::multifilament_config(1, {{"machine_start_gcode", "; U1_CHAMBER_MODE={chamber_cooling_mode}\n"},
                                                               {"temperature_vitrification", vitrification[scenario]},
                                                               {"filament_is_high_temperature", scenario == 3}});
    const std::string output  = Test::slice({Test::cube(4.)}, config);
    CHECK(output.find("; U1_CHAMBER_MODE=" + std::to_string(expected[scenario])) != std::string::npos);
}

TEST_CASE("Snapmaker chamber cooling considers every used filament", "[U1SupportCompatibility][U1ChamberCooling]")
{
    auto config = Test::multifilament_config(2, {{"machine_start_gcode", "; U1_CHAMBER_MODE={chamber_cooling_mode}\n"},
                                                 {"temperature_vitrification", "80,50"},
                                                 {"filament_is_high_temperature", "1,0"}});
    Print print;
    Model model;
    std::vector<std::vector<ConfigBase::SetDeserializeItem>> overrides{{{"extruder", 1}}, {{"extruder", 2}}};
    Test::init_print(std::vector<TriangleMesh>{Test::cube(4.), Test::cube(4.)}, print, model, config, &overrides);
    REQUIRE(print.extruders().size() == 2);
    const std::string output = Test::gcode(print);
    CHECK(output.find("; U1_CHAMBER_MODE=2") != std::string::npos);
}
