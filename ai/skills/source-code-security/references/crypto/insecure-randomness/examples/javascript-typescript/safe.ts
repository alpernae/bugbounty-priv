import crypto from "crypto";
import express from "express";

const app = express();

export function createPasswordResetToken(userId: string): string {
  const random = crypto.randomBytes(32).toString("base64url");
  const issuedAt = Date.now();
  return `${userId}.${issuedAt}.${random}`;
}

app.post("/password-reset", (req, res) => {
  const token = createPasswordResetToken(String(req.body.userId));
  res.json({ resetToken: token });
});

export default app;
