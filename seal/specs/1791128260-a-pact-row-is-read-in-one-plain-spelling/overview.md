# a pact row is read in one plain spelling — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this item; `docs/the-pact.md` §*How a signatory names the pact*, §*What this does not see*; `templates/config.md` §*Pact*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file*; PR #784's branch at `b16cee46` (its code, tests and `rounds/round-4-report.md`)
· evidence: `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md` — ten `Re-read ·` rows, one `Corrected ·` row for 0.18.1 C1, and O1–O3
· verified: executed — the four pact modules, the census, the S11 modules and every module reading a touched document, narrow; 35 `mutation-check` breaks, each red; red-at-base runs per phase. Not run — the full suite, the sealer's

## Why this work exists

A pact row the table walk did not take was read as the default, so
`--reverify` re-stamped a moved row with no pact-change record; now a pact
row is read in one spelling and every other line naming a pact is refused.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The vendored copy's line reading | Scope 2: "It judges each line by the line's own shape instead (`CONFIG_ROW_RE`, already in the file)." / the code reads a line by its row shape only where no `str.splitlines`-only character cuts it | the code | `CONFIG_ROW_RE`'s `\s` takes U+2028 and kin, so a cut `Pact` row matched it as plain while the plugin refuses it; the guard is the reader's own `pieces == 1` condition (`phases/phase-3.md`) |
| S9 (a)'s corpus run | "the S2 corpus run through the vendored branch" / the whole corpus runs through `notify_may_be_always` in-process, and 25 spellings run end to end | the code | 1,751 subprocess runs with a scratch repository each would cost minutes per run of the module; the branch is one line that calls the unit |
| S6 | one writer case / two: a notify line below a `Pact` row, and a `Pact` line below a table that holds none | both | the second is where "refusing is not split by item" reaches the writer |
| The evidence-check skill's vendored sentence | spec silent (Scope 5 lists `docs/the-pact.md` and `templates/config.md`) / `skills/evidence-check/SKILL.md` §*Re-verifying is recomputing the hash* gained the refused-line clause | the code | it stated the old vendored rule, which became incomplete; worded apart from `docs/the-pact.md` because `test_no_passage_is_pasted_into_a_second_file` measures the pair |
| Record lines naming #784's units | `spec.md`, `plan.md` and `phases/phase-1.md` name `stray_refusal`, `shape_line`, `PACT_ROW_SHAPE` and others / `evidence-check --strict` refused them as names not in the tree | each line carries `NAME NOT IN TREE`; `spec.md`'s framing stamp on `templates/config.md#"## Pact"` is written without the stamp form | they name #784's units on purpose; the framing stamp states a hash framing saw, which the template's edit moved |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at the head | the sealer, spawned by the orchestrator after the rounds settle |
| The merge with sibling E (PR #786): both move `record_pact_changes`' hash and both edit `tests/test_a_signatory_records_a_pact_change.py`, so whichever squashes second re-reads the rows citing it again at the merged base | the orchestrator, at the second squash |

## Not done

The blind side is documented and not closed (Q1, default (a)). YAML front
matter, which github.com renders as a table and cmark-gfm does not, is not
read; the orchestrator ruled it out of scope in round 1 of PR #793.

## Fed back into the spec

- *Inferred during implementation:* the vendored copy reads a line by its row
  shape only where no `str.splitlines`-only character cuts it (Scope 2).
- *Inferred during implementation:* one predicate serves both readings,
  `names_a_pact(text, piped=True)`, with `piped=False` for a walked row's item
  (the plan's `word(item)`).
- *Inferred in round 1's fix pass of PR #793:* a file holding an HTML table
  cell (`HTML_CELL`, `<td` or `<th`) drops the pipe condition for every
  line, in both readers.
- *Inferred in rounds 1-3's fix passes of PR #793:* a line directly above
  one `UNDER_A_HEADER` matches is a table's header, read whole and with no
  `|` asked, by both readers: the delimiter row is read as cmark-gfm renders
  one (outer pipes optional, a vertical tab or form feed, a block quote, a
  one-column row with no pipe), held by construction against the oracle.
