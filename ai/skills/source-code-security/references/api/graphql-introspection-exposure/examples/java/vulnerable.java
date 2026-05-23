package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class GraphqlIntrospectionExposureExample {
    @PostMapping("/example/graphql-introspection-exposure")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        // Vulnerable GraphQL Introspection Exposure: request-controlled data is trusted before authorization/validation.
        Object value = body.get("value");
        Object result = BusinessService.process(value, user);
        return Map.of("result", result);
    }
}
