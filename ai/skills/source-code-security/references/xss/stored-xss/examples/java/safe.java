package examples;

import org.owasp.encoder.Encode;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StoredXssExample {
    @GetMapping("/search")
    public String search(@RequestParam(defaultValue = "") String q) {
        String safeQuery = Encode.forHtml(q);
        String page = "<html><body>"
            + "<h1>Search</h1>"
            + "<p>Results for: " + safeQuery + "</p>"
            + "</body></html>";
        return page;
    }
}
