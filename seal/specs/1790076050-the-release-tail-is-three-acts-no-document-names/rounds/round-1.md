# 1790076050-the-release-tail-is-three-acts-no-document-names — review round 1

| Field | Value |
|---|---|
| Target SHA | b29c86053b7092b24ac91ba756a39895be6c0599 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 500 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `317a96e0ebcc3b36b927c22ab5f2a81469528748..d2b1e19487e7b656ea016335264ad78582ac5231`, 2 commits |
| Contract changes | none |
| New units | spend_label (depth 1); test_an_already_closed_issue_reports_no_removal_that_failed (depth 1); test_an_already_closed_issue_reports_a_removal_that_worked (depth 1); test_a_dry_run_over_an_already_closed_issue_names_the_label_too (depth 1); test_every_report_of_the_removal_goes_through_one_place (depth 1); test_the_label_is_two_states_and_nothing_schedules_from_it (depth 1) |
| Needs a fix | yes — findings 1, 2, 3, 4, 5 and 6. Finding 1 is the one that changes what the release writes; 2 is a figure in a policy document that no record supports; the other four are a crash path, two records that misname what they point at, and a case whose two assertions are not bound to the call they judge. |
| Loses a record or crashes | no — finding 1 writes a false line into a job log rather than losing a record, and finding 3's crash is reachable only from a local console the release does not use. Nothing found leaves the root, and no path this release exercises crashes. |

- [x] Pass

## What this round was asked

Round 1, the first reading of the built branch, with nothing to inherit. Spec
compliance against the frame first, and the tickets ranked below `docs/`.

The round was pointed at the eight divergences `overview.md` records, and at
four of them in particular: the three facts the build found wrong in its own
frame and corrected; the pinned case that forbade `gh issue edit` and was
restated rather than relaxed, with the question whether the property its own
message claims still holds; the reworded *Nothing reads this label*, with the
question whether what replaced it is true of the tree; and the `seal/ledger.md`
row REMOVED rather than re-pointed, with both halves to judge — that the
removal was the right act, and that the carried-forward row's coordinates
resolve and say what it claims.

Two things no case in this suite can prove were named as such and handed to the
round as a reading rather than a run: the tag-triggered job actually running,
and the live label write. The round was asked whether what ships would work
when that release runs.

#499 was named as filed and not repaired here, with the question whether the
class reaches a second case.

The broad gate was withheld. The eight modules and the lint the orchestrating
session had already run were named so the round would not spend itself
repeating them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | an already-closed issue reports a removal that failed, and a dry run over one says nothing about the label | `.github/scripts/close_issues_on_release.py:263-272` | **fixed** `cd4f9512` | fixed at cd4f9512; Executed in a clone: the job log prints `could not remove …` and then `removed …` for the same issue, and the label survives. No case sets an issue closed before `main()` runs |
| 2 | `docs/branch-and-release.md`'s 244 / 88 / *exactly one names a tag* are recorded nowhere and contradict the 258 / 96 the phase record and the script docstring carry for the same file on the same day | `docs/branch-and-release.md:91-95` | **fixed** `cd4f9512` | fixed at cd4f9512; Read: `phases/phase-3.md`'s table sums to 310 and gives 157+96+5 with a `sha`; `grep` over the work item and `docs/` finds 244 and 88 in this paragraph alone |
| 3 | the one new script with no `console.to_utf8()`, printing U+2014 from an arm a person types | `.github/scripts/tracker_labels.py:135` | **fixed** `cd4f9512` | fixed at cd4f9512; Read: both sibling new scripts call it at `:195` and `:238`; `hooks/console.py` says each entry point carries the call; `tests/test_console_is_not_utf8.py` enumerates `hooks/` only |
| 4 | a case named for the sentence it no longer asserts, and ledger row T1 anchors its claim on that name | `tests/test_a_release_is_sized_by_a_criterion.py:226` | **fixed** `cd4f9512` | fixed at cd4f9512; Read: the body asserts `One thing reads it`; the sibling case in `tests/test_release_hygiene.py` was renamed in the same commit for the same reason |
| 5 | the R2 removal cites `CONTRIBUTING.md` §*Running the checks*, which says the opposite, and the arm that exists is conditioned on code that went away | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:61-69` | **fixed** `cd4f9512` | fixed at cd4f9512; Read: §*House rules* gives two arms, both about the code leaving; R2's anchors still resolve and `evidence-check` agrees. The act is right; the grounds are not there |
| 6 | the restated hygiene case checks `--remove-label` and `--add-label` against the whole file rather than against the one `issue edit` it counted | `tests/test_release_hygiene.py:1083-1095` | **fixed** `cd4f9512` | fixed at cd4f9512; Read: an `issue edit` carrying `--remove-label` plus `--add-assignee` passes every assertion. The restatement's reasoning is sound; the binding is not |
| ⬜ | the closing records state 14 anchors (13), `R2's two anchors out` (one), and omit S9 from the re-stamped list; `questions.md:29` keeps a measured-false frame claim | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/overview.md:5` | answered | ⬜ — a correction to this run's own paperwork, not to the tool, so `Needs a fix` does not count it. The measured figures are in the finding above |
| ⬜ | two `gh api` reads of the same issue where `_issue_api` already returns both fields | `.github/scripts/close_issues_on_release.py:257-258` | answered | ⬜ — executed: reads `[100, 7, 7]`. One extra call per closed issue per release, against a 1,000/hour budget. Raised for the record, not commissioned |
| ⬜ | the release body reaches `gh` as one argv element; largest real section 33,553 of a 131,072 limit | `.github/scripts/publish_release_note.py:179-191` | answered | ⬜ — executed over the real `CHANGELOG.md`. Four times the headroom today. `--notes-file -` removes the ceiling if anybody wants it |
| ⬜ | `clau.de` and two real organisation names enter the tree and `tests/test_no_real_identifiers.py` cannot see any of them | `.github/scripts/plugin_directory_check.py:81-85` | answered | ⬜ — read: `DOMAIN_RE` covers `com\|io\|net\|org\|ai\|dev` only and checks no organisation names. The placement is reasoned in `spec.md`; the green build is not what cleared it |
| ⬜ | *One thing reads it* — the reconcile step in the same workflow also reads the label, to decide whether to create it | `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move* | answered | ⬜ — *one workflow* is exactly true and the section is about the label on an issue. The rewording IS true of the tree, which is the question the prompt asked |
| ❓ | the broad gate — the full suite, the repository-wide lint and the typecheck | `skills/verify/scripts/broad_gate.py` | out of verified scope | `agent-contract` §2 and `agents/warden.md` hand it to the sealer; the prompt asked for none, so nothing was declined. Answerer: the `sealer`, in its single run |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree, checked out at `b29c8605`; every probe below ran there and the clone was removed afterwards | the worktree was never written to except for this report |
| probe: `close_issues_on_release.main()` over an issue already closed, carrying `size: now`, with a tracker that refuses the edit | `could not remove 'size: now' from #7: HTTP 502 — the issue is closed either way` followed by `removed 'size: now' from #7`; the label is still on the issue |
| probe: the same issue under `DRY_RUN=1` | `#7 already closed (named by #100) — leaving it` and nothing about the label; the open-issue path prints `would remove` |
| probe: counting `_issue_api` reads for one pull request naming one issue | `[100, 7, 7]` — the same issue read twice |
| probe: `publish_release_note.section_body` over the real `CHANGELOG.md` for 0.13.0 / 0.12.3 / 0.12.1 / 0.11.4 | 4152 / 7112 / 20984 / 12592 characters, and no body contains a later `## ` heading |
| probe: `publish_release_note.title_from` over the real tagged commit messages of v0.13.0 / v0.12.3 / v0.12.1 / v0.11.4 | three read the `release:` line; v0.12.3 falls back to the tag name and says which it used |
| probe: largest released `CHANGELOG.md` section, against the per-argument limit | 33,553 characters (0.9.1) of 131,072 |
| `python3 skills/evidence-check/scripts/evidence_check.py .` in the clone at `b29c8605` | `1452 ok · 0 drifted · 0 broken`; the work item's fragment reports `13 ok` |
| the same at `6d410023` | `1440 ok`; `seal/ledger.md` alone goes 1440 → 1439 across the range |
| mechanical count of backticked coordinates in the ledger fragment | 13 total, 13 unique |
| `correction_check.py --range 6d410023...b29c8605` | `no merge commit in 6d41002..b29c860, so no correction can have been dropped at one` — exit 0 |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py tests/test_a_document_that_names_a_script_says_how_to_reach_it.py tests/test_one_word_one_meaning.py -q` — the three constraints `plan.md` named that the handoff's eight modules do not cover | `76 passed, 7 skipped` |
| the eight modules the orchestrating session already ran, `ruff check` and `ruff format --check` | not re-run — `agent-contract` §3, the handoff carries them |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's single run, after the rounds settle, and this round did not take it |
| the tag-triggered job running on GitHub, and the live `gh label create` on the tracker | **not run here and not runnable here** — `agent-contract` §6 withholds both from every agent. `overview.md` names the releasing session |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The arm neither `CONTRIBUTING.md` §*House rules* nor `CLAUDE.md` carries: a `seal/ledger.md` claim falsified by code a branch ADDED, whose own anchors still resolve. The act taken here is right and undocumented | `seal/follow-up.md` | the repository owner, at the next change to `CONTRIBUTING.md` §*House rules* |
| Whether `console.to_utf8()` is owed by every `.github/scripts/` entry point as a class — five of nine call it and nothing pins any of them. Finding 3 fixes the one instance this branch introduced; the class is bigger than this branch | `seal/follow-up.md` | whoever owns `hooks/console.py`'s convention |
| `tests/test_the_gate_names_every_step_ci_runs.py#test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before` reddening in any checkout whose path contains `release` — **already deferred**, as issue #499, by the build. Not re-litigated here; I looked for the class reaching a second case and did not find one | issue #499 | whoever owns that module; the `sealer` first, since it decides whether the broad gate meets it from where it stands |
