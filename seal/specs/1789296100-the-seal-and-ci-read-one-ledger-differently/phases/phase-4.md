# 1789296100-the-seal-and-ci-read-one-ledger-differently — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `b07f0d0` |
| Ran by | unknown — the spawn prompt named no model, and the value is the spawning session's to fill |

## What this phase was asked

The records, in this work item's own fragments: `changelog.md` here and
`seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md`, with
`CHANGELOG.md` and `seal/ledger.md` not appended to. `overview.md` closed.

## What this phase found

**The feature caught its own branch, and that is S1's strongest verification.**
`bin/evidence-check .` over the real repository came back **exit 1** with four
drifted rows and the sentence as its last printed line — not a fixture, the
tree this work was written in. The same run after the re-verification below
came back **exit 0, 1153 ok · 0 drifted**, with the sentence absent. S1 and S3
both hold against the repository as well as against the fixtures.

**`seal/ledger/` did not exist in this repository and this work item created
it.** The directory is named by `CLAUDE.md`, by `seal/ledger.md`'s own header
and by the checker's default glob, and no branch had yet written a fragment
into it. Nothing needed adding for it to be read: the first run over the new
file reported it beside `seal/ledger.md` under its own heading.

**Two of the four rows were written with a coordinate that produced no row at
all**, and the run said nothing. `ANCHOR_RE` takes a bare identifier at the
major level and **only a quoted string after the `>`**, so
`…#main>LENIENT_NOTICE@…` and `…#gate>EVIDENCE@…` matched nothing: the check
reported `3 ok` where five coordinates were present, `--reverify` rewrote three
hashes and named neither missing row, and the exit code stayed 0. Quoting both
minor anchors brought it to `5 ok` with nothing else changed.

That is a second trigger for a silence `seal/follow-up.md` already tracks from
the other end — a hash that is not eight hex characters. One instance came from
the hash and one from the locator, which widens what a fix has to catch, so the
measurement was added to that existing row rather than opening a second one.
`spec.md` scopes the defect itself out and it stays out; what is recorded is
evidence for the person who decides what to call it.

**The gate's ledger call site is in `gate()`, not `main()`.** `spec.md`
§*Data & interfaces* names `skills/verify/scripts/broad_gate.py#main` as a
coordinate this work builds on. `main` there is lines 644-678 and does not
contain the call; `gate` is lines 516-641 and does. The ledger row carries the
correct anchor with the finding in its Notes cell, and the structural case
reads neither — it walks from `checks[LEDGER]` until the parentheses balance.

**Seven `seal/ledger.md` rows drifted under this work's edits, and all seven
claims still hold.** Each was re-read against the changed section before
`--reverify` was run, and each row's `Checked` cell gained `2026-09-13` with
the grounds in its Notes:

| Row | Why the claim survives the edit |
|---|---|
| the two entry points a fix pass closes on | `main` gained one printed line under an exit code that did not move |
| S9 · the four documents that draw the root list `config.md` | both READMEs' ledger sections gained a sentence; the `config.md` line of the layout listing is untouched in either language |
| R3 · the floor is stated once, in the sentence naming `FLOOR` | the added `CONTRIBUTING.md` paragraph states no version number |
| R4 · `bin/test` named before the `uvx` form | the paragraph sits between the fenced block and *Name a module*, so the order and the no-write label are unchanged |
| every ledger path a person reads goes through `display_name` | the added line prints a module constant and no path |
| R5 · the records arm's quotation rules | the records arm is untouched; `main` changed only where it grades and where it prints |
| S1 · the full run is the sealer's | that sentence is unchanged and still names both the section and the definition |

Touching `seal/ledger.md` is what `CLAUDE.md` §*a change writes fragments*
permits and requires here: the rule forbids **appending**, and re-verifying a
row whose anchor this branch changed content under is what leaves the ledger
true. The new claims went to the fragment; not one row was appended to the
shared file.

**`--reverify` rewrites the hash and never the `Checked` column**, which is a
row in that ledger and turned out to be the operative fact of this phase: the
seven dates and their grounds were written by hand, one asserted edit per row,
with the cell count checked at seven so a stray pipe could not shift a column.

**Run at this phase's close:**

| Command | Result |
|---|---|
| `bin/evidence-check .`, exit code read directly | **exit 0** · `1153 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, records arm `0 refused · 0 drifted` |
| `bin/unverified-check --baseline origin/release/v0.11.3 seal/specs/` | **exit 0** · this work item reads `3 open · 0 closed` |
| `bin/test` over the new module and the seven that read what this work changed | **359 passed** |
| `uvx ruff check` and `ruff format --check` over the two changed Python files | clean, both formatted |
| `git diff --stat` against the base | `CHANGELOG.md` is not in it |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the shared `seal/ledger.md` had no row removed, only seven re-verified in place | none |
