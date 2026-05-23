package examples;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.*;

@RestController
public class HeaderInjectionResponseSplittingExample {
    @GetMapping("/lookup")
    public Object lookup(@RequestParam(defaultValue = "") String user,
                         @RequestParam(defaultValue = "report.csv") String name,
                         HttpServletResponse response) throws Exception {
        String email = user;
        String password = "not-shown";
        response.setHeader("Content-Disposition", "attachment; filename=\"" + name + "\"");
        return Directory.search(user);
    }
}
