# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 275ec872 |
| Ran by | unknown — the phase-2 spawn prompt named no agent or model; the orchestrating session fills this |

## What this phase was asked

Phase 2 of `plan.md` only, closed and handed back; phase 3 not started,
because it rebases onto #841's twins sampling, which has not landed (W4). The
owner answered P1–P4 on 2026-10-06, all (a), recorded at 707872aa: the list
holds the recorded subcommands with their counts (P1); a `$( … )`, backtick
or `<( … )` body is read through the same three shapes, recursively, so a
body of listed git is listed and one holding a switch, a `checkout` or an
unlisted subcommand stops with that shape's own rewrite, and M3 should fall
to 34 (P2); `update-ref` and `symbolic-ref` stay unrecognised and the stop
names `git -C <scratch clone>` or waiting for the other session (P3); an
untokenizable command holding `git` stops as written and the stop names
splitting it and `git commit -F <file>` (P4). P2 changes In 1 of the approved
frame, so it is fed back into `spec.md` and recorded in `overview.md`.
Handle W3's two findings from phase 1: `command_strings` returns no string
for `eval "git switch x"`, and a redirection after `git` is read as the
subcommand word. Commit as each step stands; no push, no pull request, no
GitHub post; lint with `uvx ruff`; run the touched modules, never the whole
suite. Hand back the commits, what phase 2 closed, each claim labelled, the
M3 figure after P2, and what phase 3 needs from #841.

## What this phase found

**The frame holds, with one cell that does not.** `spec.md` In 3 and S3 make
the stop an `ask` without the press in every state that matters, ACTIVE
included. `docs/worktree-guard-spec.md` §A row 1 denies a branch-form
`checkout` in an ACTIVE tree with nobody asked, and policy outranks the spec,
so the build denies there whatever the press. The deny costs nobody a prompt
(the model rewrites, as under the press), and an `ask` would have let one
approval run `git checkout <branch>` over a working session, which the base
never allowed. `questions.md` P5 puts it to the owner with the one-line way
back.

**A stop that asks has to judge a creation on the same line first.** The
first green run failed `test_the_guard_is_never_silent_where_the_writer_records`:
`git worktree add ../wt f && git checkout feature/x` in an IDLE tree drew the
new stop's `ask`, and approving it would create the worktree with the
creation question never put. It is the defect `choose`'s `before_ask` was
written for, one site over, and `stop_unrecognised` now takes the same hook.
The frame did not name it; the existing property case caught it.

**A substitution body is read from the command's text, not from a
segment.** The frozen splitter strips the quotes off a segment's tokens and
cuts a body at its own `;` and `|`, so a body rebuilt from one segment is not
the body the shell runs. Read from the judgment text it is, and the price is
the tree: a body (and an untokenizable command) belongs to no one segment, so
it is judged in the session's own tree, the #686 fallback and the stand-in
the commit gate uses for a body's commit. `cd W && F=$(git checkout x)` with
`W` dirty and the session's tree clean is silent. Named in `overview.md`
§*Not verified* for the warden and phase 4's §*Known limits*.

**W3, both findings.** `eval`'s argument is found the way the commit gate's
`_eval_argument` finds it (`command_word` with `eval` as the stand-in, past a
redirection on the second reading, past `builtin`), because `command_strings`
hands back nothing for it. A redirection read as the subcommand word (`git
2>/dev/null status`, `git switch>/dev/null x`) is a shape of its own, kind
`redirection`, whose rewrite moves the redirection to the end; it is not
read past, because In 1 reads the frozen reading's words and nothing more.
The shell's string is read with `reparsed_texts` rather than
`command_strings`: it returns every word that might be the string, and the
wrong direction there is a stop rather than a silence.

**The hidden-git class is exactly what the wider reader reads and the frozen
one does not.** Measured on the two readers before building: the frozen
reading already reads `if`/`while`/`for … do`/`!`/`(`/`{`, `xargs`,
`timeout`, `exec`, `time` and `case` arms, so `wide.parse_git` finding git
where `cmdline_base.parse_git` finds none leaves redirections (in front of
`git` or glued to it), `noglob`, `nocorrect`, `repeat N` and zsh's `for i (…)`
and `foreach`. `builtin git` is read by neither. A `2>&1` cuts a segment at
its `&`, so `merged_view` is read too, and a group with a part the frozen
reading reads as git is that part's: `git switch feature/x 2>&1` still meets
the ladder.

**Where the reader fails, the bare word stops.** With `hooks/cmdline.py`
unloaded, or a reader raising, a string, a body or a hidden position holding
the bare word `git` is the finding, kind `unread`, so a broken reader costs a
stop where the tree matters and never a silence. A plain git command is read
by the frozen reading and is unaffected.

**Seen red.** Against the unchanged guard (38a54f83, hooks at the base):
S3, the S3 shape-naming case, S4, S5, S6, S7, S8 and S9 failed; after the
build, W1's text pin and W3's fail-closed case failed against the base's hook
put back in place from `a9d7b0e5` (and restored from a copy, hash compared).
S1 and W2 hold at the base by construction (a listed shape spawned nothing
there either, and the base read one tree once), so both were shown red by
mutation. Every unit this phase added was broken one at a time through
`mutation-check`, 31 breaks, each run against the cases that cover it, and
every one went red: one `LEAVES_THE_TREE` row; `_restores`'s path word and
its spaced-redirection skip; the `worktree` and `stash branch` branches and
the redirection-as-subcommand branch of `_git_finding`; `_eval_text`;
`_wide_git`'s unglued half; `_hidden_in`'s string reading; `_merged_findings`'
skip and its finding; `_command_findings`' bodies, untokenizable and
text-test branches; `_first_finding_in`'s depth bound, its switch/creation
branch and its merged view; the `_sessions` and `_changes` memos;
`tree_matters`' unusable and dirty halves; the press read swapped for the
consent record (S7); the ACTIVE deny; `before_ask`; the item dedupe and cap;
`_item`'s body descent; `_spoken`; `_BARE_GIT`; `main`'s no-repository
silence; and the press reader's wiring into `main`. The `_spoken` break was
refused once because the formatter had wrapped its line, and was re-run on
the wrapped text.

These had no case reaching them until that enumeration: `git worktree list`,
`git stash` and `git stash branch`, a `--` followed by nothing or by a
redirection only (glued or spaced), a glued `git>`, a cut `2>&1` in front of
`git` and inside a body, the body depth bound, the item cap and dedupe, a
`-C` naming no repository under an ACTIVE stub, a switch carrying `2>&1`, and
the quoting of a multi-word token. Each got a case in a8d3d1c6 or 275ec872.

**M3 after P2, by a probe and not by phase 3's re-read.** A deleted
`test_tmp_826_m3.py`, run as `python3 -I` from the session scratchpad with
this branch's `hooks/` loaded, read every Bash `tool_use` in every `*.jsonl`
under `~/.claude/projects/*SpecSeal*/` as distinct (command, cwd) pairs, and
replayed each through the build's own readers before any tree is read
(`_segment_finding` per frozen segment, `_merged_findings`,
`_command_findings`): no git spawned, every count tree-blind. Self-check
first: S3's ten probe shapes all stopped and S1's five did not. Its pair
definition is not phase 1's (it reads the entry's own `cwd` and found 22,628
pairs in cut 1 and 35,816 in cut 2, against phase 1's 31,193 and 33,220), so
these numbers are not the before/after comparison; phase 3's re-read, with
phase 1's definition, is.

| | Cut 1 | Cut 2 |
|---|---|---|
| pairs stopped tree-blind | 207 | 352 |
| of them, a `checkout` without `-- <word>` | 188 | 321 |
| an unlisted subcommand | 16 | 25 |
| a string handed to a shell | 0 | 4 |
| an untokenizable command | 3 | 3 |
| a body finding (any kind) | 2 | 3 |
| **M3: an unlisted subcommand, its own plain spelling** | **16** | **25** |

M3's 25 in cut 2 are `update-ref` 16, `check-ref-format` 2, `hash-object` 2,
and one each of `version`, `cherry`, `detach`, `$s` and `$o` (a subcommand
held in a shell variable). Every other stopped pair now has a plain spelling
the stop names: P2 (a) turned the 575 listed-git bodies silent and gave the
rest their inner shape's rewrite, and P4 (a) named one for the untokenizable
command. On phase 1's own definition, a body of listed git read as listed
gives the 34 the owner was told; this probe reads 25 by the build's readers.

**A finding for phase 3's re-read.** `check-ref-format`, `hash-object`,
`cherry` and `version` are git subcommands this probe sees recorded in cut 1
and phase 1's 55-word table does not hold, and `symbolic-ref`, which phase 1
counted once, does not appear here. Under P1 (a) a recorded subcommand that
leaves the branch belongs on the list, so phase 3's re-read, on phase 1's
definition, decides whether these four are rows; phase 2 added none on a
probe whose definition is not the frozen one.

**What phase 3 inherits.** 48 cases of
`tests/test_guard_resolves_the_tree_it_judges.py` fail now, all asserting a
reading this work removes or the old verdict for a shape that is unrecognised
by design: `test_what_only_the_wider_reading_finds_is_put_to_the_person` (15
parameters), `test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer`
(5), `test_a_segment_the_base_reads_no_git_in_does_not_take_the_first_slot`
(5; the deny holds, the `top` the stub is first asked about is now the
session's tree, where the hidden git sits),
`test_a_redirection_word_is_not_read_as_a_branch_name` (6),
`test_a_switch_wherever_its_redirection_stands_meets_the_dirty_tree_row` (5),
`test_a_restore_wherever_its_redirection_stands_stays_silent` (3, a
`checkout` restore without `--`),
`test_a_restore_before_a_hidden_switch_does_not_silence_the_question` (2),
`test_a_newly_read_checkout_in_front_takes_no_question_away` (2), and one
each of `test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard`,
`test_a_creation_only_the_wider_reading_finds_is_silent_under_consent`,
`test_the_question_names_both_kinds_and_says_it_in_korean`,
`test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` and
`test_a_message_search_over_a_dirty_tree_is_asked`. They were left alone:
#841 changes that module, and phase 3 rebases onto it before retiring them.
The other nine modules that load the guard passed (888 passed, 1 skipped,
the 165 s case deselected).

**What phase 3 needs from #841.** The commit on #841's branch, or the
release-branch commit it lands as, that holds the sampled form of
`test_no_twin_is_asked_unless_an_operator_cuts_the_segment`, so the rebase
deletes the sampled case and the `Corrected ·` row for D1 of 0.18.2 is
written once (W4). Phase 2 neither ran that case nor touched it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| candidate C's call sites in `main` (`quiet()`, which asked `wider_only_kinds` and `ask_what_only_the_wider_reading_finds` at each silent exit) | the unrecognised stop (`stop_unrecognised`); the two functions stay defined until phase 3 deletes them |
| `main`'s reach into `classify` (both readings, `base_only` and #790's) and its `newly_read`/`past_the_base` slot rule | `shape_of` and `_segment_finding`; `classify` stays defined until phase 3 |
