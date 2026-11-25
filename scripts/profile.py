#!/usr/bin/env python3
"""Generate the profile README and its SVG assets.

Usage: python3 scripts/profile.py [output dir, default: repository root]
"""
import os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
import gen
from gen import (THEMES, PROJECTS, FONT, MONO, svg, card, text, pill, icon, icon_tile, lang_dot,
                 pixels_svg, pixel_text, grid_from_art, ISLAND, write, LANG)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# ---------------------------------------------------------------- extra pixel icons
STAR = grid_from_art([
    "................",
    ".......kk.......",
    "......kyyk......",
    "......kyyk......",
    ".....kyyyyk.....",
    "kkkkkkyyyyykkkkk",
    "kyyyyyyyyyyyyyyk",
    ".kyyyyyyyyyyyyk.",
    "..kyyyyyyyyyyk..",
    "...kyyyyyyyyk...",
    "...kyyyyyyyyk...",
    "..kyyyyookyyyk..",
    "..kyyyokk.kyyk..",
    ".kyyokk....kyyk.",
    ".kokk.......kok.",
    ".kk..........kk.",
], {"k": "#713f12", "y": "#facc15", "o": "#ca8a04"})
CHEST = grid_from_art([
    "................",
    "................",
    "..kkkkkkkkkkkk..",
    ".kwwwwwwwwwwwwk.",
    ".kwddddddddddwk.",
    ".kwddddddddddwk.",
    ".kkkkkkggkkkkkk.",
    ".kwwwwwgGwwwwwk.",
    ".kwdddddgddddwk.",
    ".kwddddddddddwk.",
    ".kwddddddddddwk.",
    ".kwddddddddddwk.",
    ".kwwwwwwwwwwwwk.",
    ".kkkkkkkkkkkkkk.",
    "................",
    "................",
], {"k": "#3b2410", "w": "#b45309", "d": "#92400e", "g": "#d4d4d8", "G": "#71717a"})
SUN = grid_from_art([
    "....kkkk....",
    "..kkyyyykk..",
    ".kyyyyyyyyk.",
    ".kyyyyyyyyk.",
    "kyyyyyyyyyyk",
    "kyyyyyyyyyyk",
    "kyyyyyyyyyyk",
    "kyyyyyyyyyyk",
    ".kyyyyyyyyk.",
    ".kyyyyyyyyk.",
    "..kkyyyykk..",
    "....kkkk....",
], {"k": "#f97316", "y": "#fbbf24"})
gen.ICONS["star"] = STAR
gen.ICONS["chest"] = CHEST

# ---------------------------------------------------------------- header banner (C base)
SKIES = {
    "day": dict(light=["#bfdbfe", "#c7e0fe", "#d0e5fe", "#d9eafe", "#e2effe", "#ebf4ff"],
                dark=["#0b1020", "#0f1630", "#131d3d", "#18254b", "#1e2d58", "#253666"]),
    "dusk": dict(light=["#fde68a", "#fcd9a0", "#fbc9a8", "#f5b8b4", "#e9aac4", "#d8a2d6"],
                 dark=["#1e1036", "#2a1446", "#3b1a54", "#55205e", "#7a2a60", "#a3395c"]),
}

def banner(t, sky="day", H=240, compact=False, prompt=None, sun=False):
    W = 840
    dark = t is THEMES["dark"]
    tag = "d" if dark else "l"
    b = [f'<clipPath id="r{tag}"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#r{tag})">']
    bands = SKIES[sky]["dark" if dark else "light"]
    bh = H / len(bands)
    for i, c in enumerate(bands):
        b.append(f'<rect x="0" y="{i * bh:g}" width="{W}" height="{bh + 1:g}" fill="{c}"/>')
    random.seed(7)
    name_x = 220 if compact else 48
    text_box = (name_x - 10, 30, name_x + 550, H - 30)
    if dark:
        for _ in range(110):
            x, y = random.randrange(0, W // 4) * 4, random.randrange(0, (H - 30) // 4) * 4
            if text_box[0] < x < text_box[2] and text_box[1] < y < text_box[3]:
                continue
            if not compact and 596 <= x <= 812 and 16 <= y <= 220:
                continue
            if compact and x < 200 and 20 < y < H - 20:
                continue
            s = random.choice([4, 4, 4, 8])
            b.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#e0e7ff" opacity="{random.choice([.4, .6, .9])}"/>')
    else:
        clouds = [(530, 22, 3), (790, 212, 3), (548, 204, 3)] if not compact else [(700, 22, 4), (600, 120, 3)]
        for cx, cy, n in clouds:
            for k in range(n):
                b.append(f'<rect x="{cx + k * 12}" y="{cy}" width="12" height="12" fill="#ffffff" opacity=".85"/>')
            b.append(f'<rect x="{cx + 12}" y="{cy - 12}" width="{(n - 2) * 12}" height="12" fill="#ffffff" opacity=".85"/>')
    if sun:
        b.append(pixels_svg(SUN, 560 if not dark else 560, 30, 6) if not dark else
                 pixels_svg({k: ("#fef3c7", .9) for k in SUN}, 560, 30, 6))
    if compact:
        b.append(pixels_svg(ISLAND, 24, (H - 128) / 2, 7))
    else:
        # profile picture in a pixel frame
        ax, ay, sc = 624, 36, 10
        fr = "#1e3a8a" if not dark else "#a5b4fc"
        b.append(f'<rect x="{ax - 8}" y="{ay - 8}" width="{160 + 16}" height="{160 + 16}" fill="{fr}" opacity=".9"/>')
        b.append(f'<rect x="{ax - 4}" y="{ay - 4}" width="{160 + 8}" height="{160 + 8}" fill="{bands[2]}"/>')
        b.append(pixels_svg(gen.ICONS["me"], ax, ay, sc))
    if sky == "dusk":
        fg, sh, sub, body = (("#fff7ed", "#3b0764", "#f9a8d4", "#fbcfe8") if dark else
                             ("#431407", "#fdba74", "#9a3412", "#7c2d12"))
    else:
        fg, sh, sub, body = (("#f8fafc", "#020617", "#a5b4fc", "#cbd5e1") if dark else
                             ("#0f172a", "#93c5fd", "#1e3a8a", "#334155"))
    if compact:
        b.append(pixel_text("PRESENTKIM", name_x, 40, 6, fg, sh))
        b.append(pixel_text("BEDROCK RESEARCH / TOOLS", name_x + 2, 98, 3, sub))
        b.append(text(name_x + 2, 140, "Carpenter by day. Building tools for Bedrock creators by night.", 14, body, 500))
    else:
        b.append(pixel_text("PRESENTKIM", 48, 64, 7, fg, sh))
        b.append(pixel_text(SUBTITLE, 50, 132, 3, sub))
        if prompt:
            b.append(text(50, 188, "$", 14, sub, 700, family=MONO))
            b.append(text(66, 188, prompt[0], 14, fg, 500, family=MONO))
            b.append(text(50, 210, prompt[1], 13, body, 400, family=MONO))
        else:
            b.append(f'<text x="50" y="192" font-family="{FONT}" font-size="15" fill="{body}">'
                     f'<tspan font-weight="700" fill="{fg}">Main job</tspan> interior carpenter.  '
                     f'<tspan font-weight="700" fill="{fg}">Hobby</tspan> programming.</text>')
    b.append("</g>")
    b.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{t["border"]}"/>')
    return svg(W, H, "\n".join(b), "PresentKim")

SUBTITLE = 'JUST KNOW THIS. "YOU ARE GOOD"'

# ---------------------------------------------------------------- pixel-cornered card shape
def pcard(w, h, t, step=4, fill=None, stroke=True):
    s = step
    pts = [(2 * s, 0), (w - 2 * s, 0), (w - 2 * s, s), (w - s, s), (w - s, 2 * s), (w, 2 * s),
           (w, h - 2 * s), (w - s, h - 2 * s), (w - s, h - s), (w - 2 * s, h - s), (w - 2 * s, h),
           (2 * s, h), (2 * s, h - s), (s, h - s), (s, h - 2 * s), (0, h - 2 * s), (0, 2 * s),
           (s, 2 * s), (s, s), (2 * s, s)]
    # inset by .5 for crisp stroke
    pts = [(min(max(x, .5), w - .5), min(max(y, .5), h - .5)) for x, y in pts]
    d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts) + "Z"
    st = f' stroke="{t["border"]}" stroke-width="1"' if stroke else ""
    return f'<path d="{d}" fill="{fill or t["card"]}"{st} shape-rendering="crispEdges"/>'

# ---------------------------------------------------------------- project card (A base)
ACCENT = {"skygear": "#f59e0b", "research": "#0ea5e9", "pmmp": "#84cc16", "gitres": "#64748b"}

def project(p, t, variant="a"):
    W, H = 414, 156
    b = []
    if variant == "pixel":
        b.append(pcard(W, H, t))
    else:
        b.append(card(W, H, t))
    if variant == "accent":
        b.append(f'<clipPath id="c{p["key"]}"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="11"/></clipPath>')
        b.append(f'<rect x="1" y="1" width="{W - 2}" height="4" fill="{ACCENT[p["key"]]}" clip-path="url(#c{p["key"]})"/>')
    if variant == "pixel":
        b.append(f'<rect x="24.5" y="24.5" width="47" height="47" fill="{t["subtle"]}" stroke="{t["border"]}" shape-rendering="crispEdges"/>')
        b.append(icon(p["icon"], 32, 32, 2))
    else:
        b.append(icon_tile(24, 24, 48, p["icon"], t, 2))
    title_font = MONO if variant == "terminal" else FONT
    b.append(text(86, 44, p["name"], 16 if variant == "terminal" else 17, t["fg"], 600, family=title_font))
    b.append(text(86, 64, p["tag"], 12, t["muted"], family=MONO if variant in ("terminal", "pixel") else FONT))
    b.append(text(W - 26, 44, "↗", 16, t["muted"], anchor="end"))
    for i, line in enumerate(p["desc"]):
        b.append(text(24, 100 + i * 19, line, 13, t["muted"]))
    b.append(lang_dot(24, 141, p["lang"], t))
    return svg(W, H, "\n".join(b), p["name"], 376)

# ---------------------------------------------------------------- values footer (B base)
VALUES = [("01", "Keep it light", "Small, fun projects I actually use.", "star"),
          ("02", "Share what I learn", "Open source gave me a lot.", "chest"),
          ("03", "Build the toolbox", "Research tech so others can create.", "hammer")]

def values(t, variant="b"):
    W, H = 840, 150 if variant != "strip" else 96
    b = [pcard(W, H, t) if variant == "pixel" else card(W, H, t, 16)]
    cw = (W - 48) / 3
    for i, (n, h, d, ic) in enumerate(VALUES):
        x = 24 + i * cw
        if i:
            b.append(f'<line x1="{x}" y1="24" x2="{x}" y2="{H - 24}" stroke="{t["border"]}"/>')
        xx = x + (20 if i else 8)
        if variant == "strip":
            b.append(icon(ic, xx, 32, 2))
            b.append(text(xx + 44, 46, h, 15, t["fg"], 600))
            b.append(text(xx + 44, 66, d, 12, t["muted"]))
        elif variant in ("pixel", "icons"):
            b.append(icon(ic, xx, 30, 2))
            b.append(text(xx + cw - 60, 46, n, 12, t["muted"], 600, family=MONO, anchor="end"))
            b.append(text(xx, 90, h, 17, t["fg"], 600))
            b.append(text(xx, 114, d, 13, t["muted"]))
        else:
            b.append(text(xx, 52, n, 12, t["muted"], 600, family=MONO))
            b.append(text(xx, 84, h, 17, t["fg"], 600))
            b.append(text(xx, 108, d, 13, t["muted"]))
    return svg(W, H, "\n".join(b), "Keep it light · Share what I learn · Build the toolbox")

# ---------------------------------------------------------------- README
P = {p["key"]: p for p in PROJECTS}

def img(path, alt, url=None):
    i = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{path}-dark.svg">'
         f'<img src="./assets/{path}-light.svg" alt="{alt}"></picture>')
    return f'<a href="{url}">{i}</a>' if url else i

def readme(intro=None):
    r = ['<p align="center">', img("header", "PresentKim"), "</p>", ""]
    if intro:
        r += [intro, ""]
    r += ['<p align="center">',
          img("skygear", "SkyGear", P["skygear"]["url"]), img("research", "bedrock-research", P["research"]["url"]),
          "<br>",
          img("pmmp", "presentkim-pm", P["pmmp"]["url"]), img("gitres", "git-resource", P["gitres"]["url"]),
          "</p>", "",
          '<p align="center">', img("values", "Keep it light · Share what I learn · Build the toolbox"), "</p>", ""]
    return "\n".join(r)

VARIANTS = {
    # H: D design + F project cards (accent bar), profile picture, new copy
    "h": dict(header=lambda t: banner(t), card="accent", values="b", intro=None),
}
OLD_VARIANTS = {
    # D: straight combination
    "d": dict(header=lambda t: banner(t), card="a", values="b", intro=None),
    # E: pixel-everything (stepped corners, pixel icons in footer), dusk sky with sun
    "e": dict(header=lambda t: banner(t, sky="dusk", sun=True), card="pixel", values="pixel", intro=None),
    # F: compact banner + project accent bars + slim footer strip
    "f": dict(header=lambda t: banner(t, H=180, compact=True), card="accent", values="strip", intro=None),
    # G: terminal flavored banner + mono card titles + icon footer, Korean intro quote
    "g": dict(header=lambda t: banner(t, prompt=("whoami", "> interior carpenter · bedrock tinkerer · open source")),
              card="terminal", values="icons",
              intro="> 직접 콘텐츠를 찍어내기보다, 새로운 기술을 연구해서 **다른 개발자들이 콘텐츠를 만들 수 있는 환경**을 만듭니다."),
}

def build(out):
    for k, v in VARIANTS.items():
        d = f"{out}/{k}"
        for tn, t in THEMES.items():
            write(f"{d}/assets/header-{tn}.svg", v["header"](t))
            for p in PROJECTS:
                write(f"{d}/assets/{p['key']}-{tn}.svg", project(p, t, v["card"]))
            write(f"{d}/assets/values-{tn}.svg", values(t, v["values"]))
        write(f"{d}/README.md", readme(v["intro"]))

def build_profile(out, key="h"):
    v = VARIANTS[key]
    for tn, t in THEMES.items():
        write(f"{out}/assets/header-{tn}.svg", v["header"](t))
        for p in PROJECTS:
            write(f"{out}/assets/{p['key']}-{tn}.svg", project(p, t, v["card"]))
        write(f"{out}/assets/values-{tn}.svg", values(t, v["values"]))
    write(f"{out}/README.md", readme(v["intro"]))

if __name__ == "__main__":
    build_profile(OUT)
    print("ok")
