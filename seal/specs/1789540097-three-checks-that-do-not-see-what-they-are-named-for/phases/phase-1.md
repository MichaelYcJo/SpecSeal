# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9d90db85 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#413. `test_both_ampersand_cells_name_both_shells` gains, per cell, an
assertion tying each shell name to the consequence that is that shell's, and
what the case still cannot see is written beside it. The existing presence
loop stays. The issue's paste-ready patch asserts over the raw table row and
this phase asserts over the flattened one, because the case's own presence
loop already flattens.

## What this phase found

**The frame's four pinned sentences are in the document exactly as it says
they are**, at `templates/config.md:206` and `:225` — `` `/bin/sh`
backgrounds ``, `` `cmd.exe` separates ``, `` That is `/bin/sh` `` and
`` `cmd.exe` sequences ``. Nothing had to be reworded to make the assertions
land, which is what `spec.md`'s A12 asks for on the other module and holds
here too.

**Flattening the two tail assertions was not free of consequence, and the
consequence is one a reader should know.** Both existing assertions —
*the second one's status* and *nothing is left running* — read the raw row
before this phase, so a hand-rewrap of either 300-column cell would have
reddened them for a reason with nothing to do with what they pin. They now
read the same flattened string the presence loop and the two new assertions
read, so the case has one input rather than two.

**What the case still cannot see is recorded in the docstring rather than
left to be found.** The `cmd.exe` half of both cells is unmeasured, and work
item `1789445605-…` already records it as unmeasured with the
`windows-latest` job named. This case pins that the document ATTRIBUTES each
behaviour to a shell; it does not and cannot pin that the behaviour is that
shell's. Asserting the attribution is what makes a later correction of the
claim visible instead of silent.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the presence loop and both tail assertions stay; the tail pair changed only which string it reads | none |
