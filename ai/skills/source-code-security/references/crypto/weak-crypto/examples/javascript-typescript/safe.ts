import crypto from "crypto";

export function encryptNote(note: string, key: Buffer): string {
  if (key.length !== 32) throw new Error("key must be 256 bits");
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const ciphertext = Buffer.concat([cipher.update(note, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();

  return Buffer.concat([iv, tag, ciphertext]).toString("base64");
}
