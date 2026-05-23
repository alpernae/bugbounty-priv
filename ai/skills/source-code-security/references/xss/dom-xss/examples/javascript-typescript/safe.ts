// public/profile.ts - bundled client-side code
const params = new URLSearchParams(window.location.search);
const displayName = params.get("name") || "guest";

const banner = document.querySelector("#welcome");
if (banner) {
  const strong = document.createElement("strong");
  strong.textContent = `Welcome ${displayName}`;
  banner.replaceChildren(strong);
}

document.querySelector("#copy-link")?.addEventListener("click", () => {
  navigator.clipboard.writeText(window.location.href);
});
