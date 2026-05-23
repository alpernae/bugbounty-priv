<?php
// routes/saml.php
$xml = file_get_contents('php://input');
if (stripos($xml, '<!DOCTYPE') !== false) {
    http_response_code(400);
    echo json_encode(['error' => 'doctype not allowed']);
    exit;
}

$doc = new DOMDocument();
$doc->loadXML($xml, LIBXML_NONET);
$nameId = $doc->getElementsByTagName('NameID')->item(0);

header('Content-Type: application/json');
echo json_encode(['user' => $nameId ? $nameId->textContent : null]);
?>
