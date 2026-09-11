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

**The 32 were opened rather than waved through, and the three that are not
records are named here.** 29 of the 32 sit in `CHANGELOG.md`, `seal/ledger.md`
or `seal/specs/`. The other three are loaded files, and each one states, about
the code it is written in, the fact the deleted row only pointed at:

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

**A fourth bullet stood here and named a place the check never reported.**
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` is not among
the 32, and the docstring at that line is about pytest-xdist being installed
by the workflow rather than by the virtualenv — not the deadlock the bullet
described. It was written from the first run's reading and not re-checked
against the exempted output. Round 1 found it (finding 5).

| Range | Grounds |
|---|---|
| `origin/release/v0.11.1...HEAD` | The range deletes `docs/flow.md`, a 120-line shipped checklist whose every row described a ticket, a release's order, or a rule owned elsewhere. Its sentences stand in the durable copies a deletion is supposed to leave behind — the tickets, `CHANGELOG.md`, and the records under `seal/specs/` — which is the case §*A deletion is one row* names. All 32 reported places were opened; the three outside the records are listed above and each states the fact where it belongs |
