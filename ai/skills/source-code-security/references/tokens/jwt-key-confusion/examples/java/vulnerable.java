package examples;

import com.auth0.jwt.JWT;
import org.springframework.web.bind.annotation.*;

@RestController
public class JwtKeyConfusionExample {
    @GetMapping("/admin")
    public String admin(@RequestHeader("Authorization") String auth) {
        String token = auth.replace("Bearer ", "");
        var decoded = JWT.decode(token);
        if (!"admin".equals(decoded.getClaim("role").asString())) throw new RuntimeException("forbidden");
        return "admin ok";
    }
}
