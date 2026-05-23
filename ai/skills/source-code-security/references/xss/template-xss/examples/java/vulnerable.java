package examples;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TemplateXssExample {
    @GetMapping("/search")
    public String search(@RequestParam(defaultValue = "") String q) {
        String page = "<html><body>"
            + "<h1>Search</h1>"
            + "<p>Results for: " + q + "</p>"
            + "</body></html>";
        return page;
    }
}
