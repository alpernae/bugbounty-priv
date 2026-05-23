<?php
// routes/search.php
$query = $_GET['q'] ?? '';

echo "<html><body>";
echo "<h1>Search</h1>";
echo "<p>Results for: " . $query . "</p>";
echo "</body></html>";
?>
