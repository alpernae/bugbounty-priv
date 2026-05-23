<?php
// routes/download.php
$root = realpath(__DIR__ . '/../uploads');
$name = basename($_GET['file'] ?? '');
$path = realpath($root . DIRECTORY_SEPARATOR . $name);

if ($path === false || strpos($path, $root . DIRECTORY_SEPARATOR) !== 0) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid file']);
    exit;
}

header('Content-Type: application/octet-stream');
readfile($path);
?>
