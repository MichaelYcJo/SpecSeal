# a tracked file the tree deleted stops the sweep — questions for the planner

<!-- seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

## What the tickets left open and the tree answered

A reader cannot tell a judgment that was decided from one that was never met,
so the decided ones are listed here with where the grounds are. Nobody should
reopen one without opening what it was decided against.

- **How far the class reaches.** Neither ticket enumerates it; #432 says
  *there are two callers here and the same helper shape exists elsewhere* and
  asks for the check to be made. Answered from the tree: **five helpers, seven
  opening call sites**, table in `spec.md` §*The reach, enumerated from the
  tree*, with the three shapes that are immune by construction and the two
  that already guard named beside it.
- **Whether a skip weakens the no-real-identifiers rule.** Answered in
  `spec.md` §*Is a skip a weakening*, in both directions, and the answer is
  not the one either ticket assumed: in the positive direction it cannot be a
  weakening, because today the same tree produces no verdict at all; in the
  INVERSE direction a bare skip buys two false alarms, at
  `tests/test_no_document_names_the_old_roots.py:142` and
  `tests/test_a_script_says_which_interpreter_it_needs.py:524`.
- **Silent skip or counted skip.** #282 offers three options and leaves the
  trade open. Answered: counted, and a case whose verdict needs the whole
  corpus declines to judge rather than judging wrongly, which is
  `pytest.skip` with a reason. The grounds are the two false alarms above and
  `seal/follow-up.md`'s first row.
- **The guard's home — the helper or the call sites.** Answered: the helper.
  #432 gives the first reason; the second is the ledger, since three of the
  five helpers carry no anchor while several call sites do, so the helper is
  also the cheaper home.
- **Whether `docs/release-checklist.md` gains a row in its table of what each
  check has caught.** Answered: no. That table is for recognising a failure
  instead of debugging it, and after this work the failure cannot occur. What
  the reader will meet is the skip count, so step 3's preamble gains one
  sentence instead.
- **Whether this work is the prerequisite a `seal/follow-up.md` row waited
  on.** Answered: no row was, all eleven read on 2026-09-18, grounds in
  `spec.md` §*Whether a `seal/follow-up.md` row was waiting on this*.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should a path missing from disk have its INDEX content swept, instead of being skipped? | **a person** | **Skip it** — one predicate per helper, the shape both tickets propose. The staged-then-removed state stays unswept: a file `git add`-ed with a real domain in it and then removed from disk without staging the removal ships that content if the index is committed. That state is unswept today as well, because today the sweep crashes on the same tree. · **Read the index for it** — one `git cat-file --batch` over the missing set, and the corpus never shrinks. It closes that hole, and it costs a second content source plus a message that has to say which one it read, in all five helpers. Why this is a person's and not a measurement: `CLAUDE.md` says both incidents that forced a history rewrite entered through this rule, so how much the rule is asked to guarantee is a value somebody has to be accountable for | **Skip it.** The build proceeds on this and phases 1 and 2 are written for it; answering *read the index* changes phases 1 and 2, not the rest | ⬜ |
| Q2 | How many paths does a fold actually leave missing, and does the counted skip equal that number? | a measurement | One run of `python3 .github/scripts/fold_ledger.py --dry-run --version X.Y.Z` names the fragments it would remove; the skip count phase 1 prints is read against it. It settles whether the reason strings are the right grain — one line per path, or a count — before `agent-contract` §14 pins them | The reason names every skipped path individually. A count alone is what `seal/follow-up.md`'s first row calls a claim removed without a word | ✅ **Answered 2026-09-18 by phase 3.** A fold removes one file per ungathered ledger fragment — one today, named by `fold_ledger.py --dry-run`; `gather_changelog.py` removes nothing. The counted skip does **not** equal it in the runner's count line: on that tree the six modules print `84 passed, 0 skipped`, because only `tracked_text_files` reaches `seal/ledger/` and both its callers are sweeps that judge what remains. The grain stays one path per reason, for the three cases that do decline |
| Q3 | Beyond the two enumerated, does any case in the five modules read the corpus to prove something is still ALIVE? | the work | Phase 3 reads every case in the five modules for a verdict that depends on the corpus being whole. `tests/test_release_hygiene.py`'s exemption-list cases were read on 2026-09-18 and are positive sweeps, but the module has the most cases of the five and the reading was not exhaustive | The two named in `spec.md` are the whole list. A third found in phase 3 is repaired in that phase and recorded, not carried back here | ✅ **Answered 2026-09-18 by phase 3.** Three, not two. The third is `tests/test_no_document_names_the_old_roots.py#test_the_scan_covers_something`, repaired in phase 3's commit. Nothing else qualifies: only `timer_offenders` consumes the corpus in `test_release_hygiene.py` and it is a positive sweep, and that module's exemption cases read named files directly |
| Q4 | Is #432's *staging the deletions makes the same tree green — 3736 passed* true, and is it this suite's present pass count? | a measurement | The figure is a ticket's aggregate, which `agent-contract` §5 says is not a coordinate. Phase 1 records the module's baseline before it edits anything, and phase 5's broad gate records the suite's. If the number is stale it is corrected in `overview.md` rather than carried | Carried as unverified, answered by phase 1's baseline | ✅ **Answered 2026-09-18 by the work.** The module's baseline is **2 passed** and it stands at **5 passed**. #432's *3736 passed* is a suite-wide aggregate; it is carried unverified to the sealer's broad run and named in `overview.md` §*Not verified* rather than repeated anywhere |

**`Who can answer` takes one of three values and nothing else.** A person's row
is the only kind that blocks the build; a measurement is settled by running
one thing, and queueing it behind a person is the wrong instrument; the work's
row is decided by the phase that meets it.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
