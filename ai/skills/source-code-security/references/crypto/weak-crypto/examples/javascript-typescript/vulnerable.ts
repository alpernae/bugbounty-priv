import crypto from "crypto";

export function encryptNote(note: string, password: string): string {
  const key = crypto.createHash("md5").update(password).digest();
  const cipher = crypto.createCipheriv("des-ede3", key, Buffer.alloc(8));
  const encrypted = Buffer.concat([cipher.update(note, "utf8"), cipher.final()]);
  return encrypted.toString("base64");
}
