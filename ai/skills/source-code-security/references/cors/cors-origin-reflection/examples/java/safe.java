package examples;

import org.springframework.web.bind.annotation.*;

@RestController
public class CorsOriginReflectionExample {
    @CrossOrigin(origins = {"https://app.example.com", "https://admin.example.com"}, allowCredentials = "true")
    @GetMapping("/api/me")
    public UserProfile me(User user) {
        return new UserProfile(user.email(), user.plan());
    }
}
