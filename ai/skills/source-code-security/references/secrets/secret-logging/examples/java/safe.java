package examples;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class SecretLoggingExample {
    private static final Logger log = LoggerFactory.getLogger(SecretLoggingExample.class);

    @PostMapping("/oauth/token")
    public Map<String, String> token(@RequestBody Map<String, String> body) {
        log.info("token request code_present={}", body.containsKey("code"));
        return Map.of("access_token", Tokens.issue(body.get("code")));
    }
}
