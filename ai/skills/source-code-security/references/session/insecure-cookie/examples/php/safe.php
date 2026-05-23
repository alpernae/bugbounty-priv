<?php
// routes/login.php
session_start();

$user = authenticate($_POST['email'], $_POST['password']);
session_regenerate_id(true);
$_SESSION['user_id'] = $user->id;
$_SESSION['role'] = $user->role;

setcookie('sid', session_id(), [
    'httponly' => true,
    'secure' => true,
    'samesite' => 'Lax',
    'path' => '/'
]);
header('Location: /dashboard');
?>
