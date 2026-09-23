# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 3b1618a |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

The row the guard finds. `seal/ledger.md`'s *The last round's fixes are read
by nobody …* row REMOVED; one row in
`seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md`
anchored on the `docs/review-chain-spec.md` unit that carries the #33
measurement (`spec.md` G4), with no anchor under `seal/specs/`;
`docs/the-evidence-ledger.md`'s `1788184145` sentence rewritten. Verified by
`bin/evidence-check --strict .` exiting 0, `./bin/settle` naming no row, and
`grep -n "seal/specs/" seal/ledger/1790138190-*.md` finding no anchor.

## What this phase found

**Two pins, both seen red first** — executed at `a118b74` with the row still
in place: `2 failed`, the first naming `seal/ledger.md:78  The last round's
fixes are read by nobody …`. Green after the removal.

`test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item` asks
`anchored_rows` over **every** work item directory, released or not, rather
than only the released ones the report reads. That is the rule G4 leaves
behind — no row this branch writes may anchor under `seal/specs/`, its own
directory included — and it has no floor: at zero directories the list is
empty and the property still holds.

**The unit the new row anchors on is the section, not a sentence in it.**
`docs/review-chain-spec.md#"## Two records, and what each of them says"`,
`--reverify` `00000000 -> 61feb2c9`. The implement skill says to leave the
minor level off unless whole-unit hashing has been measured to drift rows on
unrelated edits, and nothing here measured that.

**The plan's grep finds two lines, and neither is an anchor** (executed):
lines 8 and 10 of the fragment are inside its HTML comment and name
`seal/specs/` in prose; neither carries `#…@hash`. The pin above is the
check that reads coordinates rather than text, and it is green.

**Verified by, as run** (executed, exit codes read directly):
`bin/evidence-check --strict .` exit 0; `./bin/settle` exit 0 with no
`anchored` heading in its output; `tests/test_settle_reads_before_it_removes.py`
and `tests/test_docs_line_wrap.py` `103 passed`;
`tests/test_the_last_rounds_fixes_are_checked.py`, the one other module that
names `1788184145`, `72 passed` — it cites the round-3 path in a docstring,
which is a prose citation the next fold is handed (`spec.md` O4).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md` §*Who checked the last round's fixes*, row *The last round's fixes are read by nobody …*, anchored at `seal/specs/1788184145-…/rounds/round-3.md` | `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md` G4, anchored at `docs/review-chain-spec.md` §*Two records, and what each of them says* |
| `docs/the-evidence-ledger.md`'s *That question, for `1788184145`, the one directory held this way today, is carried by #517's design comment* — answered | the same paragraph: *that trade was taken (#517)* |
