<?php
// routes/ping.php
$host = $_GET['host'] ?? '';
$output = shell_exec("ping -c 1 " . $host . " 2>&1");

header('Content-Type: text/plain');
echo $output;
?>
