# BUILD — news-image-20261127 "The World in One Day"

Entry: newspaper front page summing up Friday 27 November 2026.
Built in a fresh session started after the competition opened (00:00 UTC /
07:00 WIB 27 Nov 2026). All code written from scratch in this session; the
26 Nov renderer was read once for layout-geometry reference only.

## Design

- 1024×1024 PNG, cream paper (#F7F1E3), serif masthead
  "THE WORLD IN ONE DAY" + "FRIDAY 27 NOVEMBER 2026".
- 6-number stat strip: EU budget €1.7tn deadlocked · Eagles 39–38 ·
  Brent $96.19 (+3.9% week) · NZ coalition 65/130 · ~2,000 Canaries
  arrivals · Cairo fire 30+ [26 Nov].
- 3 lead panels with flat drawn illustrations (EU summit flags; Kim
  missile; Eagles stadium + goalposts) + verification labels + source tags.
- 10-card grid (stories #4–#13), each with a small drawn scene.
- One-row UTC timeline, 00:35–03:00 UTC — the day's first hours, "when the
  world learned it" (built ~03:30 UTC, so the timeline covers what had been
  reported by then; later hours were not yet reported at build time).
- 27-item tail list in 3 columns; world map with 5 numbered pins + legend;
  DATE CHECK box; footer "MAKE.FUN // 27 NOV 2026 // 40 STORIES · 12 REGIONS
  · 13 SCENES".

## Gemini design review (NO-GO, overruled on evidence — see GEMINI-REVIEW-NOTE.md)

Gemini's verdict was NO-GO, but every one of its factual claims failed
verification against the sources, so only its two sound cautions were applied:
1. Eagles final whistle moved 00:30 → 00:35 UTC (kickoff was 21:30 UTC per
   Sportradar; Gemini's claimed 03:30–04:00 UTC finish assumed a start time
   that never happened).
2. Cairo toll given as "30+" (sources vary 30–32).
Gemini also called the chess rest day "unverifiable/hypothetical" — wrong:
Guardian (26 Nov 21:11 UTC) and the FIDE schedule both say Fri 27 Nov is a
rest day, Game 4 Sat 28 Nov. Its design advice (cut to 15–20 stories, drop
the DATE CHECK box) was rejected: this exact 40-story density is the proven
pattern of this series (26 Nov v3 got CONDITIONAL GO from Gemini itself).

## Stories (40: 31 pure 27 Nov, 9 flagged [26 Nov])

Pure 27 Nov: #1 EU budget deadlock · #2 Kim vows more warheads · #3 Eagles
39–38 Cowboys · #4 NZ coalition one short · #5 IAEA Zaporizhzhia bid ·
#6 Black Friday opens · #7 Zelenskyy grid warning · #8 Gaza strikes kill 10
· #9 Brent near month high · #10 Asia shares steady · #11 Duterte ICC trial
starts Monday · #12 Japan $350bn defence plan · #13 Tube strike day 1 ·
#14 prisoner swap "shortly" · #15 no attack on Putin home, US says ·
#16 Houthis claim Jizan strikes · #17 Indonesia palm-oil fee · #18 OPEC+
extends output cap · #19 Trafigura shuts zinc smelter · #20 S. Korea court
clears ex-president · #21 Depardieu to face trial · #22 arrests at William
& Kate's · #23 FAA halts Miami traffic · #24 record 2,000 reach Canaries ·
#25 Myanmar rejects ICJ parts · #26 Germany pays Syrians to return ·
#27 ECB picks Hernández de Cos · #28 Su-34 base hit · #29 Stavropol power
station hit · #30 UK £9m wind farm · #31 chess 1.5–1.5, rest day.
Flagged [26 Nov]: #32 China protests Japan over Diaoyu · #33 Cairo fire
30+ · #34 Indonesia mine flood 14 dead · #35 two Italians killed in Kuwait
· #36 Serbia vote 27 Dec · #37 Congo Ebola 12,021 cases · #38 RSF drones
kill 19 in Sudan · #39 UK £8bn submarines · #40 Progress 97 docks at ISS.

All 40 headlines and decks rendered verbatim from RESEARCH.md (scripted
cross-check: render audit 0 issues). No story dropped or changed.

DATE CHECK box: masthead date + "31 of the 40 stories are pure 27 Nov; 9
stem from 26 Nov" + rejected: Macy's parade (in the 26 Nov image), Riemann
proof claim (one blog, unverified), "300 Russians in Mali" (no source).

## Files

- `render.py` — build tool (NOT committed to GitHub): draws entry.png.
- `main.py` — entrypoint (committed): stdlib only, copies entry.png to
  $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png), verifying PNG
  magic + IEND trailer + ≤1 MiB + byte-identical copy. Written from scratch,
  then revised once (added post-copy verification).
- `entry.png` — the image (committed). 1024×1024, 208,402 bytes, deterministic
  (identical sha256 da96e363… across repeated runs).
- `README.md` — from the live requirements template (badges for
  0xsolsepatu/news-image-sol06, run command, referral r4c0y56z).
- `LICENSE` — MIT (from the kit starter, as the kit instructs).
- `RESEARCH.md`, `gemini-design-prompt.txt`, `gemini-design-response.txt`,
  `GEMINI-REVIEW-NOTE.md` — records (the Gemini files are NOT committed to
  GitHub in the parent's flow; they sit in the workdir for the bundle).
- `.makefun/owner.json` — added by the parent at repo creation (wallet claim).

## Local check

- `python3 render.py` → 0 issues, all sections within budget.
- `main.py` run twice → identical sha256 da96e363499cd5a45349c7a5c4246d940d4
  5e506f06fd6f364f697a9649ca7ce, matching entry.png.
- Visual check at 1024px and 300px: masthead, stat strip, lead/grid
  headlines, timeline and tail structure all read at 300px; map pins were
  de-cluttered (8 → 5) after the first visual pass.
- Kit check (`node cli/makefun.mjs check --kit . --repo <workdir> --worktree`,
  run 27 Nov ~09:51 WIB): 4 passed (competition_open, snapshot 11 files /
  268,415 bytes, license_osi MIT, entrypoint main.py → python3.13), 1 failed
  (transcripts_present — no transcripts uploaded yet; expected, the parent
  bundles them), 14 skipped, 5 checked at submission (repo_public,
  repo_owner, repo_created_after_open, commit_in_repo, duplicate_snapshot —
  all parent-side at repo creation/push/submit).
