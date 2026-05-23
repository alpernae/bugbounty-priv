<?php
// routes/rules.php
$body = json_decode(file_get_contents('php://input'), true);
$order = ['total' => (float)($body['total'] ?? 0), 'country' => 'TR'];

$expression = $body['expression'] ?? 'false';
$result = eval('return ' . $expression . ';');

header('Content-Type: application/json');
echo json_encode(['order' => $order, 'result' => $result]);
?>
