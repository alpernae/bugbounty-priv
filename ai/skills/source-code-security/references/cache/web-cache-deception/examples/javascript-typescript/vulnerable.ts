import express from "express";

const app = express();

app.get("/profile", (req, res) => {
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  res.setHeader("Cache-Control", "public, max-age=600");
  res.type("html").send(`
    <link rel="canonical" href="https://${host}/profile">
    <h1>${req.user.email}</h1>
  `);
});

export default app;
