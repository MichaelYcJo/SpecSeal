# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `5da403c` |
| Ran by | specseal:smith on Opus 5 |

## What this phase was asked

Write `seal/specs/<id>/changelog.md` and the closing memo. `## Not verified` is
a `| Item | Who must answer |` table or the line `none — <why>`; prose inside it
exits 1, and a previous session in this release hit that three times in a row.
Verified by the fragment conventions in `CLAUDE.md` and `unverified_check` on
the memo.

## What this phase found

**The memo carries four open rows and every one of them names a person or a
segment**, which is the only shape that keeps *someone will look at it* from
becoming nobody did: the broad gate goes to the orchestrating session, the
label's final spelling and the stale milestone description to the repository
owner, and one judgement to the reviewer first. `bin/unverified-check` reads
`4 open · 0 closed`, exit 0.

**A survivor sweep was run even though this is a build rather than a fix pass,
because the range deletes a shipped sentence.** `bin/survivor-check --range
7e17f5e..HEAD` reported four places still carrying wording the range removed,
all four traceable to the one removed ledger row rather than to the document
edit:

| Standing text | Verdict |
|---|---|
| `seal/specs/1789100139-…/phases/phase-2.md:62` and `:60` | excused — a closed work item's phase record, true at its own SHA, and the placement it describes is still the placement |
| `seal/specs/1789100139-…/changelog.md:22` | excused, and **named in the hand-back as the one judgement worth a second reading**: #351's fragment quotes the replaced sentence and is gathered into the same released section as this work item's entry |
| `seal/ledger.md:736` | excused — a phrase collision. The shared phrases are `re anchored 2026 09` and `s hash moved`, the vocabulary every re-anchoring note in that file uses; the row is about `## Phases` in another document |

Each is a row in `survivors.md` anchored on a quote, so the exemption stops
holding the moment that text changes. Re-run with `--exempt`: exit 0, *every
survivor is excused by a row above (4)*.

**`questions.md`'s five work-and-measurement rows are closed in this phase**,
each with what was executed rather than with a letter. Two of them changed
something: Q6 found the frame's absence check green before the edit, and Q7
found a second drifted ledger row the frame did not name.

**The changelog fragment states what a reader of the released section needs and
nothing the diff already holds** — the misreading that motivated the change, the
criterion, why the evidence is prose, the label in two states, and what does not
change. It does not name a version, so the same hygiene constraint that shaped
the document shapes the entry.

| Ran | Exit | Reading |
|---|---|---|
| `bin/unverified-check <the memo>` | 0 | `4 open · 0 closed` |
| `bin/survivor-check --range 7e17f5e..HEAD` | 1 | four places still carrying removed wording |
| `bin/survivor-check --range … --exempt <survivors.md>` | 0 | all four excused |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
