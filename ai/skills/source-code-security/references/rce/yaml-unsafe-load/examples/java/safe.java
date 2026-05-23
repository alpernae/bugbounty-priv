package examples;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.bind.annotation.*;
import java.util.Base64;

@RestController
public class YamlUnsafeLoadExample {
    record SessionState(String userId, String theme) {}
    private final ObjectMapper mapper = new ObjectMapper();

    @GetMapping("/session/restore")
    public SessionState restore(@RequestParam String state) throws Exception {
        byte[] data = Base64.getDecoder().decode(state);
        SessionState session = mapper.readValue(data, SessionState.class);
        if (session.userId() == null) throw new IllegalArgumentException("invalid session");
        return session;
    }
}
