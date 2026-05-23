package examples;

import javax.script.ScriptEngineManager;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
public class EvalCodeInjectionExample {
    @PostMapping("/rules/preview")
    public Map<String, Object> preview(@RequestBody Map<String, Object> body) throws Exception {
        String expression = String.valueOf(body.getOrDefault("expression", "false"));
        Object result = new ScriptEngineManager()
            .getEngineByName("JavaScript")
            .eval(expression);
        return Map.of("result", result);
    }
}
