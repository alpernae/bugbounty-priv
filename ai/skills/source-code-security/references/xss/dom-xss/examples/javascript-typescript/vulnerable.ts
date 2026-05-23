// public/profile.ts - bundled client-side code
const params = new URLSearchParams(window.location.search);
const displayName = params.get("name") || "guest";

const banner = document.querySelector("#welcome");
if (banner) {
  banner.innerHTML = `<strong>Welcome ${displayName}</strong>`;
}

document.querySelector("#copy-link")?.addEventListener("click", () => {
  navigator.clipboard.writeText(window.location.href);
});
