<?php
// routes/admin.php
$token = str_replace('Bearer ', '', $_SERVER['HTTP_AUTHORIZATION'] ?? '');
$publicKey = file_get_contents(__DIR__ . '/../keys/jwt-public.pem');
$claims = JWT::decode($token, new Key($publicKey, 'RS256'));

if (($claims->iss ?? '') !== 'https://auth.example.com' || ($claims->role ?? '') !== 'admin') {
    http_response_code(403);
    echo json_encode(['error' => 'forbidden']);
    exit;
}

echo json_encode(['admin' => true]);
?>
