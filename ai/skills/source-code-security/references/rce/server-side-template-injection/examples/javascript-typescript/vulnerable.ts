import express from "express";
import ejs from "ejs";

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post("/email/preview", async (req, res) => {
  const template = String(req.body.template || "Hello <%= name %>");
  const html = ejs.render(template, { name: req.body.name || "customer" });
  res.type("html").send(html);
});

export default app;
