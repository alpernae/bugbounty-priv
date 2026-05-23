package examples;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@RestController
public class ZipSlipExample {
    private static final Path IMPORT_ROOT = Path.of("var/imports");

    @PostMapping("/import")
    public void importTheme(MultipartFile archive) throws Exception {
        try (InputStream input = archive.getInputStream();
             ZipInputStream zip = new ZipInputStream(input)) {
            ZipEntry entry;
            while ((entry = zip.getNextEntry()) != null) {
                Path target = IMPORT_ROOT.resolve(entry.getName());
                if (!entry.isDirectory()) {
                    Files.createDirectories(target.getParent());
                    Files.copy(zip, target);
                }
            }
        }
    }
}
