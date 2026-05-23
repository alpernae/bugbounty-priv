package examples;

import org.springframework.web.bind.annotation.*;
import java.net.http.*;
import java.net.URI;

@RestController
public class BlindSsrfExample {
    private final HttpClient client = HttpClient.newHttpClient();

    @GetMapping("/fetch-preview")
    public String fetch(@RequestParam String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url)).GET().build();
        return client.send(request, HttpResponse.BodyHandlers.ofString()).body();
    }
}
