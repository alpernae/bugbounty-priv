import express from "express";

const app = express();
app.use(express.json());

app.post("/rules/preview", (req, res) => {
  const expression = String(req.body.expression || "false");
  const order = { total: Number(req.body.total || 0), country: "TR" };
  const result = eval(expression);
  res.json({ order, result });
});

export default app;
