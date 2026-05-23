<?php
// routes/import_zip.php
$dest = realpath(__DIR__ . '/../var/imports');
$archive = $_FILES['file']['tmp_name'];
$zip = new ZipArchive();
$zip->open($archive);

function normalize_target(string $path): string {
    $path = str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $path);
    $prefix = str_starts_with($path, DIRECTORY_SEPARATOR) ? DIRECTORY_SEPARATOR : '';
    $parts = [];
    foreach (explode(DIRECTORY_SEPARATOR, $path) as $part) {
        if ($part === '' || $part === '.') {
            continue;
        }
        if ($part === '..') {
            array_pop($parts);
            continue;
        }
        $parts[] = $part;
    }
    return $prefix . implode(DIRECTORY_SEPARATOR, $parts);
}

for ($i = 0; $i < $zip->numFiles; $i++) {
    $name = $zip->getNameIndex($i);
    $target = normalize_target($dest . DIRECTORY_SEPARATOR . $name);
    if (strpos($target, $dest . DIRECTORY_SEPARATOR) !== 0) {
        continue;
    }
    if (str_ends_with($name, '/')) {
        mkdir($target, 0750, true);
        continue;
    }
    mkdir(dirname($target), 0750, true);
    $src = $zip->getStream($name);
    $dst = fopen($target, 'xb');
    stream_copy_to_stream($src, $dst);
    fclose($src);
    fclose($dst);
}

header('Content-Type: application/json');
echo json_encode(['imported' => true]);
?>
