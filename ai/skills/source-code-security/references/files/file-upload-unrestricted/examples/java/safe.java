package examples;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.nio.file.*;
import java.util.*;

@RestController
public class FileUploadUnrestrictedExample {
    private static final Set<String> ALLOWED = Set.of("image/png", "image/jpeg");

    @PostMapping("/avatar")
    public Map<String, String> upload(@RequestParam MultipartFile file) throws Exception {
        if (!ALLOWED.contains(file.getContentType())) throw new IllegalArgumentException("bad type");
        String id = UUID.randomUUID().toString() + ".bin";
        Path destination = Paths.get("var/uploads", id).normalize();
        file.transferTo(destination);
        return Map.of("fileId", id);
    }
}
