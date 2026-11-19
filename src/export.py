"""导出模块：把库里的数据写成网页要读的 data.json。"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

CST = timezone(timedelta(hours=8))


def export(items, digest_text, out_path="data.json"):
    payload = {
        "generated_at": datetime.now(CST).isoformat(timespec="seconds"),
        "digest": digest_text,
        "items": items,
    }
    Path(out_path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[export] 已写出 {out_path}，共 {len(items)} 条")
