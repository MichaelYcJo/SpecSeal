# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — review round 2

| Field | Value |
|---|---|
| Target SHA | 39ef351cc9e778604f83d7d6c97e6a8101f81f74 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 699 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `0cbadb8e6c16e409a68ab14494b93dac6c187198..4744a1c045ba7e02c6190c56aee6a89cc915b0eb`, 5 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a slash-joined word read as a path home), 🟡 2 (a path home loses its underscores) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is the verifying round. It targets `39ef351c` and verifies round 1's fix range `613b9389..bf446934`, four commits, together with the merge `613b9389` itself, which nobody had reviewed. It was asked whether round 1's five `fixed` verdicts are closed with their class. It was also asked to review the units the fixes created as finding surfaces, and to check the merge against both parents: every note kept, each hash from the side that edited its unit, and #638's preflight intact.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `HOME_TOKEN`'s path arm reads words joined by a slash (`CI/CD`, `and/or`, `stdout/stderr`) as a path, and one placed before an issue hides the issue: `deferred — the stdout/stderr split is #700's` prints `stdout/stderr` | `skills/verify/scripts/broad_gate.py:2400` | **fixed** `fa03671d` | fixed at fa03671d; executed at the target over four cells; requiring an extension fixes all four, and the twelve parametrized cases and the sealer module stay green (216 passed) |
| 🟡 2 | a path home is read after `EMPHASIS`, which removes every `_`, so `tests/test_the_gate_names_every_step_ci_runs.py` prints as `tests/testthegatenameseverystepciruns.py` | `skills/verify/scripts/broad_gate.py:2423` | **fixed** `fa03671d` | fixed at fa03671d; executed at the target; this line predates the fix (depth 0), and the fix made a path a first-class home; the paste-ready marks keep the name, sealer module green with it |
| ⬜ 3 | `overview.md` §Not done says the names reach a failed preflight's per-check lines; `not_sealed` puts them on the head only, and the preflight replaces the head | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/overview.md:39` | answered | corrected at 23542d92; overview.md says the names ride only the head line, which the preflight replaces; `not_sealed` executed with names: only line 0 carries them; paperwork, a correction |
| ⬜ 4 | four release rows re-hashed at the merge over the two headings both sides edited carry no *at the merge* note, where #638's fragment rows over the same headings do | `seal/releases/0.15.4.md` | answered | corrected at 23542d92; the four rows re-hashed at the merge carry an at-the-merge note; rows 0.15.1 N3, 0.15.4 A5 and C4, 0.15.7 N9; hashes right (`evidence-check` at `613b9389`, 0 drifted); both sides' notes present; paperwork, a correction |
| ⬜ 5 | two comments give one reason for an absent invoked path, the direct run, and leave out an installed copy older than #666 | `skills/verify/scripts/broad_gate.py:3006` | **fixed** `fa03671d` | fixed at fa03671d; read; also the `gate_copy` docstring at `:450`; the rest of round 1's 🟡 4 class; behaviour right |
| 🟢 | round 1's 🟡 1 is closed — a list of counts or homes continues beneath its label | `skills/verify/scripts/broad_gate.py:266` | confirmed | executed: `1790645290` and `1790297085` show every home, every row 23 columns or fewer; `beside` draws any height |
| 🟢 | round 1's 🟡 2 is closed for the tree's four rows and the typed shapes | `skills/verify/scripts/broad_gate.py:2405` | confirmed | executed over every deferred row of every `round-N.md` and over `to #664`, `→ #664`, `→ later`: right home, ASCII; the two remaining misreads are 🟡 1 and 🟡 2 |
| 🟢 | round 1's 🟡 3 is closed — the base cannot be dropped silently | `skills/verify/scripts/broad_gate.py:2829` | confirmed | mutations executed: argument dropped raises `TypeError` and fails a case; `None` fails `test_a_release_pull_request_is_sealed_as_ci_would_judge_it` |
| 🟢 | round 1's 🟡 4 and ⬜ 5 are closed in the four places named | `docs/the-broad-gate.md:106` | confirmed | read in the diff; the documents case pins all four, green (executed) |
| 🟢 | the merge keeps every note of both sides, a right hash on every row, no row duplicated or lost | `seal/releases/0.15.7.md` | confirmed | three-way probe over nine files executed; `evidence-check .` at `613b9389` 0 drifted; `correction-check` exit 0 |
| 🟢 | #638's preflight survives the merge: head unchanged, `--record` refused first, no coverage line, early return | `skills/verify/scripts/broad_gate.py:2793` | confirmed | combined diff read; eleven `preflight` cases green (executed) |

## Paste-ready fixes

```python
# What a home looks like inside a deferral's prose: an issue, or a file — a
# path whose last part carries an extension, so `CI/CD`, `and/or` and
# `stdout/stderr` stay words and an issue after them is still found (round 2
# of #666).
HOME_TOKEN = re.compile(r"#\d+|(?<![\w/.-])[\w-][\w.-]*(?:/[\w.-]+)*\.[A-Za-z]\w+\b")
```
```python
        # Words joined by a slash are words, not a path (round 2 of #666).
        ("deferred — the stdout/stderr split is #700's", "#700"),
        ("deferred to whoever owns CI/CD next", "to whoever owns CI/CD next"),
        ("deferred — read/write order is in seal/follow-up.md", "seal/follow-up.md"),
```
```python
# The marks a home is read without: code spans, asterisks, and an underscore
# at a word's edge. Not `chain_check.EMPHASIS`, which removes every `_` and
# so prints `tests/test_x.py` as `tests/testx.py` (round 2 of #666).
HOME_MARKS = re.compile(r"`|\*+|(?<!\w)_+|_+(?!\w)")
```
```python
    s = chain.MARKER.sub("", HOME_MARKS.sub("", cell).strip())
    rest = s[len(chain.DEFERRED) :].strip(chain.SEPARATORS)
```
```python
        # A file name keeps its underscores (round 2 of #666).
        (
            "deferred `tests/test_the_gate_names_every_step_ci_runs.py`",
            "tests/test_the_gate_names_every_step_ci_runs.py",
        ),
        (
            "deferred to `skills/verify/scripts/broad_gate.py`'s owner",
            "skills/verify/scripts/broad_gate.py",
        ),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the sealer, CI-steps, range, stamp and broad-gate-rule modules, in the clone | exit 0, 351 passed |
| `bin/evidence-check .` unscoped, then `--strict .`, at the target | both exit 0; `total: 3237 ok · 0 drifted · 0 broken` |
| `bin/evidence-check .` unscoped at the merge `613b9389` | exit 0; `total: 3233 ok · 0 drifted · 0 broken` |
| `bin/correction-check --range origin/release/v0.17.0...HEAD`, `origin/release/v0.17.0` at `a340221b` | exit 0; one merge examined, no marker dropped |
| a one-off three-way probe over the nine release files both parents edited: rows, notes, hashes, one-sided cells | rows equal; every note present; one-sided hashes from the editing side; both-edited hashes are the merge's own |
| a one-off probe: `rounds_rows` for `1790645290` and `1790297085`, `deferred_home` over every deferred row of the tree and fifteen typed cells, `wrapped` over six lists, `not_sealed` with names | every home shown; tree rows right; slash, underscore and later-issue cells as reported; names on line 0 only |
| the gate's coverage call with the argument dropped, then the three gate modules (`-x`) | exit 1, `TypeError`, `test_the_stamp_says_how_many_steps_the_seal_did_not_answer` fails |
| the gate's coverage call given `None`, then the three gate modules | exit 1, 1 failed (`test_a_release_pull_request_is_sealed_as_ci_would_judge_it`), 303 passed |
| 🟡 1's and 🟡 2's fixes applied in the clone, the probe re-run, then the sealer module | probe: 17 of 18 cells right, `e.g.` the one left; sealer module exit 0, 216 passed; file restored with `git checkout` |
| the eleven `preflight` cases across the sealer and broad-gate-rule modules | 11 passed |
| the full suite, repository lint and typecheck (the broad gate) | not yet: not run by this round; it is the sealer's once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2555` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2366` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2713` | round 1's 🟡 3 — fixed |
| round-1 | `docs/the-broad-gate.md:106` | round 1's 🟡 4 — fixed |
| round-1 | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/changelog.md:11` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2616` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:3047` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_gate_names_every_step_ci_runs.py:1100` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2911` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.15.1.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/sealer-stamp.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
