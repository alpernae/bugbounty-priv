import express from "express";
import csrf from "csurf";

const app = express();
const csrfProtection = csrf({ cookie: { httpOnly: true, sameSite: "lax", secure: true } });
app.use(express.urlencoded({ extended: false }));

app.post("/billing/card", csrfProtection, async (req, res) => {
  await saveCard(req.user.id, req.body.token);
  res.redirect("/billing");
});

export default app;
