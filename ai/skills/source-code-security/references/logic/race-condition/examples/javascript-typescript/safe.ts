import express from "express";
import { prisma } from "./db";

const app = express();

app.post("/coupons/:code/redeem", async (req, res) => {
  const updated = await prisma.coupon.updateMany({
    where: { code: req.params.code, remaining: { gt: 0 } },
    data: { remaining: { decrement: 1 } }
  });

  if (updated.count !== 1) return res.status(409).json({ error: "sold out" });
  res.json({ redeemed: true });
});

export default app;
