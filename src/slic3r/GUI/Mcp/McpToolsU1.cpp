#include "McpTools.hpp"
#include "McpService.hpp"
#include "libslic3r/U1FilamentPlan.hpp"
#include "slic3r/GUI/I18N.hpp"

#include <stdexcept>

namespace Slic3r { namespace GUI { namespace Mcp {

void register_u1_tools(McpService& service)
{
    using nlohmann::json;
    const json integers = {{"type", "array"}, {"items", {{"type", "integer"}}}};
    service.registry().add(
        inspect_tool("u1_plan_filament_partition", L("Plan U1 filament partition"),
                     "Propose a filament partition across four nozzle diameters using FOrca's bounded optimizer. "
                     "Advisory only; does not change the project, check material compatibility or send printer commands. "
                     "Indices are zero-based; head_ace describes operator-declared hardware, not detected capabilities.",
                     object_schema({{"events", integers},
                                    {"nozzle_diameters", {{"type", "array"}, {"items", {{"type", "number"}}}}},
                                    {"filament_nozzle", integers},
                                    {"head_ace", {{"type", "array"}, {"items", {{"type", "boolean"}}}}}},
                                   {"events", "nozzle_diameters", "filament_nozzle"}),
                     [](const json& args, ToolContext&) {
                         try {
                             return ToolResult::ok(plan_u1_filament_partition(args));
                         } catch (const std::invalid_argument& error) {
                             return ToolResult::error(error.what());
                         }
                     }));
}

}}} // namespace Slic3r::GUI::Mcp
