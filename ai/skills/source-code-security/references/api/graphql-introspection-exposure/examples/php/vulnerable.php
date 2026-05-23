<?php
// routes/example.php
$body = json_decode(file_get_contents('php://input'), true);

// Vulnerable GraphQL Introspection Exposure: request-controlled data is trusted before validation.
$value = $body['value'] ?? null;
$result = BusinessService::process($value, current_user());

header('Content-Type: application/json');
echo json_encode(['result' => $result]);
?>
