# Implementation Plan: 1788305134-the-reader-stops-where-it-need-not

<!-- specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

## Summary

Re-apply the two reader fixes from a branch that lost its history, close the
four 🟡 its round 2 left open, and prove the part of it nobody reviewed. The
re-application turned out to be a verification: the tree at the branch point
already carried the whole change plus a later, unreviewed aimed reset. The
aimed reset was measured against bash and found to open a class of fail-opens
the wide reset had closed by accident; that class is closed by a body count
beside the name environment, and the run that found it is recorded so the
next reader can re-run it.

## Technical context

| Coordinate | What it gives this work |
|---|---|
| `hooks/cmdline.py#walk_directories` | The loop that threads `states`, `parked` and `env` across segments. `depth` joins them there |
| `hooks/cmdline.py#_unseen` · `#_runs` · `#OPAQUE` · `#LOOP_WORDS` | The aimed reset — the code round 2's 🟡 3/4/5 asked for, present at the branch point and reviewed by nobody. The unit this item had to prove |
| `hooks/cmdline.py#_bind` · `#_forget` | What a segment inside a body must do instead of binding: `_forget` drops every shape `_bind` takes or unbinds |
| `hooks/cmdline.py#understood` | The acceptance test both halves share. It asked the reserved-word question of the first token only |
| `hooks/cmdline.py#strip_subshell` | The rule for a glued `(cd`; `_nesting` counts openers the same way and does not count a glued closer |
| `tests/test_a_path_the_command_wrote_out.py` | 44 tests at the branch point, 8 of them for the aimed reset; 7 added here |
| `hooks/commit-review-gate.py#commit_invocations` | The gate's entry point, where the executed scenarios are measured |

**What breaks in six months.** The body count is read from posix-mode `shlex`
tokens, so it cannot tell a quoted word from a reserved one. Its errors were
shaped so that the cheap direction is the common one: an opener counts
anywhere (over-count → prompts), a closer only in command position
(under-count → prompts). A future contributor who "fixes" `echo fi` by
counting closers anywhere reopens eight shapes the differential found; the
test `test_a_bodys_later_statement_is_not_a_top_level_one` carries two of
them for that reason.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Revert the aimed reset to the wide one (`env = {}` for every refusal) | Strictly safer and strictly worse: `if …; then … fi` is the commonest shape in a script and every one of them prompted. Round 2 called 🟡 3 a decision, and the goal in `CLAUDE.md` decides it against the design that asks | rejected — the aim is kept and proven instead |
| Keep the aimed reset as found | 82 fail-opens in 1,790 inputs, all newly opened by it. A body's second statement bound as top level in every compound-command shape bash has | rejected — this is the finding |
| Empty the environment at every closer (`fi`, `done`, `}`) | Closes the class but reintroduces the wide reset for every compound command: a name bound BEFORE the body would be lost at `fi` | rejected — that is 🟡 3 again |
| Count closers wherever they stand | `echo fi` inside a body closed it early and the assignment after it bound — measured, eight shapes | rejected — closers count in command position, `)` last as well |
| An integer count (round 0) | A count cannot say which body a closer closes: a multi-line `case` arm pattern `a )` is a `)` last in its segment, and it brought the count to zero before the arm body (round 1 🔴 2); the glued `f(){` opened nothing (🔴 3) | replaced in round 1 by a stack — `)` pops only a `(`, every closer only its own opener |
| Count openers wherever they stand (round 0) | `git commit -m "(wip) x"; SB=/two` and `grep -c '(' f; SB=/two` opened a body that never closed and prompted for the rest of the string (round 1 🟡 6) | rejected in round 1 — openers count in command position only. Safe because a closer pops only its own opener, so an uncounted opener inside a counted body leaves the outer body open until its own closer |
| Carry quote provenance out of the splitter | Would also close Q1's single-quoted operand. Costs a new field on every token through a splitter three readers share | deferred — `questions.md` Q4, the repository owner |
| Model bodies for the directory half too | The directory half already reports a superset (`parked` keeps the un-moved shell), so it over-asks rather than opens. Changing it is a second work item with its own prompt-volume argument | deferred — `questions.md` Q5 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | What of the old change is in the tree: a file-by-file diff of the old branch's tip against the branch point, the two new test files located, the four 🟡 traced to code | **Executed**: `git diff fix/stops-the-reader-need-not-make -- <files>`; the scope run at the branch point, 295 passed; 7 mutations from round 2's 🟡 7, 6 red and 1 (the `_unseen` bare-name rule) surviving | a456076 — the record; no code moved |
| 2 | The aimed reset proven or corrected: a differential run of the wide reset against the aimed one over compound-command shapes, every newly resolved input checked against bash | **Executed**: 1,790 inputs, bash 3.2.57 as oracle — 82 fail-opens, two families, both closed; re-run 0 fail-open, 0 lost | 9ea31d8 |
| 3 | The body count, the prefix refusal in `understood`, the blind-sweep pin, with tests; 7 mutations of the new mechanism each red | S10 · S11 · S12; 301 passed in the scope; `ruff check` and `ruff format --check` clean | 9ea31d8 |
| 4 | The SDD set, `changelog.md`, the ledger fragment with content anchors, `evidence-check --strict` at 0 broken | the checker's own output — 104 ok · 0 broken; `unverified-check --baseline origin/release/v0.3.0` — 4 open, each with an answerer, 0 unreadable | 0903bfe |
| 5 | Round 1's fixes: the body stack, the function-call reset, the array and the three writers, openers in command position; the differential in the tree as `tests/test_the_reader_agrees_with_bash.py` | S13–S17; 10 mutations of the new mechanism each red; the in-tree differential (25 × 27 inputs, bash 3.2.57) and a scratch differential of 2,109 inputs against the reader at `dd7e45e` — 0 fail-open now, 124 there, 0 resolutions lost | f0442a7 |

## Operational impact

- **Shapes that newly prompt, measured against the reader at `dd7e45e` over
  2,109 inputs.** Round 0 claimed no new prompt on a shape that resolved
  correctly before; that was not true and round 1 said so. What newly prompts
  falls in four families, and bash agrees with the old answer only in the
  first two: (1) an assignment as a later statement of a body that DOES run —
  a true `if`/`elif` branch, a matching `case` arm, a `for` with items, a
  brace group, `time { … }`, a function body when the function is called —
  because the reader cannot tell a body that ran from one that did not;
  (2) `${SB:=…}` / `${SB=…}` on a name that already has a value, and `((SB=…))`
  or `let` in a pipeline stage; (3) `! eval …`, `time source …`, `! select`
  — the prefix hid a word `understood` refuses, and the same segments were
  fail-opens under other inputs; (4) `(cd <x> && make)` followed by an
  assignment, the glued-closer cost. Everyday shapes round 1 named —
  `git commit -m "(wip) x"; SB=/two`, `grep -c '(' f; SB=/two`, nested `if`,
  `time { …; }` — resolve. No shape newly answers: 0 fail-opens in the run,
  where `dd7e45e` had 124.
- **`understood` refuses more**, and the directory half inherits it in the
  fail-closed direction: `time pushd <x>; git commit` stops where it used to
  read as unmoved.
- No migration, no new dependency, no new environment variable, no
  signature change. `.git/specseal-*` marks are unaffected.
