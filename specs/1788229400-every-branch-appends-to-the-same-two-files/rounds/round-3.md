# 1788229400-every-branch-appends-to-the-same-two-files — review round 3

| Field | Value |
|---|---|
| Target SHA | `0d2a73b673881c2e80d2ebbaf89d88dac8e6e286` |
| Diff base | `origin/main` (`708e348`) |
| PR | not yet |
| Broad gate | run by the orchestrator after the redesign below |
| Fixes checked by | the orchestrator, by the mutations round 3 named |
| Needs a fix | no — and the branch then changed direction, see the closing section |

- [x] Pass

## Round 2's ten findings

The verifying round re-derived each rather than inheriting round 2's verdict.
`efe1946` carries the code, `ecb54f3` · `041fb2a` · `f3a52e9` the row move,
`0895567` the documents.

| Round 2 | Verdict | Grounds |
|---|---|---|
| 🔴 1 | **closed** | Squash simulation from `708e348`: `tests/test_ledger_stamps_resolve.py` 3 passed, `test_a_rider_reaches_its_file.py` 8 passed, `--strict` exit 0. The fragment writes no stamp, and a case asserts that rather than relying on it |
| 🔴 2 | **closed** | On the squashed tree the moved row derives the squash commit and a line inserted at the cited range makes it report DRIFTED, exit 1. The tripwire is alive |
| 🟡 3 | **closed** | `CONTRIBUTING.md` and `CLAUDE.md` now both say **appends** and both name removal-and-rewrite as what the rule permits |
| 🔴 4 | **closed** | A genuinely drifted row carrying two stamps reports `DRIFTED · row carries 2 stamps`, exit 1. With the ancestor's committer date skewed later, the ancestor still wins — the ordering is by ancestry |
| 🟡 5 | **closed** | Two spellings of one commit on an untouched row give `1 ok`, `--strict` exit 0 |
| 🟡 6 | **half** | `--default-repo` clears with both header rows declared; `--map` cannot be cleared by any header. Deferred |
| 🟡 7 | **half** | `--help`, the module docstring and the template are corrected; `skills/evidence-check/SKILL.md:32` was not. Became 🟡 D |
| 🟡 8 | **closed** | Mutation: the prose pass restored to unbounded turns its case red |
| 🟡 9 | **closed** | Mutation: the declared pass re-bounded turns its case red. Round 1's 🟡 6 fix went from no case to two |
| 🟡 10 | **closed** | The assertion is restored for all six documents and accepts both wrappings. Verified not vacuous |

## What round 3 opened, and what happened to it

No 🔴. Three items, all fixed at `2d56812`.

| # | Finding | Verdict | Grounds |
|---|---|---|---|
| 🟡 A | `widest_baseline`'s ancestry ordering had no case that could fail — replacing its body with `return shas[0]` left all 62 ledger cases green, and that reverts the choice to whichever cell came first, which is what round 2's 🔴 4 exists not to trust | **closed** `2d56812` | The implementer found the reviewer's fixture covered only the ancestry branch and added one for the committer-date fallback, so the mutation kills two cases rather than one. Four narrowed mutations each kill exactly their own case |
| 🟡 B | `test_one_commit_written_at_two_lengths_is_one_stamp` asserted on a drifted row, where 🔴 4's fix makes both readings agree. Reverting the dedup left 62 passed | **closed** `2d56812` | Rewritten against an untouched row, where the readings differ. The implementer moved the assertion off the exit code, since both readings exit 0 there and only the verdict text discriminates |
| 🟡 D | `skills/evidence-check/SKILL.md:32` was byte-identical to `d279efa` and false twice over — `--strict` also turns `UNMEASURED` and `AMBIGUOUS` into exit 2, and neither of those fails the run either way | **closed** `2d56812` | This one shipped to plugin users |

The reviewer judged that a fourth round whose whole content is *were two
functions and one sentence added* costs more than the check it performs, and
named the verification instead. The orchestrator ran it.

## The addendum, and what it corrected

The orchestrator handed the reviewer a lead: this branch moved 20 ledger rows
into a fragment, and `tests/test_ledger_stamps_resolve.py` reads
`.specseal/map.md` alone. **The lead's central premise was wrong**, and the
reviewer refuted it by execution.

`0895567` — a commit on this branch — added a guard that globs
`.specseal/map/*.md`. Cloning the branch, cutting a later work item from
`0d2a73b`, and writing a fragment that stamps a branch-only commit turns that
new case red **before** the squash, which is earlier than the old check ever
managed. The reach followed the rows in the same commit that moved them.

What remained was narrower and went to issue #56: the single-path `LEDGER`
constant, reachability measured against `HEAD` rather than the merge target
(which predates this branch), and an emptiness assertion that would report a
completed migration as a broken check roughly two dozen work items out.

The reviewer also found **🟡 F**, which the lead had not: `CLAUDE.md:96-98`
required a row moved into a fragment to carry its stamp along, and a new
assertion forbade any stamp in a fragment. **The two rules forbade each other**,
and a session obeying the document would break the build on a message telling
it to do what the document forbids. Not reachable by this branch's own
migration, which moves only invalidated rows and rewrites those afresh.

## The branch then changed direction

🟡 F put a choice to the repository owner, and the answer was to look past it.
Every mechanism this branch had built — `git blame`, first appearance, stamps,
`UNMEASURED`, `AMBIGUOUS`, and the two rules that now forbade each other — was
compensation for one fact: **a ledger coordinate was a line number, and a line
number moves for edits that have nothing to do with the claim.** Measured on
this branch, 12 of 23 commits touched `.specseal/`.

The owner's decision, stated as a rule change rather than a reconciliation:
*the repository is pre-1.0, and a better mechanism that is demonstrated beats
consistency with what is written today.* The review chain was explicitly
waived for the redesign, and the demonstration was not.

A row now cites a **symbol anchor** and a **content hash**, and no commit
appears in a ledger row at all. Drift is a hash mismatch rather than an
interval. The proof, executed:

| Requirement | Result |
|---|---|
| Migrate the real coordinates faithfully | 51 distinct coordinates → 62 anchors; **51 faithful, 0 partial, 0 failed**. Every new region contains every non-blank line the old range covered |
| Catch what the old scheme caught | A statement added to `_hides_a_commit` on the real ledger gives `1 drifted`, exit 1 |
| Not report what it falsely reported | A line inserted above everything in that file moves every line number, and the ledger still reads `41 ok` |
| The stale-on-arrival case (`questions.md` Q1) | Branch B changes the cited code and squashes first, A second: `DRIFTED` on the first run, exit 1 |
| Mutation-test every new branch | **13 mutations, 13 killed, 0 survived** |

`evidence_check.py` went 747 → 372 lines and no longer imports `subprocess`;
the checker runs no git at all. Wall clock, median of five: 356 ms → 114 ms.

Issues closed by the redesign, each checked rather than assumed: **#52** (no
stamps, no git), **#31** (the symbol *is* the coordinate; absent is BROKEN),
**#23**, **#14** and **#12** (by removal — they describe invariants that no
longer exist), **#56** (all three items), and 🟡 F itself.
`tests/test_ledger_stamps_resolve.py` and `tests/test_evidence_check_hardening.py`
are gone, their surviving properties folded into cases that run no git.

## Deferred, and to where

| What | Where |
|---|---|
| 🟡 C — a row reached through `--map` cannot clear its verdict from any header | superseded by the redesign; confirm at the follow-up rather than assuming |
| 🟡 E — `templates/evidence-check.yml` advises starting without `--strict` on the line above the one that ships it | still open, template-facing |
| Renaming a symbol reads as BROKEN rather than as a rename | a new class of red that did not exist before. Honest — the checker cannot know the new name is the same thing — and recorded in the skill's Known limits |

## Executed probes

| What was run | Result |
|---|---|
| the four ledger test files, as shipped | 62 passed at round 3, 64 after `2d56812` |
| four narrowed mutations over 🟡 A and 🟡 B | each kills exactly its own case; as shipped 64 passed |
| squash simulation, `test_ledger_stamps_resolve.py` · `test_a_rider_reaches_its_file.py` | 3 passed · 8 passed |
| `git log -L` on the fragment at `12e2ee4` and `f3a52e9` | `9cc7aaf` against `f3a52e9` — an in-place rewrite is not a new line, removal-then-write is |
| future-fragment probe | the fragment guard goes red pre-squash; the old file's case stays green — the lead corrected |
| the redesign's five proofs and 13 mutations | above |
| orchestrator, after the redesign | `41 ok · 0 drifted · 0 broken · 0 external`; zero `path:line` and zero SHA-shaped tokens across both ledgers; `evidence_check.py` 372 lines with no git reference |
