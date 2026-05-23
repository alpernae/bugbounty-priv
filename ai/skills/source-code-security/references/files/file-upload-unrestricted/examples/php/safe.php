<?php
// routes/avatar.php
$file = $_FILES['file'];
$allowed = ['image/png', 'image/jpeg'];

if (!in_array(mime_content_type($file['tmp_name']), $allowed, true)) {
    http_response_code(400);
    echo json_encode(['error' => 'bad file type']);
    exit;
}

$name = bin2hex(random_bytes(16)) . '.bin';
move_uploaded_file($file['tmp_name'], __DIR__ . '/../var/uploads/' . $name);

header('Content-Type: application/json');
echo json_encode(['fileId' => $name]);
?>
