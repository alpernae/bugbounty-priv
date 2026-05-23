<?php
// middleware/cors.php
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allowed = ['https://app.example.com', 'https://admin.example.com'];

if (in_array($origin, $allowed, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Access-Control-Allow-Credentials: true');
    header('Vary: Origin');
}

echo json_encode([
    'email' => current_user()->email,
    'plan' => current_user()->plan
]);
?>
