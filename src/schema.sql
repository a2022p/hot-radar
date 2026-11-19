-- 热点雷达数据库结构（SQLite）
CREATE TABLE IF NOT EXISTS items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    source        TEXT NOT NULL,              -- 来源: github / hackernews / v2ex
    title         TEXT NOT NULL,              -- 标题
    url           TEXT NOT NULL UNIQUE,       -- 原文链接（去重键）
    heat          TEXT,                       -- 热度: stars today / points / 回复数
    extra         TEXT,                       -- 补充信息: 描述 / 评论数 / 节点
    summary       TEXT,                       -- AI 一句话摘要
    fetched_at    TEXT NOT NULL,              -- 最近抓取时间 (ISO8601, UTC+8)
    summarized_at TEXT                        -- AI 摘要生成时间
);

CREATE INDEX IF NOT EXISTS idx_items_source  ON items(source);
CREATE INDEX IF NOT EXISTS idx_items_fetched ON items(fetched_at);
