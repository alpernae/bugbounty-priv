package examples;

import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.Set;

@RestController
public class MissingWebhookSignatureExample {
    private static final Set<String> ALLOWED_FIELDS = Set.of("displayName", "avatarUrl");

    @PostMapping("/example/missing-webhook-signature")
    public Map<String, Object> handle(@RequestBody Map<String, Object> body, User user) {
        Authz.requireActiveUser(user);
        Map<String, Object> clean = Validators.pick(body, ALLOWED_FIELDS);
        Object result = BusinessService.process(clean, user);
        return Map.of("result", result);
    }
}
