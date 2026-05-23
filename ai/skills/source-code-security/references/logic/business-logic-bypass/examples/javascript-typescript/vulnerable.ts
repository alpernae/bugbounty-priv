import express from "express";

const app = express();
app.use(express.json());

app.post("/checkout", async (req, res) => {
  const cart = await loadCart(req.user.id);
  const discount = Number(req.body.discountPercent || 0);
  const total = cart.subtotal - cart.subtotal * (discount / 100);

  const order = await createOrder(req.user.id, { total, discount });
  res.json(order);
});

export default app;
