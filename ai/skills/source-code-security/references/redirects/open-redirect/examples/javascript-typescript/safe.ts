import express from "express";

const app = express();
const allowedPaths = new Set(["/dashboard", "/settings", "/billing"]);

app.get("/login/callback", (req, res) => {
  const next = String(req.query.next || "/dashboard");
  const target = allowedPaths.has(next) ? next : "/dashboard";
  res.redirect(target);
});

export default app;
