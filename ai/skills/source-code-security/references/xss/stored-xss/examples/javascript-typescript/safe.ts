import express from "express";
import escapeHtml from "escape-html";

const app = express();
app.use(express.urlencoded({ extended: false }));

const comments: Array<{ author: string; body: string }> = [];

app.post("/comments", (req, res) => {
  comments.push({
    author: String(req.body.author || "anon"),
    body: String(req.body.body || "")
  });
  res.redirect("/comments");
});

app.get("/comments", (_req, res) => {
  const rows = comments
    .map(c => `<article><b>${escapeHtml(c.author)}</b><p>${escapeHtml(c.body)}</p></article>`)
    .join("\n");

  res.type("html").send(`<main>${rows}</main>`);
});

export default app;
