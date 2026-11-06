#include "SnapmakerPrinterAgent.hpp"
#include "SnapmakerFilamentState.hpp"
#include <limits>
#include "Http.hpp"
#include "MoonrakerPrinterAgent.hpp"
#include "IPrinterAgent.hpp"
#include "libslic3r/PresetBundle.hpp"
#include "slic3r/GUI/GUI_App.hpp"

#include "nlohmann/json.hpp"
#include <boost/log/trivial.hpp>
#include <vector>
#include <string>
#include "libslic3r/Preset.hpp"
#include <cstddef>
#include <utility>

namespace Slic3r {

namespace {

constexpr const char* SNAPMAKER_AGENT_VERSION = "0.0.2";

std::string find_closest_color_preset_by_vendor_and_type(const PresetCollection& filaments,
                                                         const std::string&      vendor_name,
                                                         const std::string&      filament_type,
                                                         const std::string&      color_rgba)
{
    std::string best_match_id       = "";
    unsigned int best_color_distance = std::numeric_limits<unsigned int>::max();
    const auto target                = SnapmakerState::rgb_value(color_rgba, true);
    if (!target || vendor_name.empty() || filament_type.empty())
        return {};

    for (const auto& p : filaments.get_presets()) {
        if (p.is_visible && p.is_compatible &&
            // Filament profile must be detached from parent to be considered for matching
            filaments.get_preset_base(p) == &p && p.config.opt_string("filament_vendor", 0u) == vendor_name &&
            p.config.opt_string("filament_type", 0u) == filament_type) {
            const auto preset_color = SnapmakerState::rgb_value(p.config.opt_string("default_filament_colour", 0u), false);
            if (!preset_color)
                continue;
            const unsigned int target_color_value = *target;
            const unsigned int p_color_value      = *preset_color;

            // Calculate Euclidean color distance in RGB space
            int dr                = int(target_color_value & 0xff) - int(p_color_value & 0xff);
            int dg                = int((target_color_value >> 8) & 0xff) - int((p_color_value >> 8) & 0xff);
            int db                = int((target_color_value >> 16) & 0xff) - int((p_color_value >> 16) & 0xff);
            unsigned int distance = dr * dr + dg * dg + db * db;

            if (distance < best_color_distance) {
                best_color_distance = distance;
                best_match_id       = p.filament_id;
            }
        }
    }
    return best_match_id;
}

} // anonymous namespace

SnapmakerPrinterAgent::SnapmakerPrinterAgent(std::string log_dir) : MoonrakerPrinterAgent(std::move(log_dir)) {}

AgentInfo SnapmakerPrinterAgent::get_agent_info_static()
{
    return AgentInfo{"snapmaker", "Snapmaker", SNAPMAKER_AGENT_VERSION, "Snapmaker printer agent"};
}

std::string SnapmakerPrinterAgent::combine_filament_type(const std::string& type, const std::string& sub_type)
{
    const std::string base = trim_and_upper(type);
    const std::string sub  = trim_and_upper(sub_type);

    if (base.empty() || base == "NONE")
        return {};

    if (sub.empty() || sub == "NONE")
        return base;

    if (sub == "CF")
        return base + "-CF";
    if (sub == "GF")
        return base + "-GF";
    if (sub == "SNAPSPEED" || sub == "HS")
        return base + " HIGH SPEED";
    if (sub == "SILK")
        return base + " SILK";
    if (sub == "WOOD")
        return base + " WOOD";
    if (sub == "MATTE")
        return base + " MATTE";
    if (sub == "MARBLE")
        return base + " MARBLE";

    // Unrecognized sub-type (brand names like Polylite, Basic, etc.) -- use base type only
    return base;
}

bool SnapmakerPrinterAgent::fetch_filament_info(std::string dev_id, FilamentSyncMode /*sync_mode*/)
{
    std::string url = join_url(device_info.base_url, "/printer/objects/query?print_task_config&filament_detect");

    std::string response_body;
    bool        success = false;
    std::string http_error;

    auto http = Http::get(url);
    if (!device_info.api_key.empty()) {
        http.header("X-Api-Key", device_info.api_key);
    }
    http.timeout_connect(5)
        .timeout_max(10)
        .on_complete([&](std::string body, unsigned status) {
            if (status == 200) {
                response_body = body;
                success       = true;
            } else {
                http_error = "HTTP error: " + std::to_string(status);
            }
        })
        .on_error([&](std::string body, std::string err, unsigned status) {
            http_error = err;
            if (status > 0) {
                http_error += " (HTTP " + std::to_string(status) + ")";
            }
        })
        .perform_sync();

    if (!success) {
        BOOST_LOG_TRIVIAL(warning) << "SnapmakerPrinterAgent::fetch_filament_info: HTTP request failed: " << http_error;
        return false;
    }

    auto json = nlohmann::json::parse(response_body, nullptr, false, true);
    if (json.is_discarded()) {
        BOOST_LOG_TRIVIAL(warning) << "SnapmakerPrinterAgent::fetch_filament_info: Invalid JSON response";
        return false;
    }

    std::array<SnapmakerState::FilamentSlot, 4> slots;
    std::string parse_error;
    if (!SnapmakerState::parse_stock_filament_snapshot(json, slots, parse_error)) {
        BOOST_LOG_TRIVIAL(warning) << "Snapmaker filament sync: " << parse_error;
        return false;
    }
    const int slot_count                   = static_cast<int>(slots.size());
    static const std::string default_color = "FFFFFFFF"; // Neutral display color only; never used for preset matching.

    std::vector<AmsTrayData> trays;
    trays.reserve(slot_count);

    for (int i = 0; i < slot_count; ++i) {
        AmsTrayData tray;
        tray.slot_index   = i;
        const auto& slot  = slots[i];
        tray.has_filament = slot.present;

        if (tray.has_filament) {
            tray.tray_type  = combine_filament_type(slot.material, slot.subtype);
            tray.tray_color = slot.rgba.value_or(default_color);

            auto* bundle = GUI::wxGetApp().preset_bundle;
            // Try to find a matching preset for this filament based on vendor, type and color.
            // If not found, default to traditional search by type only or generic type mapping.
            if (bundle && !tray.tray_type.empty()) {
                const std::string filament_id = slot.rgba ? find_closest_color_preset_by_vendor_and_type(bundle->filaments, slot.vendor,
                                                                                                         tray.tray_type, *slot.rgba) :
                                                            "";

                if (!filament_id.empty()) {
                    tray.tray_info_idx = filament_id;
                    BOOST_LOG_TRIVIAL(warning) << "Filament sync: Found manufacturer-specific profile for slot " << i << ": "
                                               << filament_id;
                } else {
                    tray.tray_info_idx = bundle->filaments.filament_id_by_type(tray.tray_type);
                }
            } else if (!tray.tray_type.empty()) {
                tray.tray_info_idx = map_filament_type_to_generic_id(tray.tray_type);
            }

            // Physical-slot NFC observations remain metadata; no writes/heating.
            tray.bed_temp    = slot.bed_temperature.value_or(0);
            tray.nozzle_temp = slot.nozzle_temperature.value_or(0);
        }

        trays.emplace_back(std::move(tray));
    }

    build_ams_payload(1, slot_count - 1, trays);
    return true;
}

} // namespace Slic3r
