import express from "express";
import crypto from "crypto";

const app = express();
app.use(express.raw({ type: "application/json" }));

app.post("/webhooks/payment", async (req, res) => {
  const signature = String(req.headers["x-provider-signature"] || "");
  const expected = crypto
    .createHmac("sha256", process.env.WEBHOOK_SECRET!)
    .update(req.body)
    .digest("hex");

  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
    return res.sendStatus(401);
  }

  const event = JSON.parse(req.body.toString());
  await markInvoicePaid(event.invoiceId, event.amount);
  res.json({ received: true });
});

export default app;
