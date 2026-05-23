import express from "express";
import { z } from "zod";

const app = express();
app.use(express.json());

const Settings = z.object({
  theme: z.enum(["light", "dark"]).optional(),
  alerts: z.object({ email: z.boolean().optional() }).optional()
}).strict();

app.post("/settings", (req, res) => {
  const settings = Settings.parse(req.body);
  res.json({ theme: settings.theme || "light", alerts: settings.alerts || { email: true } });
});

export default app;
