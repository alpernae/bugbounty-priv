package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class WebsocketAuthzExample {
    @PostMapping("/example/websocket-authz")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        // Vulnerable WebSocket Authorization Bypass: request-controlled data is trusted before authorization/validation.
        Object value = body.get("value");
        Object result = BusinessService.process(value, user);
        return Map.of("result", result);
    }
}
