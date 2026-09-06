# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — review round 1

| Field | Value |
|---|---|
| Target SHA | 579a916dbcaec31b2d35006353b2bbc4fbe3aa35 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 201 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | DATED_RECORD (depth 1); what_to_write_instead (depth 1); test_the_message_has_a_route_for_every_token_the_check_refuses (depth 1); test_the_experiments_prefix_covers_only_a_dated_record (depth 1); test_a_version_that_ends_a_sentence_is_still_a_version (depth 1) |
| Needs a fix | yes — findings 1 and 2 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, spawned against `579a916` with the draft pull request already open
and nothing to inherit. The prompt carried the committed spec chain, the two
tickets, and five labelled facts: the red-then-green pair, the eleven
mutations, the enumeration over the loaded set, #98's five quoting readings,
and the ledger re-verification — each with the coordinate that makes it
falsifiable, and the broad gate marked `unverified` and explicitly not this
segment's to run.

Beyond the axis table, the round was told to walk six axes this change asks
for by name: the **boundary**, because the rule *is* a comparison against the
running version; **what the token regex reads as a version**, given that the
build's own enumeration had missed `v0.3.0` where its plan's table did not
have it; **the scope of each exemption against the argument written beside
it**, the three being deliberately different widths; **whether a file can be
made exempt by naming itself**, since the exempt set is a list inside the
test while the tracked set comes from `git ls-files`; **the failure message
as a deliverable**, because #179's *Done when* makes it one; and **#98 as
comment-and-record only**, which is the hazard rather than the safety — no
assertion in this repository reads what a comment claims about a tool.

It was also told which form of the ledger check to read (unscoped) and which
form of the suite to run (narrow, named modules), that the full suite is the
orchestrator's, and to write around #187 and #189 — the record generator
drops report prose, and a bare pipe in a Verdicts cell truncates the row.

The first two of those six axes are where both findings came from.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 a version-shaped token immediately followed by a period never matches, so a version at the end of a sentence is invisible — including the running one, which the substring check this replaced caught | `tests/test_release_hygiene.py:56` | **fixed** `ea02184` | fixed at ea02184 — `` — the trailing lookaround is split into `(?!\w)(?!\.\d)`, so what is refused is a continuing number rather than any following period. The fix pass then mutated its own addition and found the reviewer's guard had no case behind it: `\d+` is greedy, so `v1.2.30` is caught whole with or without `(?!\w)`, and the case said to be guarding it could not see the loss. `0.9.0rc1` is the assertion that now pins it; executed: `timers_in` answers `[]` for `right for 0.8.3.` where the substring test is True; the replacement regex passes all 22 module cases and leaves the tree with no offender |
| 2 | 🟡 the `docs/experiments/` prefix exempts `README.md` and `README.ko.md`, which its own argument — the file name carries the date — is not true of; it is also the one exemption a new file joins by choosing its path | `tests/test_release_hygiene.py:82` and `:102-107` | **fixed** `e25ff8b` | fixed at e25ff8b — `` — a `/` entry exempts only a file whose own name begins with a date. The reviewer's patch searched the whole path, which left a dated DIRECTORY exempting every undated file beneath it; the fix pass read the date from the basename instead, which is what the reviewer's own sentence says, and added `README-2026-09-03-conventions.md` so a name cannot join the exemption by appending a date; executed: `timers_in("docs/experiments/README.md", "ships in 0.9.0", "0.8.3")` answers `[]`; the README opens by prescribing the dated name it does not itself carry |
| 3 | ⬜ the failure message offers three routes and none fits a date or another language's patch version, both of which the token regex reads as releases | `tests/test_release_hygiene.py:196-215` | **fixed** `e0cb595` | fixed at e0cb595 — `` — the orchestrator reversed the instruction to leave it: the message is this branch's own text, so it is a branch-caused defect and this repository fixes those where they arise. The fix pass measured which half was missing rather than assuming both: `3.13.9` already had a route, `VERSIONS_OF_ANOTHER_PRODUCT` with bash's entry as the worked example, and only a dotted date had none. One sentence added, no exemption for a date and no change to the token regex — a lookaround edited to exclude one shape is how finding 1 arrived. The message moved into `what_to_write_instead()` so the case reads the words a person sees rather than a copy; executed: `2026.09.03` and `3.13.9` are refused; nothing in the loaded set hits it |
| 4 | ✅ the red-then-green pair is the one claimed, and names exactly one offender | `62287e9` and `86a6e20` | answered | executed in a fresh clone: 1 failed / 24 passed at `62287e9`, message names `docs/issues-and-milestones.md:28 names 0.9.0` and nothing else |
| 5 | ✅ #98's three places all corrected, and no fourth place carries the old sentence | `tests/test_the_pull_request_language_is_the_repositorys.py:764-786`, `seal/ledger.md:562`, `rounds/round-5.md:68,80` | answered | executed: every `quotePath` occurrence in the tree read; the remaining four state only that the config is on by default, which is true |
| 6 | ✅ the in-place edit to `seal/ledger.md` is the fragment rule's stated exception, not a violation of it | `seal/ledger.md:550,562` | answered | read `CONTRIBUTING.md` §*House rules*; executed `evidence-check .` unscoped, 713 ok · 0 drifted · 0 broken |
| 7 | ✅ the enumeration over the tree as it now stands adds no offender, and every allowed token is one of the five plus `v0.3.0` | the nine `LOADED` prefixes at `579a916` | answered | executed: 64 files walked through `timers_in`, no refusal |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py tests/test_the_pull_request_language_is_the_repositorys.py -q` at `579a916` | 142 passed, exit 0 |
| `pytest tests/test_release_hygiene.py -q` at `62287e9`, fresh clone | 1 failed / 24 passed, exit 1; the failure names `docs/issues-and-milestones.md:28 names 0.9.0` and nothing else |
| `./bin/evidence-check .` unscoped at `579a916` | 713 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |
| the loaded-set enumeration re-run through `timers_in` at `579a916` | no offender; `1.2.3` x4, `0.2.0`, `v0.3.0`, `2.1.259` x2, `4.4.17`, and the three records of a moment |
| boundary probe: 14 texts through `timers_in`, and the same texts through the substring check this replaced | sentence-final versions answer `[]`; the substring check caught the running one — finding 1 |
| the replacement regex against all 22 no-argument cases in the module, and over the loaded set | every case passes, no offender — the fix costs no committed fixture |
| `timers_in` over three paths under `docs/experiments/` that no dated record would use | all `[]` — finding 2 |
| every `quotePath` occurrence in the tree, read | three corrected, four unrelated and true, the fragment the ticket cites folded into `seal/ledger.md` at 0.8.3 |
| `fold_ledger.py --check`, then `--version 0.9.0 --dry-run` | exit 1, then exit 0 — the answer `phases/phase-4.md` already records |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
