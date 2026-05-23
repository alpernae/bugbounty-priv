<?php
// routes/token.php
$body = json_decode(file_get_contents('php://input'), true);
error_log('token request code_present=' . (isset($body['code']) ? 'true' : 'false'));

echo json_encode([
    'access_token' => issue_token($body['code'])
]);
?>
