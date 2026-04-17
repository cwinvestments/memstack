#!/usr/bin/env python3
"""
Live SEO/GEO audit — Python stdlib only, no API keys, no pip installs.

Fetches a deployed URL and checks title, meta description, heading
hierarchy, image alt attributes, JSON-LD, canonical, Open Graph,
robots meta, viewport, robots.txt (with AI bot rules), sitemap.xml,
page load time, and link composition. Prints a severity-tagged
scorecard matching the memstack seo-geo/site-audit skill format.

Usage: python live_audit.py https://example.com

Exit codes: 0 = pass, 1 = high-severity issues, 2 = critical issues.
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser


USER_AGENT = "MemStack-SiteAudit/1.0 (+https://memstack.pro)"
FETCH_TIMEOUT = 30
AI_BOTS = [
    "GPTBot",
    "ChatGPT-User",
    "PerplexityBot",
    "ClaudeBot",
    "anthropic-ai",
    "Google-Extended",
]


def fetch(url, method="GET", timeout=FETCH_TIMEOUT):
    """Return (status, headers_dict, body, elapsed_sec) or 4x None on error."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
            method=method,
        )
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace") if method == "GET" else ""
            elapsed = time.time() - start
            return resp.status, dict(resp.headers), body, elapsed
    except Exception:
        return None, None, None, None


class PageParser(HTMLParser):
    """Single-pass extractor for title, meta, headings, images, links, JSON-LD."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self._title_buf = []
        self.meta = []
        self.headings = []
        self._cur_h = None
        self._h_buf = []
        self.images = []
        self.links = []
        self.jsonld_blocks = []
        self._in_jsonld = False
        self._jsonld_buf = []
        self.canonical = None
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
            self._title_buf = []
        elif tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            if (a.get("rel") or "").lower() == "canonical":
                self.canonical = a.get("href")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cur_h = int(tag[1])
            self._h_buf = []
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt")})
        elif tag == "a":
            if a.get("href"):
                self.links.append(a["href"])
        elif tag == "script":
            if (a.get("type") or "").lower() == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = []
        elif tag == "html":
            self.lang = a.get("lang")

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self.title = "".join(self._title_buf).strip()
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._cur_h is not None:
            self.headings.append((self._cur_h, "".join(self._h_buf).strip()))
            self._cur_h = None
        elif tag == "script" and self._in_jsonld:
            self.jsonld_blocks.append("".join(self._jsonld_buf))
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title:
            self._title_buf.append(data)
        if self._cur_h is not None:
            self._h_buf.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)


def meta_content(meta_list, **kwargs):
    """Find first meta tag where all kwargs match (case-insensitive). Return content or None."""
    for m in meta_list:
        if all((m.get(k) or "").lower() == v.lower() for k, v in kwargs.items()):
            return m.get("content")
    return None


def check_title(p):
    if not p.title:
        return [("CRITICAL", "Missing <title> tag")], "missing"
    n = len(p.title)
    if n < 30:
        return [("MEDIUM", f"Title too short ({n} chars; 50-60 ideal)")], f"{n} chars"
    if n > 70:
        return [("MEDIUM", f"Title too long ({n} chars; likely truncated in SERP)")], f"{n} chars"
    return [], f"{n} chars"


def check_description(p):
    desc = meta_content(p.meta, name="description")
    if not desc:
        return [("HIGH", "Missing meta description")], "missing"
    n = len(desc)
    if n < 100:
        return [("MEDIUM", f"Description too short ({n} chars; 150-160 ideal)")], f"{n} chars"
    if n > 170:
        return [("MEDIUM", f"Description too long ({n} chars; likely truncated)")], f"{n} chars"
    return [], f"{n} chars"


def check_headings(p):
    issues = []
    levels = [h[0] for h in p.headings]
    h1 = levels.count(1)
    if h1 == 0:
        issues.append(("CRITICAL", "No <h1> tag found"))
    elif h1 > 1:
        issues.append(("HIGH", f"Multiple <h1> tags ({h1}); should be exactly 1"))
    # Flag skipped levels (e.g., h1 followed by h3 with no h2 between)
    seen_max = 0
    for lvl in levels:
        if lvl > seen_max + 1 and seen_max != 0:
            issues.append(("MEDIUM", f"Heading hierarchy skips from h{seen_max} to h{lvl}"))
        if lvl > seen_max:
            seen_max = lvl
    summary = f"h1:{h1}, h2:{levels.count(2)}, h3:{levels.count(3)}, h4+:{sum(1 for l in levels if l >= 4)}"
    return issues, summary


def check_images(p):
    total = len(p.images)
    if total == 0:
        return [], "no <img> elements"
    missing = [img for img in p.images if img.get("alt") is None]
    empty = [img for img in p.images if img.get("alt") == ""]
    issues = []
    if missing:
        sev = "MEDIUM" if len(missing) < 5 else "HIGH"
        srcs = ", ".join(img["src"][:60] for img in missing[:3])
        issues.append((sev, f"{len(missing)}/{total} images missing alt attribute (e.g. {srcs})"))
    if empty and not missing:
        issues.append(("LOW", f"{len(empty)}/{total} images have empty alt (decorative or unlabeled)"))
    return issues, f"{total} images, {len(missing)} missing alt, {len(empty)} empty alt"


def check_jsonld(p):
    if not p.jsonld_blocks:
        return [("MEDIUM", "No JSON-LD structured data found")], "none"
    types = []
    issues = []
    for block in p.jsonld_blocks:
        try:
            data = json.loads(block.strip())
        except Exception:
            issues.append(("MEDIUM", "Invalid JSON in application/ld+json block"))
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            graph = item.get("@graph")
            if isinstance(graph, list):
                for g in graph:
                    if isinstance(g, dict) and g.get("@type"):
                        types.append(str(g["@type"]))
            elif item.get("@type"):
                types.append(str(item["@type"]))
    summary = f"{len(p.jsonld_blocks)} block(s): {', '.join(types) if types else 'no @type'}"
    return issues, summary


def check_canonical(p, url):
    if not p.canonical:
        return [("MEDIUM", "No canonical URL tag")], "missing"
    c = p.canonical.rstrip("/")
    u = url.rstrip("/")
    if c != u:
        return [("LOW", f"Canonical differs from fetched URL: {p.canonical}")], p.canonical
    return [], p.canonical


def check_og(p):
    present = []
    missing = []
    for tag in ("og:title", "og:description", "og:image"):
        if meta_content(p.meta, property=tag):
            present.append(tag)
        else:
            missing.append(tag)
    issues = []
    if missing:
        sev = "LOW" if len(missing) < 3 else "MEDIUM"
        issues.append((sev, f"Missing Open Graph tags: {', '.join(missing)}"))
    return issues, f"{len(present)}/3 present ({', '.join(present) or 'none'})"


def check_robots_meta(p):
    content = meta_content(p.meta, name="robots")
    if not content:
        return [], "default (indexable)"
    if "noindex" in content.lower():
        return [("HIGH", "robots meta contains 'noindex' — page excluded from search")], content
    return [], content


def check_viewport(p):
    vp = meta_content(p.meta, name="viewport")
    if not vp:
        return [("HIGH", "Missing viewport meta tag (hurts mobile ranking)")], "missing"
    return [], vp


def _looks_like_html(body):
    """Return True if body looks like an HTML page (common auth-redirect failure mode)."""
    if not body:
        return False
    head = body[:500].lstrip().lower()
    return head.startswith("<!doctype html") or head.startswith("<html") or "<!doctype html" in head


def _content_type(headers):
    """Extract content-type value (lowercased, no parameters) from a headers dict."""
    if not headers:
        return ""
    # urllib returns header keys in their original case; match case-insensitively.
    for key, value in headers.items():
        if key.lower() == "content-type":
            return str(value).split(";")[0].strip().lower()
    return ""


def check_robots_txt(base_url):
    parsed = urllib.parse.urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    status, headers, body, _ = fetch(robots_url)
    if status != 200 or not body:
        return [("HIGH", "robots.txt not found or unreachable")], "missing"

    ctype = _content_type(headers)
    # Common failure mode: auth middleware intercepts /robots.txt and returns login HTML
    # with status 200. A naive "status == 200" check would mark this 'present'.
    if _looks_like_html(body) or ctype == "text/html":
        return [
            ("HIGH", f"robots.txt returned HTML instead of plain text (content-type: {ctype or 'unknown'}) — likely an auth redirect or route misconfig intercepting /robots.txt; crawlers cannot read the rules"),
        ], "broken (HTML response)"

    # Shape check: a real robots.txt has at least one User-agent directive
    lc = body.lower()
    if "user-agent:" not in lc:
        return [
            ("HIGH", "robots.txt reachable but contains no 'User-agent:' directive — not a valid robots.txt response"),
        ], "broken (no User-agent directive)"

    mentioned = [b for b in AI_BOTS if b.lower() in lc]
    issues = []
    if not mentioned:
        issues.append(("MEDIUM", f"robots.txt has no explicit AI bot rules ({', '.join(AI_BOTS)})"))
    return issues, f"present; AI bots mentioned: {', '.join(mentioned) if mentioned else 'none'}"


def check_sitemap(base_url):
    parsed = urllib.parse.urlparse(base_url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    status, headers, body, _ = fetch(sitemap_url)
    if status != 200 or not body:
        return [("HIGH", "sitemap.xml not found")], "missing"

    ctype = _content_type(headers)
    # Same auth-redirect failure mode as robots.txt
    if _looks_like_html(body) or ctype == "text/html":
        return [
            ("HIGH", f"sitemap.xml returned HTML instead of XML (content-type: {ctype or 'unknown'}) — likely an auth redirect or route misconfig intercepting /sitemap.xml; search engines cannot discover pages"),
        ], "broken (HTML response)"

    # Shape check: must contain <urlset> or <sitemapindex>
    body_lc = body.lower()
    if "<urlset" not in body_lc and "<sitemapindex" not in body_lc:
        return [
            ("HIGH", "sitemap.xml reachable but contains no <urlset> or <sitemapindex> — not a valid XML sitemap"),
        ], "broken (not a valid sitemap)"

    return [], "present"


def check_load_time(elapsed):
    if elapsed is None:
        return [], "unknown"
    if elapsed > 3.0:
        return [("HIGH", f"Page load {elapsed:.2f}s exceeds 3s target")], f"{elapsed:.2f}s"
    if elapsed > 2.0:
        return [("MEDIUM", f"Page load {elapsed:.2f}s (target <2s)")], f"{elapsed:.2f}s"
    return [], f"{elapsed:.2f}s"


def count_links(p, base_url):
    base_host = urllib.parse.urlparse(base_url).netloc.lower()
    internal = external = anchor = 0
    for href in p.links:
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            anchor += 1
            continue
        host = urllib.parse.urlparse(href).netloc.lower()
        if host and host != base_host:
            external += 1
        else:
            internal += 1
    return internal, external, anchor


EMOJI = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, Exception):
        pass
    ap = argparse.ArgumentParser(description="Live SEO/GEO audit (stdlib only)")
    ap.add_argument("url", help="URL to audit (https:// prepended if omitted)")
    args = ap.parse_args()

    url = args.url if args.url.startswith("http") else "https://" + args.url

    print("🔎 Site Audit — Live URL Scan")
    print("")
    print(f"Target: {url}")

    status, headers, body, elapsed = fetch(url)
    if not body:
        print(f"\n❌ FAILED to fetch {url} (status={status})")
        sys.exit(3)
    print(f"Status: {status}")
    print("")

    page = PageParser()
    try:
        page.feed(body)
    except Exception as e:
        print(f"⚠️  HTML parse warning: {e}\n")

    checks = [
        ("Title",       check_title(page)),
        ("Description", check_description(page)),
        ("Headings",    check_headings(page)),
        ("Images",      check_images(page)),
        ("JSON-LD",     check_jsonld(page)),
        ("Canonical",   check_canonical(page, url)),
        ("Open Graph",  check_og(page)),
        ("Robots meta", check_robots_meta(page)),
        ("Viewport",    check_viewport(page)),
        ("Load time",   check_load_time(elapsed)),
        ("robots.txt",  check_robots_txt(url)),
        ("sitemap.xml", check_sitemap(url)),
    ]

    internal, external, anchor = count_links(page, url)
    checks.append(("Links", ([], f"{internal} internal, {external} external, {anchor} anchor/other")))

    all_issues = []
    for _name, (issues, _summary) in checks:
        all_issues.extend(issues)

    print("## Checks\n")
    for name, (issues, summary) in checks:
        mark = "✅" if not issues else "⚠️ "
        print(f"{mark} {name}: {summary}")
    print("")

    if all_issues:
        print("## Issues (by severity)\n")
        for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            for s, m in [i for i in all_issues if i[0] == sev]:
                print(f"  {EMOJI[s]} {s}: {m}")
        print("")

    crit = sum(1 for i in all_issues if i[0] == "CRITICAL")
    high = sum(1 for i in all_issues if i[0] == "HIGH")
    med = sum(1 for i in all_issues if i[0] == "MEDIUM")
    low = sum(1 for i in all_issues if i[0] == "LOW")
    score = max(0, 100 - (crit * 20 + high * 10 + med * 4 + low * 1))

    print("## Summary\n")
    print(f"  Overall score: {score}/100")
    print(f"  🔴 Critical: {crit}    🟠 High: {high}    🟡 Medium: {med}    🔵 Low: {low}")
    print(f"  Total issues: {len(all_issues)}")
    print("")
    print("🔎 Site Audit — Complete")

    if crit > 0:
        sys.exit(2)
    if high > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
