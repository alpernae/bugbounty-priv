import express from "express";

const app = express();

app.get("/profile", (req, res) => {
  res.setHeader("Cache-Control", "private, no-store");
  res.type("html").send(`
    <link rel="canonical" href="https://app.example.com/profile">
    <h1>${escapeHtml(req.user.email)}</h1>
  `);
});

export default app;
