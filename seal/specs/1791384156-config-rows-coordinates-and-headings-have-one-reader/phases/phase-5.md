# 1791384156-config-rows-coordinates-and-headings-have-one-reader — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 3327c81e |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 5: the checker reads headings by the rule on shown lines — a
`heading_rule` switch beside `fence_rule` with a vendored twin held equal;
`heading_path`, `text_regions`, `file_units`, `citation_for`,
`content_matches` and `resolve_unit` compute `.md` regions over
`gfm_lines(unquoted(text))`; `pact_check.py#clause_hash` inherits. Then the
released rows: `evidence-check --strict .` names each drifted or broken
heading-path row, `--reverify --into` writes the `Re-read ·` rows, and the
rows citing `agents/warden.md`'s fenced `## Verdicts` and `## Paste-ready
fixes` get `Corrected ·` rows re-pointed to `## Report`. Verified by S8, S11
and S12's second grep.

## What this phase found

**Headings on shown lines, text on written lines.** `markdown_lines(text)` is
`gfm_lines(unquoted(text))`. `heading_path` and `file_units`' `.md` arm read
it whole; `text_regions` matches an anchor's text on the lines as written
and asks the heading rule of the shown line, so an anchor on a line inside a
fence still finds its paragraph, as it did. Every region is hashed over the
lines as written. `content_matches` needed no edit: it reads `file_units`
and hashes the raw lines.

**The released rows moved by exactly the frame's bound.** `evidence-check
--strict .` after the change: 24 heading-path citations DRIFTED —
`CONTRIBUTING.md` §*Running the checks* (16, the section now running past a
fenced `##` to its real end), `agents/warden.md` §*Report* (4),
`README.md` §*Shared or local* and its Korean twin (2 each) — and 4 BROKEN,
the rows on the fenced `## Verdicts` and `## Paste-ready fixes`. 28 in all.
Each drifted claim was read against its section and holds; each is a
`Re-read ·` row in the fragment. The four BROKEN rows, and 0.11.4's row that
recorded this very defect as a known limit, take `Corrected ·` rows: the
warden rows re-pointed to `## Report`, the limit row restating the repaired
reading. R7 of 0.8.1 is the better for it: §*Report* now holds the two
terminal lines the row claimed and its old anchor stopped short of.

**`--reverify --into` wrote a `Re-read ·` row for two rows whose claim did
not hold or whose family was being corrected** — 0.11.4's limit row and
R7's drifted `## Report` coordinate — because it reads hashes, not claims.
Both were taken out of the fragment before the commit and replaced by the
`Corrected ·` rows; a reader of `--into` output has to read each written
row's claim, which is what the procedure already says.

**S12's heading grep exempts lines the spec did not list by name**: the
fold's and the gathered changelog's own `## X.Y.Z` lines (spec Out names
them as a family), the fold's demotion of a fragment's headings, and
YAML and Python comments in `deferral_check.py` and the rider check. The
fold's demotion is the one exemption that is a markdown-heading reader: it
rewrites a fragment's heading bytes at the release, reads `^(#{1,6})\s`, and
moving it onto the one rule changes what the fold writes for an indented
heading. Left, and named in `overview.md` §*Not done*.

**Direction and prompt budget.** A region ends where the renderer's section
ends; a row anchored on a quoted heading is BROKEN until re-pointed. No gate
gains a stop. Budget 0.

**Seen red (§15).** The S8 cases and the twin case ran against 5623d728's
checker (`git stash`): all three failed. The heading grep's rule, run over
5623d728's scripts by a probe, named the six old spellings. `mutation-check`:
red for `resolve_unit` on raw lines, `file_units` on raw lines, the twin's
three-space bound, and — after cases were added for each — `text_regions`'
heading arm and `clause_hash` on raw lines; one equivalent mutant,
`citation_for`'s heading trail on raw lines, recorded in row K23.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the checker's own `^(#{1,6})\s` | `evidence_check.py#heading_rule` (the shared rule, or `vendored_heading_level`) |
| the units `agents/warden.md`'s fenced `## Verdicts`, `## Executed probes`, `## Deferred` and `## Paste-ready fixes` were to the checker | no unit: they are example headings in a fence; the four rows citing two of them are corrected in the fragment |
