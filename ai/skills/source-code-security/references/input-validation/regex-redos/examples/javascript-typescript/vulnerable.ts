import express from "express";

const app = express();

app.get("/validate-email", (req, res) => {
  const email = String(req.query.email || "");
  const pattern = /^([a-zA-Z0-9_.+-]+)+@(([a-zA-Z0-9-]+)+\.)+[a-zA-Z]{2,}$/;
  res.json({ valid: pattern.test(email) });
});

export default app;
