#!/usr/bin/env python3
"""Generate profile README drafts (A: minimal, B: bento, C: pixel)."""
import os, re, sys
from PIL import Image

REF = os.path.join(os.path.dirname(__file__), "ref")
OUT = sys.argv[1] if len(sys.argv) > 1 else "drafts"

FONT = ("ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', "
        "'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', Helvetica, Arial, sans-serif")
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'D2Coding', monospace"

THEMES = {
    "light": dict(bg="#ffffff", card="#ffffff", border="#e4e4e7", fg="#09090b", muted="#71717a",
                  subtle="#f4f4f5", ring="#d4d4d8", accent="#18181b", accentfg="#fafafa"),
    "dark": dict(bg="#09090b", card="#09090b", border="#27272a", fg="#fafafa", muted="#a1a1aa",
                 subtle="#18181b", ring="#3f3f46", accent="#fafafa", accentfg="#09090b"),
}

# ---------------------------------------------------------------- pixel icons
def grid_from_png(path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            if a > 0:
                px[(x, y)] = ("#%02x%02x%02x" % (r, g, b), a / 255)
    return px

def grid_from_art(art, pal):
    px = {}
    for y, row in enumerate(art):
        for x, c in enumerate(row):
            if c in pal:
                px[(x, y)] = (pal[c], 1)
    return px

def pixels_svg(px, x0, y0, s):
    """Rects merged along rows."""
    out = []
    rows = {}
    for (x, y), v in px.items():
        rows.setdefault(y, []).append((x, v))
    for y, items in rows.items():
        items.sort()
        i = 0
        while i < len(items):
            x, v = items[i]
            j = i
            while j + 1 < len(items) and items[j + 1][0] == items[j][0] + 1 and items[j + 1][1] == v:
                j += 1
            col, a = v
            op = "" if a >= 0.999 else f' fill-opacity="{a:.2f}"'
            out.append(f'<rect x="{x0 + x * s:g}" y="{y0 + y * s:g}" width="{(j - i + 1) * s:g}" height="{s:g}" fill="{col}"{op}/>')
            i = j + 1
    return "\n".join(out)

def gitres_svg(x0, y0, s):
    raw = open(os.path.join(REF, "gr.svg")).read()
    inner = re.sub(r"^<svg[^>]*>|</svg>$", "", raw.strip())
    return f'<g transform="translate({x0},{y0}) scale({s})">{inner}</g>'

ICONS = {}
ICONS["skygear"] = grid_from_png(os.path.join(REF, "sg.png"))

# PMMP plugin: plug
ICONS["pmmp"] = grid_from_art([
    "................",
    "....kk....kk....",
    "....sk....sk....",
    "....sk....sk....",
    "..kkkkkkkkkkkk..",
    "..khhhhhhhhhmk..",
    "..khllllllllmk..",
    "..khllllllllmk..",
    "..khllllllllmk..",
    "...kmlllllllk...",
    "....kmmmmmmk....",
    ".....kkllkk.....",
    ".......lk.......",
    ".......lk.......",
    ".......lk.......",
    ".......kk.......",
], {"k": "#2e1065", "l": "#8b5cf6", "m": "#6d28d9", "h": "#c4b5fd", "s": "#d4d4d8"})

# bedrock-research: book with bookmark
ICONS["research"] = grid_from_art([
    "................",
    "...kkkkkkkkkk...",
    "..kccccccccrck..",
    "..kchhhhhhcrck..",
    "..kchccccccrck..",
    "..kcccccccccck..",
    "..kcccgggggcck..",
    "..kcccgddgdcck..",
    "..kcccddddcdck..",
    "..kcccdddddcck..",
    "..kccccccccccck.",
    "..kdddddddddddk.",
    "..kpppppppppppk.",
    "..kdddddddddddk.",
    "...kkkkkkkkkkk..",
    "................",
], {"k": "#0c2a1a", "c": "#16a34a", "h": "#86efac", "r": "#ef4444", "g": "#4ade80",
    "d": "#15803d", "p": "#f4f4f5"})

# personal mark: hammer
ICONS["hammer"] = grid_from_art([
    "................",
    "..kkkkkkkkk.....",
    ".khhhhhhhhhk....",
    ".kmmmmmmmmmkkk..",
    ".kmmmmmmmmmmmmk.",
    ".kdddddddddkkk..",
    "..kkkkwwkkk.....",
    "......wwk.......",
    "......wwk.......",
    "......wwk.......",
    "......lwk.......",
    "......wwk.......",
    "......wwk.......",
    "......lwk.......",
    "......kkk.......",
    "................",
], {"k": "#18181b", "h": "#e4e4e7", "m": "#a1a1aa", "d": "#71717a", "w": "#b45309", "l": "#d97706"})

# floating sky island (24x16)
ISLAND = grid_from_art([
    "...........tt...........",
    "..........tTTt..........",
    ".........tTTTTt.........",
    "........tTTTTTTt........",
    ".........tTTTTt.........",
    "...........bb...........",
    "...........bb...........",
    "..gGgGgGgGgbbGgGgGgGg...",
    "..GGGGGGGGGGGGGGGGGGGG..",
    "..ddddddDdddddddDddddd..",
    "...dDdddddddDdddddddd...",
    "....ddddsdddddddsddd....",
    ".....dddddsdddddddd.....",
    "........ddddsddd........",
    "..........dddd..........",
    "...........dd...........",
], {"t": "#166534", "T": "#22c55e", "b": "#92400e", "g": "#4ade80", "G": "#16a34a",
    "d": "#78350f", "D": "#92400e", "s": "#71717a"})

def icon(name, x, y, s):
    if name == "gitres":
        return gitres_svg(x, y, s)
    return pixels_svg(ICONS[name], x, y, s)

# ---------------------------------------------------------------- 5x7 pixel font
GLYPHS = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00001", "00001", "00001", "10001", "10001", "01110"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    " ": ["00000"] * 7,
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00000", "00100"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "X2": [],
}

def pixel_text(text, x0, y0, s, fill, shadow=None):
    out = []
    cx = x0
    for ch in text.upper():
        g = GLYPHS.get(ch, GLYPHS[" "])
        for gy, row in enumerate(g):
            for gx, b in enumerate(row):
                if b == "1":
                    if shadow:
                        out.append(f'<rect x="{cx + gx * s + s}" y="{y0 + gy * s + s}" width="{s}" height="{s}" fill="{shadow}"/>')
        for gy, row in enumerate(g):
            for gx, b in enumerate(row):
                if b == "1":
                    out.append(f'<rect x="{cx + gx * s}" y="{y0 + gy * s}" width="{s}" height="{s}" fill="{fill}"/>')
        cx += 6 * s
    return "\n".join(out)

def pixel_width(text, s):
    return len(text) * 6 * s - s

# ---------------------------------------------------------------- helpers
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

DISP = {}
def svg(w, h, body, title, disp=None):
    dw = disp or w
    dh = round(h * dw / w)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{dw}" height="{dh}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}" shape-rendering="auto">\n<title>{esc(title)}</title>\n{body}\n</svg>\n')

def card(w, h, t, r=12, fill=None):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{r}" '
            f'fill="{fill or t["card"]}" stroke="{t["border"]}"/>')

def text(x, y, s, size, fill, weight=400, family=FONT, anchor="start", ls=None):
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{l}>{esc(s)}</text>')

def pill(x, y, label, t, filled=False, size=12):
    w = int(len(label) * size * 0.58) + 20
    bg = t["accent"] if filled else t["subtle"]
    fg = t["accentfg"] if filled else t["fg"]
    stroke = "none" if filled else t["border"]
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w}" height="23" rx="11.5" fill="{bg}" stroke="{stroke}"/>'
            + text(x + w / 2 + .5, y + 16, label, size, fg, 500, anchor="middle")), w

def icon_tile(x, y, size, name, t, scale):
    pad = (size - 16 * scale) / 2
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{size - 1}" height="{size - 1}" rx="10" '
            f'fill="{t["subtle"]}" stroke="{t["border"]}"/>' + icon(name, x + pad, y + pad, scale))

LANG = {"Go": "#00ADD8", "PHP": "#4F5D95", "TypeScript": "#3178c6", "MDX": "#fcb32c"}

PROJECTS = [
    dict(key="skygear", icon="skygear", name="SkyGear", url="https://github.com/PresentKim/SkyGear",
         lang="Go", tag="Factory server",
         desc=["Sky-island factory server for Bedrock on Dragonfly —",
               "machines, research and fairy magic."]),
    dict(key="research", icon="research", name="bedrock-research", url="https://github.com/PresentKim/bedrock-research",
         lang="MDX", tag="Knowledge base",
         desc=["Sourced notes on JSON UI, Ore UI, Script API and",
               "the protocol — collected and shared in Korean."]),
    dict(key="pmmp", icon="pmmp", name="presentkim-pm", url="https://github.com/presentkim-pm",
         lang="PHP", tag="PocketMine-MP",
         desc=["Plugins and libraries for PocketMine-MP,",
               "built as tools for other server developers."]),
    dict(key="gitres", icon="gitres", name="git-resource", url="https://github.com/PresentKim/git-resource",
         lang="TypeScript", tag="Web app",
         desc=["Preview every image in a GitHub repository",
               "straight from its URL. gitresource.com"]),
]

def lang_dot(x, y, lang, t):
    return (f'<circle cx="{x + 5}" cy="{y - 4}" r="5" fill="{LANG[lang]}"/>'
            + text(x + 16, y, lang, 12, t["muted"]))

# ================================================================= Draft A
def a_header(t):
    W, H = 840, 216
    b = [card(W, H, t)]
    b.append(icon_tile(32, 32, 88, "hammer", t, 4))
    b.append(text(144, 68, "PresentKim", 30, t["fg"], 700, ls=-0.5))
    b.append(text(144, 96, "Interior carpenter by day, hobby developer by night.", 15, t["muted"]))
    x = 144
    for i, lab in enumerate(["Minecraft Bedrock", "PocketMine-MP", "Dragonfly", "Open source"]):
        p, w = pill(x, 112, lab, t, filled=(i == 0))
        b.append(p)
        x += w + 8
    b.append(f'<line x1="32" y1="160" x2="{W - 32}" y2="160" stroke="{t["border"]}"/>')
    b.append(f'<text x="32" y="189" font-family="{FONT}" font-size="14" font-weight="500" fill="{t["fg"]}">'
             f'I research how Bedrock works and turn it into tools, '
             f'<tspan fill="{t["muted"]}" font-weight="400">so other people can build the content.</tspan></text>')
    return svg(W, H, "\n".join(b), "PresentKim")

def a_project(p, t):
    W, H = 414, 156
    b = [card(W, H, t)]
    b.append(icon_tile(24, 24, 48, p["icon"], t, 2))
    b.append(text(86, 44, p["name"], 17, t["fg"], 600))
    b.append(text(86, 64, p["tag"], 12, t["muted"]))
    b.append(text(W - 26, 44, "↗", 16, t["muted"], anchor="end"))
    for i, line in enumerate(p["desc"]):
        b.append(text(24, 100 + i * 19, line, 13, t["muted"]))
    b.append(lang_dot(24, 141, p["lang"], t))
    return svg(W, H, "\n".join(b), p["name"], 376)

# ================================================================= Draft B
def b_hero(t):
    W, H = 840, 260
    b = [card(W, H, t, 16)]
    # right: island panel
    px, py, pw, ph = 520, 16, 304, 228
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{t["subtle"]}"/>')
    # subtle pixel grid
    grid = []
    for gx in range(px + 16, px + pw, 16):
        grid.append(f'<line x1="{gx}" y1="{py}" x2="{gx}" y2="{py + ph}"/>')
    for gy in range(py + 16, py + ph, 16):
        grid.append(f'<line x1="{px}" y1="{gy}" x2="{px + pw}" y2="{gy}"/>')
    b.append(f'<g stroke="{t["border"]}" stroke-width="1" opacity="0.6">{"".join(grid)}</g>')
    b.append(pixels_svg(ISLAND, px + (pw - 24 * 9) / 2, py + 30, 9))
    b.append(text(40, 58, "HELLO, I'M", 12, t["muted"], 600, family=MONO, ls=2))
    b.append(text(40, 100, "PresentKim", 40, t["fg"], 700, ls=-1))
    b.append(text(40, 136, "Hobby developer researching Minecraft: Bedrock", 15, t["muted"]))
    b.append(text(40, 158, "Edition — and building the tools that come out of it.", 15, t["muted"]))
    x = 40
    for i, lab in enumerate(["Carpenter", "Bedrock", "Go", "PHP", "TypeScript"]):
        p, w = pill(x, 196, lab, t, filled=(i == 0))
        b.append(p)
        x += w + 8
    return svg(W, H, "\n".join(b), "PresentKim")

def b_tile(p, t, wide):
    W, H = (548, 200) if wide else (284, 200)
    b = [card(W, H, t, 16)]
    b.append(icon(p["icon"], 24, 24, 3))
    b.append(text(W - 24, 40, "↗", 16, t["muted"], anchor="end"))
    b.append(text(24, 106, p["tag"].upper(), 11, t["muted"], 600, family=MONO, ls=1.5))
    b.append(text(24, 132, p["name"], 20, t["fg"], 700, ls=-0.3))
    if wide:
        b.append(text(24, 158, " ".join(p["desc"]).replace("gitresource.com", ""), 13, t["muted"]))
    else:
        b.append(text(24, 158, p["desc"][0][:40].rsplit(" ", 1)[0] + "…", 13, t["muted"]))
    b.append(lang_dot(24, 184, p["lang"], t))
    return svg(W, H, "\n".join(b), p["name"])

def b_values(t):
    W, H = 840, 150
    b = [card(W, H, t, 16)]
    cols = [("01", "Keep it light", "Small, fun projects I actually use."),
            ("02", "Share what I learn", "Open source gave me a lot."),
            ("03", "Build the toolbox", "Research tech so others can create.")]
    cw = (W - 48) / 3
    for i, (n, h, d) in enumerate(cols):
        x = 24 + i * cw
        if i:
            b.append(f'<line x1="{x}" y1="24" x2="{x}" y2="{H - 24}" stroke="{t["border"]}"/>')
        xx = x + (20 if i else 8)
        b.append(text(xx, 52, n, 12, t["muted"], 600, family=MONO))
        b.append(text(xx, 84, h, 17, t["fg"], 600))
        b.append(text(xx, 108, d, 13, t["muted"]))
    return svg(W, H, "\n".join(b), "Values")

# B tile descriptions shortened
B_SHORT = {
    "skygear": "Sky-island factory server on Dragonfly — machines, research, fairy magic.",
    "research": "Bedrock dev wiki,",
    "pmmp": "PocketMine-MP plugins",
    "gitres": "Preview every image in a GitHub repo straight from its URL.",
}
B_SHORT2 = {"research": "sourced & shared.", "pmmp": "and libraries."}

def b_tile2(p, t, wide):
    W, H = (548, 200) if wide else (284, 200)
    b = [card(W, H, t, 16)]
    b.append(icon(p["icon"], 24, 24, 3))
    b.append(text(24, 100, p["tag"].upper(), 11, t["muted"], 600, family=MONO, ls=1.5))
    b.append(text(24, 126, p["name"], 20, t["fg"], 700, ls=-0.3))
    b.append(text(24, 150, B_SHORT[p["key"]], 13, t["muted"]))
    if p["key"] in B_SHORT2:
        b.append(text(24, 168, B_SHORT2[p["key"]], 13, t["muted"]))
    b.append(lang_dot(W - 24 - 16 - len(p["lang"]) * 7, 40, p["lang"], t) if False else "")
    b.append(lang_dot(24, 186 if p["key"] not in B_SHORT2 else 190, p["lang"], t) if False else "")
    # language chip bottom-right
    lw = len(p["lang"]) * 7 + 30
    b.append(f'<g transform="translate({W - 24 - lw},{28})">'
             f'<rect x=".5" y=".5" width="{lw}" height="22" rx="11" fill="{t["subtle"]}" stroke="{t["border"]}"/>'
             f'<circle cx="13" cy="11.5" r="4" fill="{LANG[p["lang"]]}"/>'
             + text(23, 15.5, p["lang"], 11.5, t["fg"], 500) + '</g>')
    return svg(W, H, "\n".join(b), p["name"], 496 if wide else 257)

# ================================================================= Draft C
def c_banner(t):
    W, H = 840, 240
    dark = t is THEMES["dark"]
    b = []
    b.append(f'<clipPath id="r"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#r)">')
    # banded pixel sky
    bands = (["#0b1020", "#0f1630", "#131d3d", "#18254b", "#1e2d58", "#253666"] if dark else
             ["#bfdbfe", "#c7e0fe", "#d0e5fe", "#d9eafe", "#e2effe", "#ebf4ff"])
    bh = H / len(bands)
    for i, c in enumerate(bands):
        b.append(f'<rect x="0" y="{i * bh:g}" width="{W}" height="{bh + 1:g}" fill="{c}"/>')
    import random
    random.seed(7)
    for _ in range(90 if dark else 0):
        x, y = random.randrange(0, W // 4) * 4, random.randrange(0, (H - 40) // 4) * 4
        s = random.choice([4, 4, 4, 8])
        if x < 580 and 40 < y < 210:
            continue
        b.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#e0e7ff" opacity="{random.choice([.4, .6, .9])}"/>')
    if not dark:  # pixel clouds
        for cx, cy, n in [(60, 40, 5), (300, 24, 4), (600, 206, 3), (760, 30, 4)]:
            for k in range(n):
                b.append(f'<rect x="{cx + k * 12}" y="{cy}" width="12" height="12" fill="#ffffff" opacity=".9"/>')
            b.append(f'<rect x="{cx + 12}" y="{cy - 12}" width="{(n - 2) * 12}" height="12" fill="#ffffff" opacity=".9"/>')
    b.append(pixels_svg(ISLAND, 600, 36, 8))
    fg = "#f8fafc" if dark else "#0f172a"
    sh = "#020617" if dark else "#93c5fd"
    b.append(pixel_text("PRESENTKIM", 48, 64, 7, fg, sh))
    sub = "#a5b4fc" if dark else "#1e3a8a"
    b.append(pixel_text("BEDROCK RESEARCH / TOOLS", 50, 132, 3, sub))
    b.append(text(50, 190, "Carpenter by day. Building tools for Bedrock creators by night.", 14,
                  "#cbd5e1" if dark else "#334155", 500))
    b.append("</g>")
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{t["border"]}"/>')
    return svg(W, H, "\n".join(b), "PresentKim")

def c_slot(p, t):
    W, H = 204, 236
    b = [card(W, H, t, 12)]
    # slot
    sx, sy, ss = 38, 24, 128
    b.append(f'<rect x="{sx + .5}" y="{sy + .5}" width="{ss}" height="{ss}" rx="8" fill="{t["subtle"]}" stroke="{t["border"]}"/>')
    # inner bevel (minecraft-ish slot, but flat)
    b.append(f'<rect x="{sx + 8}" y="{sy + 8}" width="{ss - 15}" height="{ss - 15}" rx="4" fill="none" stroke="{t["ring"]}" stroke-dasharray="4 4"/>')
    b.append(icon(p["icon"], sx + (ss - 96) / 2 + .5, sy + (ss - 96) / 2 + .5, 6))
    b.append(text(W / 2, 182, p["name"], 15, t["fg"], 600, anchor="middle"))
    # lang
    lw = len(p["lang"]) * 7 + 20
    x0 = (W - lw) / 2
    b.append(f'<circle cx="{x0 + 5}" cy="{205}" r="4" fill="{LANG[p["lang"]]}"/>')
    b.append(text(x0 + 15, 209, p["lang"], 12, t["muted"]))
    return svg(W, H, "\n".join(b), p["name"], 186)

# ================================================================= README writers
def pic(path, alt, width=None, raw=False):
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{path}-dark.svg">'
            f'<img src="{path}-light.svg" alt="{alt}"{w}></picture>')

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def build(out):
    for tn, t in THEMES.items():
        write(f"{out}/a/assets/header-{tn}.svg", a_header(t))
        for p in PROJECTS:
            write(f"{out}/a/assets/{p['key']}-{tn}.svg", a_project(p, t))
        write(f"{out}/b/assets/hero-{tn}.svg", b_hero(t))
        write(f"{out}/b/assets/values-{tn}.svg", b_values(t))
        for p, wide in zip(PROJECTS, [True, False, False, True]):
            write(f"{out}/b/assets/{p['key']}-{tn}.svg", b_tile2(p, t, wide))
        write(f"{out}/c/assets/banner-{tn}.svg", c_banner(t))
        for p in PROJECTS:
            write(f"{out}/c/assets/{p['key']}-{tn}.svg", c_slot(p, t))

    P = {p["key"]: p for p in PROJECTS}

    def img(path, alt, url=None):
        """GFM only: theme-specific images via #gh-*-mode-only fragments."""
        parts = []
        for tn, frag in (("light", "gh-light-mode-only"), ("dark", "gh-dark-mode-only")):
            i = f"![{alt}](./assets/{path}-{tn}.svg#{frag})"
            parts.append(f"[{i}]({url})" if url else i)
        return "".join(parts)

    def card(k):
        return img(k, P[k]["name"], P[k]["url"])

    links = ("[SkyGear](https://github.com/PresentKim/SkyGear) · "
             "[bedrock-research](https://github.com/PresentKim/bedrock-research) · "
             "[presentkim-pm](https://github.com/presentkim-pm) · "
             "[git-resource](https://gitresource.com)")

    # ---- A
    a = [img("header", "PresentKim"), "",
         card("skygear") + " " + card("research"),
         card("pmmp") + " " + card("gitres"), "",
         "가볍고 즐겁게 만들고, 알게 된 것은 나눕니다.", ""]
    write(f"{out}/a/README.md", "\n".join(a))

    # ---- B
    bb = [img("hero", "PresentKim"), "",
          card("skygear") + " " + card("research"),
          card("pmmp") + " " + card("gitres"), "",
          img("values", "Keep it light · Share what I learn · Build the toolbox"), ""]
    write(f"{out}/b/README.md", "\n".join(bb))

    # ---- C
    cc = [img("banner", "PresentKim"), "",
          " ".join(card(k) for k in ["skygear", "research", "pmmp", "gitres"]), "",
          "> 직접 콘텐츠를 찍어내기보다, 배드락의 새로운 기술을 연구해서 **다른 개발자들이 콘텐츠를 만들 수 있는 환경**을 만드는 걸 좋아합니다.",
          "> 오픈 소스에서 받은 만큼, 알게 된 것은 나눕니다.",
          "",
          f"- [**SkyGear**]({P['skygear']['url']}) — Sky-island factory server for Bedrock (Go · Dragonfly)",
          f"- [**bedrock-research**]({P['research']['url']}) — Bedrock JSON UI · Ore UI · Script API · protocol wiki",
          f"- [**presentkim-pm**]({P['pmmp']['url']}) — PocketMine-MP plugins & libraries",
          f"- [**git-resource**]({P['gitres']['url']}) — Preview images of any GitHub repo · [gitresource.com](https://gitresource.com)",
          ""]
    write(f"{out}/c/README.md", "\n".join(cc))

if __name__ == "__main__":
    build(OUT)
    print("ok")
