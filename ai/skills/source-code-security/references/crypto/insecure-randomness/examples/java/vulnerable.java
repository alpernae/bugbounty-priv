package examples;

import java.util.Random;

public class InsecureRandomnessExample {
    private final Random random = new Random();

    public String resetToken(String userId) {
        int suffix = random.nextInt(1_000_000);
        return userId + "." + System.currentTimeMillis() + "." + suffix;
    }
}
