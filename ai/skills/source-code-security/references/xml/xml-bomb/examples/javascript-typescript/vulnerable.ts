import express from "express";
import libxmljs from "libxmljs2";

const app = express();
app.use(express.text({ type: "application/xml" }));

app.post("/saml/consume", (req, res) => {
  const doc = libxmljs.parseXml(req.body, { noent: true });
  const user = doc.get("//NameID")?.text();
  res.json({ user });
});

export default app;
