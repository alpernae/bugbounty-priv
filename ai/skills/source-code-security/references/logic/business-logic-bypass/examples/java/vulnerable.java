package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class BusinessLogicBypassExample {
    @PostMapping("/example/business-logic-bypass")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        // Vulnerable Business Logic Bypass: request-controlled data is trusted before authorization/validation.
        Object value = body.get("value");
        Object result = BusinessService.process(value, user);
        return Map.of("result", result);
    }
}
