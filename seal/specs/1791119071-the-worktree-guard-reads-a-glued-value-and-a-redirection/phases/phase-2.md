# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a2614c09 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build the word reader and its option table in `hooks/worktree-guard.py`, and
route `classify`'s `switch` and `checkout` arms, `switch_kind`'s and
`_bare_words` through it, with `hooks/cmdline_base.py` and S11 byte-identical
and no import of `hooks/cmdline.py` for the reduction. Rewrite §*Which
tree*'s first paragraph, the #678 sentence and §*Known limits* in the same
commit as the code, and move the pin. Add the `KINDS` rows, the `classify`
cases, the generated A4/A5 property built by extending `_redirections()` and
`_shapes()` rather than writing a second generator, A7 (reading `git -h`
through `subprocess` with `encoding="utf-8"`) and A8. Each new case seen red
at `94d7b2e0`; A6's comparison in a deleted probe; W1 settled by comparing
the two reductions over the generated shapes. If the generated cases read
sibling C's splitter, say which function they depend on.

## What this phase found

**W1: the two reductions agree everywhere, so `_bare_words` reads through
the local one.** Over every segment and merged view of every shape `_shapes`
builds for `RESTORES`, `ASKABLE` and this item's creations, switches and
twins — 50,568 views — `wide.unglued` plus `wide._without_redirections` and
the guard's `handed_words` gave the same words for every one (executed, a
deleted `test_tmp_*` probe). `_bare_words` is now a call to `handed_words`.

**Seen red at `94d7b2e0`** (executed: the module, as it stands at the end
of this phase, run with `94d7b2e0`'s `hooks/worktree-guard.py` copied over the
build's and then restored from the commit): 67 cases failed. 18 `KINDS` rows
— every stuck, aggregated-and-stuck and long-stuck spelling, `switch -c`
alone, a value, a `-b` after `--`, a bare redirection; the separate S3/L1/L3
rows stay green there, because the base's tree-blind reading takes the value
for a name. 28 of the 32 `classify` creation spellings (all but S1), both V
switches on `checkout`, five twins. The generated A4 case (6,854 silent
shapes on its first run) and A5 (891 twins asked). Four of the six `main()`
positions (R0, R1, R3, R4 glued; R4 spaced and R5 the base already read).
The R& case, because C subtracted the switch the frozen side read `2>` as
naming. A7, A8 and the four unit cases, because the table, the reduction and
the resolver did not exist; each of those was also shown red by the mutant of
the unit it pins (below). The two policy pins were red against the policy
text as it stood, before it was rewritten.

**Every unit added was mutated, one at a time, through `bin/mutation-check`,
and each break turned the module red** — 39 breaks across
`_redirection_width`, `handed_words`, `_long_option`, `read_switch_words`,
`switch_kind`, `classify`'s two arms, `_bare_words`, the table and the
operator list. The first pass left four survivors, and each got a case:
an ambiguous long prefix taking its first match (no table here has a
value-taking option first among an ambiguous set, so it is pinned on a
synthetic `_Options`), `-t` taking the next word (no switch spelled `-t
feature/x` was generated), `classify`'s `--` check (redundant unless a name
stands before the `--`), and an operator taken out of the copied list. On
that last one, `&>` taken out stays green, because a glued `&` is cut and
dropped before the operator is read; `<>` taken out turns three cases red,
and A8's docstring says so.

**One rule was taken out rather than tested.** The first draft resolved
`--no-…` as a negation. A negation takes no value and creates nothing,
which is exactly how a word git refuses reads, and no long name of either
subcommand begins with `no-`. No case could tell the two apart, so the rule
was dropped and `_long_option`'s docstring says why.

**A5 needed one more distinction than `spec.md` drew.** Where an `&`- or
`|`-led operator cuts the segment before a `--`, the frozen loop reads the
words before the cut alone: `git checkout feature/x <&1 -- README.md` is a
restore, and `classify` judges the switch to `feature/x` (32 generated
shapes). `94d7b2e0` did the same, so it is not this change's; the A5 case
holds only candidate C to §*Which tree*'s rule in those positions, and
§*Known limits* names the shape.

**A6: nothing that switches went quiet** (executed, a deleted probe running
the phase-1 sweep with the build's `hooks/`). Of the 20,729 switching shapes,
none is silent (7,025 at the base). 1,130 shapes the base asked are now
silent, all of four spellings: `checkout -- -b y` (579), `checkout
--conflict feature/x` (316), `checkout --conflict merge .` (226) and
`checkout -- feature/x` with the redirection glued to `--` (9). git switched
on none of them (phase 1's M1, and re-run for `checkout --conflict merge .`,
`checkout -->/dev/null feature/x`, `checkout --<<<word feature/x`,
`checkout --conflict 2>/dev/null feature/x` and `checkout -- -b>/dev/null
y`). 230 no-switch shapes are newly asked, every one with its redirection
before the subcommand, glued to it, or `&`-led — candidate C's positions,
where §*Which tree*'s rule asks a file's name as a branch's. At the base the
frozen side read the redirection word as a name and subtracted them.

**M1's two exceptions changed nothing in the table.** `--c` on `switch` is an
ambiguous prefix and reads as nothing; `-U`, `--unified` and
`--inter-hunk-context` take a value, as the table says, and §*Known limits*
names that `checkout -U 3 feature/x` is asked although git refuses it.

**What the generated cases depend on in `hooks/cmdline.py`.** Through
`wider_only_kinds` and the A5 case they read
`split_segments_with_separators`, `merged_view`, `drop_heredoc_bodies`,
`drop_comments`, `parse_git` and `_REDIRECTION` (A8 and `_redirections`).
Sibling C (#773) changes heredoc-body handling for the waiver reads in
`hooks/tokens.py`; none of these functions is that one. `_placed` builds
heredoc shapes (`<<EOF … EOF`), so if C's change ever reaches
`drop_heredoc_bodies`, these cases are where it shows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `_bare_words`'s own reduction through `wide.unglued` and `wide._without_redirections` | `hooks/worktree-guard.py#handed_words`, which gives the same words for all 50,568 generated views |
| the policy sentence naming `-b` or `-B` as the only creating options a `checkout` carries | `docs/worktree-guard-spec.md` §*Which tree*, the rewritten sentence, pinned by `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` |
