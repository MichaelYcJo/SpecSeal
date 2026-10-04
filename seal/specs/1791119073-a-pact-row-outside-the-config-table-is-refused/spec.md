# Feature Specification: a pact row outside the config table is refused

<!-- seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#759. A `| Pact notify | always |` row that `seal/config.md` holds where
`hooks/config.py#config_rows` does not read it is read as the default,
`when the pact is touched`. Under `always`, `evidence-check --reverify` then
re-stamps a moved ledger row citing no clause and records no pact change.
The re-stamp clears the drift, and the drift is the only thing that would
have recorded it. #756 closed the same loss for a vendored copy and for a
doubled row; this closes it for a row the reader never reaches.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-pact.md` §*How a signatory names the pact* | One reader answers both rows for every caller, and a value that will not parse, or a row written twice, "has no value at all". A row written where the reader does not read it joins that list |
| `docs/the-pact.md` §*A signatory records a pact change* | The record is written inside the re-read, and a declaration that will not read leaves the row rather than re-stamping it. The writer's `blind` rule (`skills/evidence-check/scripts/evidence_check.py#record_pact_changes`) already does that for `notify=None`; this work only has to produce `notify=None` |
| `docs/the-pact.md` §*What this does not see*, the vendored paragraph | A copy with no `hooks/` leaves a moved row wherever `seal/config.md` holds a `Pact` row and a `Pact notify` row that both carry a value. That copy has to stay at least as cautious as the plugin's reader after this work |
| `templates/config.md` §*Pact* | "A row that will not parse is refused in a sentence, never read as absent." This work extends that sentence to a row the reader does not reach |
| `hooks/config.py#config_rows` docstring, #82 rounds 1 and 2 | The table ends at the first line that is not a row, a second header, or a stray separator. **This rule does not move.** Other readers depend on it, and the fix sits beside it rather than inside it |
| `hooks/config.py#unfenced` and `#hidden_lines` (#429, #667) | A line inside a closed fence or a closed line-start HTML comment is not a line of any table here. A pact row there is an example, and it is not refused |
| `hooks/config.py#declared_pacts` docstring (round 1 of #647, white 5) | The pact reader is the one reader in this module that refuses rather than failing silent, on purpose. The scope decision below rests on this |
| `tests/test_every_reader_ends_a_line_where_gfm_does.py` (#664), and round 2 of #756, 🟡 1 | `config_rows` cuts lines with `str.splitlines` and reads cell space as Python's `\s`. A detector that cuts or matches any other way misses rows the reader reads. Census reason `F` is the one a new split in this unit takes |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Enumerate the class; pin every sentence a person reads; see each new case red |

## The decision #759 left open: pact rows only

#759 asks whether the rule covers every `seal/config.md` row or only the pact
rows. **Only the pact rows.** The tree decides it. Below is every reader of
`config_rows`, and what a refusal of a whole file would do to each.

| Reader | Row it reads | What an absent row does today | What a file-wide refusal would do |
|---|---|---|---|
| `hooks/config.py#declared_mode`, read by `hooks/mode-gate.py` (a `PreToolUse` hook) and `seal mode` | `Mode` | Loud already. The first Bash call is denied and the second is asked until `seal mode` writes the row (`templates/config.md` head) | A `PreToolUse` hook that refuses wrongly stops a session with nobody able to get past it. `hooks/config.py#refusal`'s docstring records that `mode-gate` deliberately does not ask it |
| `hooks/config.py#reference_roots` | `Reference specs` | The default: every `specs` directory outside the root is history, read and never written | A new state for every check that asks it. A misplaced row errs toward reading more as history, and no record is lost |
| `skills/verify/scripts/broad_gate.py#broad_command`, `#rows_read`, `#refusal` | `Broad gate` | Loud already. Exit 2 with nothing run, and the refusal names a fenced, commented or piped row (`missing_row`) | Nothing new. The row is already refused when it is not read |
| `skills/evidence-check/scripts/correction_check.py#cutoff_at`; `skills/evidence-check/scripts/evidence_check.py#frozen_from` through `#config_reader` (`#vendored_config_rows` in a copy) | `Ledger frozen from` | No freeze. `--reverify` re-stamps released rows in place, and correction-check's arm is off | Silent, the one non-pact case that is. But nothing is lost: the in-place re-stamp is a diff to `seal/releases/*.md` that the pull request shows, and git keeps the old hash. It is reported as a candidate below, not built here |
| `skills/settle/scripts/fold_check.py#declared` | `Fold shape from`, `Document line ceiling`, `Over the ceiling` | The fold arms are off | A new `Unusable` state for the release step. No record is lost |
| `skills/implement/scripts/seal.py` (re-exports `config_rows`; `with_row` writes) | `Mode` | `seal mode` fills the row | A refused file would stop `seal mode` writing the row that ends the refusal |
| Sessions reading the prose rows | `Commit and pull request language`, `Record language` | English, visible in every output | Nothing to refuse to; a session reads the file |
| `hooks/config.py#pact_declaration`, read by `chain_check.py`, `pact_check.py` (through `#declared_pacts`) and `evidence_check.py#record_pact_changes` | `Pact`, `Pact notify` | **Silent, and the loss cannot be undone.** The re-stamp clears the drift that is the only trigger for the record (`record_pact_changes` docstring: "a re-stamp without its record would lose the trigger for good") | Already a refusing reader. `notify=None` with a refusal is a state all three callers handle today |

The pact reader is the only one whose default destroys the evidence that
would correct it. It is also already documented as the module's one
refusing reader (`declared_pacts`, white 5). Every other reader's failure
direction is documented as silence on purpose, or is already loud. A
file-wide rule would add a refused state to seven readers to close one loss.

## Scope

**In.**

1. `hooks/config.py#pact_declaration` refuses a **stray pact row**. A stray
   pact row is a line shaped as a `Pact` or `Pact notify` row with a value
   that `config_rows` did not read as that row. The reader's answer then
   carries a refusal sentence naming the line, and `notify` is `None`, the
   value a doubled row already produces. `pacts` stays the list the table
   parsed.
2. **The shape** is the vendored copy's grammar, word for word, held once
   in `hooks/config.py` and pinned equal to
   `evidence_check.py#NOTIFY_ROW_SHAPE`. That grammar is any case, any
   indentation, an optional block-quote `>`, a pipe, `Pact` or
   `Pact<\s+>notify`, a pipe, and a first value character that is neither
   space nor pipe. Requiring a value keeps the template's empty rows
   (`templates/config.md`, the `| Pact |  |` and `| Pact notify |  |` rows)
   from being refused. Round 2 of #756, 🟡 2, is why.
3. **Where a stray is looked for: two cuts.** The first is the reader's own
   cut: `unfenced(text.splitlines(), text)`, the same line source
   `config_rows` reads, with `\s` as Python reads it. The second is GFM's
   cut, `hooks/blocks.py#gfm_lines`. On that cut, a line holding a character
   that only `str.splitlines` ends a line at counts as a stray only when the
   reader read none of its pieces as a pact row. That catches
   `| Pact notify | always |`: GFM renders it as one row, and the reader
   cuts it into two lines that are neither row. It leaves
   `| Pact | URL | | Pact notify | always |` read as it is today, because
   the reader takes both of its pieces. A line hidden by `hidden_lines` is
   not a stray on either cut.
4. **A stray `Pact notify` refuses only where a `Pact` value stands.** That
   value can be in the table, or on a stray `Pact` line. A notify row with no
   pact is ignored today wherever it stands (`templates/config.md` §*Pact*,
   "ignored where none does"). Refusing it would leave every moved row in a
   repository that holds no pact, which is round 2 of #756's 🟡 2 in the
   plugin's reader. A stray `Pact` line with a value always refuses. With no
   `Pact` row in the table it is the worse case, because under the default
   `notify` a row citing that pact's clause is re-stamped unrecorded
   (`record_pact_changes`: `names` is empty, so it returns 0).
5. **The vendored copy gets the same rule.** It already matches its shape on
   every line, inside the table or not (`record_pact_changes`, the
   `config is None` branch). So every stray on the reader's cut already
   leaves the row there. What it lacks is the GFM cut: under
   `| Pact notify | always |` beside a `Pact` row it re-stamps
   unrecorded, where the plugin will now leave the row. The vendored branch
   matches its shape over the union of both cuts.
6. The callers change no code. Each gets a case end to end:
   `record_pact_changes` leaves the row (`LEFT`, exit 1, nothing re-stamped,
   nothing recorded); `pact-check` prints `REFUSED` and exits 2; `chain-check`
   prints the refusal as a notice and its exit does not move.
7. The documents say it, and the sentences are pinned (§14).
   `docs/the-pact.md` §*How a signatory names the pact* gets the clause and
   its `Enforced by:` cases. `templates/config.md` §*Pact* extends its
   refused-row sentence.

**The class, enumerated by construction** (§12). A pact row with a value
fails to reach `config_rows` in one of these places. Each is read off the
code of `config_rows`, every arm of it:

| # | Where the line stands | The arm of `config_rows` that passes it by |
|---|---|---|
| W1 | Above the first `\| Item \| Value \|` header, and in a file with no header at all | `if not seen_header: … continue` |
| W2 | Between the header and the first row, on a line `CONFIG_ROW` does not match | the `if not match:` arm with nothing found: `continue` |
| W3 | Below a blank line that ended the table | `if not match: if found: break` |
| W4 | Below a paragraph of prose, a heading, a list item, a thematic break or an HTML block line that ended it | same arm |
| W5 | Below a second `\| Item \| Value \|` header, in a second config table | `CONFIG_HEADER.match(line) … if found: break` |
| W6 | Below a stray separator, or a delimiter row of another table | `CONFIG_SEPARATOR.match(…) … if found: break` |
| W7 | Below a pipe line of another width, such as the header of a three-column table (`templates/config.md` ships them) | `if not match: if found: break` |
| W8 | **The pact line ends the table itself**: indented one to three spaces, block-quoted, three or more cells, no closing pipe, or an escaped pipe against the closing pipe (#415's narrowing) | same arm, on the pact line |
| W9 | Read as a row, under another spelling: another case (`pact notify`), a doubled inner space, or a Unicode space inside the item (`Pact notify`) | taken, but `item == PACT_NOTIFY_ROW` is false |
| W10 | After a character only `str.splitlines` ends a line at, on a line the reader's cut makes a row-shaped line of its own (`prose \| Pact notify \| always \|`) | W3 or W4 on the reader's cut |
| W11 | A pact row GFM renders whole that the reader's cut splits into pieces neither of which is a row (`\| Pact notify \| always \|`) | W8 on each piece |

**Out.**

- **Every other row of `seal/config.md`.** The decision above gives the
  grounds. The one silent case among them is a misplaced `Ledger frozen from`
  row. It is a different failure, because nothing is lost. It is reported to
  the orchestrator as a candidate to file, not built.
- **`config_rows`'s stop rule and output.** They are unchanged. An internal
  walk that also yields each row's line index is allowed (plan, phase 1),
  as long as `config_rows` returns the same list for every input.
- **A pact row inside a closed fence or a closed line-start HTML comment.**
  It is an example, under #429 and #667's rule, and it is not refused. The
  vendored copy still leaves a row there. That is the cautious direction,
  and round 3 of #756 confirmed it cannot lose a record.
- **A pact row marked as a list item** (`- | Pact notify | always |`). Both
  grammars read it as prose, and GFM renders no row there.
- **`chain-check`'s and `pact-check`'s `notify` wording** ("a value that will
  not parse", "will not parse"). It is printed beside the new refusal
  sentence, which names the real cause. A row the reader does not read as
  one is a row that did not parse. Rewording two pinned prints is not this
  work.
- **`evidence_check.py#vendored_config_rows`.** It reads `Ledger frozen
  from` alone, and no pact value passes through it. Under the decision
  above it gets no rule.

## User scenarios & acceptance *(mandatory)*

In every row, "refused" means `pact_declaration` returns a refusal sentence
naming the line as written, and `notify` is `None`. `URL` is
`git@example.com:org/orders-api.git`.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 W3 | A table with `Mode` and `Pact URL`, a blank line, then `\| Pact notify \| always \|`. **Then** refused | case in `tests/test_a_signatory_declares_its_pact.py`, red at the base |
| S2 W1–W8, W10 | Each way in the table above, one parametrized case per way, with `Pact URL` in the table. **Then** refused | same module, one id per way, each red at the base |
| S3 W9 | `\| pact notify \| always \|`, `\| Pact  notify \| always \|`, `\| Pact notify \| always \|` inside the table. **Then** refused | same module |
| S4 W11 | `\| Pact notify \| always \|` inside the table, under `Pact URL`. **Then** refused | same module, the character built from its code point |
| S5 stray `Pact` | `\| Pact \| URL \|` below the table's end, and none in it. **Then** refused, `pacts == []`. Under the default notify, `evidence-check --reverify` with a moved row citing `pact:orders-api/…` leaves it: exit 1, nothing re-stamped, nothing recorded | reader case, and a writer case in `tests/test_a_signatory_records_a_pact_change.py`, red at the base |
| S6 no pact, stray notify | No `Pact` value anywhere, and `\| Pact notify \| always \|` below the table. **Then** `([], None, [])`, as today | reader case; a writer case: re-stamped at exit 0 |
| S7 not a stray | A pact row inside a closed fence, inside a closed HTML comment, as a list item, and with an empty value (`\| Pact notify \|  \|`) below the table. **Then** no refusal, and the table's own rows read as today | reader cases |
| S8 read as today | `\| Pact \| URL \| \| Pact notify \| always \|` in the table. **Then** `notify == "always"` and no refusal | reader case |
| S9 the writer | S1 with a ledger row citing no clause whose code moved. **When** `evidence-check --reverify --into …` runs. **Then** a `LEFT` line naming the refusal, exit 1, the ledger byte-identical, and no `seal/pact-changes/` | `tests/test_a_signatory_records_a_pact_change.py`, red at the base |
| S10 the pact's repository | S1 at a signatory. **When** `pact-check` runs at the pact's repository. **Then** a `REFUSED` line carrying the refusal sentence, and exit 2 | `tests/test_pact_check.py`, red at the base |
| S11 the signatory's CI | S1. **When** `chain-check` runs. **Then** a notice carrying the refusal sentence, and the exit status unchanged | `tests/test_a_signatorys_ci_prints_its_pact.py`, red at the base |
| S12 the vendored copy, cut | A copy with no `hooks/`, under S1. **Then** the moved row citing no clause is left, exit 1 | this holds today. The case is seen red by narrowing the vendored match to lines inside the table |
| S13 the vendored copy, GFM cut | A copy with no `hooks/`, under S4. **Then** left, exit 1 | red at the base: re-stamped at exit 0 today |
| S14 one grammar | `hooks/config.py`'s shape and `evidence_check.py#NOTIFY_ROW_SHAPE` have equal `pattern` and `flags` | a case. It is seen red by editing either pattern |
| S15 nothing else moves | Every existing case of the four pact modules, `tests/test_the_mode_question_is_asked_once.py` and `tests/test_the_seal_is_taken_once_by_the_sealer.py` passes unchanged | those modules, run at the phase boundary |
| S16 the sentences | `docs/the-pact.md` §*How a signatory names the pact* and `templates/config.md` §*Pact* say a pact row the reader does not reach is refused, never read as the default. The refusal sentence's text is pinned | a pin per sentence, seen red with the sentence deleted |

## Data & interfaces

- `hooks/config.py#pact_declaration(text)` keeps its return shape,
  `(pacts, notify, refusals)`. What is new: one refusal per stray line, and
  `notify = None` where a stray stands under a `Pact` value. A stray `Pact`
  line refuses with `pacts` as the table parsed them, so `pact-check` also
  reports `ONE_SIDED` where the table named no pact. That is the true
  consequence.
- **The refusal sentence names the line as written, stripped, and says
  where it should go.** The builder chooses the final text, and S16 pins it.
  It reads after "a `Pact` row this CI does not verify: " in `chain-check`,
  after `REFUSED <url> seal/config.md` in `pact-check`, and after "the
  `Pact` rows will not read: " in the writer's `LEFT` line, so it starts
  lower-case with the quoted line. A shape that fits all three:
  `` `| Pact notify | always |` is shaped as a `Pact notify` row and is not
  read as one — it stands outside the `| Item | Value |` table or spells the
  item another way; write it as a row of that table ``.
- A module constant for the shape in `hooks/config.py` (a name such as
  `PACT_ROW_SHAPE`). It is equal to
  `skills/evidence-check/scripts/evidence_check.py#NOTIFY_ROW_SHAPE`, and
  S14 pins the equality.
- A new `.splitlines(` call in a `hooks/config.py` unit takes a census entry
  in `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS`,
  reason `F`. If the split moves out of `config_rows` into an
  index-carrying walk, the entry moves with it.
- Ledger rows that cite a unit this work edits are released rows under
  `Ledger frozen from` (`seal/config.md`), so they are re-read in this work
  item's fragment (`docs/the-evidence-ledger.md` §*A released row is read
  again in the branch's fragment*). Seen at framing, read: `0.18.0.md` row 6
  (`pact_declaration`, `declared_pacts`), row 8 (`templates/config.md`
  `## Pact`); `0.18.1.md` rows 168, 170, 175, 201, 228. `evidence-check`
  names the full set at the build.

## Open questions → questions.md

`questions.md` holds no row only a person can answer. Its head lists what
the tree decided, so nobody reopens it.

Framed 2026-10-04 by framer, before the build.
