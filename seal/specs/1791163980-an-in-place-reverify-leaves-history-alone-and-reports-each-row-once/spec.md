# Feature Specification: an in-place `--reverify` leaves history alone and reports each row once

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issues #785, #792 (and its comment) and #781. All three are about what an
in-place `evidence-check --reverify` writes and prints. All three were found
by the 0.18.2 work item
`1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move`,
whose records are still in the tree. That item's design stands, and this one
builds on it: the dependency-ordered walk and the bounded re-walk
(`cited_first`), the fold of one coordinate's walks (`walked_move`,
`owed_moves`), the key every printed hash line uses (`first_old`, `said_here`),
the skip of a citation's move (D3), and the rule that a line claiming a write
waits for the write (`told`).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, the family paragraph (*Of the members that record a coordinate, only the readings with the newest `Checked` date count …*) | Decides #785. A reading the family's newest reading outranks is no longer what the coordinate is judged by. Re-stamping it and adding a date to it claims a reading of a row nobody opened, and the added date can make it the newest reading. |
| The same section, the `--into` paragraph: *`--checked` writes that date into every row whose hash it moves; it says every such row was re-read, so read each row citing a drifted coordinate first* | Bounds #785. The re-read the flag asserts is owed for a **drifted** coordinate. A family that already holds the code owes none. A drifted family keeps today's behaviour: every member whose hash moves is re-stamped (D1). |
| The same section, *A `Corrected ·` row supersedes the family of the row it cites, whose coordinates are not checked again* | Puts a superseded family inside #785's class (D1, row 3). `--strict` judges none of its coordinates, so no re-stamp of one is owed. `released_drift` already skips superseded families for the same reason. |
| The same section, *Without the row, a released row is kept true where it stands*, last two sentences: a narrowed run *names, by its root row, each family … where no in-place re-stamp of the files it read clears that family … and exits 1* | Decides #792's first half. The `--ledger` remedy is true only where a file the run did not write holds the reading that keeps the family drifted. The exit 1 stays, and only the remedy the line names changes (D3). |
| The same section, *Five things `--reverify` leaves at exit 0 while `--strict` exits 2*, third item: *Under a released root the same coordinate is named, and the run exits 1* | This is the unnarrowed run's naming that #792 found carrying the wrong remedy. The item's statement stays true. Only the line's words change. |
| The same paragraph's first sentence, *re-stamps a re-read row in place with a dated note* | #781. The owner decided on 2026-10-05, in the routing batch: the sentence is corrected to name the `Checked` date, and the writer's output does not change (D4). |
| `skills/evidence-check/SKILL.md` §*Re-verifying is recomputing the hash*, *It rewrites the hash of every row whose anchor resolves*; the usage text in `evidence_check.py`'s module docstring (*rewrite the hash of every resolvable row*); `reverify`'s docstring | Each states the behaviour D1 changes, so each changes with it and is pinned (§14). |
| `seal/config.md` `Ledger frozen from` | This repository's own re-reads go into this item's fragment through `--into`. `seal/releases/0.18.2.md:91` states that the home names a dated note, which D4 makes false, so it takes a `Corrected ·` row (D5). |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Each defect is fixed across its class, enumerated below by construction. Every changed sentence a person reads is pinned in the same commit. Every new case is seen red before it is committed. |

## Scope

### In

**D1 (#785): an in-place re-stamp leaves a coordinate alone where its family
does not owe a re-read of it.**

- `reverify` judges every code coordinate on a family member's line **once,
  before its first walk**. The judgment is `family_view`'s own: a coordinate
  is left alone where `view.held[root][coord]` is non-empty, or where the
  member's family is in `view.superseded`.
  - Left alone means: its hash is not rewritten, its row is not dated for it,
    it is not named in the hash, dated or undated lines, and it hands MOVES no
    part.
  - A row with other coordinates the run does re-stamp is dated as today,
    once.
- The view is built over every ledger the repository carries
  (`default_patterns(root)`), plus the run's own `ledgers`, the way `main`
  builds it for `released_drift`. So a narrowing that leaves out the file
  holding the newest reading changes nothing.
- **Why it is judged before the walk and not live.** The walk changes ledger
  lines, never code, so a code coordinate's grading cannot change during the
  run. Only the dates change, and a date the run adds can promote a reading
  to newest. A live judgment would make the result depend on walk order.
  *Inferred during implementation, round 1 (yellow 2):* a coordinate naming
  a line of a ledger the run writes is the exception, because the walk can
  move that line, so it is never judged held. A held coordinate no one place
  holds, on a row the run dates, is left and named as any such coordinate is
  (yellow 1), unless one of its places, for a claim exactly one, holds what
  the row recorded (round 2); where its only place is one the declaration
  rule is unsure of and it has no claim, it is re-pointed onto the one
  destination that reconstructs its hash, as the ordinary path does (#808).
- **Unchanged:**
  - a row outside every family is its own newest reading;
  - a coordinate whose family is drifted: every member whose hash moves is
    re-stamped, which is what the `--checked` paragraph asserts;
  - a citation, which is a ledger line and not a code coordinate, so the
    family view does not grade it;
  - every BROKEN and left coordinate outside a superseded family.

**D2 (#792's comment): each coordinate's outcome is printed once, after the
walks settle.**

- Today every `left` line is printed only on a file's first walk
  (`say = quiet if repeat else print`). So a `left` that a later walk clears
  is never taken back, and a later walk's `left` is never printed.
- The `left` lines are kept per coordinate, under the key the hash lines
  already use (`key_at`). They are printed once the walks end, as the fold
  says:
  - A coordinate whose last walk to change anything left it prints its last
    `left` line.
  - One that a later walk read unchanged or re-stamped prints no `left` line.
  - One whose move landed keeps its one hash line, as #786 made it.
- The printed lines and MOVES come from the same rule (`walked_move` /
  `owed_moves`), so they cannot disagree. The line for a citation follows
  the same rule, although its move is never handed to MOVES (D3 of the 0.18.2
  item).
- The `left` lines claim no write, so they stay outside `told`, as they are
  today. They print at the end of `reverify`, before the record step, in the
  order the walks first met the coordinates.

**D3 (#792): the family `LEFT` line in `main`'s unfrozen arm names only a
remedy the run supports.**

- Today the line always ends *the newest reading … sits in a file this run
  did not write; run it without `--ledger`*. For each coordinate the line
  owes, the run now knows which of two reasons holds:
  - **(i) Outside the run.** A member reading of the coordinate that does not
    hold sits in a file this run did not write.
  - **(ii) Left by the run.** The run left the coordinate itself on a member
    in a file it wrote. The walk's last outcome was `left` (D2), or the row
    was left whole for having no date cell.
- The `--ledger` clause is printed only for (i). The (ii) clause says the run
  left the coordinate and points at the line naming why. A line where both
  hold carries both clauses. An unnarrowed run cannot reach (i), because it
  writes every file the view holds a member in.
- The exit code does not change: 1 wherever the line is printed.
- `citations_left`'s `LEFT` line is right as it stands. It names only a file
  the narrowing left out, so an unnarrowed run never reaches it. It is
  enumerated below and not edited.

**D4 (#781): the document says what the writer writes.**

- The sentence *re-stamps a re-read row in place with a dated note* in
  `docs/the-evidence-ledger.md` is corrected to name the date the reading
  adds to the row's `Checked` cell.
- Its pin in `tests/test_a_merge_cannot_silently_drop_a_correction.py`
  `RE_READ_SENTENCES` follows, and so does the comment above that tuple.
- No code changes for #781.

**D5: this item's records.**

- Its fragment `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md`.
- `Re-read ·` rows, written by `--reverify --into` and narrowed to what was
  read, for the released rows whose cited units this item's edits drift.
- A `Corrected ·` row over `seal/releases/0.18.2.md:91`, whose claim says
  the home names a dated note.
- The `changelog.md` fragment.
- A `survivors.md` where `survivor-check` reports a place sharing words with
  the removed *dated note* sentence. The 0.18.2 item's directory is one
  candidate.

### The class each defect belongs to, enumerated by construction (§12)

**Class 1, #785: an in-place re-stamp of a code coordinate that `--strict`
does not judge by that reading.** The axes are the family state of the
coordinate before the run, the member's role, and whether the freeze puts its
file in the walk. Narrowing and `--checked` are separate axes, after the
table.

| Family state of the coordinate | Row outside every family | Member, no freeze (every file walked) | Fragment member, freeze | Released member, freeze |
|---|---|---|---|---|
| Held by a newer reading (#785's probe) | n/a | **left alone** (today: re-stamped and dated) | **left alone** (today: re-stamped and dated) | not walked, as today |
| Held by a reading on the same date: a union, so a drifted tie member is graded OK | n/a | **left alone** | **left alone** | not walked |
| Superseded by a `Corrected ·` row | n/a | **left alone** | **left alone** | not walked |
| Drifted: no newest reading holds it | n/a | re-stamped, as today | re-stamped, as today | not walked; `--into` writes or names its root, as today |
| No family | re-stamped, as today | — | — | — |

Further axes, each with one answer:

- **Narrowing.**
  - The file holding the holding reading is in the narrowing, or out of it:
    the same answer, because the view is the whole repository's.
  - One consequence is a behaviour change. Unfrozen, narrowed to the release
    file whose root a fragment reading outranks, today's run re-stamps the
    root. That moves the line the fragment cites, so `citations_left` names
    the fragment row and the run exits 1. After D1 the root is left, and the
    run exits 0.
- **`--checked` given or not.**
  - Given: a left-alone row is not dated.
  - Not given: it is not named in the undated list.
- **Pact.** A left-alone coordinate hands MOVES nothing, so no pact change is
  recorded for it, under any `Pact notify` value.
- **Coordinate kind.** A citation is outside the class: `family_view` does
  not grade it. A rename is outside it too. A coordinate at its old path is a
  different coordinate from the newer reading's at its new path, so the old
  one's family is drifted or BROKEN, and it is re-pointed as today.

**Class 2, #792's comment: a printed line about a coordinate that a later walk
contradicts.** A coordinate's walks form a sequence over `{moved, unchanged,
left}`. A file in `cited_first`'s `once` list has length 1, and a file in
its `again` list has length up to the walk bound. The printed lines are the
fold of the sequence, which is the rule
`test_every_walk_sequence_hands_over_what_the_file_holds` already holds for
MOVES:

- a hash line iff some walk moved it, `first -> last landed`;
- a `left` line iff the last walk that was not `unchanged` left it, with that
  walk's reason;
- nothing otherwise.

The sequences of length 2 and 3, 36 of them, are the case's parameters, as
they are for MOVES. Static `left` reasons are in the class too: *path escapes
the repository* and *not in any known checkout* repeat identically on every
walk, and print once.

**Class 3, #792: a `LEFT` line naming a remedy the run cannot use.**

| `LEFT` line | Narrowed | Unnarrowed |
|---|---|---|
| Family still DRIFTED, reason (i) only | `--ledger` clause (as today) | unreachable: every file the view holds a member in is written |
| Family still DRIFTED, reason (ii) only | **(ii) clause** (today: `--ledger` clause) | **(ii) clause** (today: `--ledger` clause; #792's probe, and A10's folded no-freeze case) |
| Family still DRIFTED, both | **both clauses** | unreachable |
| Family still DRIFTED, neither found | a measurement (questions Q3); the line names no remedy it cannot support | same |
| A citation this run moved, in a file the narrowing left out (`citations_left`) | `--ledger` clause, true (as today) | unreachable: no file is left out |
| `undatable`, `MALFORMED`, `OVERFLOW`, `ledger unreadable`, could not be written | name no `--ledger` remedy today | the same |

**Class 4, #781: a statement that the in-place re-stamp writes a note.** Found
with `git grep -n 'dated note'` at `e5cede76`:

| Instance | In scope |
|---|---|
| `docs/the-evidence-ledger.md`, the *Without the row* paragraph's first sentence | D4 |
| `tests/test_a_merge_cannot_silently_drop_a_correction.py`, `RE_READ_SENTENCES`, and the comment above it | D4 |
| `seal/releases/0.18.2.md:91`, a `Corrected ·` row whose claim says the home names the dated note | D5: corrected |
| `docs/experiments/README.md:17` | Out: a dated note on an experiment's result, which is another subject |
| Earlier work items' `spec.md`, `plan.md` and `questions.md`, which say a session re-stamped a row *with a dated note*: a Notes trace those sessions wrote by hand | Out: records of what those sessions did, which stay true. Retired by `settle`. A `survivors.md` row names any that `survivor-check` reports. |

### Out, each with its reason

- **An outranked reading in a *drifted* family.** It is still re-stamped and
  dated. The `--into` paragraph tells the reader to read every row citing a
  drifted coordinate before `--checked`, and #785 asks only for a family that
  already holds. Re-stamping only the newest reading would need a rule for a
  newest reading the run cannot write: released under the freeze, or in a
  file the narrowing left out. That is a new design, for a new issue if the
  owner wants it.
- **`seal/follow-up.md`'s row on *`--reverify` re-stamps every row that
  cites it*.** That row is about several rows outside one family citing one
  unit. D1 narrows it only where those rows are one family, so the row's
  open options are unchanged. This item does not edit the shared file.
- **`README.md`, `README.ko.md`, `templates/ledger.md`, `CONTRIBUTING.md`.**
  Each was read at `e5cede76`. Each says `--reverify` recomputes the hash and
  dates *every row whose hash it moves*, which stays true. None says every
  resolvable row is rewritten, and none describes a `LEFT` remedy.
- **`docs/the-pact.md` §*A signatory records a pact change*.** It says a
  re-stamp in place records each row's move. A left-alone row moves nothing,
  so the sentence stays true. The phase that edits the code re-reads it and
  edits it only if the reading finds it false.
- **The frozen arm's `reverify_into` lines.** They already read families
  (`later_reading`, `newest_hash`) and name no `--ledger` remedy.
- **Building a Notes trace into the in-place writer.** The owner decided
  against it (#781).

## User scenarios & acceptance *(mandatory)*

Every case lands in `tests/test_a_released_row_is_read_again_in_a_fragment.py`
unless the row says otherwise. Each one is seen red at the base `a3aa139a`,
where the defect is old, or under the mutation the row names.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1: #785's probe | **Given** the freeze; released R1 at `handler@h0` 2026-01-01; fragment A re-reads R1 at `h1` 2026-02-01; fragment B re-reads R1 at `h2` 2026-03-01; the code at `h2`; `--strict` exits 0. **When** `--reverify --checked 2026-04-01 .` runs (no `--into`). **Then** A's line is byte-identical, no hash line or dated line names A, the exit is 0, and `--strict` exits 0. | New case, red at the base (which rewrites A to `h2` and dates it `2026-02-01 · 2026-04-01`) |
| S2: the root outranked, no freeze | **Given** no freeze; R1 at `h0`; fragment B at `h2`, newer, holding. **When** an unnarrowed run, then one narrowed to the release file. **Then** R1's line is byte-identical both times, both runs exit 0, and no `LEFT` line is printed. | New case, parametrised over the narrowing. Red at the base: the narrowed run exits 1 on `citations_left` |
| S3: a tie | **Given** two members dated the same day, one holding and one not. **When** a run with `--checked`. **Then** the drifted one is left alone. | New case, red at the base |
| S4: a superseded family | **Given** no freeze; R1 drifted, and a `Corrected ·` row citing it. **When** a run. **Then** R1 is not re-stamped, and the `Corrected ·` row's own coordinates are re-stamped as today. | New case, red at the base |
| S5: the control | **Given** a drifted family: no newest reading holds. **Then** every member whose hash moves is re-stamped and dated, as today. | New case, green at the base and red under the mutation *leave every family member alone* |
| S6: undated | S1's tree without `--checked`. A is absent from the *took a new hash and kept their date* list. | Parameter of S1 |
| S7: no pact change for a left-alone row | **Given** S1's tree in a signatory with `Pact notify \| always` and a `routing.md`. **When** the run. **Then** no record row names A. | New case in `tests/test_a_signatory_records_a_pact_change.py`, red at the base |
| S8: every walk sequence prints what the file holds | For each of the 36 sequences, the printed lines are the fold: a hash line iff a move landed, a `left` line iff the last non-`unchanged` walk left it. | New case beside `test_every_walk_sequence_hands_over_what_the_file_holds`, driving whatever unit D2 adds; red under the mutation *print on the first walk only* |
| S9: walk 0's `left` taken back | The tree of `test_a_coordinate_left_and_then_read_unchanged_records_nothing`, run through `main`. **Then** no line says X1 is left, and `--strict` reads it clean. | Extends that case or adds one beside it; red at the base (post-review-check-2's ⬜ 2) |
| S10: an unnarrowed run that leaves a coordinate itself | A10's *folded, no freeze, unnarrowed* tree, and the 0.18.2 first post-review pass's X1 *move then left* shape. **When** an unnarrowed run. **Then** the family `LEFT` line names the coordinate and that the run left it. It names no `--ledger` remedy. The exit stays 1. | New case, red at the base (post-review-check ⬜ 2) |
| S11: a narrowed run, reason (i) | `test_an_unfrozen_narrowed_reverify_names_a_family_it_could_not_clear`: the `--ledger` clause is still printed. | Existing case, kept green; its assertion tightened to the clause |
| S12: a narrowed run, reason (ii) | Narrowed to the file holding the member the run leaves itself, with no newer reading outside it. **Then** the (ii) clause, and no `--ledger` clause. | New case, red at the base |
| S13: the documents say it | The skill's re-verify paragraph, the usage text, `reverify`'s docstring and the ledger home each state D1. The home's *Without the row* paragraph states D3's unnarrowed half. Each new sentence is pinned. | `test_the_home_names_each_thing_no_re_read_clears`, or a new parametrised pin; each red with its sentence deleted (§15) |
| S14: #781 | The *Without the row* sentence names the `Checked` date. `RE_READ_SENTENCES` pins the new words. | `tests/test_a_merge_cannot_silently_drop_a_correction.py` and `tests/test_the_ledger_rules_have_one_home.py`; red with the sentence reverted |
| S15: no pasted passage, no long line, no real identifier | `tests/test_no_passage_is_pasted_into_a_second_file.py`, `tests/test_docs_line_wrap.py`, `tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py` pass | Run narrow, phase 3 |
| S16: the ledger reads clean | `bin/evidence-check --strict --ledger seal/ledger/<this id>.md .` exits 0. The `Corrected ·` row over 0.18.2:91 names the corrected claim's coordinates. | Executed, phase 3 |

## Data & interfaces

- **`reverify`'s positional signature is unchanged.** Its callers are `main`'s
  two arms and the tests. It builds the family view itself from `root`, so a
  test calling it with one ledger still gets the whole repository's
  judgment.
  - The set of coordinates the run left (D3's reason ii) reaches `main`
    through a new keyword argument. It works the way `moves` and `told` do:
    a list the caller passes and `reverify` appends to.
  - The exact name of that argument is the work's.
- **The printed line formats are unchanged**, except the family `LEFT` line's
  remedy clause (D3). The hash line, the `left` reasons, the count line and
  the dated and undated lists keep their words.
- **The record format and `pact-check` are untouched.** A record written
  before this release stays as written.
- **No new dependency, no migration.**

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-05 by framer, before the build.
