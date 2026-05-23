package examples;

import org.springframework.web.bind.annotation.*;
import java.net.http.*;
import java.net.*;
import java.util.Set;

@RestController
public class BlindSsrfExample {
    private static final Set<String> ALLOWED_HOSTS = Set.of("api.partner.example", "images.example-cdn.com");
    private final HttpClient client = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NEVER).build();

    @GetMapping("/fetch-preview")
    public int fetch(@RequestParam String url) throws Exception {
        URI uri = URI.create(url);
        if (!"https".equals(uri.getScheme()) || !ALLOWED_HOSTS.contains(uri.getHost())) {
            throw new IllegalArgumentException("blocked upstream");
        }
        HttpRequest request = HttpRequest.newBuilder(uri).GET().build();
        return client.send(request, HttpResponse.BodyHandlers.discarding()).statusCode();
    }
}
