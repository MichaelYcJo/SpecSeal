# the file said to delete it when the last box was ticked — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

**This range deletes a shipped section, which is the one case per-survivor
rows cannot serve**, and `skills/code-review/scripts/survivor_check.py`
§*A deletion is one row, because otherwise it is 153* is the escape it is
written for. `docs/flow.md` was 120 lines and every one of them was a
description of something else — a ticket, a release's order, a rule stated
where it is enforced — so the sentences the deletion removes stand by design
in the durable copies: the tickets on GitHub, `CHANGELOG.md`, and the design
records under `seal/specs/`.

**Every reported place was opened rather than waved through, and the ones
that are not records are named here.** The count moves, so it is written with
the tree it was taken in: **32 at `ae2d0ac`** — 29 records, 3 loaded files —
and **36 at the branch tip**, 31 records and 5 loaded files. Two things move
it. The range: `origin/<base>...HEAD` re-resolves, so each commit measures a
wider one. And what this file quotes: an exemption's quote joins the written
side and leaves the search set (#308), so withdrawing the fourth bullet below
returned its place to the reported set. The gate is exit 0 at every one of
them. The loaded-file places, each stating about the code it is written in
the fact the deleted row only pointed at:

- `CLAUDE.md:81` — the repo rule that `seal` named three things at once.
  `docs/flow.md`'s #331 row said the same thing as scheduling rationale, and
  `CLAUDE.md` is the owner: the pointer went, the rule stayed.
- `tests/test_a_record_states_what_the_tree_has.py:1013` and
  `skills/evidence-check/scripts/evidence_check.py:2189` — both record the
  Windows leg of CI having been red on the records arm's coordinate
  assertion. #103's row cited that measurement as its third defect shape;
  both of these are the measurement, written where it was taken.

Correcting any of the three would delete a true sentence from the file that
owns it, in order to remove a resemblance to a row that no longer exists.

**A fourth bullet stood here and described a place wrongly.**
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` carries a
docstring about pytest-xdist being installed by the workflow rather than by
the virtualenv — not the deadlock the bullet described. It was written from
the first run's reading and not re-checked. Round 1 found it (finding 5).

**Withdrawing it is what put that place back in the reported set**, which is
the same #308 behaviour: while the bullet stood, its quote was on the written
side and the place was invisible to the check. So round 1's *not among them*
was true of a tree the bullet itself had made, and round 2 found that
(finding 11). The withdrawal still stands — the sentence was wrong about what
is written there — and the place is excused by the range row like the
others.

| Range | Grounds |
|---|---|
| `origin/release/v0.11.1...HEAD` | The range deletes `docs/flow.md`, a 120-line shipped checklist whose every row described a ticket, a release's order, or a rule owned elsewhere. Its sentences stand in the durable copies a deletion is supposed to leave behind — the tickets, `CHANGELOG.md`, and the records under `seal/specs/` — which is the case §*A deletion is one row* names. All 32 reported places were opened; the three outside the records are listed above and each states the fact where it belongs |

## Round 1's fix range — six per-survivor rows

`bfe8cdb..62c22ca` reported five places, which is few enough for a row each.
The range row above does not reach them: its spec resolves to a different
range, so it excuses nothing here, and the check said so with exit 1.

**Two of the five are the class contract §12 warns about, and both were
opened.** One is a second file making the same heading claim finding 2
corrected; one is a second case asserting `parsed["planning"] is None`. Both
are true where they stand, for reasons that are not the same reason, and each
is written out below rather than summarised.

| Path | Quote | Grounds |
|---|---|---|
| `skills/code-review/orchestration.md` | `The headings keep the` `Orchestrator:` `prefix they were written with` | **The twin of finding 2, and it is true here.** #265 moved five sections into this file and every one of them was already prefixed; none gained the prefix and none changed name, which is what was false of the section #351 added to `skills/implement/orchestration.md`. The wording differs in the load-bearing word too — *written with* covers a section authored in place with the prefix, where *marked with* claimed a marking that predated the move. Correcting this sentence would make a true statement vaguer in order to match a file whose defect it does not share |
| `tests/test_waiver_decided_at_start.py` | `assert parsed["planning"] is None` | **A second case asserts the same expression and its premise is sound.** It reads `templates/sdd-routing.md`, not the committed declarations: the claim is that the shipped placeholder `\| Planning \| <framer, or: the session> \|` must parse as unanswered, so copy-and-never-revisit lands on *not answered* rather than on a wrong record. A template is not a declaration somebody answered, so no legal answer can ever make this fire. Executed 2026-09-11: 17 passed, exit 0 |
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-4.md` | `the exemption count R1 states is three MECHANISMS rather than four entries` | The sentence attributes the mechanism count to **R1**, which is where it is correct and where it still stands after finding 6 moved it off R3. A build phase record states what that phase found on the day it ran; this one found the right thing |
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md` | `seven offending lines remained and all seven were in the file being deleted` | The measurement is stated in the release note and in R1's ledger note on purpose — one is what ships to a reader, the other is the row a checker anchors. Two audiences, one fact, and neither is a restatement of the other's rule |
| `hooks/routing.py` | `as f:` | Incidental idiom, not a shared claim. The overlap the check scored is `with open(path, encoding="utf-8") as f:` followed by a `routing.parse` call — the shape of every reader of a declaration in this repository. There is no sentence here to correct |
| `seal/ledger.md` | `the exemption count is three MECHANISMS, not four entries` | **A survivor by construction: the fix was to remove a duplicate, so the original is what is left.** Finding 6 was that R3 (line 1367) carried R1's note byte-identically. Removing it from R3 makes R1's own copy at line 1366 read as wording the range removed — which it is, at the coordinate it was removed FROM, and not at the one it belongs to. R1 is the row whose clause states the three-exemptions count, so this sentence is correct there and is the only place it now stands. Correcting it would delete the sentence the correction existed to leave in one place |
