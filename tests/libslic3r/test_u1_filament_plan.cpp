#include <catch2/catch_test_macros.hpp>
#include "libslic3r/U1FilamentPlan.hpp"

#include <stdexcept>
#include <vector>

using Slic3r::plan_u1_filament_partition;
using nlohmann::json;

namespace {
json request() { return {{"events", {0, 1, 0, 1}}, {"nozzle_diameters", {0.2, 0.4, 0.6, 0.8}}, {"filament_nozzle", {0, 1}}}; }
} // namespace

TEST_CASE("U1 planning preserves a feasible four-head partition without printer side effects", "[U1FilamentPlan]")
{
    const auto result = plan_u1_filament_partition(request());
    REQUIRE(result["ok"] == true);
    CHECK(result["advisory_only"] == true);
    CHECK(result["material_compatibility"] == "not_checked");
    CHECK(result["swaps_proposed"] == 0);
    REQUIRE(result["proposed_nozzle"].size() == 2);
    CHECK(result["proposed_nozzle"][0] != result["proposed_nozzle"][1]);
}

TEST_CASE("U1 planning rejects invalid nozzle and filament mappings before search", "[U1FilamentPlan]")
{
    auto args      = request();
    args["events"] = {-1};
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args           = request();
    args["events"] = {4294967295ULL};
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args                     = request();
    args["nozzle_diameters"] = {0.4, 0.4, 0.4};
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args                        = request();
    args["nozzle_diameters"][0] = 0.0;
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args             = request();
    args["head_ace"] = {1, 1, 1, 1};
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args                       = request();
    args["filament_nozzle"][0] = 4;
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args           = request();
    args["events"] = json::array();
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args                = request();
    args["start_print"] = true;
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
}

TEST_CASE("U1 planning bounds the combinatorial search", "[U1FilamentPlan]")
{
    auto args               = request();
    args["events"]          = {0, 1, 2, 3, 4, 5, 6, 7, 8};
    args["filament_nozzle"] = {-1, -1, -1, -1, -1, -1, -1, -1, -1};
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args           = request();
    args["events"] = std::vector<int>(4097, 0);
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
    args                    = request();
    args["filament_nozzle"] = {-1, -1, -1, -1, -1, -1, -1, -1};
    args["events"]          = std::vector<int>(4096, 0);
    for (int index = 0; index < 8; ++index)
        args["events"][index] = index;
    CHECK_THROWS_AS(plan_u1_filament_partition(args), std::invalid_argument);
}

TEST_CASE("A tied-cost diameter change still requires reslicing", "[U1FilamentPlan]")
{
    auto args               = request();
    args["filament_nozzle"] = {3, 2};
    const auto result       = plan_u1_filament_partition(args);
    REQUIRE(result["ok"] == true);
    CHECK(result["improved"] == false);
    CHECK(result["requires_reslice"] == true);
}
