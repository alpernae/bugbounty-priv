import express from "express";
import ldap from "ldapjs";
import { escapeFilter } from "ldap-escape";

const app = express();
const client = ldap.createClient({ url: process.env.LDAP_URL! });

app.get("/directory", (req, res) => {
  const user = escapeFilter(String(req.query.user || ""));
  const filter = `(&(objectClass=person)(uid=${user}))`;

  client.search("ou=people,dc=example,dc=com", { filter }, (_err, search) => {
    const results: unknown[] = [];
    search.on("searchEntry", entry => results.push(entry.object));
    search.on("end", () => res.json(results));
  });
});

export default app;
