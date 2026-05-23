import express from "express";
import { XMLParser } from "fast-xml-parser";

const app = express();
app.use(express.text({ type: "application/xml", limit: "64kb" }));

const parser = new XMLParser({
  processEntities: false,
  ignoreAttributes: false
});

app.post("/saml/consume", (req, res) => {
  if (req.body.includes("<!DOCTYPE")) {
    return res.status(400).json({ error: "doctype not allowed" });
  }
  const doc = parser.parse(req.body);
  res.json({ user: doc?.Response?.Assertion?.NameID || null });
});

export default app;
