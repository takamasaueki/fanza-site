# =====================================================
# create_site.py
# SEO強化 完全版
# ・meta description
# ・OGP
# ・canonical
# ・JSON-LD
# ・関連記事
# ・パンくず
# ・sitemap.xml
# ・robots.txt
# =====================================================

import requests
import re
import os
import shutil
from collections import Counter

# =====================================================
# 設定
# =====================================================

API_ID = "D77Q7aTPWZhpKRnF0HSw"
AFF_ID = "takayanh-990"

BASE_URL = "https://example.com"

# =====================================================
# 出力フォルダ
# =====================================================

folders = [
    "genre",
    "item",
    "actress",
    "search"
]

# =====================================================
# 初期化
# =====================================================

for folder in folders:

    if os.path.exists(folder):

        shutil.rmtree(folder)

    os.makedirs(
        folder,
        exist_ok=True
    )

# =====================================================
# ジャンル
# =====================================================

genres = [
    ("", "index", "おすすめAVランキング"),
    ("巨乳", "big", "巨乳AVランキング"),
    ("人妻", "wife", "人妻AVランキング"),
    ("熟女", "mature", "熟女AVランキング"),
    ("中出し", "nakadashi", "中出しAVランキング"),
    ("制服", "uniform", "制服AVランキング"),
    ("ギャル", "gal", "ギャルAVランキング"),
]

# =====================================================
# URL管理
# =====================================================

all_urls = []

# =====================================================
# API
# =====================================================

def get_items(keyword="", hits=10, offset=1):

    url = "https://api.dmm.com/affiliate/v3/ItemList"

    params = {
        "api_id": API_ID,
        "affiliate_id": AFF_ID,
        "site": "FANZA",
        "service": "digital",
        "floor": "videoa",
        "hits": hits,
        "offset": offset,
        "keyword": keyword,
        "sort": "rank",
        "output": "json"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        data = response.json()

        return data.get(
            "result",
            {}
        ).get(
            "items",
            []
        )

    except Exception as e:

        print(e)

        return []

# =====================================================
# 安全ファイル名
# =====================================================

def safe_filename(text):

    text = re.sub(
        r'[\\/:*?"<>|]',
        '',
        text
    )

    return text[:80]

# =====================================================
# SEO description
# =====================================================

def make_description(text):

    text = re.sub(
        '<.*?>',
        '',
        text
    )

    return text[:120]

# =====================================================
# HTML開始
# =====================================================

def html_start(
    title,
    description="",
    canonical="",
    image=""
):

    return f"""
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1.0">

<title>{title}</title>

<meta name="description"
content="{description}">

<link rel="canonical"
href="{canonical}">

<meta property="og:title"
content="{title}">

<meta property="og:description"
content="{description}">

<meta property="og:image"
content="{image}">

<meta property="og:type"
content="website">

<meta property="og:url"
content="{canonical}">

<script type="application/ld+json">

{{
"@context":"https://schema.org",
"@type":"WebPage",
"name":"{title}",
"description":"{description}",
"url":"{canonical}"
}}

</script>

<style>

body {{
    background:#111;
    color:white;
    margin:0;
    font-family:Arial;
}}

a {{
    text-decoration:none;
}}

.header {{

    background:
    linear-gradient(
        90deg,
        #ff6600,
        #ff0033
    );

    padding:15px 20px;

    position:sticky;

    top:0;

    z-index:999;
}}

.header-inner {{

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:20px;
}}

.logo {{

    font-size:30px;

    font-weight:bold;
}}

.container {{
    width:1300px;
    margin:20px auto;
}}

.layout {{
    display:flex;
    gap:20px;
    align-items:flex-start;
}}

.sidebar {{

    width:220px;

    background:#1b1b1b;

    padding:15px;

    border-radius:12px;

    position:sticky;

    top:90px;

    max-height:calc(100vh - 100px);

    overflow-y:auto;
}}

.sidebar::-webkit-scrollbar {{
    width:6px;
}}

.sidebar::-webkit-scrollbar-thumb {{
    background:#444;
}}

.sidebar-title {{
    font-size:20px;
    margin-bottom:15px;
}}

.sidebar a {{

    display:block;

    background:#222;

    color:white;

    padding:10px;

    border-radius:8px;

    margin-bottom:8px;
}}

.sidebar a:hover {{
    background:#ff6600;
}}

.main {{
    flex:1;
}}

.card {{

    display:flex;

    gap:20px;

    background:#1b1b1b;

    padding:20px;

    border-radius:12px;

    margin-bottom:20px;
}}

.card img {{
    border-radius:10px;
}}

.info {{
    flex:1;
}}

.info p {{
    color:#ccc;
    line-height:1.7;
}}

.btn {{

    display:inline-block;

    background:#ff0033;

    color:white;

    padding:12px 20px;

    border-radius:8px;

    margin-top:10px;
}}

.btn:hover {{
    background:#ff3366;
}}

.grid {{

    display:grid;

    grid-template-columns:
    repeat(auto-fill,minmax(220px,1fr));

    gap:20px;
}}

.grid-card {{

    background:#1b1b1b;

    border-radius:12px;

    overflow:hidden;
}}

.grid-card img {{
    width:100%;
}}

.grid-info {{
    padding:12px;
}}

.breadcrumb {{

    margin-bottom:20px;

    color:#aaa;
}}

.related-title {{

    margin-top:60px;

    font-size:28px;
}}

@media screen and (max-width:768px) {{

    .container {{
        width:95%;
    }}

    .layout {{
        flex-direction:column;
    }}

    .sidebar {{
        width:auto;
        position:static;
        max-height:none;
    }}

    .card {{
        flex-direction:column;
    }}

    .card img {{
        width:100%;
        height:auto;
    }}

}}

</style>

</head>

<body>

<div class="header">

<div class="header-inner">

<div class="logo">
きょうはこれでいいや。
</div>

</div>

</div>

<div class="container">

<div class="layout">

<div class="sidebar">

<div class="sidebar-title">
ジャンル
</div>
"""

# =====================================================
# サイドバー
# =====================================================

def create_sidebar():

    html = ""

    for keyword, filename, title in genres:

        html += f"""
<a href="../genre/{filename}_1.html">
{title}
</a>
"""

    html += """
<div class="sidebar-title"
style="margin-top:30px;">
人気女優
</div>
"""

    for actress in popular_actresses[:30]:

        actress_file = safe_filename(actress)

        html += f"""
<a href="../actress/{actress_file}.html">
{actress}
</a>
"""

    return html

# =====================================================
# HTML終了
# =====================================================

def html_end():

    return """
</div>
</div>
</div>
</body>
</html>
"""

# =====================================================
# 女優収集
# =====================================================

actress_counter = Counter()

all_items = get_items("", hits=100)

for item in all_items:

    actresses = item.get(
        "iteminfo",
        {}
    ).get(
        "actress",
        []
    )

    for actress in actresses:

        name = actress.get(
            "name",
            ""
        )

        if name:

            actress_counter[name] += 1

popular_actresses = [
    name
    for name, count
    in actress_counter.most_common(100)
]

# =====================================================
# 作品ページ
# =====================================================

def create_item_page(item):

    title = item.get("title", "")

    safe_title = safe_filename(title)

    filename = f"item/{safe_title}.html"

    canonical = f"{BASE_URL}/{filename}"

    all_urls.append(canonical)

    affiliate_url = item.get(
        "affiliateURL",
        "#"
    )

    image = item.get(
        "imageURL",
        {}
    )

    img = (
        image.get("large")
        or image.get("small")
        or ""
    )

    actresses = item.get(
        "iteminfo",
        {}
    ).get(
        "actress",
        []
    )

    actress_links = ""

    for actress in actresses:

        name = actress.get(
            "name",
            ""
        )

        actress_file = safe_filename(name)

        actress_links += f"""
<a
href="../actress/{actress_file}.html"
style="color:#ffcc66;margin-right:10px;">
{name}
</a>
"""

    comment = item.get(
        "iteminfo",
        {}
    ).get(
        "comment",
        ""
    )

    description = make_description(comment)

    html = html_start(
        title=f"{title}｜人気AVレビュー",
        description=description,
        canonical=canonical,
        image=img
    )

    html += create_sidebar()

    html += f"""
</div>

<div class="main">

<div class="breadcrumb">
TOP ＞ 作品ページ ＞ {title}
</div>

<h1>{title}</h1>

<div class="card">

<img src="{img}" width="350">

<div class="info">

<p>
{actress_links}
</p>

<p>
{description}
</p>

<a
class="btn"
href="{affiliate_url}">
▶ FANZAで見る
</a>

</div>

</div>

<div class="related-title">
関連記事
</div>
"""

    related_items = get_items(
        "",
        hits=6
    )

    html += """
<div class="grid">
"""

    for rel in related_items:

        rel_title = rel.get(
            "title",
            ""
        )

        rel_img = rel.get(
            "imageURL",
            {}
        )

        rel_image = (
            rel_img.get("large")
            or rel_img.get("small")
            or ""
        )

        rel_page = create_item_page_simple(rel)

        html += f"""
<div class="grid-card">

<img src="{rel_image}">

<div class="grid-info">

<p>
{rel_title[:40]}
</p>

<a
class="btn"
href="../{rel_page}">
▶ 詳細
</a>

</div>

</div>
"""

    html += """
</div>
</div>
"""

    html += html_end()

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    return filename

# =====================================================
# 簡易作品ページ
# =====================================================

def create_item_page_simple(item):

    title = item.get("title", "")

    safe_title = safe_filename(title)

    return f"item/{safe_title}.html"

# =====================================================
# sitemap
# =====================================================

def create_sitemap():

    xml = """<?xml version="1.0" encoding="UTF-8"?>

<urlset
xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for url in all_urls:

        xml += f"""
<url>
<loc>{url}</loc>
</url>
"""

    xml += """
</urlset>
"""

    with open(
        "sitemap.xml",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(xml)

# =====================================================
# robots.txt
# =====================================================

def create_robots():

    robots = f"""
User-agent: *

Allow: /

Sitemap:
{BASE_URL}/sitemap.xml
"""

    with open(
        "robots.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(robots)

# =====================================================
# 実行
# =====================================================

items = get_items("", hits=30)

for item in items:

    create_item_page(item)

create_sitemap()

create_robots()

print("SEO強化サイト生成完了")