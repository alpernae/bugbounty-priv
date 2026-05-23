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
        String sql = "SELECT id,total,status FROM invoices WHERE status = '" + status + "'";
        Statement statement = connection.createStatement();
        ResultSet rs = statement.executeQuery(sql);
        return JsonUtil.toJson(rs);
    }
}
