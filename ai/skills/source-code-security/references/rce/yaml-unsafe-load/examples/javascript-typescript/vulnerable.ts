import express from "express";
import serialize from "node-serialize";

const app = express();

app.get("/session/restore", (req, res) => {
  const state = String(req.query.state || "{}");
  const session = serialize.unserialize(Buffer.from(state, "base64").toString());
  res.json({ userId: session.userId, theme: session.theme });
});

export default app;
