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
| `--ledger GLOB` | ledgers to scan (default `.specseal/map.md`) |
| `--default-repo PATH` | migration ledgers cite the ORIGINAL repo with unprefixed paths — resolve them against this checkout |
| `--map NAME=PATH` | resolve `NAME/...` prefixed coordinates against another checkout |
| `--strict` | drift exits 2, the broken-coordinate code, instead of 1 — it fails the run either way |

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| `BROKEN` (exit 2) | file gone or range beyond file length | fix the coordinate now — a broken ground is worse than none |
| `DRIFTED` (exit 1; 2 under `--strict`) | commits since the row's baseline SHA touched the range | re-open the coordinate, re-verify the claim, and write the SHA you verified at into the row's Checked column |
| `EXTERNAL` | path resolves in no known checkout | pass `--map`/`--default-repo`, or accept as out of scope |
| `OK` | resolves, untouched since its baseline | nothing |

Drift is `git diff baseline..HEAD` per cited file, overlapped against the
cited range. **Each row carries its own baseline**: a commit SHA in its
Checked column, falling back to the header's when the row has none. No
baseline that exists in the checked repo → drift checking is skipped and the
run says so.

### Re-verify a row, not the ledger

```
| CLAUSE | `src/service.py:120-134` | ... | 2026-08-24 `a1b2c3d` | ... |
```

The SHA is the commit the row was read at, so re-verification drains row by
row. A single ledger-wide baseline makes drift all-or-nothing — one wide
refactor drifts every row at once, and the cheapest way out of that is
bumping the header, which re-dates every claim without re-reading any of
them. Bump the header only when the ledger genuinely starts over.

A row SHA older than the header's is not an exemption: it says that row has
not been read since, and it drifts accordingly.

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
