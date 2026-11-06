#pragma once

#include <nlohmann/json.hpp>
#include <array>
#include <cstdint>
#include <optional>
#include <string>
#include <utility>

namespace Slic3r { namespace SnapmakerState {

// Stock U1 source contract: u1-klipper 7ac453b50fe6779b2ec0b759038a17da5e6d671d,
// extras/print_task_config.py and extras/filament_detect.py. Inventory is four
// PHYSICAL slots; the separate 32-entry extruder_map_table is a job mapping.
struct FilamentSlot
{
    bool present{false};
    std::string material;
    std::string subtype;
    std::string vendor;
    std::optional<std::string> rgba;
    std::optional<int> bed_temperature;
    std::optional<int> nozzle_temperature;
};

inline std::optional<std::uint32_t> rgb_value(const std::string& text, bool alpha)
{
    const size_t start = !text.empty() && text.front() == '#' ? 1 : 0;
    if (text.size() - start != (alpha ? 8u : 6u))
        return std::nullopt;
    std::uint32_t rgb = 0;
    for (size_t i = start; i < text.size(); ++i) {
        const char ch = text[i];
        int digit     = ch >= '0' && ch <= '9' ? ch - '0' :
                        ch >= 'a' && ch <= 'f' ? ch - 'a' + 10 :
                        ch >= 'A' && ch <= 'F' ? ch - 'A' + 10 :
                                                 -1;
        if (digit < 0)
            return std::nullopt;
        if (i < start + 6)
            rgb = (rgb << 4) | static_cast<std::uint32_t>(digit);
    }
    return rgb;
}

inline bool parse_stock_filament_snapshot(const nlohmann::json& response, std::array<FilamentSlot, 4>& slots, std::string& error)
{
    error.clear();
    if (!response.is_object() || !response.contains("result") || !response["result"].is_object() ||
        !response["result"].contains("status") || !response["result"]["status"].is_object()) {
        error = "Missing stock U1 result.status object";
        return false;
    }
    const auto* status = &response["result"]["status"];
    if (!status->contains("print_task_config") || !(*status)["print_task_config"].is_object()) {
        error = "Missing stock U1 print_task_config object";
        return false;
    }
    const auto& config = (*status)["print_task_config"];
    const auto exist   = config.find("filament_exist");
    if (exist == config.end() || !exist->is_array() || exist->size() != slots.size()) {
        error = "Stock U1 inventory must report four physical filament slots; extended topology requires its own capability adapter";
        return false;
    }
    std::array<FilamentSlot, 4> parsed;
    for (size_t i = 0; i < parsed.size(); ++i) {
        if (!(*exist)[i].is_boolean()) {
            error = "Invalid stock U1 filament presence value";
            return false;
        }
        parsed[i].present = (*exist)[i].get<bool>();
    }
    const std::array<const char*, 4> fields{{"filament_type", "filament_sub_type", "filament_vendor", "filament_color_rgba"}};
    for (size_t field = 0; field < fields.size(); ++field) {
        const auto values = config.find(fields[field]);
        if (values == config.end())
            continue; // Unreported material metadata remains unknown, never PLA.
        if (!values->is_array() || values->size() != parsed.size()) {
            error = "Stock U1 filament metadata does not match the physical slots";
            return false;
        }
        for (size_t i = 0; i < parsed.size(); ++i) {
            if (!(*values)[i].is_string() || (*values)[i].get_ref<const std::string&>().size() > 256) {
                error = "Invalid stock U1 filament metadata value";
                return false;
            }
            const std::string text = (*values)[i].get<std::string>();
            if (field == 0)
                parsed[i].material = text == "NONE" ? "" : text;
            if (field == 1)
                parsed[i].subtype = text == "NONE" ? "" : text;
            if (field == 2)
                parsed[i].vendor = text == "NONE" ? "" : text;
            if (field == 3 && rgb_value(text, true))
                parsed[i].rgba = text;
        }
    }
    const auto detection = status->find("filament_detect");
    if (detection != status->end() && detection->is_object()) {
        const auto info = detection->find("info");
        if (info != detection->end() && info->is_array() && info->size() == parsed.size()) {
            for (size_t i = 0; i < parsed.size(); ++i) {
                const auto& tag = (*info)[i];
                if (!tag.is_object() || !tag.contains("VENDOR") || !tag["VENDOR"].is_string() || tag["VENDOR"] == "NONE" ||
                    tag["VENDOR"] == "")
                    continue;
                const auto temperature = [&tag](const char* key) -> std::optional<int> {
                    const auto value = tag.find(key);
                    if (value == tag.end() || !value->is_number_integer())
                        return std::nullopt;
                    // Protocol fields are unsigned 16-bit metadata, not heater targets.
                    if (*value < 0 || *value > 65535)
                        return std::nullopt;
                    return value->get<int>();
                };
                parsed[i].bed_temperature    = temperature("BED_TEMP");
                parsed[i].nozzle_temperature = temperature("FIRST_LAYER_TEMP");
            }
        }
    }
    slots = std::move(parsed); // Commit only a completely validated inventory.
    return true;
}

}} // namespace Slic3r::SnapmakerState
