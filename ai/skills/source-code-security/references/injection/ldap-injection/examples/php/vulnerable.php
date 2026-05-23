<?php
// routes/directory.php
$ldap = ldap_connect($_ENV['LDAP_URL']);
ldap_bind($ldap, $_ENV['LDAP_USER'], $_ENV['LDAP_PASSWORD']);

$user = $_GET['user'] ?? '';
$filter = "(&(objectClass=person)(uid=$user))";
$result = ldap_search($ldap, "ou=people,dc=example,dc=com", $filter);

header('Content-Type: application/json');
echo json_encode(ldap_get_entries($ldap, $result));
?>
