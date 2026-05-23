import express from "express";
import mysql from "mysql2/promise";

const app = express();
const db = await mysql.createPool(process.env.DATABASE_URL!);

app.get("/invoices", async (req, res) => {
  const status = String(req.query.status || "open");
  const sql = `SELECT id, total, status FROM invoices WHERE status = '${status}'`;
  const [rows] = await db.query(sql);
  res.json({ invoices: rows });
});

export default app;
