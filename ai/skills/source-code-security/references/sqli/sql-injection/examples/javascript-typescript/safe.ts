import express from "express";
import mysql from "mysql2/promise";

const app = express();
const db = await mysql.createPool(process.env.DATABASE_URL!);

app.get("/invoices", async (req, res) => {
  const status = String(req.query.status || "open");
  const [rows] = await db.execute(
    "SELECT id, total, status FROM invoices WHERE status = ?",
    [status]
  );
  res.json({ invoices: rows });
});

export default app;
