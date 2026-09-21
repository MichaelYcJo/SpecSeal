# 1789985781-the-gates-arm-list-is-maintained-by-hand — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 99f9bf1 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The arms the partition found missing, whatever the count. A5 red against the
gate as it stands; A3 red when an arm is deleted while its row stands.

## What this phase found

**A5's red is the defect itself, and it drew the stamp.** The fixture is a
branch whose merge resolved `seal/ledger.md` by taking one side and reverted
the other side's correction. Against the gate as it stood, the run came back
**exit 0 with the seal drawn** — every other arm green, the ledger row
reading `1 ok . 0 broken`, because the restored row's hash is *correct* for
the text that was restored. That is the whole of #468 in one run: the seal is
not wrong about what it checked, it is short.

**Two arms, not six, and the line that decides it is whether the plugin ships
the check.** `correction_check.py` and `seal.py` are under `skills/`, so the
gate runs the same script CI runs and there is no second reader to drift. The
other four local-answer steps run `.github/scripts/…`, which exists in this
repository and in no other clone of the plugin.

**The `corrections` arm takes the survivor arm's range, and inherits its
known non-equivalence.** The workflow skips both steps when the base is
`main`; the gate skips neither. That difference predates this work — the
survivor arm has had it since it was added — and closing it is the class
*does a mirrored arm ask its step's question*, which `spec.md` §*What this
repair cannot see* puts outside this work item. Named here so the next reader
does not take the new arm for the place it entered.

**Corrected 2026-09-21 by review round 1, finding 2**: this paragraph sent
that class to #423, which ships in this release and is about the base the
gate resolves rather than about a guard. Its home is **#473**, opened for it.

**The `mode` arm needed a behavioural case of its own.** A3 is structural: it
says the arm named in a row is an arm `gate()` runs. Deleting the arm reddened
A3 and nothing else, which is a pin only a reader of the source can break. The
second case runs the gate over a repository whose `Mode` row says `local`
beside a committed root — the one direction of that disagreement CI can ever
reach — and both cases are red when the arm goes.

**A3 is written in both directions too.** An arm the gate runs and no row
accounts for is as much a hole as a row naming an arm that does not run: the
`suite` and `ledger` arms answer the workflow's *other* jobs, so they are
named in the case rather than left to be inferred from their absence.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the gate's silence about a merge that dropped a correction | the `corrections` arm, and `PARTITION`'s row for that step |
| the gate's silence about a `Mode` row that disagrees with the folder | the `mode` arm, and `PARTITION`'s row for that step |
