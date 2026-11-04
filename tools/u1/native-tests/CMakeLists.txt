cmake_minimum_required(VERSION 3.16)
project(UltimateU1ComponentTests LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
get_filename_component(U1_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)
enable_testing()
add_subdirectory("${U1_ROOT}/tests/catch2" "${CMAKE_CURRENT_BINARY_DIR}/catch2" EXCLUDE_FROM_ALL)
add_executable(u1_component_tests
    "${U1_ROOT}/src/slic3r/GUI/Mcp/McpProtocol.cpp"
    "${U1_ROOT}/src/libslic3r/FosFilamentArrangement.cpp"
    "${U1_ROOT}/src/libslic3r/U1FilamentPlan.cpp"
    "${U1_ROOT}/tests/slic3rutils/test_u1_mcp_protocol.cpp"
    "${U1_ROOT}/tests/slic3rutils/test_mcp_file_policy.cpp"
    "${U1_ROOT}/tests/libslic3r/test_u1_filament_plan.cpp")
target_include_directories(u1_component_tests PRIVATE "${U1_ROOT}/src" "${U1_ROOT}/deps_src")
target_link_libraries(u1_component_tests PRIVATE Catch2::Catch2WithMain)
option(U1_ENABLE_SANITIZERS "Instrument the native component target with undefined-behavior checks" OFF)
if(U1_ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang" AND NOT MSVC)
    target_compile_options(u1_component_tests PRIVATE -fsanitize=undefined,float-cast-overflow -fno-sanitize-recover=all)
    target_link_options(u1_component_tests PRIVATE -fsanitize=undefined,float-cast-overflow)
endif()
if(MSVC)
    target_compile_options(u1_component_tests PRIVATE /W4)
else()
    target_compile_options(u1_component_tests PRIVATE -Wall -Wextra -Wpedantic)
endif()
add_test(NAME u1_component_tests COMMAND u1_component_tests)

option(U1_ENABLE_HTTP_TESTS "Build the unchanged upstream MCP HTTP tests when Boost is available" OFF)
if(U1_ENABLE_HTTP_TESTS)
    find_package(Boost 1.83 REQUIRED CONFIG COMPONENTS headers)
    find_package(Threads REQUIRED)
    add_executable(u1_mcp_http_tests
        "${U1_ROOT}/src/slic3r/GUI/Mcp/McpHttpServer.cpp"
        "${U1_ROOT}/tests/slic3rutils/test_mcp_http.cpp")
    target_include_directories(u1_mcp_http_tests PRIVATE "${U1_ROOT}/src" "${U1_ROOT}/deps_src")
    target_link_libraries(u1_mcp_http_tests PRIVATE Boost::headers Catch2::Catch2WithMain Threads::Threads)
    if(WIN32)
        target_link_libraries(u1_mcp_http_tests PRIVATE ws2_32 mswsock)
    endif()
    add_test(NAME u1_mcp_http_tests COMMAND u1_mcp_http_tests)
endif()
