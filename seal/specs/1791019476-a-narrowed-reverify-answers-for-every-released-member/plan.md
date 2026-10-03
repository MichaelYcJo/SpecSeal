# Implementation Plan: a narrowed `--reverify` answers for every family a file it read holds a member of (#740)

<!-- seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/plan.md
     The decisions D1–D5, the scenarios S1–S9 and the enumeration are in
     spec.md; this file says in what order they are built and how each phase
     is shown. -->

Approved 2026-10-03 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

There are three phases, and the class comes first.

1. 🟡 16 is planted as an enumeration over where a family's members sit, and as the two cases round 3 asked for. Each is seen red, then one filter in `released_drift` changes, and the home sentence and the changelog follow.
2. ⬜ 17 is one message, pinned and documented.
3. The ledger is made true under the freeze, and the surviving-wording sweep runs over the whole range.

## Technical context

**What this builds on.** Every unit below was read at `2b1dcb1f`, in
`skills/evidence-check/scripts/evidence_check.py` unless another file is named.

- **`#released_drift`.** It builds `wanted` from the released files among LEDGERS. A first loop grades released rows outside every family. A second loop walks `view.readings` and skips a family with `if top[0] not in wanted`. That filter is the one site keyed on a family's root file: `git grep 'top\[0\]'` over `*.py` returns it alone.
- **`#family_view`.** It returns `families`, `{root: [members]}`, which holds every member including the root, and `readings`, which holds only the families that are not superseded.
  - The emission loop applies the newest-reading rule. A reading that is OK but outranked becomes DRIFTED with "matches only the reading of {checked(key) or 'no date'}". This is ⬜ 17's site.
  - The `checked` helper returns `""` for a date `calendar_date` rejects, which is why an invalid date reads as "no date".
- **`#main`, the `--reverify` branch.**
  - Without the freeze, it calls `reverify(ledgers, …)` and then `released_drift(ledgers, view, …)`, and prints `LEFT` per owed root.
  - Under the freeze, it re-stamps the `writable` fragments and then calls `reverify_into(released, view, into, …)`. Only `released` reaches `released_drift` there, so a narrowed fragment is never in `wanted`. D2 changes this argument.
- **`#reverify_into`.** It writes nothing but INTO. It cites the family's root (`citation_for` on the key) and slices each coordinate from the line its match came from, so any member's match is usable.
- **`#built_name`.** It prints `/` on every platform, so a `LEFT` line's path compares the same on Windows. The test module's `run` already decodes UTF-8, and its fixture writers pass `encoding="utf-8"`.
- **`tests/test_a_released_row_is_read_again_in_a_fragment.py`.** It is 1,366 lines, with the helpers `released`, `fragment`, `citation`, `frozen`, `digests`, `unit_hash` and `edit_handler`, and the `INTO` constant. Round 2's siblings, `test_a_narrowed_into_re_reads_a_family_a_fragment_outranks` and `test_an_unfrozen_narrowed_reverify_names_a_family_it_could_not_clear`, are the template for S1 and S2.

**Constraints.**

- **No `git stash`.** A case is seen red by reverting the one filter line with `Edit`, or by running it against `git show 2b1dcb1f:skills/evidence-check/scripts/evidence_check.py` saved to a scratch path. Never by stashing.
- **Every file read and write in a new case passes `encoding="utf-8"`.**
  - A printed path is compared in POSIX form.
  - A path a test builds and then compares with output is normalised with `.replace(os.sep, "/")`.
  - Windows CI failed #736 on both (`c3f8215a`, `bb86e305`).
- **Fixtures use neutral values only** (`tests/test_no_real_identifiers.py`).
- **`evidence-check` makes no git call** (`tests/test_a_row_points_by_content.py#test_the_checker_asks_git_for_nothing`).
- **Narrow runs only.** Run the modules the phase touched. The broad gate belongs to the sealer (agent contract §2).

**Failure direction.** The change makes a narrowed `--reverify` report more:

- more `LEFT` lines;
- exit 1 where it exited 0;
- rows written under the freeze where none were.

A wrong report costs one re-read. A wrong silence, which is today's behaviour, lets a narrowed run say nothing while the same narrowed `--strict` fails, and the person who narrowed as the home tells them to finds out at the broad gate. The noisier direction is the cheaper one.

**What breaks in six months, for the chosen approach.**

1. **A new placement of a family member.** A third citing verb, or a member kind `ledger_kind` returns `None` for, would add a value to the M or N axis that the product does not hold. The enumeration names its axes in its docstring, so the next verb's author can see where to add one.
2. **The product's runtime.** 72 cells of three subprocess runs each sit in a module the suite already runs. If it is slow under `bin/test`, M2 says how to cut it without losing a cell kind.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Membership over every ledger read (D1, D2), with an invariant asserted over the full product** | The fragment cell widens the ticket's *released member* wording (questions.md Q1). Runtime grows by up to 216 subprocess calls (M2) | **chosen** |
| Round 3's paste-ready fix: membership over released members only, collected from the graded readings | It leaves the fragment cell open: a narrowing to a fragment holding an outranked older re-read exits 0 while the narrowed `--strict` reads it DRIFTED. That is the same class, one file kind over, and agent contract §12 is the rule it breaks | rejected |
| Keep the filter on the root, and make the narrowing notice say that families rooted elsewhere were not answered | It changes the home's promise instead of keeping it. A person narrowing to the release file they re-read gets a sentence where they needed the row written | rejected |
| Refuse `--reverify --ledger` whenever a family crosses the narrowing | It stops the documented workflow, "narrow the write with `--ledger` to the files you read", for every family with members in two files, which after a fold is most of them | rejected |
| Pin only the two report cases | The two cases are the instance. #736's fix pass probed 32 narrowing variants by flag and missed this one, because the axis that mattered was where the members sit. Examples by flag are what missed it | rejected |
| A new test module for the enumeration | Its helpers live in the existing module, and copying them makes two fixture builders to keep in step. No size ceiling applies to `tests/` (`templates/config.md`: `Document line ceiling` covers top-level `docs/*.md`) | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | 🟡 16, built in this order. **(a)** In the test module, the enumeration case over spec §*The class, enumerated*, asserting S4's invariant per cell, plus the superseded-family control cell. **(b)** The report's two cases as S1 and S2 (spec), named for what they hold. **(c)** All of them seen red against `2b1dcb1f`'s filter, with the red cells listed in `phases/phase-1.md`. **(d)** The fix: `released_drift`'s filter tests `view.families[top]` against the identities of all of LEDGERS; the first loop stays released-only; the docstring is rewritten (round 3's text, widened to "a file LEDGERS names"); `main`'s freeze branch passes the full narrowed list to `reverify_into`, whose docstring follows; and `main`'s no-freeze comment is rewritten. **(e)** The home's **Without the row** sentence (spec S7). **(f)** The changelog fragment's first `### Fixed` entry | the new cases red at the old filter and green after (executed); `tests/test_a_released_row_is_read_again_in_a_fragment.py`, `tests/test_two_branches_re_read_one_released_row.py`, `tests/test_a_merge_cannot_silently_drop_a_correction.py`, `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`, `tests/test_the_ledger_rules_have_one_home.py` and `tests/test_docs_line_wrap.py` (executed, narrow) | 72a9c90a |
| 2 | ⬜ 17: the S6 case pinning both substrings, seen red against the old wording; D5's three forms in `family_view`'s emission loop; one sentence in the home's family paragraph saying that a `Checked` date the calendar does not have orders nothing and is named as written; the changelog's second entry | the case red then green (executed); the test module, `tests/test_the_ledger_rules_have_one_home.py` and `tests/test_docs_line_wrap.py` (executed, narrow) | 62aa88a6 |
| 3 | The ledger under the freeze. L4 in `seal/ledger/1790993138-….md` gets its claim corrected in place with a `Corrected <date>` note: the deferred clause goes, and the clause says what D1 and D4 do. This work item's own rows go into `seal/ledger/1791019476-….md`: N1 for the narrowed family answer and its enumeration case, N2 for the invalid-date message. Then `evidence-check --reverify --into seal/ledger/1791019476-….md --checked <date>`, after reading every row citing a drifted coordinate: the released rows citing `#main` and the #736 fragment rows citing the edited units. Then `bin/survivor-check --range 2b1dcb1f...HEAD`, with anything kept judged in this directory's `survivors.md` | `evidence-check --strict .` reads 0 drifted (executed); `git diff --name-only 2b1dcb1f...HEAD -- seal/releases seal/ledger.md` is empty (executed); survivor-check's output read in full (executed); `tests/test_no_real_identifiers.py` and `tests/test_one_word_one_meaning.py` (executed, narrow) | e7c09bf7 |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
**Re-read the column after any rebase**, or it names commits that resolve in
one clone and nowhere else.

## Operational impact

- **No migration, no new environment variable, no new dependency, no new flag.**
- **Behaviour change for an installed copy.** A narrowed `--reverify` can now exit 1, or write rows under the freeze, where it exited 0 having done nothing. A script that narrows `--reverify` and treats exit 1 as failure will see it in exactly the cells where `--strict` with the same narrowing already failed.
- **Ordering in 0.18.0.** #736's fragment is folded into `seal/releases/0.18.0.md` at the release. L4 is corrected while it is still a fragment, so this branch must land before the 0.18.0 fold. If the fold lands first, L4 becomes a released row, and the correction becomes a `Corrected ·` row in this work item's fragment that cites it. W2 holds that branch.
