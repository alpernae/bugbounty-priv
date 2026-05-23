import express from "express";
import unzipper from "unzipper";
import fs from "fs";

const app = express();

app.post("/import", async (req, res) => {
  await req.pipe(unzipper.Extract({ path: "var/imports" })).promise();
  res.json({ imported: true });
});

export default app;
