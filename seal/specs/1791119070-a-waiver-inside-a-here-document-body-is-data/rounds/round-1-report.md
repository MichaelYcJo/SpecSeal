# Round 1 report — a waiver inside a here-document body is data (#773)

| Field | Value |
|---|---|
| Work item | `1791119070-a-waiver-inside-a-here-document-body-is-data` |
| Target | PR #783, branch `fix/773-a-waiver-inside-a-here-document-body-is-data`, `b414c720` |
| Base | `release/v0.18.2` at `94d7b2e0` |
| Round | 1 (a finding round: spec compliance, then quality) |
| Ran by | specseal:warden on claude-opus-5-5 |

Worked in a `git clone --no-local` of the worktree at `b414c720`, under the
session scratchpad's directory for this work item and round. Nothing was
written in the worktree but this file. Every command shape below is described
in words; the strings live in the test modules named beside them. No command
that commits was run, here or in the clone; every verdict below comes from the
gate's decision functions called from Python, or from the hook's `main()`
driven the way the suite drives it.

## Summary

The change does what `spec.md` asks. Both consent reads on the commit gate's
path now leave here-document bodies out. No third read on that path was
missed. The direction claim holds by the structure of the code, not only on
the cases. The seven new red-first cases are red against the base hooks and
green at the target, and I reproduced that myself. The two plan corrections
are right. Nothing found needs a fix. The four findings are all ⬜: one
redundant branch that can never be pinned, and three wording or efficiency
points.

## Stage 1 — spec compliance

### (1) Both consent reads leave the bodies out, and there is no third read

**Read.** `hooks/commit-review-gate.py:686` makes `has_marker` the AND of two
scans: `_reads_marker` over the command as written, and `_reads_marker` over
`tokens.without_bodies(command)`. Its two call sites, `judge` at
`hooks/commit-review-gate.py:1122` and `main`'s unreadable branch at
`hooks/commit-review-gate.py:1418`, both pass the raw command. That is right,
because `without_bodies` applies `one_heredoc.reduce` itself.
`hooks/tokens.py:86` makes `given` the intersection of the bare words of the
raw command and the bare words of `without_bodies(command)`.

**The class, enumerated by construction from the token tables.** I grepped
every hook, `bin/` and `skills/` script for the two commit-gate tokens and for
`gate.TOKENS`, `tokens.KNOWN`, `tokens.given` and `tokens.words`. A waiver on
the commit gate's path reaches a decision in exactly these places:

| Where the decision is made | What it reads | Command text read? |
|---|---|---|
| `judge` and `main` in `hooks/commit-review-gate.py` | `has_marker` | yes — in scope, fixed |
| `hooks/answer-write.py` | `tokens.given` | yes — in scope, fixed |
| `hooks/commitgate.py#waived` (the git hook) | `answers.given` over the stored token files, and `git config --get-all specseal.waive` | no. `answers.write` (`hooks/answers.py:134`) writes only the tokens `given` handed it, and `answers.given` matches the stored command against the hook's ancestry argv (`hooks/answers.py:186`). It reads no token out of text |

`tokens.steps_around_hooks` and `tokens.is_plain` also read the raw command,
bodies included. They are not consent reads: they decide whether the
PreToolUse reading stands aside, and reading more there keeps the reading in.
`hooks/worktree-guard.py#has_token` is the same class at another gate, and it
is out of scope. #780 is filed and open, and `overview.md` *Not done* names it.

**Overview's *Not verified* item 1, answered by reading.** The overview asked
whether a body token could still reach the git hook end to end. It cannot.
`given` is the only producer of what `answers.write` stores, and
`commitgate.waived` reads only what was stored plus git's own config. So the
unit rows in `tests/test_the_old_spellings_reach_the_hook.py#test_a_token_is_a_bare_word_and_nothing_else`
cover the whole path. One fact makes this path matter: a sink-less `cat` fed a
heredoc, followed by a plain commit, is a shape `tokens.is_plain` accepts. In a
clone where git decides, `given` is therefore the only consent read for such a
command.

### (2) The direction claim holds by structure

**Read.**

- `has_marker` is `base AND X` (`hooks/commit-review-gate.py:686`), so it
  implies the base read. `given` is `base ∩ X` (`hooks/tokens.py:86`), so it is
  a subset of the base read. Neither depends on what X computes.
- Every consumer is monotone in the waived set:
  - `gate.arms_missing` adds an arm exactly when that arm is *not* in `waived`
    (`hooks/gate.py`, the two `not in waived` conditions).
  - `main`'s unreadable branch fires on `not has_marker`
    (`hooks/commit-review-gate.py:1418`).
  - `commitgate.waived` adds only the arms whose files were written.
- So a smaller waived set can only add a stop. The one place where a stop can
  change form is a target set holding both an unreadable target and a readable
  target that stands on its parity arm. There the base took the readable
  target's deny-or-ask, and the new read takes the unreadable branch's
  deny-or-ask. Both are stops, so this is a stop turning into a stop, never
  silence.
- **The one way the direction could still invert is an exception.**
  `hooks/dispatch.py:21` skips a gate that raises, and a skipped commit gate is
  silence. That is the comment at `hooks/commit-review-gate.py:1302`.
  `has_marker` now runs `one_heredoc.reduce`, `drop_heredoc_bodies` and a
  second `split_segments` on text the base never handed them. **Executed:** a
  fuzz of 60,000 random strings built from shell-significant pieces raised
  nothing from `has_marker` or `given`, and found no string where either new
  read honours a token its base read did not. By reading,
  `_heredoc_split` is a single iterative pass, `_heredoc_word` is bounded, and
  `words` catches the lexer's `ValueError`.

### (3) M2 — the `reduce` half is equivalent, not merely unpinned

**Executed.** I took every string in
`tests/test_one_heredoc_shape_agrees_with_the_shell.py#corpus` and
`#program_corpus`, and built variants with the token placed on each body line
in five spellings: bare, after a word, appended to the line, in a comment, and
single-quoted. That gave 13,308 strings `reduce` admits. For every one of
them, two things held:

- `drop_heredoc_bodies`' text, with the opener's ` <<'D'` removed, equals
  `reduce`'s text up to trailing newlines.
- `_reads_marker` and the known-token set from `_bare` agree between the two
  texts.

**Read — why it is structural.** Clause B's grammar admits no `#` outside a
quoted word, no `$`, no `(` and no backslash on line 1. So `_heredoc_split`
ends line 1 in its neutral state and takes `D` for the delimiter. Clause A
bans the carriage return. Clause C makes the terminator the first line
exactly equal to `D`, which is the same comparison `_heredoc_split` makes.
Clause D leaves no other `<<`. The two readers therefore remove the same body
and differ only by the redirect and its delimiter word, and no consent read
can turn those into a waiver token. The branch is therefore not dead code (it runs) but
redundant, and that is ⬜ 1 below.

### (4) The two plan corrections

**Read.**

- G6: `seal/releases/0.17.0.md:77` cites the `hooks/tokens.py#given` anchor at `e436fefe`. The
  corrected sentence in `plan.md` §*Operational impact* states that hash for
  that anchor and row. **Correct.**
- `classify`: `hooks/cmdline_base.py` holds no `classify`. Sibling D's branch
  (`fix/764-…`) edits `hooks/worktree-guard.py#classify` and `#switch_kind`,
  and touches no other hook file. **Correct.** Two leftovers sit in the same
  class (⬜ 2): `spec.md:79` still names the old coordinate, and the
  correction's own wording, "the only `classify`", is false.
- I checked the plan's counts on the same list: seven rows of
  `seal/releases/0.18.1.md` cite `main` at `553b6500`, and `commit_invocations`
  at `1cf73673` is cited once by `seal/ledger.md`, five times by
  `seal/releases/0.16.0.md` and once by `seal/releases/0.18.1.md`. All hold.

### Scenarios S1–S7

**Executed.** I ran both hook files as they stood at `94d7b2e0` over the target
tree, then restored them. Seven cases were red, each on its verdict assertion:
S1, the three S2 openers, S5, and `given`'s two body rows. Seventeen were
green, including S3's four forms and S6. At `b414c720` the two touched modules
gave 306 passed. That matches `phases/phase-1.md` §*How red was shown*.

**Read.**

- S7: both `Enforced by:` lines name the new cases. The four comments no
  longer say the consent read sees the whole command.
- S6 is a loop rather than a parametrized case, which is a form difference and
  not a gap.
- `spec.md` case 5, the over-drop, has no pin, and the overview hands that to
  this round. My answer: it should stay unpinned. A pin would hold a splitter
  imprecision in place, and the first fix to `_heredoc_split` would have to
  delete it. My one attempt to build a case-5 input, an ANSI-C-quoted word
  ahead of a line carrying the token, did not over-drop. So whether case 5 is
  reachable is unshown either way (⬜ 3).

## Stage 2 — quality

### ⬜ 1 — `without_bodies` carries a branch no case can ever tell apart

`hooks/tokens.py:74`. On every string the one-shape reader admits, the
`reduce` branch gives the same consent outcome as `drop_heredoc_bodies`
alone (stage 1 (3)). So M2 survives by construction, not for want of a case.

What keeping it costs:

- a mutant that every future `mutation-check` run reports as surviving;
- a docstring that reads as if the two readers differ;
- one more regex match per call, which is negligible.

What it buys: the consent reads stay tied to the commit reading's text for
that shape even if `_heredoc_split`'s boundaries move. That is the frame's
stated reason, and it is real.

The fix is to say so in the docstring: equivalent today, kept as a guard
against drift in the splitter. Removing the branch would also be correct.
Neither changes behaviour, and no release ships a defect either way.

### ⬜ 2 — the coordinate correction left two instances behind

Both sit in `seal/specs/`, so this is paperwork and a correction.

- `spec.md:79`, in §*Out*, still says sibling D edits a `classify` in
  `cmdline_base.py`. This is the same wrong coordinate phase 2 corrected in
  `plan.md`. The checker cannot catch it, because a bare file name before `#`
  resolves to nothing and `classify` is then read as a bare name that the tree
  carries.
- `phases/phase-2.md:39-40` and `overview.md:20` both say the only `classify`
  is `hooks/worktree-guard.py#classify`. `hooks/dispatch.py#classify` exists
  too (`hooks/dispatch.py:207`).

The fix:

- Reword `spec.md:79` the way `plan.md`'s sentence was reworded.
- In the other two places, write "the `classify` beside `switch_kind`" in
  place of "the only one".

### ⬜ 3 — the changelog counts one new stop, and the spec names two

`changelog.md:14` says "One stop is new" and describes case 4. `spec.md` case 5
is a second way a waiver the base honoured is now refused: text the splitter
takes for a body and the shell does not. It is rare, and I could not build
one, but the spec states it as real. A person who meets it would find no
changelog line explaining the stop.

The fix: one clause in the changelog saying that a token after text the gate
wrongly reads as a heredoc can also be refused, with the same way on (the
token on the first line, or the git-native spelling). This is paperwork.

### ⬜ 4 — `has_marker` recomputes the body-free text on every call

`hooks/commit-review-gate.py:686` calls `without_bodies(command)` per marker.
`judge` calls `has_marker` once per arm for every target
(`hooks/commit-review-gate.py:1122`), and `main` calls it once more
(`hooks/commit-review-gate.py:1418`). So one Bash call re-runs `reduce`,
`_heredoc_split` and `split_segments` over the same text 2N+1 times for N
targets. Each pass is microseconds on a command-sized string, so this is
cleanup and not a defect. If anyone touches the function again, computing the
body-free text once per command and passing it in is the cheaper shape.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `without_bodies`' `reduce` branch is equivalent to `drop_heredoc_bodies` on every admitted string, so M2 survives by construction; the docstring does not say so | `hooks/tokens.py:74` | open | Executed: 13,308 admitted variants, zero text or verdict differences. Read: clauses A–D of `hooks/one_heredoc.py` leave `_heredoc_split` in its neutral state at the opener's newline with the same delimiter and the same terminator test |
| ⬜ 2 | The `classify` correction left `spec.md:79` naming the old coordinate, and phase 2 and the overview call worktree-guard's `classify` "the only" one while `hooks/dispatch.py:207` holds another | `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/spec.md:79` | open | Read: grep for `def classify` over `hooks/`. Paperwork, a correction |
| ⬜ 3 | The changelog says one stop is new; `spec.md` case 5 is a second | `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/changelog.md:14` | open | Read against `spec.md` case 5. Paperwork, a correction |
| ⬜ 4 | `has_marker` recomputes `without_bodies` per marker and per target | `hooks/commit-review-gate.py:686` | open | Read: call sites at `:1122` (per arm, per target) and `:1418`. Cleanup only |
| 🟢 | Both consent reads on the commit gate's path leave here-document bodies out, and the class holds no third read | `hooks/commit-review-gate.py:686`, `hooks/tokens.py:86` | confirmed | Read: every reader of the two tokens enumerated from `gate.TOKENS` and `tokens.KNOWN`; `commitgate.waived` reads stored files and git config, not text. Executed: the new cases are red at the base hooks and green at the target |
| 🟢 | The new reads can only refuse, by structure | `hooks/commit-review-gate.py:686`, `hooks/tokens.py:86`, `hooks/gate.py` `arms_missing` | confirmed | Read: AND and intersection with the base read, and every consumer monotone in the waived set. Executed: 60,000-string fuzz, no exception and no newly honoured token |
| 🟢 | The two corrected `plan.md` coordinates are right | `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/plan.md` §*Operational impact* | confirmed | Read: `seal/releases/0.17.0.md:77` cites `given` at `e436fefe`; sibling D's branch edits `hooks/worktree-guard.py#classify`; `hooks/cmdline_base.py` has none |
| 🟢 | A body token cannot reach the git hook end to end | `hooks/answers.py:134`, `hooks/commitgate.py:83` | confirmed | Read: `answers.write` stores only what `given` returns, and nothing downstream reads command text for a token |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` and `tests/test_the_old_spellings_reach_the_hook.py` at `b414c720`, in the clone | 306 passed |
| The same two modules, `-k` on the S1/S2/S3/S5/S6 cases and `test_a_token_is_a_bare_word_and_nothing_else`, with `hooks/tokens.py` and `hooks/commit-review-gate.py` checked out at `94d7b2e0` over the target tree, then restored | 7 failed (S1, the three S2 openers, S5, `given`'s two body rows), 17 passed |
| A pure-function probe (one temporary test file, run once, deleted): for 13,308 admitted variants of `corpus` and `program_corpus` with the token on each body line, compare `reduce`'s text with `drop_heredoc_bodies`' text with the opener's redirect removed, and compare `_reads_marker` and the known-token sets between them | 0 text differences, 0 verdict differences |
| The same probe: 60,000 random strings from shell-significant pieces, seed 773; call `has_marker` and `given`, and compare each with its base read | 0 exceptions; 0 strings where a new read honours a token its base read did not |
| The same probe: one hand-built case-5 attempt, an ANSI-C-quoted word ahead of a line carrying the token | no body found; both reads keep the token, as at the base. Case 5 not reached |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet — not run by anyone at this SHA; it belongs to the sealer, once the rounds settle |

Needs a fix: no
Loses a record or crashes: no

Nothing here is open that needs a fix, so the broad gate comes due: what is
due is the sealer's spawn, after this round's ⬜ rows are answered or left.

## Proof block

Files opened in this round, at `b414c720` unless noted:

- `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/`:
  `spec.md`, `plan.md` (and its diff from `cdd9c7ac`), `questions.md`,
  `phases/phase-1.md`, `phases/phase-2.md`, `overview.md`, `changelog.md`
- `seal/ledger/1791119070-a-waiver-inside-a-here-document-body-is-data.md`
- `seal/releases/0.17.0.md` (row G6), and a grep of `seal/releases/*.md` and
  `seal/ledger.md` for the `main` and `commit_invocations` anchors
- `hooks/tokens.py`, `hooks/commit-review-gate.py` (`commit_invocations`,
  `has_marker`, `_reads_marker`, `judge`, `main`), `hooks/one_heredoc.py`,
  `hooks/cmdline.py` (`drop_comments`, `_heredoc_word`,
  `drop_heredoc_bodies`, `heredoc_bodies`, `_heredoc_split`,
  `split_segments`), `hooks/answer-write.py`, `hooks/answers.py`,
  `hooks/commitgate.py` (`waived`), `hooks/gate.py` (`arms_missing`),
  `hooks/dispatch.py` (header and `GROUPS`), `hooks/routing.py` (`parse`'s
  docstring)
- `docs/commit-review-gate-spec.md` and `docs/the-commit-gate-inside-git.md`
  (the diff hunks)
- `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`,
  `tests/test_the_old_spellings_reach_the_hook.py`,
  `tests/test_a_gate_that_fails_says_so.py` (the diff hunks), and
  `tests/test_one_heredoc_shape_agrees_with_the_shell.py` (`corpus`,
  `program_corpus`)
- sibling D's branch `fix/764-…`: `git diff --stat` and hunk headers under
  `hooks/` against `94d7b2e0`
- `bin/test`, `bin/survivor-check` (headers)
