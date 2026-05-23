import express from "express";
import { prisma } from "./db";

const app = express();

app.post("/coupons/:code/redeem", async (req, res) => {
  const coupon = await prisma.coupon.findUnique({ where: { code: req.params.code } });
  if (!coupon || coupon.remaining <= 0) return res.status(409).json({ error: "sold out" });

  await prisma.coupon.update({
    where: { code: req.params.code },
    data: { remaining: coupon.remaining - 1 }
  });

  res.json({ redeemed: true });
});

export default app;
