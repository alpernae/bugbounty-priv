package examples;

import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletResponse;

@RestController
public class OpenRedirectExample {
    @GetMapping("/login/callback")
    public void callback(@RequestParam(defaultValue = "/dashboard") String next,
                         HttpServletResponse response) throws Exception {
        response.sendRedirect(next);
    }
}
