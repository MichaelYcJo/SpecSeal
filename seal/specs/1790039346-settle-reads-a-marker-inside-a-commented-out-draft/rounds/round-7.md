# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 7

| Field | Value |
|---|---|
| Target SHA | b5d2906b3445c95d038b82056c2a3934c84a6ce6 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | 5e2ede92 against 3cdfd8ad |
| Fixes checked by | no fixes to check |
| Fix range | `b5d2906b3445c95d038b82056c2a3934c84a6ce6..b5d2906b3445c95d038b82056c2a3934c84a6ce6`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1, the missing indentation bound in `_paragraph_ends_at`. The run is capped, so whether it is fixed here as round 6's five were, or filed, is the orchestrator's call; the fix is one guard and it was measured green. |
| Loses a record or crashes | no — no `FOLD_MARKER` line changes state anywhere in the tree, `docs/` carries nothing finding 1 can reach, and the fix range leaves `folded_items` answering identically at `133fdfd5` and at this SHA. |

- [x] Pass

## What this round was asked

A verifying round at the diff of round 6's fixes — `133fdfd5..c57e5b2a`, two
commits — and narrow by construction. Round 6's `Fixes checked by` read
`nobody`, which `chain_check` refuses at a ready pull request, and the gate
names the way out itself: a round that opens nothing needing a fix does not
consume the cap.

The sequence before it was not the usual one and the round was told so. Round
6 was the last round the cap allowed and it opened five findings, so they were
filed as #491 and the record closed `deferred`. The owner asked why a one-line
verified repair had been filed instead of made; the grounds were re-examined
and found weak — `FENCE_RE` is a unit round 4 of this work item created and
the character-level oracle is this branch's outright — so all five were fixed
here, the record was corrected in place, and #491 was narrowed.

So this round read those fixes: whether the fence bound moved in the reader
and the oracle together, whether the five mutations the fix pass reports all
redden something now that it had to widen its own generator to make them, the
three smaller repairs, and the orchestrator's two `spec.md` lines. It was also
asked for one judgment somebody can disagree with: whether this reader, the
fourth formulation of a rule whose every earlier formulation opened a shape
the one before parked, is done.

The broad gate was withheld — the sealer's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The ATX indentation bound went into the oracle and not into the reader, so `live_lines` reads a marker live on a legal document the oracle parks; four more stops ignore indentation in both, where the case cannot see them | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | deferred #491 | #491 — The run stops here, and this is where the stopping is recorded. Seven rounds is past every bound the chain has; the cap is three, five while a 🔴 is open, and the reopening rule allows one. The finding is real and it is the same class the branch has met five times — a bound in the oracle and not in the reader, so the case cannot see it — but it **moves no line of liveness anywhere in this tree**, measured by the round over all 1,461 `.md` files, and `folded_items` answers identically across the repository with and without it. #491 already owns the bounds of these readers and names the repository owner, which is the test #493 proposes for whether a finding is filed at all; Executed in a clone at this SHA. 1,749 disagreeing lines over 1,461 `.md` files; the four-line document above reads `[live, live, live, live]` against the oracle's `[live, parked, parked, parked]`. Removing the oracle's bound leaves 192 passed exit 0, so nothing pins it. Bounding the reader: 192 passed exit 0 and 0 lines of liveness move |
| ⬜ 2 | The generator comment credits the lone-token branch with the indented delimiter as well as the setext underline | `tests/test_unverified_rows_close.py#documents_with_several_spans_on_a_line` | deferred #491 | #491 — A generator comment overstating what its lone-token branch carries; Executed, four generator variants against four reverts. The branch carries the setext revert alone; the `"    ```"` token and the hand-written row carry the delimiter |
| ⬜ 3 | The corpus floor's unique-id assertion prints the occurrence count on failure | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | deferred #491 | #491 — A wrong count in a failure message; Read. `assert len({...}) >= 80, len(occurrences)` |
| ⬜ 4 | The constant's comment repeats the `blank_fences` sentence thirteen lines later | `skills/verify/scripts/unverified_check.py#FENCE_RE` | deferred #491 | #491 — A sentence repeated thirteen lines later in a constant's comment; Read, and the claim itself verified: `blank_fences` holds its own `^\s*` and no other gate reads `FENCE_RE` |
| ⬜ 5 | G3's round 6 clause is spliced ahead of the round 5 clause, so *the earlier oracle* reads as a third one | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Goals* G3 | deferred #491 | #491 — G3's two clauses in an order that makes the earlier oracle read as a third one. Located under `seal/specs/`, a correction to the run's paperwork; Read. Both facts true, the order wrong |
| ⬜ 6 | §*Not verified* says the oracle shared the reader's two indentation bounds; neither had them, and today the counts are two and one | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | deferred #491 | #491 — `overview.md` §*Not verified* describing neither the old state nor the new. Same location, same kind; Read against the diff that made the sentence |
| ⬜ 7 | The shape family's docstring says *the two controls*; there is one | `tests/test_unverified_rows_close.py#test_every_shape_five_review_rounds_named` | deferred #491 | #491 — A pre-existing docstring counting two controls where there is one; Collected: 8 rows, one control. Pre-existing, outside the fix range |
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
```python
        if s.startswith("|"):
            return True
        if indent > 3:
            return False
        if s.startswith(">"):
            return True
```
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
| round-1 | `skills/verify/scripts/unverified_check.py#live_lines` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | round 1's 2 — fixed |
| round-1 | `skills/settle/scripts/settle.py#coordinates` | round 1's 3 — answered |
| round-1 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/unverified_check.py` | round 1's 🟢 confirmation — confirmed |
| round-1 | `skills/settle/scripts/settle.py#main` | round 1's 🟢 confirmation — confirmed |
| round-1 | both test modules | round 1's 🟢 confirmation — confirmed |
| round-1 | `tests/test_a_row_points_by_content.py:763` | round 1's ⬜ — confirmed |
| round-2 | both test modules and `skills/verify/scripts/unverified_check.py` | round 2's 🟢 confirmation — confirmed |
| round-2 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/survivors.md` | round 2's ⬜ — confirmed |
| round-2 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-1-report.md:191` | round 2's ⬜ — confirmed |
| round-2 | the repository | round 2's ❓ out of verified scope — not run |
| round-3 | `skills/verify/scripts/unverified_check.py:107-110` | round 3's ⬜ 3 — fixed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | round 3's ⬜ — confirmed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:30` | round 3's 🟢 confirmation — confirmed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Operational impact* | round 3's 🟢 confirmation — confirmed |
| round-4 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | round 4's ⬜ 3 — fixed |
| round-4 | `skills/verify/scripts/unverified_check.py:107-118` | round 4's 🟢 confirmation — fixed |
| round-5 | `skills/verify/scripts/unverified_check.py#is_block_boundary` | round 5's 1 — fixed |
| round-5 | `tests/test_unverified_rows_close.py#a_character_level_reading` | round 5's 2 — fixed |
| round-5 | `skills/verify/scripts/unverified_check.py#comment_scan` | round 5's 3 — fixed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Data & interfaces* | round 5's ⬜ 4 — fixed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | round 5's ⬜ 5 — fixed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md` | round 5's ⬜ — confirmed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/` | round 5's 🟢 confirmation — confirmed |
| round-5 | the two affected modules | round 5's 🟢 confirmation — confirmed |
| round-6 | `skills/verify/scripts/unverified_check.py#FENCE_RE` | round 6's 1 — fixed |
| round-6 | `tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules` | round 6's 2 — fixed |
| round-6 | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | round 6's 3 — fixed |
| round-6 | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | round 6's 5 — fixed |
| round-6 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Goals* G3 | round 6's ⬜ 6 — fixed |
| round-6 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | round 6's ⬜ 8 — fixed |
| round-6 | `skills/verify/scripts/unverified_check.py#_partner_ahead` | round 6's ⬜ — confirmed |
| round-6 | `seal/ledger.md` | round 6's 🟢 confirmation — confirmed |
| round-6 | `seal/specs/` | round 6's 🟢 confirmation — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 1 — the ATX bound in the oracle and not the reader | #491 | the repository owner |
| 2 to 7 — six corrections, three in shipped comments and three under `seal/specs/` | #491 | the repository owner |
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 and confirmed in rounds 4, 5 and 6 | the orchestrator |
