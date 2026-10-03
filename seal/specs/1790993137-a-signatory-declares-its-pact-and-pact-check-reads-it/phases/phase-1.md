# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 18920f77 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 1, the relationship row: `Pact` and `Pact notify` read and
validated in `hooks/config.py`, beside `reference_roots`, so `chain_check.py`
and `pact_check.py` import one reader. `templates/config.md` gains a section
for both rows, and its *What no row governs* gains the three notify values.
`skills/config/SKILL.md`'s row table gains both rows, and every count of that
table's rows is corrected. Verified by a new
`tests/test_a_signatory_declares_its_pact.py` covering S1-S3 at the reader
level, with `tests/test_the_pull_request_language_is_the_repositorys.py`
still passing. The spawn added: the names are `pact`, `signatory` and
`pact-check`; the pact's repository gets no noun; every case is seen red
first; every test module reading an edited document is run.

## What this phase found

**The frame does not hold in one place, and the phase built to the part that
does.** `plan.md` §*Technical context* says the two rows' parsing lives in
`hooks/config.py` and that `seal.py#normalise_remote` is imported, not
copied. Both cannot be true: `skills/implement/scripts/seal.py` imports
`hooks/config.py` by plain name, so the reader importing `seal.py` is a
cycle, and `hooks/config.py`'s own docstring says a hook must not load that
two-thousand-line command to read a row. So `normalise_remote` moved into
`hooks/config.py`, byte for byte but one docstring paragraph saying why, and
`seal.py` keeps the name as an alias. That is the arrangement the same
docstring records for the `Mode` reader, and it keeps one normaliser.
`questions.md` Q12 is answered for `seal.py` here; its other half, loading
`evidence_check.py` by path, is phase 5's.

**The reader's API.** `pact_declaration(text)` returns
`(pacts, notify, refusals)`: `pacts` as `(as written, normalised, name)`,
`notify` lowercased with the default where a `Pact` row stands and `None`
where none does, and `refusals` as sentences. `declared_pacts(home)` reads
`<home>/config.md` and answers a file that will not read as no row. Phase 4
prints the refusals and phase 5 exits 2 on them; phase 5 reads another
repository's `config.md` and should call `pact_declaration` on the text it
read, so an unreadable file there is its own refusal rather than no row.

**What it refuses**, decided while writing it, each with a case: two `Pact`
rows; an empty entry between separators; an entry holding a space; an entry
reducing to no host and path; a name outside `[A-Za-z0-9_.-]`; two entries
naming one repository; two entries ending in one name (the anchor could not
say which pact it cites); a notify value outside the three; two `Pact notify`
rows. An empty `Pact` value is no pact, the direction every reader in that
module fails in.

**`/specseal:config` shows ten rows, not nine.** Its table and the front-door
case's `ROWS` were missing `Reference specs`, which `templates/config.md` has
shipped since #688, so the skill's *every row, present or not* was already
false. Correcting the count to the rows this work adds would have written a
second false number, so `Reference specs` went in with the two new rows.

**Ledger rows this phase drifted (Q13, phase 1).** Twelve rows cited four
coordinates this phase edited: `templates/config.md#"## What no row
governs"` (six rows in `seal/releases/0.5.0.md`),
`templates/config.md#"# Repository config"` (one),
`skills/config/SKILL.md#"## Procedure"` (two in `0.5.0.md`, one in
`0.12.0.md`) and `seal.py#normalise_remote` (one in `0.5.0.md`, one in
`0.9.1.md`). Each was read against the edit and carries a dated note. The two
`normalise_remote` rows are corrected in place, their coordinate following
the function to `hooks/config.py`, because the alias left behind holds no
`isinstance` guard. That note in turn drifted the row in
`seal/releases/0.13.1.md` anchored on `0.5.0.md`'s `### 1788398967` section,
which was re-read and noted as well. `evidence-check .` then reported no
drifted, broken or malformed row in any ledger.

**Verified, executed.** Red: with the four implementation files stashed, the
eight new cases and four front-door cases failed (12 failed, 16 passed).
Green: the 24 test modules that name `templates/config.md`,
`skills/config/SKILL.md`, `hooks/config.py` or `seal.py` gave 1826 passed,
7 skipped. `ruff check` and `ruff format --check` passed on the four Python
files.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `def normalise_remote` in `skills/implement/scripts/seal.py` | `hooks/config.py#normalise_remote`; `seal.py` keeps the name as an alias |
