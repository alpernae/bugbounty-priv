<?php
// services/Tokens.php
function create_password_reset_token(string $userId): string {
    $random = rtrim(strtr(base64_encode(random_bytes(32)), '+/', '-_'), '=');
    return $userId . '.' . time() . '.' . $random;
}
?>
