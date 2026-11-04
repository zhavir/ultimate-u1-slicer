#pragma once

#include <nlohmann/json.hpp>

namespace Slic3r {

// Advisory only. Throws std::invalid_argument for an unsafe or incomplete request. Does not
// mutate project configuration, contact hardware, or assert that a material pair is compatible.
nlohmann::json plan_u1_filament_partition(const nlohmann::json& arguments);

} // namespace Slic3r
