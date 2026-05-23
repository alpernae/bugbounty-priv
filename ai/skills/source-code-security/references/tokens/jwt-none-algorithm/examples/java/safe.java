package examples;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import org.springframework.web.bind.annotation.*;

@RestController
public class JwtNoneAlgorithmExample {
    private final Algorithm algorithm = Algorithm.RSA256(Keys.publicKey(), null);

    @GetMapping("/admin")
    public String admin(@RequestHeader("Authorization") String auth) {
        String token = auth.replace("Bearer ", "");
        var verifier = JWT.require(algorithm)
            .withIssuer("https://auth.example.com")
            .withAudience("example-api")
            .build();
        var decoded = verifier.verify(token);
        if (!"admin".equals(decoded.getClaim("role").asString())) throw new RuntimeException("forbidden");
        return "admin ok";
    }
}
