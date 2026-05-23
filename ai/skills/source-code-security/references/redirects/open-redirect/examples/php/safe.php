<?php
// routes/callback.php
$next = $_GET['next'] ?? '/dashboard';
$allowed = ['/dashboard', '/settings', '/billing'];

if (!in_array($next, $allowed, true)) {
    $next = '/dashboard';
}

header('Location: ' . $next);
exit;
?>
