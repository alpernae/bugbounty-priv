<?php
// routes/avatar.php
$file = $_FILES['file'];
$destination = __DIR__ . '/../public/uploads/' . $file['name'];

move_uploaded_file($file['tmp_name'], $destination);

header('Content-Type: application/json');
echo json_encode(['publicUrl' => '/uploads/' . $file['name']]);
?>
