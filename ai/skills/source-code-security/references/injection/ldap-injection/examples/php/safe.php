<?php
// routes/directory.php
$ldap = ldap_connect($_ENV['LDAP_URL']);
ldap_bind($ldap, $_ENV['LDAP_USER'], $_ENV['LDAP_PASSWORD']);

$user = $_GET['user'] ?? '';
if (!preg_match('/^[a-zA-Z0-9._-]{1,40}$/', $user)) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid user']);
    exit;
}

$filter = "(&(objectClass=person)(uid=" . ldap_escape($user, '', LDAP_ESCAPE_FILTER) . "))";
$result = ldap_search($ldap, "ou=people,dc=example,dc=com", $filter);

header('Content-Type: application/json');
echo json_encode(ldap_get_entries($ldap, $result));
?>
