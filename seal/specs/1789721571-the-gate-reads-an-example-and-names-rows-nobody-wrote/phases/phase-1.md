# 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 59c750a |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#430's class, enumerated as four sites in `spec.md` §*The two classes,
enumerated* → *#430 — a sentence about what lies below a line, computed
without asking*, all four in `skills/verify/scripts/broad_gate.py`:
`missing_row`'s `stopper is None`, `mine is stopper` and `reached` arms, and
the `hides_this_row(below)` refusal below them. The `else` arm was named out
of scope and left. With them: `missing_row`'s docstring paragraph that
enumerates the arms, `skills/config/SKILL.md`'s sentence about what a bare
pipe costs, one case per site each seen red against its own unfixed arm, A9
keeping the old sentence alive, and A11 run before and after.

The spawn carried the wording contract from `spec.md` §*Data & interfaces*
and one instruction about method: *Each arm asks `below` as well as
`stopper`. `missing_row` already holds `below` — it is the second element it
unpacked.* It also carried a standing order — confirm each site's
reachability before writing its case, and where a site is not reachable as
framed, leave it out of scope and say which and why rather than writing a
case that cannot be seen red.

`hooks/config.py` and `skills/implement/scripts/seal.py` were phase 2's and
not to be touched.

## What this phase found

**All four sites are reachable as framed, and the enumeration is complete.**
Measured before the first edit, by calling `hooks/config.py#refusal` and
`config_rows` over eight files built to reach each arm in both directions.
Q2 of `questions.md` is answered *all reachable* for #430's half; #429's
three shapes are phase 2's to measure. Site 4 in particular is reachable with
`below` holding exactly this gate's row — `[('Broad gate', 'bin/test -q')]` —
which is the state in which *Every other row under that line is gone the same
way* names a row nobody wrote.

**One instruction in the spawn is false, and it is the one about method.**
`below` is not available to site 1 and never can be. `hooks/config.py#refusal`
appends to `below` only under `if stopper is not None`, so `below` describes
the rows written under the STOPPING line — and site 1 is by definition the arm
where no line stopped the reader. Measured: the same arm reached with the
quoted line as the table's only row and with a `Mode` row written under it
gives `below == []` both times, while `config_rows` gives `[]` and
`[('Mode', 'shared')]`. An arm keyed on `below` would have printed *nothing
was written below it* over a file whose `Mode` row had arrived perfectly well
— which is #415 round 1 🟡 1 coming back one sentence over, the exact failure
this work item is the second half of.

What site 1 reads instead is what the table reader returned, through the same
reader, in a new unit `broad_gate.py#rows_read`. That is a safe question in
that arm alone, and the unit's docstring carries the proof: a row that had
parsed ABOVE the quoted line would have set `stopper` to that line, which is
site 2's arm, so in site 1 every row the reader returned is below the quoted
line. Sites 2, 3 and 4 read `below` exactly as the spawn said. The divergence
is written up in `overview.md` with both sides quoted.

**Two cases already in the suite pinned the defect, and both keep their
subject.** `test_a_second_refused_line_is_what_decides_what_a_first_one_cost`
asserted `LOST` for a file whose refused `Broad gate` line is the last row of
its table — four lines under a docstring paragraph saying in so many words
that such a line *loses nothing below it, because there is nothing below it*.
The defect and its own description were sitting one paragraph apart, recorded
as what the tree did. `test_the_gate_reads_every_refused_line_and_not_only_the_first`
carried the same assertion over a second last-row fixture. Both are about
which ARM is chosen, which is unchanged and still pinned by the assertion
beside each; only the sentence the arm prints moved. Neither rewrite was
foreseen by `plan.md`, and `questions.md` Q4 is the same question one phase
early — the answer here is *a fixture's answer moved, and it was a case
pinning the defect*.

**Failure direction: none, as `plan.md` predicted.** No arm is chosen
differently, no verdict changes, and nothing new can refuse. A11 measured
before and after: this repository's own `seal/config.md` gives mode `shared`,
the `Broad gate` command byte-identical to the row as written, `refusal` of
`([], [], None)`, and no refusal built at all. It is now a case rather than a
one-off reading.

**Platform.** Nothing here inspects a process or a path, so no branch varies
by operating system. The one console fact worth recording for phase 2: an
ad-hoc probe printing these messages on this machine raises
`UnicodeEncodeError: 'cp949' codec` on the em dash, and `PYTHONIOENCODING=utf-8`
is the way past it. It is a property of the console; `broad_gate.py` moves its
own streams to UTF-8 at `main`, and the suite never meets it.

**What phase 2 has to know.** `missing_row` now calls the table reader twice
for one refusal — `refusal(home)` and, in site 1's arm only, `rows_read(home)`
— and each call re-reads `config.md` and re-imports `hooks/config.py` by path.
The fence rule phase 2 puts in that module therefore has to answer the same
way on both calls, which it will by construction since both go through the
same module. Phase 2's own `broad-gate` sentence about a fenced
`| Broad gate |` line lands between site 4's refusal and the absent-row
refusal, and the four sentences above are the regression surface its cases
re-run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The unconditional sentences at three of `missing_row`'s arms and at the hidden-row refusal | Nowhere — each is still printed, now under the condition that makes it true. `survivor-check --range 9d13934..59c750a` reports no removed wording still standing (exit 0, read directly) |
| `LOST` as the assertion for a last-row fixture, in two existing cases | The new wording, in the same two cases, with the arm each pins untouched; and `test_a_refused_line_last_in_its_table_took_nothing_and_is_told_so`, which pins both directions of that shape |
