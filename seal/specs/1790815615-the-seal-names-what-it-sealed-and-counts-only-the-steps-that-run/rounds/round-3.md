# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — review round 3

| Field | Value |
|---|---|
| Target SHA | 111ef570a47de827c08b75d3ffc4b409ee1989a5 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 699 |
| Broad gate | 66ab0102 against a340221b |
| Fixes checked by | no fixes to check |
| Fix range | `111ef570a47de827c08b75d3ffc4b409ee1989a5..2c86816a5da596205f757a396f0d1ca0131939ec`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a dotted name before an issue is read as the home), 🟡 2 (an underscore at a path segment's edge is taken off) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is the verifying round after the run's one reopening, so it ends the run. It targets `111ef570` and verifies round 2's fix range `0cbadb8e..4744a1c0`, five commits. It was asked whether round 2's five verdicts are closed with their class, by re-running round 2's home probes over typed cells and every deferred row in the tree. It was also asked to judge the smith's departure from the paste-ready fix, the dropped lookbehind.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a dotted name that is not a file (`chain_check.verdict_of`, `re.sub`, `Node.js`) placed before an issue is printed as the home and hides the issue; the bare-name arm was widened from `.md` to any extension | `skills/verify/scripts/broad_gate.py:2404` | deferred #708 | #708 — The run ended capped at round 3; #708 carries the five cells and the report's pattern; executed at the target over five cells, all wrong, all right at `0cbadb8e`; round 2's 🟡 1 class, opened by `fa03671d`; the fix is executed green over 24 cases and 73 tree rows |
| 🟡 2 | an underscore at the edge of a path segment is still taken off, inside a code span too, so a package's private directory or a dunder module name prints without its underscores | `skills/verify/scripts/broad_gate.py:2431` | deferred #708 | #708 — The same unit and the same issue; no deferred row in the tree today is misread; executed at the target over four cells, all wrong; round 2's 🟡 2 class, closed only for the interior instance at `90e5e27`; ledger N9 says *its underscores kept* |
| 🟢 | round 2's 🟡 1 finding is closed for its instance — slash-joined words stay words | `skills/verify/scripts/broad_gate.py:2404` | confirmed | executed: four round-2 cells right; reverting `HOME_TOKEN` fails five new cases; the class goes on as 🟡 1 |
| 🟢 | round 2's 🟡 2 finding is closed for its instance — an interior underscore is kept | `skills/verify/scripts/broad_gate.py:2431` | confirmed | executed: reverting the marks line fails the two new cases; the class goes on as 🟡 2 |
| 🟢 | round 2's ⬜ 3 is closed — the overview says the names ride only the head line the preflight replaces | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/overview.md:39` | confirmed | read at `seal_stamp.py:472` and `broad_gate.py:2915`; `survivor-check` over the range exits 0 with the work item's `survivors.md` |
| 🟢 | round 2's ⬜ 4 is closed — the four rows re-hashed at the merge carry a merge note | `seal/releases/0.15.4.md` | confirmed | read: 0.15.1 N3, 0.15.4 A5 and C4, 0.15.7 N9, earlier notes kept; `evidence-check .` 0 drifted |
| 🟢 | round 2's ⬜ 5 is closed — both places name an installed copy older than #666 | `skills/verify/scripts/broad_gate.py:3015` | confirmed | read, and the installed 0.16.0 copy read: it redirects and sets no invoked-path variable |
| 🟢 | the smith's departure from the paste-ready lookbehind is right | `skills/verify/scripts/broad_gate.py:2404` | confirmed | executed: with the lookbehind, `deferred see ./seal/follow-up.md` fails, 1 of 24; the lookbehind limits where a match starts, never where it ends |

## Paste-ready fixes

```python
# What a home looks like inside a deferral's prose: an issue, or a file —
# a path whose last part carries an extension, or a bare `.md` name. A bare
# dotted name is not a file, so `chain_check.verdict_of`, `re.sub` and
# `Node.js` stay words and an issue after them is still found (round 3 of
# #666), as `CI/CD`, `and/or` and `stdout/stderr` do (round 2).
HOME_TOKEN = re.compile(
    r"#\d+|[\w-][\w.-]*(?:/[\w.-]+)+\.[A-Za-z]\w+\b|[\w-][\w.-]*\.md\b"
)
```
```python
        # A dotted name is not a file, and an issue after it is the home
        # (round 3's 🟡 1).
        ("deferred — chain_check.verdict_of's reading is #703's", "#703"),
        ("deferred — the Node.js port is #702's", "#702"),
        ("deferred — `round_record.py`'s owner, see #709", "#709"),
```
```python
    marks = "".join(
        part if i % 2 else re.sub(r"\*+|(?<![\w/.])_+|_+(?![\w/.])", "", part)
        for i, part in enumerate(cell.split("`"))
    )
```
```python
        # An underscore at a segment's edge is the file's, not a mark, and
        # nothing inside a code span is a mark (round 3's 🟡 2).
        ("deferred to src/pkg/_internal/io.py", "src/pkg/_internal/io.py"),
        ("deferred to `src/pkg/_internal/io.py`", "src/pkg/_internal/io.py"),
        ("deferred to pkg/__init__.py", "pkg/__init__.py"),
```
```text
The marks are taken off by a narrower pattern than `chain_check.EMPHASIS`,
which removes every `_`: nothing inside a code span is a mark, and outside
one, asterisks and an underscore that no letter, `/` or `.` touches, so
`tests/test_x.py` and `src/pkg/_internal/io.py` keep their names (round 2's
🟡 2 and round 3's 🟡 2 of #666).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q` in the clone at the target | exit 0, 225 passed |
| a one-off probe: `deferred_home` over 31 typed cells and every deferred row of every `round-N.md` in the tree | round 2's four cells and the `./`, `../`, `to #664`, `→ #664`, `→ later` cells right; 73 tree rows right, all ASCII; the dotted-name and edge-underscore cells wrong, as reported |
| the home cases (`-k home`) with `HOME_TOKEN` reverted to `0cbadb8e`'s | exit 1, 5 failed: the four slash cells and the `./` cell |
| the home cases with the marks line reverted to `chain.EMPHASIS` | exit 1, 2 failed: the two underscore cells |
| the home cases with round 2's paste-ready lookbehind in place of the shipped regex | exit 1, 1 failed: `deferred see ./seal/follow-up.md` |
| the home cases and the typed probe with both fixes above applied | exit 0, 24 passed; 29 of 31 typed cells as expected (the other two read words, as described); 73 tree rows unchanged; file restored, `git status` clean |
| `bin/evidence-check .`, unscoped, at the target | exit 0; `total: 3237 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow` |
| `bin/survivor-check --range 0cbadb8e..4744a1c0`, then again with `--exempt` set to the work item's `survivors.md` | exit 1 with one survivor (the P3 note), then exit 0, excused by the row |
| the full suite, repository lint and typecheck (the broad gate) | not yet: this round did not run them; they are the sealer's once the rounds settle |

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
| round-2 | `skills/verify/scripts/broad_gate.py:2400` | round 2's 🟡 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2423` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/overview.md:39` | round 2's ⬜ 3 — answered |
| round-2 | `seal/releases/0.15.4.md` | round 2's ⬜ 4 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:3006` | round 2's ⬜ 5 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:266` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2405` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2829` | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.15.7.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2793` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
