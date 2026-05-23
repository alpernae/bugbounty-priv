<?php
// routes/profile.php
header('Cache-Control: private, no-store');

echo "<link rel='canonical' href='https://app.example.com/profile'>";
echo "<h1>" . htmlspecialchars(current_user()->email, ENT_QUOTES, 'UTF-8') . "</h1>";
?>
