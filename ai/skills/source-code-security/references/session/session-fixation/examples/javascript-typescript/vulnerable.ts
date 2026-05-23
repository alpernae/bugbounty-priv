import express from "express";

const app = express();

app.post("/login", async (req, res) => {
  const user = await authenticate(req.body.email, req.body.password);
  req.session.userId = user.id;
  req.session.role = user.role;
  res.redirect("/dashboard");
});

export default app;
