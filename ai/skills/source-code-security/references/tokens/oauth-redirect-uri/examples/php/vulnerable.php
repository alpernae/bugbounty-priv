<?php
// routes/callback.php
$next = $_GET['next'] ?? '/dashboard';
header('Location: ' . $next);
exit;
?>
