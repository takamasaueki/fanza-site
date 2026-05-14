# create_site.py
# 完成形テンプレート（API ID / affiliate ID を自分の値に置き換え）
import os
import requests
from pathlib import Path
from datetime import datetime

# =====================
# 設定（ここを書き換え）
# =====================
API_ID = "D77Q7aTPWZhpKRnF0HSw"
AFFILIATE_ID = "takayanh-990"
SITE_URL = "http://eromatrix.com/"
SITE_NAME = "きょうはこれでいいや。"

BASE_API = "https://api.dmm.com/affiliate/v3/ItemList"
ROOT = Path(".")
for d in ["genre", "item", "actress", "search", "articles"]:
    (ROOT / d).mkdir(exist_ok=True)

ARTICLES = [
    ("av-actress-ranking-2026", "2026年人気AV女優ランキング", "注目女優まとめ"),
    ("beginner-recommend", "初心者向けおすすめジャンル", "人気ジャンル紹介"),
    ("popular-genre", "人気ジャンルまとめ", "定番ジャンルまとめ"),
]

ACTRESSES = ["三上悠亜", "河北彩花", "葵つかさ", "深田えいみ", "明日花キララ"]
GENRES = ["巨乳", "人妻", "制服", "中出し", "企画"]


def fetch_items(keyword="人気", hits=20):
    params = {
        "api_id": API_ID,
        "affiliate_id": AFFILIATE_ID,
        "site": "FANZA",
        "service": "digital",
        "floor": "videoa",
        "keyword": keyword,
        "hits": hits,
        "output": "json",
    }
    try:
        r = requests.get(BASE_API, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data.get("result", {}).get("items", [])
    except Exception:
        return []


def page(title, body):
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><style>body{{font-family:sans-serif;max-width:1100px;margin:auto;padding:20px;background:#fafafa}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}} .card{{background:#fff;padding:12px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.08)}} img{{max-width:100%;border-radius:8px}} a{{text-decoration:none;color:#c2185b}} .header{{font-size:32px;font-weight:700;margin-bottom:16px}}</style></head><body><div class="header">{SITE_NAME}</div>{body}</body></html>'''


def write(path, content):
    Path(path).write_text(content, encoding="utf-8")


def create_home(items):
    cards = []
    for item in items:
        title = item.get("title", "作品")
        url = item.get("affiliateURL") or item.get("URL") or "#"
        image = item.get("imageURL", {}).get("large") or ""
        cards.append(f'<div class="card"><a href="{url}" target="_blank">' + (f'<img src="{image}">' if image else '') + f'<p>{title}</p></a></div>')
    body = f'<p><a href="/articles/index.html">記事一覧</a> | <a href="/actress/index.html">女優一覧</a> | <a href="/genre/index.html">ジャンル一覧</a></p><div class="grid">{"".join(cards)}</div>'
    write("index.html", page(SITE_NAME, body))


def create_list_pages():
    actress_links = []
    for name in ACTRESSES:
        slug = f"actress/{name}.html"
        write(slug, page(name, f"<h1>{name}</h1><p>代表作・人気作品紹介ページ</p><p><a href=\"/\">トップへ戻る</a></p>"))
        actress_links.append(f'<li><a href="{name}.html">{name}</a></li>')
    write("actress/index.html", page("女優一覧", f"<ul>{''.join(actress_links)}</ul>"))

    genre_links = []
    for name in GENRES:
        slug = f"genre/{name}.html"
        write(slug, page(name, f"<h1>{name}</h1><p>{name}ジャンル作品一覧</p><p><a href=\"/\">トップへ戻る</a></p>"))
        genre_links.append(f'<li><a href="{name}.html">{name}</a></li>')
    write("genre/index.html", page("ジャンル一覧", f"<ul>{''.join(genre_links)}</ul>"))


def create_articles():
    links = []
    for slug, title, desc in ARTICLES:
        html = page(title, f"<h1>{title}</h1><p>{desc}</p><p>更新日: {datetime.now().strftime('%Y-%m-%d')}</p><p><a href='/'>トップへ戻る</a></p>")
        write(f"articles/{slug}.html", html)
        links.append(f'<li><a href="{slug}.html">{title}</a></li>')
    write("articles/index.html", page("記事一覧", f"<ul>{''.join(links)}</ul>"))


def create_seo_files():
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "/sitemap.xml")
    urls = ["/", "/articles/index.html", "/actress/index.html", "/genre/index.html"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append(f"<url><loc>{SITE_URL}{u}</loc></url>")
    xml.append("</urlset>")
    write("sitemap.xml", "\n".join(xml))


def main():
    items = fetch_items()
    create_home(items)
    create_list_pages()
    create_articles()
    create_seo_files()
    print("生成完了")

if __name__ == "__main__":
    main()
