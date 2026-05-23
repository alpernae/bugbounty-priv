import express from "express";
import jsep from "jsep";

const app = express();
app.use(express.json());

const allowedFields = new Set(["total"]);
app.post("/rules/preview", (req, res) => {
  const field = String(req.body.field || "");
  const min = Number(req.body.min || 0);
  const order = { total: Number(req.body.total || 0), country: "TR" };

  if (!allowedFields.has(field)) return res.status(400).json({ error: "bad field" });
  const parsed = jsep(`${field} > ${min}`);
  const result = order.total > min;
  res.json({ parsedType: parsed.type, result });
});

export default app;
