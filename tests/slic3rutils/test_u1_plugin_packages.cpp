#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>

#include "plugin_test_utils.hpp"
#include "slic3r/plugin/PluginLoader.hpp"
#include "slic3r/plugin/PluginFsUtils.hpp"
#include "slic3r/plugin/PluginManager.hpp"
#include "slic3r/plugin/PythonInterpreter.hpp"

#include <boost/dll/runtime_symbol_info.hpp>
#include <chrono>
#include <fstream>

using namespace Slic3r;
namespace fs = boost::filesystem;

namespace {
struct PluginRuntime
{
    ScopedDataDir data{"u1-bundled-plugin"};
    bool initialized = PluginManager::instance().initialize();
    ~PluginRuntime() { PluginManager::instance().shutdown(); }
};
} // namespace

TEST_CASE("Packaged U1 integration wheels install and register native script capabilities", "[U1Plugins][PluginLifecycle][Python]")
{
    const std::string package = GENERATE("u1_studio_plugin", "u1_bambu_converter_plugin");
    CAPTURE(package);
    PluginRuntime runtime;
    REQUIRE(runtime.initialized);
    const fs::path wheel = boost::dll::program_location().parent_path() / "u1_plugins" / (package + "-0.1.0-py3-none-any.whl");
    REQUIRE(fs::is_regular_file(wheel));

    PluginDescriptor descriptor;
    std::string error;
    REQUIRE(plugin_loader::install_plugin(wheel, "", descriptor, error));
    INFO(error);
    CHECK(error.empty());
    CHECK(descriptor.entry_package == package);

    auto& manager = PluginManager::instance();
    manager.discover_plugins(false, true);
    REQUIRE(manager.try_get_valid_plugin_descriptor(descriptor.plugin_key, descriptor));
    // Loading the entry registers a capability without importing lxml or contacting
    // anything. Real Studio inspection/dependencies are tested by the Python suite.
    manager.load_plugin(descriptor.plugin_key, true);
    REQUIRE(manager.wait_for_plugin_load(descriptor.plugin_key, std::chrono::seconds(60), error));
    INFO(error);
    REQUIRE(error.empty());
    REQUIRE(manager.is_plugin_loaded(descriptor.plugin_key));
    const auto capabilities = manager.get_plugin_capabilities(descriptor.plugin_key, PluginCapabilityType::Unknown, false);
    REQUIRE(capabilities.size() == 1);
    CHECK(capabilities.front()->type() == PluginCapabilityType::Script);
    CHECK(capabilities.front()->name() ==
          (package == "u1_studio_plugin" ? "Snapmaker Studio inspection" : "Bambu-to-U1 converter connector"));
    CHECK(manager.unload_plugin(descriptor.plugin_key));
}

TEST_CASE("Bundled U1 plugins become discoverable without loading or replacing user packages", "[U1Plugins][PluginInstall]")
{
    PluginRuntime runtime;
    REQUIRE(runtime.initialized);
    const fs::path bundled = boost::dll::program_location().parent_path() / "u1_plugins";
    std::string error;
    CHECK(plugin_loader::stage_bundled_plugins(bundled, {}, error) == 2);
    INFO(error);
    REQUIRE(error.empty());
    const auto discovered = discover_plugin_packages({runtime.data.plugins_dir().string()}, error);
    REQUIRE(error.empty());
    REQUIRE(discovered.size() == 2);
    for (const auto& descriptor : discovered) {
        CHECK_FALSE(PluginManager::instance().is_plugin_loaded(descriptor.plugin_key));
        PluginInstallState state;
        REQUIRE(read_install_state(fs::path(descriptor.plugin_root), state));
        CHECK_FALSE(state.enabled);
        const fs::path marker = fs::path(descriptor.plugin_root) / "user-customization.txt";
        std::ofstream(marker.string()) << "preserve this";
    }
    CHECK(plugin_loader::stage_bundled_plugins(bundled, discovered, error) == 0);
    REQUIRE(error.empty());
    for (const auto& descriptor : discovered) {
        std::ifstream stream((fs::path(descriptor.plugin_root) / "user-customization.txt").string());
        std::string line;
        std::getline(stream, line);
        CHECK(line == "preserve this");
    }
}
