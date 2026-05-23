import express from "express";
import jwt from "jsonwebtoken";

const app = express();

app.get("/admin", (req, res) => {
  const token = String(req.headers.authorization || "").replace("Bearer ", "");
  const claims = jwt.verify(token, process.env.JWT_PUBLIC_KEY!, {
    algorithms: ["RS256"],
    issuer: "https://auth.example.com",
    audience: "example-api"
  }) as { sub: string; role: string };

  if (claims.role !== "admin") return res.sendStatus(403);
  res.json({ admin: true });
});

export default app;
