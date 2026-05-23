import express from "express";
import multer from "multer";
import path from "path";

const app = express();
const upload = multer({
  dest: "var/uploads",
  limits: { fileSize: 2 * 1024 * 1024 },
  fileFilter: (_req, file, cb) => {
    const allowed = new Set(["image/png", "image/jpeg"]);
    cb(null, allowed.has(file.mimetype));
  }
});

app.post("/avatar", upload.single("file"), (req, res) => {
  const id = crypto.randomUUID();
  const extension = path.extname(req.file?.originalname || "").toLowerCase();
  res.json({ fileId: id, extension });
});

export default app;
