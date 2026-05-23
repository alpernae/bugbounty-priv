import express from "express";
import merge from "lodash.merge";

const app = express();
app.use(express.json());

app.post("/settings", (req, res) => {
  const defaults = { theme: "light", alerts: { email: true } };
  const settings = merge(defaults, req.body);
  res.json(settings);
});

export default app;
