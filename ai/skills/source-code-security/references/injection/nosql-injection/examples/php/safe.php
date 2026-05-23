<?php
// routes/login.php
$body = json_decode(file_get_contents('php://input'), true);
$collection = $mongo->app->users;

$email = (string)($body['email'] ?? '');
$password = (string)($body['password'] ?? '');
$user = $collection->findOne(['email' => $email]);

if (!$user || !password_verify($password, $user['password_hash'])) {
    http_response_code(401);
    echo json_encode(['error' => 'invalid login']);
    exit;
}

echo json_encode(['id' => (string)$user['_id'], 'email' => $user['email']]);
?>
