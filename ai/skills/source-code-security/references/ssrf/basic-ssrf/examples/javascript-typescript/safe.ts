import express from "express";
import dns from "dns/promises";
import ipaddr from "ipaddr.js";

const app = express();
const allowedHosts = new Set(["api.partner.example", "images.example-cdn.com"]);

async function assertSafeUrl(raw: string): Promise<URL> {
  const url = new URL(raw);
  if (!["https:"].includes(url.protocol) || !allowedHosts.has(url.hostname)) {
    throw new Error("blocked upstream");
  }
  const addresses = await dns.lookup(url.hostname, { all: true });
  if (addresses.some(a => ipaddr.parse(a.address).range() !== "unicast")) {
    throw new Error("private address blocked");
  }
  return url;
}

app.get("/fetch-preview", async (req, res) => {
  const url = await assertSafeUrl(String(req.query.url || ""));
  const upstream = await fetch(url, { redirect: "manual" });
  res.json({ status: upstream.status });
});

export default app;
