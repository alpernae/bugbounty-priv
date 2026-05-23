package examples;

import java.security.SecureRandom;
import java.util.Base64;

public class InsecureRandomnessExample {
    private final SecureRandom random = new SecureRandom();

    public String resetToken(String userId) {
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        return userId + "." + System.currentTimeMillis() + "." + Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}
