# 1790076050-the-release-tail-is-three-acts-no-document-names — review round 2

| Field | Value |
|---|---|
| Target SHA | 11f3cde83dc2f617de293c92f959d1c1a95880b2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 500 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `cbd90ff8d0812437e696c85eced51553a5b17de4..1f1305b8bc9f0a68b4e9df7a8f34af8b33c83315`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1, 2 and 3. Finding 1 is the one in the tool: the guard finding 6 built is skipped whenever the script's argv is re-spelled, so an `issue edit` that also assigns, milestones or writes a body passes it. Findings 2 and 3 are one row each of `seal/follow-up.md`, a tracked document this branch writes to — an answerer that is a condition, and a figure about a corpus that is false on both its numbers. |
| Loses a record or crashes | no — nothing found leaves the root, nothing crashes, and no path this release exercises is affected. All three findings are a guard that can go quiet and two rows that misstate what they point at. |

- [x] Pass

## What this round was asked

The verifying round, at the diff of round 1's fixes rather than at the branch —
`317a96e0..d2b1e194`, two commits — with round 1's record as the agenda and its
six verdicts inherited.

The job was the answers, not new findings, with one surface exempt and read as
a finding surface instead: the six units round 1's `New units` row names, which
nobody has reviewed, `spend_label` among them.

Six claims of the fix pass were handed over as claims. That finding 2's figures
were re-derived rather than pasted and the paste-ready fix was itself wrong,
with the wrong figures traced to a measurement of a different population. That
finding 1 was fixed as a class by moving the report into one unit both branches
call, with one of four cases a positive control. That finding 6 took two
spellings because the first parsed zero calls. That finding 3 was probed rather
than cased, on stated grounds. That finding 5's grounds were fixed and its gap
deferred, and that the round's own two deferrals existed only in the record
until the fix pass wrote them into `seal/follow-up.md`. And that the anchor
count moved 14 → 13 → 14 for a reason.

One ⬜ was answered as a reading rather than a change and the reading was what
the round was asked to judge. #505 was named as a defect in the record
generator rather than in this work.

The broad gate was withheld, and the round was told the run ends at it if
nothing needing a fix is opened.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | finding 6's `ast` reader runs under `if edits:`, so a re-spelling of the argv takes the folded count to zero and the case asserts nothing about what the script edits | `tests/test_release_hygiene.py:1084` | **fixed** `718d0aca` | fixed at 718d0aca; Executed in a clone at `11f3cde8`: the argv rewritten with one comment between its words and `--add-assignee` added gives a folded count of 0 and the case exits 0, with the script assigning a person on every removal |
| 🟡 2 | the new §*House rules* row's answerer is *the repository owner, at the next change to `CONTRIBUTING.md` §*House rules**, which is the condition-wearing-a-person's-clothes the file's own header forbids | `seal/follow-up.md:80` | **fixed** `718d0aca` | fixed at 718d0aca; Executed: `tests/test_a_rider_reaches_its_file.py` green. Its guard tests one literal, `next time`, so the new spelling passes. §12 — the class is the shape, and the check enumerates a spelling |
| 🟡 3 | *five of nine `.github/scripts/` modules call it and four do not* is false on both numbers, and carries no moment | `seal/follow-up.md:81` | **fixed** `718d0aca` | fixed at 718d0aca; Executed at `11f3cde8`: 13 `.py` files, all 13 with a `__main__`, 6 call `console.to_utf8()` and 7 do not; before the fix, 5 and 8. Copied from round 1's deferral cell rather than re-derived |
| ⬜ | two `path#name` occurrences of the case finding 4 renamed are unmarked, so they name a unit the tree does not have | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:25` | answered | ⬜ — this run's own paperwork. Executed: `evidence-check` green (`14 ok`, `1453 ok`, `0 refused`) because the `path#name` form is read as a coordinate, not as a prose name, so the checker was never what would catch it |
| ⬜ | a 103-column line left by the re-join, in a paragraph that otherwise wraps at 68–78 | `docs/branch-and-release.md:100` | answered | ⬜ — readability only; the sentence is correct. Executed: `tests/test_docs_line_wrap.py` green, and this file is not in its covered list |
| ⬜ | the `console.to_utf8()` call this branch added is pinned by nothing and `overview.md` §*Not done* does not say so, while the same fix pass wrote that sentence for the `DOMAIN_RE` reading | `.github/scripts/tracker_labels.py:148` | answered | ⬜ — the decision not to add a case is right: the existing case spawns each gate by hand, so one script is the coordinate fix and the directory reds seven standing non-callers. Only the disclosure is missing |
| 🟢 | finding 2's figures, re-derived rather than pasted, and the command that re-derives them | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-3.md:56-96` | confirmed | Executed live 2026-09-22 against the directory file: 310 / 258 / 258 / 96 / 91 / 52, exact. The five non-`main` refs are the two version-shaped and three branch-shaped strings the record names, which is why dropping the tag claim was right |
| 🟢 | finding 1 fixed as a class — `spend_label` reached from all three sites, `drop_label` from nowhere else | `.github/scripts/close_issues_on_release.py:189` | confirmed | Executed over the whole tree: no caller outside the module, so `Contract changes: none` is right. Three of the four new cases are red against the pre-fix script |
| 🟢 | the positive control, shown red by deleting the line it pins | `tests/test_a_declared_label_reaches_the_tracker.py:336` | confirmed | Executed: green against the pre-fix script, red when the success print inside `spend_label` is deleted. §15's second route, which the section states as an alternative to the first |
| 🟢 | finding 6's second spelling reddens on the escape the round named | `tests/test_release_hygiene.py:1101-1131` | confirmed | Executed: `--add-assignee` beside `--remove-label` reds the case. Both argv shapes are collected, so the first spelling's zero-parse is fixed |
| 🟢 | the 14/13 anchor count, and the corpus figure that follows it | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/overview.md:5` | confirmed | Executed in a clone at `11f3cde8`: the fragment reports `14 ok`, the corpus `1453 ok · 0 drifted · 0 broken`, and a mechanical count gives 14 total, 14 unique |
| 🟢 | the ⬜ answered as a reading — `DOMAIN_RE` returns zero matches over the two lines, and the corpus does include the file | `.github/scripts/plugin_directory_check.py:81-85` | confirmed | Executed: three matches in the whole file, all the API host and all allowlisted; zero on lines 81, 82 and 85. The corpus is every tracked text file, so the pattern is what cannot see them, which is what `overview.md` §*Not done* says |
| ⬜ | round 1's `## Paste-ready fixes` cell reads *no paste-ready fix in the report* while the report carries six | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/rounds/round-1.md:63` | answered | ⬜ — a defect in the record generator, filed as #505 by the orchestrating session. Not this branch's to fix or to work around; carried here so the next reader of that cell knows why it is wrong |
| ❓ | the broad gate — the full suite, the repository-wide lint and the typecheck | `skills/verify/scripts/broad_gate.py` | out of verified scope | `agent-contract` §2 and `agents/warden.md` hand it to the sealer. The prompt withheld it, so nothing was declined. Answerer: the `sealer`, in its single run |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree, checked out at `11f3cde8`; every probe below ran there, and the clone and its virtual environment were removed afterwards | the worktree was written to once, for this report |
| the five new and renamed cases at `11f3cde8` | `5 passed` |
| probe: `"--add-assignee"` appended beside `"--remove-label"` in `drop_label`'s argv, then the restated hygiene case | `1 failed` — finding 6's second spelling reddens on the escape the round named |
| probe: the success print deleted from inside `spend_label`, then the three already-closed cases | `1 failed, 2 passed` — the positive control reddens on the line it pins |
| probe: the four new cases against the pre-fix script (`317a96e0`) | three red; `test_an_already_closed_issue_reports_a_removal_that_worked` green, which is the positive control |
| probe: the argv rewritten across lines with one comment between its words and `--add-assignee "someone"` added, then the restated hygiene case | folded count **0**, case **exit 0** — the script assigns a person on every removal and the case says it is clean. Finding 1 |
| `tests/test_a_rider_reaches_its_file.py tests/test_docs_line_wrap.py` — the two modules the `seal/follow-up.md` and `docs/` edits reach and the handoff's five do not | `54 passed` — the answerer guard and the wrap list are both blind to what this fix pass wrote |
| `evidence_check.py .` in the clone at `11f3cde8` | `total: 1453 ok · 0 drifted · 0 broken`; the fragment `14 ok`; `72 names read · 0 refused` |
| mechanical count of backticked coordinates in the ledger fragment | 14 total, 14 unique |
| `gh api repos/<owner>/<directory>/contents/.claude-plugin/marketplace.json`, the command `phases/phase-3.md` now carries | `310 / 258 / 258 / 96 / 91 / 52` and the five non-`main` refs — every figure in the corrected paragraph, exact |
| `DOMAIN_RE` driven over `plugin_directory_check.py` | three matches in the whole file, all the API host and all in `ALLOWED_DOMAINS`; zero on lines 81, 82 and 85 |
| count of `.py` files under `.github/scripts/`, of those carrying `__main__`, and of those calling `console.to_utf8()` | 13 / 13 / 6, against 5 before the fix. Finding 3 |
| `uvx ruff check` and `ruff format --check` over the five files this range changed | exit 0 and exit 0, read directly. `E402` is selected and does not fire: ruff allows an import after a `sys.path` edit, which is the shape both sibling scripts already use |
| `bin/deferral-check .` in the clone | exit 0, read directly |
| the eight modules, the five modules of the fix range, and the repository-wide lint the orchestrating session already ran | not re-run — `agent-contract` §3, the handoff carries them |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's single run, after the rounds settle, and this round did not take it |
| the tag-triggered job running on GitHub, and the live label write on the tracker | **not run here and not runnable here** — `agent-contract` §6 withholds both from every agent |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/close_issues_on_release.py:263-272` | round 1's 1 — fixed |
| round-1 | `docs/branch-and-release.md:91-95` | round 1's 2 — fixed |
| round-1 | `.github/scripts/tracker_labels.py:135` | round 1's 3 — fixed |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:226` | round 1's 4 — fixed |
| round-1 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:61-69` | round 1's 5 — fixed |
| round-1 | `tests/test_release_hygiene.py:1083-1095` | round 1's 6 — fixed |
| round-1 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/overview.md:5` | round 1's ⬜ — answered |
| round-1 | `.github/scripts/close_issues_on_release.py:257-258` | round 1's ⬜ — answered |
| round-1 | `.github/scripts/publish_release_note.py:179-191` | round 1's ⬜ — answered |
| round-1 | `.github/scripts/plugin_directory_check.py:81-85` | round 1's ⬜ — answered |
| round-1 | `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move* | round 1's ⬜ — answered |
| round-1 | `skills/verify/scripts/broad_gate.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `test_the_header_stops_the_answerer_that_is_really_a_condition` tests one literal, `next time`, while the rule it guards is a shape — *at the next change to X*, *when X is next opened*, *whoever gets to X first* all pass it. Widening it is mechanism with its own false-positive argument to make, which a fix pass may not add. Finding 2 fixes the one instance; the class is the check | a candidate row for `seal/follow-up.md`, to be written by the session that acts on finding 2 | the repository owner |
| Whether `console.to_utf8()` is owed by every `.github/scripts/` entry point as a class — **already deferred** by round 1's fix pass, to `seal/follow-up.md:81`. Not re-litigated; finding 3 corrects that row's figure and nothing else about it | `seal/follow-up.md` | whoever owns `hooks/console.py`'s convention |
| The arm neither `CONTRIBUTING.md` §*House rules* nor `CLAUDE.md` carries, for a claim falsified by code a branch added — **already deferred** by round 1, to `seal/follow-up.md:80`. Finding 2 is about that row's answerer cell, not about the question in it | `seal/follow-up.md` | the repository owner |
| `round-1.md`'s `## Paste-ready fixes` cell reading *no paste-ready fix in the report* against a report carrying six — **already filed as #505** by the orchestrating session, in the record generator rather than in this work | issue #505 | whoever owns `skills/code-review/scripts/round_record.py` |
