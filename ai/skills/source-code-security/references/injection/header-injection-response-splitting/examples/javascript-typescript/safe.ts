import express from "express";

const app = express();

app.get("/download", (req, res) => {
  const raw = String(req.query.name || "report.csv");
  const filename = raw.replace(/[^a-zA-Z0-9._-]/g, "_").slice(0, 80);
  res.attachment(filename || "report.csv");
  res.type("text/csv").send("id,total\n1,42\n");
});

export default app;
