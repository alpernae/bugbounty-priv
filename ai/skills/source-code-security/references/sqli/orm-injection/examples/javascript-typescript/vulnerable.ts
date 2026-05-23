import { PrismaClient } from "@prisma/client";
import express from "express";

const prisma = new PrismaClient();
const app = express();

app.get("/users", async (req, res) => {
  const sort = String(req.query.sort || "createdAt");
  const rows = await prisma.$queryRawUnsafe(
    `SELECT id, email FROM users ORDER BY ${sort} DESC`
  );
  res.json(rows);
});

export default app;
