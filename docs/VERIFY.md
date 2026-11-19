# 验证记录

每次改动后的验证方式与结果，保持"改了什么 → 怎么验的 → 结果如何"的习惯。

## 2026-11-19 · v0.1.0 初版验证

| 验证项 | 方式 | 结果 |
|---|---|---|
| 全部模块语法 | `python -m py_compile src/*.py` | ✅ 通过 |
| GitHub Trending 爬虫 | 本地真实运行 `python src/main.py --no-ai` | ✅ 抓到 15 条，标题/热度/描述字段齐全 |
| Hacker News 爬虫 | 同上（Algolia API） | ✅ 抓到 15 条，points/评论数字段齐全 |
| V2EX 爬虫 | 同上 | ⚠️ 本次本地网络超时；单源失败不影响整体（故障隔离生效），导出仍正常 |
| 故障隔离 | 观察 V2EX 超时后流程是否继续 | ✅ 其余来源正常入库并导出 |
| SQLite 去重 | 连续运行两次，检查第二次新增数 | ✅ 相同 URL 不重复插入，仅刷新热度 |
| 导出 data.json | 检查 JSON 结构与字段 | ✅ generated_at / digest / items 齐全 |
| AI 摘要与简报 | 需 DEEPSEEK_API_KEY，配置后运行 `python src/main.py` | 待配置 Key 后验证；无 Key 时 `--no-ai` 降级路径已验证 |
| 钉钉推送 | 需 DINGTALK_WEBHOOK，配置后运行 `--push` | 未配置时安静跳过已验证 |
| 网页看板 | 浏览器打开 index.html（本地 http.server） | ✅ 卡片渲染、来源筛选正常（示例数据） |

> 备注：V2EX 接口在部分网络环境较慢，超时时间 15s；如长期失败可在
> `src/fetchers.py` 的 `SOURCES` 中临时移除该来源，不影响其余功能。
