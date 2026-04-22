#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          🌐  Interactive Web Scraper Tool  🌐                ║
║        Ethical · Modular · Clean · User-Friendly             ║
╠══════════════════════════════════════════════════════════════╣
║  SOURCES:                                                    ║
║   • quotes.toscrape.com   — Famous Quotes                   ║
║   • books.toscrape.com    — Books & Prices                   ║
║   • news.ycombinator.com  — Tech / Hacker News               ║
║   • Any custom URL        — Generic extractor                ║
╚══════════════════════════════════════════════════════════════╝
"""

import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
from datetime import datetime
import random


# ─── ANSI COLOURS ────────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    DIM     = "\033[2m"
    WHITE   = "\033[97m"

def bold(t):    return f"{C.BOLD}{t}{C.RESET}"
def cyan(t):    return f"{C.CYAN}{t}{C.RESET}"
def green(t):   return f"{C.GREEN}{t}{C.RESET}"
def yellow(t):  return f"{C.YELLOW}{t}{C.RESET}"
def red(t):     return f"{C.RED}{t}{C.RESET}"
def magenta(t): return f"{C.MAGENTA}{t}{C.RESET}"
def dim(t):     return f"{C.DIM}{t}{C.RESET}"
def blue(t):    return f"{C.BLUE}{t}{C.RESET}"


# ─── UI HELPERS ───────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=64, color=C.DIM):
    print(f"{color}{char * width}{C.RESET}")

def banner():
    clear()
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════╗
║          🌐  Interactive Web Scraper Tool  🌐                ║
║        Ethical · Modular · Clean · User-Friendly             ║
╚══════════════════════════════════════════════════════════════╝{C.RESET}
""")

def section_header(title, emoji="📌"):
    print()
    divider("═")
    print(f"  {emoji}  {bold(cyan(title))}")
    divider("═")

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def success(m): print(f"  {green('✔')}  {m}")
def warn(m):    print(f"  {yellow('⚠')}  {yellow(m)}")
def error(m):   print(f"  {red('✘')}  {red(m)}")
def info(m):    print(f"  {blue('ℹ')}  {dim(m)}")


# ─── NETWORK ─────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def fetch(url: str, timeout: int = 12):
    """Return BeautifulSoup or None."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except requests.exceptions.MissingSchema:
        error("Invalid URL — it must start with http:// or https://")
    except requests.exceptions.ConnectionError:
        error("Cannot connect. Check your internet connection or the URL.")
    except requests.exceptions.Timeout:
        error("Request timed out — the site may be down or too slow.")
    except requests.exceptions.HTTPError as e:
        error(f"HTTP {e.response.status_code} error.")
    except Exception as e:
        error(f"Unexpected error: {e}")
    return None


# ─── DEMO DATA ────────────────────────────────────────────────────────────────

DEMO_QUOTES = [
    {"quote": "The only way to do great work is to love what you do.",
     "author": "Steve Jobs", "tags": "inspirational, work, passion"},
    {"quote": "In the middle of every difficulty lies opportunity.",
     "author": "Albert Einstein", "tags": "motivation, wisdom"},
    {"quote": "It does not matter how slowly you go as long as you do not stop.",
     "author": "Confucius", "tags": "perseverance, wisdom"},
    {"quote": "Life is what happens when you're busy making other plans.",
     "author": "John Lennon", "tags": "life, philosophy"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.",
     "author": "Eleanor Roosevelt", "tags": "dreams, future"},
    {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
     "author": "Winston Churchill", "tags": "courage, success"},
    {"quote": "Imagination is more important than knowledge.",
     "author": "Albert Einstein", "tags": "creativity, knowledge"},
    {"quote": "It always seems impossible until it's done.",
     "author": "Nelson Mandela", "tags": "perseverance, inspiration"},
    {"quote": "The best time to plant a tree was 20 years ago. The second best time is now.",
     "author": "Chinese Proverb", "tags": "wisdom, action"},
    {"quote": "Strive not to be a success, but rather to be of value.",
     "author": "Albert Einstein", "tags": "success, value"},
    {"quote": "Two roads diverged in a wood, and I took the one less traveled by.",
     "author": "Robert Frost", "tags": "choices, life"},
    {"quote": "You miss 100% of the shots you don't take.",
     "author": "Wayne Gretzky", "tags": "motivation, sports"},
]

DEMO_BOOKS = [
    {"title": "A Light in the Attic",             "price": "£51.77", "rating": "⭐⭐⭐",     "avail": "In stock"},
    {"title": "Tipping the Velvet",               "price": "£53.74", "rating": "⭐",         "avail": "In stock"},
    {"title": "Soumission",                        "price": "£50.10", "rating": "⭐",         "avail": "In stock"},
    {"title": "Sharp Objects",                     "price": "£47.82", "rating": "⭐⭐⭐⭐",    "avail": "In stock"},
    {"title": "Sapiens: A Brief History",          "price": "£54.23", "rating": "⭐⭐⭐⭐⭐",  "avail": "In stock"},
    {"title": "The Midnight Library",              "price": "£29.99", "rating": "⭐⭐⭐⭐⭐",  "avail": "In stock"},
    {"title": "Atomic Habits",                     "price": "£14.99", "rating": "⭐⭐⭐⭐⭐",  "avail": "In stock"},
    {"title": "The Hitchhiker's Guide to Galaxy",  "price": "£11.99", "rating": "⭐⭐⭐⭐⭐",  "avail": "In stock"},
    {"title": "1984",                              "price": "£8.99",  "rating": "⭐⭐⭐⭐⭐",  "avail": "In stock"},
    {"title": "To Kill a Mockingbird",             "price": "£9.49",  "rating": "⭐⭐⭐⭐",   "avail": "In stock"},
    {"title": "Brave New World",                   "price": "£7.99",  "rating": "⭐⭐⭐⭐",   "avail": "In stock"},
    {"title": "The Great Gatsby",                  "price": "£6.99",  "rating": "⭐⭐⭐",     "avail": "In stock"},
]

DEMO_NEWS = [
    {"title": "OpenAI Releases New Model with Enhanced Reasoning",
     "url": "https://openai.com", "score": "432 points", "source": "openai.com"},
    {"title": "Rust Overtakes C++ in Systems Programming Survey 2026",
     "url": "https://survey.dev", "score": "318 points", "source": "survey.dev"},
    {"title": "Linux Kernel 7.0 Released with Major Performance Improvements",
     "url": "https://kernel.org", "score": "290 points", "source": "kernel.org"},
    {"title": "Python 3.14 Brings Free-Threaded Mode to Production",
     "url": "https://python.org", "score": "275 points", "source": "python.org"},
    {"title": "New Study: Remote Work Boosts Developer Productivity by 22%",
     "url": "https://hbr.org",   "score": "241 points", "source": "hbr.org"},
    {"title": "WebAssembly 3.0 Spec Finalised — Runs in Every Major Browser",
     "url": "https://webassembly.org", "score": "198 points", "source": "webassembly.org"},
    {"title": "EU AI Act Enforcement Begins: What Developers Need to Know",
     "url": "https://techcrunch.com", "score": "187 points", "source": "techcrunch.com"},
    {"title": "Ask HN: What's Your Go-To Stack in 2026?",
     "url": "https://news.ycombinator.com", "score": "166 points", "source": "news.ycombinator.com"},
    {"title": "GitHub Copilot Now Supports Voice Coding on macOS",
     "url": "https://github.blog", "score": "154 points", "source": "github.blog"},
    {"title": "Cloudflare Workers Now Support Python Natively",
     "url": "https://blog.cloudflare.com", "score": "143 points", "source": "blog.cloudflare.com"},
]


def apply_filters(items, keyword, limit):
    if keyword:
        items = [i for i in items
                 if keyword.lower() in " ".join(str(v) for v in i.values()).lower()]
    return items[:limit]


# ─── LIVE SCRAPERS ────────────────────────────────────────────────────────────

def live_scrape_quotes(limit, keyword):
    results, page = [], 1
    while len(results) < limit:
        soup = fetch(f"http://quotes.toscrape.com/page/{page}/")
        if not soup:
            return []
        cards = soup.select("div.quote")
        if not cards:
            break
        for card in cards:
            if len(results) >= limit:
                break
            t = card.select_one("span.text")
            a = card.select_one("small.author")
            tags = [tg.get_text() for tg in card.select("a.tag")]
            if t and a:
                q = {"quote":  t.get_text(strip=True).strip('\u201c\u201d"\''),
                     "author": a.get_text(strip=True),
                     "tags":   ", ".join(tags)}
                if keyword and keyword.lower() not in q["quote"].lower() \
                           and keyword.lower() not in q["author"].lower():
                    continue
                results.append(q)
        page += 1
    return results


def live_scrape_books(limit, keyword):
    results, page = [], 1
    star = {"One":"⭐","Two":"⭐⭐","Three":"⭐⭐⭐","Four":"⭐⭐⭐⭐","Five":"⭐⭐⭐⭐⭐"}
    while len(results) < limit:
        soup = fetch(f"http://books.toscrape.com/catalogue/page-{page}.html")
        if not soup:
            return []
        cards = soup.select("article.product_pod")
        if not cards:
            break
        for card in cards:
            if len(results) >= limit:
                break
            title_tag = card.select_one("h3 a")
            price_tag = card.select_one("p.price_color")
            avail_tag = card.select_one("p.availability")
            rat_tag   = card.select_one("p.star-rating")
            rat_word  = rat_tag["class"][1] if rat_tag else "One"
            if title_tag and price_tag:
                b = {"title":  title_tag["title"],
                     "price":  price_tag.get_text(strip=True),
                     "rating": star.get(rat_word, "?"),
                     "avail":  avail_tag.get_text(strip=True) if avail_tag else "N/A"}
                if keyword and keyword.lower() not in b["title"].lower():
                    continue
                results.append(b)
        page += 1
    return results


def live_scrape_news(limit, keyword):
    soup = fetch("https://news.ycombinator.com/")
    if not soup:
        return []
    results = []
    for row in soup.select("tr.athing"):
        if len(results) >= limit:
            break
        ta  = row.select_one("span.titleline > a")
        sub = row.find_next_sibling("tr")
        sc  = sub.select_one("span.score") if sub else None
        si  = row.select_one("span.sitestr")
        if ta:
            item = {"title":  ta.get_text(strip=True),
                    "url":    ta.get("href", "N/A"),
                    "score":  sc.get_text(strip=True) if sc else "N/A",
                    "source": si.get_text(strip=True) if si else "N/A"}
            if keyword and keyword.lower() not in item["title"].lower():
                continue
            results.append(item)
    return results


def live_scrape_custom(url, limit, keyword):
    soup = fetch(url)
    if not soup:
        return []
    results = []
    for tag in soup.find_all(["h1", "h2", "h3", "p"]):
        if len(results) >= limit:
            break
        text = tag.get_text(strip=True)
        if len(text) < 20:
            continue
        if keyword and keyword.lower() not in text.lower():
            continue
        results.append({"type": tag.name.upper(), "text": text})
    return results


def smart_scrape(mode, limit, keyword, url=""):
    """Try live first; fall back to demo. Returns (items, is_demo)."""
    if mode == "custom":
        return live_scrape_custom(url, limit, keyword), False

    fn = {"quotes": live_scrape_quotes,
          "books":  live_scrape_books,
          "news":   live_scrape_news}[mode]
    items = fn(limit, keyword)
    if items:
        return items, False

    # Demo fallback
    pool = {"quotes": DEMO_QUOTES, "books": DEMO_BOOKS, "news": DEMO_NEWS}[mode]
    shuffled = pool[:]
    random.shuffle(shuffled)
    return apply_filters(shuffled, keyword, limit), True


# ─── DISPLAY ─────────────────────────────────────────────────────────────────

def display_quotes(items):
    section_header("Famous Quotes", "💬")
    for i, q in enumerate(items, 1):
        print(f"\n  {cyan(bold(str(i)))}. {C.WHITE}\"{q['quote']}\"{C.RESET}")
        print(f"     {magenta('— ' + q['author'])}")
        if q.get("tags"):
            print(f"     {dim('Tags: ' + q['tags'])}")
    divider()

def display_books(items):
    section_header("Books & Prices", "📚")
    print(f"  {dim('#'):<5} {'Title':<42} {'Price':<10} {'Rating':<14} Avail")
    divider()
    for i, b in enumerate(items, 1):
        title = b["title"][:40] + ".." if len(b["title"]) > 40 else b["title"]
        print(f"  {cyan(str(i)):<4} {title:<42} {green(b['price']):<10} {b['rating']:<14} {dim(b['avail'])}")
    divider()

def display_news(items):
    section_header("Tech News — Top Stories", "📰")
    for i, n in enumerate(items, 1):
        print(f"\n  {cyan(bold(str(i)))}. {bold(n['title'])}")
        print(f"     {dim('📡 ' + n['source'] + '  •  ' + n['score'])}")
        if n["url"].startswith("http"):
            print(f"     {blue(n['url'][:80])}")
    divider()

def display_custom(items):
    section_header("Custom Page Extraction", "🔍")
    for i, it in enumerate(items, 1):
        label = cyan(f"[{it['type']}]") if it["type"] in ("H1","H2","H3") else dim(f"[{it['type']}]")
        text  = it["text"][:110] + "…" if len(it["text"]) > 110 else it["text"]
        print(f"\n  {cyan(str(i))}. {label}  {text}")
    divider()

DISPLAY_FN = {"quotes": display_quotes, "books": display_books,
              "news": display_news, "custom": display_custom}


# ─── SAVE ────────────────────────────────────────────────────────────────────

def save_results(items, label):
    if not items:
        return
    stamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_lbl = label.lower().replace(" ", "_").replace("&", "and")
    fmt = input(f"\n  Save as  [1] TXT  [2] CSV  [3] Both  [Enter to skip]: ").strip()
    if fmt not in ("1", "2", "3"):
        info("Save skipped.")
        return

    if fmt in ("1", "3"):
        fname = f"scraped_{safe_lbl}_{stamp}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"Category  : {label}\nTimestamp : {ts()}\n{'='*60}\n\n")
            for i, item in enumerate(items, 1):
                f.write(f"{i}. " + " | ".join(str(v) for v in item.values()) + "\n")
        success(f"Saved → {bold(fname)}")

    if fmt in ("2", "3"):
        fname = f"scraped_{safe_lbl}_{stamp}.csv"
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)
        success(f"Saved → {bold(fname)}")


# ─── INPUT HELPERS ────────────────────────────────────────────────────────────

def ask_limit():
    while True:
        raw = input(f"  How many results? {dim('[1-100, default 10]')}: ").strip()
        if raw == "":
            return 10
        if raw.isdigit() and 1 <= int(raw) <= 100:
            return int(raw)
        warn("Enter a number between 1 and 100.")

def ask_keyword():
    return input(f"  Keyword filter? {dim('[Enter to skip]')}: ").strip()


# ─── MENU & MAIN LOOP ─────────────────────────────────────────────────────────

MENU = {
    "1": ("Quotes",         "quotes.toscrape.com",  "quotes"),
    "2": ("Books & Prices", "books.toscrape.com",   "books"),
    "3": ("Tech News",      "news.ycombinator.com", "news"),
    "4": ("Custom URL",     "any URL you provide",  "custom"),
}

def show_menu():
    banner()
    print(f"  {bold('Choose what to scrape:')}\n")
    for key, (label, src, _) in MENU.items():
        print(f"    {cyan(bold(key))}.  {bold(label):<24} {dim('← ' + src)}")
    print(f"\n    {yellow(bold('Q'))}.  Quit\n")
    divider()

def run():
    while True:
        show_menu()
        choice = input(f"  {bold('Your choice')}: ").strip().lower()

        if choice == "q":
            banner()
            print(f"  {green('Thanks for using the Web Scraper! Goodbye 👋')}\n")
            sys.exit(0)

        if choice not in MENU:
            warn("Invalid choice. Enter 1, 2, 3, 4, or Q.")
            input(dim("  Press Enter to continue…"))
            continue

        label, source, mode = MENU[choice]
        custom_url = ""

        if mode == "custom":
            custom_url = input(f"\n  Enter URL {dim('(include http:// or https://)')}: ").strip()
            if not custom_url:
                warn("No URL entered.")
                input(dim("  Press Enter to continue…"))
                continue

        print()
        limit   = ask_limit()
        keyword = ask_keyword()

        print()
        info(f"Scraping: {source}  •  limit={limit}" +
             (f"  •  filter='{keyword}'" if keyword else ""))
        info(f"Timestamp: {ts()}")
        print()

        items, is_demo = smart_scrape(mode, limit, keyword, url=custom_url)

        if not items:
            warn("No results found — try removing the keyword filter or raising the limit.")
        else:
            DISPLAY_FN[mode](items)
            live_badge = f" {green('[LIVE]')}" if not is_demo else f" {yellow('[DEMO]')}"
            success(f"{len(items)} item(s) retrieved.{live_badge}")
            if is_demo:
                info("Live scraping unavailable on this network — showing built-in sample data.")
                info("On a real internet connection, actual site data is scraped.")
            save_results(items, label)

        print()
        cont = input(f"  {bold('Scrape again?')} {dim('[Y / N]')}: ").strip().lower()
        if cont != "y":
            banner()
            print(f"  {green('Thanks for using the Web Scraper! Goodbye 👋')}\n")
            sys.exit(0)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(f"\n\n  {yellow('Interrupted — Goodbye!')}\n")
        sys.exit(0)