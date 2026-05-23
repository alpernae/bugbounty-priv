import express from "express";

const app = express();

app.get("/fetch-preview", async (req, res) => {
  const url = String(req.query.url || "");
  const upstream = await fetch(url);
  const body = await upstream.text();

  res.json({
    status: upstream.status,
    sample: body.slice(0, 200)
  });
});

export default app;
