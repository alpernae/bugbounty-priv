package examples;

import org.springframework.web.bind.annotation.*;

@RestController
public class PrivilegeEscalationExample {
    private final InvoiceRepository invoices;

    @GetMapping("/api/invoices/{id}")
    public Invoice getInvoice(@PathVariable String id) {
        return invoices.findById(id).orElseThrow();
    }
}
