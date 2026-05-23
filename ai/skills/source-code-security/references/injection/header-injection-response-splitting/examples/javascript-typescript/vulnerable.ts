import express from "express";

const app = express();

app.get("/download", (req, res) => {
  const filename = String(req.query.name || "report.csv");
  res.setHeader("Content-Disposition", `attachment; filename="${filename}"`);
  res.type("text/csv").send("id,total\n1,42\n");
});

export default app;
