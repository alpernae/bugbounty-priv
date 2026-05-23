<?php
// routes/profile.php
$user = current_user();
$body = json_decode(file_get_contents('php://input'), true);
$allowed = ['display_name', 'avatar_url'];

foreach ($allowed as $key) {
    if (array_key_exists($key, $body)) {
        $user->$key = $body[$key];
    }
}

$user->save();
echo json_encode($user->toArray());
?>
