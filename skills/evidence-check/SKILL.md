---
name: evidence-check
description: |
  Verify that the evidence ledger's spec-to-code coordinates still resolve —
  broken links fail, ranges touched since the baseline demand re-verification.
  Use when: checking ledger health, before merging spec-driven work, wiring
  the check into CI, or after large refactors.
  NOT for: judging whether the code is CORRECT — this checks that the
  evidence still points somewhere, not that the claim is still true.
---

# evidence-check — does the ledger still point at what it claims?

Specs rot silently: code moves, the ledger's `file:line` coordinates keep
claiming grounds that are no longer there, and the next reader trusts them.
This skill makes that rot mechanical to catch — the same way a broken test
catches a regression.

## Run

```bash
evidence-check [ROOT]          # on PATH while the plugin is enabled
# from a session, simply:
evidence-check --strict .
```

| Flag | Meaning |
|---|---|
| `--ledger GLOB` | ledgers to scan (default `.specseal/map.md` and `.specseal/map/*.md`) |
| `--default-repo PATH` | migration ledgers cite the ORIGINAL repo with unprefixed paths — resolve them against this checkout |
| `--map NAME=PATH` | resolve `NAME/...` prefixed coordinates against another checkout |
| `--strict` | drift exits 2, the broken-coordinate code, instead of 1 — it fails the run either way |

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| `BROKEN` (exit 2) | file gone or range beyond file length | fix the coordinate now — a broken ground is worse than none |
| `DRIFTED` (exit 1; 2 under `--strict`) | commits since the row's baseline touched the range | re-open the coordinate, re-verify the claim, and put the date you verified it in the row's Checked column |
| `EXTERNAL` | path resolves in no known checkout | pass `--map`/`--default-repo`, or accept as out of scope |
| `OK` | resolves, untouched since its baseline | nothing |

Drift is `git diff baseline..HEAD` per cited file, overlapped against the
cited range. **Each row carries its own baseline**, and three things can supply
it, in this order:

1. a **stamp** written in the row — a date and a SHA together, `2026-08-24
   a1b2c3d` — for rows written under the older rule. A bare hex word is prose,
   not a stamp, and is not read as one;
2. **the commit the row first appeared in**, derived from its own line's
   history — the ordinary case;
3. the ledger header's baseline, where neither can answer.

Only when all three come up empty is drift checking skipped, and the run says
so on the ledger's own line.

### Re-verify a row, not the ledger

```
| CLAUSE | `src/service.py:120-134` | ... | 2026-08-24 | ... |
```

The Checked column holds the date somebody read the code and nothing else.
Re-verification drains row by row, because a row's baseline is its own last
change. A single ledger-wide baseline makes drift all-or-nothing — one wide
refactor drifts every row at once, and the cheapest way out of that is bumping
the header, which re-dates every claim without re-reading any of them. Bump the
header only when the ledger genuinely starts over.

**Why the row writes no SHA.** There is no commit a feature branch could write
that is both reachable after a squash and current with its coordinates: name
the base and the row reads DRIFTED at birth, name the branch and the squash
leaves it pointing at nothing. That happened — seven rows, repaired by hand,
one cell at a time. Blame is computed on the tree as it stands, so after the
squash it answers with the squash commit, which is what the repair wrote in.

**First appearance, not last touch.** Last touch is what a single `git blame`
answers for free, and it resets a row on any edit to its line, a typo
included. Measured on this plugin's own ledger: last touch is later than the
written stamp on all 36 rows, never equal and never earlier — a strictly
narrower diff window than the stamps it replaces, with nothing re-read to earn
it — and one release commit that rewrote stamps in bulk held the baseline for
16 of them. By first appearance it holds none. Deriving the baseline automates
a failure the written stamp already had and widens what triggers it; first
appearance narrows it back.

**What it costs**: one git call per row rather than one per file, measured at
about 13 ms a row against 17 ms for a whole-file blame. Rows with a stamp never
reach it.

**Moving a row between ledger files keeps its stamp, verbatim.** `git log -L`
does not follow a row out of a file that stays, so a moved row's derived
baseline is the move itself. Carrying the stamp is what makes a migration cost
nothing; stripping it collapses every window it touched at once. (Renaming a
whole ledger file is different — git detects that and follows it.)

### One fragment per work item

A work item's rows go in `.specseal/map/<work-item-id>.md`, which the default
globs already read. Two branches never queue at one file, because no two work
items share an id, and **a fragment needs no baseline header**: every row in it
measures from its own line. Fragments are never gathered back — a row is
checked against the code it cites, not concatenated.

## Known limits

- Coordinates cited as bare filenames (`service.py:120`, no directory) cannot
  be resolved and are reported EXTERNAL — the tool never guesses by fuzzy
  matching, because a wrong resolution would validate the wrong evidence.
  Cite root-relative paths (the ledger template's notation).
- DRIFTED means "someone must re-verify", not "the claim is wrong".
- Overlap is judged in BASELINE line numbering (the numbering citations were
  written in). A coordinate whose lines merely SHIFTED because of edits above
  it is not flagged — its content is intact, but its line numbers are stale;
  re-anchoring shifted-only coordinates is future work.

## CI

`/specseal:evidence-ci` does the wiring: it vendors `scripts/evidence_check.py`
to `tools/` and writes `.github/workflows/evidence-check.yml`, resolving the
plugin's own path so nobody has to know where it is installed. Re-running it
diffs the vendored copy against the current one.

Vendoring over fetch-at-run keeps CI deterministic and offline-safe, and puts
the checker in the diff where a reviewer can see it change.
