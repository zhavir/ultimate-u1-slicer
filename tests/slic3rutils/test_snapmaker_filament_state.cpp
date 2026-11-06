#include <catch2/catch_test_macros.hpp>
#include "slic3r/Utils/SnapmakerFilamentState.hpp"

using namespace Slic3r::SnapmakerState;
using nlohmann::json;

namespace {
json stock_snapshot()
{
    // Source-derived stock u1-klipper contract, not a captured hardware response.
    return {{"result",
             {{"status",
               {{"print_task_config",
                 {{"filament_exist", {true, true, false, true}},
                  {"filament_type", {"PLA", "PETG", "NONE", "TPU"}},
                  {"filament_sub_type", {"NONE", "NONE", "NONE", "NONE"}},
                  {"filament_vendor", {"Snapmaker", "Vendor", "NONE", "Vendor"}},
                  {"filament_color_rgba", {"FF0000FF", "00FF00FF", "FFFFFFFF", "0000FFFF"}},
                  {"extruder_map_table", std::vector<int>(32, 3)}}},
                {"filament_detect",
                 {{"info",
                   {{{"VENDOR", "Snapmaker"}, {"BED_TEMP", 60}, {"FIRST_LAYER_TEMP", 210}},
                    {{"VENDOR", "Vendor"}, {"BED_TEMP", 80}, {"FIRST_LAYER_TEMP", 245}},
                    {{"VENDOR", "NONE"}, {"BED_TEMP", 0}, {"FIRST_LAYER_TEMP", 0}},
                    {{"VENDOR", "Vendor"}, {"BED_TEMP", 50}, {"FIRST_LAYER_TEMP", 220}}}}}}}}}}};
}
} // namespace

TEST_CASE("Stock U1 physical inventory is independent of logical job mapping", "[SnapmakerFilament]")
{
    std::array<FilamentSlot, 4> slots;
    std::string error;
    REQUIRE(parse_stock_filament_snapshot(stock_snapshot(), slots, error));
    CHECK(error.empty());
    CHECK(slots[0].material == "PLA");
    CHECK(slots[1].material == "PETG");
    CHECK_FALSE(slots[2].present);
    CHECK(slots[3].material == "TPU");
    REQUIRE(slots[0].nozzle_temperature);
    CHECK(*slots[0].nozzle_temperature == 210);
    CHECK(*slots[3].nozzle_temperature == 220);
    CHECK_FALSE(slots[2].nozzle_temperature);
}

TEST_CASE("Missing U1 RFID and material metadata stays unknown", "[SnapmakerFilament]")
{
    auto snapshot = stock_snapshot();
    auto& status  = snapshot["result"]["status"];
    status.erase("filament_detect");
    status["print_task_config"].erase("filament_type");
    std::array<FilamentSlot, 4> slots;
    std::string error;
    REQUIRE(parse_stock_filament_snapshot(snapshot, slots, error));
    CHECK(slots[0].material.empty());
    CHECK_FALSE(slots[0].nozzle_temperature);
    CHECK(slots[0].present);
}

TEST_CASE("Invalid U1 inventory cannot partially replace the last snapshot", "[SnapmakerFilament]")
{
    for (int corruption = 0; corruption < 5; ++corruption) {
        auto snapshot = stock_snapshot();
        auto& config  = snapshot["result"]["status"]["print_task_config"];
        if (corruption == 0)
            config["filament_exist"] = json::array({true, false});
        if (corruption == 1)
            config["filament_exist"][1] = "true";
        if (corruption == 2)
            config["filament_type"][1] = 42;
        if (corruption == 3)
            config["filament_vendor"][1] = std::string(257, 'x');
        if (corruption == 4)
            config["filament_exist"] = std::vector<bool>(32, true);
        std::array<FilamentSlot, 4> slots;
        slots[0].material = "previous observation";
        std::string error;
        CHECK_FALSE(parse_stock_filament_snapshot(snapshot, slots, error));
        CHECK_FALSE(error.empty());
        CHECK(slots[0].material == "previous observation");
    }
}

TEST_CASE("Invalid U1 tag metadata is ignored without parsing exceptions", "[SnapmakerFilament]")
{
    auto snapshot                                            = stock_snapshot();
    auto& status                                             = snapshot["result"]["status"];
    status["print_task_config"]["filament_color_rgba"][0]    = "not-a-color";
    status["filament_detect"]["info"][0]["FIRST_LAYER_TEMP"] = "210";
    status["filament_detect"]["info"][1]["BED_TEMP"]         = -1;
    status["filament_detect"]["info"][3]["FIRST_LAYER_TEMP"] = 65536;
    std::array<FilamentSlot, 4> slots;
    std::string error;
    REQUIRE(parse_stock_filament_snapshot(snapshot, slots, error));
    CHECK_FALSE(slots[0].rgba);
    CHECK_FALSE(slots[0].nozzle_temperature);
    CHECK_FALSE(slots[1].bed_temperature);
    CHECK_FALSE(slots[3].nozzle_temperature);
}

TEST_CASE("Malformed U1 response envelopes are rejected safely", "[SnapmakerFilament]")
{
    for (const json& response : {json(nullptr), json(1), json::array(), json{{"result", 7}}, json{{"result", {{"status", nullptr}}}}}) {
        std::array<FilamentSlot, 4> slots;
        std::string error;
        CHECK_FALSE(parse_stock_filament_snapshot(response, slots, error));
        CHECK_FALSE(error.empty());
    }
}

TEST_CASE("U1 color matching validates the complete RGB or RGBA value", "[SnapmakerFilament]")
{
    CHECK(rgb_value("#12AB34", false) == std::optional<std::uint32_t>(0x12AB34));
    CHECK(rgb_value("12ab34FF", true) == std::optional<std::uint32_t>(0x12AB34));
    CHECK_FALSE(rgb_value("12ab34ZZ", true));
    CHECK_FALSE(rgb_value("#12ab34", true));
    CHECK_FALSE(rgb_value("12ab34FF", false));
    CHECK_FALSE(rgb_value("", false));
    CHECK_FALSE(rgb_value("#", false));
}
