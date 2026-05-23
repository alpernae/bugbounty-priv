<?php
// routes/ping.php
$host = $_GET['host'] ?? '';
if (!filter_var($host, FILTER_VALIDATE_IP)) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid host']);
    exit;
}

$cmd = ['ping', '-c', '1', $host];
$process = proc_open($cmd, [1 => ['pipe', 'w'], 2 => ['pipe', 'w']], $pipes);
$output = stream_get_contents($pipes[1]) . stream_get_contents($pipes[2]);

header('Content-Type: text/plain');
echo $output;
?>
