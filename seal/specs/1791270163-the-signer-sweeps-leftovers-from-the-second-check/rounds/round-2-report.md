# Round 2 report — 1791270163-the-signer-sweeps-leftovers-from-the-second-check

| Field | Value |
|---|---|
| Target SHA | a374154b |
| Base | `origin/release/v0.20.0` at a9d7b0e5 (the merge base) |
| Range read | round 1's fix range `5bc0a48f..149ef480` (five commits) and the round-close commit `149ef480..a374154b`; round 1's whole range only where a fix leans on it |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at a374154b under the session scratchpad's `1791270163-…/round-2/clone`, run with the worktree's existing `.venv` interpreter (cmarkgfm 2025.10.22, the version `.github/scripts/run_tests.py` pins); the clone and the probes were removed at hand-over |

## Summary

This is the verifying round. All four fixes close the findings they answer,
and each was opened and run here. One gap of the same class as round 1's
yellow 1 is still open, and it sits in an alternative round 1 did not probe:

- **🟡 1 — an ordered list item written `01.` (or `001)`) directly under the
  statement stays exempt.** cmark-gfm ends the statement's paragraph there,
  because the list starts at 1. The span's list alternative accepts only a
  bare `1`. The alternative's text came in with ee631b6b, inside round 1's
  range, and round 1 probed `2.` but not a leading zero. The unit it sits in,
  `without_the_policy_span`, was changed by round 1's fix 5ed7503e, so
  `round-record new` counts this finding as the run's first fix of a fix
  (measured in a dry run of the generator in a scratch clone).
- **⬜ 2 — the overview says `survivor-check` left "no removed wording still
  standing".** Three places still stand and are excused in `survivors.md`.
  This is a correction to the run's paperwork.

Nothing found here loses a record or crashes. 🟡 1 is a gap in a test sweep,
not in `pact-check` or any reader.

## What the account claimed, and what was found

- **Claimed (round 1 record, yellow 1 fixed at 5ed7503e):** a table and a
  footnote definition under the statement now end the span. Executed: the two
  table shapes, a delimiter row directly under the statement's last line, and
  a footnote definition are each green through the span function at 5bc0a48f
  and red at HEAD. cmark-gfm renders each one outside the statement's
  paragraph. The lazy continuation line is green at both, and the unplanted
  file is green at HEAD. Claim holds.
- **Claimed (R6's re-read row, 6365df4b):** the plants above were green
  before the fix and red after it. Executed, as above. Claim holds for the
  shapes it names. It does not name `01.`, which is 🟡 1.
- **Claimed (the ledger fragment's R1 row, 6365df4b):** the new `pact_reviews`
  assertion is red with the quote rebuilt from the cells for a header of more
  than one cell. Executed: the S4 case passes at HEAD and fails with exactly
  that mutation in `hooks/config.py`. `SIGNER_HEADER` has one cell, so the
  mutation touches only the review-record path, and the failure is the new
  assertion. Claim holds.
- **Claimed (the fragment, after the fix pass):** its coordinates are fresh,
  the S4 case at its new hash. Executed: `bin/evidence-check --ledger` on the
  fragment with `--strict`, exit 0, 21 ok, 0 drifted, 0 broken. Claim holds.
- **Claimed (`overview.md:26`, 53649c22):** round 1's fix pass ran
  `survivor-check` over its whole fix range, "exit 0, no removed wording still
  standing". Executed over `5bc0a48f..149ef480`: exit 1 without the exemption
  file, three places standing; exit 0 with `--exempt` pointing at
  `survivors.md`, all three excused. The exit is right and the rest of the
  sentence is not (⬜ 2).
- **Claimed (`overview.md:26`):** a fix pass answers `survivor-check` over its
  own range. Read `agents/smith.md` §*Phases* item 3: it says exactly that.
  Claim holds.
- **Claimed (`survivors.md`):** the three standing places are the frame and
  a dated handoff. Read `spec.md:90`, `questions.md:26` and `handoff.md:14`:
  each is written under the first routing answer or before round 1, and each
  grounds cell says so. The exemptions hold.

## Findings from execution

### 🟡 1 — an ordered list item written with leading zeros directly under the statement stays exempt

`tests/test_one_word_one_meaning.py:749`. The list alternative is
`(?:[-*+]|1[.)])[ \t]`. CommonMark lets an ordered list interrupt a paragraph
when its start number is 1, and cmark reads the start number as an integer
of up to nine digits. So `01.`, `001)` and `000000001.` all start at 1, and
all of them end the statement's paragraph. Each was planted directly under
the statement's last line and run through cmark-gfm and the span function:

| Plant | cmark-gfm renders | span at 5bc0a48f | span at HEAD |
|---|---|---|---|
| `01. a Signatory row` | `<p>` then `<ol>` | green (exempt) | green (exempt) |
| `001) a Signatory row` | `<p>` then `<ol>` | green | green |
| `  01. a Signatory row` (indented) | `<p>` then `<ol>` | green | green |
| `02. a Signatory row` (control) | inside the `<p>` | green | green |
| `1. a Signatory row` (control) | `<p>` then `<ol>` | red | red |

This matters for the same reason round 1's yellow 1 did. `spec.md:24` cites
§12 for this class: "every block GFM lets begin directly under a paragraph's
last line ends the span". The docstring of `without_the_policy_span` says
the same, the changelog fragment says the check "again sweeps whatever
follows", and R6's re-read row dates that claim as true. A person who writes
`01. Signatory …` under the statement gets no red. The shape is rarer than a
table, but the gap is the same quiet one this work item exists to close.

The fix bounds the leading zeros at eight, so the marker is at most nine
digits, which is cmark's own limit. Executed in the clone with the fence
applied: `01.`, `001)`, the indented `01.` and `000000001.` turn red. The
ten-digit `0000000001.`, which cmark keeps inside the paragraph, stays green.
`02.` and `10.` stay green and `1.` stays red. Every one of thirteen plants
agrees with cmark-gfm. The unplanted file stays green, and
`tests/test_one_word_one_meaning.py` passes with the fence (exit 0,
21 passed). The file was restored afterwards.

## Findings from reading

### ⬜ 2 — the overview says no removed wording is still standing, and three places are

`seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:26`.
The row says the fix pass's run ended "exit 0, no removed wording still
standing". The run over `5bc0a48f..149ef480` reports three places still
carrying the removed wording. It exits 0 only because `survivors.md` excuses
all three. A reader who trusts the sentence would not look for
`survivors.md`, which is where the judgment actually sits. This is a
correction to the run's paperwork and is not counted in `Needs a fix`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An ordered list item with leading zeros (`01.`, `001)`) directly under the statement starts at 1, so cmark-gfm ends the statement's paragraph there, but the span's list alternative accepts only a bare `1`, so the old word in it stays exempt | `tests/test_one_word_one_meaning.py:749` | open | executed: cmark-gfm renders `<p>` then `<ol>` for three leading-zero plants; all three green through the span function at 5bc0a48f and at HEAD; the fence turns them red, agrees with cmark-gfm on thirteen plants, keeps the baseline green, and the module passes (21) |
| ⬜ 2 | The overview says the fix pass's `survivor-check` run left no removed wording standing; three places stand, excused in `survivors.md` | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:26` | open | executed: `survivor-check` over `5bc0a48f..149ef480` exits 1 with three standing places, and exits 0 with `--exempt`; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | round 1's yellow 1 is closed for the table and the footnote definition | `tests/test_one_word_one_meaning.py:753` | confirmed | executed: two table shapes, a delimiter row under the statement's last line and a footnote definition, each rendered outside the paragraph by cmark-gfm, green at 5bc0a48f and red at HEAD; continuation and baseline green; the leading-zero list item is this round's yellow 1 |
| 🟢 | round 1's white 2 is closed — R6's re-read row and the changelog name the table and the footnote definition | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | confirmed | read: the row's grounds and the changelog's list name both blocks; executed: the plants the row describes behave as it says; the fragment checks `--strict`, exit 0, 21 ok |
| 🟢 | round 1's white 3 is closed — the overview names the sealer and each fix pass | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24` | confirmed | read against `routing.md` and `agents/smith.md` §*Phases* item 3; the survivor sentence beside it is this round's white 2 |
| 🟢 | round 1's white 4 is closed — the review record's glued quote is pinned | `tests/test_a_signer_declares_its_pact.py:1292` | confirmed | executed: the S4 case passes at HEAD and fails with the quote rebuilt from the cells for a multi-cell header, a mutation only the new `pact_reviews` assertion can see |
| 🟢 | round 1's white 5 stays answered — the comprehension is unchanged | `hooks/config.py:1350` | confirmed | read: `hooks/config.py` is not in the fix range, so the answer's grounds stand as written |

## Executed probes

| What was run | Result |
|---|---|
| cmark-gfm, plain and with footnotes, over eleven plants under the statement's last line; each also through the span function at 5bc0a48f and at HEAD | tables (outer pipes, two cells, a delimiter row directly under the statement) and the footnote definition outside the paragraph, green then red; `01.`, `001)` and the indented `01.` outside the paragraph, green both; `02.` and the continuation inside, green both; `1.` red both; a footnote label with a space stays in the paragraph and is swept at HEAD, which errs toward sweeping more; baseline green |
| the S4 case at HEAD, then with the glued quote rebuilt from the cells for a header of more than one cell | exit 0, 1 passed; then exit 1, 1 failed; `hooks/config.py` restored, clone clean |
| 🟡 1's fence applied in the clone: thirteen plants through cmark-gfm and the fenced span function, the baseline, then `tests/test_one_word_one_meaning.py` | all thirteen agree with cmark-gfm; baseline green; exit 0, 21 passed; the file restored, clone clean |
| `bin/evidence-check --ledger` on this item's fragment, `--strict` | exit 0; 21 ok · 0 drifted · 0 broken |
| `bin/survivor-check --range 5bc0a48f..149ef480`, with and without `--exempt` pointing at `survivors.md` | exit 1, three standing places, without it; exit 0, all three excused, with it |
| `bin/round-record new` over this report, in a second scratch clone, then the clone removed | the record written with all seven verdict rows, both fences and both fields; `Fix of a fix` reads `first`, keyed on `without_the_policy_span`; its chain-check exits 2 only because the clone carries no `origin/release/v0.20.0` |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this round ran none of it, and the sealer answers it once the rounds settle |

## Regression tests to plant

- 🟡 1: no new case. The two sweep cases hold it. The `01.` and `001)` plants
  are the ones to see red before the fence and green after removing it, as
  phase 1 and round 1's fix pass did for theirs.

## Facts for the evidence ledger

- R6's `Re-read ·` row, once 🟡 1's fix lands: an ordered list item that
  starts at 1 with leading zeros (`01.`, `001)`) is green before the fix and
  red after it, in both sweep cases; `02.` and a ten-digit `0000000001.`, which
  cmark-gfm keeps inside the paragraph, are green both times.

## Paste-ready fixes

### 🟡 1

```python
        r"|(?:[-*+]|0{0,8}1[.)])[ \t]"  # a list item that can interrupt a paragraph
```

It replaces line 749 of `tests/test_one_word_one_meaning.py`. An ordered
list interrupts a paragraph only when it starts at 1, and cmark reads up to
nine digits, so up to eight leading zeros before the `1`. Executed in the
clone as described under 🟡 1.

### ⬜ 2 and the R6 row (the run's paperwork)

```text
overview.md, Not verified, the survivor-check row: "round 1's fix pass ran
it over its whole fix range from 5bc0a48f; three places still carry the
wording it removed, each excused in survivors.md, and it exits 0 with that
file as its exemption".
R6's Re-read row, grounds, appended once 🟡 1's fix lands: an ordered list
item starting at 1 with leading zeros (01., 001)) under the statement, green
in both sweep cases before and red after; 02. and a ten-digit marker, which
cmark-gfm keeps in the paragraph, green both times.
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1, an ordered list item written `01.` or `001)`
directly under the statement still stays exempt from the sweep.
Loses a record or crashes: no

## Proof block

Files opened: `tests/test_one_word_one_meaning.py` (`PACT_RENAMED` through
`test_no_pact_text_names_a_signer_the_way_0_18_did`, the `read` helper, the
second sweep's call), its 5bc0a48f version (through the probe),
`tests/test_a_signer_declares_its_pact.py` (the S4 case),
`hooks/config.py` (`SIGNER_HEADER`, `PACT_REVIEW_HEADER`, `read_table`),
`tests/gfm_table_oracle.py` (head and `rendered`),
`.github/scripts/run_tests.py` (the cmarkgfm pin), `docs/the-pact.md`
(the statement under the `1791239490` fold marker), `agents/smith.md`
(§*Phases* item 3, the `survivor-check` step), `agents/sealer.md` (the
survivors arm), this item's `routing.md`, `rounds/round-1.md`,
`rounds/round-1-report.md`, `spec.md` (line 24, through `grep`),
`survivors.md`, the ledger fragment and `overview.md`, both through the fix
diff, and the log and diffs of `5bc0a48f..149ef480` and `149ef480..a374154b`.
