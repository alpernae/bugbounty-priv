<?php
// services/Crypto.php
function encrypt_note(string $note, string $key): string {
    if (strlen($key) !== 32) {
        throw new InvalidArgumentException('key must be 256 bits');
    }
    $iv = random_bytes(12);
    $tag = '';
    $ciphertext = openssl_encrypt($note, 'aes-256-gcm', $key, OPENSSL_RAW_DATA, $iv, $tag);
    return base64_encode($iv . $tag . $ciphertext);
}
?>
