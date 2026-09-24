# 1790260565-a-ledger-row-carries-two-readings-in-one — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | a67c1721 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#569 ⬜ 1: #569's paste-ready block goes in as the reviewer wrote it. Three
needles join `CONFLICT_SENTENCES`, `OWNED_SENTENCES` becomes
`CONFLICT_SENTENCES[-7:]`, the comment that said "the checker says which
after the fact" is rewritten, and the owner's case asserts the third outcome
("the edit made false is corrected there first"). Each clause was to be seen
red once per carrier. `CLAUDE.md` was to be mutated only in a scratch copy,
never in place. E1 and E2 (`seal/releases/0.15.1.md`) each gain a dated
`Re-read` note, and no document changes.

## What this phase found

- **The block went in green, as #569 measured.** The module ran at
  `52 passed` with the block applied. No document needed a word, which
  matches the spec's reading that every needle already stood in all three
  carriers.
- **Seen red (§15), nine deletions, each on the case it belongs to.** A
  Python probe copied `CLAUDE.md`, `CONTRIBUTING.md`,
  `docs/the-evidence-ledger.md` and `docs/release-checklist.md` into a
  scratch directory, pointed the module's `ROOT` there, and deleted one
  clause at a time. No carrier in the worktree was written, so nothing had to
  be restored.

  | Carrier | Clause deleted | Case that went red |
  |---|---|---|
  | `CLAUDE.md` | its claim first corrected in place with a `` `Corrected <date>` note `` where the edit made it false | `test_a8_…` |
  | `CLAUDE.md` | and to neither side where both did | `test_a8_…` |
  | `CLAUDE.md` | which is re-read against every edit the merged unit carries | `test_a8_…` |
  | `CONTRIBUTING.md` | the third bullet, *the code still stands and your edit made the claim false …* | `test_a8_…` |
  | `CONTRIBUTING.md` | and to neither side where both did | `test_a8_…` |
  | `CONTRIBUTING.md` | which is re-read against every edit the merged unit carries | `test_a8_…` |
  | `docs/the-evidence-ledger.md` | and one the edit made false is corrected there first, with a `` `Corrected <date>` note `` | the owner's case, on its own new assertion |
  | `docs/the-evidence-ledger.md` | and to neither side where both did | the owner's case |
  | `docs/the-evidence-ledger.md` | and the row is re-read against every edit the merged unit carries, one side's or both | the owner's case |

  With the edit arm's clause deleted from the owner, the shared needle
  `` `Corrected <date>` note `` was still present in the text, carried by the
  halves paragraph's `` `Corrected <date>` notes ``. That is the reviewer's
  reason for the owner's own assertion, reproduced.
- **E1 and E2 drifted by exactly the two units this phase edited.**
  `--reverify` over `0.15.1.md` changed E1 and E2 and nothing else. E2's
  Checked date moved to 2026-09-25. E1's was already 2026-09-25 from
  phase 2.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the comment "the checker says which after the fact" above the #509 needles | the reviewer's comment in its place, naming *neither side where both did* and the re-read |
