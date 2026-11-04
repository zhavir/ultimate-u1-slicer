#pragma once

#include <filesystem>
#include <string>
#include <system_error>
#include <utility>
#include <vector>

namespace Slic3r { namespace GUI { namespace Mcp {

// Operator-owned roots, independent of MCP arguments. Canonical component comparisons reject
// sibling-prefix matches, traversal and symlink escapes. Does not protect against another local
// process replacing a path between authorization and opening it.
class FileAccessPolicy
{
public:
    explicit FileAccessPolicy(std::vector<std::filesystem::path> roots) : m_roots(std::move(roots)) {}

    bool permits(const std::filesystem::path& path, std::string& error) const
    {
        namespace fs = std::filesystem;
        error.clear();
        if (!path.is_absolute()) {
            error = "MCP file paths must be absolute";
            return false;
        }
        for (const auto& component : path)
            if (component == "..") {
                error = "MCP file paths must not contain parent traversal";
                return false;
            }
        std::error_code ec;
        const fs::path resolved = fs::weakly_canonical(path, ec);
        if (ec) {
            error = "Cannot resolve MCP file path";
            return false;
        }
        for (const fs::path& root : m_roots) {
            if (!root.is_absolute() || !fs::is_directory(root, ec) || ec)
                continue;
            const fs::path canonical_root = fs::canonical(root, ec);
            if (ec)
                continue;
            auto component = resolved.begin();
            auto parent    = canonical_root.begin();
            while (parent != canonical_root.end() && component != resolved.end() && *parent == *component) {
                ++parent;
                ++component;
            }
            if (parent == canonical_root.end())
                return true;
        }
        error = "MCP file access denied: authorize its directory with U1_MCP_ALLOWED_ROOTS before launching Ultimate U1";
        return false;
    }

private:
    std::vector<std::filesystem::path> m_roots;
};

}}} // namespace Slic3r::GUI::Mcp
