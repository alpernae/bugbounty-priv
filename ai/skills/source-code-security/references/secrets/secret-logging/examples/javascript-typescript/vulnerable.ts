import express from "express";
import pino from "pino";

const app = express();
const logger = pino();
app.use(express.json());

app.post("/oauth/token", (req, res) => {
  logger.info({ body: req.body, headers: req.headers }, "token request");
  res.json({ access_token: issueToken(req.body.code) });
});

export default app;
