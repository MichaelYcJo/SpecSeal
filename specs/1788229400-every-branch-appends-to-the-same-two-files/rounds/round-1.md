# 1788229400-every-branch-appends-to-the-same-two-files — review round 1

| Field | Value |
|---|---|
| Target SHA | `ce09b50e62510259d006ce6482267425459f99cb` |
| Diff base | `origin/main` (`708e348`) |
| PR | not yet |
| Broad gate | not yet |
| Fixes checked by | `round-2` |
| Needs a fix | yes — five 🔴 and five 🟡 |

- [ ] Pass

## How the ten findings relate

Three groups, one cause each time: something changed and the other half of it
did not follow.

```
① the design moved during implementation (last touch → first appearance, 9a7ce62)
     ├─ four documents still state the rejected reading        [1] 🔴
     └─ the case written to catch that left those four out     [2] 🔴

② the derived baseline has three places it cannot answer for
     ├─ renaming a ledger file turns its drift check off       [3] 🔴
     ├─ a row with no baseline prints like a checked one       [4] 🔴
     ├─ the coordinate substitution manufactures a stamp       [5] 🟡
     └─ the header cut is dead on this repository's own ledger [6] 🟡

③ the fragment convention reached half the documents
     ├─ the two a session actually reads still say Unreleased  [7] 🔴
     ├─ the path that bases on main gets no instruction        [8] 🟡
     ├─ three new changelog cases pass against a stub          [9] 🟡
     └─ a duplicated paragraph and an empty table row         [10] 🟡
```

Every finding in group ② reports LESS than the scheme it replaces. Issue #28
is that shape, so none of them was graded down for being quiet.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | Four documents still say the baseline comes from `git blame`, which is the last-touch reading this work item measured and rejected. Two of them ship to plugin users through `hygiene.yml`'s `ships` glob | `README.md:150` · `README.ko.md:143-144` · `templates/sdd-plan.md:50-51` · `skills/implement/SKILL.md:348` | **fixed** `aacae56` | Verified by the orchestrator, executed: `grep -c 'git blame'` returns 1 · 1 · 1 · 2 and `first appear` returns 0 in all four. The four were written at `1dc2531` and `22b3690`; `9a7ce62` changed the design and brought only `CLAUDE.md`, `templates/map.md`, `skills/evidence-check/SKILL.md` and `.specseal/map.md` along |
| 🔴 2 | The case written to catch exactly that omitted the four files that have it. Its own docstring predicts the failure | `tests/test_a_row_measures_from_its_own_history.py:487-503` | **fixed** `aacae56` | Verified by the orchestrator, read: the loop holds three tuples — `CLAUDE.md`, `templates/map.md`, `skills/evidence-check/SKILL.md`. `README.ko.md` is Korean and will not match `first appear`, so it needs its own assertion on 처음 나타난 / 마지막으로 건드린 |
| 🔴 3 | Renaming a ledger file turns that file's drift check off entirely. `first_appearance` hands `git log -L` the working-tree path together with a pre-rename anchor commit, git answers `fatal: There is no path …` rc 128, and the row falls through to [4] and prints `ok` | `skills/evidence-check/scripts/evidence_check.py:204-216` | **fixed** `b1291b1` | Reviewer-executed against a scratch repository: before the rename `0 ok · 1 drifted`, exit 1; after `1 ok · 0 drifted`, exit 0. The orchestrator did not re-run it. The docstring at `:186-188` claims the opposite — git does follow the rename, this code does not. `tests/…:328` passes `HEAD` rather than the anchor the code passes, so the case is green |
| 🔴 4 | A row with no baseline at all is appended as `OK`, indistinguishable from a row that was compared and found untouched. The summary line then says `each row measures from its own history` for a row that measured from nothing | `skills/evidence-check/scripts/evidence_check.py:394-403` | **fixed** `b1291b1` | Verified by the orchestrator, read: `if base:` guards the comparison and `findings.append(("OK", coord, ""))` runs unconditionally after it. Reviewer-executed: a committed row and an uncommitted row citing the same range print `1 ok · 1 drifted`. `spec.md`'s acceptance condition 3 holds only where a header baseline exists, and a fragment has none — while a fragment spends most of its working life uncommitted |
| 🟡 5 | Two defects on one line. The coordinate substitution collapses a coordinate to one space, joining a date to a hex word that was never beside it, and `STAMP_RE` reads the pair as a stamp. And the first resolvable stamp in the physical row wins, while `Verified behavior` — free prose, where this repository's fragments do name commits — sits BEFORE `Checked` | `skills/evidence-check/scripts/evidence_check.py:271-274` · `templates/map.md:76` | **fixed** `b1291b1` (code) · `aacae56` (docs) | Reviewer-executed, both halves. The claim in `templates/map.md:41-44` that a row's baseline needs a date and a SHA together, so prose in a row is inert, is too strong: it disarms a bare hex word, not prose that writes a date and a SHA in sequence. No row in either current ledger carries two distinct stamps today |
| 🟡 6 | The header cut does not fire on this repository's own ledger or on the template. `header_of` applies the 2000-character cap first, and `.specseal/map.md`'s first coordinate-citing row sits at char 3732 | `skills/evidence-check/scripts/evidence_check.py:94-100` | **fixed** `b1291b1` | Reviewer-measured: `.specseal/map.md` header 2000 (capped, not cut), `templates/map.md` 2000 (capped), the fragment 1528 (cut). This change grew the ledger header by roughly 800 characters and it now touches the cap; the `Baseline` row is at char 753, so another 1250 characters above it push it out of the window and the header fallback disappears while printing the same line as the designed state |
| 🔴 7 | The two documents a session actually reads still file the entry under `## Unreleased`, and a case pins that sentence in place. `CHANGELOG.md` has no such heading, so a `smith` following its own contract either creates one — reddening two cases — or appends under `## 0.1.0`, which is the collision this work item exists to remove | `agents/smith.md:65` · `skills/implement/SKILL.md:306` · `tests/test_release_hygiene.py:172` | **fixed** `aacae56` | Verified by the orchestrator, executed: `grep -rn '## Unreleased'` returns all three and returns nothing from `CHANGELOG.md`. `spec.md:119`'s acceptance condition 9 names `test_the_changelog_is_gathered_at_release.py` as its verifier, and that file checks only `CONTRIBUTING.md`, `docs/branch-and-release.md` and `CLAUDE.md` — so the condition was asserted, not verified, and is not true. `test_release_hygiene.py` now pulls both ways: `:172` requires the heading, `test_no_section_accumulates_entries_in_the_shared_file` forbids it |
| 🟡 8 | A feature branch basing on `main` meets the new `--check` gate with no instruction anywhere. The row it reads still says the heading gets dated, which is a rename that no longer exists, and `CONTRIBUTING.md:61` makes running the gather read as a rule violation | `.github/workflows/hygiene.yml:61-67` · `skills/implement/SKILL.md:306-311` · `CONTRIBUTING.md:57-64` | **fixed** `aacae56` | Reviewer, read. `skills/implement/SKILL.md:308-311` names basing on `main` a legitimate choice when a gate misfires, and `46b66d9` took that path |
| 🟡 9 | Three of the eleven new changelog cases pass against a script that only exits 0. `:119` checks the return code alone; `:125` carries the design's central decision — a marker rather than text matching — and checks neither the gather's exit code nor that the marker landed; `:162` is a negative assertion that holds when the gather fails entirely | `tests/test_the_changelog_is_gathered_at_release.py:119` · `:125` · `:162` | **fixed** `aacae56` | Reviewer-executed with a `sys.exit(0)` stub. The same lesson is already written in `tests/test_release_hygiene.py:184-188` |
| 🟡 10 | The fragment says the same thing twice and `follow-up.md` kept an empty table row where an entry was removed | `.specseal/map/1788229400-….md:16-25` · `.specseal/follow-up.md:40` | **fixed** `aacae56` | Reviewer, read. The parser at `tests/test_a_rider_reaches_its_file.py:35-48` skips empty rows, so nothing is red |

## Executed probes

| What was run | Result |
|---|---|
| `bin/evidence-check .` (reviewer) | `45 ok · 0 drifted · 0 broken`, exit 0, 0.47 s — matches the implementer |
| `uvx ruff check . && uvx ruff format --check .` (reviewer) | passed, 64 files already formatted |
| `gather_changelog.py --check` (reviewer) | exit 1, naming this work item's own fragment — the intended direction |
| `gather_changelog.py --version 0.2.0 --dry-run` (reviewer) | section generated with its marker, exit 0 |
| rename probe (reviewer) | `1 drifted`/exit 1 before, `1 ok`/exit 0 after — 🔴 3 |
| uncommitted-row probe (reviewer) | two rows citing the same range print `1 ok · 1 drifted` — 🔴 4 |
| `STAMP_RE` probe (reviewer) | substitution manufactures `deadbeef1`; a preceding cell's `cdb2434` beats the author's `9a7ce62` — 🟡 5 |
| `header_of` measurement (reviewer) | map.md 2000 capped · template 2000 capped · fragment 1528 cut — 🟡 6 |
| `grep -c 'git blame'` / `first appear` over the four documents (orchestrator) | 1 · 1 · 1 · 2 and 0 · 0 · 0 · 0 — 🔴 1 confirmed independently |
| the case's file list at `:487-503` (orchestrator, read) | three tuples, the four files absent — 🔴 2 |
| `grep -rn '## Unreleased'` over the three carriers and `CHANGELOG.md` (orchestrator) | present in all three, absent from `CHANGELOG.md` — 🔴 7 confirmed independently |
| `evidence_check.py:392-403` (orchestrator, read) | `OK` appended unconditionally after the `if base:` block — 🔴 4 confirmed independently |

The full suite, `ruff check .` and `ruff format --check .` across the tree did
not run this round. The broad gate is the orchestrator's, once, after the
rounds settle.

## Not reproduced

A sub-agent reported that reordering rows within one ledger resets the derived
baseline. The reviewer built the fixture and got the same baseline and
`2 drifted` before and after the reordering. Recorded rather than raised.

## Decided by the repository owner during this round

| Question | Answer |
|---|---|
| How the new no-baseline verdict enters the exit code | fails under `--strict` only. It prints a line and passes otherwise, which matches how `drifted` already behaves and keeps a session holding an uncommitted fragment out of a red light it would learn to ignore |
| `questions.md` Q2 — a SHA in a fragment's prose header read as the file's baseline | the reviewer's third option: read it, and print one line saying where it came from. Its failure direction is noisy, and it does not break the ledger shape `tests/test_evidence_check_hardening.py::test_custom_ledger_glob` has |

## Left for the repository owner

- Whether `hygiene.yml`'s new step fires on a real release pull request. Read,
  not run; the branch condition matches the version-bump step above it.
- `hygiene.yml`'s `types:` has no `edited`, so changing a pull request's base
  to `main` after the fact does not re-run the check, and a green from when the
  base was a release branch stays on that SHA. The reviewer could not
  reproduce the event.
- What `git log -L` costs on a ledger an order of magnitude larger. Measured at
  36 rows, one clone, macOS: 455 ms for 36 walks against 17 ms for one blame.
