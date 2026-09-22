# 1790076050-the-release-tail-is-three-acts-no-document-names — review round 3

| Field | Value |
|---|---|
| Target SHA | a32d6d77bc837afc0c279e8ab70a0cfdf1517b85 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 500 |
| Broad gate | 59a72d91 against 6d410023 |
| Fixes checked by | no fixes to check |
| Fix range | `a32d6d77bc837afc0c279e8ab70a0cfdf1517b85..c95fe9066b7b3048324bee80601eb03f5900b99e`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1 and 2, and neither is in what round 2 asked to have repaired. Finding 1 is two tracked files saying the new reader closes an escape it leaves open, in a row that asks the owner to convert two more cases on that basis. Finding 2 is a checker gap the run met by accident and recorded with the wrong cause. The run's one reopening is spent, so both are deferred with the repository owner named and neither commissions a fourth round. |
| Loses a record or crashes | no — nothing found leaves the root, nothing crashes, and no path this release exercises is affected. Finding 1 is a claim about a check that is stronger than the check; finding 2 is a checker that reads less than a record says it reads. Both are silence where a warning was assumed, and neither writes or drops anything. |

- [x] Pass

## What this round was asked

The last record of the run. The reopening was spent at round 2, so nothing this
round opened could take a fourth round — anything needing a fix is deferred
with a named answerer or becomes an issue, and the round was told so before it
started.

Target: the diff of round 2's fixes, `cbd90ff8..1f1305b8`, two commits, with
rounds 1 and 2 inherited. Round 1's `New units` named six units nobody had
reviewed and they were the finding surface; `Contract changes` read none.

Five claims were handed over: that the class was wider than round 2's finding
and the five forbidden verbs were substring searches for the same reason; that
a sibling `seal/follow-up.md` row was changed beyond what the round asked;
that writing the deferral row tripped the guard it describes; that the renamed
case's nine occurrences were enumerated and the markers placed on the name's
own line; and that two survivors are the removed reader still standing in two
other modules, exempted with grounds.

One claim of the fix pass about the checker was handed over to be verified
rather than believed — that `evidence-check` would not have caught an invented
unit name in a `seal/follow-up.md` row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the case docstring and the new `seal/follow-up.md` row both say the `ast` reader closes *a value moved into a constant*, and it does not — the row asks the owner to convert two more cases on that premise | `tests/test_release_hygiene.py:1054-1060` | answered — corrected at `c95fe906` | Executed in a clone at `a32d6d77`: a `gh issue reopen` argv whose first word, or whose verb, is a module constant leaves the case at `1 passed`; the same argv spelled plainly, or with a comment between its words, reds it. `words` keeps only `ast.Constant` strings, so a name in the first three positions shifts the prefix. The cap is spent, so this is a deferral rather than a commissioned fix |
| 🟡 2 | `seal/follow-up.md` is outside the records corpus, so a bare invented name in it passes too — and the recorded reason, `path#name` read as a coordinate, is a second and separate gap that applies inside a live work item | `skills/evidence-check/scripts/evidence_check.py:1919` | deferred #508 | Executed, four injections in a clone at `a32d6d77`: bare and `path#name` in `seal/follow-up.md` both exit 0 with 0 refused; bare in this work item's `spec.md` exits 2 with 1 refused; `path#name` in the same file exits 0. The records arm reads `seal/specs/<id>/` for ids with a ledger fragment, and `RECORD_NAME_RE` requires the whole backticked span to be an identifier |
| ⬜ | `survivors.md`'s round 1 comment says *the four below* and this range inserted two rows before round 1's fourth | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/survivors.md:41` | answered | ⬜ — this run's own paperwork, prose accuracy only. Executed: `read_exemptions` parses row by row and skips blanks and comments, so no exemption row is lost and `survivor-check` is unaffected |
| ⬜ | `phase-4.md:43` and `:202` say the case allows *at most one* `issue edit` while it now requires exactly one | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:43` | answered | ⬜ — this run's own paperwork. Read: the change to exactly one is deliberate and reasoned at `tests/test_release_hygiene.py:1128`; the record is the coordinate a reader opens to check what the case does |
| ⬜ | the close assertion drops the `str(issue)` operand the folded form pinned, and nothing records the trade | `tests/test_release_hygiene.py:1116-1119` | answered | ⬜ — `len(closes) == 1` is stronger on the count, which the old form did not check at all, and the operand is the same thing the `edit` argv already leaves unread. Only the disclosure is missing |
| 🟢 | the new case reddens on both escapes the round named — `--add-assignee` on the `edit` argv, and a re-spelled `gh issue reopen` | `tests/test_release_hygiene.py:1116-1136` | confirmed | Executed in a clone at `a32d6d77`: `--add-assignee` gives `1 failed`; a `gh issue reopen` argv spread across lines with a comment between two of its words gives `1 failed`, where the folded reader counted zero. The plain spelling is the control and also reds |
| 🟢 | `edit` is exactly one rather than at most one, and the change is shown red | `tests/test_release_hygiene.py:1127-1134` | confirmed | Executed: with the one `issue edit` argv replaced by a `gh api` call the case gives `1 failed`. Under `<= 1` that state passed, which is what let the whole parse be skipped |
| 🟢 | the sibling answerer change is the same rule's other arm, not scope the pass took | `seal/follow-up.md:81` | confirmed | Read: the header states one sentence with two arms — names a person, and no condition attached. A role is the first arm. Executed: all 19 answerer cells now read *the repository owner* |
| 🟢 | the guard joins the whole row and searches it, so it cannot be discussed in the file it guards | `tests/test_a_rider_reaches_its_file.py:132-133` | confirmed | Read: the assertion is over `" ".join(row)` for every row of the section, with no cell distinction, so a row quoting the literal while describing it reds although its answerer is unconditional. The new row's description of the guard is accurate |
| 🟢 | the nine occurrences of the renamed case, and the marker on the name's own line | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/spec.md:201` | confirmed | Executed over the whole tree: nine occurrences in seven files; six marked, every marker on the name's own line, which is the line `evidence-check` exempts; the three unmarked are round records. The handoff's reason — that round 1's markers sat on the following line — is not supported: all three were already on the name's line at `cbd90ff8` and this range did not move them |
| 🟢 | the corrected `console.to_utf8()` census | `seal/follow-up.md:81` | confirmed | Executed independently at `a32d6d77`: 13 `.py` files under `.github/scripts/`, 13 carrying a `__main__`, 6 calling `to_utf8()` and 7 not. Exactly the row's figures, and the seven non-callers are the ones `overview.md` now names |
| 🟢 | the 103-column line is re-wrapped, paragraph and all | `docs/branch-and-release.md:100-104` | confirmed | Executed: the re-wrapped lines run 75, 76, 76, 75, 8. The one line still over 88 in that paragraph is 91 and is a single unbreakable path, unchanged by this range |
| 🟢 | the two survivors' exemption and its grounds | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/survivors.md:59-60` | confirmed | Read: both cited cases exist and both still carry the folded forbidden-verb loop; the positive assertions are in the direction a fold cannot silently pass. Executed: `read_exemptions` skips blanks and comments, so the inserted block costs no row. The grounds argue the act correctly; finding 1 is about a different sentence in the same row |
| ⬜ | round 1's `## Paste-ready fixes` cell reading *no paste-ready fix in the report* — already filed as #505 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/rounds/round-1.md:63` | answered | ⬜ — carried from round 2 unchanged. A defect in the record generator, not in this branch, and nothing in this range touches it |
| ❓ | the broad gate — the full suite, the repository-wide lint and the typecheck | `skills/verify/scripts/broad_gate.py` | out of verified scope | `agent-contract` §2 and `agents/warden.md` hand it to the sealer. The prompt withheld it, so nothing was declined. Answerer: the `sealer`, in its single run |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree at `a32d6d77`; every probe below ran there, the script or document was restored after each, and the clone and its environment were removed afterwards | the worktree was written to once, for this report |
| the hygiene case at `a32d6d77`, unmodified | `1 passed` — the baseline every probe below is read against |
| probe: `--add-assignee "someone"` added to the one `gh issue edit` argv | `1 failed` — the first escape the round named is closed |
| probe: a `gh issue reopen` argv spread across lines with one comment between two of its words | `1 failed` — the second escape is closed; this is what the folded reader counted as zero |
| probe: a plainly spelled `gh issue reopen` argv (the control) | `1 failed` |
| probe: the one `gh issue edit` argv replaced by a `gh api` call | `1 failed` — `== 1` shown red where `<= 1` passed |
| probe: a `gh issue reopen` argv whose first word is a module constant | **`1 passed`** — finding 1 |
| probe: a `gh issue reopen` argv whose verb is a module constant | **`1 passed`** — finding 1 |
| probe: a bare invented unit name injected into `seal/follow-up.md` prose, then `evidence-check` over the repository | exit 0 · 114 names read · **0 refused** — finding 2 |
| probe: the same name as `path#name` in `seal/follow-up.md` prose | exit 0 · 114 names read · 0 refused |
| probe: a bare invented unit name in this work item's `spec.md` (the control) | **exit 2** · 115 names read · **1 refused** |
| probe: the same name as `path#name` in this work item's `spec.md` | exit 0 · 114 names read · 0 refused — the gap round 2's record described |
| `evidence_check.py .` in the clone at `a32d6d77` | `total: 1453 ok · 0 drifted · 0 broken`; the fragment `14 ok`; `1 work item read · 99 unread · 114 names read · 0 refused`. Exit 0, read directly. Every figure the fix pass reported, exact |
| independent count of `.py` files under `.github/scripts/`, of those carrying a `__main__`, and of those calling `to_utf8()` | 13 / 13 / 6, so 7 non-callers. The corrected row's figures, re-derived rather than read |
| enumeration of the renamed case's old name over the whole tree, with each occurrence's marker placement | 9 occurrences in 7 files; 6 marked, all 6 on the name's own line; 3 unmarked and all 3 round records |
| `uvx ruff check` and `ruff format --check` over `tests/test_release_hygiene.py` in the clone | exit 0 and exit 0, read directly |
| measured line widths of the re-wrapped paragraph in `docs/branch-and-release.md` | 75 · 76 · 76 · 75 · 8. The one line over 88 in that paragraph is a 91-column unbreakable path this range did not touch |
| the eight modules and the repository-wide lint the orchestrating session ran; the 88 passed over the hygiene, rider and wrap modules; `survivor-check` over this fix range | not re-run — `agent-contract` §3, the handoff carries them |
| the 357 passed over fourteen modules, `ruff` 0/0, and `deferral-check`, `correction-check` and `unverified-check` the fix pass reports | not re-run — the handoff carries them, and §2 does not put them in this round's hands |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's single run, after the rounds settle, and this round did not take it |

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
| round-2 | `tests/test_release_hygiene.py:1084` | round 2's 🟡 1 — fixed |
| round-2 | `seal/follow-up.md:80` | round 2's 🟡 2 — fixed |
| round-2 | `seal/follow-up.md:81` | round 2's 🟡 3 — fixed |
| round-2 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:25` | round 2's ⬜ — answered |
| round-2 | `docs/branch-and-release.md:100` | round 2's ⬜ — answered |
| round-2 | `.github/scripts/tracker_labels.py:148` | round 2's ⬜ — answered |
| round-2 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-3.md:56-96` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/close_issues_on_release.py:189` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_declared_label_reaches_the_tracker.py:336` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_release_hygiene.py:1101-1131` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/rounds/round-1.md:63` | round 2's ⬜ — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `ast` reader closes the whitespace escape and not a value moved into a constant or a verb spelled through a variable, while a case docstring and a `seal/follow-up.md` row both say it is repaired — and that row asks the owner to convert two more cases on that premise. Measured at round 3, exit 0 on both open spellings | a correction to `seal/follow-up.md:83` and to the docstring at `tests/test_release_hygiene.py:1054`, with the paste-ready forms above | the repository owner |
| `seal/follow-up.md` is outside `evidence-check`'s records corpus, so no name in it is checked at all, and `path#name` is invisible to the name reader inside the work items that ARE read. Two gaps, both measured; nothing in the tree records either | an issue against `skills/evidence-check/scripts/evidence_check.py`, with the paste-ready body above | the repository owner |
| The guard that stops an answerer from being a condition tests one spelling while the rule is a shape — **already deferred** by round 2, written into `seal/follow-up.md:82` by its fix pass. Not re-litigated; verified as written and its second measurement confirmed | `seal/follow-up.md` | the repository owner |
| Whether `console.to_utf8()` is owed by every `.github/scripts/` entry point — **already deferred** by round 1, to `seal/follow-up.md:81`. Its figures are now correct and re-derived; nothing about the question moved | `seal/follow-up.md` | the repository owner |
| The arm neither `CONTRIBUTING.md` §*House rules* nor `CLAUDE.md` carries — **already deferred** by round 1, to `seal/follow-up.md:80`. Round 2 fixed that row's answerer; the question in it is untouched | `seal/follow-up.md` | the repository owner |
| Whether the two remaining folded forbidden-verb readers are converted — **already deferred** by this fix range, to `seal/follow-up.md:83`. Finding 1 is about how that row states the benefit, not about the question | `seal/follow-up.md` | the repository owner |
| `round-1.md`'s `## Paste-ready fixes` cell — **already filed as #505**, in the record generator rather than in this work | issue #505 | whoever owns `skills/code-review/scripts/round_record.py` |
