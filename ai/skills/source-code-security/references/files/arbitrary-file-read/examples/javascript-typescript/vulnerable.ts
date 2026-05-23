import express from "express";
import fs from "fs/promises";
import path from "path";

const app = express();

app.get("/download", async (req, res) => {
  const name = String(req.query.file || "");
  const filePath = path.join(process.cwd(), "uploads", name);
  const data = await fs.readFile(filePath);
  res.type("application/octet-stream").send(data);
});

export default app;
