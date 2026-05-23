package examples;

import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletRequest;

@RestController
public class CachePoisoningExample {
    @GetMapping("/profile")
    public String profile(HttpServletRequest request, User user) {
        String host = request.getHeader("X-Forwarded-Host");
        return "<link rel='canonical' href='https://" + host + "/profile'><h1>" + user.email() + "</h1>";
    }
}
