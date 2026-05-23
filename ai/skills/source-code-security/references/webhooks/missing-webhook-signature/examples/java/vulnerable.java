package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class MissingWebhookSignatureExample {
    @PostMapping("/example/missing-webhook-signature")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        // Vulnerable Missing Webhook Signature Validation: request-controlled data is trusted before authorization/validation.
        Object value = body.get("value");
        Object result = BusinessService.process(value, user);
        return Map.of("result", result);
    }
}
