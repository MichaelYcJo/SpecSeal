# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — round 7 report

Target SHA `b5d2906b3445c95d038b82056c2a3934c84a6ce6`, the tip of
`fix/489-settle-reads-a-marker-inside-a-commented-out-draft`, base
`origin/release/v0.13.0` at `3cdfd8ad`, draft pull request 490. Fix range
`133fdfd5cbfa3ec7aef73452ccff2e34b6e46aa8..c57e5b2a`, two commits. Reviewed in
a `git clone --no-local` at that SHA; nothing was written in the working tree
but this file, and every probe was deleted before this was handed over.

## What this round was asked, and what it opened

The verifying round that closes round 6's `Fixes checked by: nobody`. Its
target is the diff of round 6's fixes rather than the branch: the fence bound
in the reader and in the oracle, the paragraph reader's stops, the docstring,
the corpus floor case, and the orchestrator's two `spec.md` lines.

**Round 6's five fixes are sound, and its figures reproduce.** I re-derived
the mutation mapping rather than reading it, and every claim round 6's fix
pass made about what its fixes buy held when I measured it — including the
one that is easiest to state and hardest to check, that bounding `FENCE_RE`
moves nothing in this repository.

It opened one thing. The indentation bound round 6 argued for went into the
oracle and into the fence, and did not go into the rest of the paragraph
reader — so the reader still stops at block starts markdown does not stop at,
and on one of them the reader and the oracle now answer differently.

**Do I believe this reader is done?** Not yet, and the reason is not the
finding below — that one is free to fix and moves no line in this tree. It is
that the answer to *where does a block end* is still a list of shapes rather
than a model, and round 6 grew that list by four entries after five rounds had
already called it settled. The design's real defence is the AND between the
two readings, and I could not break that from any side: on the four shapes I
built to try it, the disagreement parked the line. What is fragile is not the
AND, it is everything the list still does not say — and the only thing that
watches the list is an oracle carrying the same list. My evidence for saying
*not yet* is that this round found a fifth entry the list gets wrong, by the
same method the last round used, at the same cost.

## The findings, in causal order

### 1. The indentation bound went into the oracle and not into the reader, so the two now disagree about an indented heading

`skills/verify/scripts/unverified_check.py:342` — `_paragraph_ends_at`, the
ATX branch — against `tests/test_unverified_rows_close.py:1601`, the oracle's
`block_ends_at`.

The oracle's branch was bounded in `44c4dded`:

```python
        if indent <= 3 and s.startswith("#"):
```

The reader's was not:

```python
    if s.startswith("#"):
        n = len(s) - len(s.lstrip("#"))
        if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
            return True
```

CommonMark 4.2 bounds an ATX heading to three spaces of indentation; at four
it is an indented code block, or, with a paragraph open, a lazy continuation
line. So the reader stops where the format does not — the over-stop round 6's
own finding 4 is about, and the direction its docstring names as the one that
goes live.

**Measured, in a clone at this SHA.** The reader and the oracle disagree on
1,749 lines of this repository's 1,461 `.md` files, every one of them a
four-space-indented `#` comment inside a quoted Python block. Whole-document
liveness does not move on any of them, because they sit inside fences. But
the disagreement is reachable outside a fence, and then it is the violation
the safety case exists to forbid:

```
a ` b
    # x
<!-- specs/quoted -->
c ` d
```

`live_lines` reads all four lines live. The oracle parks the last three — its
block does not end at line 2, so the run on line 1 pairs with the run on line
4 and the marker is inside a code span. *The scan calls a line live that the
format parks* is exactly what
`test_the_scan_never_reads_live_what_the_format_parks` asserts can never
happen, and this document is legal markdown.

The case stays green only because its generator does not reach the shape at
this seed: a leading four-space run before a `#` token needs four consecutive
`" "` tokens, and 2,000 documents do not produce one. Nothing pins the
oracle's side either — removing the oracle's `indent <= 3` leaves the two
modules at 192 passed, exit 0, because it makes the oracle agree with the
reader and agreement is what the case cannot report.

**The same class, one level wider.** The bound is missing from four more
stops, in the reader and in the oracle alike, so the case is blind to those
rather than merely lucky: a thematic break, a bullet, an ordered marker and a
setext underline all stop at any indentation.

| line | reader | oracle | CommonMark |
|---|---|---|---|
| `    ***` | stops | stops | indented code block — no stop |
| `    - item` | stops | stops | lazy continuation — no stop |
| `    1. item` | stops | stops | lazy continuation — no stop |
| `        ===` | stops | stops | lazy continuation — no stop |

That is round 5's finding 2 and round 6's finding 2 arriving a third time: a
rule the oracle takes from the reader cannot be reported by the case built on
it. And it contradicts the sentence `44c4dded` put into the oracle's own
docstring — *each rule is the format's rule and no other*.

**The fix is free.** Bounding the reader's ATX stop alone, or bounding every
stop below the table row in both readings, each leaves the two modules at 192
passed, exit 0, and each moves 0 lines of liveness across all 1,461 `.md`
files. The paste-ready fix below is the wider one, because §12 asks for the
class rather than the coordinate.

### 2. The generator comment claims more for the lone-token branch than it buys

`tests/test_unverified_rows_close.py:1757` —
`documents_with_several_spans_on_a_line`.

The comment says a lone token is what lets the case see *a setext underline
and an indented delimiter*. Measured by removing one generator change at a
time and reverting each paragraph correction against it:

| generator | revert `FENCE_RE` | revert ATX | revert ordered | revert setext |
|---|---|---|---|---|
| as shipped | 2 red | red | red | red |
| without the lone-token branch | 2 red | red | red | **green** |
| without the five new tokens | 1 red | **green** | **green** | **green** |

The lone-token branch carries the setext revert and nothing else. The
indented delimiter is carried by the `"    ```"` token, which reaches the fuzz
joined with a space token, and by the hand-written row — which is the one
that stays red in every column. The sentence overstates a measurement that
was taken; it does not overstate the fix.

### 3. The corpus floor's failure message reports a number the assertion is not about

`tests/test_unverified_rows_close.py:1899`.

```python
    assert len({line for _, line, _ in occurrences}) >= 80, len(occurrences)
```

The assertion is about unique ids and the message prints the occurrence count,
so a failure of the unique-id floor prints `94` for a set whose size was 83 or
lower. One token.

### 4. The constant's comment says the same thing twice

`skills/verify/scripts/unverified_check.py:113` and `:126` — *`blank_fences`
keeps its own copy of the fence pattern because it serves the other gates and
this scan may not move it*, then *`blank_fences` keeps the old spelling
because it serves the other gates and this scan may not move it*, thirteen
lines apart in one comment block. The claim itself is true and I checked it:
`blank_fences` carries its own inline `^\s*` pattern and no other gate reads
`FENCE_RE`.

### 5. `spec.md` G3's new clause splits the round 5 clause from its subject

`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`
§*Goals* G3. The round 6 clause is spliced in ahead of the round 5 one, so the
row now reads *…round 6 found the first version of that reading sharing the
scan's own fence bound… — the earlier oracle borrowed `live_lines`'s own
boundary list, which round 5 found…*. A reader meets round 6 first and then an
*earlier oracle*, which sounds like a third one. Both facts are true; the
order is what is wrong. This is a correction, not a fix to commission.

### 6. `overview.md` says the oracle shared two bounds the reader did not have

`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md`
§*Not verified* — *its oracle shared the reader's two indentation bounds*. The
defect was that neither had them. And as of this SHA the oracle has two and
the reader has one, which is finding 1 — so the sentence describes neither the
old state nor the new one. A correction.

### 7. The shape family's docstring counts two controls where there is one

`tests/test_unverified_rows_close.py:1866` —
`test_every_shape_five_review_rounds_named`, *One row per shape a review round
of this work item found, and the two controls*. Collected: 8 rows, of which
one is the control (`a genuine marker, nothing quoted`). Pre-existing — the
docstring is untouched by this fix range — and named here because the family
gained a row in it.

## What I confirmed rather than opened

**The fence bound and the oracle's bound are genuinely in step.** Reverting
`FENCE_RE` to `^\s*` reddens two cases, the fuzz and the hand-written
indented-delimiter row. Reverting the oracle's bound alone reddens the fuzz —
the trap round 5 named, now caught rather than merely described. With both as
shipped, the two documents report 0 unsafe lines; with the oracle lax and the
reader bounded, the fenced-example document reports 5, which is the figure
ledger row R14 states.

**Bounding `FENCE_RE` moves 0 lines in all 1,461 `.md` files**, re-derived on
the landed module rather than carried.

**The paragraph rule's corpus figures are right, and they are the landed
rule's rather than the proposed one's.** Comparing the whole module at
`133fdfd5` against the module at this SHA: liveness moves on exactly 6 lines
in 4 files, every one under `seal/specs/`, five toward parked and one toward
live, and **not one of them is a `FOLD_MARKER` line**. `folded_items` answers
identically across the tree. That is what ledger row R15 claims, measured
independently.

**The corpus floor really is stronger.** Under a regression that parks the
first occurrence of every repeated marker, the old dictionary form stays
green — all three named markers and 83 keys — and the occurrence form reports
11 parked lines. `seal/ledger.md` at this SHA: 2,430 lines, 761 not-live, 94
occurrences, 83 unique, 0 parked.

**The docstring's measured example reproduces.** `["text `", "===", "text `",
"plain prose", "text `"]` reads `[T, T, T, F, F]` as shipped and
`[T, F, F, T, T]` with the setext stop removed — the last two lines going live
where the format parks them, which is what the docstring says.

**I went looking for the reverse of finding 1 and did not find it.** An
absolute three-space bound is wrong for a fence inside a list item, where
CommonMark measures the three spaces from the item's content column — and this
repository has two such fences, in `skills/evidence-ci/SKILL.md` and
`skills/implement/orchestration.md`. It does not reach `folded_items`:
`FOLD_MARKER` is `^<!-- specs/(\S+) -->$`, line-anchored, so a marker indented
inside such a fence can never match, and a marker at column zero would end the
list item and the fence in the format too. On the five-space case I built, the
reader at `133fdfd5`, the reader at this SHA and the oracle all agree. `docs/`,
the only tree `folded_items` reads, carries no indented fence.

**G3 and A6's note state what is true now.** G3's added clause is accurate —
the oracle did share the scan's fence bound and the bound moved in both — and
A6's note now says the acceptance that replaced it is the safety direction
rather than agreement, which is what G3 four rows above records the design as
forbidding. Only the reading order in G3 is wrong, which is finding 5.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The ATX indentation bound went into the oracle and not into the reader, so `live_lines` reads a marker live on a legal document the oracle parks; four more stops ignore indentation in both, where the case cannot see them | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | open | Executed in a clone at this SHA. 1,749 disagreeing lines over 1,461 `.md` files; the four-line document above reads `[live, live, live, live]` against the oracle's `[live, parked, parked, parked]`. Removing the oracle's bound leaves 192 passed exit 0, so nothing pins it. Bounding the reader: 192 passed exit 0 and 0 lines of liveness move |
| ⬜ 2 | The generator comment credits the lone-token branch with the indented delimiter as well as the setext underline | `tests/test_unverified_rows_close.py#documents_with_several_spans_on_a_line` | open | Executed, four generator variants against four reverts. The branch carries the setext revert alone; the `"    ```"` token and the hand-written row carry the delimiter |
| ⬜ 3 | The corpus floor's unique-id assertion prints the occurrence count on failure | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | open | Read. `assert len({...}) >= 80, len(occurrences)` |
| ⬜ 4 | The constant's comment repeats the `blank_fences` sentence thirteen lines later | `skills/verify/scripts/unverified_check.py#FENCE_RE` | open | Read, and the claim itself verified: `blank_fences` holds its own `^\s*` and no other gate reads `FENCE_RE` |
| ⬜ 5 | G3's round 6 clause is spliced ahead of the round 5 clause, so *the earlier oracle* reads as a third one | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Goals* G3 | open | Read. Both facts true, the order wrong |
| ⬜ 6 | §*Not verified* says the oracle shared the reader's two indentation bounds; neither had them, and today the counts are two and one | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | open | Read against the diff that made the sentence |
| ⬜ 7 | The shape family's docstring says *the two controls*; there is one | `tests/test_unverified_rows_close.py#test_every_shape_five_review_rounds_named` | open | Collected: 8 rows, one control. Pre-existing, outside the fix range |
| 🟢 confirmation | Round 6's finding 1 — the fence bound — is fixed, and the reader's and the oracle's bounds move together | `skills/verify/scripts/unverified_check.py#FENCE_RE` | confirmed | Executed. Reverting the reader's bound reddens 2 cases; reverting the oracle's alone reddens the fuzz; the lax oracle calls the corrected reader unsafe on 5 lines of the fenced-example document and the bounded one on 0 |
| 🟢 confirmation | Round 6's finding 2 — the oracle's blindness — is fixed for the fence and for the three paragraph rules the generator now reaches | `tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules` | confirmed | Executed, the mutation mapping derived rather than carried; the table in finding 2 above is it |
| 🟢 confirmation | Round 6's finding 3 — the docstring — is fixed and its measurement reproduces | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | confirmed | Executed. The setext document reads `[T, T, T, F, F]` shipped and `[T, F, F, T, T]` with the stop removed |
| 🟢 confirmation | Round 6's finding 4 — the paragraph stops — moves liveness on exactly 6 lines in 4 files, all under `seal/specs/`, five toward parked, and on no `FOLD_MARKER` line | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | confirmed | Executed, the whole module at `133fdfd5` against the whole module at this SHA over 1,461 files. `folded_items` is unchanged across the tree |
| 🟢 confirmation | Round 6's finding 5 — the corpus floor — is fixed and the new form catches what the old one could not | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | confirmed | Executed. A regression parking every first duplicate leaves the dictionary form green and the occurrence form red on 11 lines |
| 🟢 confirmation | The absolute three-space bound does not break a fenced example inside a list item, and could not reach `folded_items` if it did | `skills/verify/scripts/unverified_check.py#FOLD_MARKER` | confirmed | Executed. `FOLD_MARKER` is line-anchored; a five-space fence inside a list item reads the same under `133fdfd5`, this SHA and the oracle; `docs/` carries no indented fence |
| 🟢 confirmation | Ledger rows R14 and R15 state figures that hold at this SHA | `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md` | confirmed | Executed: 0 lines for the fence bound over 1,461 files, 5 unsafe lines for the lax oracle, 6 lines across 4 files for the paragraph rule, 761 / 94 / 83 for `seal/ledger.md` |
| 🟢 confirmation | G3 and A6's note state what is true now | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` | confirmed | Read against the code and against G3's own sentence about agreement. Only the reading order is wrong, which is ⬜ 5 |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. I ran the two affected modules and nothing else. The caller answers it |

## Paste-ready fixes

Finding 1, the reader — `skills/verify/scripts/unverified_check.py`,
`_paragraph_ends_at`, replacing the two lines that open the body after the
blank-line check:

```python
    if s.startswith("|"):
        return True
    # CommonMark bounds every block start below to three spaces of
    # indentation. At four a heading, a thematic break, a bullet, an ordered
    # marker and a setext underline are an indented code block or a lazy
    # continuation, and stopping there is an over-stop — the direction that
    # goes live (round 7). The table row above is the deliberate exception:
    # GFM parses a row's cells independently at any indentation.
    if len(line) - len(line.lstrip(" ")) > 3:
        return False
    # `>` is the format's own rule (CommonMark 5.1).
    if s.startswith(">"):
        return True
```

Finding 1, the oracle — `tests/test_unverified_rows_close.py`,
`block_ends_at`, replacing the combined table-row and block-quote check. The
`indent <= 3` guards already on the heading and the fence become redundant and
can go:

```python
        if s.startswith("|"):
            return True
        if indent > 3:
            return False
        if s.startswith(">"):
            return True
```

Both together: 192 passed, exit 0, and 0 lines of liveness move over all
1,461 `.md` files.

Finding 3 — `tests/test_unverified_rows_close.py`:

```python
    unique = {line for _, line, _ in occurrences}
    assert len(unique) >= 80, len(unique)
```

## Executed probes

| What was run | Result |
|---|---|
| the two affected modules in a `git clone --no-local` at the target SHA | 192 passed, exit 0, read with `echo $?` and not through a pipe |
| nine mutations, each applied alone and restored, against both modules | reader fence bound → 2 red; reader ATX guard → fuzz red; reader ordered rule → fuzz red; reader setext rule → fuzz red; oracle fence bound → fuzz red; **oracle ATX bound → green**; oracle setext rule → fuzz red; generator lone-token branch → green; reader ATX bounded → green |
| four generator variants against four paragraph reverts | the five new tokens carry the ATX, ordered and setext reverts; the lone-token branch carries the setext revert alone; the delimiter revert stays red in every column |
| `_paragraph_ends_at` against the oracle's `block_ends_at`, 22 crafted lines and every `.md` file in the tree | 2 crafted lines differ and 1,749 tree lines differ, all of them an indented `#` |
| the four-line indented-heading document through `live_lines` and the oracle | reader `[live, live, live, live]`, oracle `[live, parked, parked, parked]` |
| the whole module at `133fdfd5` against the whole module at this SHA, over 1,461 `.md` files | 6 lines move, in 4 files, all under `seal/specs/`, 5 toward parked; 0 `FOLD_MARKER` lines |
| `FENCE_RE` reverted alone on the landed module, over 1,461 `.md` files | 0 lines move |
| the reader's ATX stop bounded, and every stop bounded, over 1,461 `.md` files | 0 lines move in both |
| the proposed bound applied to reader and oracle together, both modules | 192 passed, exit 0 |
| the fenced-example and straddling documents against the bounded and the lax oracle | bounded 0 unsafe in both; lax 5 unsafe on the fenced-example document |
| the setext document with and without the stop | `[T, T, T, F, F]` shipped, `[T, F, F, T, T]` without — the last two lines going live |
| a five-space fence inside a list item, marker at column zero, through `133fdfd5`, this SHA and the oracle | all three agree; `FOLD_MARKER` does not match an indented marker |
| `docs/*.md` scanned for a fence opener indented four or more spaces | none |
| `seal/ledger.md` through `live_lines` | 2,430 lines, 761 not-live, 94 marker occurrences, 83 unique ids, 0 parked |
| the corpus floor under a regression parking every first duplicate | the dictionary form green, the occurrence form red on 11 lines |
| the shape family collected | 8 rows, 7 shapes and 1 control |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it, and with nothing in finding 1 blocking, it has come due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-6 | `skills/verify/scripts/unverified_check.py#FENCE_RE` | round 6's 1 — fixed, re-derived here |
| round-6 | `tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules` | round 6's 2 — fixed, and finding 1 above is its residue |
| round-6 | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | round 6's 3 and 4 — fixed; finding 1 above opens the same unit |
| round-6 | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | round 6's 5 — fixed, and shown stronger by execution |
| round-6 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Goals* G3 | round 6's ⬜ 6 — fixed; ⬜ 5 above is the reading order it left |
| round-6 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | round 6's ⬜ 7 — fixed |
| round-6 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | round 6's ⬜ 8 and ⬜ 9 — fixed; ⬜ 6 above is what the new row states |
| round-6 | `skills/verify/scripts/unverified_check.py#_partner_ahead` | round 6's ⬜ — confirmed, untouched by this range |
| round-6 | the repository | round 6's ❓ out of verified scope — not run |
| round-5 | `skills/verify/scripts/unverified_check.py#comment_scan` | round 5's 3 — fixed, untouched by this range |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 and confirmed in rounds 4, 5 and 6 | the orchestrator |

Needs a fix: yes — finding 1, the missing indentation bound in
`_paragraph_ends_at`. The run is capped, so whether it is fixed here as round
6's five were, or filed, is the orchestrator's call; the fix is one guard and
it was measured green.

Loses a record or crashes: no — no `FOLD_MARKER` line changes state anywhere
in the tree, `docs/` carries nothing finding 1 can reach, and the fix range
leaves `folded_items` answering identically at `133fdfd5` and at this SHA.

## Proof block

Opened in a `git clone --no-local` at `b5d2906b`:
`skills/verify/scripts/unverified_check.py`,
`tests/test_unverified_rows_close.py`, `bin/test`,
`skills/evidence-ci/SKILL.md`, `skills/implement/orchestration.md`,
`seal/ledger.md`,
`seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`,
and under
`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/`:
`spec.md`, `overview.md`, `changelog.md`, `rounds/round-6.md`,
`rounds/round-6-report.md`. Read at `133fdfd5` through `git show`:
`skills/verify/scripts/unverified_check.py`.
