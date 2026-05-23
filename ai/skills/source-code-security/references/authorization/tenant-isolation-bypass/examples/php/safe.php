<?php
// routes/invoice.php
$id = $_GET['id'] ?? '';
$invoice = Invoice::where('id', $id)
    ->where('organization_id', current_user()->organization_id)
    ->first();

if (!$invoice) {
    http_response_code(404);
    echo json_encode(['error' => 'not found']);
    exit;
}

header('Content-Type: application/json');
echo json_encode($invoice->toArray());
?>
