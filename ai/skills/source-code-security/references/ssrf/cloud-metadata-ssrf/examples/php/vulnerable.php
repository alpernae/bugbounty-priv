<?php
// routes/fetch_preview.php
$url = $_GET['url'] ?? '';
$body = file_get_contents($url);

header('Content-Type: application/json');
echo json_encode([
    'status' => 200,
    'sample' => substr($body, 0, 200)
]);
?>
