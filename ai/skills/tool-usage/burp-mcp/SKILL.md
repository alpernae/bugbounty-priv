---
name: burp-mcp
description: Use Burp Suite via the PortSwigger MCP server (setup + verification + tool list + usage patterns).
---

# Burp MCP

## Scope
Use this skill when you need to drive Burp Suite through the PortSwigger MCP server extension (SSE server + optional stdio proxy).

## Preconditions (Burp side)
1. Load the extension JAR into Burp Suite.
2. In Burp, open the `MCP` tab and configure:
   - `Enabled`: on
   - Host/port: defaults to `http://127.0.0.1:9876`
   - Optional: enable config-editing tools (this gates config mutation tools)
3. If your MCP client only supports stdio, use the packaged proxy jar that forwards to the SSE URL.

Read first: `references/portswigger-mcp-server-README.md`.

## Verify Connectivity
Before assuming tools work, verify the server is reachable.

Depending on the client and your Burp config, the SSE endpoint may be either:
- `http://127.0.0.1:9876`
- `http://127.0.0.1:9876/sse`

## Tool Discovery Rule (Important)
Do not assume tool names.

Tools registered as `mcpTool<T>` / `mcpPaginatedTool<T>` have names auto-derived from their Kotlin `data class` name.

Use one of:
1. List tools from your MCP client (preferred; source of truth).
2. Consult the locally-generated snapshot: `references/burp-mcp-tools.md` (generated from `Tools.kt`).

## Common Workflows
### Replay / craft requests
- `send_http1_request`: One-off HTTP/1.1 request/response round-trip.
- `send_http2_request`: One-off HTTP/2 request/response round-trip (pseudo headers + headers + body).
- `create_repeater_tab`: Send an HTTP/1.1 request into Repeater (use CRLF correctly).
- `send_to_intruder`: Send an HTTP/1.1 request into Intruder (use CRLF correctly).

### Proxy history triage
- `get_proxy_http_history` / `get_proxy_http_history_regex`
- `get_proxy_websocket_history` / `get_proxy_websocket_history_regex`

### Burp runtime toggles
- `set_proxy_intercept_state`: Enable/disable Proxy Intercept.
- `set_task_execution_engine_state`: Pause/unpause Burp's task execution engine.

### Active editor
- `get_active_editor_contents`: Read the currently-focused message editor contents.
- `set_active_editor_contents`: Set editor contents (only works if current editor is editable).

### Scanner / Collaborator (Professional edition only)
- `get_scanner_issues`: Enumerate scanner issues.
- `generate_collaborator_payload`: Create a Collaborator payload (optionally with custom data).
- `get_collaborator_interactions`: Poll for interactions (optionally filtered by payloadId).

### Encoding helpers
- `url_encode`, `url_decode`
- `base64_encode`, `base64_decode`
- `generate_random_string`

### Options export / import
- `output_project_options`, `output_user_options`
- `set_project_options`, `set_user_options` (gated by the extension config toggle)

## Guardrails / Common Denials
- HTTP requests may be denied by Burp's MCP HTTP permission checks (target host/port + request content).
- History access may be denied by Burp's MCP history-access controls.
- Config mutation tools are disabled unless the user enables them in the Burp MCP tab.

## References
- `references/portswigger-mcp-server-README.md`
- `references/burp-mcp-tools.md`
