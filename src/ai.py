"""AI 模块：调用 DeepSeek 接口生成一句话摘要与每日简报。失败自动降级，不阻塞主流程。"""
import json
import os
import urllib.request

API = "https://api.deepseek.com/chat/completions"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")


def _chat(prompt, timeout=60):
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        raise RuntimeError("未设置 DEEPSEEK_API_KEY")
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
    }).encode("utf-8")
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def summarize(items):
    """items: [{id, source, title}, ...] -> {id: 一句话摘要}"""
    if not items:
        return {}
    lines = "\n".join(f"{i['id']}. [{i['source']}] {i['title']}" for i in items)
    prompt = (
        "你是科技资讯编辑。给下面每条热点标题写一句中文摘要（30字以内），"
        "说明它是什么、为什么火；英文标题先翻译大意再点评。\n"
        "严格输出 JSON 对象：键为编号、值为摘要，不要输出任何其他文字：\n" + lines
    )
    try:
        text = _chat(prompt).strip()
        text = text[text.find("{"): text.rfind("}") + 1]
        raw = json.loads(text)
        return {int(k): str(v) for k, v in raw.items()}
    except Exception as e:
        print(f"[ai] 摘要失败，降级为原标题: {e}")
        return {i["id"]: i["title"] for i in items}


def digest(items):
    """items: [{source, title, summary}, ...] -> 今日简报一段话"""
    if not items:
        return "今天没有抓到新热点。"
    lines = "\n".join(
        f"- [{i['source']}] {i['title']}: {i.get('summary') or ''}" for i in items[:20]
    )
    prompt = (
        "根据以下科技热点，用中文写一段120字以内的「今日简报」，语气轻松但信息量足，"
        "点出最值得关注的2-3个趋势：\n" + lines
    )
    try:
        return _chat(prompt).strip()
    except Exception as e:
        print(f"[ai] 简报失败，降级为统计句: {e}")
        return f"今天共收录 {len(items)} 条热点，详情见下方卡片。"
