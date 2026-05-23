import express from "express";
import fs from "fs/promises";
import path from "path";

const app = express();
const root = path.resolve(process.cwd(), "uploads");

app.get("/download", async (req, res) => {
  const name = path.basename(String(req.query.file || ""));
  const filePath = path.resolve(root, name);
  if (!filePath.startsWith(root + path.sep)) {
    return res.status(400).json({ error: "invalid file" });
  }

  const data = await fs.readFile(filePath);
  res.type("application/octet-stream").send(data);
});

export default app;
