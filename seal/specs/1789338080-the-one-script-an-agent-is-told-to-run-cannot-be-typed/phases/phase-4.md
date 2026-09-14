# 1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 9693c3a |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Write `changelog.md` and `seal/ledger/1789338080-….md` as fragments, never the
shared `CHANGELOG.md` or `seal/ledger.md`, and close `overview.md`. Verify with
the two hygiene-adjacent modules, `evidence-check --strict .` on the fragment,
and `uvx ruff check` / `ruff format --check` on the one new test file.

## What this phase found

**Three of the five ledger anchors did not resolve as first written, and the
reason is a rule the ledger's own examples do not show.** A quoted-literal
anchor is matched against the WHOLE LINE, whitespace-normalised — `text_regions`
in `skills/evidence-check/scripts/evidence_check.py` — so
`bin/round-record#"skills/code-review/scripts/round_record.py"` is BROKEN even
though that exact string is in the file, on a line with other text around it.
The three were rewritten as full lines with escaped inner quotes and all
seven anchors then resolved. A shell script and a `.cmd` file have no symbol
for `ast` to find, so a full-line literal is the only anchor form available
for a `bin/` wrapper at all.

**`evidence-check --strict .` was red at first, and not on this branch's own
fragment.** The fragment came back `7 ok · 0 drifted`; seven anchors elsewhere
in `seal/ledger.md` — eleven rows — drifted, every one of them a section phase
3 edited. Each claim was re-read against its section before anything was
re-stamped, and none is about a command's spelling or a locator's placement.
`--reverify` then moved eleven hashes; the diff of `seal/ledger.md` is those
eleven rows and nothing else, verified by comparing every changed row with its
predecessor under the eight hex characters masked out.

**`--reverify` does not move the `Checked` column, and `CLAUDE.md` defines
re-verifying as re-reading followed by that command.** So eleven rows now carry
a date older than the day they were last read. Not repaired here — it is
`evidence_check.py` behaviour, which #318 is not about — and handed over in
`overview.md` §Not done and in the report, for an issue rather than for
`seal/follow-up.md`, which says a repository with a tracker should hold none.

**Phase 4 is where the branch's own `Not verified` rows settle, and both name
somebody.** The broad gate is the sealer's under §2; the three `Ran by` cells
are the orchestrator's under `templates/sdd-phase.md`, which forbids the
segment to fill them from its own idea of what it is.
`unverified-check --baseline origin/release/v0.11.4` reads the file and exits
0 with both rows open.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
