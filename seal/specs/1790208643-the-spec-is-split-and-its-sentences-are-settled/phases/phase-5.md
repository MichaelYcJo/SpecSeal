# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 1ccaa24f |
| Ran by | specseal:smith on Claude Opus 5.5 (1M context) — the agent as the spawn prompt's first line names it, the model as the commit trailer it prescribes names it |

## What this phase was asked

#466's pin, one population wider.
`tests/test_the_contributor_has_a_procedure.py`'s release-branch case reads
the files `tests/test_release_hygiene.py#LOADED` names, through that
module's `tracked` (imported, not copied). It keeps the four surfaces as the
loud first parameter set and allows the three history phrases by name, and
it is seen red over a planted `skills/x/SKILL.md` and over this tree before
`correction_check.py:23` changes. `correction_check.py:23` and
`bin/correction-check:10` spell `release/vX.Y.Z`, and M3 is recorded.

## What this phase found

**The four standing names are the frame's four** (executed: `git ls-files`
over `LOADED` with `grep -nE 'release/v[0-9]+\.[0-9]+\.[0-9]+'`):
`agents/smith.md:104` (the rider's dated measurement),
`docs/issues-and-milestones.md:370` (*the branch `release/v0.3.0` shipped as
0.2.0*), and `correction_check.py:23` (`release/v1.2.3`, illustrative) and
`:133` (`release/v0.9.3`, a merge its history walk found).

**What was built** (read). The existing parametrised case stays as it was:
the three `CONVENTION_SURFACES` must name `release/vX.Y.Z` and no concrete
branch. Beside it are `RELEASE_BRANCH`, `RELEASE_BRANCH_HISTORY` (one
whitespace-collapsed sentence per file, removed from that file's text before
the search, so the name is allowed only inside its sentence) and
`concrete_release_branches(root)`, which reads `tracked(*LOADED, root=root)`.
Three cases use them. The tree case fails on any name outside a history
sentence. The fixture case builds a real git tree holding a skill with a
usage line naming `release/v1.2.3` beside the issues document's history
sentence, and asserts exactly the skill is named. The history case is
parametrised over the allowlist and fails when an allowed sentence is gone,
so an allowance cannot outlive what it allows.

**Seen red over this tree before the spelling changed** (executed, `bin/test
tests/test_the_contributor_has_a_procedure.py -q -p no:xdist`, exit 1,
`1 failed, 21 passed`). The one failure named
`skills/evidence-check/scripts/correction_check.py: release/v1.2.3`, and the
three history names were allowed. After `:23` and `bin/correction-check:10`
spell `release/vX.Y.Z`, the three phase-5 modules gave `118 passed` (the
procedure, hygiene and correction modules).

**Every added unit mutated one at a time, restored from held bytes and
sha256-compared** (executed, a scratch script run from the repository root;
`tests/__pycache__` cleared between mutations). The six below were killed:

| Mutation | Result |
|---|---|
| `review_chain_text` reads only the run document | killed (`1 failed`) |
| `REVIEW_CHAIN_DOCS` loses the record document | killed |
| the history sentence is not removed before the search | killed |
| `RELEASE_BRANCH` matches nothing | killed (the fixture case) |
| the population narrowed to one surface | killed (the fixture case) |
| one allowlist entry dropped | killed (the tree case) |
| the direct-answer module's widened gone half reads its own file only | **survived** |

The survivor is an absence clause, and no mutation of the reader can kill an
absence on a tree where the forbidden sentence stands nowhere. What kills it
is the sentence planted in a sibling, which phase 2 did
(`test_each_carrier_says_what_the_direct_answer_requires[parts0]` red with
*nothing required; the declaration is printed* appended to the run
document). The same holds for the other eleven widened absences, each seen
red by that probe.

**M3** (executed, `git log --oneline -S'release/v0.22.0' -- hooks/cmdline.py`):
`716d8548 Initial commit`, the framer's reading. `hooks/` is outside the
population by Q2's default, so the four mentions stand, recorded here and not
corrected.

**The ledger** (executed): no anchor drifted in this phase, and
`evidence-check --strict .` exit 0, `1767 ok`. `uvx ruff check` and
`uvx ruff format --check` over the test module and `correction_check.py`,
exit 0 each.

**For the fragment, drafted and written at phase 6**: the widened pin, on
`tests/test_the_contributor_has_a_procedure.py#concrete_release_branches`,
`#RELEASE_BRANCH_HISTORY` and its three cases.

**What `CLAUDE.md` needs: nothing from this phase.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `release/v1.2.3` in `correction_check.py`'s usage line and `bin/correction-check`'s comment | the same two lines, as `release/vX.Y.Z` |
