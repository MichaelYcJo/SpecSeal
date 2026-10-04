# Implementation Plan: a here-document body is data to the commit gate (#739)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.
Q1–Q3 take the frame's defaults (move the one corpus row; strict `python3 -` is data; a sink beside a commit keeps today's reading). Q1 was reported to the owner at the spawn, because the trade it settles is the owner's by `docs/commit-review-gate-spec.md`.

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

Today the commit gate reads every here-document body back as shell to ask whether it commits. Under this change a body is data in one narrow, positively described shape, where it is provably not executed:

- its delimiter is quoted and its terminator arrives;
- the line is a plain line in `is_plain`'s construction;
- its consumer is `cat`, `tee` or a Python program read from stdin;
- nothing else on the line can run a file a sink wrote.

Everything outside that shape reads exactly as it does now. `spec.md` §*The rule (R)* is the contract.

## Technical context

The coordinates are content anchors, read at `101f9bd0`.

- `hooks/cmdline.py#_heredoc_split` is the one pass that drops bodies, and `#_heredoc_word` reads the delimiter and throws away whether it was quoted. `drop_heredoc_bodies` and `heredoc_bodies` are views over it. `hooks/cmdline_base.py` is a frozen byte copy of an older `cmdline.py` and is never edited.
- `hooks/commit-review-gate.py#commit_invocations` reads the top-level bodies in the loop `for body in heredoc_bodies(drop_comments(command)): if _hides_a_commit(body): found.append(Invocation((), (), base=_unresolved_base(cwd)))`. That unplaceable invocation is what produced #739's text, `UNREADABLE_CONSTRUCT`. `#_reads_a_commit` recurses into bodies, substitutions, `eval` arguments and host strings. R1 leaves that recursion alone.
- `hooks/tokens.py#is_plain` is the positive-shape model. It holds the sets `PLAIN_PROGRAMS`, `PLAIN_GIT` and `PLAIN_CONFIG`, the predicate `steps_around_hooks`, and a shlex lexer with `punctuation_chars=";&|<>\n"` over the command with comments and bodies dropped. `is_plain` is the owner's P7 rule and stays byte-for-byte as it is.
- `hooks/worktree-guard.py#_judgment_text` and the `wide` reading only ever DROP bodies. The guard does not change.
- `tests/test_no_shape_the_base_stops_reads_silent.py#corpus` holds #665's rounds 2 and 3 rebuilt. It is the regression net for this exact narrowing, and only the one row `spec.md` S10 names may leave it.

**What breaks in six months.** A word inside the allowed set turns out to run a file or its stdin, for example a `gh` subcommand that executes scripts. Or bash and the shlex lexer disagree about where a word ends in some construct (c) allows, and the opener count still matches by coincidence, so a body is given to the wrong command. Two things bound both: the set is closed, and the count check in (d) catches any disagreement that changes the number of openers. The way it shows up: a reviewer, or `test_no_shape_the_base_stops_reads_silent.py` gaining a row, finds a bash-executed commit that reads silent. The repair is to remove the word or add the construct to (c)'s exclusions. Nothing has to be redesigned.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A — enumerate the interpreters that RUN a body (shells), everything else data | Fails open on every runner the list misses. Legacy #75 rejected it for that reason. Work item `1790635415`'s version (#665, a "known interpreter is data" list) gave five shapes that read silent while bash committed, across two rounds, and it was reverted | rejected |
| B — a closed list of DATA consumers, a positive line shape, quoted delimiter, top level only | The residual risks in *What breaks in six months* above | **chosen** |
| C — change no code and write every shape into the known limits (the ticket's second checkbox) | Opens no hole. But every PR body and record note an orchestrator writes about the gate keeps losing the whole Bash call, and that is the first goal's failure, measured three times in one run | rejected. Only the unquoted and nested shapes go to the known limits, as R's boundary |
| D — B, plus unquoted bodies read for their substitutions only | Needs a body scanner where quotes are literal. `substitution_bodies` skips `'…'`, so reusing it skips `'$(git commit)'`, which bash runs. That fails open | out of scope (spec §Scope) |
| E — B applied at every nesting level | `bash <<<"$(cat <<'EOF' … )"` and `source /dev/stdin <<<"$(…)"` run the body. The inner reading cannot see that, so both would read silent | rejected (R1) |
| F — B with `cat`/`tee` only, Python out | Leaves #739's rows 1 and 3, two of its three measured refusals, as they are. It keeps the corpus untouched | rejected (`questions.md` Q2) |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The reader says what each body is.** `cmdline.py` gains the per-body record (text, quoted, terminated) from `_heredoc_split`'s one pass. `drop_heredoc_bodies` and `heredoc_bodies` become views over it with identical output. `_heredoc_word` reports quoting under R2a, so a `$` is never quoted. No gate behaviour changes yet | new unit cases for the record over every R2a/b value (spec §Shapes, rows 1–3); `uv run pytest tests/test_what_the_reader_understands.py tests/test_the_frozen_reading_never_grows.py` plus the new cases, narrow | f7b40db8 |
| 2 | **The gate reads only what can run.** The R2c–f shape check, then `commit_invocations`' top-level loop skips the bodies R makes data. S1–S8 planted in the gate's test module, each seen red at `101f9bd0` (S1–S4) or green before and after (S5–S8). The S10 row moved, with its docstring sentence | `uv run pytest` on `tests/test_gate_judges_the_repo_it_commits_to.py`, `tests/test_no_shape_the_base_stops_reads_silent.py`, `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`, `tests/test_a_commit_behind_a_reserved_word_is_judged.py`, `tests/test_the_commit_gate_decides_at_the_commit.py`, `tests/test_an_automation_run_meets_no_commit_prompt.py`, `tests/test_a_gate_that_fails_says_so.py`, narrow | 33a8f1f3 |
| 3 | **The words say it.** The two `docs/commit-review-gate-spec.md` paragraphs (the one opening **A file edit goes through the `Edit` tool** and the one opening **Two readings that prompted that run stay as they are**), and the S8-relevant sentence of the **What stays unread** paragraph if it needs one. `skills/agent-contract/SKILL.md` §9's "reads a heredoc body as shell, on purpose". `Enforced by:` lines name the new cases. The changelog fragment per `docs/the-record-layout.md` §*A change writes fragments, never a shared file*, and the ledger re-reads per `spec.md` §Data | `uv run pytest tests/test_edits_go_through_the_edit_tool.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_a_document_has_room_for_the_next_fold.py`, narrow; `evidence-check` over the fragment | 2d223ab4 |

The broad gate (full suite, lint, typecheck) is the sealer's, after the review rounds settle. No phase runs it.

## Operational impact

No migration, environment variable or dependency. Behaviour change for users: a Bash call matching R that used to be refused with the unplaceable-construct text now passes, or is judged only for its real commits. Every other call reads as before. Plugin users see the change at the next release, through the changelog entry.
