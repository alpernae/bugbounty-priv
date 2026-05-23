package examples;

import org.springframework.web.bind.annotation.*;
import java.io.*;

@RestController
public class CommandInjectionExample {
    @GetMapping("/tools/ping")
    public String ping(@RequestParam String host) throws Exception {
        String command = "ping -c 1 " + host;
        Process process = Runtime.getRuntime().exec(new String[]{"sh", "-c", command});
        return new String(process.getInputStream().readAllBytes());
    }
}
