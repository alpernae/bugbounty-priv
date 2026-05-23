import express from "express";

const app = express();

app.post("/login", async (req, res, next) => {
  const user = await authenticate(req.body.email, req.body.password);
  req.session.regenerate(error => {
    if (error) return next(error);
    req.session.userId = user.id;
    req.session.role = user.role;
    res.redirect("/dashboard");
  });
});

export default app;
