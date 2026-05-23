<?php
// routes/import_zip.php
$zip = new ZipArchive();
$zip->open($_FILES['file']['tmp_name']);
$zip->extractTo(__DIR__ . '/../var/imports');
$zip->close();

header('Content-Type: application/json');
echo json_encode(['imported' => true]);
?>
