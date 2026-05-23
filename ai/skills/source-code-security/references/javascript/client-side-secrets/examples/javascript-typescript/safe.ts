import Stripe from "stripe";
import express from "express";

const app = express();
const stripeKey = process.env.STRIPE_SECRET_KEY;
if (!stripeKey) throw new Error("STRIPE_SECRET_KEY is required");

const stripe = new Stripe(stripeKey, { apiVersion: "2023-10-16" });

app.post("/checkout", async (req, res) => {
  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    line_items: [{ price: req.body.priceId, quantity: 1 }],
    success_url: "https://app.example.com/success"
  });
  res.json({ url: session.url });
});

export default app;
