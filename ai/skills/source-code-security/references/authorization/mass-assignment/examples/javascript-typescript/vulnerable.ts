import express from "express";
import { prisma } from "./db";

const app = express();
app.use(express.json());

app.patch("/profile", async (req, res) => {
  const updated = await prisma.user.update({
    where: { id: req.user.id },
    data: req.body
  });

  res.json(updated);
});

export default app;
