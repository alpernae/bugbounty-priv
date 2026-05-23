package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class DependencyConfusionExample {
    @PostMapping("/example/dependency-confusion")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        // Vulnerable Dependency Confusion: request-controlled data is trusted before authorization/validation.
        Object value = body.get("value");
        Object result = BusinessService.process(value, user);
        return Map.of("result", result);
    }
}
