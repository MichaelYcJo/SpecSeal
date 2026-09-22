# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `93a65ebd` |
| Ran by | `specseal:smith` on Opus 5 (1M context) — the agent definition names no `model`, and the spawning session passed no override, so the segment inherited the session's model |

## What this phase was asked

**The dry run over this repository's own 97, read.** Its numbers into
`overview.md`; `changelog.md` and `seal/ledger/<id>.md` written. **Nothing
removed.**

Verified by A10.

## What this phase found

**The run costs 0.10 s and removes nothing, and both halves were read rather
than assumed.** `settle` over 98 directories: 97 released, 81 grouped into 37
segments, 16 named, 0 skipped, one unreleased. `settle --retire` reports
`nothing to retire` at exit 1 — read with `echo $?` on a redirected run, not
through a pipe, which is where an earlier reading of the same command gave 0
because `head` was in the way. `git status --porcelain` after both is the
work this branch wrote and nothing else.

**The two numbers that matter to the fold's own work item are not the
headline.** 81 foldable is the size of the corpus; **37 is the size of the
judgment**, because that is how many standing statements somebody writes, and
**21 of the 37 hold a single work item** — so the act is wide and shallow.
The other is that **16 items have no segment at all**, 14 of them because they
wrote no ledger row, and for those nothing in the tree says what they were
about. That is the fold's real open question and it is now a measured one.

**Writing the ledger fragment forced a decision the spawn prompt had
answered the other way, and the grounds are in `overview.md`.**
`evidence-check --reverify` re-stamps every drifted row it finds, including
rows in `seal/ledger.md` that this branch's own edits had drifted — seven
anchors, eleven rows. The prompt says not to touch that file. Reverting it
left `evidence-check --strict` at `7 drifted`, and the checker's own closing
line says `broad-gate` runs it with `--strict`, where drift is exit 2 and the
tree comes back NOT SEALED. So the sealer would have refused the branch. Each
of the eleven was re-read against the edit that drifted it and carries a dated
note; one was re-verified by execution. No row was appended there, which is
what the fragment rule's word actually is.

**The ledger fragment's own coordinates were written with `@00000000` and
filled in by `--reverify`.** `seal/follow-up.md`'s first open row records that
a coordinate whose hash is not eight hex characters produces no row at all and
says so silently; `@00000000` is the spelling that same row records as picked
up and re-verified, which is why it was used rather than a placeholder that
would have dropped five claims without a word.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing — the phase adds the two fragments and reads the tree | none |
