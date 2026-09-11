# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — review round 2

| Field | Value |
|---|---|
| Target SHA | ab069b1e58c0c0278f6a9cf6f078f8b24a4777fa |
| Ran by | specseal:warden on Opus 5 |
| PR | #360 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 16, the module's `Environment:` line, which enumerates three of the four variables the script reads and omits the one whose absence is silent. Findings 5 and 17 are corrections and do not count. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

# round 2 — the verifying round's paragraph

| | |
|---|---|
| Target | the **diff of round 1's fixes**, `076d691..ab069b1` — not the branch |
| Review at | `ab069b1e58c0c0278f6a9cf6f078f8b24a4777fa` |
| Base of the branch | `origin/release/v0.11.1` = `f9c6907` |
| Draft pull request | #360 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-1.md`, closed — 6 fixed, 1 answered, 1 deferred |

## The job, and the one surface that is not verification

**The answers, not new findings** — for each of round 1's fifteen verdicts, is
it actually closed.

**One exception, and it is a finding surface.** `round-1.md`'s `New units` row
names four cases the fix pass created, each at depth 1:

- `test_the_range_is_measured_to_the_head_the_pull_request_names`
- `test_without_a_named_head_the_range_ends_at_HEAD`
- `test_the_milestone_list_is_read_past_the_first_page`
- `test_every_input_the_script_reads_is_handed_to_it_by_the_step`

A unit the fixes created has been reviewed by nobody, so these are *is this
correct*, not *did this close something*. One fix commit in this repository's
history created eight new units and four carried defects.

## What the fix pass says it did, to be checked rather than inherited

- **Finding 1 — it did not paste the reviewer's fix.** The report justified
  `--jq` with *`--paginate` over an array endpoint concatenates arrays into
  something `json.loads` refuses*, and the pass measured that false on gh
  2.92: seventeen pages merged into one list of 33 and `json.loads` took it.
  It took `--paginate` alone. **The orchestrating session re-derived this** —
  `gh --version` is 2.92.0 and the same command returns 33. Judge the fix, not
  the premise.
- **Finding 2 — it made the range true rather than documenting the collapse.**
  The step now passes `HEAD_SHA: ${{ github.event.pull_request.head.sha }}`
  and measures to it, with a fallback to `HEAD` when no such variable exists.
  The merge-ref behaviour of `actions/checkout` remains **read**, not
  executed, by anyone: no case here runs a workflow.
- **Finding 3 — it declined the reviewer's replacement sentence** because it
  was positional in the same way the defect was, and it left the box where it
  is rather than moving it, arguing that boxes 1 and 2 confirm what arrived
  and a milestone cannot be judged before that. Judge both halves.
- **Finding 6 turned from a note into a case** because finding 2's fix added
  `HEAD_SHA`, which **fails silent**: absent, it falls back to the merge ref
  and reinstates finding 2 with nothing saying so.
- Three ledger anchors drifted and were re-verified with round 1's finding
  written beside them rather than removed.
- The suite caught one of the pass's own: a non-raw docstring raised
  `SyntaxWarning: invalid escape sequence`.

## Executed by the orchestrating session at `6ed1689`

Exit codes read directly, no pipe:

- `bin/test -q` over the two new modules and six they touch → **169 passed,
  exit 0**.
- `gh --version` → 2.92.0; `gh api --paginate "repos/<owner>/<repo>/milestones?state=all&per_page=2"`
  → `json.loads` accepts it, 33 milestones. The pass's correction of the
  report holds.
- `git status --porcelain` → empty.

## Still unverified, and they stay that way

Finding 8 — whether `issues: read` reaches a pull request body — is deferred
to `overview.md` §*Not verified* with the repository owner as answerer, at the
0.11.1 release pull request. Do not settle it by writing to the tracker. The
broad gate is the `sealer`'s; do not run it.

## Not a finding

The gate run against the live tracker refuses naming **#359 and #361**. #361
is in `release: 0.11.1` deliberately and ships in this release, so the
milestone is true as planned and the refusal is the gate seeing work that is
not merged yet. Do not report it and do not write the pair into anything.

## The line the run ends on

Answer the job in a line of its own — `Needs a fix: no`, or `yes` and what
does. A 🟡 answered with grounds is `no`. **The reopening is one**: if this
round opens something, its own fixes get one more verifying round and a
second is refused, after which the run ends `capped`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 — is the milestone read's fail-open closed | `.github/scripts/release_completeness_check.py:116-141` | answered | Executed. `--paginate` present with `per_page=100` and `json.loads` kept. The decline of `--jq` re-derived on gh **2.100.0** rather than inherited from the pass's 2.92.0: `--paginate` over the milestones endpoint returns one merged JSON list of 33 at `per_page=2` and at `per_page=100`, `json.load` accepts both, exit 0. Mutations M1 (flag dropped) and M2 (`per_page` lowered to 30) each turn `test_the_milestone_list_is_read_past_the_first_page` red and nothing else |
| 2 | Round 1's finding 2 — is the fork-point range true in CI | `.github/scripts/release_completeness_check.py:84-102`, `:259-282`; `.github/workflows/hygiene.yml:270-283` | answered | Executed and read. The head reaches BOTH commands — `merge_base(base, point)` and `subjects_since(…, point)`. Mutations M3 (`HEAD_SHA` never read), M4 (head into `merge_base` only) and M5 (head into the log only) each turn `test_the_range_is_measured_to_the_head_the_pull_request_names` red. Read: the step sits in the one `release` job whose single checkout at `hygiene.yml:28-30` is `fetch-depth: 0`, so the named head commit and `origin/main` are both objects the job holds. The merge-ref behaviour of `actions/checkout` stays read, not executed, by anyone |
| 3 | Round 1's finding 3 — does the shipped sentence point at the right box | `docs/issues-and-milestones.md:127-129` | answered | Read, and checked against the checklist rather than the fix table. Step 0 holds four boxes at `docs/release-checklist.md` lines 14, 18, 40 and 50; line 40 is the milestone box and its own words are what the new sentence names. The decline to move the box holds: boxes 1 and 2 establish what the branch carries, which is what the milestone is compared against |
| 4 | Round 1's finding 4 — is Q3's answerer sent to a run that can reach the create path | `overview.md` §*Not verified*; `questions.md` Q3 | answered | Read. Both cells carry the corrected answerer, the reason the label already existed, and the note that this branch's squash still answers `--add-label`. The decline to name a version holds against `docs/branch-and-release.md` |
| 5 | Round 1's finding 5 — is the module count corrected | `overview.md:9` fixed; `overview.md:31` not | **fixed** `64d830b` | fixed at 64d830b — ``, `overview.md:31`, *Eight modules* → *Nine*. Both figures re-derived rather than inherited, and the module list at `:9` names the same nine. **Class swept rather than the coordinate**, which is what produced this finding: `grep -rniE "\b(eight\|nine)\b"` over the work item excluding `rounds/` returns **five** hits — `overview.md:9` already correct, `overview.md:31` this one, `questions.md:17` and `plan.md:81` both counting open milestone issues, a different subject and both true, and `phases/phase-5.md:31`'s *Eight rows*, which counts ledger rows and agrees with `overview.md:9`. (This cell said *four* while naming the fifth in its own next breath; round 3 re-ran the command and reported it as finding 20.) The `rounds/` records keep their *eight*: they are past-state documents read at their own target SHA, and `round-1-report.md:17` saying *165 across the eight modules the paragraph names* is a true statement about what that paragraph said; Executed at `:9` and re-derived rather than inherited: 121 cases over the six document modules and 54 over the three the build touched, exit 0 each, so 171 at the build and **175** after the fixes — exactly what the line now says. `:31` still reads *Eight modules were run narrowly instead*. Same false count, second coordinate, `agent-contract` §12. Under `seal/specs/`, so a correction to the paperwork rather than to the tool |
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
| 16 | 🟡 The module's `Environment:` line enumerates three variables and the script reads four — `HEAD_SHA` is missing, and it is the one entry whose absence is silent | `.github/scripts/release_completeness_check.py:48-49` | **fixed** `4eda3a5` | fixed at 4eda3a5 — ``, `.github/scripts/release_completeness_check.py:48-52`. The finding holds as stated: `grep -n environ` over the file returns four reads — `HEAD_BRANCH:251`, `REPO:260`, `BASE:261`, `HEAD_SHA:266` — and the line named three. It now names `HEAD_SHA` with its default (`HEAD`) and one clause saying its absence is the silent one, pointing at `merge_base` for the cost. **The paste-ready text was taken in part and declined in part:** it restated the merge-ref argument in full, and that argument already stands twice in this file — `merge_base`'s docstring at `:88-98` and the comment above `point` at `:262-265`. A third copy adds a third place to keep in step, which is the failure mode finding 16 is itself an instance of. The enumeration, the default and the pointer are what close the defect; the retelling is what the finding says is already there. **Class swept:** only two scripts in `.github/scripts/` carry an `Environment:` line. The sibling's is complete — its fifth, `DRY_RUN`, has its own paragraph at `:44-46` — and `close_issues_on_release.py` reads four and carries no such line at all, so there is no false enumeration there and it is outside this branch's diff; Read, and the class enumerated: `grep -rn "HEAD_BRANCH"` over the tree finds exactly one enumeration of this script's inputs, so the class is one. The sibling `label_merged_on_release_branch.py:48` lists all four of its own, which is why the line is read as exhaustive. No behaviour today — the only caller is pinned by `test_every_input_the_script_reads_is_handed_to_it_by_the_step` |
| 17 | ⬜ A new unit's docstring says the case covers four entries; its loop covers five | `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488` vs `:492` | **fixed** `f4384ed` | fixed at f4384ed — ``, `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488`. *all four* → *every entry*. The reviewer's paste-ready text was taken over the arithmetic correction *all five*: the tuple at `:492` has five members today and the step's `env:` block can gain a sixth, which would rot *five* exactly as it rotted *four*. The sentence now describes the loop rather than counting it. No case pins this and none was added — the unit is round 1's own fix surface, so a case for it would be depth 2; Read. The tuple is `("GH_TOKEN", "HEAD_BRANCH", "HEAD_SHA", "BASE", "REPO")` and `round-1.md` row 6 says five. Four is the count of variables the script itself reads, so the sentence is describing something other than the case it is attached to |

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/release_completeness_check.py:100` | round 1's 1 — fixed |
| round-1 | `.github/scripts/release_completeness_check.py:71-84`, `:236`; `.github/workflows/hygiene.yml:269-280` | round 1's 2 — fixed |
| round-1 | `docs/issues-and-milestones.md:127-128` vs `docs/release-checklist.md:14,18,40,50` | round 1's 3 — fixed |
| round-1 | `overview.md` §*Not verified*; `questions.md` Q3 | round 1's 4 — fixed |
| round-1 | `overview.md:9` | round 1's 5 — fixed |
| round-1 | `.github/workflows/hygiene.yml:269-280` | round 1's 6 — fixed |
| round-1 | `.github/scripts/release_completeness_check.py:12-14` | round 1's 7 — answered |
| round-1 | `.github/workflows/hygiene.yml:20-22` | round 1's 8 — deferred |
| round-1 | `.github/scripts/release_completeness_check.py#judge` | round 1's 9 — answered |
| round-1 | `.github/workflows/hygiene.yml:277` | round 1's 10 — answered |
| round-1 | `.github/scripts/release_completeness_check.py:212-219` | round 1's 11 — answered |
| round-1 | `.github/scripts/label_merged_on_release_branch.py:77` | round 1's 12 — answered |
| round-1 | `docs/` | round 1's 13 — answered |
| round-1 | prompt vs `docs/branch-and-release.md` | round 1's 14 — withdrawn |
| round-1 | `seal/specs/*/survivors.md` | round 1's 15 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `issues: read` reaches a pull request body through the issues endpoint | `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md` §*Not verified* | the repository owner, at the 0.11.1 release pull request |
