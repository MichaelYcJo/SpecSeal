# 1790815614-a-joined-projects-specs-is-read-and-never-taken — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | e3ebaf0b |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

The `Reference specs` row in `templates/config.md` (the table and a section:
grammar, `none`, the default, what it governs, the BDD-`specs/` cost); one
resolver in `hooks/config.py`, `reference_roots` and `under_reference_root`;
`survivor_check.py` leaving reference roots out of `corpus` and `corrected`
through one predicate, `WORK_ITEM_DIR` narrowed to `seal/specs/`; the standing
statement in `docs/review-chain-spec.md` §*The survivor sweep* gaining
*outside the reference roots* and the new cases on its `Enforced by:` line.
C1 red before the resolver exists, D1 red against the old walk. The pool size
on this repository before and after (Q2), and Q3 decided.

## What this phase found

**The default reaches a case that predates it.**
`test_a_specs_directory_outside_the_seal_root_stays_in_the_range` (round 1's
finding 4 of an earlier work item) asserted a deleted `docs/specs/login-flow/`
is measured. Under the ticket's default — every directory named `specs`
outside the root, at any depth — `docs/specs/` is a reference root and out of
the range, so the case went red. What it pinned is that `WORK_ITEM_DIR` is
anchored and does not read `docs/specs/` as a work item; that property still
holds and still matters where a repository puts its `specs/` back. The case
now declares `Reference specs | none` and pins exactly that. `overview.md`
records it as a divergence.

**A case that is red against the old code is not proof the fixture works.**
The first top-level-`specs/` case went red against `6fd620bd`'s module — and
stayed red against the new one, exit 0 both ways, because a single verbatim
sentence never cleared the floor. The old module's silence came from
`retired_by_rule`; the new module's silence came from the score. Rebuilt on
the deletion shape the `docs/specs/` case uses, it is red against the old
pattern and green against the new, and both `WORK_ITEM_DIR` mutations turn it
red.

**The resolver does not import `optin`.** `hooks/config.py` is loaded by path
by scripts that bring `blocks.py` along; a third sibling is a new way for a
copy to break. `HOME = "seal"` is spelled there and held equal to
`optin.HOME` by a case.

**Q2: this repository has no reference root.** `survivor-check --range
cd24f516..HEAD` examined 555 files at `6fd620b` (old module) and 556 at
`f0e626c` (new module, one test file added between); at `f0e626c6` the pool
is 556 with the predicate and 556 with it switched off, from a read-only
script in the scratch directory. No tracked path sits under a `specs`
directory outside `seal/`. The ticket's 530 is not reproduced.

**Q3 left as is.** Under the default, a team's `specs/x/rounds/` is out of
both sides before `records_a_past_round` is asked; under `none` it is read as
a past round, the shape it always matched.

**`seal/releases/0.15.1.md` C2 was false after the change and is corrected
in place**: an ungathered pre-0.4.0 `specs/<id>/changelog.md` is out of the
sweep under the default. Eighteen other rows across eight release files were
re-read and re-stamped with a dated note; their claims hold.

Two mutations of the first mutation list would have survived the cases as
first written — the empty-`home` guard (no `config.md` in the process's own
directory made it unobservable) and the dedupe. Both got an assertion before
the run; twenty-one mutations, twenty-one red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `WORK_ITEM_DIR`'s top-level `specs/` arm, the pre-0.4.0 spelling of a work item directory | `survivor_check.py#WORK_ITEM_DIR`'s comment and the module docstring's **A reference root.** paragraph; row D1 of `seal/ledger/1790815614-….md` |
