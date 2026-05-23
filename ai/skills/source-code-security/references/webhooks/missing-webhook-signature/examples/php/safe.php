<?php
// routes/example.php
$body = json_decode(file_get_contents('php://input'), true);
require_active_user(current_user());

$allowed = ['display_name', 'avatar_url'];
$clean = array_intersect_key($body, array_flip($allowed));
$result = BusinessService::process($clean, current_user());

header('Content-Type: application/json');
echo json_encode(['result' => $result]);
?>
