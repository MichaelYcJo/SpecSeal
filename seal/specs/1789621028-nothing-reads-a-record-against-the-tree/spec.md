# Feature Specification: nothing reads a record against the tree

<!-- seal/specs/1789621028-nothing-reads-a-record-against-the-tree/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

Three tickets, one branch. **#344 is the class and it carries an open question
about its own shape; #426 and #427 are two instances inside the generator that
writes the records.** The milestone's ordering argument is that taking an
instance first fixes it at its own coordinate and the reader that would have
caught all five places is never built, so the shape is decided here, before
anything is built.

## The shape #344 left open, decided from the tree

#344 states the question in its own words: *whether the answer is anchors in
records, a checker that re-reads them, or a rule that a range is pinned when
it is written.* All three were opened against the tree. The answer this work
item builds is **the third, at the one place that has a shape a generator can
write and a checker can read — the record itself.**

Four facts decided it, and each is a coordinate a reviewer can open.

- **The second option is already built, and it is already at its limit.**
  `skills/evidence-check/scripts/evidence_check.py` has a records arm from
  #190 — it reads every live work item's records for a name the tree lacks
  and for a stamp the tree contradicts, and
  `tests/test_a_record_states_what_the_tree_has.py:979` runs it against this
  repository's own records. So *nothing reads a record against the tree* is
  not true as written. What is true is narrower: **nothing reads the parts of
  a record that are claims about commits**, and that checker cannot be the one
  to. Its own module docstring states the bar — *No fixture here runs git, and
  no fixture here may* — because the checker calls git for nothing outside
  `--migrate`. A range is a claim about commits. The checker that reads it has
  to be the one already allowed to ask git, which is
  `skills/code-review/scripts/chain_check.py`.
- **The first option is refused where it would land.**
  `tests/test_a_record_states_what_the_tree_has.py:508`,
  `test_a_location_column_is_not_an_unmigrated_coordinate`, exists to make the
  records arm *not* read a `Location` cell as a coordinate, and
  `templates/sdd-round.md:293` prescribes `path:line` for that cell. Turning
  Locations into content anchors is a migration across 223 committed round
  records and a change to the template's prescribed format, re-anchored by
  people who did not write them. It is a work item, not a phase. Q1 of
  `questions.md` puts it to the repository owner; the default is refused.
- **The prose the range is written in has no shape to check.** Measured across
  the tree on 2026-09-17: **39 fix-table files, 11 of which state a range in
  their first eight lines, in eleven different spellings, and two of the
  eleven name `HEAD`.** `Range \`a..b\`, seven commits, on` ·
  `Range: \`a..b\`. Two commits;` · `The fix range is \`a..b\`, two commits.` ·
  `Fix range \`a..b\`, five commits.` · `Target reviewed \`906c78b3\`, over the
  range \`5137e934..HEAD\`.` — no two alike. A rule enforced by parsing that is
  a rule enforced by guessing.
- **A pinned range and a count derived from it cannot go stale, so nothing
  has to re-read them.** That is what makes the third option the cheap one
  rather than the weak one: prevention at the write is not a lesser form of
  the checker here, it removes the thing the checker would have been for.

**So the authoritative statement of a fix range moves out of prose and into
the record, written by the generator that already resolves it.** The prose
header in a fixes file is left exactly as it stands, and the grounds for
leaving it are the eleven spellings above.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between a refusal the generator makes on its own and a rule a person is told, the first is chosen. Every new refusal here fires without anybody at the keyboard |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Phases 2, 3 and 4 each add a refusal. Each owes a test seen red, a stated failure direction, and a prompt budget in the pull request body |
| `skills/implement/SKILL.md` §3, top rung | This alters what a record asserts and what CI reads at a pull request, so `spec.md` and `plan.md` are owed before the first edit. `routing.md`'s `Planning` row already records that a framer drew them |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* | This is a BUILD, so mechanism is allowed here and not in the fix passes that follow. Anything a later round finds that needs new mechanism is `deferred #N`, not added |
| `agent-contract` §12 | #427's write is one of three verdict words. The fix is owed to all three, not to `fixed` |
| `agent-contract` §15 | Every case this work plants is shown red before it is committed, and the handover says how |
| `agent-contract` §14 | Three refusal messages are text a person reads and acts on. Each is pinned by a case in the same commit |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`. `seal/ledger.md` is touched only if this branch removes code an existing row cites |
| `CLAUDE.md` §*a ledger coordinate names content, never a position* | Ledger rows this work adds carry `path#unit@hash`. It does **not** follow that a record's `Location` cell becomes one — that is Q1, and the tree currently refuses it |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | Two checkers now read a record. Any new name says which reader it belongs to; `tests/test_one_word_one_meaning.py` is the check |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Planted records and fixtures use neutral values |
| `docs/review-chain-spec.md` §*The fix surface — `Contract changes` and `New units`* | The precedent for adding a record field: the generator derives it, the template documents it, `chain_check` reads it, a `*_FROM` cutoff lets earlier work items print instead of fail |

## Scope

### In

1. **#426 — the wholeness guard stops comparing against a constant.**
   `tests/test_chain_hooks_hardening.py`, inside
   `test_the_questions_are_collected_before_the_work_not_during_it` (`:1026`):
   the sweep records `len(body.encode("utf-8"))` and asserts it equals
   `os.path.getsize` of the file it read. The assertion then has no number in
   it to be wrong. Confirmed at the coordinate: the floor is `size > 1000` at
   `:1150`, the comment claiming wholeness is at `:1147`, and `agents/scribe.md`
   is **3764 bytes** — so any truncation between 1001 and 3763 bytes truncates
   all five definitions and the guard stays green.
2. **#427, the write half — `close` stops prefixing a cell it has already
   prefixed.** `skills/code-review/scripts/round_record.py:3771`,
   `cells[GROUNDS_COL] = grounds + (f"; {old}" if old else "")`. The guard
   covers all three verdict words, because `fixed`, `answered` and `deferred`
   all reach that line and all three join rather than overwrite.
3. **#427, the read half — an existing duplicate becomes visible.** A new arm
   in `chain_check.py` names a record whose `Grounds` cell carries its own
   close-prefix twice. The ticket is explicit that stopping the second write
   and leaving the standing duplicates unreadable closes the instance and not
   the class.
4. **#344 — the fix range is pinned where it is written, and read at the pull
   request.** Three parts, and they are one slice:
   - `close --range` refuses an end that is not a commit somebody can open —
     SHA-shaped and resolving to itself. `HEAD`, `@`, a branch and a tag all
     refuse. `parse_range` at `:2737` today resolves any ref and refuses none
     of them;
   - `close` writes the resolved range and its commit count into the record as
     a field, derived from what it already has in hand;
   - `chain_check` re-reads that field against the tree at the pull request,
     behind a cutoff of the `STRICT_FROM` shape (`chain_check.py:480` and the
     nine cutoffs below it), so the 223 records already committed print rather
     than fail.
5. **The five places #344 enumerates, re-located and corrected.** They live in
   `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/`.
   Each correction carries an HTML comment beside it saying what it was read
   against and when — the convention `rounds/round-3.md:19` already records
   for a hand-repaired cell.
6. **The fragments and the closing memo** — `changelog.md`, `seal/ledger/<id>.md`,
   `overview.md`.

### Out, and why

| Left out | Why |
|---|---|
| Content anchors in a record's `Location` cell | The first of #344's three options. 223 records, ~90 work items, a change to the round template's prescribed format, and a case in the tree that exists to refuse it. Q1 puts it to the owner; the default is no |
| Parsing the fixes file's prose `Range` header | Eleven files, eleven spellings, measured. There is no convention there to enforce |
| Widening `evidence_check`'s records arm to do any of this | That checker calls git for nothing, by rule and by its own test module's stated bar. A range is a claim about commits |
| Re-anchoring or re-stamping anything in `seal/ledger.md` | Nothing here removes code an existing row cites. The branch writes its own fragment |
| `evidence-check`'s silence on a malformed coordinate | `seal/follow-up.md` row 1. It is about the ledger's own `ANCHOR_RE` and names a decision the owner has not made. Not a prerequisite this work supplies |
| The `survivors.md` exclusion (#371 and #308) | `seal/follow-up.md` row 4. A different checker and a different class |
| A `deferred #N` Status value in `templates/sdd-plan.md` | `seal/follow-up.md` row 8. This work item writes no such row |
| Records of any work item other than 1789034970's | Unless phase 3's new arm names one at exit 1, in which case that record is corrected in the phase that found it and the fact is recorded |
| A bigger threshold in #426 | The ticket refuses it by name: it moves the silent range instead of closing it |
| Asserting exact byte counts as literals in #426's case | The ticket refuses it by name: a case that reddens on ordinary edits is one people delete |

### Whether a `seal/follow-up.md` row was waiting on this

**No row was, and all eleven were read.** The two that come closest are row 1,
`evidence-check` ignoring a malformed coordinate, and row 9, seven ledger rows
anchored on a whole heading path. Both are about the **ledger's** anchors and
about `evidence_check`; this work item changes neither that checker nor any
anchor. Nothing here unblocks them and no row is deleted.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A definition is truncated in the middle of the silent range | Given the sweep's read is `f.read(2000)` · When the module runs · Then it is exit 1 | `bin/test tests/test_chain_hooks_hardening.py`, three mutations: `f.read(10)`, `f.read(2000)`, the loop's iterable replaced by `()`. Each exit 1, baseline exit 0 |
| The wholeness guard does not redden on an ordinary edit | Given any definition is reworded · When the module runs · Then it is exit 0 | Add a sentence to `agents/scribe.md` in the worktree, run the module, revert |
| A record corrected and re-closed does not double its grounds | Given a record whose Verdict cells were restored to `open` and whose Grounds still carry a close-prefix · When `round-record close` runs with the same fix table · Then it refuses, names the finding, and writes no cell | The #427 reproduction, run against a planted record; and the guard deleted, the same input, the doubled row produced |
| The guard covers the class, not the word | Given the same situation with `answered` and with `deferred #N` · When `close` runs · Then each refuses | One case per verdict word, each seen red with the guard deleted |
| A record already carrying a doubled cell is named | Given a planted record whose `Grounds` cell carries two close-prefixes · When `chain-check` runs at the pull request · Then exit 1, naming the file, the finding number and the repeated text | A planted fixture; and this repository's 223 committed records at exit 0 — measured 2026-09-17 as **zero** surviving duplicates, which the phase discloses rather than claims as a catch |
| A fix range cannot be stated as something that moves | Given `close --range <a>..HEAD` · When it runs · Then it refuses, names the end, and writes no cell | A probe against a scratch repository, driven from Python (§8) |
| The record states the range as commits somebody can open | Given `close --range <a>..<b>` with both ends pinned · When it runs · Then the record carries the resolved range and the commit count the tree holds | Read the written record; compare the count with `git rev-list --count <a>..<b>` |
| A record whose stated range the tree contradicts is named at the pull request | Given a record whose count or whose ends disagree with the tree · When `chain-check` runs · Then exit 1, naming the record and which half disagrees | A planted record, exit read directly (§1) |
| A work item begun before the cutoff is not failed by the new field | Given a record with no such row and a work-item id below the cutoff · When `chain-check` runs · Then it prints and does not fail | The 223 records already in the tree, at exit 0 |
| Each new refusal is text a reader can act on | Given each of the three refusals · When it fires · Then the message says what is wrong and what to do instead, and a case pins that half | `agent-contract` §14. The refusal's second half is the half that has to survive a reword — `seal/follow-up.md` row 7 is this exact omission, found in an earlier release |
| The five places say what the tree says | Given each of #344's five bullets · When it is opened at its coordinate · Then either the record is corrected, or the bullet's premise is recorded as false today with what was found instead | Read-only. Each corrected line quoted in `overview.md` beside what it was read against |

## Data & interfaces

Nothing on the wire and no schema. Three shapes change, and all three are read
by machines:

- **`round-record close`'s argument contract.** `--range` gains a refusal. The
  set of inputs it accepts narrows, which is a contract change in the sense
  `docs/review-chain-spec.md` §*The fix surface* uses — the round record for
  this work's own review will carry it.
- **The round record's field table.** One row is added. `templates/sdd-round.md`
  documents it, `chain_check` reads it, and a cutoff of the `STRICT_FROM` shape
  governs which work items it is fatal for. `docs/review-chain-spec.md` gains
  the subsection, beside §*The fix surface* which is its model.
- **`chain_check`'s exits.** Two new refusals. Neither may fail open
  (`tests/test_gates_do_not_fail_open.py` is the standing check).

Ledger rows this work adds go in `seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md`,
as `path#unit@hash`, kept as they are settled and written at a phase boundary.

## Open questions → questions.md

Four rows, and only one of them is a person's. `questions.md` in this
directory carries them, and its head lists what the tickets left open that the
tree answered — so nobody reopens the shape decision above without reading why
it went the way it did.

<!-- The line below is the framer's mark. -->

Framed 2026-09-17 by framer, before the build.
