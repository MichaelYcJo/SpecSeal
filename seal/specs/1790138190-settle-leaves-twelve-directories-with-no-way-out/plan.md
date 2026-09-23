# Implementation Plan: settle leaves twelve directories with no way out

<!-- seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/plan.md
— HOW, in phases. This is the Design Gate's artifact. -->

Approved 2026-09-23 by the orchestrating session, under the owner's `automation` preset, when `smith` was spawned.

## Summary

Seven phases. The first two are #511 — the guard, then the one row it finds
today. The next three give the spec-less directory its way out and carry
that way out through every reader that tells a retirement from a deletion,
ending at the state a complete fold reaches: no `seal/specs/` at all. The
sixth writes down that a fold is not a work item, which is what breaks the
regress, and the seventh closes the work item.

The guard comes first because every later phase widens the set it protects:
a rule arm that could remove a directory a ledger row anchors into would
reopen #511 the moment it shipped. The CI readers come after the command
because they ask the command's predicate, and the empty-root phase comes
after the readers because the probe that proves it runs them.

**Nothing is retired on this branch** (`spec.md` O2). Every destructive run
happens in `tmp_path` or in a scratch clone that is deleted before the phase
closes.

## Technical context

- `skills/settle/scripts/settle.py` — `survey` classifies released items
  (guard first, then marker, then segment); `retire` reads its candidates
  from the tree again (`marked & present & released`), keeps what an open
  `evidence-todo.md` row holds, and exits 1 when it kept anything.
  `coordinates` reads rows **inside marker sections only**, which is why the
  guard needs its own read of every live line (`spec.md` G3).
- `skills/verify/scripts/unverified_check.py#folded_items`, `#live_lines`,
  `#check_file`, `#overviews_at`, `#show` — the fold record's one reader and
  the pieces the rule arm's predicate is built from; the `--baseline` block
  of `#main` is the first CI reader (`spec.md` G5).
- `skills/code-review/scripts/chain_check.py#main` — the `retired` arm, the
  second CI reader; it already loads `unverified_check.py` as `reader`.
- `skills/code-review/scripts/survivor_check.py#corrected`,
  `#records_a_past_round`, `#corpus` — the third; it loads no sibling today,
  and loading `unverified_check.py` by path is what `chain_check.py#load`
  already does from the same directory.
- `.github/workflows/hygiene.yml` and `templates/hygiene.yml` run all three
  on every pull request; **neither workflow changes** — the readers do.
- `seal/ledger.md` — 50 rows anchor `chain_check.py`, 18 `survivor_check.py`,
  14 `unverified_check.py`, 5 `settle.py`, 13 `docs/review-chain-spec.md`, 1
  `skills/settle/SKILL.md`, 1 `seal/README.md`, 7 `README.md`, 4
  `README.ko.md`, 3 `docs/release-checklist.md`, 2 and 1 the two
  `docs/one-root-by-lifetime` editions, and **none** `docs/the-evidence-ledger.md`
  (counted by `grep -o` over `seal/ledger.md` and `seal/ledger/*.md`, read).
  An edit to an anchored unit drifts its rows; each is re-read and
  re-verified in the phase that drifts it, never re-pointed.

**What breaks in six months.** A reader of retirement written twice. Four
parties ask whether a removed directory was retired, and today two of them
disagree with the command about the rule arm. If the predicate were spelled
in each, the next condition added to it — a changelog fragment, a `plan.md`
— would land in one and not the others, and the first sign would be a fold
pull request red in CI after `settle --retire` said the removal was fine.
That is why phase 4 is one function asked four times, and why its case
asserts that each reader calls it rather than re-deriving it.

**The second thing that breaks**: a floor re-pointed so that it passes only
once the corpus is gone. `docs/the-evidence-ledger.md` calls that a
lowering. Phase 5's floors are run against this branch's full tree **and**
against an emptied clone, and both have to be green.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Retire the spec-less directories with a marker line in `docs/` | a marker is the fold's record; over no prose it asserts a fold that never happened, and `unverified_check` then reads an open memo row as *absorbed by a policy document* | rejected — #517's body and D3 |
| An acknowledgement file, `seal/settles/` or a row somewhere, per retired directory | a record of a moment that accumulates and needs folding in turn | rejected — D2 |
| The rule arm exactly as D3's sentence says, open memo rows and all | `1788177600`, `1788395377` and `1790134781` lose open `## Not verified` rows with no reader noticing, and `unverified_check --baseline` refuses the fold anyway unless it too is taught to drop them — #514's L2 is the measured instance | rejected — `spec.md` G2; recorded as a judgment in `questions.md` |
| Teach only `settle`, leave the CI readers alone | the first fold pull request under the rule arm fails `unverified_check` and `chain_check` for every spec-less directory it removes, and the only way past is a marker D3 forbids | rejected — `spec.md` G5 |
| Spell the rule arm's predicate in each reader | the drift above; the marker arm already had this defect once, when `chain_check` did not grow the arm `unverified_check` had (`docs/review-chain-spec.md` §*The declaration…*: *this reader had not grown it*) | rejected — one function beside `folded_items` |
| Keep the `survivors.md` range-row and put it in a work item directory the fold opens only for it | a directory per fold is the regress D1 removes | rejected |
| Keep the range-row and route the fold straight to `main`, where the survivor step exits early | decides the owner's open second comment by the back door | rejected — `questions.md` Q1; the range exclusion makes either route pass |
| The fold runs through a lightweight review route with no directory | the chain's records live in `rounds/` and `chain_check` reads nowhere else; a route without a directory needs a second home for them, which D2 refuses | rejected — `spec.md` §*Which of D1's two answers* |
| `settle --retire` refuses the whole run when any row anchors inside the set | stricter, and unlike the evidence-todo guard beside it, which keeps per directory; a fold with one held directory could retire nothing | rejected — per directory, exit 1, as `docs/the-evidence-ledger.md` already says a hit gets |
| `settle --retire` removes the anchored row itself | which row goes is a judgment about a claim, and the command reads and groups (`docs/one-root-by-lifetime.md` §*What keeps `settle` light*) | rejected |
| Retire the eight clean spec-less directories on this branch | #517 §*Sequencing* orders ship-then-fold; a mechanism branch that also deletes 8 directories is two reviews in one diff, and the survivor sweep on this branch's own pull request would read the removals through the change under review | rejected — `spec.md` O2; A9 runs it on a scratch clone instead |
| Treat an absent `seal/specs/` as exit 2 and make the workflow skip the step | `templates/hygiene.yml` ships to every repository, so each would need the workflow edit; a reader that refuses its own settled state is the defect | rejected — the reader learns the state |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#511's guard.** `overview.md` opened (the frame's own `spec.md` turns `tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview` red until it exists). `settle` names every live ledger row — `seal/ledger.md` whole, above the first marker included, and every `seal/ledger/*.md` — whose anchor lies under a released work item's directory; `settle --retire` keeps each candidate a row anchors into, removes the rest, exits 1, and prints per row REMOVED or narrow (`spec.md` G3). `skills/settle/SKILL.md` §4 and `docs/the-evidence-ledger.md`'s *nothing refuses the removal first* paragraph say so in the same commit | A1–A3 in `tests/test_settle_reads_before_it_removes.py`, each seen red against the unfixed `retire` (`agent-contract` §15); `./bin/settle` on this branch names the `seal/ledger.md` row against `1788184145` and nothing else; the settle module and `tests/test_docs_line_wrap.py` | 62a7c6b |
| 2 | **The row the guard finds.** `seal/ledger.md`'s *The last round's fixes are read by nobody …* row REMOVED; one row in `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md` anchored on the `docs/review-chain-spec.md` unit that carries the #33 measurement (`spec.md` G4), no anchor under `seal/specs/`; `docs/the-evidence-ledger.md`'s `1788184145` sentence rewritten | `bin/evidence-check --strict .` exits 0; `./bin/settle` names no row; `grep -n "seal/specs/" seal/ledger/1790138190-*.md` finds no anchor | 3b1618a |
| 3 | **The rule arm in `settle`.** The report's own heading for a released spec-less directory; `--retire` removes it with no marker; a directory with an open memo row or an open `evidence-todo.md` row kept and named. For every directory it would retire, by either arm, the report lists the open `## Not verified` rows, the paths outside `seal/specs/` citing into it (a `specs/<id>…/` path, never a marker or a bare id), and the `tests/` files naming `seal/specs`. The predicate lands in `unverified_check.py` beside `folded_items`, asked of the working tree here. `skills/settle/SKILL.md` §1 and §4, `docs/the-evidence-ledger.md`'s *kept by name* rule, and both READMEs' `settle` row move in this commit | A4, A5 as cases, seen red first; a case that a guard-held rule-arm directory stays (phase 1's guard over the widened set); `./bin/settle` on this branch lists the ten released spec-less directories under the new heading with `1788177600` and `1788395377` named as kept and their four rows printed; the settle module, `tests/test_one_word_one_meaning.py`, `tests/test_docs_line_wrap.py` | |
| 4 | **The CI readers ask the same predicate.** `unverified_check.py --baseline` names a rule retirement apart from a fold and still refuses an open row or a base `spec.md`; `chain_check.py --baseline` prints `retired:` for it; `survivor_check.py` drops a retired directory's paths — either arm — from both sides of the range. `docs/review-chain-spec.md` §*The declaration, and where the check went instead*, `survivor_check.py`'s own §*A deletion is one row* docstring and the two readers' help text say so | A6–A8 as cases in `tests/test_unverified_rows_close.py`, `tests/test_chain_check_at_the_pull_request.py`, `tests/test_a_corrected_sentence_survives_elsewhere.py`, each seen red first; a case that each reader calls the one predicate; **A9 on a scratch clone** — `settle --retire` committed there, then the three readers against its parent, every exit code read directly, the clone deleted | |
| 5 | **An empty root is green.** `settle` and `settle --retire` exit 0 with a sentence on an empty or absent `seal/specs/` under a present root; `unverified_check.py` does the same for that root's `specs` path and still refuses any other missing path; every floor in `spec.md` G8 answered by `skills/settle/SKILL.md` §3 — an independent listing that holds at any size, or its property moved into a corpus built in `tmp_path` — and none lowered | **A10 on a scratch clone** with every directory under `seal/specs/` removed and committed: the G8 modules, `settle`, `settle --retire` and `unverified_check.py --baseline <parent> seal/specs/`; the same modules on this branch's tree; each re-pointed floor shown red with its defect planted (A11); clone deleted | |
| 6 | **A fold is not a work item.** `skills/settle/SKILL.md` gains the rule (no directory, no routing question, `: '[no-review]';` on every commit, judged at its pull request) and §*What a fold branch owes* loses the range-row and *Nothing in `seal/ledger.md` moves* (`questions.md` Q3's default); `docs/release-checklist.md` §2b; `docs/the-evidence-ledger.md`; a dated section in `docs/one-root-by-lifetime.md` and `.ko.md`; `seal/README.md` and `templates/seal-README.md`, byte for byte. Every pin those sentences had moves with them — `test_the_skill_carries_the_survivors_row_a_fold_branch_owes` among them | the settle module's document cases, `tests/test_first_setup_asks_once.py`, `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py`; each moved pin seen red with its new sentence deleted | |
| 7 | **Close.** `overview.md` finished; `changelog.md`; the ledger fragment written in one pass with every row the phases drafted; `survivors.md` only for what `bin/survivor-check --range origin/release/v0.14.0...HEAD` reports and a person judges correct where it stands (`questions.md` Q6); every row phases 1–6 drifted re-read and re-verified; the final `./bin/settle` report on this branch written into `phases/phase-7.md` as what the post-release fold will face | `bin/evidence-check --strict .`; `bin/survivor-check --range origin/release/v0.14.0...HEAD` with this branch's `survivors.md` if any; `bin/unverified-check --baseline origin/release/v0.14.0 seal/specs/`; `skills/code-review/scripts/chain_check.py --baseline origin/release/v0.14.0` — every exit code read directly. The broad gate is the `sealer`'s, after the rounds | |

**Phase 4's and 5's scratch clones.** A clone of this repository at the
phase's commit, under the scratchpad, driven from Python so no command line
carries a commit (`agent-contract` §8). `--released-at` is given a ref that
resolves in the clone and names `main`'s commit as this repository has it —
a local clone's `origin/main` is this repository's `main` branch, which may
be behind. What each run printed goes into the phase record; the clone, and
anything else the probe made, is gone before the phase closes (§7).

**What each phase record says it dropped.** Every sentence it rewrote in a
document, and whether it was overturned (D1, D3, #511) or moved; every row
it drifted, re-read, and re-verified.

## Operational impact

- **No workflow file changes.** Three shipped readers change what they
  accept (`spec.md` G6), so a repository running `templates/hygiene.yml`
  gets the new verdicts with the plugin update, and nothing to edit.
- **`settle` prints more and removes more.** The report gains headings and
  three listings; `--retire` gains an arm that removes without a marker, and
  a guard that keeps. Its exit codes are unchanged except that a settled
  root is 0.
- **A fold is a no-work-item change from now on.** A session that has run
  one as a work item before finds the skill telling it not to.
- `seal/ledger.md` loses one row. Rows on edited units change hash and gain a
  dated `Re-read` note.
- **The prompt budget is zero** (`CONTRIBUTING.md` §*What a change to a gate
  must carry*): nothing added asks anybody anything.
- **Platform honesty.** The readers and the guard are path arithmetic over
  `/`-joined repository paths and `os.path` on disk; the Windows leg of
  `.github/workflows/test.yml` runs every case this adds, and a case that
  compares a path compares one spelling.
