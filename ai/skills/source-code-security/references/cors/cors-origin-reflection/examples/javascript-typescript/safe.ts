import express from "express";

const app = express();
const allowedOrigins = new Set(["https://app.example.com", "https://admin.example.com"]);

app.use((req, res, next) => {
  const origin = String(req.headers.origin || "");
  if (allowedOrigins.has(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Credentials", "true");
    res.setHeader("Vary", "Origin");
  }
  next();
});

app.get("/api/me", (req, res) => {
  res.json({ email: req.user.email, apiPlan: req.user.plan });
});

export default app;
