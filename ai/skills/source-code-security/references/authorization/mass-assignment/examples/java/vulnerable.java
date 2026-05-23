package examples;

import org.springframework.web.bind.annotation.*;

@RestController
public class MassAssignmentExample {
    private final UserRepository users;

    @PatchMapping("/profile")
    public User update(@RequestBody User incoming, User currentUser) {
        incoming.setId(currentUser.getId());
        return users.save(incoming);
    }
}
