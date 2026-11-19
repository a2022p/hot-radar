"""抓取模块：从公开来源拉取热点列表。仅用 Python 标准库，零第三方依赖。"""
import html as html_lib
import json
import re
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) hot-radar/0.1"}


def _get(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def github_trending(limit=15):
    """GitHub 今日趋势榜（HTML 解析）"""
    page = _get("https://github.com/trending?since=daily")
    items = []
    blocks = re.findall(r'<article class="Box-row">(.*?)</article>', page, re.S)
    for b in blocks[:limit]:
        m = re.search(r'<h2[^>]*>.*?<a href="/([^"]+)"', b, re.S)
        if not m:
            continue
        repo = m.group(1).strip()
        d = re.search(r'<p class="col-9[^"]*">(.*?)</p>', b, re.S)
        desc = html_lib.unescape(re.sub(r"<[^>]+>", "", d.group(1))).strip() if d else ""
        s = re.search(r'([\d,]+)\s+stars today', b)
        items.append({
            "source": "github",
            "title": repo,
            "url": f"https://github.com/{repo}",
            "heat": f"{s.group(1)} stars today" if s else "",
            "extra": desc,
        })
    return items


def hackernews(limit=15):
    """Hacker News 首页（Algolia 官方 API，JSON）"""
    data = json.loads(_get("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"))
    items = []
    for h in data.get("hits", [])[:limit]:
        title = h.get("title") or ""
        if not title:
            continue
        items.append({
            "source": "hackernews",
            "title": title,
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
            "heat": f"{h.get('points', 0)} points",
            "extra": f"{h.get('num_comments', 0)} comments",
        })
    return items


def v2ex(limit=15):
    """V2EX 今日热帖（官方 API，JSON）"""
    data = json.loads(_get("https://www.v2ex.com/api/topics/hot.json"))
    items = []
    for t in data[:limit]:
        items.append({
            "source": "v2ex",
            "title": t.get("title", ""),
            "url": t.get("url", ""),
            "heat": f"{t.get('replies', 0)} 回复",
            "extra": (t.get("node") or {}).get("title", ""),
        })
    return [i for i in items if i["title"]]


SOURCES = {"github": github_trending, "hackernews": hackernews, "v2ex": v2ex}


def fetch_all():
    """抓取全部来源；单个来源失败不影响整体（运维思维：故障隔离）"""
    out = []
    for name, fn in SOURCES.items():
        try:
            got = fn()
            print(f"[fetch] {name}: {len(got)} 条")
            out.extend(got)
        except Exception as e:
            print(f"[fetch] {name} 失败: {e}")
    return out
