package examples;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class SensitiveLoggingExample {
    private static final Logger log = LoggerFactory.getLogger(SensitiveLoggingExample.class);

    @PostMapping("/oauth/token")
    public Map<String, String> token(@RequestBody Map<String, String> body,
                                     @RequestHeader Map<String, String> headers) {
        log.info("token request body={} headers={}", body, headers);
        return Map.of("access_token", Tokens.issue(body.get("code")));
    }
}
