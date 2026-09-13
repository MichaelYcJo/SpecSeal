# Review round 3 — the verifying round for round 2's one fix

Target SHA `a5fa14bac2ea877864a5ad54363ddd51a3056447`, branch
`fix/354-the-seal-and-ci-read-one-ledger-differently`, pull request 378.
Scope as given: the single commit `ae5b935..6730690`, three paragraphs
re-wrapped in three files. No agent was spawned (contract §6). The broad gate
was not run and is not this round's (contract §2).

Round 1's and round 2's verdicts are inherited. Nothing either round closed
was re-opened.

## Round 2's one fix holds

`6730690` re-wrapped three paragraphs and changed no word. Comparing each file
at `ae5b935` against the same file at `6730690` with every run of whitespace
collapsed to one space, the three diffs are empty. The commit touches three
files, nine lines added and nine removed, and nothing else.

The substance of round 2's finding 10 is closed. The 101-column line in
`spec.md` is gone, and so is the 16-column orphan in `overview.md`. What the
finding said would reach `CHANGELOG.md` no longer does.

The changelog bullet still reads correctly as a changelog entry. Its words,
its `- **…**` lead, its two-space continuation indent and its trailing `(#354)`
are unchanged, and the paragraph it sits in reads in one pass.

## The split repair is genuine

I checked this rather than taking the account's word for it, and both arms
agree.

By ancestry, `6730690` is not an ancestor of `ae5b935` — the record commit is
the fix commit's parent, not its descendant. `ae5b935` touches only the three
files under `rounds/`; asking git for the three re-wrapped paths inside that
commit returns nothing, so the record really does not carry the work its own
verdicts commission.

By the check itself, `chain_check.py` over this work item prints no
`written_late` message for `round-2.md`. That is the arm that refused the
first attempt, and it is quiet now. The two messages it does print are the
two states this round and the sealer close, and neither is a defect in the
commit under review:

- `Broad gate` is `not yet` on the last record. That is the sealer's, and it
  is what comes due once this round's record lands.
- `Pass` is checked beside `Fixes checked by: nobody`. This round is what
  fills that cell; `round-2.md` then names round 3 and round 3's own record
  reads `no fixes to check`.

## The two records say what the commit did

`round-2.md`'s narrative says the orchestrator re-folded the three paragraphs
after the round, and names it as an edit the round did not read. `6730690`
re-folds exactly those three paragraphs in exactly those three files. Its row
10 carries `fixed` and the commit, and the commit message names round 2's
finding 10 as its cause.

`Contract changes` and `New units` both read `none`, which the commit bears
out: it adds no unit and touches no contract surface. The empty code span in
row 10's grounds cell is the already-ridered `fix_table` defect that round 2's
own Deferred table names so it is not re-reported; it is left alone here for
the same reason.

The commit message's claim that nothing went red is true for the reason it
gives. `tests/test_docs_line_wrap.py` holds an explicit `COVERED` list, and no
path under `seal/specs/` and no `CHANGELOG.md` is in it. I read the list; I
did not re-run the module, because round 2 already ran it at 23 passed and the
fix cannot have changed what the list contains.

## ⬜ The fold was not cascaded, so the changelog still holds a short line

`seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/changelog.md:8`
and `…/spec.md:10`.

The re-wrap re-broke the lines the finding named and stopped there instead of
re-flowing the rest of each paragraph. In `changelog.md` the 30-column orphan
at the old line 7 became a 40-column line at line 8; in `spec.md` the fold that
removed the 101-column line left a 31-column line at line 10. `overview.md` was
cascaded properly and is clean at 74/78/76/67 columns.

The changelog is the file whose reason for mattering was that it ships
verbatim, so the ragged line does reach `CHANGELOG.md` at the release the way
the old one would have.

**This is ⬜ and it should not be commissioned.** Markdown joins soft-wrapped
lines, so nothing anyone reads differs; `CHANGELOG.md` is outside
`test_docs_line_wrap.py`'s `COVERED` list, so nothing goes red; and the fix
would cost another commit plus another verifying round to change no rendered
output. It is written down so that whoever next edits these paragraphs folds
the whole paragraph rather than the line.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 2's finding 10 is fixed: the three paragraphs were re-wrapped and no word moved | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/changelog.md` · `overview.md` · `spec.md` | answered | executed — each file at `ae5b935` against the same file at `6730690` with whitespace collapsed, all three diffs empty; `git show --stat` is three files, 9 insertions and 9 deletions, nothing else |
| 2 | The changelog bullet still reads as a changelog entry after the re-wrap | `…/changelog.md:4-21` | answered | read — words, `- **…**` lead, two-space continuation indent and the trailing `(#354)` all unchanged; it is the file that is concatenated verbatim at the release, so it was read whole |
| 3 | The `written_late` repair is genuine: the record commit does not contain the fix and does not descend from it | `ae5b935` · `6730690` | answered | executed — `git merge-base --is-ancestor 6730690 ae5b935` exits 1 and the reverse exits 0, read directly; `git show --name-only ae5b935` is three `rounds/` files and no re-wrapped path; `chain_check.py --baseline release/v0.11.3` prints no `written_late` line for `round-2.md` |
| 4 | The commit message's "nothing went red" is true for the reason it gives | `tests/test_docs_line_wrap.py` `COVERED` | answered | read — the list carries no `seal/specs/` path and no `CHANGELOG.md`; round 2 had already run the module at 23 passed and the fix cannot change the list |
| 5 | `round-2.md` describes the edit `6730690` actually made, and its `Contract changes` and `New units` cells hold | `…/rounds/round-2.md` | answered | read — the narrative names the same three re-folded paragraphs, row 10 carries `fixed` and the commit, and the commit adds no unit and touches no contract surface |
| 6 | ⬜ The fold was not cascaded: a 40-column line remains mid-paragraph in `changelog.md` and a 31-column line in `spec.md` | `…/changelog.md:8` · `…/spec.md:10` | open | executed — column widths measured per line at both commits: `overview.md` cascaded to 74/78/76/67, `changelog.md` moved its orphan from 30 columns to 40, `spec.md` replaced a 101-column line with a 31-column one. A correction only; nothing renders differently and no check covers either path |

## Executed probes

| What was run | Result |
|---|---|
| `git show --stat ae5b935..6730690` | three files — `changelog.md`, `overview.md`, `spec.md` under the work item — **9 insertions, 9 deletions**. Nothing else moved |
| Each of the three files at `ae5b935` against the same file at `6730690`, every run of whitespace collapsed to one space | **all three diffs empty.** The re-wrap changed line breaks and no word |
| Per-line display widths of the three paragraphs at both commits | `overview.md` 74/78/76/67, cascaded clean; `changelog.md` orphan moved 30 → 40 columns; `spec.md` 101-column line replaced, 31-column line left at line 10 |
| `git merge-base --is-ancestor 6730690 ae5b935` and the reverse | **exit 1** and **exit 0**, read directly. The record commit is the fix commit's parent, so the adding commit does not descend from the fix |
| `git show --name-only ae5b935`, and `git show --stat ae5b935` restricted to the three re-wrapped paths | three `rounds/` files; the restricted form returns **nothing**. The record commit does not contain the fix |
| `chain_check.py --baseline release/v0.11.3 --root .` | **exit 1**, read directly. **No `written_late` line for `round-2.md`** — the arm that refused the first attempt is quiet. The two messages printed are `Broad gate` is `not yet` and `Pass` beside `Fixes checked by: nobody`, which the sealer and this round's record close |
| `git merge-base --is-ancestor bc70e7d HEAD` | **exit 0** — `round-2.md`'s `Target SHA` is reachable from HEAD, so the reachability line above it is the requirement being stated and not a failure |
| `git status --porcelain` at the start, and again after every command | **empty each time.** Every command was read-only; no file was written inside the repository except this report |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It has not been taken at any SHA on this branch and it is not this round's to take (contract §2). This round opens nothing needing a fix, so it is what comes due next: the sealer's spawn, not a run for the session reading this to assemble |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `round_record.py`'s `fix_table` cuts the SHA out of the middle of its own code span, so row 10 of `round-2.md` reads `fixed at 6730690 — ``;`. **Already ridered** and already named in round 2's Deferred table so it is not re-reported as new. Listed here only to say it was seen again and left alone | the existing rider on that function | the repository owner |
| Whether `broad-gate`'s own end-to-end run shows the notice absent at exit 2 | `overview.md` §*Not verified*. Already deferred by this branch | the sealer |
| `ANCHOR_RE` drops a coordinate it cannot parse instead of naming it | `seal/follow-up.md` §*Schedulable items with nowhere else to go*. Already deferred, and round 2 confirmed the row's count | the repository owner |
| The framer / overview-case contradiction | #379. Already deferred by round 1's fix pass | the repository owner |

Needs a fix: no

Loses a record or crashes: no

Round 2's one fix holds and the split repair is genuine. The single ⬜ above
changes nothing anyone reads and nothing any check measures; it is a note for
the next editor of those paragraphs, not work to commission. The run has
nothing open, so the broad gate is what comes due.

## Proof

Opened, at `a5fa14b` unless stated:

- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/changelog.md`, at `ae5b935` and at `6730690`
- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md`, at `ae5b935` and at `6730690`
- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md`, at `ae5b935` and at `6730690`
- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/rounds/round-2.md`
- `tests/test_docs_line_wrap.py`, the docstring and the `COVERED` list
- `skills/code-review/scripts/chain_check.py`, `written_late` and its caller
- The commit messages of `ae5b935`, `6730690` and `a5fa14b`
