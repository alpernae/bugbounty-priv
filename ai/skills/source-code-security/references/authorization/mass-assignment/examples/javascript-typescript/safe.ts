import express from "express";
import { z } from "zod";
import { prisma } from "./db";

const app = express();
app.use(express.json());

const ProfileUpdate = z.object({
  displayName: z.string().max(80).optional(),
  avatarUrl: z.string().url().optional()
});

app.patch("/profile", async (req, res) => {
  const data = ProfileUpdate.parse(req.body);
  const updated = await prisma.user.update({
    where: { id: req.user.id },
    data
  });

  res.json(updated);
});

export default app;
