import express from "express";

const app = express();

app.use("/.git", express.static(".git"));
app.use("/uploads", express.static("uploads", { dotfiles: "allow" }));

app.get("/debug/env", (_req, res) => {
  res.json(process.env);
});

export default app;
