# Implementation Plan: a loaded file may not name a version that has not shipped

## Summary

`test_no_loaded_file_hardcodes_the_running_version` reads one number —
the version in `plugin.json` — so a document naming a version that has not
shipped yet is green every day until the day it ships, and red on the release's
own preparation commit, after the broad gate has already run. The repair is to
read the comparison rather than the equality: **a version at or above the
running one is a timer and is refused; a version below it is history and is
kept.** That one rule allows `docs/issues-and-milestones.md:156` — *the branch
`release/v0.3.0` shipped as 0.2.0* — which is the case that decides against
widening to every version this repository has ever shipped.

#98 rides the branch because it is the first one 0.9.0 opens. It is
comment-and-record only, and its cost is that the correction lands inside
`shipped_templates`' hashed region, so two ledger rows are re-read.

## Technical context

- `tests/test_release_hygiene.py:39-72` — the check. `version() in f.read()` is
  a substring test, which is why `v0.9.0` is caught today and why a regex
  replacing it must allow the `v` prefix without consuming it.
- `tests/test_release_hygiene.py:50-54` — `RECORDS_OF_A_MOMENT`, three exact
  paths. A fourth entry needs `CONTRIBUTING.md`'s argument, and
  `docs/experiments/` is a prefix rather than a path.
- **[executed]** the enumeration over the loaded set at `6f96eab`, by
  `git ls-files` over the same nine prefixes the test uses, minus the three
  exempt paths. Every version-shaped token in it:

  | Where | Token | Under the new rule |
  |---|---|---|
  | `docs/issues-and-milestones.md:28` | `0.9.0` | **refused** — the ticket |
  | `docs/issues-and-milestones.md:59,74` | `1.2.3` ×3 | allowed by the illustrative exemption |
  | `docs/issues-and-milestones.md:156` | `0.2.0` | allowed — below the running version |
  | `docs/experiments/2026-09-03-…{,ko}.md:4` | `2.1.259` | allowed — records of a moment |
  | `skills/implement/scripts/seal.py:611` | `4.4.17` | allowed — declared as bash's |

  Five distinct tokens, one of them the defect. The list is what makes the
  exemptions countable rather than speculative.
- `tests/test_the_pull_request_language_is_the_repositorys.py:757-761` — #98's
  comment, inside `shipped_templates`. `seal/ledger.md:550,562` are the two
  rows anchored on `…#shipped_templates@b1407676`.

**What breaks in 6 months.** The illustrative value is itself a version this
repository could one day ship. On the day `1.2.3` becomes the running version,
an exemption written as a bare string would hide exactly the defect it was
added beside. So the exemption asserts its own precondition: the illustrative
version must be one this repository has neither shipped nor is shipping, and
the check says so when that stops being true.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Sweep the one line and change no check (#179's first candidate) | The next author writes `0.10.0` into a document and the sweep is a fact about one afternoon. Nothing is in the way, which is how this line arrived | **No** — it is the floor, not the answer |
| Widen to every version the repository has shipped, read from tags or `CHANGELOG.md` (#179's second) | It refuses `docs/issues-and-milestones.md:156`, whose whole subject is that a branch named `v0.3.0` shipped as `0.2.0`. A rule that cannot state that fact is refusing history | **No**, and this case is why |
| Add `docs/issues-and-milestones.md` to `RECORDS_OF_A_MOMENT` (#179's third) | That file is not a record of a moment — it is the standing document for the tracker's conventions, and it is edited every release. The exemption would cover its future lines too | **No**, as the ticket already says |
| Refuse a version at or above the running one; allow what is below it | A version belonging to another product is above the running one and is not a timer. Three occurrences today, in two shapes: a dated experiment record naming the tool it measured on, and a comment naming bash. The first is a record of a moment by the same argument the list already carries; the second is one declared entry | **Yes** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The check refuses a version at or above the running one, over version-shaped tokens with an optional `v` prefix; `RECORDS_OF_A_MOMENT` gains `docs/experiments/` with its argument; the illustrative version and bash's are declared, each with its reason; the failure message names the file, the line, the token and what to write instead; the illustrative value asserts it is neither shipped nor shipping | The case seen **red** first against `docs/issues-and-milestones.md:28` on the unmodified tree, then green after phase 2; fixtures for a below-running version, an at-or-above one and the illustrative one; `uvx ruff` | |
| 2 | `docs/issues-and-milestones.md:28` names no real version, and the reason sits where the next author writing one will read it — the paragraph at `:59-64` already carries that reason and is what the new line points at | The phase-1 case, now green; the document read | |
| 3 | #98: the comment at `tests/…:757-761`, the section name at `seal/ledger/1788360817-…md:86` and round 5's summary say what each argument does; the `:884-886` docstring says *each* rather than *the only*; the two rows anchored on `shipped_templates` are re-verified at the hash the edit produces | The four quoting variants and the control-character fifth, re-executed on this machine and recorded; `./bin/evidence-check .` unscoped; `--reverify` naming the two rows | |
| 4 | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` fragments | The fragments; `.github/scripts/fold_ledger.py --check` | |

## Operational impact

None at runtime. One gate refuses more than it did, which `CONTRIBUTING.md`
requires the pull request body to state, and the widening is what makes a
document naming an unshipped version fail on the commit that writes it.
