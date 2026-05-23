import express from "express";
import { z } from "zod";

const app = express();

const SessionSchema = z.object({
  userId: z.string().uuid(),
  theme: z.enum(["light", "dark"]).default("light")
});

app.get("/session/restore", (req, res) => {
  const state = String(req.query.state || "{}");
  const parsed = JSON.parse(Buffer.from(state, "base64").toString());
  const session = SessionSchema.parse(parsed);
  res.json({ userId: session.userId, theme: session.theme });
});

export default app;
