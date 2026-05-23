import express from "express";
import { MongoClient } from "mongodb";

const app = express();
app.use(express.json());
const db = new MongoClient(process.env.MONGO_URL!).db("app");

app.post("/login", async (req, res) => {
  const user = await db.collection("users").findOne({
    email: req.body.email,
    password: req.body.password
  });

  if (!user) return res.status(401).json({ error: "invalid login" });
  res.json({ id: user._id, email: user.email });
});

export default app;
