# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | f272342 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The ledger, the tracker row, and the records. A prose move of this size was
expected to turn rows DRIFTED, and a row whose anchor the change **removes**
is removed in `seal/ledger.md` with the new claim written into this work
item's own fragment. Tick only the `#265` row of `docs/flow.md`'s 0.9.3
section.

## What this phase found

**Two anchors BROKEN, three rows, five DRIFTED — and the branch's base is
clean, so all of them are this branch's.** Confirmed by running the checker
against `d2f5712` in a throwaway `--no-local` clone: 932 ok, 0 drifted, 0
broken. That is what made `--reverify` on `seal/ledger.md` safe to run at all;
the narrowing exists to keep `--reverify` off a row somebody else has to
judge, and here there was no such row.

**The three removed rows came back from `--reverify` with the hashes they
had.** `b1368831`, `c0dc63a1`, `21ad749e` and `98a430c2` are the same values
the removed rows carried, against `orchestration.md` instead of `SKILL.md`.
That is the strongest statement available that the prose moved unchanged, and
it is a by-product of the coordinate being content rather than position.

**One removal falsified a sentence, and the sentence was not a count.** The
`1788277657` block's intro reads *rows for the work item that wrote the
per-segment bars and the resume rule*, and the resume-rule row was one of the
two removed. A note under that intro now says where the row went. The
`1788433011` block's header comment says *five rows* over a block of nine, so
it was already inaccurate and removing L4 does not newly falsify it — left
alone rather than tidied, because a pre-existing inaccuracy in a folded
comment is not this branch's to rewrite.

**The rider in `agents/smith.md` fired.** Editing §Phases for the
reference fix drifted the stamp on the `# RIDER:` comment at line 60. Read:
it asks a future editor not to quiet the commit-gate waiver example by
breaking it, and names the owner's Q2 as its own resolution. This change does
not touch the example, so the rider was re-stamped rather than acted on —
which is the branch that drifted it saying so, instead of a later branch
finding a stale stamp with no account.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Three rows from `seal/ledger.md`, whose anchors' headings left `skills/code-review/SKILL.md` | `seal/ledger/1788873630-the-orchestrator-sections-leave-the-reviewers-payload.md`, re-stated against the file that holds the prose, with the released sections named as where their verification history stays |
| Nothing else | none |
