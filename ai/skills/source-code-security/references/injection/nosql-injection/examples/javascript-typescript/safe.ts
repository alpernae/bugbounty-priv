import express from "express";
import { MongoClient } from "mongodb";
import bcrypt from "bcryptjs";

const app = express();
app.use(express.json());
const db = new MongoClient(process.env.MONGO_URL!).db("app");

app.post("/login", async (req, res) => {
  const email = String(req.body.email || "");
  const password = String(req.body.password || "");
  const user = await db.collection("users").findOne({ email });

  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    return res.status(401).json({ error: "invalid login" });
  }

  res.json({ id: user._id, email: user.email });
});

export default app;
