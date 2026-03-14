# Agent Rules: GitHub Operations

## G-001: GitHub MCP Priority

### Objective

Ensure consistency, efficiency, and reliability in GitHub interactions by prioritizing the use of the GitHub MCP server tools over external CLI commands (`gh`).

### Rule Definition

1. **MCP First**: For any GitHub-related action (listing/searching/reading/writing issues, pull requests, files, branches, commits, or repository metadata), the agent **MUST** use the corresponding `github-mcp-server` tool.
2. **Fallback Strategy**: The `gh` CLI (via `run_command`) should **ONLY** be used in the following scenarios:
    - The `github-mcp-server` is unavailable or fails to connect.
    - The specific action required is not supported by the MCP tools (e.g., complex repository configuration, certain audit logs, or specific extensions).
    - An MCP operation fails repeatedly but the same operation is known to be possible via `gh` CLI.
3. **Verification**: After performing a GitHub operation, verify the result using MCP tools (e.g., use `pull_request_read` after `create_pull_request`) unless the tool output itself provides sufficient confirmation.

### Motivation

- **Rate Limiting**: MCP tools often have handled rate limiting or use optimized authentication.
- **Context Awareness**: MCP tools return structured JSON data that is easier for the agent to parse than CLI string output.
- **Reliability**: MCP tools are purpose-built for agentic interactions with the GitHub API.

### Examples

#### Example 1: Creating a Pull Request

- **Preferred**: `mcp_github-mcp-server_create_pull_request`
- **Fallback**: `gh pr create --title "..." --body "..."`

#### Example 2: Checking Issue Status

- **Preferred**: `mcp_github-mcp-server_issue_read`
- **Fallback**: `gh issue view <number>`
