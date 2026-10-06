# Round 3 report — 1791270163-the-signer-sweeps-leftovers-from-the-second-check

| Field | Value |
|---|---|
| Target SHA | eea27ad0 |
| Base | `origin/release/v0.20.0` at a9d7b0e5 (the merge base) |
| Range read | round 2's fix range `f649a21b..e3c9bc9d` (four commits) and the round-close commit `e3c9bc9d..eea27ad0`; nothing else in the branch was re-reviewed |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at eea27ad0 under the session scratchpad's `1791270163/round-3/clone`; cmark-gfm through `cmarkgfm` 2025.10.22, the version the repository's test runner pins; the probe file was deleted after its run and the clone removed at hand-over |

## Summary

This is the verifying round, and the last one of this run. Both of round 2's
fixes close their findings, and neither opens a new one. Each was opened here
and each was run.

- **Round 2's yellow 1 is closed.** An ordered list item that starts at 1
  with leading zeros now ends the policy span, exactly where cmark-gfm ends
  the statement's paragraph. Nineteen plants were run through the span
  function before and after the fix and through cmark-gfm, and all nineteen
  agree with cmark-gfm at HEAD.
- **Round 2's white 2 is closed.** The overview's `survivor-check` row now
  says what the tool does over round 1's fix range.
- **The fix pass's own paperwork holds.** Its new `survivors.md` row excuses
  the one survivor `survivor-check` names over round 2's fix range. The R6
  re-read row in the ledger fragment is at the new hash and checks clean.
- **⬜ 1 — one docstring line was not reflowed.** The fix inserted three
  sentences into `without_the_policy_span`'s docstring and left
  `continuation line stays inside,` as a short line of its own. It reads
  badly. Behaviour and facts are right, so it does not count toward
  `Needs a fix`.

Nothing in this range loses a record or crashes. The span function is a test
helper, and no reader or hook changed in the range.

## What the account claimed, and what was found

- **Claimed (round 2 record, yellow 1 fixed at 1ffe9e75):** an ordered list
  item written `01.` or `001)` under the statement now ends the span.
  Executed: `01.`, `001)`, `000000001.`, `00000001)`, ` 01.`, `   001)` and
  `01.` followed by a tab, each planted directly under the statement's last
  line, are green through the span function at f649a21b and red at eea27ad0.
  cmark-gfm renders each one as an `<ol>` outside the paragraph. Claim holds.
- **Claimed (the docstring at `tests/test_one_word_one_meaning.py:737`):**
  `02.` and a ten-digit `0000000001.` stay in the paragraph. Executed: those
  two, plus `10.`, `00.`, `0.`, `011.`, `001 .`, a four-space `    01.`,
  `01.signatory` and `01)signatory`, are green both before and after the fix.
  cmark-gfm keeps every one inside the paragraph. `1.` and `1)` are red both
  times. Claim holds, so the at-most-nine-digit bound in `0{0,8}1` is right
  on both sides.
- **Claimed (R6's re-read row, 55801b0f):** the row names the zero-padded
  plants, and `without_the_policy_span` is at `942fa103`. Executed:
  `bin/evidence-check --ledger` on the fragment with `--strict` exits 0,
  21 ok, 0 drifted, 0 broken. The plants the row names behave as the row
  says (the probe above). Claim holds.
- **Claimed (`overview.md:26`, cdee5dfe):** round 1's fix pass left three
  places standing, each excused in `survivors.md`, and the tool exits 0 only
  with that file as its exemption. Executed: `bin/survivor-check --range
  5bc0a48f..149ef480` exits 1 with three places, and exits 0 with `--exempt`
  pointing at `survivors.md` (all three excused). Claim holds.
- **Claimed (`survivors.md`, e3c9bc9d):** the one survivor of round 2's fix
  range is another work item's scenario quoting the line `survivor-check`
  prints for a clean run. Executed: `bin/survivor-check --range
  f649a21b..e3c9bc9d` exits 1 and names exactly
  `seal/specs/1790260564-a-moved-file-counts-as-written/spec.md:173`, and
  exits 0 with `--exempt`. Read: the quoted line is the one the tool prints
  for a clean run, at `skills/code-review/scripts/survivor_check.py:2197`.
  The grounds are true.
- **Claimed (round 2 record, closed at eea27ad0):** `New units` none,
  `Contract changes` none. Read: the fix range adds no `def` and changes no
  signature. The one code change is one alternative of the regex inside an
  existing unit, plus its docstring. Claim holds.

## Findings from reading

### ⬜ 1 — a short docstring line left behind by the inserted sentences

`tests/test_one_word_one_meaning.py:741` reads only
`continuation line stays inside,`. The fix inserted its three sentences
in front of `A lazy` and did not reflow what followed. Every other line of
the docstring runs to the same width, so this one reads like a paragraph
break that is not there. No behaviour and no stated fact changes. A fence is
given below for convenience only.

### Class enumeration (agent contract §12)

The class is "a paragraph-interrupting block the span's regex does not end
at". The fix's alternative is the only list-start alternative in the span
function. Read: the other list-marker regexes in the tree, in
`hooks/config.py:1043`, `hooks/blocks.py:104`,
`skills/evidence-check/scripts/evidence_check.py:5191`,
`skills/settle/scripts/settle.py:561` and
`skills/code-review/scripts/survivor_check.py:583`, recognise a list item
anywhere and do not decide whether one interrupts a paragraph. None of them
carries the start-at-1 rule, so none is an instance of this class.

One overreach is still there, and it errs toward sweeping more. An empty
item such as `01. ` followed by a line end matches the alternative, but
cmark-gfm does not let an empty item interrupt a paragraph. That is the same
behaviour `1. ` and `- ` had before this work item. It can only make the
sweep stricter, never let the old word through, so it is not a finding.

## Findings from execution

None beyond the confirmations above.

## Regression tests to plant

None. The plants were run as a deleted probe, the same way R6's re-read row
records the earlier rounds' plants, and the sweep cases read the real
`docs/the-pact.md`.

## Facts for the evidence ledger

None new. R6's re-read row already states what this round ran again.

## Broad gate

Not yet run. This round leaves nothing open that needs a fix, and the round
record after it ends the run. So the broad gate has come due: the sealer is
the next spawn. That spawn runs the full suite, the repository-wide lint and
the typecheck once, at the settled HEAD.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The fix's inserted sentences left `continuation line stays inside,` as a short docstring line of its own, unreflowed | `tests/test_one_word_one_meaning.py:741` | open | read: the line and its neighbours; cosmetic, the behaviour and the stated facts are right, so it is not counted in `Needs a fix` |
| 🟢 | round 2's yellow 1 is closed — a list item starting at 1 with leading zeros ends the span | `tests/test_one_word_one_meaning.py:753` | confirmed | executed: nineteen plants through the span function at f649a21b and eea27ad0 and through cmark-gfm; eight zero-padded starts at 1 green before and red after; ten shapes cmark-gfm keeps in the paragraph green both times; all nineteen agree with cmark-gfm at HEAD; the unplanted file green; `tests/test_one_word_one_meaning.py`, 21 passed |
| 🟢 | round 2's white 2 is closed — the overview's survivor row states the tool's result | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:26` | confirmed | executed: `survivor-check` over `5bc0a48f..149ef480` exits 1 with three places, and exits 0 with `--exempt` pointing at `survivors.md`, as the row now says |
| 🟢 | round 2's fix pass excused its one survivor with true grounds | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/survivors.md:24` | confirmed | executed: `survivor-check` over `f649a21b..e3c9bc9d` names only `spec.md:173` of another work item, exit 1, and exits 0 with `--exempt`; read: the quote is the tool's own clean-run line at `skills/code-review/scripts/survivor_check.py:2197` |
| 🟢 | R6's re-read row is at the fixed unit's hash and names the zero-padded plants | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | confirmed | executed: `evidence-check --ledger` on the fragment, `--strict`, exit 0, 21 ok; the plants it names behave as it says |
| 🟢 | round 1's yellow 1 stays closed for the table and the footnote definition | `tests/test_one_word_one_meaning.py:757` | confirmed | read: the fix changed only the list alternative, and the table, footnote and break alternatives are byte for byte as round 2 executed them |
| 🟢 | round 1's whites 3, 4 and 5 stay closed or answered | `tests/test_a_signer_declares_its_pact.py:1292` | confirmed | read: no file those three name, other than the overview row above, is in round 2's fix range, so round 2's grounds stand; carried, not re-run |

## Executed probes

| What was run | Result |
|---|---|
| a deleted probe: nineteen list-marker plants directly under the statement's last line, each through the span function taken from f649a21b and from eea27ad0, and the statement's paragraph plus the plant through cmark-gfm | all nineteen agree with cmark-gfm at HEAD; `01.`, `001)`, `000000001.`, `00000001)`, ` 01.`, `   001)` and `01.` with a tab green before and red after; `1.` and `1)` red both times; `0000000001.`, `02.`, `10.`, `00.`, `0.`, `011.`, `001 .`, `    01.`, `01.signatory` and `01)signatory` green both times; the unplanted file green at HEAD |
| `bin/test tests/test_one_word_one_meaning.py -q -n auto` in the clone at eea27ad0 | exit 0, 21 passed |
| `bin/survivor-check --range f649a21b..e3c9bc9d`, then with `--exempt` pointing at `survivors.md` | exit 1, one place, `seal/specs/1790260564-a-moved-file-counts-as-written/spec.md:173`; then exit 0, one excused |
| `bin/survivor-check --range 5bc0a48f..149ef480`, then with `--exempt` pointing at `survivors.md` | exit 1, three places; then exit 0, three excused |
| `bin/evidence-check --ledger` on this item's fragment, `--strict` | exit 0; 21 ok · 0 drifted · 0 broken |
| `bin/round-record new` over this report in the clone, `--baseline a9d7b0e5`, then the clone reset | see the line under this table |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this round ran none of it, and the sealer answers it once, next |

The `round-record new` dry run's result is in the hand-over summary rather
than here, because this report is its input.

## Paste-ready fixes

### ⬜ 1

```python
    line over a delimiter row (#831). An ordered list interrupts a paragraph
    only when it starts at 1, and cmark reads a start number of at most nine
    digits, so `1.`, `01.` and `000000001)` end the span while `02.` and a
    ten-digit `0000000001.` stay in the paragraph (round 2 of #831). A lazy
    continuation line stays inside, and so does a pipe line over a `---` with
    no pipe in it, which GFM makes part of the statement's setext heading. The
    delimiter's cell count is not matched against the header's, so the end
    errs toward sweeping more. The cut is made before flattening, which is
    what would erase the blank line."""
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened in this round:

- `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/rounds/round-2.md`
- `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/rounds/round-2-report.md` (head and the claims section)
- `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/survivors.md`
- `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/changelog.md`
- `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md` (lines 15–40)
- `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md` (the diff of rows 1–3)
- `tests/test_one_word_one_meaning.py` (lines 708–800 and 855–880)
- `docs/the-pact.md` (the statement at line 27 and its paragraph)
- the diffs `f649a21b..e3c9bc9d` and `e3c9bc9d..eea27ad0`
- `bin/test`, `.github/scripts/run_tests.py` (the `cmarkgfm` pin only)
