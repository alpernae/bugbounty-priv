<?php
// routes/session_restore.php
$state = $_GET['state'] ?? '';
$session = unserialize(base64_decode($state));

header('Content-Type: application/json');
echo json_encode([
    'userId' => $session['userId'],
    'theme' => $session['theme'] ?? 'light'
]);
?>
