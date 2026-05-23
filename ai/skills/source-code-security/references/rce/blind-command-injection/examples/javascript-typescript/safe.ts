import express from "express";
import { execFile } from "child_process";
import { isIP } from "net";

const app = express();

app.get("/tools/ping", (req, res) => {
  const host = String(req.query.host || "");
  if (!isIP(host)) return res.status(400).json({ error: "invalid host" });

  execFile("ping", ["-c", "1", host], { timeout: 3000 }, (error, stdout, stderr) => {
    if (error) return res.status(500).send(stderr);
    res.type("text/plain").send(stdout);
  });
});

export default app;
