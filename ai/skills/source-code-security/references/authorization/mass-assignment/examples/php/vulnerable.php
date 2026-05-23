<?php
// routes/profile.php
$user = current_user();
$body = json_decode(file_get_contents('php://input'), true);

foreach ($body as $key => $value) {
    $user->$key = $value;
}

$user->save();
echo json_encode($user->toArray());
?>
