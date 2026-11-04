#pragma once

#include <string>
#include <initializer_list>

namespace Slic3r { namespace GUI { namespace Mcp {

// Only reviewed, typed slicer operations. In particular, no generic UI/action/script/plugin
// bridge can be used to click Print, run a macro, edit connections or bypass file authorization.
// Keep printer-control disabled until operator approval is implemented in that adapter.
inline bool u1_slicer_tool_allowed(const std::string& name)
{
    for (const char* allowed : {"get_state", "list_objects", "select", "transform", "arrange", "slice", "cancel", "get_preview",
                                "list_plates", "wait", "list_presets", "u1_plan_filament_partition"})
        if (name == allowed)
            return true;
    return false;
}

}}} // namespace Slic3r::GUI::Mcp
