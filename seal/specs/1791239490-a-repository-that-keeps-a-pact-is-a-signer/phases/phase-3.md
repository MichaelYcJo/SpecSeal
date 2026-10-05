# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 88f5f658 |
| Ran by | unknown — the spawn prompt named no agent or model, and this record is not where a segment names itself |

## What this phase was asked

The ledger and the fragment (`plan.md` phase 3): name the BROKEN families,
write one `Corrected ·` row per family carrying every coordinate the claim
still rests on at its new place, new rows for the reader, the printed line,
the check, the templates and the policy, the changelog fragment under
`### Changed`, and `overview.md` closed. The spawn prompt fixed the ledger
handling: `seal/config.md` declares `Ledger frozen from | 1790993141`, so no
released ledger file is edited and every re-read or correction goes into
`seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md`
(`docs/the-evidence-ledger.md` §*A released row is read again in the
branch's fragment*).

## What this phase found

- **M1, measured.** `evidence-check --strict .` after phases 1 and 2 read
  198 drifted and 103 broken coordinate readings. Grouped by family root
  through the checker's own `released_drift`, that is 67 released rows a
  reading is owed: 26 with a BROKEN coordinate, 41 drifted only. The 26 are
  the frame's grep list without P11, which no anchor of the rename moved.
- **Two drift-only rows took a `Corrected ·` row, not a re-read**, because
  their claims named the old word as a fact: P11 (0.18.0, *`pact` and
  `signatory` keep the owner's meanings*) and E6 (0.18.2, *points at
  `docs/the-pact.md` §A signatory records a pact change*). A re-read would
  have dated a claim that is false as written. So 28 `Corrected ·` rows, and
  the frame's grep had found 27 of them; E6 was found by reading the claims.
- **Four claims are restated, not only renamed**, because #822 added to the
  behaviour they state: the P8 correction (0.18.1, `pact_signers` reads the
  old header where the text holds no `Signer` table, and returns which), P7
  (the count notice gains the rename sentence), P9 (`pact-check` reads either
  header). Each says so in its Notes. D1 (0.18.1) stays a re-read: its claim
  holds in substance, and its Notes say what #822 added.
- **The other 39 drift-only rows were read and re-read** by
  `--reverify --into … --checked 2026-10-06`, one `Re-read ·` row each. Every
  drift came from a word swap in the unit the row cites (a section of
  `skills/implement/orchestration.md`, `evidence_check.py#reverify`'s printed
  strings, the record-layout trees, the table walker's fixtures), and no
  claim among them states the word. The run wrote 39 rows and left none.
- **The rows were drafted by a script in the session's scratch directory**
  that read the families through `released_drift` and hashed every
  coordinate through `current_hash`, so no hash was typed by hand; the
  fragment was then written with the `Write` tool and diffed against the
  draft (two intended differences: P8's label, R7's wording).
- **The records arm refused 19 lines of this work item's own records** that
  name an identifier the rename removed (`pact_signatories`, `_signatory`, · NAME NOT IN TREE
  `SIGNATORY_URL`, three old test names). Each such line in `spec.md`, · NAME NOT IN TREE
  `plan.md`, `phases/phase-1.md` and `overview.md` now carries
  `· NAME NOT IN TREE`, the marker `skills/evidence-check/SKILL.md` names for
  a record that means a name the tree no longer has. This touched the
  framer's `spec.md` and `plan.md` on those lines alone.
- **The changelog fragment gathers clean**: `gather_changelog.py --version
  0.19.0 --dry-run` exit 0, the fragment under `### Changed` with no `## `
  line.

Executed at 88f5f658, exit codes read directly:

| Command | Exit |
|---|---|
| `uv run python skills/evidence-check/scripts/evidence_check.py --strict .` | 0 — 6057 ok, 0 drifted, 0 broken; records arm 0 refused |
| `python3 skills/evidence-check/scripts/correction_check.py --range origin/release/v0.19.0...HEAD` | 0 — no released ledger file changed |
| `git diff --stat origin/release/v0.19.0...HEAD -- seal/ledger.md seal/releases` | 0, empty output |
| `python3 .github/scripts/gather_changelog.py --version 0.19.0 --dry-run` | 0 |
| `bin/unverified-check --baseline origin/release/v0.19.0` | 0 |
| `bin/test -p no:xdist tests/test_a_row_points_by_content.py tests/test_release_hygiene.py -k no_ledger_row` | 0 — 2 passed, the two cases that read the real ledgers' row shape |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none — no released row is removed under the freeze; each moved family is superseded by its `Corrected ·` row in this work item's fragment |
