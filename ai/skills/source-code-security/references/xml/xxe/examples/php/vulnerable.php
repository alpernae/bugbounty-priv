<?php
// routes/saml.php
libxml_disable_entity_loader(false);
$xml = file_get_contents('php://input');

$doc = new DOMDocument();
$doc->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
$nameId = $doc->getElementsByTagName('NameID')->item(0);

header('Content-Type: application/json');
echo json_encode(['user' => $nameId ? $nameId->textContent : null]);
?>
