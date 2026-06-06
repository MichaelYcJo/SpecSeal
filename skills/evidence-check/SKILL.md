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
python3 "$(dirname "$(realpath "$0")")"/scripts/evidence_check.py [ROOT]
# from a session, simply:
python3 <this skill dir>/scripts/evidence_check.py --strict .
```

| Flag | Meaning |
|---|---|
| `--ledger GLOB` | ledgers to scan (default `docs/**/_evidence.md`) |
| `--default-repo PATH` | migration ledgers cite the ORIGINAL repo with unprefixed paths — resolve them against this checkout |
| `--map NAME=PATH` | resolve `NAME/...` prefixed coordinates against another checkout |
| `--strict` | drift also fails the run (exit 2) |

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| `BROKEN` (exit 2) | file gone or range beyond file length | fix the coordinate now — a broken ground is worse than none |
| `DRIFTED` (exit 1) | commits since the ledger's baseline SHA touched the range | re-open the coordinate, re-verify the claim, update the row's Checked column (and the baseline note if wholesale) |
| `EXTERNAL` | path resolves in no known checkout | pass `--map`/`--default-repo`, or accept as out of scope |
| `OK` | resolves, untouched since baseline | nothing |

Drift is detected from the baseline commit SHA in the ledger's header (the
template requires one) — `git diff baseline..HEAD` per cited file, overlapped
against the cited range. No baseline that exists in the checked repo → drift
checking is skipped and the run says so.

## Known limits

- Coordinates cited as bare filenames (`service.py:120`, no directory) cannot
  be resolved and are reported EXTERNAL — the tool never guesses by fuzzy
  matching, because a wrong resolution would validate the wrong evidence.
  Cite root-relative paths (the ledger template's notation).
- DRIFTED means "someone must re-verify", not "the claim is wrong". Line
  numbers shifting without semantic change still drift — that is intended:
  the coordinate itself is now stale either way.

## CI

Vendor `scripts/evidence_check.py` into the target repo (e.g. `tools/`) and
use `templates/evidence-check.yml` from this plugin as the workflow. Vendoring
over fetch-at-run keeps CI deterministic and offline-safe.
