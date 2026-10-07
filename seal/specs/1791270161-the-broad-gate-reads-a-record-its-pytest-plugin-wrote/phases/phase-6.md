# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | e4b1187b |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The gate says what the record left out (`spec.md` Scope 6 as reframed;
round 3's 🟡 3 and ⬜ 4). `NO_RECORD_AT_HEAD` and `NO_RECORD` name both
causes of a missing record; `RunRecord` gains `unplaced`, summed by
`read_record` from the `end` lines; the failure form prints one sentence
where the head record's count is non-zero; the **New?** bullet of
`skills/verify/SKILL.md` follows the reasons; pins moved (S27, S28). S27
and S28 seen red, a mutant of the count through `bin/mutation-check`.

## What this phase found

**The two causes are the only two left.** With the refusal and the guard
gone in phase 5, a pytest that loaded the recorder and wrote no record is
one whose `SPECSEAL_RECORD_DIR` it could not open or write, and the
recorder then warns `specseal_pytest_record: no record written: <error>`.
The two reasons name that warning by its text, through one shared clause,
`NO_RECORD_CAUSES`, formatted with the kept file each run's output is in
(`suite.txt` at `HEAD`, `suite-at-base.txt` at the base). The pin also
asserts the recorder's source still carries the warning's text, so the
reason cannot name a warning the recorder stopped printing.

**The same one-cause sentence stood in five more places**, enumerated by
grepping every shipped file for "loaded the recorder" and "loaded the
gate's recorder" (§12): rule 3's base row of the table and its `HEAD`
fallback sentence, the **New?** bullet's first two causes, the changelog
fragment's `new?` bullet and its fallback sentence, and three comments in
`broad_gate.py` (`failure_lines`, the heading constants, the failure loop).
Each now says "left a record"; rule 3's and the bullet's two sentences and
the changelog's are pinned, and the one-cause wording is asserted gone.
Sentences in cases that describe a layout where no pytest loaded the
recorder (a row that runs no pytest, a first runner under `env -i`) are
true of their layout and stand.

**The sentence prints wherever the suite failed and the count is
non-zero**, not only under a listing: a session whose only failure is a
test with no file of its own has an empty list, and the sentence is then
the one line that says why the suite is red. It is printed unindented, so
`verdict_of` and every reader of `  <file>  <word>` lines never take it for
a file.

**Seen red (executed).** Run through a script that put 2775a237's
`broad_gate.py`, `skills/verify/SKILL.md`, `templates/config.md`, the
changelog fragment and the recorder in place and restored them from the
bytes it read first: 6 failed — the reader's unit case (`RunRecord` has no
`unplaced`), the reasons pin (the one-cause text), both gate cases over the
sentence (no `UNPLACED`), the rule-3 pin and the S28 pin (the recorder's
count sentence). The self-removing module through the gate passed there, as
it should: it pins phase 5's Alternative U, and its red is the `isfile`
mutant below.

**Mutants (executed, `bin/mutation-check`, each `red`):** the `end`-kind
check dropped and the integer check loosened (the unit case, which plants
an `unplaced` on a `test` line and one spelled as a string); the count set
rather than summed (three records, 2 and 1); the sentence printed always (a
failing suite whose record placed everything); the head record's count not
handed to the failure form (S27 through the gate); the recorder's `isdir`
made `not isfile` (the self-removing module through the gate, which then
reads `new`).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| "no pytest … loaded the gate's recorder" as the one cause of a missing record, in both reasons, rule 3, the **New?** bullet, the changelog fragment and three comments | "left a record", with both causes named (`NO_RECORD_CAUSES`) |
