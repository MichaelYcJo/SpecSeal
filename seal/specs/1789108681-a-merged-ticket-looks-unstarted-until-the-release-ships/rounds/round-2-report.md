# round 2 — the verifying round's report

| | |
|---|---|
| Target | the diff of round 1's fixes, `076d691..ab069b1` |
| Review at | `ab069b1e58c0c0278f6a9cf6f078f8b24a4777fa` |
| Base of the branch | `origin/release/v0.11.1` = `f9c6907` |
| Ran by | specseal:warden on Opus 5 |
| Where the work was done | a `git clone --no-local` at the target SHA, in the session scratchpad, deleted before this report was written |

Round 1's fifteen verdicts are answered below. Fourteen are closed on my own
grounds. One — finding 5 — is closed at the coordinate it named and open one
line away, which is the same class at a second place. Three fixes the pass
declined to take whole were checked as decisions rather than inherited, and
all three declines hold.

The four units the fixes created are all correct and all four were seen red.

## The three surfaces, and what each one turned out to be

### Round 1's four blocking findings are closed, and two of them by measurement

**Finding 1 — the milestone read now pages, and the decline was right.**
`milestone_titles` at `.github/scripts/release_completeness_check.py:116-141`
carries `--paginate` and keeps `json.loads`. The fix pass declined the
paste-ready `--jq .[].title` on the grounds that the reviewer's premise was
false, and that decline is the half worth re-deriving rather than inheriting.
Re-derived today on gh **2.100.0**, not on the 2.92.0 the pass measured:
`gh api --paginate "repos/<owner>/<repo>/milestones?state=all&per_page=2"` —
seventeen pages — returns a single JSON list of 33 that `json.load` accepts,
exit 0, and `per_page=100` returns the same list. So `--paginate` merges
arrays on both versions and `--jq` would have been added against a fact.

Two mutations red: the flag dropped, and `per_page` lowered below the
maximum. Both turn `test_the_milestone_list_is_read_past_the_first_page` red
and nothing else.

**Finding 2 — the range is true in CI now, and the fix is threaded through
both commands.** `main()` reads `HEAD_SHA`, `merge_base(base, point)` and
`subjects_since(…, point)` both take it, and the step passes
`github.event.pull_request.head.sha`. The job that holds the step is the one
`release` job, whose single `actions/checkout@v4` at `hygiene.yml:28-30`
carries `fetch-depth: 0`, so the head commit the pull request names is an
object the job holds and `origin/main` is a ref it holds — the fix cannot
fail for a missing object.

Three mutations red, and they separate the three ways this could be done
wrong: `HEAD_SHA` never read; the head threaded into `merge_base` alone; the
head threaded into the log alone. Each turns
`test_the_range_is_measured_to_the_head_the_pull_request_names` red.

What stays **read** rather than executed is the merge-ref behaviour of
`actions/checkout` itself. No case here runs a workflow, and this round ran
none either.

**Finding 3 — the sentence is content-addressed and the claim under it is
true.** `docs/issues-and-milestones.md:127-129` now names the box by what it
asks instead of by where it sits. Checked against the checklist rather than
against the fix table: `docs/release-checklist.md` step 0 holds four boxes,
at lines 14, 18, 40 and 50, and line 40 opens *The milestone `release: X.Y.Z`
holds what this release is actually carrying, and nothing else* — which is
the box the new sentence describes. The second half of the new sentence, that
it is ticked before any of the release's cost is paid, is true of step 0 as a
whole: step 1 is the first thing that writes anything.

The pass also declined to move the box, against `phases/phase-4.md:58`. That
decline holds on the checklist's own ordering — boxes 1 and 2 establish what
the release branch carries, and the milestone box compares the milestone
against exactly that.

**Finding 4 — the answerer is corrected in both cells and the version is
rightly not named.** `overview.md` §*Not verified* and `questions.md` Q3 both
now send the question to the first squash into a release branch whose
`merged: X.Y.Z` label does not yet exist, and both say why this branch's
squash is not it.

### Round 1's notes: five closed, one closed at its coordinate and open one line away

Findings 6 and 7 are closed. Finding 6's new case covers the whole `env:`
block and every entry in it is pinned — five mutations red, one per entry,
plus one pointing `HEAD_SHA` at the merge ref's own sha. Finding 7 is
disclosed in the module docstring at `:15-22` and the behaviour is unchanged,
which is what `answered` means.

**Finding 5 is the one that is not finished.** See finding 5's row below and
the new finding it produced.

Findings 9 through 15 were closed by round 1 on its own grounds and nothing in
the fix diff reaches them: `judge`, the step's shell guard, the hotfix skip
and `label_merged_on_release_branch.py` are all untouched by
`076d691..ab069b1`. `survivor_check.py` over the fix range exits 0 against
879 files and 31 removed sentences, so 15 stays true of the fixes too.

### The four new units — correct, and every one of them red-able

All four pin a property rather than a spelling, and each is red for its own
mutation and for no other. The counting reconciles: 121 cases over the six
document modules and 54 over the three the build touched is **175**, which is
the figure the fix wrote into `overview.md:9` — 171 at the build plus the four
planted here.

One correction in the fourth unit's prose, below.

## Findings

🟡 **`.github/scripts/release_completeness_check.py:48-49` — the module's own
`Environment:` line still enumerates three variables, and the script now reads
four.** Finding 2's fix added `HEAD_SHA` and documented it in three places —
`merge_base`'s docstring, the comment above `point` in `main()`, and the
comment in the step's `env:` — and left out the one line whose job is to list
the script's inputs. The line reads *Environment: `REPO`, `HEAD_BRANCH`
(`github.head_ref`), and `BASE` …*.

Why it matters rather than reads badly. The sibling script's same line,
`label_merged_on_release_branch.py:48`, enumerates all four of its own
variables, so the convention in this directory is that the line is exhaustive
and a reader is entitled to treat it that way. The variable it omits is
`HEAD_SHA`, and the fix pass's own argument for turning finding 6 from a note
into a case is that `HEAD_SHA` is the one entry whose absence is **silent** —
it falls back to `HEAD`, which in CI is the merge ref, which reinstates
finding 2 with nothing saying so. So the enumeration drops precisely the input
a second caller most needs to be told about.

This is a documentation defect and not a behaviour one: the only caller today
is the step, and `test_every_input_the_script_reads_is_handed_to_it_by_the_step`
pins it. The cost is paid by whoever writes the second caller.

⬜ **`overview.md:31` still says eight modules — the same false count finding 5
fixed at `overview.md:9`.** The broad-gate row in §*Not verified* ends *Eight
modules were run narrowly instead*, and nine were: 121 cases over six modules
and 54 over three, both executed in the clone today. Finding 5 was fixed at
the coordinate it named rather than over the class that produced it, which is
`agent-contract` §12. The row is under `seal/specs/`, so it is a correction to
the run's paperwork and not something the tool ships.

⬜ **`tests/test_a_release_cannot_ship_an_untrue_milestone.py:488` says the
case covers four entries; the loop at `:492` covers five.** The docstring ends
*the case covers all four rather than one*, and the tuple it describes is
`("GH_TOKEN", "HEAD_BRANCH", "HEAD_SHA", "BASE", "REPO")`. Round 1's record
row 6 says five. Four is defensible as the count of variables the *script*
reads — `GH_TOKEN` is read by `gh` — but the sentence is about the case, and
the case asserts five.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 — is the milestone read's fail-open closed | `.github/scripts/release_completeness_check.py:116-141` | answered | Executed. `--paginate` present with `per_page=100` and `json.loads` kept. The decline of `--jq` re-derived on gh **2.100.0** rather than inherited from the pass's 2.92.0: `--paginate` over the milestones endpoint returns one merged JSON list of 33 at `per_page=2` and at `per_page=100`, `json.load` accepts both, exit 0. Mutations M1 (flag dropped) and M2 (`per_page` lowered to 30) each turn `test_the_milestone_list_is_read_past_the_first_page` red and nothing else |
| 2 | Round 1's finding 2 — is the fork-point range true in CI | `.github/scripts/release_completeness_check.py:84-102`, `:259-282`; `.github/workflows/hygiene.yml:270-283` | answered | Executed and read. The head reaches BOTH commands — `merge_base(base, point)` and `subjects_since(…, point)`. Mutations M3 (`HEAD_SHA` never read), M4 (head into `merge_base` only) and M5 (head into the log only) each turn `test_the_range_is_measured_to_the_head_the_pull_request_names` red. Read: the step sits in the one `release` job whose single checkout at `hygiene.yml:28-30` is `fetch-depth: 0`, so the named head commit and `origin/main` are both objects the job holds. The merge-ref behaviour of `actions/checkout` stays read, not executed, by anyone |
| 3 | Round 1's finding 3 — does the shipped sentence point at the right box | `docs/issues-and-milestones.md:127-129` | answered | Read, and checked against the checklist rather than the fix table. Step 0 holds four boxes at `docs/release-checklist.md` lines 14, 18, 40 and 50; line 40 is the milestone box and its own words are what the new sentence names. The decline to move the box holds: boxes 1 and 2 establish what the branch carries, which is what the milestone is compared against |
| 4 | Round 1's finding 4 — is Q3's answerer sent to a run that can reach the create path | `overview.md` §*Not verified*; `questions.md` Q3 | answered | Read. Both cells carry the corrected answerer, the reason the label already existed, and the note that this branch's squash still answers `--add-label`. The decline to name a version holds against `docs/branch-and-release.md` |
| 5 | Round 1's finding 5 — is the module count corrected | `overview.md:9` fixed; `overview.md:31` not | **open** | Executed at `:9` and re-derived rather than inherited: 121 cases over the six document modules and 54 over the three the build touched, exit 0 each, so 171 at the build and **175** after the fixes — exactly what the line now says. `:31` still reads *Eight modules were run narrowly instead*. Same false count, second coordinate, `agent-contract` §12. Under `seal/specs/`, so a correction to the paperwork rather than to the tool |
| 6 | Round 1's finding 6 — is the step's `env:` block pinned | `.github/workflows/hygiene.yml:270-283` | answered | Executed. Five mutations red, each naming its own entry: `HEAD_SHA` dropped, `HEAD_SHA` pointed at `github.sha`, `BASE` dropped, `REPO` dropped, `GH_TOKEN` dropped — the last also turns `test_the_job_asks_for_a_token_that_can_read_issues` red, which is the older case doing its job |
| 7 | Round 1's finding 7 — a reverted squash stays in D | `.github/scripts/release_completeness_check.py:15-22` | answered | Read. The module docstring's D definition now states it, why nothing subtracts the original claim, and what it would cost. The behaviour is unchanged, which is what `answered` rather than `fixed` means, and adding a second reader of revert bodies is mechanism a fix pass may not add |
| 8 | Round 1's finding 8 — whether `issues: read` reaches a pull request body | `.github/workflows/hygiene.yml:20-22` | deferred `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md` §*Not verified* | Read. The home exists, carries the question, the tree's one precedent, the reasoning and the direction if it does not hold, and names the repository owner at the 0.11.1 release pull request. Not settled here and not settled by writing to the tracker |
| 9 | Round 1's finding 9 — `M \ D` from commits, `L \ D` fails, `D \ L` reports | `.github/scripts/release_completeness_check.py#judge` | answered | Read: `judge` is untouched by `076d691..ab069b1`, so round 1's grounds still stand at the same content |
| 10 | Round 1's finding 10 — the step's guard is the release-only one | `.github/workflows/hygiene.yml:283-288` | answered | Read: the fix diff added lines to the step's `env:` and changed no line of the `run:` guard |
| 11 | Round 1's finding 11 — the hotfix skip fires and makes no call | `.github/scripts/release_completeness_check.py:250-257` | answered | Read: untouched by the fix diff; the new `point` read sits after the skip's `return 0` |
| 12 | Round 1's finding 12 — the readers are imported and the closer is unchanged | `.github/scripts/label_merged_on_release_branch.py` | answered | Read: the file is absent from the fix diff entirely |
| 13 | Round 1's finding 13 — no document this branch touched names a real version | `docs/` | answered | Executed: `test_release_hygiene` 32 passed inside the 121 over six modules, exit 0, at the target SHA |
| 14 | Round 1's finding 14 — the hotfix paragraph the prompt claimed | prompt vs `docs/branch-and-release.md` | withdrawn | Round 1 withdrew it and the fix diff touches that file not at all |
| 15 | Round 1's finding 15 — no survivors on this work item | `seal/specs/*/survivors.md` | answered | Executed over the FIX range rather than inherited: `survivor_check.py --range 076d691..ab069b1` exits 0, 879 files against 31 removed sentences, no removed wording still standing |
| 16 | 🟡 The module's `Environment:` line enumerates three variables and the script reads four — `HEAD_SHA` is missing, and it is the one entry whose absence is silent | `.github/scripts/release_completeness_check.py:48-49` | **open** | Read, and the class enumerated: `grep -rn "HEAD_BRANCH"` over the tree finds exactly one enumeration of this script's inputs, so the class is one. The sibling `label_merged_on_release_branch.py:48` lists all four of its own, which is why the line is read as exhaustive. No behaviour today — the only caller is pinned by `test_every_input_the_script_reads_is_handed_to_it_by_the_step` |
| 17 | ⬜ A new unit's docstring says the case covers four entries; its loop covers five | `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488` vs `:492` | **open** | Read. The tuple is `("GH_TOKEN", "HEAD_BRANCH", "HEAD_SHA", "BASE", "REPO")` and `round-1.md` row 6 says five. Four is the count of variables the script itself reads, so the sentence is describing something other than the case it is attached to |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on `test_a_release_cannot_ship_an_untrue_milestone`, `test_a_merged_ticket_says_so_on_the_tracker` and `test_ci_gives_the_checks_what_they_need`, in the clone at the target SHA | **54 passed, exit 0** |
| `bin/test -q` on `test_docs_line_wrap`, `test_one_word_one_meaning`, `test_release_hygiene`, `test_no_real_identifiers`, `test_the_rules_have_one_owner` and `test_a_question_says_who_can_answer_it` | **121 passed, exit 0**. With the 54 above this is 175 over nine modules, which is the figure finding 5's fix wrote |
| Mutation probe, eleven mutations applied one at a time to the clone and reverted, `test_a_release_cannot_ship_an_untrue_milestone` run after each | **10 red, 1 survived.** Red: `--paginate` dropped · `per_page` lowered to 30 · `HEAD_SHA` never read · head threaded into `merge_base` only · head threaded into the log only · `HEAD_SHA` dropped from the step · `HEAD_SHA` pointed at `github.sha` · `BASE` dropped · `REPO` dropped · `GH_TOKEN` dropped. Each names exactly the unit it should. Survived: `or "HEAD"` rewritten as a default argument |
| The surviving mutation, judged rather than reported | **Not a finding.** `hygiene.yml` triggers on `pull_request` alone, so `github.event.pull_request.head.sha` is never the empty string the `or` spelling defends against, and the step's own guard exits 0 for any base that is not `main`. Unreachable, so unpinnable without a case that lies |
| `gh --version` in this checkout | **2.100.0** — not the 2.92.0 the fix pass measured on, which is why finding 1's decline was re-derived rather than inherited |
| `gh api --paginate "repos/<owner>/<repo>/milestones?state=all&per_page=2"` to a file, then `json.load`, exit code read directly | **exit 0, one `list` of 33.** Same at `per_page=100`. `--paginate` merges arrays on 2.100.0 as it did on 2.92.0, so the pass's correction of round 1's premise holds on both |
| `evidence_check.py --strict .`, unscoped, in the clone | **exit 0** — 1137 ok · 0 drifted · 0 broken. The three anchors the pass re-verified resolve |
| `survivor_check.py --range 076d691..ab069b1` | **exit 0** — 879 files against 31 removed sentences |
| `uvx ruff check` and `uvx ruff format --check` on the two changed Python files | **exit 0** each; 2 files already formatted |
| `git status --porcelain` in the clone after every mutation was reverted, and in the working tree at the end | empty both times. The clone and the probe script are deleted |
| The broad gate — the full suite, the repository-wide `ruff check .` and `ruff format --check .` | **not yet.** It is the sealer's, `agent-contract` §2 assigns it there, and this round ran nothing broad. It comes due once finding 16 is answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `issues: read` reaches a pull request body through the issues endpoint | `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md` §*Not verified* | the repository owner, at the 0.11.1 release pull request |

## Paste-ready fixes

```python
Environment: `REPO`, `HEAD_BRANCH` (`github.head_ref`), `BASE` for the ref
the range is measured from (default `origin/main`), and `HEAD_SHA` for the
commit it is measured TO (default `HEAD`). `HEAD_SHA` is listed here because
it is the only one whose absence is silent: without it the range ends at
whatever the checkout left at `HEAD`, which on a `pull_request` event is the
merge ref, and `merge_base` explains what that costs.
```

```markdown
| **The broad gate.** `seal/config.md` names it — `bin/test -q && uvx ruff check . && uvx ruff format --check .` — and it was deliberately not run: `skills/agent-contract/SKILL.md` §2 assigns it to the sealer, once, after the review rounds settle. Nine modules were run narrowly instead | the orchestrator, by spawning the `sealer` |
```

```python
    `HEAD_SHA` is neither. Losing it falls back to `HEAD`, which in CI is the
    merge ref — so the step goes green, the range silently collapses to the
    spelling `questions.md` Q8 rejected, and finding 2 is back with nothing
    saying so. One silent entry in the block is what turns the note into a
    case, and the case covers every entry rather than one, because a reader
    deleting a line does not first ask which kind it is.
    """
```

Needs a fix: yes — finding 16, the module's `Environment:` line, which
enumerates three of the four variables the script reads and omits the one
whose absence is silent. Findings 5 and 17 are corrections and do not count.

Loses a record or crashes: no

## Proof block

Opened and read in full or in the named range: `.github/scripts/release_completeness_check.py`,
`.github/workflows/hygiene.yml`, `.github/scripts/label_merged_on_release_branch.py:48`,
`docs/issues-and-milestones.md:124-131`, `docs/release-checklist.md:1-120`,
`tests/test_a_release_cannot_ship_an_untrue_milestone.py`, `bin/test`,
`skills/code-review/scripts/round_record.py:2530-2600`, and in this work item
`rounds/round-2-asked.md`, `rounds/round-1.md`, `rounds/round-2-fixes.md`,
`overview.md`, `questions.md`, `seal/ledger/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships.md`.

Everything labelled **Executed** above was run in a `git clone --no-local` of
this repository at `ab069b1`, inside the session scratchpad, with exit codes
read directly and never through a pipe. The clone and the probe script were
deleted before this report was written; `git status --porcelain` in the
working tree is empty and this report is the only file it gained.
