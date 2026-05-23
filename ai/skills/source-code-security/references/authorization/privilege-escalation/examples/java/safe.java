package examples;

import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
public class PrivilegeEscalationExample {
    private final InvoiceRepository invoices;

    @GetMapping("/api/invoices/{id}")
    public Invoice getInvoice(@PathVariable String id, @AuthenticationPrincipal User user) {
        return invoices.findByIdAndOrganizationId(id, user.organizationId()).orElseThrow();
    }
}
