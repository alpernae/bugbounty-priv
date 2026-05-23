import express from "express";
import xpath from "xpath";
import { DOMParser } from "@xmldom/xmldom";

const app = express();
const xml = `<users><user name="alice" role="admin"/></users>`;
const doc = new DOMParser().parseFromString(xml);

app.get("/xml-user", (req, res) => {
  const name = String(req.query.name || "");
  if (!/^[a-z0-9._-]{1,40}$/i.test(name)) {
    return res.status(400).json({ error: "invalid name" });
  }
  const nodes = xpath.select("//user", doc)
    .filter((node: any) => node.getAttribute("name") === name);
  res.json({ matches: nodes.length });
});

export default app;
