# 1788501054-a-check-reports-clean-while-something-is-missing — review round 5

| Field | Value |
|---|---|
| Target SHA | 111a6df |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | not yet — no broad run has happened on this branch at all, and it stays held: 🔴 1 is red on the release branch, so a broad run taken now is spent rather than banked |
| Fixes checked by | round-6 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🔴 1, the correction walk fails on `release/v0.8.0` and at the release→`main` pull request once this branch is squashed; and 🟡 2, both of `_correction_traces`' bounds are load-bearing and held by no case, one of them stopping enforcement the moment `Pass` is ticked |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE CAP IS SPENT AT THIS RECORD, and the floor fired here too. Both are
written down because they decide different things and both point one way.

`docs/review-chain-spec.md` §*The review run has a bound, and an end*: three
rounds ordinarily, and up to five ONLY while a 🔴 is open and only to close it.
Five rounds have run and every one found something. Round 4's 🔴 is what
licensed rounds four and five; five is the ceiling.

The floor is the other rule and it fired independently: *stop when a round
finds nothing that leaves the root and nothing that crashes*, and this round's
`Loses a record or crashes` is `no`. The spec's own sentence covers exactly
this pair — *a round that meets the floor may still have opened a 🔴 in a line
a person reads, and that round consumes the cap and ends the run in the same
breath.*

So the run ends at this record, and 🔴 1 is open at the end of it. That is a
state the documents describe and do not resolve: 🔴 means *blocks merge*, the
cap says no sixth round, and `Fixes checked by | nobody — <why> |` beside a
checked `Pass` FAILS the pull request by design. The three ways out are named
in the Deferred table and the choice is the repository owner's.

Written and committed before the fix pass it commissions, so both fix-surface
rows start pending. -->

## What this round was asked

The third verifying round of this run, at `git diff 4a28283..111a6df` — **eight
commits**, given as a count the round was told to re-take, and it did:
`git rev-list --count` returns 8.

Round 4's seven verdicts as the agenda, and what `round-4.md`'s `New units`
names — seven units and three widened cases — as the finding surface. Those
seven are the units round 4's fix pass invented, and nobody had reviewed them.

**Eight specific things to try to break**, named with coordinates: the new
checker units judged as code, and specifically **what survives a squash**; the
count of field-cell changes, which four rounds had each got differently; the
fourth recorded limit the pass called a real hole; the removal of both riders;
the fifteen mutations and the one that could have passed vacuously; the pin
loop that went from three copies to five; **the orchestrator's own row, inside
the target**; and the terminal condition itself — is there anything here a
sixth round would find.

**A sixth axis was named beyond the table's floor for this round alone: what
survives a squash.** `CLAUDE.md` fixes the merge method per direction, a
feature branch squashes into its release branch, and this repository has
already lost a `# RIDER:` stamp to exactly that — a patch release exists to fix
one line of it. That axis is what found 🔴 1.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The correction walk goes red the moment this branch is squashed. `test_a_cell_corrected_after_the_record_landed_says_so_in_the_record` reads each record's history with `git log -- <rel>` and guards on `assert changes`. A feature branch merges into its release branch by **squash**, so all four records collapse into one commit, every record then has exactly one, `changes` is 0 and the guard fires | `tests/test_a_record_precedes_the_fixes_it_commissions.py:896` | open | **Executed** by the round in a clone, and **re-executed by the orchestrator**: branch from `origin/release/v0.8.0`, `git merge --squash 111a6df`, one commit — each of `round-1.md` … `round-4.md` goes from 4, 3, 3 and 2 commits to **1**, and the case fails with *the walk compared no field cells at all*. The mechanism is confirmed rather than predicted by the records already on `main`: the orchestrator sampled six and every one has exactly 1 commit. `.github/workflows/test.yml` runs on `pull_request` and on `push` to `main` at `fetch-depth: 0`, so the feature→release pull request stays green and the **release→`main`** one is red. The guard proves the wrong thing about the wrong tree: its job is *the reader still reads cells* and it asks *this repository's history still contains an edited record*, which the merge method is entitled to make false. The round's replacement proves the reader on a fixture built in the case and lets the real-tree walk assert only what it finds |
| 🟡 2 | Both bounds of `_correction_traces` are load-bearing, held by no case, and one of them stops enforcing the moment this run ends. The reader bounds the record's body on the literal `- [ ] Pass` | `tests/test_a_record_precedes_the_fixes_it_commissions.py:816-828` | open | **Executed** by the round, three states each. The marker bound: with `round-3.md`'s trace deleted the scoped reader goes red and the unscoped one **passes**, because that record names `New units` twice in its ordinary reasoning before the marker — and deleting the marker split with the records untouched leaves all 140 green, so no case holds it. The `Pass` bound: `body = text.split("- [ ] Pass", 1)[-1]` finds nothing once the box reads `- [x] Pass`, so the body starts at the top of the file and a marker written **inside a parsed field cell** is accepted as the trace — the one place `templates/sdd-round.md` forbids, and forbids on this branch's own measured evidence. **Orchestrator re-verified by reading the unit**: the split is on the unticked spelling, literally. Ticking `Pass` is the edit that ends this run |
| 🟢 3 | Round 4's 🔴 1 — the malformed `New units` cell | `rounds/round-3.md:11` | answered | **Executed**: `depth_problems` returns `([], [], [], [])` for all four records' cells, run through the checker rather than read; the case passes; `chain_check` exits 1 on **two** lines, both `round-4.md`'s mid-run state. The error is gone |
| 🟢 4 | Round 4's 🟡 2 — one reason given for two widenings | `rounds/round-3.md:23-45` | answered | **Read**: the paragraph is out of the cell and the two reasons are separate. `93c8b89` is confirmed as `phase-2.md`'s `Commit` cell, so `skipped_by_narrowing` predates the review run and that widening was by choice |
| 🟢 5 | Round 4's 🟡 3 — the false limit on `says_not_yet`'s guards | `chain_check.py` | answered | **Executed**, cache purged: dropping `not rest` alone turns **20 red**, and the docstring says 20 where round 4 measured 19 — the difference is an assertion this same pass added, which the mutation now also kills. Both direct facts pinned, and the corrected wording pinned as text |
| 🟢 6 | Round 4's 🟡 4 — the rider standing in for a pin depth allows | `chain_check.py`, `tests/…` | answered | **Executed**: rider gone, pins are assertions inside a case that already covers the unit, so no unit and no depth question. `test_a_rider_reaches_its_file.py` passes and is not vacuous — 20 `RIDER:` lines remain and its own guard covers the empty case |
| 🟢 7 | Round 4's 🟡 5 — the fallback sentence false off Windows | `evidence_check.py` | answered | **Executed**: both paragraphs corrected and pinned, in the source and in `overview.md`. `bin/unverified-check` exits 0 with the Windows pairing open and the windows CI leg named — §13 stated rather than claimed closed |
| 🟡 8 | Round 4's 🟡 6 — the limit written in five places, pinned in three | `tests/test_a_record_precedes_the_fixes_it_commissions.py` | open, folded into 🟡 2's fix | The loop covers five and the fifth is pinned on the sentence rather than its emphasis. But `assert len(copies) == 5` is a tautology over a literal tuple: **executed**, a sixth copy appended to `spec.md` and the case still passed. The docstring's *if a sixth copy is added, it is added here too* is enforced by nothing. Same class, same file — the honest guard is a tree-wide grep for the phrase compared against the tuple |
| 🟢 9 | Round 4's 🟡 7 — a corrected cell leaving no trace | the four records | answered as the rule, defective as the unit | **Executed**: the walk finds three corrections, each traced under `CORRECTED IN PLACE`, and breaking `FIELD_ROW` turns the case red so the guard fires. The rule holds; the unit that enforces it is 🔴 1 and 🟡 2 |
| 🟢 10 | The orchestrator's own two rows at `111a6df` | `rounds/round-4.md:10-11` | answered | **Executed**, AST comparison over the **full** range `4a28283..111a6df`, docstrings stripped: zero top-level units added, removed or changed in either checker, so `Contract changes | none` holds over a range wider than the trailing comment cites. `New units` names exactly the seven the diff finds added — six in one test file, one in another — and the three widened cases show as changed rather than added. Both rows accurate |

## Executed probes

| What was run | Result |
|---|---|
| the five changed suites, in a `--no-local` clone at HEAD | **148 passed** |
| **the release squash, reproduced** — branch from `origin/release/v0.8.0`, `git merge --squash 111a6df`, one commit, then the case | records go 4·3·3·2 commits → **1·1·1·1**; the case **fails** on `assert changes`. Run by the round, and again by the orchestrator from a Python driver |
| record commit counts on `main`, sampled by the orchestrator | six records, **1 commit each** — the mechanism is already visible in the tree rather than only predicted |
| `_correction_traces` read directly by the orchestrator | the body split is on the literal `- [ ] Pass`, the unticked spelling — 🟡 2 |
| five code mutations and four record mutations | the marker bound and the `Pass` bound both survive code mutation with the suites green — 🟡 2 |
| a sixth copy of the escape claim appended to `spec.md` | the case still passes — 🟡 8 |
| dropping `not rest` alone from `says_not_yet` | **20 red**, matching the corrected docstring |
| every parsed cell of all four records through `says_none`, `says_not_yet`, `depth_problems`, `yes_or_no`, `nobody_reason` and `CHECKER_RE` | clean — round 4's 🔴 does not recur |
| AST comparison of top-level units over `4a28283..111a6df`, docstrings stripped | 0 changed in either checker; 7 added; 3 widened cases changed |
| `chain_check.py --baseline origin/release/v0.8.0`, by the round and by the orchestrator | exit 1, **two** lines, both `round-4.md`'s mid-run state |
| `evidence_check.py .` **unscoped**, no `--reverify` | exit 1, `535 ok · 1 drifted · 0 broken` — S8 alone at `@45edf260` |
| `uvx ruff check` on the five changed Python files · `bin/unverified-check` | passed · exit 0 |
| `git status --porcelain` and `git rev-parse HEAD` after the round | empty, `111a6df` — HEAD did not move, clone and probes removed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–4 | the count of whichever class the round is enumerating | Five rounds, five counts, and each was found wrong by the next — three ledger rows, then four of eight, then eight of ten, then nine of nine, and now 12/9/3 → 14/11/3. This round's is the first that moves for a reason anyone can name: two more pending fills landed |
| round 4 | `tests/test_a_record_precedes_the_fixes_it_commissions.py`, the units the fix pass invented | Round 4 closed its findings by building a new rule and a new reader. Round 5's 🔴 and 🟡 are both inside that reader. A sixth reader would be the third |
| round 5 | `.github/workflows/test.yml:43-46` | The comment there explains why the full history is fetched — for the rider stamps. A second guarantee now leans on git history and the file says nothing about it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The run's end, with 🔴 1 open.** The cap is spent at this record and the floor fired here as well, and 🔴 means *blocks merge*. Three ways out: **(a)** fix 🔴 1 and 🟡 2 and set this record's `Fixes checked by` to `nobody — the cap is spent`, which prints on every run and **fails the pull request beside a checked `Pass`**; **(b)** fix 🔴 1 and 🟡 2 and read the fixes with a verifying round, which **costs no round** — `skills/code-review/SKILL.md` says a round that opens nothing needing a fix does not consume the cap, so this is not an overrun and this row's earlier wording, *run a sixth round over the cap*, was wrong; **(c)** revert the correction-trace rule entirely — it was invented by round 4's fix pass to close a 🟡, it is the only thing on this branch keying on git history, and it has now produced the run's second 🔴. Under (c) round 4's 🟡 7 goes to the tracker and the branch loses the structural problem. **The repository owner chose (c)**, carried out in `phases/phase-9.md`; round 4's 🟡 7 is issue #159 | this row | **answered — the repository owner** |
| **The broad gate** — the full suite, the repository-wide lint and the typecheck. Still not run at all on this branch, and held on purpose: 🔴 1 is red on the release branch | `overview.md` §Not verified | the orchestrator, once 🔴 1 is settled |
| `plan.md:43`'s *575 cases green across the seventeen suites*, carried unopened because seventeen suites is the broad run | `overview.md` §Not verified | the orchestrator, at the broad run |
| Whether `st_ino == 0` arrives on `windows-latest`, and the `normcase` pairing the corrected §13 limit describes | `overview.md` §Not verified | the windows CI leg at this pull request |
| `questions.md` Q2, Q3 and Q4, all three confirmed written as questions with labelled options and a stated default | `questions.md` | the repository owner |
| ❓ `phases/phase-8.md`'s `Commit` cell backticks its hash where phases 1–7 write it bare. `test_a_phase_hands_the_next_one_a_record.py` checks field names only and passes, `plan.md` backticks all eight, and nothing resolves the value — the round could not judge whether the bare form is a convention or an accident | this row | the orchestrator |
| The round counted 84 records on `main` where the orchestrator's own `git ls-tree` count is **76**. Neither number changes the finding — every one sampled has exactly 1 commit — but the two do not agree and nobody has reconciled them | this row | nobody yet; it is an aggregate, which `docs/review-handoff-protocol.md` says is not a coordinate |
