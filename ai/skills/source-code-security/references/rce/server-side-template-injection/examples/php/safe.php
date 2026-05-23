<?php
// routes/rules.php
$body = json_decode(file_get_contents('php://input'), true);
$order = ['total' => (float)($body['total'] ?? 0), 'country' => 'TR'];

$field = $body['field'] ?? '';
$min = (float)($body['min'] ?? 0);
if ($field !== 'total') {
    http_response_code(400);
    echo json_encode(['error' => 'bad field']);
    exit;
}

header('Content-Type: application/json');
echo json_encode(['result' => $order['total'] > $min]);
?>
