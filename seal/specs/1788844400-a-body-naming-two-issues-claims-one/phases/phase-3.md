# 1788844400-a-body-naming-two-issues-claims-one — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | a7c8190 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The prose signpost in the document a person writing a pull request body would
open, the changelog fragment, the ledger fragment, and the open questions —
each as a fragment under this work item, never appended to `CHANGELOG.md` or
to `seal/ledger.md`.

## What this phase found

**`tests/test_no_real_identifiers.py` caught the prose explaining why the
fixture was not committed.** The spec and the test module both said PR #162's
body is not a fixture *because it carries a `<name>.ai` session URL* — and
naming the domain is the thing that check forbids, wherever it appears. The
sentence now says *a domain outside the fixture allowlist* and names none. The
allowlist was not extended: the repo rule says never to make that test pass by
adding to it, and here there was nothing to add — the fixture is not wanted in
the tree at all.

That is the check catching exactly what it exists for, one layer up from
where anyone would look for it: not a fixture carrying a real identifier, but
the note explaining that a fixture must not.

**The signpost quotes the failing shape inside code spans**, so a pull request
body quoting `docs/issues-and-milestones.md` is not itself reported as an
instance of the defect — which is the property the fence and span cases pin,
demonstrated by the document that describes them.

**Nine ledger rows, re-verified narrowed.** `evidence_check.py --strict
--ledger 'seal/ledger/1788844400-….md' .` reports `9 ok · 0 drifted · 0
broken`, and prints the one ledger the narrowing did not read
(`seal/ledger.md`), which is the orchestrator's at the pull request.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
