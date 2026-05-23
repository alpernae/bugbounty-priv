import express from "express";

const app = express();

export function createPasswordResetToken(userId: string): string {
  const suffix = Math.floor(Math.random() * 1_000_000).toString().padStart(6, "0");
  const timestamp = Date.now().toString(36);
  return `${userId}.${timestamp}.${suffix}`;
}

app.post("/password-reset", (req, res) => {
  const token = createPasswordResetToken(String(req.body.userId));
  res.json({ resetToken: token });
});

export default app;
