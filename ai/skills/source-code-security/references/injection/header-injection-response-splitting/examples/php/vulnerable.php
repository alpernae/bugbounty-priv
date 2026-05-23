<?php
// routes/download.php
$filename = $_GET['name'] ?? 'report.csv';

header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="' . $filename . '"');
echo "id,total\n1,42\n";
?>
