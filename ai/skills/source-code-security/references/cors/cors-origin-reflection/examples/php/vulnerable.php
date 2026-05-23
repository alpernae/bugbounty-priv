<?php
// middleware/cors.php
$origin = $_SERVER['HTTP_ORIGIN'] ?? '*';
header('Access-Control-Allow-Origin: ' . $origin);
header('Access-Control-Allow-Credentials: true');

echo json_encode([
    'email' => current_user()->email,
    'plan' => current_user()->plan
]);
?>
