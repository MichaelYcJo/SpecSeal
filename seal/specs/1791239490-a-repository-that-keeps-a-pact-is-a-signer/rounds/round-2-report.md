# Round 2 report — 1791239490-a-repository-that-keeps-a-pact-is-a-signer

| Field | Value |
|---|---|
| Target SHA | ec7974055bc05fb933948f5f8022e74f3336e23f |
| Base | `origin/release/v0.19.0` |
| Pull request | #827 (draft) |
| Round kind | verifying — round 1's fix range `d1e0b2c6..b4a5ebb4` |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Round 1's one blocking-class finding is closed. A pact or a pact review
record that holds both headers now reads the `Signer` table and refuses the
old one in every shape round 1 named. A file with one header, or one that
names the old word in prose, a fence or a comment, is not refused.
`pact-check` exits 2 on each two-table shape, and `chain-check` prints the
refusal as a notice with its exit unchanged. The policy span now ends at
the next `##` heading. The tree-wide case refuses the word in every live
file round 1 planted it in. All seven cases the fix pass wrote or rewrote
fail against the reader as it stood before the fix.

What remains is six ⬜, none of which ships a defect:

1. `read_table` names one old table twice when its header is written
   without spaces (⬜ 5).
2. The policy span still runs past a heading below level 2 (⬜ 6). This is
   round 1's white 2 one level down.
3. The tree-wide case exempts five test modules whole, where every use it
   needs is the capitalised header cell (⬜ 7).
4. Two fixtures describe their shape backwards (⬜ 8).
5. The policy's `Enforced by:` line misses the two new cases that hold its
   new clauses (⬜ 9).
6. Two ledger rows carry stale evidence (⬜ 10). This is a paperwork
   correction.

HEAD of the checkout and of the clone stayed at ec797405 for the whole
round.

## What this round was asked

Whether round 1's yellow 1 refusal reaches every shape round 1 named, for
a pact and for a pact review, without refusing a one-header text or the
old word in prose. Whether `pact-check` exits 2 and `chain-check` keeps its
exit on those shapes. Whether the policy span ends at its statement, and
whether the tree-wide case holds every tracked live file, with its
exemptions read as places the word could return through. Whether the eight
units the fix pass added are correct. Whether ledger rows R1, P8, R5 and R6
say what the code now does.

Carried from round 1 rather than re-derived: the enumeration of readers.
There are three call sites, all through `hooks/config.py#read_table`. A
`git grep` at ec797405 for `read_table(` finds the same two callers,
`pact_signers` and `pact_reviews`, so the carry held.

## Findings — from execution

### Round 1's yellow 1 is closed

A probe file in the clone ran `pact_signers` over 17 pact shapes and
`pact_reviews` over 8 review shapes. It then ran `pact-check` and
`chain-check` end to end.

| Shape | Pact | Review | `pact-check` | `chain-check` |
|---|---|---|---|---|
| old above, heading, new | one refusal naming `\| Signatory \|` | one refusal | exit 2 (the case) | exit unchanged, refusal as notice |
| old above, blank line, new | one refusal | one refusal | exit 2 | exit unchanged, refusal as notice |
| new, heading, old below | one refusal | one refusal | exit 2 | exit unchanged, refusal as notice |
| new, blank line, old directly below | the stray-row refusal only | the stray-row refusal only | exit 2 | not run |
| new only / old only | no refusal; header new / old | no refusal | — | old only: rename sentence, exit unchanged |
| new, plus old word in prose or inline code | no refusal | no refusal | — | — |
| new, plus old table in a fence, a comment, a commented-out block | no refusal | no refusal (fence) | — | — |

`chain-check` was run with the round record passing and failing. It
exited 0 and 1 in every shape, the same as the new header alone.

The review end to end was run with the old table below the new one and
with the old table above after a blank line. Both exit 2, and both print
a `REFUSED` line saying the record also holds the old three-column header.
The new header alone exits 0.

The fix pass's cases are each seen red against the old reader. With
`hooks/config.py` put back to d1e0b2c6's version in the clone, seven cases
fail. They are the S4 reader case, the S4 broken-table case, the
`pact-check` S4 case, the review S5 case, and the three parametrizations of
the walker case. That matches R1's note, "seven cases across four modules".

### Round 1's white 2 and white 3 are closed, as planted

The word was planted alone in nine places and the two sweep cases were
run each time.

- **Red in both cases.** The `## When there is a pact at all` heading,
  which was round 1's plant, and `read_table`'s docstring.
- **Red in the tree-wide case.** `CHANGELOG.md`,
  `templates/seal-README.md`, `README.md`, `chain_check.py`'s module
  docstring, and a comment above `RENAMED_IN` in `hooks/config.py`.
- **Green.** A `###` heading inserted after the statement (⬜ 6), and a
  lowercase comment in `tests/test_pact_check.py` (⬜ 7).

### ⬜ 5 — an old header written without spaces is named twice

`hooks/config.py:1344`.

`read_table` skips its own refusal where an existing refusal contains the
old header as `\`| Signatory |\``, spaced as the code writes it. The
walk's stray-row refusal quotes the line as the file wrote it. Take a
`Signer` table, a blank line, and `|Signatory|` directly below. The walk
reads `|Signatory|` as the old header. The file then gets two refusals for
one table, the stray-row one and the new one.

The cost is one duplicate line under exit 2, which is the exit either way.
But the docstring says "the refusal is not added where the walk's stray-row
refusal already names the old header". The S4 case's docstring says "it is
not named twice". Both are false for that spelling.

The fix compares the cells each refusal quotes, not the spelling. It was
executed in the clone. The unspaced shape, the spaced one, the heading
shape and the review shape each give one refusal. The six pact modules
passed (3447).

### ⬜ 6 — the policy span still runs past a heading below level 2

`tests/test_one_word_one_meaning.py:733`, `without_the_policy_span`.

The span stops at the first `" ## "` in the flattened text. A `###`
heading flattens to `" ### "`, which does not contain `" ## "`. So a
`### Signatory history` heading written between the statement and
`## When there is a pact at all` falls inside the exemption, and both
cases stay green. Executed.

The function's docstring and ledger row R6 both say "the next heading". It
costs nothing today, because no heading of that level sits there. It is
the class round 1's white 2 named, one level down.

The fix stops at a heading of any level. Executed: the module is green
(21), and the same `###` plant turns both cases red.

### ⬜ 7 — five compatibility modules are exempt whole

`tests/test_one_word_one_meaning.py:816`, with `RENAMED_COMPAT` at 791.

The tree-wide case skips the five compatibility modules entirely. Every
use of the word in them is the capitalised header cell, in a fixture, a
tuple or a pinned sentence. That was executed by `grep` over the five
modules. The exemption is still wider than that. A docstring or comment
there saying the word in lowercase passes. Executed: a planted
`# a signatory's checkout` in `tests/test_pact_check.py` stays green.

The sweep's own module has to stay exempt whole, because its pattern, a
retired identifier and a work item id name the word.

Read: the case's docstring says "Each exception is asserted to exist". The
assertion covers `RENAMED_COMPAT` and the two span files.
`RENAMED_RECORDS`' five prefixes are not asserted. All five exist today.

The fix sweeps the five modules for the lowercase word, and `Signatories`,
case-sensitively, and leaves the sweep's own module whole. Executed: the
module is green (21), and the planted comment turns the tree-wide case red.
The prefix assertion in the same fence was not run.

## Findings — from reading

### ⬜ 8 — two fixtures describe their shape backwards

`tests/test_a_pact_review_takes_a_pact_change.py:216` and
`tests/test_pact_check.py:268`.

The review case's docstring says "An old table above the new one holds a
row the new table does not". Both tables hold the same row. The refusal
the case asserts does not depend on that, so the case still holds. But the
sentence describes a fixture the case does not build.

The `pact-check` S4 case commits with the message "a new table above an
old one". The old table is the one above.

### ⬜ 9 — the policy's `Enforced by:` line misses the cases that hold its new clauses

`docs/the-pact.md:42`.

The statement now says that an old header beside the new one is refused,
for a pact or a pact review record. It also still says that every text
this plugin ships says `signer`. The line lists the two pact cases for the
first clause. It does not list
`tests/test_a_pact_review_takes_a_pact_change.py#test_s5_a_review_record_holding_both_headers_is_refused`,
which is the one case for the review half. For the second clause it lists
only `test_no_pact_text_names_a_signer_the_way_0_18_did`. That case reads
`pact_texts()`. The case that holds the clause over every tracked file is
`test_no_live_text_says_the_word_0_19_0_renamed`.

### ⬜ 10 — R5 and P8 carry evidence from before the fix (paperwork)

`seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:33`
(R5) and `:17` (Corrected · P8).

This is a correction to the run's paperwork. It is not counted in
`Needs a fix`.

- **R5.** The row was reworded and re-stamped to `2a846fac`. Its evidence
  still says the folded-statement case "resolved the new statement's five
  `Enforced by:` targets", in phase 1's and phase 2's slice runs. The line
  now has six targets.
- **P8.** The claim gained "a pact holding both … are refused". The row
  cites no case that holds that clause, and its evidence is the phase slice
  runs from before the fix. R1 cites the cases.

For both rows the reading is right. `evidence-check --ledger` on the
fragment reports 429 ok, 0 drifted and 0 broken, and the folded-statement
module is green in this round's slice. The evidence cells name runs from
before the claim they now support.

## What was checked and holds

- **R1 and R6.** Both say what the code does. R1's both-headers clause
  matches every shape in the table above. R6's "from its fold marker to the
  next heading or marker" is true for `##` (see ⬜ 6). Its list of records
  and six modules matches `RENAMED_RECORDS` and `RENAMED_COMPAT`. Its
  evidence names the red plants the fix pass ran, and this round
  reproduced them.
- **The overview.** The S4 row and the new function row in `overview.md`
  are accurate (round 1's white 4).
- **The changelog fragment.** It says `pact-check` exits 2 and
  `chain-check` prints a notice. Both were executed.
- **The renamed S4 case.** `git grep` finds the name it replaced nowhere
  outside the round records.
- **Shapes left unrefused, judged right.** An old table in a block quote,
  and a lowercase `| signatory |` table, beside a `Signer` table are not
  refused. The walker reads no table in a block quote under either header.
  A lowercase header was never a header 0.18.x read, so neither holds rows
  that were ever signers.

## Regression tests to plant

- `tests/test_a_signer_declares_its_pact.py`, in the S4 case: the
  unspaced old header directly below, asserting one refusal (⬜ 5, fence
  below). The reader probe gives two refusals before the fix and one
  after, so it is red against today's code.
- The two sweep plants (⬜ 6, ⬜ 7) are mutations, not cases. Run them
  through `bin/mutation-check` if the fixes land.

## Facts for the evidence ledger

- If ⬜ 5 lands, `hooks/config.py#read_table`'s hash moves, and R1 and P8
  are re-read against it. Their claims are unchanged.
- If ⬜ 6 or ⬜ 7 lands, R6's claim gains "the next heading of any level"
  and the lowercase sweep of the five modules.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking-class finding is closed — a pact or pact review record holding both headers refuses the old one in every shape round 1 named, and no one-header or prose text is refused | `hooks/config.py:1326` | confirmed | executed: 17 pact and 8 review shapes through the reader; `pact-check` exit 2 on old-above-blank, new-heading-old and new-blank-old, review exit 2 on two shapes; `chain-check` exit 0/1 unchanged on three shapes; seven fix-pass cases red against d1e0b2c6's reader |
| 🟢 | round 1's white 2 is closed — the policy span ends at the next `##` heading | `tests/test_one_word_one_meaning.py:733` | confirmed | executed: the old word planted in `## When there is a pact at all` turns both sweep cases red; the class's remainder is ⬜ 6 |
| 🟢 | round 1's white 3 is closed — every tracked live file is swept | `tests/test_one_word_one_meaning.py:801` | confirmed | executed: plants in `CHANGELOG.md`, `templates/seal-README.md`, `README.md`, `chain_check.py`'s docstring, `read_table`'s docstring and above `RENAMED_IN` each turn the tree-wide case red |
| 🟢 | round 1's white 4 is closed — the overview's S4 row names every two-table shape and the function is a recorded divergence | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | confirmed | read against the reader probe's table |
| ⬜ 5 | An old header written without spaces directly below the `Signer` table is named twice, against `read_table`'s docstring and the S4 case's | `hooks/config.py:1344` | open | executed: two refusals before the fix, one after; 3447 passed with the fix |
| ⬜ 6 | The policy span stops at `##` only, so a `###` heading after the statement is exempt | `tests/test_one_word_one_meaning.py:733` | open | executed: a `### Signatory history` plant leaves both cases green; the fix turns both red and keeps the module green |
| ⬜ 7 | Five compatibility modules are exempt whole, though every use they need is the capitalised header cell; "each exception is asserted to exist" skips the record prefixes | `tests/test_one_word_one_meaning.py:816` | open | executed: a lowercase comment in `tests/test_pact_check.py` stays green; the fix turns it red and keeps the module green |
| ⬜ 8 | The review case's docstring says the old table holds a row the new one does not, and both hold the same row; the `pact-check` S4 commit message reverses which table is above | `tests/test_a_pact_review_takes_a_pact_change.py:216` | open | read |
| ⬜ 9 | The policy's `Enforced by:` line omits the review both-headers case and the tree-wide sweep, the cases that hold two of its clauses | `docs/the-pact.md:42` | open | read |
| ⬜ 10 | R5's evidence counts five `Enforced by:` targets where there are six, and P8's new clause cites no case that holds it | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:33` | open | paperwork correction; not counted in Needs a fix; `evidence-check --ledger` on the fragment 429 ok |
| ❓ | The full suite, lint and typecheck, and S12's `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` | the tree at ec797405 | ❓ out of verified scope | steps of the broad gate, which is the sealer's; the sealer answers it now that this round leaves nothing needing a fix |

## Executed probes

| What was run | Result |
|---|---|
| eight modules in a `git clone --no-local` at ec797405: the six pact modules, `test_a_folded_statement_names_what_enforces_it`, `test_docs_line_wrap` | exit 0, 3514 passed |
| `pact_signers` over 17 pact shapes and `pact_reviews` over 8 review shapes | see the table under round 1's yellow 1 |
| `pact-check` end to end: old above after a blank line, old below under a heading, old directly below | exit 2 in all three, the refusal line printed, no rename line |
| `pact-check` end to end on a review record: new above with old below under a heading, old above after a blank line, new only | exit 2, exit 2, exit 0 |
| `chain-check` over new only, old above under a heading, old above after a blank line, old below under a heading, old only, with the round record passing and failing | exit 0 passing and 1 failing in every shape; the refusal as a notice on the three two-table shapes; the rename sentence on old only |
| the seven fix-pass cases with `hooks/config.py` at d1e0b2c6 | exit 1, 7 failed |
| the two sweep cases with the old word planted in nine places, one at a time | red for seven; green for a `###` heading after the statement and a lowercase comment in a compatibility module |
| ⬜ 6's fix applied, the module, then the `###` plant | 21 passed; then both cases red |
| ⬜ 7's fix applied, the module, then the lowercase plant | 21 passed; then the tree-wide case red |
| ⬜ 5's fix applied, the reader on four shapes, then the six pact modules | one refusal each; exit 0, 3447 passed |
| `bin/evidence-check --ledger seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md .` | exit 0; `total: 429 ok · 0 drifted · 0 broken` |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's broad gate, now due |
| `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` (S12) | not yet — steps of the broad gate, the sealer's |

### ⬜ 5 — the reader on the unspaced shape, before the fix

```
PACT N new, blank, old unspaced: signers=['orders-web'] header=('Signer',) refusals=['has a `Signer` table that ends above `|Signatory|`, a row the walk never reaches — it and every signer below it would go unread', 'also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it']
```

### Round 1's yellow 1 — `pact-check` on old above after a blank line

```
REFUSED seal/pact.md — the pact also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it
pact-check: the pact `orders-api` — 1 of 1 signer read · 1 ok · 0 superseded · 0 not taken · 0 unmatched · 0 broken · 0 pact changes read · 0 taken
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### ⬜ 5 — `hooks/config.py#read_table`, the skip

```python
        if holds_old and not any(
            table_cells(quoted) == old
            for r in refusals
            for quoted in re.findall(r"`([^`]*)`", r)
        ):
```

### ⬜ 5 — `tests/test_a_signer_declares_its_pact.py`, appended to the S4 case

```python
    # Written without its spaces, the old header is quoted as written by the
    # stray-row refusal, and is still named once.
    _, refusals, _ = config.pact_signers(
        signer + "\n|Signatory|\n|---|\n|https://example.com/org/billing|\n"
    )
    assert len(refusals) == 1 and "ends above `|Signatory|`" in refusals[0], refusals
```

### ⬜ 6 — `tests/test_one_word_one_meaning.py#without_the_policy_span`

```python
    heading = re.search(r" #{1,6} ", rest)
    stops = [
        i
        for i in (rest.find("<" + "!--"), heading.start() if heading else -1)
        if i != -1
    ]
```

### ⬜ 7 — `tests/test_one_word_one_meaning.py`, the tree-wide case

```python
# The compatibility cases need the old word only as the header cell, which is
# capitalised; their prose is swept for it in lower case.
PACT_HEADER_WORD = re.compile(r"signator(?:y|ies)|Signatories")
```

```python
    for prefix in RENAMED_RECORDS:
        assert any(p.startswith(prefix) for p in tracked), (
            f"{prefix} is excepted below and holds no tracked file"
        )
    said = []
    for rel in tracked:
        if rel.startswith(RENAMED_RECORDS) or rel == "tests/test_one_word_one_meaning.py":
            continue
```

```python
        pattern = PACT_HEADER_WORD if rel in RENAMED_COMPAT else PACT_RENAMED
        said.extend(f"{rel}: {m.group(0)}" for m in pattern.finditer(text))
```

### ⬜ 8 — the review case's docstring and the S4 commit message

```python
    """Round 1's yellow 1, for a pact review record. An old table above the
    new one is never read while the new one stands; read silently, a row
    only it held would be dropped and the record it took would read `NOT
    TAKEN` again with nothing saying why. It is refused at exit 2 instead."""
```

```python
    commit(world["api"], "an old table above a new one")
```

### ⬜ 9 — `docs/the-pact.md`, appended to the statement's `Enforced by:` line

```
, tests/test_a_pact_review_takes_a_pact_change.py::test_s5_a_review_record_holding_both_headers_is_refused, tests/test_one_word_one_meaning.py::test_no_live_text_says_the_word_0_19_0_renamed
```

Needs a fix: no

Loses a record or crashes: no

The broad gate is now due. This round leaves nothing needing a fix, so
what comes due is the sealer's spawn.

## Proof block

Files opened this round, at ec797405 in the clone or in the checkout
(read-only):
`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/rounds/round-1.md`,
`rounds/round-1-report.md`, the fix-range diff of `overview.md` and
`changelog.md`; `hooks/config.py` (`gfm_table` to `renamed_header`);
`skills/code-review/scripts/chain_check.py` (the pact notice, 4075-4105);
`skills/evidence-check/scripts/pact_check.py` (530-560, 715-745);
`tests/test_one_word_one_meaning.py` (`flat`, `pact_texts`, the fix-range
diff); `tests/test_pact_check.py`, `tests/test_a_pact_review_takes_a_pact_change.py`,
`tests/test_a_signers_ci_prints_its_pact.py` (helpers and the new cases);
`tests/test_a_signer_declares_its_pact.py`,
`tests/test_one_table_walker_reads_what_gfm_renders.py` (the fix-range
diff); `tests/test_docs_line_wrap.py` (`LIMIT`, `COVERED`);
`docs/the-pact.md` (§*The words*, lines 20-48);
`seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md`
(rows R1, P8, R5, R6, and the fix-range diff); `CHANGELOG.md` (head);
`bin/test`. The probe file, the plant scripts and the clone were deleted
before handover.
