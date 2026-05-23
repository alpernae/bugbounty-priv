import express from "express";
import { prisma } from "./db";

const app = express();

app.get("/api/invoices/:id", async (req, res) => {
  const invoice = await prisma.invoice.findUnique({
    where: { id: req.params.id }
  });

  if (!invoice) return res.status(404).json({ error: "not found" });
  res.json(invoice);
});

export default app;
