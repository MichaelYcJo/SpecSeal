# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 7

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-7.md -->

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | `3194525` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The work item's own records: `changelog.md` and
`seal/ledger/1789455558-….md` in this repository's fragment convention, and
`overview.md` carrying the corpus measurements and every divergence. Verified
by `bin/evidence-check --strict .` with the exit read directly, red-first by
changing one character in one new row's hash, then
`bin/unverified-check --baseline origin/release/v0.12.0`.

The two divergence rows already owed were handed over rather than re-derived,
and the measurements were copied from `questions.md` Q3/Q4/Q5 and from
`phases/phase-2.md` and `phase-3.md` rather than re-run against a tree that has
moved.

## What this phase found

**`--strict` cannot reach exit 0 on this branch, and that is the third
divergence.** The run is **exit 2, `1267 ok · 7 drifted · 0 broken`**. All
seven drifted anchors are units this branch changed and `seal/ledger.md`
already cites — `close`, `seal`, `fix_table`, `reach_forward`, and three test
units. Drift is the mechanism firing correctly rather than a defect: it says
somebody moved the content under a claim, go re-read it.

**So the claims were re-read, all thirteen rows that cite those seven
anchors.** Twelve still hold. Two are worth naming because they read as though
they might not and do not: S6's *the number of `raise Refused` sites in `seal`
is six, counted rather than described* survives a reworded message, because
rewording changes no site; and the fix-table row's *`chain.SEPARATORS` … is not
widened* survives phase 3, because the period went to the two call sites and
the constant is untouched.

**One claim is false, and it is why this branch touches `seal/ledger.md` after
all.** The row ending *…and the case that pins it asserts the whole output
holds no bare `the seal`* cites the assertion phase 5 deleted. `CLAUDE.md`
§*a change writes fragments* states the exception in as many words — a branch
that removes code an existing shared row cites must touch that file to leave
the ledger true, the row is removed there, and the new claim is written into
the branch's own fragment. That is what happened: one line deleted, nothing
else in the file changed, and the superseding row is the fifth in the
fragment.

**The premise the spawn gave for keeping the file closed was the thing that
turned out false.** It said nothing on this branch removes code an existing
shared row cites. One thing does, and the ledger is what found it — which is
the whole point of a ledger and the reason to have re-read rather than
re-verified blind.

**The six remaining anchors were deliberately NOT re-verified**, and the
reasons are three. `--reverify` rewrites hashes and never the `Checked`
column — a gap a standing `# RIDER:` at `evidence_check.py#reverify` measured
on six rows of this very file — so running it would record a re-read nobody
could see. It would put a multi-row edit to the shared file on a branch while
two others are in flight, which is what the fragment convention exists to
prevent. And **CI runs the check without `--strict`**, where drift is exit 1
and a printed warning; only exit ≥ 2 fails the workflow, so nothing is broken
by leaving them. The reading is recorded so the owner's re-verify at the
release is one command over rows already judged.

**The records arm refused three files and all three were this work item's own.**
`handoff.md:61` and, once written, `overview.md`'s row about it: naming
`test_both_ampersand_cells_name_both_shells` in backticks makes a document <!-- NAME NOT IN TREE: the third instance of the very class this paragraph describes — a record that reports the name acquires it. The case lives on `fix/401-402-…`, which this branch did not cut from. -->
say a name the tree does not carry, and a document that reports the problem
acquires it. Both lines now carry `NAME NOT IN TREE` with the reason — the
case module lives on `fix/401-402-…`, which this branch did not cut from —
and the arm reports **0 refused**. The third was this record itself, caught only because the check was re-run after the commit — which is the argument for running it again on the tree you are handing over rather than on the one you were writing against.

**The fragment reopens `seal/ledger/`, which the 0.11.5 fold emptied.** Six
rows, one per ticket, cut by what each claim is about rather than by the phase
that wrote it. Scoped, they read `23 ok · 0 drifted · 0 broken`, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md`'s row claiming the seal refusal's pin asserts the whole output holds no bare `the seal` — the assertion is gone, so the claim is false | `seal/ledger/1789455558-….md`, row 5, which carries the superseding claim: the sweep owns the rule alone, and the module-local pins that remain are the two positive ones plus `before the sealer runs` |
