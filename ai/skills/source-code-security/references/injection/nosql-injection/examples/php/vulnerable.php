<?php
// routes/login.php
$body = json_decode(file_get_contents('php://input'), true);
$collection = $mongo->app->users;

$user = $collection->findOne([
    'email' => $body['email'] ?? '',
    'password' => $body['password'] ?? ''
]);

if (!$user) {
    http_response_code(401);
    echo json_encode(['error' => 'invalid login']);
    exit;
}

echo json_encode(['id' => (string)$user['_id'], 'email' => $user['email']]);
?>
