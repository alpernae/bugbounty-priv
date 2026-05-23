package examples;

import org.springframework.core.io.FileSystemResource;
import org.springframework.web.bind.annotation.*;
import java.nio.file.*;

@RestController
public class ArbitraryFileReadExample {
    private static final Path ROOT = Paths.get("uploads").toAbsolutePath().normalize();

    @GetMapping("/download")
    public FileSystemResource download(@RequestParam String file) {
        Path path = ROOT.resolve(Paths.get(file).getFileName()).normalize();
        if (!path.startsWith(ROOT)) throw new IllegalArgumentException("invalid file");
        return new FileSystemResource(path);
    }
}
