# Feature Specification: the checker is wrong about itself, and nothing goes red

<!-- seal/specs/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Release 0.11.5's first and only work item. Six tickets, three packages, one
thread: **every one was found by a review round exercising the review chain's
own checker, and every one is that checker saying something false while the
suite stays green.**

The thread is not a theme somebody noticed afterwards. It is the reason the six
belong in one work item rather than six, and it decides what the acceptance
below is about: not the edits, but **what would now go red**. Five of the six
are states the suite is silent on today, and the sixth (#395) is a seam that
was built, found to be wrong in four places, and then reverted whole rather
than shipped.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides the two judgments the tickets leave open (#335, #333): between two designs that catch the same defect, the one that stops to ask a person is the more expensive. It does **not** license catching less. |
| `skills/agent-contract/SKILL.md` §12 *A defect belongs to a class — enumerate the class* | Three of the six tickets name one coordinate for a defect with more than one instance in the tree. #142 names one `_real_records`; there are two. #395's boundary claim is stated in five carriers. The fix is owed to every instance, and the handover says which were enumerated. |
| `skills/agent-contract/SKILL.md` §15 *A new case is not planted until it has been seen red* | Every ticket here exists because a case was green over a defect. A case planted by this work that has not been seen red repeats the thing being repaired. |
| `skills/agent-contract/SKILL.md` §14 *A fix that changes what a person sees documents it and pins it* | #333 and #335 both change a refusal message a person is stopped by, and #334 is entirely about a message's two readings. The new text is pinned in the same commit. |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* | #334's repair **is** a unit, and so is #142's positive control. Both must arrive with a build phase, not in a review round — see `plan.md`'s phase order. |
| `templates/sdd-round.md` §*New units* — *A fix pass may add a unit. That unit's fix may not*, and the depth is declared **per entry** | The rule `depth_two` enforces, and the sentence that decides #333: one fix pass can produce a depth-1 and a depth-2 unit in the same breath, so a per-file answer is structurally unable to state what the record is required to state. |
| `docs/review-handoff-protocol.md` §*The Fixes checked by field* — *Only a later round may be named, so the **last** record of a finished run can only read `no fixes to check` or `nobody — <why>`* | **Decides #335**, and it is ratified policy rather than a template. `docs/review-chain-spec.md` §*What the record carries* says it twice more (*a checker has to be later, and the last record has none*), and `skills/code-review/orchestration.md`'s three-value table a third time. |
| `templates/sdd-round.md` §*Fixes checked by* — *naming a `round-N` says a later round opened these fixes* | The same rule where the value is written. `CHECKER_RE` tests the shape and cannot test the position, which is the whole of #335. |
| `templates/sdd-round.md` §*Inherited coordinates* — *Coordinates carry; conclusions do not* | The section #342 is about. The `Why` cell carries a conclusion today, and that is what goes stale. |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | Evidence rows go to `seal/ledger/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red.md`; the changelog entry goes to this directory's `changelog.md`. Neither `seal/ledger.md` nor `CHANGELOG.md` is appended to. |
| `CLAUDE.md` §*A ledger coordinate names content, never a position* | The rows this work writes are `path#major@hash`, with no line number and no commit. |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | The fixtures #334 and #142 need are neutral-valued; `tests/test_no_real_identifiers.py` reads them. |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* | Why #395 exists at all: work item `1789356180` was taken one round past the bound, the broad gate showed the cost, and `1ff0a6c` reverted rounds 2 and 3 whole. This work item is where that seam comes back. |

## Scope

### In — six tickets, and exactly these six

| # | Where | What is wrong, in one line |
|---|---|---|
| **#395** | `skills/code-review/scripts/round_record.py`, `tests/test_a_finding_id_is_a_bare_integer.py`, `docs/review-chain-spec.md`, `seal/ledger.md` | The whole reverted seam: the verdict-column arm, the crash it introduced, and the seven prose and assertion defects around them. |
| **#342** | `round_record.py#inherited_rows`, and the reach that does not exist | Two records committed together state the same eight findings as open and as fixed. |
| **#335** | `round_record.py#seal` | `CHECKER_RE` tests the shape of `Fixes checked by` and not its position, so `round-N` on a **last** record passes the refusal, the cell is written, and the chain check that runs after refuses the same row. |
| **#334** | `skills/verify/scripts/broad_gate.py` ← `round_record.py` | The gate discriminates on a literal the other package prints; nothing binds them, and changing the print leaves 130 cases green. |
| **#333** | `round_record.py#depth_two` | `inside = [n for r, n in added if r == f]` compares the FILE, so every unit added to that file is attributed to whichever fix row the walk reaches first. The refusal fired correctly and named the wrong finding and the wrong enclosing unit. |
| **#142** | `tests/test_chain_check_at_the_pull_request.py#_real_records` and its twin | Says it reads HEAD, calls `git ls-files` which reads the index; and nothing tests the test — replacing both `failures.extend(errors)` with `pass` leaves it green. |

### #395's real shape, because the ticket's title is not its body

The map that reaches a reader from the ticket list is *four prose and assertion
edits*. That is the first half of the ticket. Its second comment (2026-09-14)
widened it, and the widened version is the scope:

`1ff0a6c` reverted **round 2's fix (`7b2c0d7`) and round 3's (`fec2c88`)
together**, because round 2's is what introduced the crash round 3 repaired.
With both gone, no later record closes on a fix, the reopening bound is never
approached, and the crash never lands. What the revert also took out is the
whole verdict-column arm, its bounds guard, its cases and its prose. So #395 is
**build, not repair**:

1. **The verdict-column arm** (round 2's 🟡 7). `verdict_rows` builds `seen`
   from the whole row and hands `finding_number` the `#` cell alone, so a row
   whose `Verdict` cell reads the literal `open` is admitted as commissioning
   nothing whenever its `#` cell carries no owed marker, and `Pass` is ticked
   over it. Six shapes measured passing at exit 0, three of them carrying no
   severity marker at all.
2. **The bounds guard the arm needs** (round 3's 🔴 1), at `VERDICT_COL` and
   **not** the header width. The wider bound turns
   `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one` red,
   which is a shipped decision to show the column a reviewer left out rather
   than invent one.
3. **The boundary** (round 4's 🟡 2). The word ends on a **space or a comma** —
   the boundary `verdict_of` actually uses — not on `chain.SEPARATORS`. Ending
   it on `SEPARATORS` over-refuses `open-ended question` and `open: see 5`, and
   couples the open verdict to a constant five other readers share.
4. **The measurement** (round 4's 🟡 1). `127 / 9 / 118` does not reproduce;
   the module's own reader gives 95 / 7 / 88 over 1,704 rows. It reaches three
   files and, once folded, the shared ledger.
5. **The overturned comment** (round 4's 🟡 3, round 3's 🟡 3). `OPEN_WORD`'s
   comment describes the exact match that was replaced, ten lines above the
   function that replaced it.
6. **The assertion that admits both answers** (round 4's 🟡 4).
   `test_a_row_missing_only_its_grounds_is_still_written_short` asserts
   `code in (0, 2)`, so it cannot fail on the regression its own name
   describes. The behaviour is correct; the case is wrong.
7. **Two notes** (round 4's ⬜ 5 and ⬜ 6): the short-row guard raises on the
   first offending row where `id_refusal` beside it names every one (#303's
   shape, two round trips per repair), and a rewrap left a three-word line in
   `docs/review-chain-spec.md`.

**Two things the reverting branch kept and this work must not undo:**
`docs/review-chain-spec.md` no longer names an unreleased version, and
`templates/config.md`'s exclusion list holds `out of verified scope`.

### Out — and why each, stated so a reader does not have to check

All five were in the 0.11.5 milestone on GitHub. **The owner moved each to
`release: 0.12.0` before this work item opened** — verified 2026-09-15 against
the tracker, where the 0.11.5 milestone now holds exactly the six tickets
above and nothing else. The reason is per-ticket as well as per-release:

| # | Title, shortened | Why it is out |
|---|---|---|
| #344 | five places where a round record says something the tree does not, and nothing reads a record against the tree | Moved to 0.12.0. It is the same thread one level up — a record against the tree rather than a checker against itself — and it needs a reader that does not exist. Sized as its own work item. |
| #174 | the broad gate's record cell holds one entry, and a run can run it more than once | Moved to 0.12.0. It is a design question about the cell's arity, and #335 changes what `seal` will write into that same cell — taking both at once would argue two designs over one row. |
| #159 | a record cell corrected in place leaves no trace, and the enforcement that caught it cannot survive the squash | Moved to 0.12.0. Marked `design:`; the repair is a mechanism choice the release has no room to argue. |
| #149 | a record says what ran a segment and what it cost, and not what its output cost the next reader | Moved to 0.12.0. Marked `design:`; touches the segment record, not the checker. |
| #331 | five ambiguous words were each found by a reader one at a time, and nothing sweeps for the sixth | Moved to 0.12.0. Its **trap** is nevertheless in scope as a constraint — see the acceptance row S12 — because #395's docstring figure is the sixth wrong measurement it is about. The sweep is out; the discipline is not. |

### Also out, and this one is not a ticket

**The broad gate is not this work item's to run.** `skills/agent-contract/SKILL.md`
§2 assigns it to `agents/sealer.md`, once, after the rounds settle. The frame
names it here because `1ff0a6c` exists precisely because a broad gate was run
and found what the rounds had not, and a reader could mistake that for an
instruction to run one early.

## User scenarios & acceptance *(mandatory)*

These become the review's stage-1 checklist. **Every row is written as a state
that is green today and must go red** — that is the shape the thread demands,
and a row phrased as an edit does not satisfy it.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| **S1 · a row the record itself calls open is not admitted** | Given a verdict row whose `#` cell carries no owed marker and whose `Verdict` cell reads the literal `open` · When it goes through `round-record new` · Then the run refuses, naming the row, and `Pass` is not ticked over it | A case per shape, over all six measured shapes, three of them carrying no severity marker. Each seen red against the arm removed. |
| **S2 · a numbered short row is refused, not a traceback** | Given a verdict row with a digit in its `#` cell and fewer cells than `VERDICT_COL` · When it goes through `new` **and** through `close` · Then both exit 2 with a sentence quoting the row, and neither raises `IndexError` | Cases on both subcommands. Red against the arm without the bound: the exit is 1 with a stack trace. |
| **S3 · a four-cell row that merely lacks its grounds is still written short** | Given `\| 1 \| one \| \`f.py:1\` \| open \|` · When it goes through `new` · Then the record is written at four cells and the exit is **0** — asserted as `code == 0`, one answer | The repaired case. Red under the header-width bound, which is the wrong bound this row exists to refuse. |
| **S4 · the open verdict ends on a space or a comma** | Given the verdict cells `open`, `open — deferred`, `open, comment only`, `open-ended question`, `open: see 5`, `opened in round 2` · When each is read · Then the first three are the open verdict and the last three are not | A parametrised case over the six spellings. Red under the `chain.SEPARATORS` boundary (which admits two of the last three) and red under equality (which rejects two of the first three). |
| **S5 · widening `chain.SEPARATORS` does not widen the open verdict** | Given `chain.SEPARATORS` gains a character · When the open-verdict reader runs · Then nothing it accepts changes | A case that mutates the constant and asserts the reader is unmoved. This is the coupling half of #395's boundary finding and the half a boundary change alone leaves open. |
| **S6 · the figure in the docstring is the figure the module's own reader gives** | Given the corpus of committed round records · When the count behind the docstring is re-taken · Then the number in the file and the number the reader gives are the same | **How the replacement was taken is part of the row** — see `plan.md` §*#331's trap, and how the new figure is taken*. The figure is stated with its population, its date and its command. |
| **S7 · the comment above the reader describes the reader** | Given `OPEN_WORD`'s introducing comment · When it is read beside the function ten lines below · Then it does not describe an exact match | Pinned the way the spec's copy already is, by a case naming the claim — `survivor-check` is structurally blind here, because the diff removes the sentence nowhere. |
| **S8 · two records committed together do not contradict each other** | Given round N-1's findings inherited into round N as `open`, and round N-1 then closed on its fix table · When both records are read · Then round N's inherited rows state what round N-1's verdict cells state | A case over a two-record fixture: close N-1, read N, assert the words agree. Red against the tree today, where N reads `open` and N-1 reads `**fixed**`. |
| **S9 · `seal` refuses `round-N` on a last record before writing the cell** | Given the last record's `Fixes checked by` reading any of `round-1`, `round-9`, `round-2.md`, `ROUND-1` · When `round-record seal` runs · Then it refuses at exit 2, **no cell is written**, and no `round-record: sealed` line is printed | Four cases, one per measured value. Red against the tree today, where all four pass the refusal, the cell is written, and the chain check that follows refuses the same row. |
| **S10 · changing the generator's print turns the gate red** | Given `round_record.py`'s `round-record: sealed` print changed to any other word · When the suite runs · Then at least one case fails | A case over the **real** pair — the real `seal` against a fixture record in each of the two states, asserting what the gate then prints. Red under the mutation; today 130 cases pass, exit 0. |
| **S11 · a depth-2 refusal names the finding whose fix added the unit** | Given a fix range where two findings in one file each sit inside a round-1 unit, and each fix adds a unit · When `close` refuses · Then the message names, for each unit, the finding whose fix commit added it | A case built on the measured #30 shape (🟡 13 at `:386-395` inside `SUMMARY_WORDS`, 🟡 14 at `:313-322` inside `quote`). Red today: the walk names whichever row it reaches first. |
| **S12 · a refusal it cannot attribute exactly still fires, and says so** | Given a fix range where one commit answers two findings, so no unit resolves to a single row · When `close` runs over a genuine depth-2 unit · Then it still refuses, and the message says the attribution is file-level and names every candidate finding rather than asserting one | A case over a single-commit fix range. The direction is decided in `plan.md` §*The two judgments*; this row is where it is checked. |
| **S13 · the real-records reader reads HEAD, and a staged record is not skipped** | Given a round record staged and not committed · When the case that walks this repository's own records runs · Then the record is not silently listed-and-skipped | A case over the lister itself. Today `git ls-files` lists it, `read_record` returns `None`, `stopping_floor` returns `([], [])`, and the case stays green. |
| **S14 · emptying the failure collection makes a case go red** | Given both `failures.extend(errors)` calls replaced with `pass` · When the module runs · Then at least one case fails | The positive control #142 asks for: a fixture record known to be refused, asserted to produce a failure, **through the same call path**. Not another assertion on the same loop. |
| **S15 · the class, not the coordinate** | Given the two `_real_records` copies (`tests/test_chain_check_at_the_pull_request.py`, `tests/test_the_reopening_is_one.py`) and the third corpus reader in `tests/test_a_finding_id_is_a_bare_integer.py` · When the repair lands · Then every member is repaired or is named with the reason it is not | §12. The handover states which were enumerated and what the enumeration was run against. |
| **S16 · this repository's own records still pass** | Given every change above · When the two cases that walk this repository's real records run · Then neither fails | `test_this_repositorys_own_round_records_pass_the_per_record_checks` and `test_this_repositorys_own_records_are_not_refused_by_the_reopening_walk`. **This is the row `1ff0a6c` was written for.** A stricter checker can turn the tree's own 176 parsed records red, and that cost does not appear on a pull request as one line. |

## Data & interfaces

No schema, no endpoint, no payload. What changes shape is three surfaces a
person or a checker reads, and the third is the one a reader will miss.

| Surface | Change | Who reads it |
|---|---|---|
| `round-record new` / `close` exit codes and refusal text | One new refusal (the verdict-column arm), one changed refusal (short rows, now bounded), one rewritten refusal (`depth_two`'s attribution) | The reviewer at the keyboard, and the orchestrator reading an exit code. §14 applies to all three. |
| `round-record seal` accepted values for `Fixes checked by` | Narrows on a last record. The refusal's *the row holds one of three values* sentence stops being true where it is printed | The sealer, and `broad_gate.py`, which reads the printed line. |
| `## Inherited coordinates`'s `Why` cell | Reaches its final word instead of freezing at `open` | The fix pass the next record is the agenda for. |

**The coordinates this work is anchored on** go to
`seal/ledger/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red.md`,
as `path#major@hash`. Two existing shared-ledger rows are in the blast radius
and are **not** appended to: `seal/ledger.md` S12 (`broad_gate.py#gate`,
`#seal_record`, and the stubbed case) states three coordinates all on the
*reading* side of #334's seam — the new claim is a fourth coordinate on the
*writing* side and belongs in this work item's own fragment. `plan.md` names
them; it does not write them.

## Open questions → questions.md

Six rows, and only one of them is a person's. See
`seal/specs/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/questions.md`.
The two judgments the tickets state and refuse to settle — #335 and #333 — are
**not** among them: both are decided in `plan.md` §*The two judgments*, with the
document that decides each, because a question a document could have answered
was never a question (`skills/implement/SKILL.md` §1).
