import express from "express";

const app = express();

app.use("/uploads", express.static("uploads", {
  dotfiles: "deny",
  index: false,
  fallthrough: false,
  setHeaders: res => res.setHeader("X-Content-Type-Options", "nosniff")
}));

app.get("/health", (_req, res) => {
  res.json({ ok: true });
});

export default app;
