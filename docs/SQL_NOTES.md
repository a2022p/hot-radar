# SQL 笔记

数据库：SQLite（文件 `src/radar.db`，本地运行后生成；Actions 环境为临时库）。
表结构见 `src/schema.sql`。以下是在本项目里真实会用到的查询。

## 1. 今天新增了哪些热点

```sql
SELECT source, title, heat
FROM items
WHERE date(fetched_at) = date('now', 'localtime')
ORDER BY id DESC;
```

## 2. 各来源累计收录条数（检查爬虫是否都活着）

```sql
SELECT source, COUNT(*) AS total, MAX(fetched_at) AS last_seen
FROM items
GROUP BY source;
```

## 3. 还没有 AI 摘要的条目（摘要任务队列）

```sql
SELECT id, source, title
FROM items
WHERE summary IS NULL OR summary = '';
```

## 4. 最近 7 天热度最高的 GitHub 项目（修数据异常时用来核对）

```sql
SELECT title, heat, fetched_at
FROM items
WHERE source = 'github'
  AND fetched_at >= datetime('now', '-7 days')
ORDER BY CAST(REPLACE(REPLACE(heat, ' stars today', ''), ',', '') AS INTEGER) DESC
LIMIT 10;
```

> 说明：`heat` 存的是展示文本（如 "812 stars today"），排序时先清洗成数字。
> 如果以后要做更复杂的报表，会把热度拆成独立的数值列，这里先保持简单。
