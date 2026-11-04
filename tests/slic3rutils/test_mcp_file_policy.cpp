#include <catch2/catch_test_macros.hpp>
#include "slic3r/GUI/Mcp/McpFilePolicy.hpp"

#include <atomic>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <string>

using Slic3r::GUI::Mcp::FileAccessPolicy;
namespace fs = std::filesystem;

namespace {
struct Sandbox
{
    fs::path root;
    Sandbox()
    {
        static std::atomic<unsigned long> serial{0};
        root = fs::temp_directory_path() / ("u1-policy-" + std::to_string(std::chrono::steady_clock::now().time_since_epoch().count()) +
                                            "-" + std::to_string(serial++));
        fs::create_directories(root / "allowed");
        fs::create_directories(root / "allowed-sibling");
        std::ofstream(root / "allowed-sibling" / "secret.txt") << "private";
    }
    ~Sandbox()
    {
        std::error_code error;
        fs::remove_all(root, error);
    }
};
} // namespace

TEST_CASE("MCP file authorization uses path components and denies by default", "[McpFilePolicy]")
{
    Sandbox sandbox;
    FileAccessPolicy policy({sandbox.root / "allowed"});
    std::string error;
    CHECK(policy.permits(sandbox.root / "allowed" / "new.3mf", error));
    CHECK_FALSE(policy.permits(sandbox.root / "allowed-sibling" / "secret.txt", error));
    CHECK_FALSE(policy.permits(sandbox.root / "allowed" / ".." / "allowed-sibling" / "secret.txt", error));
    CHECK_FALSE(policy.permits("relative.3mf", error));
    CHECK_FALSE(FileAccessPolicy({}).permits(sandbox.root / "allowed" / "new.3mf", error));
    CHECK_FALSE(FileAccessPolicy({sandbox.root / "missing"}).permits(sandbox.root / "missing" / "new.3mf", error));
}

TEST_CASE("MCP file authorization refuses symlinks that escape a root", "[McpFilePolicy]")
{
    Sandbox sandbox;
    std::error_code ec;
    fs::create_directory_symlink(sandbox.root / "allowed-sibling", sandbox.root / "allowed" / "escape", ec);
    if (ec) {
        SKIP("This platform does not permit unprivileged symlink creation");
    }
    FileAccessPolicy policy({sandbox.root / "allowed"});
    std::string error;
    CHECK_FALSE(policy.permits(sandbox.root / "allowed" / "escape" / "secret.txt", error));
    CHECK_FALSE(policy.permits(sandbox.root / "allowed" / "escape" / "new.gcode", error));
}

TEST_CASE("MCP file authorization accepts Unicode names inside an authorized root", "[McpFilePolicy]")
{
    Sandbox sandbox;
    const fs::path directory = sandbox.root / "allowed" / fs::u8path(u8"material-\u6750\u6599");
    fs::create_directory(directory);
    FileAccessPolicy policy({sandbox.root / "allowed"});
    std::string error;
    CHECK(policy.permits(directory / fs::u8path(u8"filam\u00e9nt.3mf"), error));
    CHECK(error.empty());
}
