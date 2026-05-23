<?php
// routes/session_restore.php
$state = $_GET['state'] ?? '';
$session = json_decode(base64_decode($state), true);

if (!is_array($session) || !is_string($session['userId'] ?? null)) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid session']);
    exit;
}

header('Content-Type: application/json');
echo json_encode([
    'userId' => $session['userId'],
    'theme' => $session['theme'] ?? 'light'
]);
?>
