<?php
// routes/invoices.php
$pdo = new PDO($_ENV['DATABASE_URL']);
$status = $_GET['status'] ?? 'open';

$stmt = $pdo->prepare('SELECT id,total,status FROM invoices WHERE status = ?');
$stmt->execute([$status]);
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

header('Content-Type: application/json');
echo json_encode(['invoices' => $rows]);
?>
