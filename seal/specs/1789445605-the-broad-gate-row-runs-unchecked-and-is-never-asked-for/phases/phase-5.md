# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | <filled by the commit that closes this phase> |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

A session that meets the refusal brings it to a person.
`broad_gate.missing_row`'s sentence stops telling the reader to write a
command and says whose the row is, naming `/specseal:config`;
`agents/sealer.md`'s exit-2 bullet and `skills/code-review/orchestration.md`
where the sealer is spawned say the refusal goes back to a person. Plus the
records: `changelog.md` and `seal/ledger/<id>.md` in this directory, and
`overview.md`. Red first by restoring the old sentence. Then
`bin/evidence-check --strict .` for the fifteen drifted rows.

## What this phase found

**A case that claimed to pin one bullet pinned the whole file, and the
mutation loop is what caught it.** `test_the_sealer_is_told_the_row_refusal_
is_a_persons_and_not_its_own` asserted *would not run as the command it reads
as* against `flat(read(sealer))`. Deleting that clause from the exit-2 bullet
left the case green, because the paragraph this phase adds below carries the
same phrase. The case now slices the bullet out and asserts against that. This
is `agent-contract` §15's own failure met while following §15 — a case that
passes against the very defect it was written for — and the only thing that
found it was breaking the document.

**Q2's number did not survive measurement.** `spec.md` §*Data & interfaces*
predicted fifteen drifted rows by anchor, counted on 2026-09-15 before the
build. `bin/evidence-check --strict .` reported **eight drifted anchors**
across sixteen citations, and the composition differs in both directions:
`broad_command` and `first_command` never drifted, because this work does not
touch them; the Bootstrap's eight rows report as one anchor line, not eight;
and four anchors nobody predicted did drift —
`templates/config.md#"# Repository config"`,
`skills/config/SKILL.md#"## Procedure"`,
`skills/code-review/orchestration.md#"# code-review — the orchestrator's
half"`, and `tests/test_the_rules_have_one_owner.py#RULES`. That is
`agent-contract` §5 on an aggregate: the number could be checked while the
claim it stood for could not.

**One claim went with the code and was removed rather than re-pointed.** S14
of work item 1788354065 said the bootstrap *asks the mode question — shared or
local, since #80 — and then the parity question, **and nothing else***. Phase
4 made it ask a third. The row is removed from `seal/ledger.md` — the one edit
to the shared file `CLAUDE.md` permits — and the new claim is a row of this
work item's fragment. Every other drifted claim was re-read and held; only its
hash moved, and `--reverify` moved it.

**`--reverify` recomputes hashes and does not touch the `Checked` column.**
Measured on the diff: fifteen rows changed hash and every `Checked` date
stayed where it was. The date is not typed by hand here — the re-read is
recorded in this record and in the fragment instead, which is where a reader
can see who re-read what and when.

**`seal/ledger/` did not exist.** This work item opens it, and the fragment
carries no header of its own: every row is a content anchor, so there is
nothing for a header to declare and `fold_ledger.py` writes the `###` at the
release.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `broad_gate.missing_row`'s *Write the repository's own broad command into it as one shell command line* and the row it printed to type | nowhere in the message — it was the instruction #401 watched a session follow. `/specseal:config` and `templates/config.md` §*Choosing a value — the criterion*, both named in the new text, are where a person gets the same help |
| `seal/ledger.md`'s S14 row for work item 1788354065, whose claim ended *and nothing else* | the last row of `seal/ledger/1789445605-…md`, which states what the bootstrap asks now |
