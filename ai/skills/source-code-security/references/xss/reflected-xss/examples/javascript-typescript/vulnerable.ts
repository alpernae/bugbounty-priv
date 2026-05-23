import express from "express";

const app = express();

app.get("/search", (req, res) => {
  const query = String(req.query.q || "");
  const html = `
    <html>
      <body>
        <h1>Search</h1>
        <p>Results for: ${query}</p>
      </body>
    </html>`;
  res.type("html").send(html);
});

export default app;
