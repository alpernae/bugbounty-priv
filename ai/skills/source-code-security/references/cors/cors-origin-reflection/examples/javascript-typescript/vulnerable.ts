import express from "express";

const app = express();

app.use((req, res, next) => {
  const origin = req.headers.origin || "*";
  res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Access-Control-Allow-Credentials", "true");
  next();
});

app.get("/api/me", (req, res) => {
  res.json({ email: req.user.email, apiPlan: req.user.plan });
});

export default app;
