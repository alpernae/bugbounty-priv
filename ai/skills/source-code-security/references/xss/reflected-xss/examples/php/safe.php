<?php
// routes/search.php
$query = $_GET['q'] ?? '';
$safeQuery = htmlspecialchars($query, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');

echo "<html><body>";
echo "<h1>Search</h1>";
echo "<p>Results for: " . $safeQuery . "</p>";
echo "</body></html>";
?>
