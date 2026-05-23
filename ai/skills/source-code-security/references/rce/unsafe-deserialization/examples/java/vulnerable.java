package examples;

import org.springframework.web.bind.annotation.*;
import java.io.*;
import java.util.Base64;

@RestController
public class UnsafeDeserializationExample {
    @GetMapping("/session/restore")
    public Object restore(@RequestParam String state) throws Exception {
        byte[] data = Base64.getDecoder().decode(state);
        ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(data));
        return in.readObject();
    }
}
