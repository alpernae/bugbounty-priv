import express from "express";

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post("/billing/card", async (req, res) => {
  await saveCard(req.user.id, req.body.token);
  res.redirect("/billing");
});

export default app;
