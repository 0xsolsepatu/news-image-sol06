#!/usr/bin/env python3
"""The World in One Day v2 — front page summing up Friday 27 November 2026.

Build tool only; NOT part of the graded entry (main.py copies entry.png).
Draws a 1024x1024 newspaper front page with Pillow: cream paper, serif
masthead, six-number figure strip, three illustrated lead panels, an
eleven-card story grid (six cards in row one, five in row two, each with a
small drawn scene), a one-row UTC timeline strip, a thirty-two-item tail
list in three columns, a world map with 5 pins, a DATE CHECK box and a
footer.

46 stories, ALL pure 27 Nov (each happened, or was first reported, on
Fri 27 Nov 2026 in some time zone). v1's nine flagged [26 NOV] items are
dropped entirely, so this edition carries no date pills for older stories —
every story wears the pale outline "27 NOV" pill. The Eagles-Cowboys game
kicked off 21:30 UTC Thu and ended ~00:30 UTC Fri; the chess match's first
rest day falls Fri 27 Nov (Guardian + FIDE schedule). Every headline and
deck below is copied from RESEARCH-v2.md. See GEMINI-v2-REVIEW-NOTE.md
for the design review.

Layout budget (1024px): header ends 122, figures 128-178, leads 184-360,
grid 366-572, timeline 578-606, tail 612-942, bottom 948-1002, footer
1006-1023. 14 drawn scenes: 3 lead illustrations + 11 grid mini-scenes.
Tail rows are 28px with 12pt headlines / 10pt decks so the tail stays
legible at 300px; grid decks are INK, not FADED, for contrast at
thumbnail size.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/makefun-newsimage-20261127/entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = "#F7F1E3"
CARD = "#FFFDF6"
INK = "#1A1A1A"
RED = "#B91C1C"
FADED = "#6B6455"
HAIR = "#B8AE97"
NAVY = "#1E2A4A"
LAND = "#D8C9A3"
GOLD = "#C9A86A"
BLUE = "#2B4C8C"
GREEN = "#2E6B34"
ORANGE = "#E07B00"

issues = []


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(d, cx, y, text, font, colour):
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font,
           fill=colour)


def pill_solid(d, x, y, label, font, h=16):
    w = d.textlength(label, font=font) + 12
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=INK)
    tw = d.textlength(label, font=font)
    d.text((x + (w - tw) / 2, y + (h - 12) / 2 - 1), label, font=font,
           fill=PAPER)
    return w


def pill_outline(d, x, y, label, font, h=16):
    w = d.textlength(label, font=font) + 12
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, outline=INK,
                        width=1, fill=CARD)
    tw = d.textlength(label, font=font)
    d.text((x + (w - tw) / 2, y + (h - 12) / 2 - 1), label, font=font,
           fill=INK)
    return w


def check(name, end, limit):
    if end > limit:
        issues.append(f"OVERFLOW {name}: ends {end}, limit {limit}")
        print(f"OVERFLOW {name}: ends {end}, limit {limit}")
    else:
        print(f"OK {name}: ends {end}/{limit}")


# ------------------------------------------------------------------ stories
# (number, tag, headline, deck, source). Caps: leads head 48 / deck 78;
# grid row 1 head 40 / deck 52; grid row 2 head 50 / deck 64; tail head 37 /
# deck 58. All 46 are pure 27 Nov.
STORIES = [
    (1, "MIDEAST", "Mine blast hits tanker in Hormuz",
     "IRGC says a tanker struck a mine Friday; a second turned back. Unverified.",
     "DPA"),
    (2, "ECONOMY", "Black Friday: $12.9bn online today",
     "Adobe forecasts $12.9bn in US online sales, +9.2%; Thanksgiving hit $7.1bn.",
     "ADOBE"),
    (3, "EUROPE", "Five nations sign $6bn BAE deal",
     "CV90 contracts signed in Stockholm; 400+ vehicles for five armies.",
     "BAE"),
    (4, "SPORT", "Eagles stun Cowboys 39\u201338",
     "21 down; Elliott's 59-yard kick seals it.",
     "REUTERS"),
    (5, "ASIA", "Kim vows more nuclear warheads",
     "KCNA: arsenal \u2018absolutely inviolable\u2019.",
     "REUTERS"),
    (6, "EUROPE", "EU budget talks end in deadlock",
     "\u20ac1.7tn budget, \u20ac45bn loan stall; 24 back loan.",
     "REUTERS"),
    (7, "OCEANIA", "NZ coalition one seat short",
     "65 of 130 seats; Luxon needs Opportunity Party.",
     "REUTERS"),
    (8, "EUROPE", "Bundestag passes \u20ac556bn budget",
     "Defence \u20ac109.7bn; new debt \u20ac210.4bn.",
     "REUTERS"),
    (9, "MARKETS", "Gold rebounds above $3,600",
     "Spot gold +2.3% to $3,650; silver jumps 5%.",
     "REUTERS"),
    (10, "MARKETS", "Wall St rallies on Black Friday",
     "Nasdaq +1.6%, Dow +500 in short session; chips lead.",
     "BARRON'S"),
    (11, "SPORT", "NZ reach 246\u20135 on day one",
     "Latham 59, Blundell 53* as Test opens in Christchurch.",
     "REUTERS"),
    (12, "SPORT", "Antonelli tops Qatar practice",
     "New champion 1:23.217; Mercedes one-two, Hadjar third.",
     "FORMULA 1"),
    (13, "EUROPE", "Tube strike: 8 days begin",
     "London drivers walk out; Circle, Piccadilly shut.",
     "REPORTS"),
    (14, "EUROPE", "IAEA seeks Zaporizhzhia ceasefire",
     "28th loss of offsite power; diesel generators run.",
     "REUTERS"),
    (15, "ECONOMY", "Black Friday doors swing open",
     "Target gift cards to $1,000; 1 in 3 shoppers use AI.",
     "THESTREET"),
    (16, "EUROPE", "Zelenskyy warns of grid attack",
     "Russia plans major strike on power grid \u2018in days\u2019.",
     "AP"),
    (17, "MIDEAST", "Israeli strikes kill 10 in Gaza",
     "Health officials report toll as ceasefire frays.",
     "AP"),
    (18, "ENERGY", "Brent holds near month high",
     "$96.19 a barrel, +3.9% on the week; Hormuz hit.",
     "REUTERS"),
    (19, "MARKETS", "Asia shares steady; dollar climbs",
     "Nikkei +0.7%; dollar set for 3rd monthly gain.",
     "REUTERS"),
    (20, "ASIA", "Duterte\u2019s ICC trial starts Monday",
     "85 murder counts from 2011\u201318 drug war; families wait.",
     "REUTERS"),
    (21, "ASIA", "Japan eyes $350bn defence plan",
     "\u00a556.3tn over five years, below military\u2019s wishes.",
     "REUTERS"),
    (22, "EUROPE", "Biggest prisoner swap \u2018shortly\u2019",
     "US envoy: Russia\u2013Ukraine swap ahead of holidays.",
     "REPORTS"),
    (23, "EUROPE", "No attack on Putin home, US says",
     "Kushner: alleged Ukraine strike \u2018did not happen\u2019.",
     "REPORTS"),
    (24, "MIDEAST", "Houthis claim Jizan port strikes",
     "Yemen rebels say they hit Saudi ports; Riyadh silent.",
     "REPORTS"),
    (25, "ASIA", "Indonesia eyes palm-oil fee",
     "Regulator proposes 0.5% levy on export sales.",
     "KUCOIN"),
    (26, "ENERGY", "OPEC+ likely extends output cap",
     "Targets to hold into Q1 2027; meeting Sunday.",
     "REUTERS"),
    (27, "ECONOMY", "Trafigura to shut zinc smelter",
     "Nyrstar plant in Netherlands closes on energy costs.",
     "KUCOIN"),
    (28, "ASIA", "S. Korea court clears ex-president",
     "Ousted leader\u2019s perjury acquittal confirmed.",
     "REPORTS"),
    (29, "CULTURE", "Depardieu to face rape trial",
     "French actor to stand trial, lawyer says.",
     "REPORTS"),
    (30, "EUROPE", "Arrests at William & Kate\u2019s",
     "Two held over burglary at country estate.",
     "REPORTS"),
    (31, "USA", "FAA halts Miami air traffic",
     "FedEx cargo jet leaves runway; traffic cancelled.",
     "REPORTS"),
    (32, "EUROPE", "Record 2,000 reach Canaries",
     "Refugees land in Spain\u2019s islands in a single day.",
     "REPORTS"),
    (33, "ASIA", "Myanmar rejects ICJ ruling parts",
     "Junta won\u2019t abide by \u2018inappropriate\u2019 aspects.",
     "REPORTS"),
    (34, "EUROPE", "Germany pays Syrians to return",
     "Bigger cash bonuses in expanded return plan.",
     "REPORTS"),
    (35, "EUROPE", "ECB picks Hern\u00e1ndez de Cos",
     "Spaniard to lead central bank; continuity seen.",
     "REUTERS"),
    (36, "EUROPE", "Su-34 base hit in Volgograd",
     "Russian fighter-jet base struck, reports say.",
     "REPORTS"),
    (37, "EUROPE", "Power station hit in Stavropol",
     "Assault strikes regional power station.",
     "REPORTS"),
    (38, "EUROPE", "UK pledges \u00a39m wind farm",
     "Funding for wind power in war-hit country.",
     "REPORTS"),
    (39, "SPORT", "Chess level at 1.5\u20131.5; rest day",
     "Game 3 drawn in 60 moves; Game 4 Saturday.",
     "GUARDIAN"),
    (40, "ASIA", "Karachi toll rises to 8 on Friday",
     "Four more bodies found after Wednesday collapse.",
     "AP"),
    (41, "USA", "Storm delays drag into Friday",
     "866 US flights cancelled by Friday morning.",
     "REPORTS"),
    (42, "ECONOMY", "Nvidia halts SE Asia shipments",
     "Tells Dell, Supermicro to stop AI servers; FT report.",
     "CRYPTOPOLITAN"),
    (43, "ASIA", "Dhaka court jails Hasina ex-aide",
     "Moon and two others held in anti-terror case.",
     "IANS"),
    (44, "OCEANIA", "Fire risk up in six states",
     "AFAC summer outlook; Flinders blaze 15,300 ha.",
     "AFAC"),
    (45, "ECONOMY", "UK shoppers to spend \u00a36.6bn",
     "PwC: \u00a36.6bn Black Friday spend expected.",
     "PWC"),
    (46, "ECONOMY", "Thanksgiving online sales $7.1bn",
     "Adobe: +10.4% on last year, reported Friday.",
     "ADOBE"),
]

BY_NUM = {s[0]: s for s in STORIES}
LEADS = [1, 2, 3]
GRID_R1 = [4, 5, 6, 7, 8, 9]
GRID_R2 = [10, 11, 12, 13, 14]
TAIL = list(range(15, 47))
LEAD_TAGS = {1: "TOP STORY", 2: "SHOPPING", 3: "DEFENCE"}

FIGURES = [
    ("$12.9bn", "BLACK FRIDAY FORECAST", "ADOBE \u00b7 27 NOV"),
    ("39\u201338", "EAGLES COMEBACK", "REUTERS \u00b7 27 NOV"),
    ("$3,650", "GOLD REBOUNDS", "REUTERS \u00b7 27 NOV"),
    ("65/130", "NZ COALITION SEATS", "REUTERS \u00b7 27 NOV"),
    ("866", "FLIGHTS AXED FRIDAY", "27 NOV"),
    ("\u20ac556bn", "GERMAN BUDGET PASSED", "REUTERS \u00b7 27 NOV"),
]

TIMELINE = [("00:30", "EAGLES 39\u201338"), ("00:45", "IAEA BID"),
            ("01:00", "KIM NUKES"), ("02:00", "NZ COUNT"),
            ("02:45", "TUBE STRIKE"), ("06:45", "GOLD $3,650"),
            ("13:00", "BAE SIGNING"), ("13:03", "HORMUZ MINE"),
            ("14:43", "FP1 ANTONELLI")]

MAP_PINS = [(205, 26, "1"), (213, 28, "2"), (284, 44, "3"),
            (158, 13, "4"), (188, 25, "5")]
MAP_LEGEND = ("1 HORMUZ MINE \u00b7 2 KARACHI TOLL \u00b7 3 CHRISTCHURCH TEST "
              "\u00b7 4 STOCKHOLM DEAL \u00b7 5 GAZA")

DATE_LINES = [
    "Masthead date: Friday 27 November 2026. All 46 stories happened, or were first reported, on 27 Nov.",
    "No [26 NOV] pills in this edition \u2014 the nine flagged items from v1 are dropped, not carried over.",
    "Left out as not 27 Nov: UNEP report (21 Oct); Hormuz two-tanker strike, UK migration, Ibiza tanker (26 Nov);",
    "Musk shares, Sarkozy order, Korea births, polio case, Carbon Budget \u2014 25 Nov or earlier (list: RESEARCH-v2.md).",
]

FOOTER = "MAKE.FUN // 27 NOV 2026 // 46 STORIES \u00b7 10 REGIONS \u00b7 14 SCENES"

# ------------------------------------------------------------------ scenes
def art_tanker(d, x, y, w, h):
    """Hormuz: tanker at sea, spiked mine at the waterline, burst."""
    for wy in (y + h - 6, y + h - 2):
        d.arc([x + 2, wy - 5, x + w - 2, wy + 5], 180, 360, fill=BLUE, width=2)
    d.polygon([(x + 10, y + h - 16), (x + w - 10, y + h - 16),
               (x + w - 24, y + h - 28), (x + 22, y + h - 28)], fill=INK)
    d.line([x + 12, y + h - 21, x + w - 12, y + h - 21], fill=CARD, width=1)
    d.rectangle([x + w * 0.55, y + h - 40, x + w * 0.55 + 26, y + h - 28],
                fill=CARD, outline=INK, width=1)
    d.rectangle([x + w * 0.64, y + h - 50, x + w * 0.64 + 8, y + h - 40],
                fill=RED)
    d.ellipse([x + w * 0.66, y + h - 56, x + w * 0.66 + 6, y + h - 50],
              outline=FADED, width=1)
    mx, my = x + w * 0.24, y + h - 20
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 7, 12
        a = math.radians(ang)
        d.line([mx + r1 * math.cos(a), my + r1 * math.sin(a),
                mx + r2 * math.cos(a), my + r2 * math.sin(a)], fill=INK,
               width=2)
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=INK)
    d.text((mx + 12, my - 16), "*", font=F(SANS_B, 16), fill=ORANGE)


def art_bags(d, x, y, w, h):
    """Black Friday: striped awning, two shopping bags, price tag."""
    for i in range(5):
        col = RED if i % 2 == 0 else CARD
        d.rectangle([x + 4 + i * (w - 8) // 5, y + 2,
                     x + 4 + (i + 1) * (w - 8) // 5, y + 12], fill=col,
                    outline=INK, width=1)
    d.polygon([(x + 14, y + 24), (x + 38, y + 24), (x + 42, y + h - 4),
               (x + 10, y + h - 4)], fill=GOLD, outline=INK, width=1)
    d.arc([x + 18, y + 16, x + 34, y + 28], 180, 360, fill=INK, width=2)
    d.polygon([(x + w - 44, y + 28), (x + w - 22, y + 28),
               (x + w - 18, y + h - 4), (x + w - 48, y + h - 4)], fill=BLUE,
              outline=INK, width=1)
    d.arc([x + w - 40, y + 20, x + w - 26, y + 32], 180, 360, fill=INK,
          width=2)
    d.rectangle([x + w - 20, y + 4, x + w - 4, y + 16], fill=CARD,
                outline=RED, width=1)
    d.text((x + w - 17, y + 4), "%", font=F(SANS_B, 10), fill=RED)


def art_cv90(d, x, y, w, h):
    """BAE deal: tracked armoured vehicle under five small flags."""
    for i, col in enumerate([BLUE, GOLD, RED, GREEN, NAVY]):
        fx = x + 12 + i * (w - 24) // 5
        d.line([fx, y + 2, fx, y + 11], fill=INK, width=1)
        d.rectangle([fx, y + 2, fx + 12, y + 9], fill=col, outline=INK,
                    width=1)
    d.rectangle([x + w * 0.36, y + 14, x + w * 0.36 + 34, y + 24], fill=INK)
    d.line([x + w * 0.36 + 34, y + 18, x + w - 10, y + 16], fill=INK,
           width=3)
    d.polygon([(x + 18, y + 40), (x + w - 18, y + 40),
               (x + w - 28, y + 28), (x + 28, y + 28)], fill=NAVY)
    d.line([x + 20, y + 34, x + w - 20, y + 34], fill=CARD, width=1)
    d.rounded_rectangle([x + 10, y + 42, x + w - 10, y + 52], radius=5,
                        fill=INK)
    for i in range(5):
        cx = x + 20 + i * (w - 40) // 4
        d.ellipse([cx - 4, y + 43, cx + 4, y + 51], fill=CARD,
                  outline=INK, width=1)


def art_stadium(d, x, y, w, h):
    """Eagles: stadium arc, goalposts, ball sailing through."""
    d.arc([x + 4, y + 2, x + w - 4, y + h + 16], 180, 360, fill=NAVY, width=3)
    for gx in (x + w * 0.3, x + w * 0.7):
        d.line([gx, y + h - 20, gx, y + h - 2], fill=INK, width=2)
    d.line([x + w * 0.3, y + h - 20, x + w * 0.7, y + h - 20], fill=INK,
           width=2)
    bx, by = x + w * 0.52, y + 9
    d.ellipse([bx - 9, by - 6, bx + 9, by + 6], fill="#7A4A21", outline=INK,
              width=1)
    d.line([bx - 9, by, bx + 9, by], fill=PAPER, width=1)
    d.line([bx - 4, by - 5, bx - 4, by + 5], fill=PAPER, width=1)


def art_rocket(d, x, y, w, h):
    """Kim: missile rising diagonally, flame, smoke, stars."""
    d.arc([x + 2, y + h - 24, x + w * 0.55, y + h + 6], 90, 200, fill=FADED,
          width=2)
    d.polygon([(x + w * 0.42, y + 26), (x + w * 0.52, y + 34),
               (x + w * 0.62, y + 18), (x + w * 0.52, y + 10)], fill=INK)
    d.polygon([(x + w * 0.52, y + 10), (x + w * 0.62, y + 18),
               (x + w * 0.72, y + 4)], fill=RED)
    d.polygon([(x + w * 0.42, y + 26), (x + w * 0.52, y + 34),
               (x + w * 0.36, y + 38)], fill=RED)
    d.polygon([(x + w * 0.40, y + 32), (x + w * 0.50, y + 40),
               (x + w * 0.34, y + h - 2)], fill=ORANGE)
    for sx, sy in ((x + 8, y + 4), (x + w - 22, y + 28)):
        d.text((sx, sy), "\u2605", font=F(SANS_B, 12), fill=GOLD)


def art_summit(d, x, y, w, h):
    """EU deadlock: long table, three flags, seated delegates."""
    d.rectangle([x, y + h - 12, x + w, y + h - 6], fill=NAVY)
    for i, cx in enumerate((x + w * 0.22, x + w * 0.5, x + w * 0.78)):
        d.rectangle([cx - 3, y + 6, cx + 3, y + h - 12], fill=INK)
        d.rectangle([cx + 3, y + 6, cx + 26, y + 20],
                    fill=[BLUE, GOLD, RED][i], outline=INK, width=1)
        d.ellipse([cx - 8, y + h - 24, cx + 8, y + h - 12], fill=FADED)
    d.text((x + w - 54, y + h - 26), "\u20ac1.7tn", font=F(SERIF_B, 13),
           fill=RED)


def art_ballot(d, x, y, w, h):
    """NZ count: ballot box with a paper going in and a check."""
    d.rectangle([x + 6, y + h - 16, x + w - 6, y + h - 2], fill=NAVY)
    d.rectangle([x + 16, y + 2, x + w - 16, y + 8], fill=INK)
    d.polygon([(x + w // 2 - 7, y + 8), (x + w // 2 + 7, y + 8),
               (x + w // 2, y + 18)], fill=PAPER)
    d.line([x + w - 16, y + h - 12, x + w - 10, y + h - 6], fill=GREEN,
           width=2)
    d.line([x + w - 10, y + h - 6, x + w - 2, y + h - 14], fill=GREEN,
           width=2)


def art_parliament(d, x, y, w, h):
    """Bundestag: columned hall with dome and flag."""
    for i in range(3):
        d.line([x + 8, y + h - 4 - i * 3, x + w - 8, y + h - 4 - i * 3],
               fill=INK, width=2)
    for i in range(4):
        cx = x + 16 + i * (w - 32) // 3
        d.rectangle([cx - 3, y + 12, cx + 3, y + h - 10], fill=INK)
    d.polygon([(x + 8, y + 12), (x + w - 8, y + 12), (x + w // 2, y + 2)],
              fill=NAVY)
    d.arc([x + w // 2 - 10, y + 12, x + w // 2 + 10, y + 26], 180, 360,
          fill=RED, width=2)
    d.line([x + w - 8, y + 2, x + w - 8, y + 12], fill=INK, width=1)
    d.rectangle([x + w - 8, y + 2, x + w + 2, y + 8], fill=RED, outline=INK,
                width=1)


def art_goldbars(d, x, y, w, h):
    """Gold: stacked bullion bars with a sparkle."""
    d.polygon([(x + 12, y + h - 4), (x + w - 12, y + h - 4),
               (x + w - 18, y + h - 14), (x + 18, y + h - 14)], fill=GOLD,
              outline=INK, width=1)
    d.polygon([(x + 24, y + h - 14), (x + w - 24, y + h - 14),
               (x + w - 30, y + h - 24), (x + 30, y + h - 24)], fill=GOLD,
              outline=INK, width=1)
    d.polygon([(x + w // 2 - 18, y + h - 24), (x + w // 2 + 18, y + h - 24),
               (x + w // 2 + 12, y + h - 34), (x + w // 2 - 12, y + h - 34)],
              fill=GOLD, outline=INK, width=1)
    d.text((x + w // 2 - 4, y + h - 33), "$", font=F(SANS_B, 10), fill=INK)
    d.text((x + w - 16, y + 2), "*", font=F(SANS_B, 14), fill=GOLD)


def art_chart(d, x, y, w, h):
    """Wall St: rising bars with an upward arrow."""
    d.line([x + 4, y + h - 4, x + w - 4, y + h - 4], fill=INK, width=2)
    d.line([x + 4, y + 2, x + 4, y + h - 4], fill=INK, width=2)
    bars = [6, 10, 8, 14, 18]
    bw = w // 6
    for i, bh in enumerate(bars):
        bx = x + 8 + i * bw
        d.rectangle([bx, y + h - 6 - bh, bx + bw - 3, y + h - 6],
                    fill=GREEN if i < 4 else RED)
    d.line([x + 8, y + h - 12, x + w - 8, y + 4], fill=RED, width=2)
    d.polygon([(x + w - 8, y + 4), (x + w - 16, y + 4),
               (x + w - 8, y + 12)], fill=RED)


def art_cricket(d, x, y, w, h):
    """Christchurch Test: bat, ball and stumps."""
    d.polygon([(x + w * 0.3, y + 4), (x + w * 0.42, y + 4),
               (x + w * 0.5, y + h - 8), (x + w * 0.38, y + h - 8)],
              fill="#C89B6A", outline=INK, width=1)
    d.rectangle([x + w * 0.33, y + h - 16, x + w * 0.39, y + h - 6],
                fill=INK)
    d.ellipse([x + w - 22, y + 6, x + w - 10, y + 18], fill=RED, outline=INK,
              width=1)
    d.arc([x + w - 22, y + 6, x + w - 10, y + 18], 300, 60, fill=PAPER,
          width=1)
    for i in range(3):
        sx = x + 8 + i * 5
        d.line([sx, y + h - 14, sx, y + h - 2], fill=GOLD, width=2)
    d.line([x + 8, y + h - 16, x + 18, y + h - 16], fill=GOLD, width=2)


def art_racecar(d, x, y, w, h):
    """Qatar FP1: low formula car with rear wing and speed lines."""
    d.polygon([(x + 8, y + h - 12), (x + w - 8, y + h - 12),
               (x + w - 16, y + h - 20), (x + 20, y + h - 20)], fill=RED)
    d.polygon([(x + w * 0.42, y + h - 26), (x + w * 0.58, y + h - 26),
               (x + w * 0.54, y + h - 20), (x + w * 0.46, y + h - 20)],
              fill=INK)
    d.line([x + w - 6, y + h - 26, x + w - 6, y + h - 18], fill=INK, width=2)
    d.rectangle([x + w - 12, y + h - 28, x + w - 2, y + h - 24], fill=INK)
    for cx in (x + w * 0.24, x + w * 0.76):
        d.ellipse([cx - 6, y + h - 10, cx + 6, y + h + 2], fill=INK)
        d.ellipse([cx - 2, y + h - 6, cx + 2, y + h - 2], fill=CARD)
    for i, ly in enumerate((y + 6, y + 12, y + 18)):
        d.line([x + 2, ly, x + 14 + i * 4, ly], fill=FADED, width=2)


def art_train(d, x, y, w, h):
    """Tube strike: red train front, windows, rails."""
    d.rounded_rectangle([x + 6, y + 2, x + w - 6, y + h - 6], radius=5,
                        fill=RED)
    d.rectangle([x + 12, y + 6, x + w // 2 - 2, y + 13], fill=PAPER)
    d.rectangle([x + w // 2 + 2, y + 6, x + w - 12, y + 13], fill=PAPER)
    d.ellipse([x + w // 2 - 4, y + h - 12, x + w // 2 + 4, y + h - 4],
              fill=GOLD, outline=INK, width=1)
    d.line([x + 4, y + h - 2, x + w - 4, y + h - 2], fill=INK, width=2)


def art_atom(d, x, y, w, h):
    """IAEA: nucleus with two orbits and electrons."""
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    d.ellipse([cx - r, cy - 4, cx + r, cy + 4], outline=NAVY, width=1)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    d.ellipse([cx + r - 5, cy - r, cx + r, cy - r + 5], fill=GOLD,
              outline=INK, width=1)
    d.ellipse([cx - r, cy + r - 5, cx - r + 5, cy + r], fill=GOLD,
              outline=INK, width=1)


LEAD_ART = {1: art_tanker, 2: art_bags, 3: art_cv90}
GRID_ART = {4: art_stadium, 5: art_rocket, 6: art_summit, 7: art_ballot,
            8: art_parliament, 9: art_goldbars, 10: art_chart,
            11: art_cricket, 12: art_racecar, 13: art_train, 14: art_atom}

# ------------------------------------------------------------------ paint
def draw_masthead(d):
    center(d, W // 2, 4, "THE WORLD IN ONE DAY", F(SERIF_B, 58), INK)
    center(d, W // 2, 70, "FRIDAY 27 NOVEMBER 2026", F(SERIF_B, 30), RED)
    d.rectangle([20, 116, W - 20, 118], fill=INK)
    d.rectangle([20, 120, W - 20, 121], fill=INK)
    check("masthead", 122, 122)


def draw_stats(d):
    y0, h = 128, 50
    box_w, gap = 157, 8
    for i, (num, label, src) in enumerate(FIGURES):
        x = 20 + i * (box_w + gap)
        d.rectangle([x, y0, x + box_w, y0 + h], outline=INK, width=1)
        center(d, x + box_w // 2, y0 + 2, num, F(SERIF_B, 24),
               RED if i % 2 == 0 else INK)
        center(d, x + box_w // 2, y0 + 27, label, F(SANS_B, 9), FADED)
        pf = F(SANS_B, 8)
        w = d.textlength(src, font=pf) + 12
        pill_solid(d, x + (box_w - w) // 2, y0 + 38, src, pf, h=13)
    check("stat strip", y0 + h, 178)


def draw_leads(d):
    y0, h = 184, 176
    pw, gap = 320, 12
    for i, num in enumerate(LEADS):
        _, tag, head, deck, src = BY_NUM[num]
        x = 20 + i * (pw + gap)
        d.rectangle([x, y0, x + pw, y0 + h], outline=INK, width=2, fill=CARD)
        LEAD_ART[num](d, x + 8, y0 + 6, pw - 16, 54)
        tf = F(SERIF_B, 22)
        tl = wrap(d, head, tf, pw - 24)
        if len(tl) > 2:
            issues.append(f"LEAD TITLE TOO LONG: {head!r}")
            print(f"LEAD TITLE TOO LONG: {head!r}")
        ty = y0 + 64
        for line in tl[:2]:
            d.text((x + 12, ty), line, font=tf, fill=INK)
            ty += 26
        df = F(SERIF, 14)
        dl = wrap(d, deck, df, pw - 24)
        if len(dl) > 2:
            issues.append(f"LEAD DECK TOO LONG: {deck!r}")
            print(f"LEAD DECK TOO LONG: {deck!r}")
        dy = ty + 2
        for line in dl[:2]:
            d.text((x + 12, dy), line, font=df, fill=INK)
            dy += 17
        ly = y0 + h - 22
        cf = F(SANS_B, 11)
        cw = pill_solid(d, x + 12, ly, LEAD_TAGS[num], cf)
        d.text((x + 16 + cw, ly + 2), f"{tag} \u00b7 {src}", font=F(SANS, 11),
               fill=FADED)
        pf = F(SANS_B, 10)
        pw2 = d.textlength("27 NOV", font=pf) + 12
        pill_outline(d, x + pw - 12 - pw2, ly, "27 NOV", pf)
        check(f"lead {num} {head[:24]}", dy, ly - 2)
    check("lead panels", y0 + h, 360)


def draw_grid(d):
    y0, ch, rgap = 366, 100, 6
    r1w, r1g = 156, 9
    r2w, r2g = 187, 12
    for i, num in enumerate(GRID_R1 + GRID_R2):
        _, tag, head, deck, src = BY_NUM[num]
        if i < 6:
            cw, cg = r1w, r1g
        else:
            cw, cg = r2w, r2g
            i -= 6
        col = i
        x = 20 + col * (cw + cg)
        y = y0 + (0 if num in GRID_R1 else ch + rgap)
        d.rectangle([x, y, x + cw, y + ch], outline=HAIR, width=1, fill=CARD)
        d.rectangle([x, y, x + 4, y + ch], fill=RED)
        tf = F(SANS_B, 8 if num in GRID_R1 else 9)
        d.text((x + 8, y + 3), f"{tag} \u00b7 {src}", font=tf, fill=RED)
        pf = F(SANS_B, 9)
        pw2 = d.textlength("27 NOV", font=pf) + 12
        pill_outline(d, x + cw - 8 - pw2, y + 3, "27 NOV", pf)
        GRID_ART[num](d, x + 8, y + 19, cw - 16, 26)
        hf = F(SERIF_B, 12)
        hl = wrap(d, head, hf, cw - 16)
        if len(hl) > 2:
            issues.append(f"GRID TITLE TOO LONG: {head!r}")
            print(f"GRID TITLE TOO LONG: {head!r}")
        ty = y + 47
        for line in hl[:2]:
            d.text((x + 8, ty), line, font=hf, fill=INK)
            ty += 14
        df = F(SERIF, 10)
        dl = wrap(d, deck, df, cw - 16)
        if len(dl) > 2:
            issues.append(f"GRID DECK TOO LONG: {deck!r}")
            print(f"GRID DECK TOO LONG: {deck!r}")
        dy = y + 76
        for line in dl[:2]:
            d.text((x + 8, dy), line, font=df, fill=INK)
            dy += 11
        check(f"grid {num} {head[:24]}", dy, y + ch - 2)
    check("story grid", y0 + 2 * ch + rgap, 572)


def draw_timeline(d):
    y0, h = 578, 28
    d.rectangle([20, y0, W - 20, y0 + h], outline=HAIR, width=1, fill=CARD)
    ry = y0 + 8
    d.text((28, ry), "FRI 27 NOV \u00b7 UTC", font=F(SANS_B, 8), fill=RED)
    slot = (1004 - 140) / len(TIMELINE)
    for j, (tm, label) in enumerate(TIMELINE):
        cx = 140 + slot * (j + 0.5)
        sw = (d.textlength(tm, font=F(SANS_B, 8)) + 3 +
              d.textlength(label, font=F(SANS, 8)))
        if sw > slot - 4:
            issues.append(f"TIMELINE TOO LONG: {tm} {label}")
            print(f"TIMELINE TOO LONG: {tm} {label}")
        tx = cx - sw / 2
        d.text((tx, ry), tm, font=F(SANS_B, 8), fill=INK)
        d.text((tx + d.textlength(tm, font=F(SANS_B, 8)) + 3, ry), label,
               font=F(SANS, 8), fill=FADED)
        d.line([cx, ry + 11, cx, ry + 13], fill=RED, width=1)
    check("timeline", y0 + h, 606)


def draw_tail(d):
    y0 = 612
    d.rectangle([20, y0, W - 20, y0 + 2], fill=INK)
    d.text((20, y0 + 4), "MORE OF THE DAY \u2014 EVERY ITEM PURE 27 NOV",
           font=F(SERIF_B, 15), fill=INK)
    row_h, col_w, col_gap = 28, 318, 14
    for i, num in enumerate(TAIL):
        _, _, head, deck, _ = BY_NUM[num]
        col, row = i % 3, i // 3
        x = 20 + col * (col_w + col_gap)
        y = y0 + 22 + row * row_h
        hf, df, pf = F(SERIF_B, 12), F(SERIF, 10), F(SANS_B, 10)
        d.text((x, y), "\u2022", font=df, fill=RED)
        tx = x + 14
        pw2 = pill_outline(d, tx, y - 1, "27 NOV", pf)
        nx = tx + pw2 + 6
        if d.textlength(head, font=hf) > col_w - 14 - (nx - x):
            issues.append(f"TAIL HEADLINE TOO LONG: {head!r}")
            print(f"TAIL HEADLINE TOO LONG: {head!r}")
        d.text((nx, y), head, font=hf, fill=INK)
        if d.textlength(deck, font=df) > col_w - 14:
            issues.append(f"TAIL DECK TOO LONG: {deck!r}")
            print(f"TAIL DECK TOO LONG: {deck!r}")
        d.text((tx, y + 13), deck, font=df, fill=FADED)
    check("tail list", y0 + 22 + 11 * row_h, 942)


def draw_bottom(d):
    y0, h = 948, 54
    d.rectangle([20, y0, 400, y0 + h], outline=INK, width=1, fill=CARD)
    d.text((28, y0 + 2), "WHERE IT HAPPENED", font=F(SANS_B, 9), fill=RED)
    ox, oy = 30, y0 + 2
    for poly in [
            [(28, 34), (38, 16), (72, 10), (104, 16), (96, 28), (72, 36)],
            [(88, 36), (104, 36), (100, 44), (90, 44)],
            [(144, 16), (160, 12), (168, 20), (156, 26)],
            [(144, 26), (172, 26), (176, 42), (156, 46), (146, 36)],
            [(176, 12), (244, 10), (276, 18), (268, 30), (216, 32),
             (182, 24)],
            [(248, 38), (272, 38), (272, 46), (250, 46)]]:
        d.polygon([(ox + px, oy + round(py * 0.75)) for px, py in poly],
                  fill=LAND)
    for px, py, label in MAP_PINS:
        cx, cy = ox + px, oy + round(py * 0.75)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        nf = F(SANS_B, 7)
        tw = d.textlength(label, font=nf)
        d.text((cx - tw / 2, cy - 3), label, font=nf, fill=PAPER)
    d.text((28, y0 + 38), MAP_LEGEND, font=F(SANS, 7), fill=FADED)
    d.rectangle([412, y0, 1004, y0 + h], outline=RED, width=2,
                fill="#FDF6E3")
    d.text((422, y0 + 2), "DATE CHECK \u2014 ALL 46 STORIES ARE PURE 27 NOV",
           font=F(SANS_B, 9), fill=RED)
    bf = F(SERIF, 8)
    dy = y0 + 14
    for line in DATE_LINES:
        if d.textlength(line, font=bf) > 572:
            issues.append(f"DATE CHECK TOO LONG: {line!r}")
            print(f"DATE CHECK TOO LONG: {line!r}")
        d.text((422, dy), line, font=bf, fill=INK)
        dy += 9
    check("date check box", dy, y0 + h - 2)
    check("bottom row", y0 + h, 1002)


def draw_footer(d):
    d.rectangle([20, 1006, W - 20, 1007], fill=INK)
    center(d, W // 2, 1008, FOOTER, F(SERIF, 10), FADED)
    check("footer", 1023, 1024)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_stats(d)
    draw_leads(d)
    draw_grid(d)
    draw_timeline(d)
    draw_tail(d)
    draw_bottom(d)
    draw_footer(d)
    img.save(OUT)
    print(f"saved {OUT}")
    print(f"ISSUES: {len(issues)}")
    for item in issues:
        print(" -", item)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
