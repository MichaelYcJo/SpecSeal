# Implementation Plan: 1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

Apply round 3's paste-ready fences for 🟡 9 and ⬜ 10 of work item 1791019475,
plus one docstring the fences did not reach (`spec.md` S4). The work splits
into a rule's text and its checks:

| Edit | Kind | Why it is that kind |
|---|---|---|
| the §*Which tree* sentence (S1–S3) | rule text | the sentence a person reads to learn when the guard asks |
| `switch_kind`'s docstring (S4) | rule text | a second statement of the same words, for the reader of the code |
| the pin (C1) | check | asserts the sentence; red when it changes |
| three `KINDS` rows (C2) | check | binds `switch_kind` to the sentence's three words; green at the base on purpose |
| the rule case's `judged=set()` and `frozen` (C3) | check | makes an existing clause able to fail |
| changelog fragment, ledger fragment | records | `docs/the-record-layout.md` |

**One phase, no split.** The rule text and its pin must land in one commit
(contract §14), so they cannot be two phases. C3 is independent but is a
dozen lines in the same module, and a phase boundary there would hand nothing
to a next phase. Two commits inside the phase keep the two findings apart in
the history the reviewer reads.

## Technical context

- `docs/worktree-guard-spec.md` lines 631–633: the sentence, inside one
  wrapped paragraph of §*Which tree, when the command walks to it*. The
  reviewer's fence replaces three lines and the start of the fourth; the
  paragraph is re-wrapped, so `_policy_text()`'s whitespace folding is what
  lets the pin match across the wrap.
- `hooks/worktree-guard.py#switch_kind` (lines 290–317): unchanged in
  behaviour. Its docstring's "so every `checkout` with a name in it counts"
  becomes a statement that matches: a `checkout` with `-b`/`-B`, or one with
  no `--` naming `-` or a word other than `.`. Exact wording is the
  builder's; it must not contradict the corrected sentence.
- `tests/test_guard_resolves_the_tree_it_judges.py`:
  `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` (1251),
  `KINDS` (1315, insert after the `"checkout with no name"` row at 1327),
  `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`
  (1204, the block at 1219–1229). The fences in the round-3 report are
  exact for the base `e141980a`.
- C3 reaches `wg.wide` (the `cmdline` module the guard imports as `wide`)
  for `drop_heredoc_bodies`, `drop_comments` and
  `split_segments_with_separators`, the same three calls `wider_only_kinds`
  makes, so the case's `frozen` is built from the same segments the views'
  sources are.

**What breaks in six months.** The pin is a string, so it catches the
sentence changing and not `switch_kind` changing. The `KINDS` rows catch the
second, but only on the words they name: a new clause added to `switch_kind`
with no row and no sentence change passes both. The rule case
(`test_every_shape…`) still uses `switch_kind` as its own oracle, so it
cannot see that either. That residue is accepted here (alternative 3 below
says what closing it would cost).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| 1. The reviewer's sentence, pin and three `KINDS` rows, verbatim, plus the docstring | the six-month residue above | **chosen**. Verified by the reviewer against `switch_kind` over 2,859 generated commands (0 differ) and green in five modules; the frame re-checked every fence against the base by reading |
| 2. Reword "naming a word" to "naming a word that does not start with `-`" | the pin text then differs from the one the reviewer verified, and the change is judged by reading only. The existing sentence already contrasts "a word" with `-` and `-b`/`-B`, and `KINDS`' `switch with no target` (`--detach` → `None`) binds the code side | rejected; a reviewer who reads "a word" as including an option can overturn this by opening the sentence |
| 3. Plant the reviewer's re-implementation of the sentence as a predicate, compared with `switch_kind` over the generator | a second hand-written copy of `switch_kind` that reads neither the sentence nor the code; it drifts from both and, when red, does not say which side moved. Every clause already has a `KINDS` row (`spec.md` table) | rejected; the clause-by-clause rows are the cheaper equivalent |
| 4. Put the pin in a new case named for the word list | one more case for one assert; the host case already pins this paragraph's other three sentences and its docstring covers "the sentence a person reads to learn when the guard asks" | rejected; the reviewer's placement is kept |
| 5. Leave `switch_kind`'s docstring | the class (contract §12) left one instance standing, in the place a reader of the code meets first | rejected; the docstring drifts released row K5 (`spec.md` *Data & interfaces*), which one `Re-read ·` row answers |
| 6. Fix C3 by asserting `wider_only_kinds(..., judged=set())` equals the default's result | tests the default, not the per-view subtraction the clause exists for | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | Commit A: S1–S4 + C1 + C2 (the sentence, the docstring, the pin, three `KINDS` rows). Commit B: C3 (the rule case's `frozen` clause). Then the records: `changelog.md` fragment (one `### Fixed` bullet, no `## ` line), `seal/ledger/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks.md` with one new row (the sentence ↔ `switch_kind` ↔ C1/C2 coordinates) and the `Re-read ·` rows for K7, `Re-read · M2` and K5 by `bin/evidence-check --reverify --into … --checked <date>` after reading each, and `overview.md` | `spec.md` A2–A7, each executed: the pin red at the base sentence; each new `KINDS` row red against its mutant; the rule case red against the `if kind:` mutant; the five modules green; `evidence-check --strict .` exit 0; `survivor-check --range e141980a...HEAD` clean or excused. Mutants reverted, no `test_tmp_*` left. The broad gate is the sealer's | |

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
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

None. No migration, no environment variable, no dependency, no behaviour
change in any hook. The guard asks exactly what it asked at `e141980a`.
