package examples;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
public class EvalCodeInjectionExample {
    private static final Set<String> ALLOWED_FIELDS = Set.of("total");

    @PostMapping("/rules/preview")
    public Map<String, Object> preview(@RequestBody Map<String, Object> body) {
        String field = String.valueOf(body.getOrDefault("field", ""));
        double min = Double.parseDouble(String.valueOf(body.getOrDefault("min", "0")));
        double total = Double.parseDouble(String.valueOf(body.getOrDefault("total", "0")));

        if (!ALLOWED_FIELDS.contains(field)) throw new IllegalArgumentException("bad field");
        return Map.of("result", total > min);
    }
}
