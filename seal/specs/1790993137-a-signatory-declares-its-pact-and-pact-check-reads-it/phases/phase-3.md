# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 9f83d171 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 3, the pact and its anchor: `PACT_ANCHOR_RE` beside
`ANCHOR_RE`, blanked at every enumerated site; `templates/pact.md`; a
`pact.md` line in every layout tree (`README.md`, `README.ko.md`,
`skills/implement/SKILL.md`, `templates/seal-README.md`, `seal/README.md`,
`docs/one-root-by-lifetime.md` and its `.ko` edition, enumerated with
`git grep -n 'parity.md'` in tree drawings); `templates/config.md`'s *What no
row governs* gains the anchor; one sentence in `templates/sdd-spec.md`'s
Grounding on how a pact clause is cited. Verified by S7 as an `evidence-check`
case, red with the blanking removed, and a case asserting `ANCHOR_RE` finds
nothing in a set of pact anchors. `questions.md` Q11 is this phase's.

## What this phase found

**Q11, answered: the blanking class is three readers, four expressions.**
Enumerated by construction over the repository's Python outside `tests/`:
every `.sub(` of a pattern whose name holds `ANCHOR` or `COORD`, every read
of `OLD_COORD_RE`, and every caller of `old_format_rows`, `malformed_rows`
and `migrate`. The members are `evidence_check.py#old_format_rows`,
`#malformed_rows` (its blanking, and its *cites no coordinate* branch, which
read `OLD_COORD_RE` over the raw cell and now reads it over the cell with
pact anchors blanked) and `#migrate`. `hooks/ledger-migrate.py` and
`reverify` reach the class only by calling those functions. Every other
`ANCHOR_RE` reader (`check_text`, `reverify`'s own walk, the records arm's
`stated_stamps` and `file_claims`, `hooks/root-migrate.py#repoint`,
`survivor_check.py`) only finds `ANCHOR_RE` matches, so a pact anchor is
passed over there by the grammar alone. `fold_ledger.py#SELF_ANCHOR_RE` and
`settle.py#COORDINATE_RE` are copies of the coordinate shape that read only
their own matches, and neither can match inside a pact anchor for the same
reason.

**A look-behind keeps a word ending in `pact` out.** `compact:x/"## A"@…`
is prose, and `PACT_ANCHOR_RE` opens with the same look-behind
`fold_ledger.py#SELF_ANCHOR_RE` uses. The hash takes six to twelve hex
characters, the width `ANCHOR_RE` takes, so the two grammars agree on what a
hash is.

**`blank_pact_anchors` keeps every offset.** `migrate` splices by position,
so the blanking writes as many spaces as it removes; the other two sites do
not need it and get it anyway, which keeps one helper.

**A pact anchor written in `Code grounds` is not a refused coordinate**, and
a cell holding nothing else still *cites no coordinate*: a clause citation is
not code grounds, and the remedy that message prints is the right one.

**My own ledger row tripped the class it describes.** P5's first wording
spelled a version and a line number in prose, which `old_format_rows` read
as an old coordinate in the fragment; the row was reworded. It is the shape
the S7 case pins, met where no pact anchor surrounded it.

**The layout case derives its drawings.** A new case,
`test_every_layout_tree_that_draws_parity_draws_the_pact`, finds the
drawings with the `git grep` the plan named, minus the work items' records
and the changelog, and asserts each has a tree line naming `pact.md`. It
found seven, the seven the plan listed.

**Ledger rows this phase drifted (Q13, phase 3).** Twenty rows across
`seal/releases/0.4.0.md`, `0.5.0.md`, `0.6.0.md`, `0.8.3.md`, `0.15.3.md`,
`0.15.4.md`, `0.16.0.md` and `0.17.0.md` cite the three blanking functions,
`templates/config.md`'s two regions, the seal README template, the four
drawings and the implement skill's layout section. Each was read against the
edit, each claim holds, and each carries a dated note; the one that needed
words was `0.15.4.md`'s `MALFORMED` row, whose claim is about a coordinate no
pattern parses and a pact anchor is now a third pattern's match. Seven of
the `0.5.0.md` rows were re-read in phase 1 too and carry both notes.

**Verified, executed.** Red: `mutation-check` broke `blank_pact_anchors`
(3 cases red), then removed it from each site alone (`old_format_rows` 3,
`malformed_rows` 1, `migrate` 1). The layout case was red with the seven
drawings stashed. Green: the 86 modules naming a file this phase touched
gave 4480 passed, 76 skipped; the phase's module gave 10 passed.
`evidence-check .` reported nothing drifted, broken, old-format or malformed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
