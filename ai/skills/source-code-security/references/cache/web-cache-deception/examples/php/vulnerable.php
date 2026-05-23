<?php
// routes/profile.php
$host = $_SERVER['HTTP_X_FORWARDED_HOST'] ?? $_SERVER['HTTP_HOST'];
header('Cache-Control: public, max-age=600');

echo "<link rel='canonical' href='https://$host/profile'>";
echo "<h1>" . current_user()->email . "</h1>";
?>
