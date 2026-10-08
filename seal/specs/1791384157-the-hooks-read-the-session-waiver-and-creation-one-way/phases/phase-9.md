# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 9

| Field | Value |
|---|---|
| Phase | 9 |
| Commit | 6e5e02bf |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

A brace in any word of any segment is the brace shape (round 3's 🟡 1–3,
⬜ 5; S17–S21, S24). `_segment_finding` reads a non-git segment on
`_git_finding`'s own test; `_brace_command_at`, `_brace_spells_git`, (NAME NOT IN TREE, removed here)
`_ONE_BRACE` and `_finding_tree`'s brace branch leave; (NAME NOT IN TREE, removed here) a non-git brace
segment is judged in `place`'s tree and every `-C <dir>` pair's tree (W3);
S17's thirteen, S18's rewritten case, S19's cost case and S20's directions
each red at a8f86f44 first; `_described`'s text re-read against a non-git
segment in both languages; §A's brace paragraph rewritten with the three
costs, the union and phase 7's figure pointing at its method; §*Known
limits*' `sh -c` bullet gains the brace-hidden `-C`; the `Enforced by:`
lines renamed; ledger row S11b rewritten in place; the changelog's brace
bullet rewritten with no command-word rule in it. `questions.md` P1 is
built on its default, **yes**, under `Automation | yes`.

## What this phase found

**The rule is one line, and the guard reads nothing more about a brace.**
`_segment_finding` stops a segment the frozen reading reads as no git where
the command holds an unquoted brace expansion and a word of the segment
holds one (`_BRACE`), the same test `_git_finding` makes for a git segment.
The three removed units and the brace branch of `_finding_tree` went with
nothing to replace them.

**W3: one finding, several trees.** `_finding_trees` answers
`_finding_tree`'s one tree, and for a non-git brace segment also every
`-C <dir>` word pair's tree, composed onto the directory `place` puts the
segment in. `main` looks each tree up once, as it already did, and the
finding is listed once, so the reason names the shape once. A glued
`-C<dir>` is not read, because `cmdline_base.parse_git` does not read it
for a git segment either (`_git_options` takes `-C` as its own word). The
union is the stopping direction; a `-C` a brace hides (`{git,} {-C,} W
switch x`) is not read, pinned by `test_a_c_a_brace_hides_is_the_named_limit`.

**W4: which cases changed.** `test_a_brace_in_no_git_word_stays_silent` is
rewritten as `test_a_brace_in_any_word_is_the_brace_shape`, its parameters
kept and three added (`A={a,b} ls`, `A={{a,b},c} ls`, the `for` loop), and
it asserts an `ask`, a `deny` in an ACTIVE tree and under the press, and
silence in a clean tree. `test_a_brace_that_makes_the_command_word_is_unrecognised`
keeps its name and gains round 3's thirteen.
`test_a_brace_command_word_is_judged_in_the_tree_its_c_names` keeps its
name, gains the `S`-dirty direction and the runner and `&`-cut forms.
`test_a_quoted_brace_in_a_git_word_stays_listed` gains S19's three. Two
cases are new: `test_a_c_a_brace_hides_is_the_named_limit` and
`test_a_quoted_brace_beside_an_unquoted_one_stops_on_both`. §A's
`Enforced by:` line names each.

**How each case was seen red.** Executed against the hooks of a8f86f44 (the
hooks are unchanged from there to 044027cc): 29 cases failed, the thirteen
round-3 spellings (silent in an ACTIVE tree), eight of S18's nine
parameters (silent in a dirty tree), all six `-C` cases (the `S`-dirty
direction was silent everywhere and the runner forms in both directions),
and the quoted-beside case. `A={{a,b},c} ls` was the one S18 parameter
already stopped, through the command-word reading, which read an assignment
before the command word. The two policy pins were red against a8f86f44's
text. The named-limit case was green there, which is its claim.

**Mutations, through `bin/mutation-check`:** the brace arm dropped, red;
the quoting gate dropped (every brace read as unquoted), red; the `-C` pairs
not read, red; the placed tree dropped from the union, red.

**The stop's text needed one change.** `_described` said the shell turns
the words "into other words before git reads them", which is false for
`cat {a,b}`. It says "before the command runs, so this guard cannot tell
which command that is" now, in both languages, and the two text pins
follow.

**Records named the removed units, and say so now.** `bin/evidence-check
--strict` refused 30 record lines naming `_brace_command_at`, (NAME NOT IN TREE)
`_brace_spells_git` or `_ONE_BRACE` once they had left (NAME NOT IN TREE): in `spec.md`,
`plan.md` and the round 2 and round 3 records. Each line carries `NAME NOT
IN TREE` beside the name, the marker the check reads; no other word of
those records changed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/worktree-guard.py#_brace_command_at`, `#_brace_spells_git` and `#_ONE_BRACE` — NAME NOT IN TREE, removed here | `hooks/worktree-guard.py#_segment_finding`'s one test; nothing reads what a brace spells or where it stands |
| `_finding_tree`'s brace branch, which parsed the words after a brace word as git | `hooks/worktree-guard.py#_finding_trees`, the union |
| `test_a_brace_in_no_git_word_stays_silent` — NAME NOT IN TREE, renamed here | `test_a_brace_in_any_word_is_the_brace_shape`, its claim inverted |
| §A's command-word sentences and the 34,633 figure | §A's reframed paragraph, its three costs and phase 7's figure with its method |
