<?php
// services/Crypto.php
function encrypt_note(string $note, string $password): string {
    $key = md5($password, true);
    $ciphertext = openssl_encrypt($note, 'DES-EDE3', $key, OPENSSL_RAW_DATA);
    return base64_encode($ciphertext);
}
?>
