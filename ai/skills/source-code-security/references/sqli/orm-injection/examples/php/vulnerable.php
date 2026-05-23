<?php
// routes/invoices.php
$pdo = new PDO($_ENV['DATABASE_URL']);
$status = $_GET['status'] ?? 'open';

$sql = "SELECT id,total,status FROM invoices WHERE status = '$status'";
$rows = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);

header('Content-Type: application/json');
echo json_encode(['invoices' => $rows]);
?>
