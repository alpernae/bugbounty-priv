import express from "express";
import escapeHtml from "escape-html";

const app = express();

app.get("/search", (req, res) => {
  const query = String(req.query.q || "");
  const safeQuery = escapeHtml(query);
  const html = `
    <html>
      <body>
        <h1>Search</h1>
        <p>Results for: ${safeQuery}</p>
      </body>
    </html>`;
  res.type("html").send(html);
});

export default app;
