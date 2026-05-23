package examples;

import org.springframework.web.bind.annotation.*;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;

@RestController
public class XxeExample {
    @PostMapping("/saml/consume")
    public String consume(@RequestBody byte[] xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setExpandEntityReferences(true);
        return factory.newDocumentBuilder()
            .parse(new ByteArrayInputStream(xml))
            .getDocumentElement()
            .getTextContent();
    }
}
