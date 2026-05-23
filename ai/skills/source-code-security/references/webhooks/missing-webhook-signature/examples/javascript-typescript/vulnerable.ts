import express from "express";

const app = express();
app.use(express.json());

app.post("/webhooks/payment", async (req, res) => {
  await markInvoicePaid(req.body.invoiceId, req.body.amount);
  res.json({ received: true });
});

export default app;
