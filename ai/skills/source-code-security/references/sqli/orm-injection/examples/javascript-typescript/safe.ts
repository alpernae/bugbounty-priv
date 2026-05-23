import { PrismaClient } from "@prisma/client";
import express from "express";

const prisma = new PrismaClient();
const app = express();
const allowedSort = new Set(["createdAt", "email", "id"]);

app.get("/users", async (req, res) => {
  const requested = String(req.query.sort || "createdAt");
  const sort = allowedSort.has(requested) ? requested : "createdAt";
  const rows = await prisma.user.findMany({
    select: { id: true, email: true },
    orderBy: { [sort]: "desc" }
  });
  res.json(rows);
});

export default app;
