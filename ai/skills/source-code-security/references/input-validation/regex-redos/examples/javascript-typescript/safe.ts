import express from "express";
import isEmail from "validator/lib/isEmail";

const app = express();

app.get("/validate-email", (req, res) => {
  const email = String(req.query.email || "").slice(0, 254);
  res.json({ valid: isEmail(email) });
});

export default app;
