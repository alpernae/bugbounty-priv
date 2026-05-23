package examples;

import java.sql.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class SqlInjectionExample {
    private final Connection connection;

    public SqlInjectionExample(Connection connection) {
        this.connection = connection;
    }

    @GetMapping("/invoices")
    public String invoices(@RequestParam(defaultValue = "open") String status) throws Exception {
        PreparedStatement ps = connection.prepareStatement(
            "SELECT id,total,status FROM invoices WHERE status = ?"
        );
        ps.setString(1, status);
        ResultSet rs = ps.executeQuery();
        return JsonUtil.toJson(rs);
    }
}
