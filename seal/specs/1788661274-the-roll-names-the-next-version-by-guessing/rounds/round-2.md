# 1788661274-the-roll-names-the-next-version-by-guessing — review round 2

| Field | Value |
|---|---|
| Target SHA | 1a91edc |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 178 |
| Broad gate | e0bb0b1, against cc0a2c6 — 2355 passed, 2 skipped, 0 failed. The FIRST run, at `1a91edc`, was red: `test_no_loaded_file_hardcodes_the_running_version` found 0.8.1 written into `docs/issues-and-milestones.md` by this branch, and the same paragraph carried two 0.8.2s that would have gone red at this release's own preparation commit. All three are now an illustrative 1.2.3 (`e0bb0b1`); the pre-existing 0.9.0 one line 28 carries is #179. `uvx ruff check .` and `format --check .` clean |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round, against `1a91edc`, targeting the diff of round 1's
fixes — `253ac8c..6a56361`, two commits. Three probes were handed over as
re-checks: the three boundary titles, the two modules at 58 passed, and the
unscoped ledger read.

Six claims of the fix pass were named as claims under §5, each to be judged
rather than repeated: whether the three-segment decomposition is exhaustive
(with a title shorter than the prefix, a non-string title and a `None` from
`gh` put to it explicitly); whether `close_issue`'s new `shipped` parameter is
right or a coupling that reads as noise; whether `.strip()` should have been
kept and pinned or removed — a question the fix pass explicitly asked this
round to settle; two of the six recorded mutations to re-run; whether fixing a
pre-existing `time.sleep` leak inside a fix pass was right; and the two
hand-re-stamped anchors of the shared ledger's F6.

The round was also told that the orchestrator's own handoff to the fix pass had
carried a wrong reproduction command, that the fix pass reported it under §5
rather than working around it, and that the same standard applied to anything
it found wrong in its own prompt.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's 🟡 1 — `rolled_from` matched the marker anywhere | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | executed: the prose title → `None`, due. Mutation *startswith guard removed* → KILLED (round 1 had it SURVIVED); `TITLE_PREFIX = TITLE_MARKER` → KILLED, 8 failed |
| 2 | Round 1's 🟡 2 — `close_issue`'s comment restated the removed convention | `.github/scripts/roll_flow_measurement_issue.py#close_issue` | answered | executed: the comment names the shipped version and `log_title(shipped)`. Mutation restoring the old wording → KILLED. No two-argument caller remains |
| 3 | Round 1's ⬜ 3 — `.strip()` unpinned | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | executed: the mutation is now KILLED. The direction question is row 14 |
| 4 | Round 1's ⬜ 4 — the unreachable guard | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | executed: `partition` is gone; deleting the `startswith` guard now fails a case. The guard is real |
| 5 | Round 1's ⬜ 5 — `partition` against `rpartition` | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | read: `partition` has no occurrence left. The marker-twice title is covered by an assertion that the answer is not a shippable version — weak but deliberate and documented in the case |
| 6 | Round 1's ⬜ 6 — the `nothing due:` line named no title | `.github/scripts/roll_flow_measurement_issue.py#main` | answered | executed: the mutation removing the quoted title → KILLED |
| 7 | Round 1's ⬜ 7 — the tracker document's looser rule | `docs/issues-and-milestones.md` | answered | executed: the mutation restoring the loose wording → KILLED. The case reads the prefix out of the module rather than a literal |
| 8 | Round 1's ⬜ 8 — the `time.sleep` leak | `tests/test_a_release_rolls_the_flow_measurement_issue.py` | answered | executed, seen red both ways. Fixing it inside the fix pass was right — the pass had already rewritten this function's signature |
| 9 | Round 1's ⬜ 9 — `spec.md` quoted half 2 with a clause removed | `seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/spec.md` | answered | read: the bullet now quotes the clause whole, states the build went against it deliberately, and gives the issue's own delegation as grounds |
| 10 | Round 1's ⬜ 10 — equality and a version moving backwards | `.github/scripts/roll_flow_measurement_issue.py#roll_is_due` | answered | untouched by this diff. Round 1's answer rests on ledger row G1, re-read: ordering would leave an old title never due once its version ships, which is the stall |
| 11 | Round 1's ⬜ 11 — `next_version` has no caller | `.github/scripts/roll_flow_measurement_issue.py` | answered | carried from round 1's *Passed on their own grounds*; untouched by this diff |
| 12 | Round 1's ⬜ 12 — the re-stamped ledger rows | `seal/ledger.md` | answered | the fix pass re-stamped F6 again, both anchors. Executed: the unscoped read is clean but for the pre-existing drift; read: the claim did not move, only the anchors |
| 13 | Round 1's ⬜ 13 — the `spec.md` acceptance divergence | `seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/overview.md` | answered | carried. Accepted in round 1; nothing here changes what it rests on |
| 14 | The `.strip()` direction the fix pass asked this round to settle | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered — keep it | neither direction can stall; the round-trip weakening is unreachable because a whitespaced version fails the changelog/version equality check before a release. Executed on fourteen boundary titles |
| 15 | The three open questions on the decomposition | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | executed: short titles → due; a non-string or `None` title raises before anything is closed or opened. Loud, and on the required side |
| 16 | The four new units, judged as code rather than as fixes | `.github/scripts/roll_flow_measurement_issue.py#TITLE_PREFIX` | answered | `TITLE_MARKER` keeps an independent reader in the test tree, so `TITLE_PREFIX` is not a constant existing only to build another. The new cases invoke `main` once each and the document check survives whitespace collapse exactly |
| ⬜ 17 | An assertion in a new case that cannot fail while the one above it passes | `tests/test_a_release_rolls_the_flow_measurement_issue.py` | answered | Recorded and not fixed. The run ends on this record, and a redundant assertion changes no verdict, no output and no rendered page — it is `fixed in passing or not at all`, and this round chose not at all rather than reopening a closed run for it. The row above says exactly which assertion and why, so whoever next edits that case does not re-derive it |
| ⬜ 18 | A source line the doc edit left unwrapped | `docs/issues-and-milestones.md` | answered | The same. A 30-character line in a file wrapped at 71–77 renders identically; what it costs is a larger diff at the paragraph's next re-wrap, which is whoever writes that re-wrap |
| ⬜ 19 | *exactly as wide as the writer, no wider* is stronger than the code | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | The shipped docstring states the rule correctly — *a version may be read out of only the third segment, and only when the first two are exactly what `log_title` wrote*. The overstatement was in the fix pass's hand-back prose and in round 1's fix-table cell, not in anything that ships, and this record is where the two counterexamples now live so the next reader meets them here rather than finding them loose |
| ⬜ 20 | The close comment names a successor `open_issue` may fail to create | `.github/scripts/roll_flow_measurement_issue.py#close_issue` | answered | read: not a regression, and `main`'s recovery handler names the identical title, so the two agree |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` at `1a91edc`, `uv venv` + pytest 9.1.1 | clone made, the worktree never written |
| the roll's module and the flow-log module, exit read directly | exit 0, 58 passed (round 1 had 55) |
| `rolled_from` on fourteen boundary titles | the prose title → `None`, due · trailing space → `'0.8.2'`, not due · the roll's own title → `'0.8.2'`, not due · short, empty, uppercase, hyphen-for-em-dash, leading space, old-convention, marker-with-nothing-after → `None`, all due · marker twice → the whole tail, due · `\xa0` before the version → `'0.8.2'` · newline suffix → `'0.8.2'` |
| round-trip `rolled_from(log_title(v)) == v` for six values | holds for ordinary versions; fails for whitespaced and empty ones — unreachable, see row 14 |
| `rolled_from` on a non-string and on `None` | `AttributeError` each, raised before `close_issue` |
| the posted `--comment`, via a monkeypatched `run` | names the shipped version and `log_title(shipped)` |
| seven mutations of the script and the tracker document | all KILLED: startswith guard · `TITLE_PREFIX = TITLE_MARKER` (8 failed) · `.strip()` · the close comment · the nothing-due line's title · the not-due guard (3 failed) · the tracker document's rule |
| the `time.sleep` leak, both ways | at the target the probe passes; with the two lines reverted it fails naming the leaked lambda |
| `evidence_check.py .` unscoped, exit read directly | exit 1, 665 ok · 1 drifted · 0 broken; the drift is `templates/config.md`, pre-existing |
| probe files and the clone deleted | all removed; the worktree is clean and was never written |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | round 1's 🟡 1 — fixed |
| round-1 | `.github/scripts/roll_flow_measurement_issue.py#close_issue` | round 1's 🟡 2 — fixed |
| round-1 | `.github/scripts/roll_flow_measurement_issue.py#main` | round 1's ⬜ 6 — fixed |
| round-1 | `docs/issues-and-milestones.md#"### `flow-measurement` is a label that is not an index"` | round 1's ⬜ 7 — fixed |
| round-1 | `tests/test_a_release_rolls_the_flow_measurement_issue.py` | round 1's ⬜ 8 — fixed |
| round-1 | `seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/spec.md` | round 1's ⬜ 9 — answered |
| round-1 | `.github/scripts/roll_flow_measurement_issue.py#roll_is_due` | round 1's ⬜ 10 — answered |
| round-1 | `.github/scripts/roll_flow_measurement_issue.py` | round 1's ⬜ 11 — answered |
| round-1 | `seal/ledger.md` | round 1's ⬜ 12 — answered |
| round-1 | `seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/overview.md` | round 1's ⬜ 13 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, the repository-wide lint, the typecheck | contract §2 keeps them out of a round | the orchestrator, at the broad gate immediately after this round |
| The roll against real GitHub — every case fakes `subprocess.run` | already deferred by round 1 to `overview.md` §Not verified | the 0.8.2 release, which is the first live run |
| ⬜ 17 and ⬜ 18 | recorded here and not fixed: the run ends on this record, and neither changes a verdict, an output or a rendered page | whoever next edits either file |
