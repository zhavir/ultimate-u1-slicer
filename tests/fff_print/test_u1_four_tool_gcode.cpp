#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>

#include "libslic3r/Config.hpp"
#include "libslic3r/GCodeReader.hpp"
#include "libslic3r/Model.hpp"
#include "libslic3r/Point.hpp"
#include "libslic3r/Print.hpp"
#include "libslic3r/PrintConfig.hpp"
#include "test_helpers.hpp"

#include <algorithm>
#include <cctype>
#include <set>
#include <string>

using namespace Slic3r;

TEST_CASE("Four-head Klipper slicing emits only the assigned tools", "[U1ToolGcode][Regression]")
{
    // A synthetic four-independent-head fixture, not a claim of calibrated U1 presets,
    // vendor docking macros, material compatibility or physical printer verification.
    const int materials       = GENERATE(1, 4);
    DynamicPrintConfig config = Test::multifilament_config(materials);
    config.set_num_extruders(4);
    config.set_deserialize_strict({
        {"nozzle_diameter", "0.4,0.4,0.4,0.4"},
        {"extruder_offset", "0x0,0x0,0x0,0x0"},
        {"printer_extruder_id", "1,2,3,4"},
        {"printer_extruder_variant", "Direct Drive Standard,Direct Drive Standard,Direct Drive Standard,Direct Drive Standard"},
        {"physical_extruder_map", "0,1,2,3"},
        {"filament_map_mode", "Manual"},
        {"filament_map", materials == 1 ? "1" : "1,2,3,4"},
        {"single_extruder_multi_material", false},
        {"gcode_flavor", "klipper"},
        {"enable_prime_tower", false},
        {"skirt_loops", 0},
        {"brim_type", "no_brim"},
        {"layer_height", 0.2},
        {"printable_area", "0x0,270x0,270x270,0x270"},
        {"machine_start_gcode", "G90\nM83\nT[initial_extruder]\n"},
        {"change_filament_gcode", "T[next_extruder]\n"},
        {"layer_change_gcode", "G92 E0\n"},
        {"use_relative_e_distances", true},
    });

    Model model;
    Print print;
    for (int index = 0; index < materials; ++index) {
        ModelObject* object = model.add_object();
        object->add_volume(Test::cube(5));
        object->config.set("extruder", index + 1);
        object->add_instance()->set_offset(Vec3d(10.0 + 15.0 * index, 10.0, 0.0));
        object->ensure_on_bed();
        print.auto_assign_extruders(object);
    }
    print.apply(model, config);
    print.set_status_silent();
    std::string gcode;
    REQUIRE_NOTHROW(gcode = Test::gcode(print));

    int active_tool   = -1;
    bool invalid_tool = false;
    std::set<int> extruding_tools;
    GCodeReader reader;
    reader.parse_buffer(gcode, [&](GCodeReader& state, const GCodeReader::GCodeLine& line) {
        const std::string command(line.cmd());
        if (command.size() > 1 && command.front() == 'T' &&
            std::all_of(command.begin() + 1, command.end(), [](unsigned char c) { return std::isdigit(c); })) {
            active_tool  = std::stoi(command.substr(1));
            invalid_tool = invalid_tool || active_tool < 0 || active_tool > 3;
        }
        if (line.extruding(state))
            extruding_tools.insert(active_tool);
    });
    CHECK_FALSE(invalid_tool);
    std::set<int> expected;
    for (int index = 0; index < materials; ++index)
        expected.insert(index);
    CHECK(extruding_tools == expected);
}
