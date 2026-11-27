# GEMINI v2 REVIEW NOTE — news-image-20261127 v2

Gemini (gemini-3.5-flash-lite) review of RESEARCH-v2.md, run 28 Nov ~00:50 WIB.
Full prompt: ~/workspace/sweep-20261127/gemini-v2-prompt.txt (full
makefun_submission_checks SKILL.md attached). Full response:
~/workspace/sweep-20261127/gemini-v2-review.txt.

## Verdict: NO-GO (layout density only) — OVERRULED on evidence

### What Gemini got right (applied: nothing to change)
- Skill check: correctly found most skill rules do not bind at content-review
  time (build-in-window, bundle sessions, keypair, makefun check all bind at
  build/bundle/submit time, not here).
- Content review: NO factual contradictions in any of the 46 stories.
  Checked items all PLAUSIBLE / VERIFIED / ACCURATE TO NOTES: Hormuz Friday
  mine vs Thursday two-tanker strike; BAE signing 8:00 AM ET 27 Nov; Eagles
  whistle ~00:30 UTC Fri; NZ 65/130; Bundestag €556bn 317–260; gold above
  $3,600 after Wednesday low $3,445.89; NZ 246/5 Christchurch; Antonelli
  1:23.217 (formula1.com 14:43 UTC); Karachi toll 8 Friday; Nvidia halt
  reported 27 Nov 02:04 (vs −3.9% move Wed); Moon jailed Fri (IANS Dhaka);
  left-out list correctly excluded.

### The one objection — layout density — and why it is overruled
Gemini claims 32 tail items "would require extremely microscopic typography
(likely below 8–10px), rendering them completely illegible" and demands
trimming to 8–12 briefs. This is generic advice, not measured against the
actual layout:
1. The tail is NOT below 8–10px: headlines are 12pt, decks 10pt, in 28px
   rows — the same sizes v1 used (12pt/11pt, 32px rows) for its 27-item tail,
   which PASSED the visual check at 1024px and 300px (see BUILD.md).
   32 items in 11 rows × 28px = 308px of a 1024px canvas; the geometry fits
   with audits, and render-v2.py refuses to build on overflow.
2. Density is the proven pattern of this series AND of the live top 10:
   rank-10 live entry has 47 stories, rank-1 has 38. Cutting to 8–12 briefs
   would make the entry LESS like the entries that actually win, not more.
3. The mock-judge analysis identified date purity, story count, and pictorial
   leads as the gaps — not density. v2 fixes exactly those three.

### Applied cautions
- None from the factual review (no errors found).
- The density objection is answered by the render audit (0 issues required)
  and the visual check at 1024px + 300px, run after rendering. If the visual
  check shows genuine cramping, the tail will be trimmed before bundling.
