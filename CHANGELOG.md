# Changelog

本项目所有改动记录于此：改了什么、为什么改、验证方式见 docs/VERIFY.md。

## [0.1.0] - 2026-11-19

### Added
- 初版：GitHub Trending / Hacker News / V2EX 三个来源爬虫（`src/fetchers.py`）
- SQLite 落库与 URL 去重、热度刷新（`src/storage.py` + `src/schema.sql`）
- DeepSeek 一句话摘要与每日简报，接口失败自动降级（`src/ai.py`）
- 静态看板：深色卡片流 + 来源筛选（`index.html` / `assets/`）
- 钉钉群机器人 markdown 推送（`src/dingtalk.py`）
- GitHub Actions 每日 09:00 (UTC+8) 定时抓取并提交 data.json（`.github/workflows/update.yml`）
- 示例 data.json，保证 Pages 开启前页面也有内容可看
