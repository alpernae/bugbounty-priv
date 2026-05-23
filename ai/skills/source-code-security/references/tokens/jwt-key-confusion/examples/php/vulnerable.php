<?php
// routes/admin.php
$token = str_replace('Bearer ', '', $_SERVER['HTTP_AUTHORIZATION'] ?? '');
$claims = JWT::decodeWithoutVerification($token);

if (($claims['role'] ?? '') !== 'admin') {
    http_response_code(403);
    echo json_encode(['error' => 'forbidden']);
    exit;
}

echo json_encode(['admin' => true]);
?>
