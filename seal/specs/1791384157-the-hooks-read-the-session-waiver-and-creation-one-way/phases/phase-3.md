# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b5ceec40 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The brace shape (`spec.md` In 5, #856, the owner's answer (c) of
2026-10-08): `_git_finding`'s `brace` arm reading the frozen words and the
judgment text's unquoted spans; `_described`'s text in both languages;
S11–S13 red first; `_rebase_names_a_branch`'s docstring; §A's brace
sentence, its two costs and phase 1's M2 figure in the failure-direction
paragraph, §*Known limits*' hidden-spelling bullet, each with its
`Enforced by:` line. The git-binding case executed under bash.

## What this phase found

**The brace reading is the command's, threaded as one flag.** `main` reads
`_unquoted_brace(judged)` once, and `_segment_finding`, `_git_finding`,
`_merged_findings` and `shape_of` take it as `braced`. A substitution body
reads its own (`_first_finding_in`), because a body is read where its quotes
are still there. The brace arm sits after the creation and switch checks and
before every other kind, so a switch and a creation keep their own rules,
as `spec.md` In 5 says, and a braced `checkout` or `stash branch` reports
the brace rather than the kind its frozen words read as.

**The pattern excludes whitespace inside the braces.** bash expands no
brace holding unquoted whitespace, and phase 1's first run showed a brace
GROUP (`{ echo ; … ; }`) matching the wider pattern. A word never holds
unquoted whitespace, so the exclusion matters only to the text read, and
`git commit -m '{a,b}' && { echo x,y; }` is the case that pins it (S12).

**The quoted spans are `hooks/tokens.py`'s.** The regex `is_plain` used
inline is a module constant now, `tokens.QUOTED_SPANS`, and `is_plain` and
the guard both read it, so the two agree on what a quote is. Where
`hooks/tokens.py` did not load, the guard reads every brace as unquoted: a
broken reader costs a stop, the direction §*Which tree* gives every other
broken read.

**How each case was seen red.** S11's four forms, red at the base hooks:
silent in an ACTIVE tree. S11's body and cut-group forms, and the
broken-reader case, each SURVIVED a mutation of its own reader until it was
planted, and is red with it. S12 is green at the base and at the head, which
is its claim; its three rules (quoted spans removed, whitespace excluded, no
`$` before the brace) were each broken through `bin/mutation-check`, red.
S13's bash half was green at the base (bash expands; git moves HEAD), and its
guard half raised at the base because `shape_of` took no `braced`; the cases
red at the base on the verdict are S11's. The Korean text and the policy pin,
red before their text.

**What #856's round-1 table predicted held under bash.** All four S11 forms
act when bash expands them (git 2.50.1): the two rebases and the stash move
HEAD, and the worktree form adds a worktree, so `BRACED` asserts all four.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the inline quoted-span regex in `hooks/tokens.py#is_plain` | `hooks/tokens.py#QUOTED_SPANS`, read by `is_plain` and the guard's `_unquoted_brace` |
| `_rebase_names_a_branch`'s phrase "read off the words bash hands git" | its docstring now says the words are read once their redirections are off; a `Corrected ·` row for released row R1 in phase 6 |
