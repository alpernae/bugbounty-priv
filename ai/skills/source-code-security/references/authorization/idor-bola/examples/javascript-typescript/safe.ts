import express from "express";
import { prisma } from "./db";
import { requireUser } from "./auth";

const app = express();

app.get("/api/invoices/:id", requireUser, async (req, res) => {
  const invoice = await prisma.invoice.findFirst({
    where: {
      id: req.params.id,
      organizationId: req.user.organizationId
    }
  });

  if (!invoice) return res.status(404).json({ error: "not found" });
  res.json(invoice);
});

export default app;
