# 1789985781-the-gates-arm-list-is-maintained-by-hand — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | f30601b |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

A4, A7, and the documents — `skills/verify/SKILL.md`, the changelog fragment,
the `seal/ledger/` fragment. A4 red against a reason reduced to a category
word; A7 red against the gate breaking where no workflow exists. Plus
`CONTRIBUTING.md` §*What a change to a gate must carry*: `overview.md` carries
the four clauses for the pull request body, and the prompt budget is zero.

## What this phase found

**A4 and A7 were both green the moment they were written, and that is the
state §15 exists to refuse.** Neither could be shown red by the absence of
code, because both assert something the gate already did — a reason that
happens to be prose, a run that happens to print nothing. Four mutations gave
them their reds: a reason cut to `EXCLUDED`, a reason that is prose and names
nothing out of reach, the panel row filled from `PARTITION` when no workflow
is there, and the coverage line written the same way.

**A4 needed a second case, because the first one's rule is too weak to mean
what A4 says.** *Several words and not a marker* passes *this one is not worth
the trouble right now*, which says exactly as much as `EXCLUDED`. The second
case asks that a reason name something out of the gate's reach, against a
vocabulary of what those things are called here. What neither catches is
written into the docstring rather than left for a reader to find.

**Three rows of the shared ledger drifted, and `--reverify` re-stamped two
that nobody had read.** The lenient run reported `1 drifted` for
`seal/ledger.md`; three rows cite `broad_gate.py#gate`, and the report names
the coordinate once. Following the documented repair — re-read it, then run
`--reverify` — therefore writes *somebody read this* over rows the reader
never opened. All three claims were read here and all three hold, each with
its own `Re-read` marker saying what was checked. The silence itself is a row
in `seal/follow-up.md` for the owner, with the three candidate repairs and
what each costs.

**`the seal` cannot be written bare in a shipped file**, and the sweep that
enforces it reads scripts as well as documents. Three comments in
`broad_gate.py` and one sentence in `skills/verify/SKILL.md` were rewritten to
say whose. The rule is this repository's own, and the failing case named the
exact phrase each time.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/verify/SKILL.md`'s silence about what a seal does not cover | the four paragraphs added to §*The broad gate*, and the panel row they describe |
| the drift on three shared-ledger rows and two of this release's fragment rows | each row's own `Re-read 2026-09-21` marker, with what was checked |
