# Round 1 report — 1791239490-a-repository-that-keeps-a-pact-is-a-signer

| Field | Value |
|---|---|
| Target SHA | 91aeafac |
| Base | `origin/release/v0.19.0` at e6d5a055 (the 0.18.3 release) |
| Pull request | #827 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

The rename holds where the spec asked for it. A pact or a pact review record
headed the 0.18.x way reads exactly as one headed `Signer`. `pact-check`
prints one rename line per such file and its exit does not move.
`chain-check` counts `signers`, appends the rename sentence on the old
header, and keeps its exit. A broken `| Signer |` table is refused and never
covered by an old one. The ledger fragment carries every coordinate the
released rows rest on, and no released file moved.

One defect, from the two-header reader (🟡 1). A file that holds both
headers is read from the `Signer` table alone, and the old table's rows go
unread with no refusal in two of the three shapes. One of those shapes, the
old table above the new, was outside the spec's S4 and is pinned silent by
two cases. In a pact that is a signer nobody reads at exit 0, which is the
failure the table walker was built to end.

Three ⬜ follow it. The sweep's policy exclusion runs one heading past the
statement it exempts. The sweep reaches fewer texts than the rename touched,
so S11 has no standing check. The overview's S4 row omits the silent shapes.

HEAD of the checkout stayed at 91aeafac for the whole round.

## What this round was asked

Spec compliance against `spec.md`, then quality: every path that reads a
pact's or a pact review's table, attacked with both headers, neither, both
at once and a broken new one; the printed lines and exit codes of
`pact-check` and `chain-check`; the sweep's exemptions as a way back for the
old word; the ledger fragment's 28 `Corrected ·` and 39 `Re-read ·` rows
against the claims they re-point; the overview's divergences. The prompt
says four divergences. `overview.md` has five rows, and all five were read.

## Enumeration: every reader of the two tables

Read at 91aeafac. `git grep` for `pact_signers(`, `pact_reviews(`,
`gfm_table(` and `read_table(` outside `tests/` finds two headers read
through one function, `hooks/config.py#read_table`, and three call sites:

| Reader | Table | Call site |
|---|---|---|
| `pact-check`, the pact | `\| Signer \|`, else the old one | `skills/evidence-check/scripts/pact_check.py:540` |
| `pact-check`, each pact review record | `\| Signer \| Change \| Verdict \|`, else the old one | `skills/evidence-check/scripts/pact_check.py:728` |
| `chain-check` at the pact's repository | `\| Signer \|`, else the old one | `skills/code-review/scripts/chain_check.py:4085` |

No other script reads either table or writes either header.
`evidence_check.py` reads only the pact-changes record, whose header never
carried the word. `templates/pact-review.md` is the one writer of the review
header, and it begins `| Signer | Change | Verdict |`.

## Findings — from execution

### 🟡 1 — a file holding both headers drops the old table's rows with no refusal

`hooks/config.py:1326` (`read_table`), pinned silent by
`tests/test_a_signer_declares_its_pact.py:1209` and
`tests/test_one_table_walker_reads_what_gfm_renders.py:593`.

`read_table` reads the `Signer` table whenever one stands and never looks
at the old header again. What happens to an old table in the same file
depends only on where it sits:

| Shape | Read | Refused |
|---|---|---|
| `Signer` above, blank line, old table below | the `Signer` rows | yes, the old header is a stray row |
| `Signer` above, heading, old table below | the `Signer` rows | **no** |
| old table above, heading, `Signer` below | the `Signer` rows | **no** |
| old table above, blank line, `Signer` below | the `Signer` rows | **no** |

The spec's S4 covers only "below". The S4 case's first two shapes and the
walker case's `both` text assert `refusals == []` for the "above" shape and
the "below, under a heading" shape. So the drop is pinned rather than
missed.

**Why it matters.** The old table holds real signers. Executed through
`pact-check` end to end: the pact lists `orders-web` (which has a checkout
and a current citation) and `orders-mobile` under `| Signatory |`, then a
heading, then `| Signer |` listing only `orders-tablet`. The run prints
`0 of 1 signer read` and never mentions `orders-web` or `orders-mobile`. It
exits 1 only because `orders-tablet` has no checkout. Give that one a
checkout and the run exits 0 with two signers nobody read. `chain-check` on
the same shape says `which lists 1 signer`, with no notice and no rename
sentence. A pact review record in the same shape drops the old table's
rows. A record a review took then reads `NOT TAKEN` again, with nothing
saying why.

**Who reaches the shape.** A person adding a signer to a 0.18.x pact who
starts the new row from `templates/pact.md`, or a person who renames the
header by writing a new table and has not yet removed the old one. The
rename line tells every 0.18.x user to edit that very table.

The reader's own docstrings set the bar this misses. Above the `gfm_table`
cases: "none drops a signer while the table reads as complete". In
`pact_signers`: "no signer is dropped while the table reads as complete".
The one shape the walk already refuses, the old table directly below with
no heading, exits 2. The other three exit as if the file held one table.

**The fix.** Where the new header reads and the old header is also in the
file, add one refusal naming the old header. Skip it where the walk's
stray-row refusal already names that header. Executed in the clone with the
fix applied: the three silent shapes each return the one new refusal, the
stray-row shape keeps its existing single refusal, and both single-header
shapes are unchanged. Over the six pact modules, 3440 passed and 4 failed:
the S4 case and the walker case's three parametrizations. Each of those
asserts the silent drop. The fence below gives their new expectations, the
policy sentence and the changelog sentence.

This keeps the owner's decision whole. The rename is still a printed line,
and a file with one header under either word is never refused. What becomes
a refusal is a file with two tables, which no rename produces.

## Findings — from reading, and from planting the word

### ⬜ 2 — the policy span the sweep exempts runs into the next section's heading

`tests/test_one_word_one_meaning.py:736`.

`PACT_RENAMED_SPANS` exempts the policy statement "from its fold marker to
the next marker". The code cuts at the next `&lt;!--`. In
`docs/the-pact.md` the statement is the last one in §*The words*, so the
next opener comes after the `## When there is a pact at all` heading. The
exemption covers that heading too. Executed: the heading rewritten to
`## When a signatory has a pact at all` leaves the case green. It costs
nothing today, but an exemption should end where the statement it names
ends. A fence below cuts at the next heading or the next opener, whichever
comes first.

### ⬜ 3 — the sweep reaches only `pact_texts()`, so S11 holds once and then nowhere

`tests/test_one_word_one_meaning.py:722`.

S11's property, that no live text keeps the word, was established by one
`git grep` pasted into `phases/phase-2.md`. The standing check is
`test_no_pact_text_names_a_signer_the_way_0_18_did`. It sweeps only
`pact_texts()`: three whole files, five sections, the pact lines of three
files, and the string constants of named units. Spec item 1 renamed the
word in files that set does not include. Executed, each planted alone, each
green:

- `templates/seal-README.md` (and so `seal/README.md`, which mirrors it)
- `docs/one-root-by-lifetime.md`
- a comment in `skills/evidence-check/scripts/pact_check.py`
- the module docstring of `skills/code-review/scripts/chain_check.py`,
  which is outside `pact_notices`
- the docstring of `hooks/config.py#read_table`, which `PACT_PRINTED` does
  not name

The same word as a string constant of `pact_check.py` turns the case red,
so the case does work inside its set. This matches spec item 8 as written,
which is why it is ⬜. The spec's own grounding row says "the check, not the
rule, is the repair", and the check covers a subset. A case that runs S11's
`git grep` and allows its listed hits would hold every live text.

### ⬜ 4 — the overview's S4 row describes two of the silent shapes as decided and omits one

`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18`.
A correction to the run's paperwork. It is not counted in `Needs a fix`.

The row reads "read from `Signer` alone where a heading stands between;
directly below with no heading, the old rows are refused". It does not
mention the old table above the new one with only a blank line between,
which is also read silently. It also does not say that the "above" shapes
sit outside spec S4. Separately, spec §*Data & interfaces* asks for "the old
tuple and the rename sentence as module constants". The code builds both in
a function, `renamed_header`, and only `RENAMED_IN` is a module constant.
The sweep excludes the function by name, so nothing breaks, but no row
records the change. If 🟡 1's fix lands, the S4 row is rewritten anyway.

## What was checked and holds

- **The compatibility reader.** Executed over 14 pact shapes and 5 review
  shapes. Old header only: read, with the old header returned. Neither:
  refused, naming `Signer`. A `Signer` header with no delimiter row, or
  directly under a line, with a valid old table elsewhere: refused as it
  stands, with no fallback. A `Signer` table inside a fence: the old table
  is read, which is right, because a fenced header is no table. Lowercase
  headers and a two-column old header: refused, as 0.18.x refused them.
- **The rename line and exits.** `renamed` writes through `say` and never
  through `found`, so no exit class sees it (read,
  `skills/evidence-check/scripts/pact_check.py:692-700`). The S2 and S5
  cases assert that the exit and the remaining output equal the new
  header's (executed in the slice).
- **`chain-check`.** Executed in four shapes. With the old header the
  notice ends with the rename sentence. Neither header, and a broken new
  header, print the refusal as a notice. All four exit 0, with no pull
  request failure.
- **The ledger fragment.** Executed: 28 `Corrected ·`, 39 `Re-read ·` and
  7 new rows. A script compared each `Corrected ·` row's coordinates with
  the released row it cites, with the old word mapped to the new: every
  released coordinate is carried. P7 and P11 add one case each. P8, whose
  label the script could not parse, was compared by hand: all 11
  coordinates of 0.18.1's corrected P8 are carried, and `read_table` and
  `renamed_header` are added. C1 cites 0.18.2's `Corrected · C1` rather than
  0.18.1's row, which continues the chain that file already began. Every
  released row whose coordinates hold the old word belongs to one of the 28
  families. `evidence-check --ledger` over the fragment alone reports 423
  ok, 0 drifted, 0 broken, and 0 refused names in the work item's prose.
  `git diff --stat` over `seal/ledger.md`, `seal/releases` and `changelog`
  is empty.
- **S11 today.** Executed: outside the records, the old word is in the
  `renamed_header` unit, the excluded policy statement, eight fold markers
  naming `1790993137-a-signatory-…`, the compatibility cases in five test
  modules (overview divergence 5), two comments in the sweep's own module,
  and this work item's ledger fragment, which quotes released claims.
- **Overview divergences 2, 3 and 5.** Read and confirmed against the code.
  `PACT_LOOSE` is unchanged, `PACT_RENAMED` is its own constant, and the
  compatibility cases spell the old header literally.
- **The changelog fragment.** Read. It sits under `### Changed` with no
  line starting `## `. `README.ko.md` keeps `signer(그 계약에 서명한 저장소)`.

## Regression tests to plant

- `tests/test_a_signer_declares_its_pact.py`: the S4 case's two silent
  shapes, plus the old table above the new one with only a blank line
  between, each asserting the one new refusal (fence 🟡 1).
- `tests/test_one_table_walker_reads_what_gfm_renders.py`: the `both` text
  in `test_the_old_header_is_read_through_the_second_attempt` asserts the
  refusal and still reads only the `Signer` rows.
- `tests/test_pact_check.py`: one end-to-end case with the old table above,
  a heading, then `| Signer |`, asserting exit 2 and the refusal line.
- `tests/test_a_pact_review_takes_a_pact_change.py`: a review record
  holding both headers is refused at exit 2.

## Facts for the evidence ledger

- R1's claim gains a clause once 🟡 1 lands: a text holding the new header
  and the old one is refused, naming the old one. Its coordinates are
  unchanged, but `hooks/config.py#read_table`'s hash moves.
- The ledger fragment's P8 claim, "a pact holding neither table … are
  refused", gains the same clause.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A file holding both headers is read from the `Signer` table, and the old table's rows go unread with no refusal where it stands above the new one, or below it under a heading; two cases pin that silence | `hooks/config.py:1326` | open | executed: `pact-check` read 0 of 1 signer with two old-table signers never named, and `chain-check` said "lists 1 signer"; the fix flips exactly the four cases that pin the drop |
| ⬜ 2 | The sweep's policy exemption runs past the statement into the next section's heading | `tests/test_one_word_one_meaning.py:736` | open | executed: the old word planted in `## When there is a pact at all` leaves the case green |
| ⬜ 3 | The sweep reaches only `pact_texts()`, so S11's property has no standing check over the other files spec item 1 renamed | `tests/test_one_word_one_meaning.py:722` | open | executed: five plants outside the set stay green, and one inside turns it red; spec item 8 scopes the sweep this way |
| ⬜ 4 | The overview's S4 row omits one silent shape and does not say the "above" shapes are outside S4; the spec's "module constants" became a function with no divergence row | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | open | paperwork correction; not counted in Needs a fix |
| 🟢 | A pact and a pact review record headed the 0.18.x way read as the new header does, with one rename line each and no exit change | `hooks/config.py:1326`, `skills/evidence-check/scripts/pact_check.py:692` | confirmed | executed: reader probe and the S2/S5 cases in the slice |
| 🟢 | A broken `\| Signer \|` table is refused and not covered by the old one | `hooks/config.py:1333` | confirmed | executed: no delimiter row and a line directly above both refuse with the header read as `Signer` |
| 🟢 | `chain-check` counts signers, carries the rename sentence on the old header, and its exit does not move | `skills/code-review/scripts/chain_check.py:4085` | confirmed | executed: four shapes, all exit 0 |
| 🟢 | Every `Corrected ·` row carries every coordinate its released row rests on, and the released files are byte-identical to the base | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md` | confirmed | executed: coordinate comparison script, `evidence-check --ledger` on the fragment (423 ok), empty `git diff --stat` |
| ❓ | S12's `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD`, and the full suite, lint and typecheck | the tree at 91aeafac | ❓ out of verified scope | both commands are steps of the broad gate (`skills/verify/scripts/broad_gate.py`), which is the sealer's; the sealer answers it once the rounds settle |

## Executed probes

| What was run | Result |
|---|---|
| `pact_signers` and `pact_reviews` over 14 pact and 5 review shapes, in a `git clone --no-local` at 91aeafac | see 🟡 1's table; every single-header and neither shape behaves as the spec says |
| `pact-check` end to end: old table (orders-web, orders-mobile), heading, `\| Signer \|` (orders-tablet) | exit 1, `0 of 1 signer read`, the two old-table signers never named |
| `chain-check` over the old header, both (old above), neither, broken new + old | exit 0 in all four; the rename sentence only on the old header; "lists 1 signer" on both |
| the sweep case with the old word planted in eight places, one at a time | red only for a string constant of `pact_check.py`; green for the seven outside the swept set or inside the policy span |
| a script comparing each `Corrected ·` row's coordinates with its released row | 27 of 28 parsed, every released coordinate carried; P8 compared by hand |
| `evidence_check.py --ledger seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md .` | exit 0; `total: 423 ok · 0 drifted · 0 broken` |
| `git diff --stat e6d5a055...HEAD -- seal/ledger.md seal/releases changelog` | empty |
| six pact modules: `test_one_word_one_meaning`, `test_a_folded_statement_names_what_enforces_it`, `test_pact_check`, `test_a_signer_declares_its_pact`, `test_a_pact_review_takes_a_pact_change`, `test_a_signers_ci_prints_its_pact` | exit 0, 2797 passed |
| 🟡 1's fix applied in the clone, then the pact modules with the walker module | exit 1, 3440 passed, 4 failed: the S4 case and the walker case's three parametrizations, each asserting the silent drop |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |
| `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` (S12) | not yet — steps of the broad gate, the sealer's |

### 🟡 1 — `pact-check` on a pact holding both tables

```
NOT FOUND https://example.com/org/orders-tablet — no checkout of it was found on this machine: add `| https://example.com/org/orders-tablet | <the path of its checkout> |` to ~/.claude/specseal/pact-paths.md
pact-check: the pact `orders-api` — 0 of 1 signer read · 0 ok · 0 superseded · 0 not taken · 0 unmatched · 0 broken · 0 pact changes read · 0 taken
```

### 🟡 1 — the fix applied, `pact_signers` per shape

```
old above, heading, new below -> (['also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it'], ('Signer',))
old above, blank, new below   -> (same refusal, ('Signer',))
new above, heading, old below -> (same refusal, ('Signer',))
new above, blank, old below   -> (['has a `Signer` table that ends above `| Signatory |`, a row the walk never reaches — it and every signer below it would go unread'], ('Signer',))
signer only                   -> ([], ('Signer',))
signatory only                -> ([], ('Signatory',))
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 — `hooks/config.py#read_table`

```python
def read_table(text, header):
    """(rows, refusals, header read) for the table of TEXT headed HEADER,
    or, where TEXT holds none, headed as HEADER was written before 0.19.0
    (`renamed_header`). A text holding a HEADER table is read from it alone,
    and an old header it also holds is refused: the rows under it would
    otherwise go unread at exit 0, wherever that table stands. Where neither
    is there, the refusal names HEADER and the header read is None, so a
    caller tells the old header from the new one without reading the text
    again (#822)."""
    rows, refusals = gfm_table(text, header)
    old = renamed_header(header)[0]
    old_rows, old_refusals = gfm_table(text, old) if old else ([], [])
    holds_old = old is not None and not (
        old_refusals and old_refusals[0].startswith("holds no ")
    )
    if not (refusals and refusals[0].startswith("holds no ")):
        if holds_old and not any(f"`| {' | '.join(old)} |`" in r for r in refusals):
            refusals = refusals + [
                f"also holds a `| {' | '.join(old)} |` header, the word before "
                f"{RENAMED_IN}, and nothing under it is read while the "
                f"`| {' | '.join(header)} |` table stands — move its rows into "
                "that table and delete it"
            ]
        return rows, refusals, header
    if holds_old:
        return old_rows, old_refusals, old
    return rows, refusals, None
```

### 🟡 1 — `tests/test_a_signer_declares_its_pact.py`, the S4 case

```python
BOTH = (
    "also holds a `| Signatory |` header, the word before 0.19.0, and nothing "
    "under it is read while the `| Signer |` table stands — move its rows into "
    "that table and delete it"
)


def test_s4_a_pact_holding_both_tables_reads_signer_and_refuses_the_old_one():
    """S4 of #822. A `| Signer |` table is read alone, and an old table
    anywhere else in the file is refused rather than left unread: above it,
    below it under a heading, or above it with only a blank line between.
    Directly below with no heading, the walk's stray-row refusal already
    names it."""
    signer = "# Pact\n\n| Signer |\n|---|\n| https://example.com/org/orders-web |\n"
    old = "| Signatory |\n|---|\n| https://example.com/org/billing |\n"
    for text in (
        signer + "\n## Before\n\n" + old + "\n## A\n\nx\n",
        f"# Pact\n\n{old}\n## Now\n\n" + signer.split("\n\n", 1)[1],
        f"# Pact\n\n{old}\n" + signer.split("\n\n", 1)[1],
    ):
        signers, refusals, header = config.pact_signers(text)
        assert [s[2] for s in signers] == ["orders-web"], (text, signers)
        assert refusals == [BOTH] and header == ("Signer",), (text, refusals)
    _, refusals, header = config.pact_signers(signer + "\n" + old)
    assert header == ("Signer",)
    assert refusals == [
        "has a `Signer` table that ends above `| Signatory |`, a row the walk "
        "never reaches — it and every signer below it would go unread"
    ], refusals
```

### 🟡 1 — `tests/test_one_table_walker_reads_what_gfm_renders.py`, the `both` text

```python
    signers, refusals, header = config.pact_signers(both)
    assert header == ("Signer",), (both, header)
    assert [s[0] for s in signers] == [v], (both, signers)
    assert len(refusals) == 1 and "also holds a `| Signatory |` header" in refusals[0], (
        both,
        refusals,
    )
```

### 🟡 1 — `docs/the-pact.md`, the statement under this work item's marker, and the changelog fragment

```
A file holding no table under the new header is read under the old one
exactly as it would be under the new; a file holding one is read from it
alone, and an old header beside it is refused, because its rows would
otherwise go unread.
```

### ⬜ 2 — `tests/test_one_word_one_meaning.py`, the end of the excluded span

```python
            head, marker, rest = text.partition(span)
            assert marker, f"{where}: the excluded span `{span}` is gone"
            # The statement ends at the next heading or the next fold marker,
            # whichever comes first; `flat` has put both on one line.
            stops = [i for i in (rest.find("<" + "!--"), rest.find(" ## ")) if i != -1]
            assert stops, (
                f"{where}: the excluded span is the last statement in the file, "
                "so this exclusion now removes everything after it"
            )
            text = head + rest[min(stops) :]
```

Needs a fix: yes — 🟡 1, a pact or pact review record holding both headers drops the old table's rows with no refusal

Loses a record or crashes: no

## Proof block

Files opened this round, at 91aeafac in the clone:
`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/spec.md`,
`overview.md`, `routing.md`, `changelog.md`, `phases/phase-2.md` (to line
60), `plan.md` (by `grep`); `hooks/config.py` (the diff, `table_cells`,
`gfm_table` to `_stops_at`, `read_table`, `pact_signers`, `pact_reviews`,
`renamed_header`); `skills/evidence-check/scripts/pact_check.py` (the diff,
`check` to its exit); `skills/code-review/scripts/chain_check.py` (the diff,
`PACT_NOT_HERE`); `skills/evidence-check/scripts/evidence_check.py` (the
diff, usage); `tests/test_one_word_one_meaning.py` (the diff, `flat`,
`pact_texts`, the pact lists); `tests/test_pact_check.py` (helpers, S1, S2,
S7); `tests/test_a_pact_review_takes_a_pact_change.py` (the diff);
`tests/test_a_signers_ci_prints_its_pact.py` (helpers, the pact cases);
`tests/test_a_signer_declares_its_pact.py` (the S4 cases);
`tests/test_one_table_walker_reads_what_gfm_renders.py` (the diff, the
old-header case); `docs/the-pact.md` (§*The words* through §*How a signer
names the pact*, and the word diff); `templates/pact.md`,
`templates/pact-review.md`; `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md`
and the released rows it cites in `seal/releases/0.18.0.md` to `0.18.3.md`;
`bin/test`; `skills/verify/scripts/broad_gate.py` (its step list).
