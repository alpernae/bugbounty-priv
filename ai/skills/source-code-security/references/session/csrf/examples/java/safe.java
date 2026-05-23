package examples;

import jakarta.servlet.http.*;
import org.springframework.web.bind.annotation.*;

@RestController
public class CsrfExample {
    @PostMapping("/login")
    public void login(HttpServletRequest request, HttpServletResponse response) {
        User user = Auth.authenticate(request.getParameter("email"), request.getParameter("password"));
        request.changeSessionId();
        request.getSession().setAttribute("userId", user.id());

        Cookie cookie = new Cookie("sid", request.getSession().getId());
        cookie.setHttpOnly(true);
        cookie.setSecure(true);
        cookie.setPath("/");
        response.addCookie(cookie);
    }
}
