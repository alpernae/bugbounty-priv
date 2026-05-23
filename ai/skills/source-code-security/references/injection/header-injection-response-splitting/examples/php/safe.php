<?php
// routes/download.php
$raw = $_GET['name'] ?? 'report.csv';
$filename = substr(preg_replace('/[^a-zA-Z0-9._-]/', '_', $raw), 0, 80) ?: 'report.csv';

header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="' . $filename . '"');
echo "id,total\n1,42\n";
?>
