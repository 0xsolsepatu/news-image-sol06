#!/usr/bin/env python3
"""The World in One Day — front page summing up Friday 27 November 2026.

Build tool only; NOT part of the graded entry (main.py copies entry.png).
Draws a 1024x1024 newspaper front page with Pillow: cream paper, serif
masthead, six-number figure strip, three illustrated lead panels, a ten-card
story grid (each card with a small drawn scene), a one-row UTC timeline strip,
a twenty-seven-item tail list in three columns, a world map with 8 pins, a
DATE CHECK box and a footer.

40 stories: 31 are pure 27 Nov (they happened, or were first reported, on
Fri 27 Nov 2026 in some time zone); the other 9 were first reported Thu 26
Nov and always carry a visible [26 NOV] tag — a solid dark pill with white
bold text, so the date discipline still reads at 300px. Pure stories carry a
pale outline "27 NOV" pill instead. The Eagles-Cowboys game kicked off
21:30 UTC Thu and ended ~00:35 UTC Fri; the chess match's first rest day
falls Fri 27 Nov (Guardian + FIDE schedule); the Cairo toll is given as
30+ because sources vary between 30 and 32. Every headline and deck below
is copied from RESEARCH.md. See GEMINI-REVIEW-NOTE.md for the design review.

Layout budget (1024px): header ends 122, figures 128-182, leads 188-372,
grid 378-594, timeline 600-630, tail 636-948, bottom 950-1006, footer
1010-1023. 13 drawn scenes: 3 lead illustrations + 10 grid mini-scenes.
Tail rows are 32px with 12pt headlines / 11pt decks so the tail stays
legible at 300px; grid decks are INK, not FADED, for contrast at
thumbnail size.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
OUT_PATH = "/home/hatch/workspace/makefun-newsimage-20261127/entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = "#F7F1E3"
CARD = "#FFFDF6"
INK = "#1A1A1A"
RED = "#B91C1C"
FADED = "#6B6455"
HAIRLINE = "#B8AE97"
NAVY = "#1E2A4A"
LAND = "#D8C9A3"
GOLD = "#C9A86A"
BLUE = "#2B4C8C"
GREEN = "#2E6B34"

problems = []

# ------------------------------------------------------------------ stories
# Each story: number, region, headline, deck, source, pure (True = 27 Nov).
# Caps: leads headline 47 / deck 78; grid 44 / 58; tail 37 / 55.
STORIES = [
    (1, "EUROPE", "EU budget talks end in deadlock",
     "\u20ac1.7tn budget and \u20ac45bn Ukraine loan stall; 24 back loan, revisit in Dec.",
     "REUTERS", True),
    (2, "ASIA", "Kim vows more nuclear warheads",
     "KCNA: nuclear arsenal \u2018absolutely inviolable\u2019; output expanding.",
     "REUTERS", True),
    (3, "SPORT", "Eagles stun Cowboys 39\u201338",
     "21 points down, Elliott\u2019s 59-yard field goal with 2 seconds left seals it.",
     "REUTERS", True),
    (4, "OCEANIA", "NZ coalition one seat short",
     "65 of 130 seats; Luxon needs Opportunity Party.",
     "REUTERS", True),
    (5, "EUROPE", "IAEA seeks Zaporizhzhia ceasefire",
     "28th loss of offsite power; diesel generators run.",
     "REUTERS", True),
    (6, "ECONOMY", "Black Friday doors swing open",
     "Target gift cards to $1,000; 1 in 3 shoppers use AI.",
     "THESTREET", True),
    (7, "EUROPE", "Zelenskyy warns of grid attack",
     "Russia plans major strike on power grid \u2018in days\u2019.",
     "AP", True),
    (8, "MIDEAST", "Israeli strikes kill 10 in Gaza",
     "Health officials report toll as ceasefire frays.",
     "AP", True),
    (9, "ENERGY", "Brent holds near month high",
     "$96.19 a barrel, +3.9% on the week; Hormuz hit.",
     "REUTERS", True),
    (10, "MARKETS", "Asia shares steady; dollar climbs",
     "Nikkei +0.7%; dollar set for 3rd monthly gain.",
     "REUTERS", True),
    (11, "ASIA", "Duterte\u2019s ICC trial starts Monday",
     "85 murder counts from 2011\u201318 drug war; families wait.",
     "REUTERS", True),
    (12, "ASIA", "Japan eyes $350bn defence plan",
     "\u00a556.3tn over five years, below military\u2019s wishes.",
     "REUTERS", True),
    (13, "EUROPE", "Tube strike: 8 days begin",
     "London drivers walk out; Circle, Piccadilly shut.",
     "REPORTS", True),
    (14, "EUROPE", "Biggest prisoner swap \u2018shortly\u2019",
     "US envoy: Russia\u2013Ukraine swap ahead of holidays.",
     "REPORTS", True),
    (15, "EUROPE", "No attack on Putin home, US says",
     "Kushner: alleged Ukraine strike \u2018did not happen\u2019.",
     "REPORTS", True),
    (16, "MIDEAST", "Houthis claim Jizan port strikes",
     "Yemen rebels say they hit Saudi ports; Riyadh silent.",
     "REPORTS", True),
    (17, "ASIA", "Indonesia eyes palm-oil fee",
     "Regulator proposes 0.5% levy on export sales.",
     "KUCOIN", True),
    (18, "ENERGY", "OPEC+ likely extends output cap",
     "Targets to hold into Q1 2027; meeting Sunday.",
     "REUTERS", True),
    (19, "ECONOMY", "Trafigura to shut zinc smelter",
     "Nyrstar plant in Netherlands closes on energy costs.",
     "KUCOIN", True),
    (20, "ASIA", "S. Korea court clears ex-president",
     "Ousted leader\u2019s perjury acquittal confirmed.",
     "REPORTS", True),
    (21, "CULTURE", "Depardieu to face rape trial",
     "French actor to stand trial, lawyer says.",
     "REPORTS", True),
    (22, "EUROPE", "Arrests at William & Kate\u2019s",
     "Two held over burglary at country estate.",
     "REPORTS", True),
    (23, "USA", "FAA halts Miami air traffic",
     "FedEx cargo jet leaves runway; traffic cancelled.",
     "REPORTS", True),
    (24, "EUROPE", "Record 2,000 reach Canaries",
     "Refugees land in Spain\u2019s islands in a single day.",
     "REPORTS", True),
    (25, "ASIA", "Myanmar rejects ICJ ruling parts",
     "Junta won\u2019t abide by \u2018inappropriate\u2019 aspects.",
     "REPORTS", True),
    (26, "EUROPE", "Germany pays Syrians to return",
     "Bigger cash bonuses in expanded return plan.",
     "REPORTS", True),
    (27, "EUROPE", "ECB picks Hern\u00e1ndez de Cos",
     "Spaniard to lead central bank; continuity seen.",
     "REUTERS", True),
    (28, "EUROPE", "Su-34 base hit in Volgograd",
     "Russian fighter-jet base struck, reports say.",
     "REPORTS", True),
    (29, "EUROPE", "Power station hit in Stavropol",
     "Assault strikes regional power station.",
     "REPORTS", True),
    (30, "EUROPE", "UK pledges \u00a39m wind farm",
     "Funding for wind power in war-hit country.",
     "REPORTS", True),
    (31, "SPORT", "Chess level at 1.5\u20131.5; rest day",
     "Game 3 drawn in 60 moves; Game 4 Saturday.",
     "GUARDIAN", True),
    (32, "ASIA", "China protests Japan on Diaoyu",
     "Vessels \u2018illegally intruded\u2019, Beijing says.",
     "XINHUA", False),
    (33, "AFRICA", "Cairo fuel-truck fire kills 30+",
     "Tanker overturns on ring road; 26 injured.",
     "AP", False),
    (34, "ASIA", "Mine flood kills 14 in Indonesia",
     "12 missing at illegal West Java gold mine.",
     "AP", False),
    (35, "MIDEAST", "Two Italians killed in Kuwait",
     "Drone attack on air-defence site; Iran blamed.",
     "REPORTS", False),
    (36, "EUROPE", "Serbia sets vote for 27 Dec",
     "Presidential election date signed off.",
     "REPORTS", False),
    (37, "AFRICA", "Congo Ebola tops 12,021 cases",
     "Deaths near 5,900 as Ituri fighting traps teams.",
     "PANA", False),
    (38, "AFRICA", "RSF drones kill 19 in Sudan",
     "Strikes hit civilians in Blue Nile state.",
     "REPORTS", False),
    (39, "EUROPE", "UK spends \u00a38bn on submarines",
     "Upgrade to speed nuclear boats back to sea.",
     "UK MOD", False),
    (40, "SPACE", "Progress 97 docks at ISS",
     "Russian cargo ship brings 3 tonnes of supplies.",
     "NASA", False),
]

BY_NUMBER = {s[0]: s for s in STORIES}
LEAD_NUMBERS = [1, 2, 3]
GRID_NUMBERS = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
TAIL_NUMBERS = list(range(14, 41))

LEAD_LABELS = {1: "TOP STORY", 2: "NUCLEAR", 3: "SPORT"}

FIGURES = [
    ("\u20ac1.7tn", "EU BUDGET DEADLOCK", "REUTERS \u00b7 27 NOV", True),
    ("39\u201338", "EAGLES COMEBACK", "REUTERS \u00b7 27 NOV", True),
    ("$96.19", "BRENT \u00b7 +3.9% WEEK", "REUTERS \u00b7 27 NOV", True),
    ("65/130", "NZ COALITION SEATS", "REUTERS \u00b7 27 NOV", True),
    ("~2,000", "CANARIES ARRIVALS", "27 NOV", True),
    ("30+", "CAIRO FIRE DEAD", "AP \u00b7 26 NOV", False),
]

# UTC timeline: single row, Fri 27 Nov — when the world learned it.
TIMELINE = [("00:35", "EAGLES 39\u201338"), ("00:50", "IAEA BID"),
            ("01:00", "KIM NUKES"), ("01:30", "JIZAN CLAIM"),
            ("02:00", "NZ COUNT"), ("02:30", "EU DEADLOCK"),
            ("02:45", "TUBE STRIKE"), ("03:00", "BRENT HIGH")]

# Map pins: (x, y, label) in the map's polygon coordinate space.
MAP_PINS = [(152, 20, "1"), (254, 20, "2"), (186, 32, "8"),
            (290, 44, "4"), (172, 38, "33")]
MAP_LEGEND_1 = "1 EU DEADLOCK \u00b7 2 KIM \u00b7 4 NZ COUNT \u00b7 8 GAZA \u00b7 33 CAIRO"
MAP_LEGEND_2 = ""

DATE_CHECK_LINES = [
    "Masthead date: Friday 27 November 2026. 31 stories happened, or were first",
    "reported, on 27 Nov; 9 stem from Thu 26 Nov and carry [26 NOV] pills.",
    "Rejected as not 27 Nov: Macy\u2019s parade (in the 26 Nov image), Riemann",
    "proof claim (one blog, unverified), \u2018300 Russians in Mali\u2019 (no source).",
]

FOOTER = "MAKE.FUN // 27 NOV 2026 // 40 STORIES \u00b7 12 REGIONS \u00b7 13 SCENES"

# ------------------------------------------------------------------ helpers
def load_typeface(path, size):
    return ImageFont.truetype(path, size)


def split_lines(draw, text, typeface, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=typeface) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(draw, cx, y, text, typeface, colour):
    w = draw.textlength(text, font=typeface)
    draw.text((cx - w / 2, y), text, font=typeface, fill=colour)


def dark_pill(draw, x, y, label, typeface, h=16):
    w = draw.textlength(label, font=typeface) + 12
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=INK)
    tw = draw.textlength(label, font=typeface)
    draw.text((x + (w - tw) / 2, y + (h - 12) / 2 - 1), label,
              font=typeface, fill=PAPER)
    return w


def outline_pill(draw, x, y, label, typeface, h=16):
    w = draw.textlength(label, font=typeface) + 12
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2,
                           outline=INK, width=1, fill=CARD)
    tw = draw.textlength(label, font=typeface)
    draw.text((x + (w - tw) / 2, y + (h - 12) / 2 - 1), label,
              font=typeface, fill=INK)
    return w


def date_pill(draw, x, y, pure, typeface):
    label = "27 NOV" if pure else "[26 NOV]"
    if pure:
        return outline_pill(draw, x, y, label, typeface)
    return dark_pill(draw, x, y, label, typeface)


# ------------------------------------------------------------------ sketches
def sketch_summit(draw, x, y, w, h):
    """EU summit: long table, three flags, seated delegates."""
    draw.rectangle([x, y + h - 12, x + w, y + h - 6], fill=NAVY)
    for i, cx in enumerate([x + w * 0.22, x + w * 0.5, x + w * 0.78]):
        draw.rectangle([cx - 3, y + 6, cx + 3, y + h - 12], fill=INK)
        flag = [BLUE, GOLD, RED][i]
        draw.rectangle([cx + 3, y + 6, cx + 26, y + 20], fill=flag,
                       outline=INK, width=1)
        draw.ellipse([cx - 8, y + h - 24, cx + 8, y + h - 12], fill=FADED)
    draw.text((x + w - 52, y + h - 26), "\u20ac1.7tn",
              font=load_typeface(SERIF_BOLD, 13), fill=RED)


def sketch_missile(draw, x, y, w, h):
    """Kim: missile rising diagonally, flame, smoke trail, stars."""
    # smoke trail
    draw.arc([x + 2, y + h - 26, x + w * 0.55, y + h + 6], 90, 200,
             fill=FADED, width=2)
    # body: diagonal from lower-left to upper-right
    draw.polygon([(x + w * 0.42, y + 26), (x + w * 0.52, y + 34),
                  (x + w * 0.62, y + 18), (x + w * 0.52, y + 10)],
                 fill=INK)
    # nose cone
    draw.polygon([(x + w * 0.52, y + 10), (x + w * 0.62, y + 18),
                  (x + w * 0.72, y + 4)], fill=RED)
    # fins
    draw.polygon([(x + w * 0.42, y + 26), (x + w * 0.52, y + 34),
                  (x + w * 0.36, y + 38)], fill=RED)
    # flame
    draw.polygon([(x + w * 0.40, y + 32), (x + w * 0.50, y + 40),
                  (x + w * 0.34, y + h - 2)], fill="#E07B00")
    for sx, sy in [(x + 10, y + 6), (x + w - 20, y + 30)]:
        draw.text((sx, sy), "\u2605", font=load_typeface(SANS_BOLD, 12),
                  fill=GOLD)


def sketch_football(draw, x, y, w, h):
    """Eagles comeback: stadium arc, goalposts, ball sailing through."""
    draw.arc([x + 4, y + 2, x + w - 4, y + h + 18], 180, 360, fill=NAVY,
             width=3)
    for gx in [x + w * 0.3, x + w * 0.7]:
        draw.line([gx, y + h - 22, gx, y + h - 2], fill=INK, width=2)
    draw.line([x + w * 0.3, y + h - 22, x + w * 0.7, y + h - 22], fill=INK,
              width=2)
    bx, by = x + w * 0.52, y + 10
    draw.ellipse([bx - 9, by - 6, bx + 9, by + 6], fill="#7A4A21",
                 outline=INK, width=1)
    draw.line([bx - 9, by, bx + 9, by], fill=PAPER, width=1)


def sketch_ballot(draw, x, y, w, h):
    draw.rectangle([x + 4, y + h - 14, x + w - 4, y + h - 2], fill=NAVY)
    draw.rectangle([x + 14, y + 2, x + w - 14, y + 8], fill=INK)
    draw.polygon([(x + w // 2 - 6, y + 8), (x + w // 2 + 6, y + 8),
                  (x + w // 2, y + 16)], fill=PAPER)


def sketch_atom(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    draw.ellipse([cx + r - 4, cy - r + 1, cx + r + 1, cy - r + 6],
                 fill=GOLD, outline=INK, width=1)


def sketch_tag(draw, x, y, w, h):
    draw.polygon([(x + 4, y + 4), (x + w - 14, y + 4), (x + w - 4, y + 14),
                  (x + w - 14, y + h - 4), (x + 4, y + h - 4)], fill=GOLD,
                 outline=INK, width=1)
    draw.ellipse([x + 10, y + 8, x + 16, y + 14], outline=INK, width=1)
    draw.text((x + 20, y + h - 18), "%", font=load_typeface(SANS_BOLD, 12),
              fill=RED)


def sketch_bolt(draw, x, y, w, h):
    cx = x + w // 2
    draw.polygon([(cx + 4, y + 2), (cx - 8, y + h // 2 + 2),
                  (cx - 1, y + h // 2 + 2), (cx - 5, y + h - 2),
                  (cx + 8, y + h // 2 - 2), (cx + 1, y + h // 2 - 2)],
                 fill=GOLD, outline=INK, width=1)


def sketch_dove(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([cx - 14, cy - 4, cx + 10, cy + 6], fill="#D9D9D9",
                 outline=INK, width=1)
    draw.polygon([(cx + 8, cy - 2), (cx + 22, cy - 8), (cx + 22, cy + 2)],
                 fill="#D9D9D9", outline=INK)
    draw.ellipse([cx - 16, cy - 12, cx + 2, cy - 2], fill="#D9D9D9",
                 outline=INK, width=1)
    draw.ellipse([cx - 20, cy - 14, cx - 14, cy - 8], fill=INK)
    draw.ellipse([cx + 4, cy + 6, cx + 8, cy + 10], fill=GREEN)


def sketch_barrel(draw, x, y, w, h):
    draw.rounded_rectangle([x + 8, y + 2, x + w - 8, y + h - 2], radius=4,
                           fill=INK)
    draw.line([x + 8, y + 9, x + w - 8, y + 9], fill=GOLD, width=2)
    draw.line([x + 8, y + h - 9, x + w - 8, y + h - 9], fill=GOLD, width=2)
    draw.text((x + w // 2 - 4, y + h // 2 - 7), "$",
              font=load_typeface(SANS_BOLD, 12), fill=GOLD)


def sketch_chart(draw, x, y, w, h):
    bars = [6, 12, 9, 16, 20]
    bw = w // 6
    for i, bh in enumerate(bars):
        bx = x + 4 + i * bw
        draw.rectangle([bx, y + h - 2 - bh, bx + bw - 3, y + h - 2],
                       fill=GREEN if i < 4 else RED)


def sketch_gavel(draw, x, y, w, h):
    draw.line([x + 6, y + h - 8, x + w - 6, y + 6], fill=INK, width=3)
    draw.rectangle([x + w - 16, y + 2, x + w - 4, y + 12], fill=NAVY)
    draw.rectangle([x + 4, y + h - 6, x + w - 4, y + h - 2], fill=INK)


def sketch_shield(draw, x, y, w, h):
    cx = x + w // 2
    draw.polygon([(cx - 12, y + 2), (cx + 12, y + 2), (cx + 12, y + 12),
                  (cx, y + h - 2), (cx - 12, y + 12)], fill=RED,
                 outline=INK, width=1)
    draw.text((cx - 4, y + 6), "\u00a5",
              font=load_typeface(SANS_BOLD, 11), fill=PAPER)


def sketch_train(draw, x, y, w, h):
    draw.rounded_rectangle([x + 4, y + 2, x + w - 4, y + h - 6], radius=4,
                           fill=RED)
    draw.rectangle([x + 10, y + 6, x + w // 2 - 2, y + 12], fill=PAPER)
    draw.rectangle([x + w // 2 + 2, y + 6, x + w - 10, y + 12], fill=PAPER)
    draw.line([x + 2, y + h - 2, x + w - 2, y + h - 2], fill=INK, width=2)


LEAD_ART = {1: sketch_summit, 2: sketch_missile, 3: sketch_football}
GRID_ART = {4: sketch_ballot, 5: sketch_atom, 6: sketch_tag, 7: sketch_bolt,
            8: sketch_dove, 9: sketch_barrel, 10: sketch_chart,
            11: sketch_gavel, 12: sketch_shield, 13: sketch_train}


# ------------------------------------------------------------------ paint
def audit(name, end, limit):
    if end > limit:
        problems.append(f"OVERFLOW {name}: ends {end}, limit {limit}")
        print(f"OVERFLOW {name}: ends {end}, limit {limit}")
    else:
        print(f"OK {name}: ends {end}/{limit}")


def paint_header(draw):
    centred(draw, CANVAS_W // 2, 4, "THE WORLD IN ONE DAY",
            load_typeface(SERIF_BOLD, 58), INK)
    centred(draw, CANVAS_W // 2, 70, "FRIDAY 27 NOVEMBER 2026",
            load_typeface(SERIF_BOLD, 30), RED)
    draw.rectangle([20, 116, CANVAS_W - 20, 118], fill=INK)
    draw.rectangle([20, 120, CANVAS_W - 20, 121], fill=INK)
    audit("header", 122, 122)


def paint_figures(draw):
    y0, h = 128, 54
    box_w, gap = 157, 8
    for i, (number, label, source, pure) in enumerate(FIGURES):
        x = 20 + i * (box_w + gap)
        draw.rectangle([x, y0, x + box_w, y0 + h], outline=INK, width=1)
        centred(draw, x + box_w // 2, y0 + 2, number,
                load_typeface(SERIF_BOLD, 24), RED if i % 2 == 0 else INK)
        centred(draw, x + box_w // 2, y0 + 28, label,
                load_typeface(SANS_BOLD, 9), FADED)
        if pure:
            pill_font = load_typeface(SANS_BOLD, 8)
            w = draw.textlength(source, font=pill_font) + 12
            dark_pill(draw, x + (box_w - w) // 2, y0 + 40, source,
                      pill_font, h=13)
        else:
            centred(draw, x + box_w // 2, y0 + 40, source,
                    load_typeface(SANS, 8), FADED)
    audit("figure strip", y0 + h, 182)


def paint_leads(draw):
    y0, h = 188, 184
    panel_w, gap = 320, 12
    for i, num in enumerate(LEAD_NUMBERS):
        story = BY_NUMBER[num]
        _, region, head, deck, source, pure = story
        x = 20 + i * (panel_w + gap)
        draw.rectangle([x, y0, x + panel_w, y0 + h], outline=INK, width=2,
                       fill=CARD)
        LEAD_ART[num](draw, x + 8, y0 + 6, panel_w - 16, 54)
        title_font = load_typeface(SERIF_BOLD, 22)
        tlines = split_lines(draw, head, title_font, panel_w - 24)
        if len(tlines) > 2:
            problems.append(f"LEAD TITLE TOO LONG: {head!r}")
            print(f"LEAD TITLE TOO LONG: {head!r}")
        ty = y0 + 66
        for line in tlines[:2]:
            draw.text((x + 12, ty), line, font=title_font, fill=INK)
            ty += 26
        deck_font = load_typeface(SERIF, 14)
        dlines = split_lines(draw, deck, deck_font, panel_w - 24)
        if len(dlines) > 2:
            problems.append(f"LEAD DECK TOO LONG: {deck!r}")
            print(f"LEAD DECK TOO LONG: {deck!r}")
        dy = ty + 2
        for line in dlines[:2]:
            draw.text((x + 12, dy), line, font=deck_font, fill=INK)
            dy += 17
        ly = y0 + h - 22
        chip_font = load_typeface(SANS_BOLD, 11)
        chip_w = dark_pill(draw, x + 12, ly, LEAD_LABELS[num], chip_font)
        src_font = load_typeface(SANS, 11)
        draw.text((x + 16 + chip_w, ly + 2), f"{region} \u00b7 {source}",
                  font=src_font, fill=FADED)
        pill_font = load_typeface(SANS_BOLD, 10)
        pw = (draw.textlength("27 NOV" if pure else "[26 NOV]",
                              font=pill_font) + 12)
        date_pill(draw, x + panel_w - 12 - pw, ly, pure, pill_font)
        audit(f"lead {num} {head[:24]}", dy, ly - 2)
    audit("lead panels", y0 + h, 372)


def paint_cards(draw):
    y0, card_h, gap = 378, 104, 8
    card_w, col_gap = 187, 12
    for i, num in enumerate(GRID_NUMBERS):
        story = BY_NUMBER[num]
        _, region, head, deck, source, pure = story
        col, row = i % 5, i // 5
        x = 20 + col * (card_w + col_gap)
        y = y0 + row * (card_h + gap)
        draw.rectangle([x, y, x + card_w, y + card_h], outline=HAIRLINE,
                       width=1, fill=CARD)
        draw.rectangle([x, y, x + 4, y + card_h], fill=RED)
        top_font = load_typeface(SANS_BOLD, 9)
        draw.text((x + 8, y + 3), f"{region} \u00b7 {source}",
                  font=top_font, fill=RED)
        pill_font = load_typeface(SANS_BOLD, 9)
        pw = draw.textlength("[26 NOV]" if not pure else "27 NOV",
                             font=pill_font) + 12
        date_pill(draw, x + card_w - 8 - pw, y + 3, pure, pill_font)
        GRID_ART[num](draw, x + 8, y + 19, card_w - 16, 28)
        title_font = load_typeface(SERIF_BOLD, 12)
        tlines = split_lines(draw, head, title_font, card_w - 16)
        if len(tlines) > 2:
            problems.append(f"GRID TITLE TOO LONG: {head!r}")
            print(f"GRID TITLE TOO LONG: {head!r}")
        ty = y + 50
        for line in tlines[:2]:
            draw.text((x + 8, ty), line, font=title_font, fill=INK)
            ty += 14
        deck_font = load_typeface(SERIF, 10)
        dlines = split_lines(draw, deck, deck_font, card_w - 16)
        if len(dlines) > 2:
            problems.append(f"GRID DECK TOO LONG: {deck!r}")
            print(f"GRID DECK TOO LONG: {deck!r}")
        dy = y + 80
        for line in dlines[:2]:
            draw.text((x + 8, dy), line, font=deck_font, fill=INK)
            dy += 11
        audit(f"grid {num} {head[:24]}", dy, y + card_h - 2)
    audit("story grid", y0 + 2 * card_h + gap, 594)


def paint_timeline(draw):
    y0, h = 600, 30
    draw.rectangle([20, y0, CANVAS_W - 20, y0 + h], outline=HAIRLINE,
                   width=1, fill=CARD)
    label_font = load_typeface(SANS_BOLD, 8)
    time_font = load_typeface(SANS_BOLD, 8)
    text_font = load_typeface(SANS, 8)
    ry = y0 + 9
    draw.text((28, ry), "FRI 27 NOV \u00b7 UTC", font=label_font, fill=RED)
    slot_w = (1004 - 140) / len(TIMELINE)
    for j, (time, label) in enumerate(TIMELINE):
        cx = 140 + slot_w * (j + 0.5)
        stamp = f"{time} {label}"
        sw = (draw.textlength(time, font=time_font) + 3 +
              draw.textlength(label, font=text_font))
        if sw > slot_w - 4:
            problems.append(f"TIMELINE TOO LONG: {stamp!r}")
            print(f"TIMELINE TOO LONG: {stamp!r}")
        tx = cx - sw / 2
        draw.text((tx, ry), time, font=time_font, fill=INK)
        draw.text((tx + draw.textlength(time, font=time_font) + 3, ry),
                  label, font=text_font, fill=FADED)
        draw.line([cx, ry + 11, cx, ry + 13], fill=RED, width=1)
    audit("timeline", y0 + h, 630)


def paint_tail(draw):
    y0 = 636
    draw.rectangle([20, y0, CANVAS_W - 20, y0 + 2], fill=INK)
    draw.text((20, y0 + 4), "MORE OF THE DAY \u2014 EVERY ITEM DATE-FLAGGED",
              font=load_typeface(SERIF_BOLD, 15), fill=INK)
    row_h = 32
    col_w, col_gap = 318, 14
    for i, num in enumerate(TAIL_NUMBERS):
        story = BY_NUMBER[num]
        _, _, head, deck, _, pure = story
        col, row = i % 3, i // 3
        x = 20 + col * (col_w + col_gap)
        y = y0 + 24 + row * row_h
        head_font = load_typeface(SERIF_BOLD, 12)
        deck_font = load_typeface(SERIF, 11)
        pill_font = load_typeface(SANS_BOLD, 10)
        draw.text((x, y), "\u2022", font=deck_font, fill=RED)
        tx = x + 14
        pw = date_pill(draw, tx, y - 1, pure, pill_font)
        nx = tx + pw + 6
        if draw.textlength(head, font=head_font) > col_w - 14 - (nx - x):
            problems.append(f"TAIL HEADLINE TOO LONG: {head!r}")
            print(f"TAIL HEADLINE TOO LONG: {head!r}")
        draw.text((nx, y), head, font=head_font, fill=INK)
        if draw.textlength(deck, font=deck_font) > col_w - 14:
            problems.append(f"TAIL DECK TOO LONG: {deck!r}")
            print(f"TAIL DECK TOO LONG: {deck!r}")
        draw.text((tx, y + 15), deck, font=deck_font, fill=FADED)
    audit("tail list", y0 + 24 + 9 * row_h, 948)


def paint_bottom(draw):
    y0, h = 950, 56
    # world map, left
    draw.rectangle([20, y0, 400, y0 + h], outline=INK, width=1, fill=CARD)
    draw.text((28, y0 + 2), "WHERE IT HAPPENED",
              font=load_typeface(SANS_BOLD, 9), fill=RED)
    ox, oy = 30, y0 + 2
    for poly in [
            [(32, 35), (40, 17), (76, 11), (108, 17), (100, 29), (76, 37)],
            [(92, 37), (108, 37), (104, 45), (94, 45)],
            [(148, 17), (164, 13), (172, 21), (160, 27)],
            [(148, 27), (176, 27), (180, 43), (160, 47), (150, 37)],
            [(180, 13), (248, 11), (280, 19), (272, 31), (220, 33), (186, 25)],
            [(252, 39), (276, 39), (276, 47), (254, 47)]]:
        draw.polygon([(ox + px, oy + round(py * 0.75)) for px, py in poly],
                     fill=LAND)
    for px, py, label in MAP_PINS:
        cx, cy = ox + px, oy + round(py * 0.75)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        nf = load_typeface(SANS_BOLD, 7)
        tw = draw.textlength(label, font=nf)
        draw.text((cx - tw / 2, cy - 3), label, font=nf, fill=PAPER)
    leg_font = load_typeface(SANS, 7)
    draw.text((28, y0 + 38), MAP_LEGEND_1, font=leg_font, fill=FADED)
    draw.text((28, y0 + 47), MAP_LEGEND_2, font=leg_font, fill=FADED)
    # DATE CHECK box, right
    draw.rectangle([412, y0, 1004, y0 + h], outline=RED, width=2,
                   fill="#FDF6E3")
    draw.text((422, y0 + 2), "DATE CHECK \u2014 31 OF 40 STORIES ARE PURE 27 NOV",
              font=load_typeface(SANS_BOLD, 9), fill=RED)
    body_font = load_typeface(SERIF, 8)
    dy = y0 + 14
    for line in DATE_CHECK_LINES:
        if draw.textlength(line, font=body_font) > 572:
            problems.append(f"DATE CHECK TOO LONG: {line!r}")
            print(f"DATE CHECK TOO LONG: {line!r}")
        draw.text((422, dy), line, font=body_font, fill=INK)
        dy += 10
    audit("date check box", dy, y0 + h - 2)
    audit("bottom row", y0 + h, 1006)


def paint_footer(draw):
    draw.rectangle([20, 1010, CANVAS_W - 20, 1011], fill=INK)
    centred(draw, CANVAS_W // 2, 1012, FOOTER,
            load_typeface(SERIF, 10), FADED)
    audit("footer", 1023, 1024)


def build():
    image = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(image)
    paint_header(draw)
    paint_figures(draw)
    paint_leads(draw)
    paint_cards(draw)
    paint_timeline(draw)
    paint_tail(draw)
    paint_bottom(draw)
    paint_footer(draw)
    image.save(OUT_PATH)
    print(f"saved {OUT_PATH}")
    print(f"ISSUES: {len(problems)}")
    for item in problems:
        print(" -", item)


if __name__ == "__main__":
    build()
