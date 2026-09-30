# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. -->

📋 implement applied
· spec:     `spec.md` (Grounding, M1–M8, F1–F8, P1–P7, R1–R9, D1–D3, the gate owed), `plan.md` (Technical context, Alternatives, Phases), `questions.md` Q1–Q3; `CLAUDE.md` §*Repo rule — commit early* and §*a change writes fragments*; `docs/the-evidence-ledger.md` "Appended is the word"; `seal/follow-up.md` header and row 69; #508, #387 (the owner's answer in the spawn), #664 body and comment; A's `round-3-report.md` paste-ready docstring
· evidence: `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md` F1–F3, P1–P2, R1–R4, H1–H2; every shared row phases 4 and 5 drifted, re-read and dated with `--checked` in its own file, each carrying a `Re-read 2026-09-29 by work item 1790635414` note (`phases/phase-4.md` and `phase-5.md` say which files), A's O4 and 0.9.0's R1 corrected in place
· verified: executed — every new case red first (base checker by extraction, or a mutant), mutants over every new unit, the lenient tree check and `correction-check`; read — the 59 re-read claims; unverified — the suite, lint and typecheck (the sealer's) and CI's three legs

## Why this work exists

`seal/follow-up.md` rows and `path#name` spans in live records named units
nothing checked, `--reverify` wrote a hash that says *somebody read this*
without the date that says when, and a form feed could hide an edit from the
hash; after this, all three are read, dated or refused by the checker.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The records heading | F7: "The records heading and the summary line say whether `seal/follow-up.md` was read" / the heading is a constant and names the file as part of what the arm reads; the summary line's last field says `read`, `no …` or `unreadable` | code | A constant cannot vary per run, and `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py` reads the heading as a constant. The per-run fact is on the line people read for the counts |
| The frame's test helper | *Technical context*: "the same five-column rule … that `tests/test_release_hygiene.py#overwide_rows` counts against" · NAME NOT IN TREE / A's squash replaced it with `evidence_check.py#overflow_rows` | code; the plan line corrected in place | Phase 2's reader refused the plan's own line, which is the arm working |
| A dotted name under an unresolved path | P4: "read exactly as the bare backticked name would be" / each segment is read as a bare name | code | A bare span holds no dot, so `Class.method` written bare is never read whole; segment by segment is the only reading of "as the bare name would be" |
| Q2 | default: "a sibling of `grounds_cells`" / A's `ledger_table_rows` is reused | code | A's squash made the sibling unnecessary, and Q2 was put to the work for exactly that |
| #664's comment: "a markdown anchor is not shifted" | true of numbering / a line-end character before `## ` ends a markdown section, and one before column-0 text ends a generic block, and both let an edit pass | widened the class | Both red at `56e53c90` on the real assertion (`phases/phase-5.md`) |
| Phase 5's list of outside readers | "each reader moved or recorded out" / `fold_check`'s ceiling count moved; its marker readers and `round_record.py`'s record reads recorded as coupled to the shared reader; the rest B's or D's | recorded | The spawn limited moves to files B and D do not touch, and the coupled readers zip their lines with `unverified_check.readable`, B's file |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over this branch | the sealer, once the review rounds settle |
| CI's Windows, Linux and macOS legs over the new cases, the `built_name` coordinate of a follow-up refusal and the local-date refusal included | the pull request's CI run |
| The Korean README's new paragraph reads as native prose | the review chain |

## Not done

- **The line-end class outside the checker.** `phases/phase-5.md` holds the
  enumeration. The readers in B's and D's files, and the ones coupled to
  `unverified_check.readable`, move together once #584 squashes: one
  splitter in the shared reader, `readable` and the `live_lines` callers on
  it, then `round_record.py`'s `raw` sites and `fold_check.py`'s marker
  readers, then `fold_check.py`'s copy deleted. That is a comment on #664 for
  the orchestrating session to post, since #664 already owns the class.
- **`seal/follow-up.md` row 69's first two options** — naming every row
  rather than every coordinate, and refusing a shared coordinate until each
  row is named — stay the owner's; the row carries a dated note saying what
  this work narrowed.
- **`CHECKED_RE`'s `[0-9]` is held by nothing**: `datetime.date.fromisoformat`
  refuses fullwidth digits by itself on the interpreter here, so the ASCII
  class is belt and braces. Kept, and said so in the ledger row.

## Fed back into the spec

*Inferred during implementation; a planner may overturn these.*

- An anchor outside any table row is a row with no date cell: under
  `--checked` it is left whole with a `LEFT` line, and without it the naming
  block says `no date cell`.
- The naming block cuts a row's first cell to 72 characters; the ledger and
  line locate the row.
- A refused `--checked` prints on stderr, prefixed `evidence_check:`, with
  nothing on stdout, as `rider_check.py` refuses `--only`.
- A `path#name` refusal names the path as the record wrote it, not the path
  `place` resolved.
