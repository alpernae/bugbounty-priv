<?php
// routes/invoice.php
$id = $_GET['id'] ?? '';
$invoice = Invoice::find($id);

if (!$invoice) {
    http_response_code(404);
    echo json_encode(['error' => 'not found']);
    exit;
}

header('Content-Type: application/json');
echo json_encode($invoice->toArray());
?>
