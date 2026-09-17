# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `CLAUDE.md` (fragments never the shared file · no real identifiers · a thing more than one party can have is named with whose · the merge method per direction), `seal/specs/1789598366-…/spec.md` + `plan.md` + `questions.md` + `routing.md`, `seal/follow-up.md`, `skills/agent-contract/SKILL.md` §§1 2 3 4 5 6 7 9 10 12 14 15 16, `skills/implement/SKILL.md`, `skills/writing-style/SKILL.md`, `~/.claude/skills/commit-pr-convention/SKILL.md`, `templates/config.md` §*Broad gate* + §*What is refused, and what stays allowed* + §*Choosing a value — the criterion*, `templates/sdd-phase.md`, `templates/sdd-overview.md`, issue #415
· evidence: five rows added to `seal/ledger/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it.md`; one row REMOVED from `seal/ledger/1789445605-…md`; ten rows elsewhere re-read and re-stamped, each with a note saying what was read
· verified: executed — the four modules the phases name, `bin/evidence-check --strict .` (exit 0), `bin/unverified-check` (exit 0), `ruff check` and `ruff format --check` over the touched files. Not executed — the full suite, the repository-wide lint and the typecheck (`agent-contract` §2)

## Why this work exists

A `Broad gate` row holding a pipe was unwritable, took every config row below
it with no message anywhere, and let `seal mode` write a second `Mode` row
into a person's file; the row is writable now, and a line that will not parse
is quoted back instead of being reported absent.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| **Which phase renames the two cases whose names state the old behaviour** | `plan.md` phase 4: *the rename of the case whose NAME states the old behaviour lands in the same commit as the fragment edit* | phase 2 | Phase 2 changes the message that `test_a_piped_row_is_refused_by_the_table_and_not_by_this_refusal` asserts, so the phase cannot close with that case standing. <!-- NAME NOT IN TREE: the old name is on this row, above; it is now `test_an_unescaped_pipe_is_named_as_a_line_that_will_not_parse`. --> Renaming it removes an anchor, and `seal/ledger/1789445605-…md` cited it, so the ledger work rode phase 2's commit. Phase 4 kept the documents |
| **Which modules phase 4 runs** | `plan.md` phase 4: `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_settings_have_a_front_door.py -q` | those two plus `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` and `tests/test_first_setup_asks_once.py` | The case pinning the template's pipe sentence is in the first of the two extra modules and the case pinning the bootstrap's is in the second. Running only the named pair would have left both documents' cases unrun by the phase that rewrote them |
| **Whether A3's fixture needs a row above the piped one** | `spec.md` A3: *a config whose `Mode` row sits below a `Broad gate` row written with `\|`* | a fixture with `Record language` above the piped row | `config_rows` breaks on an unparseable line only once it has found a row. With the piped row FIRST, the rows below it survive and the defect does not reproduce. Measured both ways round; `spec.md` A1 is unaffected because its piped row is the table's second |
| **A case no scenario asks for** | spec silent | `test_a_three_column_row_still_ends_the_table` added | Widening what a cell may hold must not widen what a ROW is. `plan.md`'s alternatives table rejects a greedy last cell on exactly this ground, and nothing in the suite would have caught that rejection being undone |
| **The escape narrows one shape, and two documents said it could not** | `plan.md` §*Operational impact*: *a widened cell pattern can only make more lines into rows, never fewer*, and `questions.md` M3 again | the behaviour is kept and the claim is corrected | A backslash immediately before a cell-ending pipe is now one escaped pipe, so `\| Broad gate \| C:\Users\x\tools\\|` stopped being a row — found by round 1 🟡 2, measured both members of the shape. Kept because the alternative is a pattern where the same bytes mean an escaped pipe in one place and a delimiter in another, and because nothing becomes unwritable: a space before the closing pipe returns the value byte for byte, the reader strips the cell. Corrected in `plan.md`, `questions.md` M3, `spec.md` §*What this repair cannot see* and the changelog; pinned by `tests/test_the_mode_question_is_asked_once.py#test_a_backslash_against_a_pipe_is_the_one_shape_the_escape_narrows` |
| **A case Q1's answer asks for and `plan.md`'s phase 1 row does not** | `questions.md` Q1, as the owner answered it: *a case must pin that a value carrying Windows path separators survives the reader unchanged* | `test_a_windows_path_survives_the_reader_exactly_as_written` added | The constraint decides the implementation: the reduction is exactly `\|`, never a general backslash unescape. Red under `re.sub(r"\\(.)", r"\1", value)`, which returns `C:UsersxPythonpython.exe -m pytest` |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the sealer, in the broad gate after the rounds settle (`agent-contract` §2) |
| every platform but macOS 15.5 — the Windows and Linux legs | the repository's own CI on the pull request. The Windows path case is a fact about the READER and runs identically everywhere; what stays unmeasured on `cmd.exe` is unchanged by this branch, because the reduction happens before any shell is reached |
| whether a `Broad gate` row a person actually writes with `\|` survives a round trip through `/specseal:config`'s own edit | the repository owner. The skill tells a session to edit the value in place and now says how a pipe is written; nothing executes that path |
| that the four claims re-read in `seal/ledger.md` and the four in `seal/ledger/1789445605-…md` are still true — read, not executed, except where a cited case was run | the repository owner. Each row carries a note saying what was read and on what date |

## Not done

**No pull-request arm reports a malformed `seal/config.md`.** `spec.md` §Out
rules it out by name: the message reaches whoever runs `broad-gate` or opens
`/specseal:config` and nobody else, and adding a CI arm is a change to a gate
that `CONTRIBUTING.md` asks its own argument for.

**`hooks/mode-gate.py` still says nothing**, deliberately, and a case pins it.
A config whose `Mode` row is hidden below an unparseable line still reads as
undeclared and the gate still simply asks the mode question again. That is the
cost of keeping a `PreToolUse` hook silent, and the alternative — a hook that
refuses wrongly — stops a session with nobody able to get past it.

**An unescaped pipe is still not a row.** Accepting one needs a greedy last
cell, whose failure scenario is in `plan.md`.

**The language rows gained no code reader.** `questions.md` M2 asked and the
answer is that none exists; giving them one is a different work item with its
own frame. What a piped row actually takes is `Mode` and `Broad gate`, and the
records say that rather than repeating #415's sentence.

## Fed back into the spec

**Inferred during implementation: the stop rule needs a row before it can
stop.** `config_rows` breaks on an unparseable line only once it has found a
row, so *a piped row takes every row below it* is true of the second row of a
table and false of the first. Neither #415, `spec.md` nor `plan.md` says it.
Every fixture in this branch states it in a comment, `templates/config.md`'s
pipe cell now carries the condition, and the ledger row records the
measurement both ways round. A planner may overturn it by deciding the
first-row case should also end the table — that would be a change to the stop
rule, which is out of scope here.
