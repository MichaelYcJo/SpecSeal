# 1789621028-nothing-reads-a-record-against-the-tree — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | a8c3a2d5 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Close out: `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` written in
one pass from the rows kept since phase 1, `overview.md` closed,
`seal/follow-up.md` left alone with the enumeration recorded. Verified by
`bin/evidence-check .` exit 0 with the new rows resolving, and the modules
this branch touched run narrowly. **The broad gate is not run here.**

## What this phase found

**Twelve ledger anchors drifted under this branch's edits, and re-verifying
them is a read rather than a command.** `bin/evidence-check .` came back exit
1 with 12 DRIFTED rows across `seal/ledger.md`. Each claim was re-read against
the code it cites before anything was re-stamped, and **all twelve still
hold** — the edits added to the units those rows anchor on rather than
changing what the rows assert. `--reverify` then moved 22 row-anchors (several
rows cite the same unit) from their old hashes to the new ones.

**`--reverify` does not move the `Checked` date, so 22 cells were moved by
hand.** That gap is `seal/follow-up.md`'s and it was #120's finding 5 — a row
re-stamped with the hash alone asserts a reading nobody took.
`templates/ledger.md` states that the column holds the date somebody read the
code, and 2026-09-17 is that date for all 22. Executed afterwards:
`bin/evidence-check .` **exit 0**, 1340 ok · 0 drifted · 0 broken · 0
old-format, and `--strict` **exit 0** as well.

**The new fragment's two heading anchors were BROKEN on the first pass, and
the cause is worth the sentence.** A heading anchor quotes the heading line
verbatim, backticks included and unescaped — `` `docs/review-chain-spec.md#"#####
The fix range — `Fix range`"@…` `` — and the first attempt escaped them as
`` \` ``, which matches no line in the file. The anchor was rebuilt by reading
the heading out of the document rather than by retyping it.

**One prose mention in a ledger cell read as an old-format coordinate.**
`survivors.md:5` written inside a Verified-behavior cell tripped
`evidence-check`'s old-format arm at exit 2, because the checker matches the
`path:line` shape wherever it appears. Reworded to name the row by what it is
rather than by where it sits — which `CLAUDE.md` asks for anyway: a row names
content, never a position.

**`seal/follow-up.md` is untouched and all eleven rows were read.** The two
nearest are `evidence-check` ignoring a malformed coordinate and seven ledger
rows anchored on a whole heading path. Both are about the **ledger's** anchors
and about `evidence_check`; this work item changes neither checker nor any
ledger anchor's shape, so nothing here unblocks them and no row is deleted.
That enumeration was taken at framing and again here.

**The verification at the branch tip, executed 2026-09-17**, exit codes read
directly:

| Run | Exit | What it printed |
|---|---|---|
| `bin/test` over 27 modules — every module this branch touches or whose subject it changed | **0** | 1100 passed, 8 skipped |
| `bin/evidence-check .` | **0** | 1340 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `bin/evidence-check --strict .` | **0** | the reading `broad-gate` takes |
| `bin/unverified-check --baseline release/v0.12.1` | **0** | 81 overviews · 275 open · 59 closed · **0 unreadable** |
| `.github/scripts/rider_check.py` | **0** | |
| `bin/survivor-check --range 5694500..a8c3a2d` | **0** | 1066 files examined, 72 removed sentences, no removed wording still standing |
| `uvx ruff check skills/ tests/ hooks/` | **0** | |
| `uvx ruff format --check skills/code-review/scripts/ tests/` | **0** | |
| `.github/scripts/fold_ledger.py --check` | **1** | names this work item's own unfolded fragment. **Expected**: a fragment lives from its first row to the release that ships it, and that check runs on pull requests into `main`, which this branch does not open |

**`survivor-check` was given a pinned range, not `origin/...HEAD`**, which is
the rule this work item builds. The command in the record names two commits,
so the run is repeatable — and phase 5 measured that even that is not
sufficient, because the checker itself moves.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `none` — this phase adds the fragments and the memo and takes nothing out of the tree | `none` |
