# 1791384156-config-rows-coordinates-and-headings-have-one-reader — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | d515308a |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 4: the heading rule — `unverified_check.py#heading_level`
lifted out of `_paragraph_ends_at`; `headings`, `chain_check.py#heading_level`,
`survivor_check.py#ledger_rows`, the fold check's heading pattern and
`payload_meter.py#heading_starts` read it; `tests/commonmark_oracle.py`
answers the ATX heading lines from `heading_open` tokens; a property case
holds the rule over the frame's shapes, a seeded corpus and every tracked
`.md`, and asserts every setext heading in the tree is a front-matter line.
Verified by S9 and S10, red first.

The session was stopped by a usage limit in the middle of this phase, with
the edits uncommitted, and resumed on the orchestrator's message; the
resumed segment read `git status` and the staged state before going on.

## What this phase found

**The rule agrees with markdown-it on every shown line of the tree.** Over
777 tracked `.md` files, comparing `heading_level` on each line the oracle
does not hide with the parser's top-level ATX headings: 0 disagreements
(probe, then the case). The setext count is the frame's: 35, all front
matter.

**One limit a line-local rule cannot see.** A heading indented one to three
spaces under a list item is the item's content. A generated corpus of 3,000
documents disagreed on exactly that shape and nothing else (probe). The
property module states it, skips such a line where a list item stands above
it, counts the skips so the generated corpus is seen to reach it, and the
tracked-file case requires the tree to hold none. No reader of a section in
this plugin reads a list item's content as structure, so the cost is a
document someone writes that way, and the case names it the day it lands.

**`readable` blanks 41 heading lines in 15 tracked files that markdown-it
shows** — `templates/config.md` and spec files that quote fences inside code
spans, found while measuring with `readable` before the comparison moved to
the oracle's own shown lines. That is the live-line family #872 holds (which
lines a reader hides), not the heading rule, so it is named there and left.

**The fold check's statements were already right.** Its own pattern was
CommonMark's; its S9 case is a pin and says so. The payload meter's
`^#{2,3} ` missed an indented heading and one followed by a tab, which the
one rule reads.

**A suite-wide guard was red from phase 1.**
`tests/test_every_reader_ends_a_line_where_gfm_does.py` names every
`splitlines` call left in a shipped script, and phase 1's `seal.py#mode_refusal`
added one; phase 1 ran the modules it touched and not this one. It is named
now with `with_row`'s reason (fragment row K21). Running the eight guard
modules the orchestrator listed found it, and found the records case red on
`plan.md`'s `heading_rule`, a name phase 5 brings into the tree.

**Direction and prompt budget.** A section's end runs past a `#NNN`-led
line to its real end: more rows inside `## Verdicts`, `## Not verified` and a
fold statement — the stricter direction; `unverified-check` now names such a
line as one inside the table that is not a row. No gate gains a stop.
Budget 0.

**Seen red (§15).** Against 5623d728's five readers (`git stash`): 30 cases
failed and 4 passed — the fold pin, the setext case (a pin over the tree),
and two parametrizations of the shapes table whose answer did not depend on
the missing name. The property cases failed there for want of
`heading_level`. `mutation-check`, every verdict `red`: the rule's
three-space bound, six-hash bound and space-or-end condition removed, and
each reader put back on its old spelling.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `fold_check.py#HEADING` · NAME NOT IN TREE | `unverified_check.py#heading_level`; 0.15.3's F1 row is corrected in the fragment |
| `payload_meter.py#HEADING` · NAME NOT IN TREE | `unverified_check.py#heading_level` at `payload_meter.py#SECTION_LEVELS` |
| the inline ATX test in `_paragraph_ends_at`, and `startswith("#")` in `headings`, `chain_check.py#heading_level` and `survivor_check.py#ledger_rows` | `unverified_check.py#heading_level` |
