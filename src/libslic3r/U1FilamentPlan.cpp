#include "U1FilamentPlan.hpp"
#include "FosFilamentArrangement.hpp"

#include <cmath>
#include <cstddef>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace Slic3r {

nlohmann::json plan_u1_filament_partition(const nlohmann::json& args)
{
    if (!args.is_object())
        throw std::invalid_argument("arguments must be an object");
    const std::set<std::string> keys{"events", "nozzle_diameters", "filament_nozzle", "head_ace"};
    for (auto it = args.begin(); it != args.end(); ++it)
        if (!keys.count(it.key()))
            throw std::invalid_argument("unknown argument: " + it.key());
    for (const char* name : {"events", "nozzle_diameters", "filament_nozzle"})
        if (!args.contains(name) || !args[name].is_array())
            throw std::invalid_argument(std::string(name) + " must be an array");
    if (args["nozzle_diameters"].size() != 4)
        throw std::invalid_argument("U1 requires exactly four physical nozzle diameters");
    if (args["events"].empty() || args["events"].size() > 4096)
        throw std::invalid_argument("events must contain between 1 and 4096 filament indices");
    if (args["filament_nozzle"].empty() || args["filament_nozzle"].size() > 16)
        throw std::invalid_argument("filament_nozzle must contain between 1 and 16 entries");

    FosArrangementInput input;
    input.topology     = 2; // FOrca head topology; does not imply that an ACE is installed.
    input.max_distinct = 8; // Bound the four-head brute-force search to 4^8 placements.
    for (const auto& value : args["nozzle_diameters"]) {
        if (!value.is_number())
            throw std::invalid_argument("nozzle diameters must be numeric");
        const double diameter = value.get<double>();
        if (!std::isfinite(diameter) || diameter < 0.1 || diameter > 1.2)
            throw std::invalid_argument("nozzle diameters must be finite and between 0.1 and 1.2 mm");
        input.phys_nozzle_diameter.push_back(diameter);
    }
    for (const auto& value : args["filament_nozzle"]) {
        if (!value.is_number_integer() || value.get<double>() < -1 || value.get<double>() > 3)
            throw std::invalid_argument("filament_nozzle entries must be integers from -1 to 3");
        input.filament_nozzle.push_back(value.get<int>());
    }
    std::set<unsigned int> distinct;
    for (const auto& value : args["events"]) {
        if (!value.is_number_integer() || value.get<double>() < 0 || value.get<double>() >= input.filament_nozzle.size())
            throw std::invalid_argument("event references an unconfigured filament");
        const auto filament = value.get<unsigned int>();
        input.events.push_back(filament);
        distinct.insert(filament);
    }
    if (distinct.size() > 8)
        throw std::invalid_argument("at most eight distinct filaments are supported per planning request");
    const std::size_t placements = std::size_t{1} << (2 * distinct.size());
    if (placements * input.events.size() > 4u * 1024u * 1024u)
        throw std::invalid_argument("planning request exceeds the bounded search work budget");
    input.head_ace.assign(4, 0);
    if (args.contains("head_ace")) {
        if (!args["head_ace"].is_array() || args["head_ace"].size() != 4)
            throw std::invalid_argument("head_ace must contain exactly four booleans");
        for (std::size_t index = 0; index < 4; ++index) {
            if (!args["head_ace"][index].is_boolean())
                throw std::invalid_argument("head_ace entries must be booleans");
            input.head_ace[index] = args["head_ace"][index].get<bool>() ? 1 : 0;
        }
    }
    const auto result     = compute_filament_arrangement(input);
    bool changes_diameter = false;
    for (std::size_t filament = 0; filament < result.proposed_nozzle.size(); ++filament) {
        const int proposed = result.proposed_nozzle[filament];
        if (proposed < 0)
            continue;
        const int current = input.filament_nozzle[filament];
        if (current < 0 || std::abs(input.phys_nozzle_diameter[current] - input.phys_nozzle_diameter[proposed]) > 1e-6)
            changes_diameter = true;
    }
    return {{"ok", result.ok},
            {"reason", result.reason},
            {"improved", result.improved},
            {"proposed_nozzle", result.proposed_nozzle},
            {"swaps_current", result.swaps_current},
            {"swaps_proposed", result.swaps_proposed},
            {"stall_seconds_current", result.stall_s_current},
            {"stall_seconds_proposed", result.stall_s_proposed},
            {"advisory_only", true},
            {"requires_reslice", changes_diameter},
            {"material_compatibility", "not_checked"},
            {"time_model", "FOrca inline swap cost only; extrusion time omitted"}};
}

} // namespace Slic3r
