"""推送模块：把每日简报推送到钉钉群机器人（webhook）。没配 webhook 就安静跳过。"""
import json
import os
import urllib.request


def push(digest_text, items, webhook=None):
    webhook = webhook or os.environ.get("DINGTALK_WEBHOOK", "")
    if not webhook:
        print("[dingtalk] 未设置 DINGTALK_WEBHOOK，跳过推送")
        return False
    top = "\n".join(f"- [{i['source']}] {i['title']}" for i in items[:5])
    text = f"### 📡 热点雷达日报\n\n{digest_text}\n\n**今日 Top5**\n\n{top}\n"
    body = json.dumps({
        "msgtype": "markdown",
        "markdown": {"title": "热点雷达日报", "text": text},
    }).encode("utf-8")
    req = urllib.request.Request(webhook, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        print("[dingtalk]", resp.read().decode("utf-8"))
    return True
