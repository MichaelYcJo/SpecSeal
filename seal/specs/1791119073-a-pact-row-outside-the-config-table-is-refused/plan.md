# Implementation Plan: a pact row outside the config table is refused

<!-- seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

## Summary

`hooks/config.py#pact_declaration` learns to see a `Pact` or `Pact notify`
row with a value that `config_rows` did not read as that row. Such a line
becomes a refusal, and `notify` becomes `None`. The writer, `pact-check` and
`chain-check` already act on that state, so they change no code and gain a
case each. The vendored copy already matches the shape on every line, and
gains only GFM's line cut. Two documents say it, and every new sentence is
pinned.

## Technical context

Read at framing, no line numbers (a line is not a coordinate here):

- `hooks/config.py#config_rows` is the table walk, with the stop rule from
  #82. `#refusal` is the tolerant walk for `broad-gate`. `#unfenced`,
  `#fence_map` and `#hidden_lines` are the one rule for hidden lines.
  `#pact_declaration` builds `rows = config_rows(text)` and filters by exact
  item. `#declared_pacts` is the strict file read.
- `skills/evidence-check/scripts/evidence_check.py#record_pact_changes`.
  The plugin branch's `blind = declared is None or declared[1] in (None,
  NOTIFY_ALWAYS)`, and `refused and unknown` leads to `LEFT` and exit 1. So
  `notify=None` plus one refusal is enough to leave every moved row. The
  vendored branch (`config is None`) matches `NOTIFY_ROW_SHAPE` over
  `said.splitlines()`, and is blind where both items are named.
- `skills/evidence-check/scripts/pact_check.py`, the `declared_pacts` loop:
  each refusal is a `REFUSED` line, and `ONE_SIDED` follows where `pacts`
  lacks this signatory.
- `skills/code-review/scripts/chain_check.py`, the `pact_declaration` call:
  each refusal is a notice, and the exit does not move.
- `hooks/blocks.py#gfm_lines` is GFM's cut, reachable from `hooks/` (the
  `skills/` copies are not).
- `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` is the
  census of `.splitlines(` calls by unit.

**The approach.** Phase 1 adds an index-carrying walk, and `config_rows`
becomes a projection of it with byte-identical output. That gives the set
of line indices the reader took as `Pact` or `Pact notify` rows. A stray is:

- on the reader's cut, an unhidden line matching the shape whose index is
  not in that set; or
- on GFM's cut, a line holding a `str.splitlines`-only character that
  matches the shape, is not hidden, and none of whose pieces' indices is in
  that set.

The notify half refuses only where a `Pact` value stands (`spec.md`
§*Scope* 4).

**What breaks in six months.**

- A new way for `config_rows` to skip a line is added and the detector does
  not hear of it. The detector does not enumerate ways, though. It compares
  the shape against the indices the walk took, so any new skip shows up as
  a stray rather than as silence. That is why this approach was chosen over
  one that lists the ways.
- The two shape copies drift apart. S14 pins them equal.
- Someone narrows the vendored match to the table. S12's mutation shows
  that case red.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A rule for every `seal/config.md` row, in `config_rows` or one level above it | Seven readers gain a refused state. `mode-gate`, a `PreToolUse` hook, would stop sessions on a file it now reads silently, which `hooks/config.py#refusal`'s docstring rules out. `seal mode` could not write the row that ends a refusal. Only the pact reader loses a record that cannot be recovered (`spec.md` §*The decision #759 left open*) | rejected |
| Change `config_rows`'s stop rule so it reads on past the table's end | #82's two rounds rejected exactly this: rows of a second table read as rows of this one. Every reader's answer would change | rejected |
| List each way the table ends, one branch per way (as `gfm_table` does for the `Signatory` table) | The list rots: #735 shipped 14 and its round 3 found 16 cases and three arms that survived their removal. A way not listed is silence | rejected |
| Count shape matches against the pact rows `config_rows` returned, with no indices | Cannot tell which line is the stray, so the refusal cannot name it. Cannot apply the GFM-cut rule (W11) without false refusals | rejected |
| **Indices from one walk, and the shape compared against them on both cuts** | A line the shape over-matches (a quoted example) is refused. That is the cautious direction, and the vendored copy already leaves there | **chosen** |
| Leave the vendored copy as it is | Under W11 the vendored copy re-stamps unrecorded where the plugin now leaves the row. That is round 2 of #756's 🟡 1 class, one cut over | rejected |
| Leave W11 out of scope | Same loss, one character apart. The vendored copy would miss it too, and a reviewer probing #664's characters finds it in round 1. A fix pass could not add the mechanism then | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The reader.** `hooks/config.py`: the index-carrying walk with `config_rows` projected from it; the shape constant; stray detection on both cuts inside `pact_declaration`, before its `not value` return; the refusal sentence; `notify=None`. Cases S1–S8 and S14 in `tests/test_a_signatory_declares_its_pact.py`, each seen red at the base first; census entry updated | that module, `tests/test_the_mode_question_is_asked_once.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_every_reader_ends_a_line_where_gfm_does.py` | |
| 2 | **The callers, end to end.** No code change is expected. S9 and S5's writer half in `tests/test_a_signatory_records_a_pact_change.py`; S10 in `tests/test_pact_check.py`; S11 in `tests/test_a_signatorys_ci_prints_its_pact.py`. Each is red with phase 1's commit reverted | those three modules | |
| 3 | **The vendored copy.** `record_pact_changes`'s vendored branch matches its shape over the reader's cut and `gfm_lines` together. S12, with its mutation, and S13, red at the base. The comment above `NOTIFY_ROW_SHAPE` names the twin in `hooks/config.py` | `tests/test_a_signatory_records_a_pact_change.py` | |
| 4 | **The records.** `docs/the-pact.md` §*How a signatory names the pact*: the clause and its `Enforced by:` cases. The vendored paragraph of §*What this does not see*, where phase 3 changes what it says. `templates/config.md` §*Pact*: the refused-row sentence. S16's pins. The ledger fragment `seal/ledger/1791119073-a-pact-row-outside-the-config-table-is-refused.md`: rows for the new units, and the re-reads of released rows citing edited units, through `evidence-check --reverify --into`. `changelog.md` in this directory | the pin module(s), `tests/test_docs_line_wrap.py`, `tests/test_no_real_identifiers.py`, `evidence-check --strict` | |

The order is the dependency order. Phases 2 and 3 read phase 1's sentence,
and phase 4 cites the units the first three create.

## Operational impact

- No migration, no new environment variable, no new dependency.
- **A compatibility change a signatory may meet.** A `seal/config.md` that
  holds a pact row the reader does not reach now refuses where it was read
  as the default. At the signatory's pull request it is a notice, and the
  exit does not move. At the pact's repository `pact-check` exits 2, and
  under `--reverify` the moved rows are left with exit 1 until the row is
  moved into the table. That is the intended change. The refusal sentence
  says where the row goes.
- **Shared with sibling E** (#774, #772, #775, cut at the same base):
  - `skills/evidence-check/scripts/evidence_check.py#record_pact_changes`.
    E edits the plugin path (#774); this work edits the vendored branch
    (phase 3). Same unit, different arms.
  - `docs/the-pact.md`. E's trigger sentence and its `Enforced by:` line
    are in §*A signatory records a pact change*; this work edits §*How a
    signatory names the pact* and possibly the vendored paragraph.
  - `templates/config.md` §*Pact*. E's trigger sentence and this work's
    refused-row sentence are a few lines apart.
  - `tests/test_a_signatory_records_a_pact_change.py`.
  - The released ledger rows citing `record_pact_changes`
    (`seal/releases/0.18.1.md` rows 168 and 175). Each item re-reads them in
    its own fragment, so the second to land re-reads again.

  Whoever squashes second merges the release branch in and re-runs these
  modules.
