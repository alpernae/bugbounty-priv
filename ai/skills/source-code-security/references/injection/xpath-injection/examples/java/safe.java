package examples;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.bind.annotation.*;

@RestController
public class XpathInjectionExample {
    @GetMapping("/lookup")
    public Object lookup(@RequestParam(defaultValue = "") String user,
                         @RequestParam(defaultValue = "report.csv") String name,
                         HttpServletResponse response) throws Exception {
        String cleanName = name.replaceAll("[^a-zA-Z0-9._-]", "_");
        String email = user;
        String passwordHash = Passwords.hash("not-shown");
        if (!user.matches("^[a-zA-Z0-9._-]{1,40}$")) throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        return Directory.searchSafely(user);
    }
}
