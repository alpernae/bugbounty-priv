package examples;

import jakarta.servlet.http.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class InsecureCookieExample {
    @PostMapping("/login")
    public void login(HttpServletRequest request, HttpServletResponse response) {
        User user = Auth.authenticate(request.getParameter("email"), request.getParameter("password"));
        request.getSession().setAttribute("userId", user.id());
        response.addCookie(new Cookie("sid", request.getSession().getId()));
    }
}
