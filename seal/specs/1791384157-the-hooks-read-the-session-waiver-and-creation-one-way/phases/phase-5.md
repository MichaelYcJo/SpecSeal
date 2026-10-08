# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 077c0bc6 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

One waiver reader and one runner (`spec.md` In 3, In 4):
`tokens.without_bodies` with the frozen fallback; `has_marker` and
`has_token` through `tokens.given`, `_reads_marker`, the guard's `carries`
and `_without_bodies` gone; `gate.git` answering `None`, `crg.git` gone,
each caller's ordinary-*no* line explicit, the three path readers handing
`None` through and `touches_code(None)` True; S7–S10 red first, S8's property
case over the three corpora; the consent-read paragraph of
`docs/commit-review-gate-spec.md`, §*The arms* of
`docs/the-commit-gate-inside-git.md` and §*Parity arm* of
`docs/the-review-and-parity-arms.md`, pinned. The orchestrator added the
eight suite-wide guard modules to the narrow run before the hand-back.

## What this phase found

**The one reader reads the words before a split fails** (`tokens._read_words`),
as phase 1 found it must for S9 to hold. `tokens.words` keeps its strict
reading, because `steps_around_hooks` reads a command that does not split as
one that steps around the hooks, and that direction stays.

**The fallback is an argument to `given`.** `hooks/tokens.py` cannot import
the frozen reader without becoming its third importer, so the guard hands
`cmdline_base.drop_heredoc_bodies` in. It is caught in `given` rather than in
`without_bodies`, because the released T1 cases replace `without_bodies`
itself with one that raises. Where `hooks/tokens.py` does not load, the
guard reads no token: a prompt the token would have spared, never a silence.

**S8 was red at the base on real disagreements**, not only on missing names:
the commit gate read `(… [worktree-ok])` as no token while the guard read it,
and an unclosed quote waived through the gate's substring and not the
guard's. Its corpus is the three modules' own commands, gathered by import.

**S7's refusal names the waiver typed in front**, which splits, rather than
`git -c specseal.waive=review`, which only the git hooks' refusal names. The
text was left alone (`overview.md`). **The `# don't [no-review]` case** this
module pinned as a documented form is refused now, and was rewritten to pin
the refusal; the apostrophe-after form took its place among the documented
ones. `test_s6_neither_read_honours_a_token_the_base_did_not` compares the
one reader against both base reads together, since `has_marker` and `given`
are one now: it reads a token only where one of them did.

**S10 runs a `git` shim**, `questions.md` W1's default: a POSIX script first
on `PATH` that exits 128 for any `diff` and execs the real git otherwise.
The cases skip on Windows, where the shim is not a program. The backstop's
path reader (`_paths_between`) survived a mutation dropping None until a case
of its own was planted.

**W2, which cases retire.** None retired. T1's four guard cases pass
unchanged through the one reader; `base_marker` in the heredoc module keeps
asserting the new read is no wider than the base's, as W2's default said.
The one rewritten case is `a trailing comment with an apostrophe`, above.

**The suite-wide guard modules found four things this branch caused, each
fixed in 077c0bc6.** `test_a_shrunken_corpus_declines_to_judge` read a git
path list in the `pre-commit` case's sanity line, which went; the
`.splitlines(` table of `test_every_reader_ends_a_line_where_gfm_does` names
`gate.lines` and drops the three units that no longer split; the guard spec's
"Until 0.21.0" became "Before #868" (`test_release_hygiene` refuses a version
at or above the running one); and `test_a_record_states_what_the_tree_has`
wanted `NAME NOT IN TREE` beside each record line naming a unit this work
item removed, including two lines of `spec.md`. The parity section's
`Enforced by:` line went too, because that section carries no statement
marker and the wrap check reads the line as prose; the pin names the three
cases instead.

**Mutations, through a scratchpad runner of `bin/mutation-check`**: the
partial read, the fallback, `has_marker`'s substring, `has_token`'s
fallback argument, `gate.git` answering "" on failure, `touches_code(None)`,
`changed_paths` and `pre_commit` dropping None, each red; `_paths_between`
red after its case.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/commit-review-gate.py#_reads_marker` and its substring fallback — NAME NOT IN TREE, removed here | `hooks/tokens.py#given`; `has_marker` is one line over it |
| the guard's `carries` closure and `_without_bodies` — NAME NOT IN TREE, removed here | `hooks/tokens.py#given`, with the frozen fallback handed in by `has_token` |
| `hooks/commit-review-gate.py#git` — NAME NOT IN TREE, removed here | `hooks/gate.py#git`, the one runner |
| the `# don't [no-review]` row of the heredoc module's documented forms | `test_a_waiver_behind_an_apostrophe_in_its_comment_waives_nothing` |
| three `.splitlines(` units in the gfm table | `("hooks/gate.py", "lines")` |
