#!/usr/bin/env python3
"""热点雷达主入口：抓取 -> 入库去重 -> AI 摘要 -> 导出网页数据 -> (可选)钉钉推送。

用法:
    python src/main.py                 # 抓取+AI+导出
    python src/main.py --no-ai         # 不调 DeepSeek，用降级文案
    python src/main.py --push          # 顺便推送钉钉群机器人
"""
import argparse
import os
from datetime import datetime, timedelta, timezone

import ai
import dingtalk
import export
import fetchers
import storage

CST = timezone(timedelta(hours=8))
HERE = os.path.dirname(os.path.abspath(__file__))


def load_env():
    """极简 .env 支持，不引入第三方依赖。"""
    env_path = os.path.join(HERE, "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main():
    ap = argparse.ArgumentParser(description="热点雷达：抓取+AI摘要+导出")
    ap.add_argument("--db", default=os.path.join(HERE, "radar.db"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "data.json"))
    ap.add_argument("--no-ai", action="store_true", help="不调用 DeepSeek，使用降级文案")
    ap.add_argument("--push", action="store_true", help="推送钉钉群机器人")
    ap.add_argument("--limit", type=int, default=60, help="导出条数上限")
    args = ap.parse_args()

    load_env()
    now = datetime.now(CST).isoformat(timespec="seconds")

    raw = fetchers.fetch_all()
    conn = storage.connect(args.db)
    storage.upsert(conn, raw, now)

    pend = storage.pending(conn)
    if pend and not args.no_ai:
        for pid, text in ai.summarize(pend).items():
            storage.set_summary(conn, pid, text, now)

    rows = storage.recent(conn, args.limit)
    if args.no_ai:
        digest_text = f"今天共收录 {len(rows)} 条热点（未启用 AI 摘要）。"
    else:
        digest_text = ai.digest(rows[:20])

    export.export(rows, digest_text, args.out)
    if args.push:
        dingtalk.push(digest_text, rows)
    conn.close()
    print("[done]", now)


if __name__ == "__main__":
    main()
