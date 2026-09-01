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
| Count openers only in command position | Under-counts a nested opener behind a `case` pattern, and the inner closer then ends the OUTER body early | rejected — openers count anywhere; the cost is prompts |
| Carry quote provenance out of the splitter | Would also close Q1's single-quoted operand. Costs a new field on every token through a splitter three readers share | deferred — `questions.md` Q4, the repository owner |
| Model bodies for the directory half too | The directory half already reports a superset (`parked` keeps the un-moved shell), so it over-asks rather than opens. Changing it is a second work item with its own prompt-volume argument | deferred — `questions.md` Q5 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | What of the old change is in the tree: a file-by-file diff of the old branch's tip against the branch point, the two new test files located, the four 🟡 traced to code | **Executed**: `git diff fix/stops-the-reader-need-not-make -- <files>`; the scope run at the branch point, 295 passed; 7 mutations from round 2's 🟡 7, 6 red and 1 (the `_unseen` bare-name rule) surviving | a456076 — the record; no code moved |
| 2 | The aimed reset proven or corrected: a differential run of the wide reset against the aimed one over compound-command shapes, every newly resolved input checked against bash | **Executed**: 1,790 inputs, bash 3.2.57 as oracle — 82 fail-opens, two families, both closed; re-run 0 fail-open, 0 lost | 9ea31d8 |
| 3 | The body count, the prefix refusal in `understood`, the blind-sweep pin, with tests; 7 mutations of the new mechanism each red | S10 · S11 · S12; 301 passed in the scope; `ruff check` and `ruff format --check` clean | 9ea31d8 |
| 4 | The SDD set, `changelog.md`, the ledger fragment with content anchors, `evidence-check --strict` at 0 broken | the checker's own output — 104 ok · 0 broken; `unverified-check --baseline origin/release/v0.3.0` — 4 open, each with an answerer, 0 unreadable | 0903bfe |

## Operational impact

- **No new prompt for a shape that resolved correctly before.** Three shapes
  newly stop, and bash disagrees with the old answer in every one: a body's
  later statement, a reserved word behind a prefix, and `(cd <x> && make)`
  followed by an assignment — the last is the one recorded cost, a prompt
  where bash has the value.
- **`understood` refuses more**, and the directory half inherits it in the
  fail-closed direction: `time pushd <x>; git commit` stops where it used to
  read as unmoved.
- No migration, no new dependency, no new environment variable, no
  signature change. `.git/specseal-*` marks are unaffected.
