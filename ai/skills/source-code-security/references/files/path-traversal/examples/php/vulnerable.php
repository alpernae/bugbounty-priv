<?php
// routes/download.php
$name = $_GET['file'] ?? '';
$path = __DIR__ . '/../uploads/' . $name;

header('Content-Type: application/octet-stream');
readfile($path);
?>
