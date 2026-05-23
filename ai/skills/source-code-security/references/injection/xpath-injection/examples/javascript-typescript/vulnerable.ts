import express from "express";
import xpath from "xpath";
import { DOMParser } from "@xmldom/xmldom";

const app = express();
const xml = `<users><user name="alice" role="admin"/></users>`;
const doc = new DOMParser().parseFromString(xml);

app.get("/xml-user", (req, res) => {
  const name = String(req.query.name || "");
  const query = `//user[@name='${name}']`;
  const nodes = xpath.select(query, doc);
  res.json({ matches: nodes.length });
});

export default app;
