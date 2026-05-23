package examples;

import org.springframework.web.bind.annotation.*;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;

@RestController
public class XmlBombExample {
    @PostMapping("/saml/consume")
    public String consume(@RequestBody byte[] xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        return factory.newDocumentBuilder()
            .parse(new ByteArrayInputStream(xml))
            .getDocumentElement()
            .getTextContent();
    }
}
