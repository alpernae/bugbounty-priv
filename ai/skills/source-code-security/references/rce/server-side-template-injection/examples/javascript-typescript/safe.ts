import express from "express";
import escapeHtml from "escape-html";

const app = express();
app.use(express.urlencoded({ extended: false }));

const templates: Record<string, string> = {
  welcome: "Hello {{name}}",
  reminder: "Reminder for {{name}}"
};

app.post("/email/preview", (req, res) => {
  const key = String(req.body.templateKey || "welcome");
  const template = templates[key] || templates.welcome;
  const name = escapeHtml(String(req.body.name || "customer"));
  res.type("html").send(template.replace("{{name}}", name));
});

export default app;
