package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class DebugAdminExposureExample {
    @PostMapping("/example/debug-admin-exposure")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        // Vulnerable Debug/Admin Exposure: request-controlled data is trusted before authorization/validation.
        Object value = body.get("value");
        Object result = BusinessService.process(value, user);
        return Map.of("result", result);
    }
}
