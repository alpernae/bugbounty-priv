import express from "express";

const app = express();
app.use(express.json());

app.post("/checkout", async (req, res) => {
  const cart = await loadCart(req.user.id);
  const coupon = await validateCoupon(req.user.id, String(req.body.coupon || ""));
  const discount = coupon ? coupon.percent : 0;
  const total = calculateServerSideTotal(cart, discount);

  const order = await createOrder(req.user.id, { total, couponId: coupon?.id });
  res.json(order);
});

export default app;
