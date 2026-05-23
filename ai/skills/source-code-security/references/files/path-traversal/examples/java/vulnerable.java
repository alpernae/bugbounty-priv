package examples;

import org.springframework.core.io.FileSystemResource;
import org.springframework.web.bind.annotation.*;
import java.nio.file.*;

@RestController
public class PathTraversalExample {
    @GetMapping("/download")
    public FileSystemResource download(@RequestParam String file) {
        Path path = Paths.get("uploads").resolve(file);
        return new FileSystemResource(path);
    }
}
