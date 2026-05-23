<?php
// routes/token.php
$body = json_decode(file_get_contents('php://input'), true);
error_log('token request body=' . json_encode($body) . ' headers=' . json_encode(getallheaders()));

echo json_encode([
    'access_token' => issue_token($body['code'])
]);
?>
