#include <catch2/catch_test_macros.hpp>
#include "slic3r/GUI/Mcp/McpProtocol.hpp"
#include "slic3r/GUI/Mcp/McpTypes.hpp"

#include <string>

using namespace Slic3r::GUI::Mcp;
using nlohmann::json;

namespace {
class RejectCaller final : public ToolCaller
{
public:
    ToolResult call(const ToolDef&, const json&) override { return ToolResult::error("must not execute"); }
};
} // namespace

TEST_CASE("Malformed RPC field types are refused without throwing", "[U1McpProtocol]")
{
    ToolRegistry registry;
    RejectCaller caller;
    McpProtocol protocol(registry, caller, ServerInfo{});
    for (const auto& body : {R"({"jsonrpc":4,"method":"ping","id":1})", R"({"jsonrpc":"2.0","method":7,"id":1})",
                             R"({"jsonrpc":"2.0","method":null,"id":1})", R"({"method":"ping","id":1})"}) {
        PostReply reply;
        REQUIRE_NOTHROW(reply = protocol.handle_post({body, "", "", ""}));
        CHECK(reply.status == 400);
        CHECK(json::parse(reply.body)["error"]["code"] == -32600);
    }
}

TEST_CASE("The official protocol negotiates legacy clients and serves the current revision", "[U1McpProtocol]")
{
    ToolRegistry registry;
    RejectCaller caller;
    McpProtocol protocol(registry, caller, ServerInfo{});
    const auto handshake = protocol.handle_post(
        {R"({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25"}})", "", "", ""});
    CHECK(json::parse(handshake.body)["result"]["protocolVersion"] == "2025-11-25");
    const auto current = protocol.handle_post(
        {R"({"jsonrpc":"2.0","id":2,"method":"ping","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28"}}})",
         "2026-07-28", "ping", ""});
    CHECK(current.status == 200);
    CHECK_FALSE(json::parse(current.body).contains("error"));
}

TEST_CASE("Integer schema validation handles extreme floating point values", "[U1McpProtocol]")
{
    const json schema = {{"type", "object"},
                         {"properties", {{"index", {{"type", "integer"}}}}},
                         {"required", {"index"}},
                         {"additionalProperties", false}};
    CHECK_FALSE(validate_arguments(schema, {{"index", 1e300}}).empty());
    CHECK_FALSE(validate_arguments(schema, {{"index", 1.5}}).empty());
    CHECK(validate_arguments(schema, {{"index", 2.0}}).empty());
    CHECK_FALSE(validate_arguments(schema, {{"index", 1}, {"printer_macro", "G28"}}).empty());
}

TEST_CASE("U1 MCP blocks action and plugin escape hatches even when annotated read only", "[U1McpProtocol]")
{
    ToolRegistry registry;
    RejectCaller caller;
    for (const char* name : {"get_state", "run_action", "ui_click", "run_python", "api_call", "start_print"}) {
        ToolDef def;
        def.name      = name;
        def.read_only = true; // A plugin's claim is not an authorization boundary.
        registry.add(def);
    }
    ServerInfo info;
    info.slicer_only = true;
    McpProtocol protocol(registry, caller, info);
    const auto listing = protocol.handle_post({R"({"jsonrpc":"2.0","id":1,"method":"tools/list"})", "", "", ""});
    const auto tools   = json::parse(listing.body)["result"]["tools"];
    REQUIRE(tools.size() == 1);
    CHECK(tools[0]["name"] == "get_state");
    for (const char* name : {"run_action", "ui_click", "run_python", "api_call", "start_print"}) {
        const auto body = json{{"jsonrpc", "2.0"},
                               {"id", 2},
                               {"method", "tools/call"},
                               {"params", {{"name", name}, {"arguments", json::object()}}}}
                              .dump();
        const auto reply = protocol.handle_post({body, "", "", ""});
        CHECK(json::parse(reply.body)["result"]["isError"] == true);
        const std::string message = json::parse(reply.body)["result"]["content"][0]["text"];
        CHECK(message.find("approval adapter") != std::string::npos);
    }
}
