# 📡 热点雷达 hot-radar

> 自动抓取 GitHub Trending / Hacker News / V2EX 热点 → DeepSeek 生成一句话摘要和每日简报 → 静态网页看板 + 钉钉群推送。
> 每天由 GitHub Actions 定时运行，**零服务器、零第三方 Python 依赖**。

🔗 **在线演示**：https://你的用户名.github.io/hot-radar/ （开启 GitHub Pages 后替换此链接）

## 它解决什么问题

每天早上打开一个链接（或收到一条钉钉消息），30 秒看完技术圈今天发生了什么，
每条热点附带 AI 写的一句话摘要，不用逐个点进去。作者本人每天在用。

## 功能

- 🕷️ 三个公开来源爬虫：GitHub Trending（HTML 解析）、Hacker News（Algolia API）、V2EX（官方 API）
- 🧠 DeepSeek AI：每条热点一句话摘要 + 每日简报段落；接口失败自动降级，不阻塞流程
- 🗄️ SQLite 落库去重（按 URL），热度每日刷新 —— schema 与示例 SQL 见 [docs/SQL_NOTES.md](docs/SQL_NOTES.md)
- 🌐 纯静态看板：深色卡片流、按来源筛选，托管在 GitHub Pages
- 🤖 钉钉群机器人推送每日简报（可选）
- ⏰ GitHub Actions 每天北京时间 9:00 自动跑一遍并提交数据（运维自动化演示）

## 本地运行

```bash
# Python 3.9+ 即可，无需 pip install 任何东西
cp .env.example .env        # 填入你的 DeepSeek API Key
python src/main.py          # 抓取 + AI 摘要 + 生成 data.json
python src/main.py --no-ai  # 没有 Key 时：跳过 AI，用降级文案
python src/main.py --push   # 配置 DINGTALK_WEBHOOK 后推送到钉钉群
```

用浏览器打开 `index.html`（或 `python -m http.server` 后访问）即可看到看板。

## 部署成公开链接（GitHub Pages）

1. 本仓库推送到你的 GitHub
2. Settings → Secrets and variables → Actions → 新建 `DEEPSEEK_API_KEY`（可选 `DINGTALK_WEBHOOK`）
3. Settings → Pages → Source 选 `Deploy from a branch`，branch 选 `main` / `(root)`
4. 在 Actions 页手动触发一次 `daily-update`，数据即变为真实抓取结果
5. 把 README 顶部的演示链接换成你的 `https://<用户名>.github.io/hot-radar/`

## 项目结构

```
├── index.html            # 看板页面
├── assets/               # 样式与前端脚本（原生 JS，无框架）
├── data.json             # 网页读取的数据（Actions 每次运行后自动提交）
├── src/
│   ├── main.py           # 主入口：抓取→入库→AI→导出→推送
│   ├── fetchers.py       # 三个来源的爬虫
│   ├── storage.py        # SQLite 读写与去重
│   ├── ai.py             # DeepSeek 调用（摘要+简报），带降级
│   ├── export.py         # 导出 data.json
│   ├── dingtalk.py       # 钉钉 webhook 推送
│   └── schema.sql        # 数据库结构
├── .github/workflows/update.yml  # 每日定时任务
└── docs/                 # SQL 笔记、验证记录
```

## AI 使用说明（本项目如何使用 AI）

- **内容层**：热点摘要与每日简报由 DeepSeek API 在线生成（`src/ai.py`）
- **开发层**：代码与文档由作者与 AI 编程助手协作完成，AI 生成的代码均经作者逐段审查、本地运行验证后才提交；改动与验证结果记录见 [CHANGELOG.md](CHANGELOG.md) 与 [docs/VERIFY.md](docs/VERIFY.md)

## 变更记录与验证

- [CHANGELOG.md](CHANGELOG.md)：每次改了什么、为什么改
- [docs/VERIFY.md](docs/VERIFY.md)：每项功能的验证方式与结果（对应"记录改动内容和验证结果"的工作习惯）
