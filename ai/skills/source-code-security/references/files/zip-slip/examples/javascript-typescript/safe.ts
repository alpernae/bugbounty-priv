import express from "express";
import unzipper from "unzipper";
import { createWriteStream } from "fs";
import fs from "fs/promises";
import path from "path";
import { pipeline } from "stream/promises";

const app = express();
const dest = path.resolve("var/imports");

async function streamToBuffer(stream: NodeJS.ReadableStream): Promise<Buffer> {
  const chunks: Buffer[] = [];
  for await (const chunk of stream) chunks.push(Buffer.from(chunk));
  return Buffer.concat(chunks);
}

app.post("/import", async (req, res) => {
  const directory = await unzipper.Open.buffer(await streamToBuffer(req));
  for (const file of directory.files) {
    const target = path.resolve(dest, file.path);
    if (!target.startsWith(dest + path.sep)) continue;
    if (file.type === "File") {
      await fs.mkdir(path.dirname(target), { recursive: true });
      await pipeline(file.stream(), createWriteStream(target, { flags: "wx" }));
    }
  }
  res.json({ imported: true });
});

export default app;
