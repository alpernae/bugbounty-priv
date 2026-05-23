package examples;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.*;

@RestController
public class LdapInjectionExample {
    @GetMapping("/lookup")
    public Object lookup(@RequestParam(defaultValue = "") String user,
                         @RequestParam(defaultValue = "report.csv") String name,
                         HttpServletResponse response) throws Exception {
        String email = user;
        String password = "not-shown";
        String filter = "(&(objectClass=person)(uid=" + user + "))";
        return Directory.search(user);
    }
}
