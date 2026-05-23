<?php
// routes/fetch_preview.php
$url = $_GET['url'] ?? '';
$parts = parse_url($url);
$allowedHosts = ['api.partner.example', 'images.example-cdn.com'];

if (($parts['scheme'] ?? '') !== 'https' || !in_array($parts['host'] ?? '', $allowedHosts, true)) {
    http_response_code(400);
    echo json_encode(['error' => 'blocked upstream']);
    exit;
}

$context = stream_context_create(['http' => ['follow_location' => 0, 'timeout' => 5]]);
$body = file_get_contents($url, false, $context);

header('Content-Type: application/json');
echo json_encode(['status' => 200, 'sample' => substr($body, 0, 80)]);
?>
