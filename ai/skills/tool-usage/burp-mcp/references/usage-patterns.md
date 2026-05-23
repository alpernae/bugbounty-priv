# Usage Patterns

## Verify setup first
- Confirm the Burp MCP extension is enabled.
- Confirm the SSE endpoint is reachable on `127.0.0.1:9876` or `127.0.0.1:9876/sse`.
- Confirm whether config-editing tools are enabled in Burp.

## Common task groups
- Replay / single request: `send_http1_request`, `send_http2_request`
- Send to Burp UI tools: `create_repeater_tab`, `send_to_intruder`
- History: `get_proxy_http_history`, `get_proxy_http_history_regex`, `get_proxy_websocket_history`, `get_proxy_websocket_history_regex`
- Collaborator: `generate_collaborator_payload`, `get_collaborator_interactions`
- Runtime toggles: `set_proxy_intercept_state`, `set_task_execution_engine_state`
- Encoders/helpers: `url_encode`, `url_decode`, `base64_encode`, `base64_decode`, `generate_random_string`

## Guardrails
- Do not assume a tool exists; confirm against the live MCP listing if available.
- History and config tools can be denied by Burp-side policy.
