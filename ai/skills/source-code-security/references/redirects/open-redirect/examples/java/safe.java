package examples;

import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletResponse;
import java.util.Set;

@RestController
public class OpenRedirectExample {
    private static final Set<String> ALLOWED = Set.of("/dashboard", "/settings", "/billing");

    @GetMapping("/login/callback")
    public void callback(@RequestParam(defaultValue = "/dashboard") String next,
                         HttpServletResponse response) throws Exception {
        response.sendRedirect(ALLOWED.contains(next) ? next : "/dashboard");
    }
}
