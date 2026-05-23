<?php
// services/Tokens.php
function create_password_reset_token(string $userId): string {
    $suffix = str_pad((string)mt_rand(0, 999999), 6, '0', STR_PAD_LEFT);
    return $userId . '.' . time() . '.' . $suffix;
}
?>
