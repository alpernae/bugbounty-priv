<?php
// routes/login.php
session_start();

$user = authenticate($_POST['email'], $_POST['password']);
$_SESSION['user_id'] = $user->id;
$_SESSION['role'] = $user->role;

setcookie('sid', session_id());
header('Location: /dashboard');
?>
