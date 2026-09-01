# Feature Specification: 1788305134-the-reader-stops-where-it-need-not

<!-- specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `hooks/cmdline.py#understood` — *"The reader used to answer 'nothing moved' for every construct it did not implement, which is a CONFIDENT answer"* | The inversion this reader is built on. Every change here keeps the direction: what it cannot compute stops, and what it can compute is computed from the command string alone |
| `hooks/cmdline.py#EXPANDS` — `"$`*?[]{}"` | Any operand containing `$` is unresolvable. Right for a value this process cannot see, wrong for one the command wrote out two tokens earlier. The substitution runs in FRONT of this test and the test stays |
| `hooks/cmdline.py#walk_directories` — `states` and `parked` thread across segments | The mechanism a name environment joins. Nothing new is invented to thread names; the environment is a third thread and the body count a fourth |
| `hooks/cmdline.py#_heredoc_split` — the arithmetic-region comment and its measurement of 51 shapes | The second defect the original item fixed, stated by the code that had it |
| `docs/review-chain-spec.md` — an unreadable destination is a stop, never a silence | The fail direction every half must keep: the reader may stop where it previously stopped, never answer where it previously refused |
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask is the more expensive. This is why the wide reset was aimed rather than kept, and why the aim had to be proven against an oracle rather than assumed |

## Scope

This item re-applies a reviewed change whose branch lost its history, and it
found the change already in the tree. What the tree carries and what this
item adds are both in scope, because the review chain reads this file.

**Already in the tree at the branch point (`2c3449f`), verified here.**

1. **A variable the command itself defines is resolvable.** `VAR=value`
   assignments written in the command string are collected in order, and
   `$VAR` / `${VAR}` in a later `-C` or `cd` operand is substituted before
   the operand is judged. One command string; nothing from the environment;
   nothing carried between tool calls.
2. **Both paren models track `${…}`.** The arithmetic-region skip in
   `_heredoc_split` and the paren stack in `drop_comments` each count
   parameter-expansion nesting, so a `((` inside `${…}` is a word. An
   unbalanced `${` leaves the heredoc opener readable, because the other
   direction hid a body as commands.
3. **The agent files say how to write a probe that commits without stopping
   the gate.** `agents/warden.md` and `agents/scribe.md` carry three shapes
   and say which to prefer.
4. **The wide reset was aimed.** A refused segment that carries no name —
   `fi`, `then echo hi`, a subshell, `pushd` — keeps the environment; one
   reaching text this reader never sees empties it; the rest forget what they
   name. This closed round 2's 🟡 3, 4 and 5 on the old chain, and it was
   written after that branch's last commit and reviewed by nobody. It is
   what this item had to prove.

**Added by this item.**

5. **A statement inside a body is never bound.** The aimed reset opened a
   class the wide one had closed by accident: a compound command's second
   statement arrives as a segment of its own and bound as top level, so
   `if false; then echo hi; SB=/three; fi; git -C "$SB"` answered `/three`
   where bash has `/one`. A body count now runs beside the environment, and
   while it is above zero an assignment is forgotten.
6. **A reserved word behind a prefix is not a simple command.** `! for SB in
   …` and `time pushd <x>` passed `understood` because only the first word
   met the reserved-word test.
7. **The bare-name rule of the blind name-writer sweep is pinned.** It had
   no test; loosening it survived the suite.

**Out.**

- **Expanding a variable this process cannot see.** `git -C "$WT"` from the
  environment stays unresolvable.
- **Loop and positional variables, command substitution, arithmetic
  expansion** in an operand. Same reason, one step further out.
- **Quote provenance.** `shlex` is posix-mode, so `'$SB'` is filled and a
  quoted `"("` opens a body. Both are recorded costs (`questions.md` Q1, Q4)
  and both fall on the side of a prompt except the single-quoted operand,
  which was pinned as a decision by the original item.
- **The directory half's reading of bodies.** `if false; then :; cd /two;
  fi; git commit` reports both `/two` and the session's directory, because a
  `cd`'s own failure is parked and a `;` merges it back. That is a superset,
  not a silence, and it is left as it is (`questions.md` Q5).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 The command defines its own path | Given `SB=/abs/path; git -C "$SB" commit -m x` · Then the target is `/abs/path`, judged like a written-out path | `tests/test_a_path_the_command_wrote_out.py::test_the_named_form_answers_what_the_written_out_form_answers` against the gate, both directions |
| S2 The composed form | `SB=/abs/path; git -C "$SB/r1" commit …` names `/abs/path/r1` | `::test_a_name_composed_with_a_suffix_resolves` |
| S3 An environment variable is still unresolvable | `git -C "$WT" commit -m x` with no assignment in the string stops exactly as before | `::test_an_environment_variable_is_still_unresolvable`, `::test_an_environment_name_still_stops_the_gate` |
| S4 A loop variable is still unresolvable, and names itself | `SB=/p; for n in 1 2; do git -C "$SB/r$n" commit; done` stops, and the reason is `$n` | `::test_a_loop_variable_keeps_its_prompt_and_names_itself` |
| S5 The last assignment wins, and only from a segment that runs | Two assignments to one name use the later; one inside a construct `understood` rejects never enters | `::test_the_later_assignment_is_the_one_used`, `::test_an_assignment_the_reader_cannot_place_never_enters` |
| S6 A `((` inside a parameter expansion is a word | `echo ${x:-((} <<EOF` · `cd /target` · `EOF` · `git commit -m real` drops the body and judges the commit where the shell is | `tests/test_what_the_reader_understands.py::test_a_parameter_expansion_paren_no_longer_imports_the_body_s_cd` |
| S7 Both paren models agree, and an unbalanced `${` fails closed | Neither model reads a `((` inside `${…}` as arithmetic; `${x:-<<E}` opens no heredoc; an unclosed `${` still lets a real heredoc open | `::test_a_hash_inside_an_expansion_closes_no_brace_in_either_model`, `::test_a_heredoc_opener_inside_an_expansion_opens_no_body`, `::test_an_unbalanced_expansion_still_lets_a_heredoc_open` |
| S8 Nothing silently opens | Given a corpus of refused-segment shapes between an assignment and a `git -C "$SB"` · Then every input the reader resolves matches what bash leaves in `$SB`, and no input the wide reset stopped is now silent unless bash agrees | **Executed here**: 1,790 inputs (26 wrappers × 70 statements), bash 3.2.57 as the oracle, 749 resolved, 0 mismatches — after 82 were found and closed (S10, S11) |
| S9 An agent can write a probe that commits | Both agent files carry the three shapes and say who the prompt reaches | `tests/test_a_probe_that_commits_says_so.py`, four tests |
| S10 A body's later statement is not top level *(inferred during implementation)* | Given a body that does not run — a false condition, an empty list, an arm that does not match, a function defined and never called — or runs in a subshell, with an assignment as its second statement · Then the name is forgotten, never bound; and after the body's closer a top-level assignment binds again | `::test_a_bodys_later_statement_is_not_a_top_level_one` (16 shapes), `::test_the_body_ends_at_its_closer`, `::test_what_moves_the_count_and_what_does_not` |
| S11 A reserved word behind a prefix is refused *(inferred during implementation)* | `! for SB in /two /three; do :; done; git -C "$SB"` stops; `! true`, `time echo hi`, `command -p ls` are still understood | `::test_a_reserved_word_behind_a_prefix_is_not_a_simple_command` |
| S12 The blind sweep forgets bare names only *(inferred during implementation)* | `if read -rp 'SB> ' ans` forgets `ans` and keeps `SB` | `::test_the_blind_sweep_forgets_bare_names_only` |

## Data & interfaces

`walk_directories` threads four things across segments: `states`, `parked`,
`env` and, from this item, `depth`. No signature changes. Both gates and the
worktree guard read the filled operand through the token list
`walk_directories` yields (`_expanded`), so no consumer is touched.

`understood` refuses one more shape (S11). It is shared with the directory
half, where the change is in the fail-closed direction: `time pushd <x>; git
commit` used to read as "nothing moved" and now stops.

**The substitution happens before the `EXPANDS` test, and the test stays.**
That ordering is what keeps S3 and S4 true and is the whole reason the change
is bounded.

## Open questions → questions.md

None blocking. Q1–Q3 are carried from the original item; Q4 and Q5 record the
two costs this item accepted.
