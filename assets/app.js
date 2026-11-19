// 热点雷达前端：读取 data.json 渲染卡片，支持按来源筛选。纯原生 JS，无框架。
const SOURCE_LABEL = { github: "GitHub", hackernews: "Hacker News", v2ex: "V2EX" };
let ALL = [];

async function load() {
  const resp = await fetch("data.json?t=" + Date.now());
  if (!resp.ok) throw new Error("data.json 加载失败: " + resp.status);
  const data = await resp.json();
  document.getElementById("generated-at").textContent =
    (data.generated_at || "").replace("T", " ").replace("+08:00", " (UTC+8)");
  document.getElementById("digest-text").textContent = data.digest || "";
  ALL = data.items || [];
  render("all");
}

function render(source) {
  const grid = document.getElementById("grid");
  const items = source === "all" ? ALL : ALL.filter((i) => i.source === source);
  grid.innerHTML = items
    .map(
      (i) => `
      <article class="card">
        <div class="head">
          <span class="badge ${i.source}">${SOURCE_LABEL[i.source] || i.source}</span>
          <span class="heat">${i.heat || ""}</span>
        </div>
        <h3><a href="${i.url}" target="_blank" rel="noopener">${escapeHtml(i.title)}</a></h3>
        ${i.summary ? `<p class="summary">🤖 ${escapeHtml(i.summary)}</p>` : ""}
        ${i.extra ? `<p class="extra">${escapeHtml(i.extra)}</p>` : ""}
      </article>`
    )
    .join("");
  if (!items.length) {
    grid.innerHTML = `<p style="color:var(--muted)">这个来源今天暂时没有数据。</p>`;
  }
}

function escapeHtml(s) {
  return String(s || "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );
}

document.getElementById("filters").addEventListener("click", (e) => {
  const btn = e.target.closest(".chip");
  if (!btn) return;
  document.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
  btn.classList.add("active");
  render(btn.dataset.source);
});

load().catch((e) => {
  document.getElementById("digest-text").textContent = "加载失败：" + e.message;
});
