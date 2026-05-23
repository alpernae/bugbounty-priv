package examples;

import org.springframework.web.bind.annotation.*;
import java.net.*;
import java.io.*;

@RestController
public class CommandInjectionExample {
    @GetMapping("/tools/ping")
    public String ping(@RequestParam String host) throws Exception {
        InetAddress address = InetAddress.getByName(host);
        if (address.isAnyLocalAddress() || address.isLoopbackAddress()) {
            throw new IllegalArgumentException("blocked host");
        }
        Process process = new ProcessBuilder("ping", "-c", "1", address.getHostAddress()).start();
        return new String(process.getInputStream().readAllBytes());
    }
}
