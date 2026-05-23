import express from "express";

const app = express();

app.post("/login", (req, res) => {
  const sessionId = createSession(req.body.email);
  res.cookie("sid", sessionId, {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/"
  });
  res.redirect("/dashboard");
});

export default app;
