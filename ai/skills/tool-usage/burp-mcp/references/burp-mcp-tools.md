# Burp MCP Tools (From Tools.kt)
Source snapshot: `portswigger-mcp-server-Tools.kt` (saved locally).
NOTE: Tool names for `mcpTool<...>` / `mcpPaginatedTool<...>` are auto-derived from the data class name. The exact derivation is implemented by the extension; confirm by listing tools from the live MCP server when in doubt.
## Explicit Tool Names
- `output_project_options` (no params)
- `output_user_options` (no params)
- `get_active_editor_contents` (no params)
## Auto-Derived Tools (mcpTool<T>)
- `send_http_1_request` (class `SendHttp1Request`): content: String, targetHostname: String, targetPort: Int, usesHttps: Boolean
- `send_http_2_request` (class `SendHttp2Request`): pseudoHeaders: Map<String, String>, headers: Map<String, String>, requestBody: String, targetHostname: String, targetPort: Int, usesHttps: Boolean
- `create_repeater_tab` (class `CreateRepeaterTab`): tabName: String?, content: String, targetHostname: String, targetPort: Int, usesHttps: Boolean
- `send_to_intruder` (class `SendToIntruder`): tabName: String?, content: String, targetHostname: String, targetPort: Int, usesHttps: Boolean
- `url_encode` (class `UrlEncode`): content: String
- `url_decode` (class `UrlDecode`): content: String
- `base_64_encode` (class `Base64Encode`): content: String
- `base_64_decode` (class `Base64Decode`): content: String
- `generate_random_string` (class `GenerateRandomString`): length: Int, val characterSet: String
- `set_project_options` (class `SetProjectOptions`): json: String
- `set_user_options` (class `SetUserOptions`): json: String
- `generate_collaborator_payload` (class `GenerateCollaboratorPayload`): customData: String?
- `get_collaborator_interactions` (class `GetCollaboratorInteractions`): payloadId: String?
- `set_task_execution_engine_state` (class `SetTaskExecutionEngineState`): running: Boolean
- `set_proxy_intercept_state` (class `SetProxyInterceptState`): intercepting: Boolean
- `set_active_editor_contents` (class `SetActiveEditorContents`): text: String

## Auto-Derived Paginated Tools (mcpPaginatedTool<T>)
- `get_scanner_issues` (class `GetScannerIssues`): count: Int, override val offset: Int
- `get_proxy_http_history` (class `GetProxyHttpHistory`): count: Int, override val offset: Int
- `get_proxy_http_history_regex` (class `GetProxyHttpHistoryRegex`): regex: String, override val count: Int, override val offset: Int
- `get_proxy_websocket_history` (class `GetProxyWebsocketHistory`): count: Int, override val offset: Int
- `get_proxy_websocket_history_regex` (class `GetProxyWebsocketHistoryRegex`): regex: String, override val count: Int, override val offset: Int
