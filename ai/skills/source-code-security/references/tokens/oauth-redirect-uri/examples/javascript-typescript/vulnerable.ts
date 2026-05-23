import express from "express";

const app = express();

app.get("/login/callback", (req, res) => {
  const next = String(req.query.next || "/dashboard");
  res.redirect(next);
});

export default app;
