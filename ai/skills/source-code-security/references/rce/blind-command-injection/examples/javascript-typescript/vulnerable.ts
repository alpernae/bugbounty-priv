import express from "express";
import { exec } from "child_process";

const app = express();

app.get("/tools/ping", (req, res) => {
  const host = String(req.query.host || "");
  exec(`ping -c 1 ${host}`, (error, stdout, stderr) => {
    if (error) return res.status(500).send(stderr);
    res.type("text/plain").send(stdout);
  });
});

export default app;
