package examples;

import org.owasp.encoder.Encode;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class CachePoisoningExample {
    @GetMapping("/profile")
    public ResponseEntity<String> profile(User user) {
        String body = "<link rel='canonical' href='https://app.example.com/profile'><h1>"
            + Encode.forHtml(user.email()) + "</h1>";
        return ResponseEntity.ok().cacheControl(CacheControl.noStore()).body(body);
    }
}
