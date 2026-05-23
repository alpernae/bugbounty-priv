package examples;

import org.springframework.web.bind.annotation.*;

@RestController
public class MassAssignmentExample {
    record ProfileUpdate(String displayName, String avatarUrl) {}
    private final UserRepository users;

    @PatchMapping("/profile")
    public User update(@RequestBody ProfileUpdate body, User currentUser) {
        User user = users.findById(currentUser.getId()).orElseThrow();
        user.setDisplayName(body.displayName());
        user.setAvatarUrl(body.avatarUrl());
        return users.save(user);
    }
}
