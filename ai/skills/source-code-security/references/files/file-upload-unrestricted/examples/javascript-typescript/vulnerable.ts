import express from "express";
import multer from "multer";

const app = express();
const upload = multer({ dest: "public/uploads" });

app.post("/avatar", upload.single("file"), (req, res) => {
  const original = req.file?.originalname || "upload.bin";
  res.json({
    publicUrl: `/uploads/${req.file?.filename}`,
    originalName: original
  });
});

app.use("/uploads", express.static("public/uploads"));
export default app;
