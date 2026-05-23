package examples;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.nio.file.*;

@RestController
public class FileUploadRceExample {
    @PostMapping("/avatar")
    public String upload(@RequestParam MultipartFile file) throws Exception {
        Path destination = Paths.get("public/uploads", file.getOriginalFilename());
        file.transferTo(destination);
        return "/uploads/" + file.getOriginalFilename();
    }
}
