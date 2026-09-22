# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 4

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Target SHA | 3c1372d6aa7ff3845c74884f5668df2dcf639db8 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | not yet |
| Fixes checked by | round-5 |
| Fix range | `a9447415a070076c774ae02e8abe09f50c3d35a1..e0ae20c78b5233f3a869ad3fbd2d0c82e7b96782`, 7 commits |
| Contract changes | test_a_code_span_closes_at_a_backtick_string_of_equal_length → pytest only |
| New units | BACKTICKS (depth 1); FENCE_RE (depth 1); is_block_boundary (depth 1); test_strip_comments_reads_through_the_one_comment_scanner (depth 1); test_the_scan_decides_a_fence_before_a_comment_or_a_span (depth 1); test_the_first_delimiter_on_the_line_wins (depth 1); a_character_level_reading (depth 1); documents_with_several_spans_on_a_line (depth 1); test_the_scan_agrees_with_a_character_level_reading (depth 1) |
| Needs a fix | yes — finding 1, the span-local stop, which still removes a work item's directory at exit 0 on a line whose closing and re-opening delimiters sit in different code spans; and finding 2, the contract's guarantee, which is stated as a measured 0 and is false. |
| Loses a record or crashes | yes — finding 1, a work item's whole SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway git repository at the target SHA. |

- [x] Pass

## What this round was asked

The verifying round, against the diff of round 3's fixes — `b202171c..dbe8006c`,
three commits — rather than the branch. Round 3's record read `Fixes checked by:
nobody`, and closing that is the job.

The bound was named in the prompt because it is not the usual one: no record on
this work item reads `Needs a fix: no`, so the reopening walk never starts and
the cap governs — three rounds, and five while a 🔴 is open. This is the fourth
of an allowed five.

The round was told the pattern rather than only the diff: three of this
branch's four rounds found a repair moving the fold gate toward deleting a
directory and the prose not following it. So the fourth formulation of the
liveness rule was to be broken in both directions on five shapes the earlier
rounds did not reach, and the fix pass's rebuilt fuzz oracle was to be judged
rather than its numbers carried — an oracle that disagrees with the round that
commissioned it is either a correction worth keeping or a measurement tuned
until it agreed.

Also handed over: the rule's newly stated contract, four claims to check
against the code; `spec.md` §*Grounding* G3, rewritten by the orchestrator
after round 3 found its ground false; a census that left two sites alone, which
is as answerable as one that changes them; and a ⬜ observation about stamps on
round records, to confirm or refute rather than reopen.

The broad gate was withheld — the sealer's, and nothing but this round's
findings stands between it and that spawn.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The stop is computed inside one span, so a closing delimiter quoted in an earlier span does not stop the blanking in a later one — a marker inside a parked draft reads as a fold record and `settle --retire` removes the work item's directory at exit 0 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `66d63889` | fixed at 66d63889 — not the round's paste-ready patch, which was the fifth guess in the same place. The three-pass composition is replaced by one scan carrying fence, comment and span state, so the mutual dependence that made every formulation a guess is gone. All four rounds' shapes are pinned, and the multi-line span `overview.md` recorded as unclosable is closed by the same change; Round 3's finding 1 is closed for its named shape and open for its class. Executed on a throwaway git repository: the two-span shape takes `settle --retire` from exit 1 *nothing to retire* to exit 0 `removed seal/specs/1700000042-quoted/` with the directory deleted, while round 3's one-span control and a quotation-free control both refuse at exit 1. `settle.coordinates` files the parked draft's row under `1700000002-beta`. Both readings park the marker — `comment_scan` over the raw document answers *began inside*, and the interleaved reading pairs the remaining backticks into a span that stops before the opening delimiter — so the finding does not rest on a markdown subtlety. Corpus unmoved and no instance today: 761 / 83 / markers live at 767, 992, 1619 / 0 lines differing. The paste-ready patch moves the stop to the line, keeps both modules green at 178 passed exit 0 and the corpus figures unchanged, and takes the structured fuzz's expensive direction from 21 lines to 0 |
| 2 | 🟡 The contract's *What it guarantees* bullet states as a measured 0 that the pass never reads live a line the reading parks; finding 1 is a counterexample and the 0 is a generator artifact | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `66d63889` | fixed at 66d63889 — `84abddef`, `178d9a7e` for the docstring, `plan.md`, `overview.md`, the changelog and the ledger; `c3aa30fe` for `spec.md` §*Grounding* G3, which is the orchestrator's. The contract changed kind rather than value: there is no approximation left, so there is no expensive-versus-cheap direction to declare, and what stands in its place is agreement with an independently written character-level reading over documents carrying several spans on a line — oracle and generator now in the tree as a case; Executed: rebuilt the interleaved oracle independently. With a generator whose lines carry at most one span, 0 expensive over 40,000 documents — the reported answer reproduces. With a generator that can put several spans on one line, the same oracle gives 16 documents and 21 lines expensive over 40,000, and every one is finding 1's shape. The fix pass's criticism of round 3's oracle is itself correct: a pure HTML reading knows no code spans and can never report a cheap-direction disagreement, which is what round 3's `0 cheap` was. So the rebuild is a correction, not a tuning; the generator is what is narrow. Neither oracle nor generator is in the tree, so no reader can re-derive either figure. The same claim is carried by `spec.md` G3, `plan.md` §*Operational impact*, `overview.md` and R8 of the ledger fragment |
| ⬜ 3 | `spec.md` G3 says three formulations moved the gate toward deleting; the docstring one commit earlier says two of the three before this one | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | **fixed** `c3aa30fe` | fixed at c3aa30fe — for G3, `178d9a7e` for the same miscount in three sites the fix pass had just written. Three of the four formulations moved the gate toward deleting, not all four: the first lost a marker and misfiled a row; Read, and counted from the branch: formulation 1 left drafts open and misfiled a row rather than deleting; formulations 2 and 3 each moved the gate toward deleting and a round caught each. *Two of the three* is right and G3's *three* has no third. Under `seal/specs/`, so a correction to the run's paperwork and outside `Needs a fix` |
| ⬜ | A stamp on a round report is tracked as a live claim, so a record states a value that did not exist at its own `Target SHA` | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | confirmed | Confirmed as asked rather than re-opened. The anchor is quoted seven times across five files, and `68a023af` rewrote five stamps in four of them. Executed: `git merge-base --is-ancestor 281308c7 7f2d6f1c` exits 1, so the hash `round-2.md` carries beside `Target SHA 7f2d6f1c` first existed three commits later. A home for the decision is `seal/follow-up.md`, not this branch |
| 🟢 confirmation | Round 3's finding 1 is closed for the shape it named | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Executed: with both delimiters inside one span, `settle --retire` refuses at exit 1 *nothing to retire* and the directory stays, against exit 0 and a deletion before `a8648f33`. The residue is finding 1 above, which is the class rather than the shape |
| 🟢 confirmation | Round 3's finding 2 is closed — the HTML ground is gone from every live site, and the census of six is answerable | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Re-derived the census rather than carrying it: swept the tree for the ground and the only live site still carrying the phrase is `overview.md:44`, which carries it to say the row used to rest on it and that it is false. Every other match is inside `round-2.md`, `round-2-report.md`, `round-3.md` or `round-3-report.md` — records, correctly left alone, because rewriting one deletes what was true at that round. What stands in the ground's place is finding 2 above |
| 🟢 confirmation | Round 3's finding 3 is closed — the `OPENER` comment no longer claims nothing blanks into such a span | `skills/verify/scripts/unverified_check.py:107-118` | **fixed**, verified | Read. The comment states why the closing delimiter is a constant, and `CLOSER` sits beside it |
| 🟢 confirmation | Both new units are red under a mutation and the mapping is one-to-one | both test modules and `skills/verify/scripts/unverified_check.py` | confirmed | Executed, three mutations each applied alone and restored, the file byte-identical after each. Dropping the stop reddens the new case alone (1 failed of 62); spelling `CLOSER` wrongly reddens the same case alone, so its value is pinned and not merely its existence; round 1's rule reddens round 2's case instead, so the new case marks exactly the step it was written for. `tests/test_unverified_rows_close.py` stays at 116 passed under all three |
| 🟢 confirmation | Three of the docstring's four contract claims hold, and the figures are the pass's own | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Read and executed. *What it approximates* is true — `live_lines` calls the pass before `opens_outside_a_comment` and the pass holds no state. *Which mistake it prefers* is true — `settle.py`'s module docstring makes the same choice in the same words, a thin policy document a reader can see against a directory deleted with nothing absorbing it. *What it gives up* is true in direction and its figure is not re-derivable. *What it guarantees* is finding 2. Round 3 recorded 5 and 0; the docstring records 0 and 132, so the numbers are the pass's own |
| 🟢 confirmation | The docstring's sentence about which openers are blanked matches the code | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Read against the `else` arm: the prose says *only those before the span's first closing delimiter* and the code blanks an opener whose end is at or before that delimiter. The prose followed the stop this time; the stop is what finding 1 is about |
| 🟢 confirmation | The fix pass's own depth reading is right | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Agreed. The new case pins a defect in the `else` arm round 2's pass created, and `blank_code_spans` is a build unit, so depth 1 is the reading; `round-record` measured 1 and did not refuse it (NAME NOT IN TREE) |
| 🟢 confirmation | `spec.md` G3 judges the build rather than excusing it, and its other claims are true | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | confirmed | Read and executed. It names its own false ground and the round that found it false. `folded_items` is reached through the `--baseline` arm at `skills/verify/scripts/unverified_check.py:1119`, which is what `.github/workflows/hygiene.yml:161` passes. The case-seen-red item holds by mutation. Its fuzz claim is finding 2 and its count of formulations is finding 3 |
| 🟢 confirmation | The corpus invariant survives the fourth formulation | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed over `seal/ledger.md`, every `seal/ledger/*.md` fragment and every top-level `docs/` document, eleven files: 761 not-live lines; 94 live marker occurrences over 83 unique ids; the three named markers live at 767, 992 and 1619; and 0 lines answering differently from the rule that blanked every span or from round 3's rule |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports the four affected modules at 335 passed exit 0, `evidence_check.py --strict .` at exit 0 with 0 drifted and 0 broken, and `survivor-check` at exit 0, all at this SHA; this round did not re-run them and does not certify them. The caller answers it |

## Paste-ready fixes

```python
        runs = [(m.start(), m.end()) for m in re.finditer(r"`+", line)]
        chars, i = list(line), 0
        # The stop is the LINE's first closing delimiter, not each span's.
        # Inside a parked draft these backticks are not spans at all: the
        # draft ends at the first closing delimiter on the line, wherever it
        # falls, and every delimiter after that point is ordinary text. A
        # closing delimiter quoted in an EARLIER span ends the draft just as
        # surely as one quoted in this span, so blanking an opener after it
        # re-opens a draft that reading has already closed — a parked marker
        # read as a fold record, and `settle --retire` removing the directory
        # at exit 0 (round 4, finding 1; round 3, finding 1 one span over).
        # Outside a draft the earlier closing delimiter is inert and the whole
        # run really is a span, so the surviving opener parks the lines below
        # it instead: fewer lines live, a fold reported as a deletion, which
        # is the direction this module has already chosen to be wrong in.
        stop = line.find(CLOSER)
        stop = len(line) if stop == -1 else stop
```
```python
            else:
                # The DELIMITER, not the span around it — and only the
                # openers this span can still be quoting, judged against the
                # line's stop above rather than this span's own text.
                for m in re.finditer(re.escape(holding), span):
                    if start + m.end() <= stop:
                        chars[start + m.start() : start + m.end()] = " " * len(holding)
```
```python
# The opening delimiter of an HTML comment, and the only one `live_lines` asks
# `blank_code_spans` to look for. Its pair is a constant too, and only because
# the pass has to know where a line's quotation STOPS: inside a parked draft
# the first closing delimiter on the line really ends it, so an opener after
# that point is ordinary text and a real opener. Nothing blanks a closing
# delimiter — see `blank_code_spans`'s docstring for why a surviving one is
# the safe half.
OPENER = "<!--"
CLOSER = "-->"
```
```python
def test_a_closer_quoted_in_one_span_stops_the_blanking_in_a_later_one(tree):
    """The residue round 4 found in round 3's repair. The stop was the span's
    and it belongs to the line: inside a parked draft the backticks are not
    spans at all, so a closing delimiter quoted in an EARLIER span ends the
    draft and an opener quoted in a LATER one re-opens it. Blanking that
    opener read a parked marker as a fold record, and `settle --retire`
    removed the directory at exit 0 with nothing having absorbed it."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the line below ends it and re-opens it
        + "prose that quotes `--> and x` then `<!--` here\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n"
        + "-->\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" not in rows.get("1700000002-beta", []), dict(rows)
```
```python
    - *What it guarantees.* Against every shape measured so far it has not
      read live a line the interleaved reading parks, which is the direction
      that retires a directory and the one this module may not be wrong in.
      That is a measurement and not a proof: the pass is an approximation of
      a reading it cannot perform, and three formulations before this one
      passed the fuzz of their day and were broken by a shape the generator
      did not build. Measured 2026-09-22 over 40,000 generated documents
      whose lines carry SEVERAL code spans each — the generator's shape is
      the whole of what a count like this covers, and a generator of
      single-span lines reports 0 for a rule that has this defect: **0**.
    - *What it gives up.* It parks lines the reading calls live — 5,287 over
      the same 40,000 documents. A marker that stops counting is a fold
      record unread: a directory kept and a deletion reported, which a person
      can see.
```
```
Two of the three formulations before this one moved the gate the other way
and a round caught each
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the two affected modules, pristine, in the clone | 178 passed, exit 0, read with `echo $?` and not through a pipe |
| the corpus under four liveness rules — fence-only, blank-every-span, round 3's, shipped | `seal/ledger.md` 761 not live; 0 lines of eleven corpus files disagree between shipped and either earlier span rule |
| unique section ids in `seal/ledger.md` under the shipped rule | 83, from 94 live marker occurrences |
| the three named markers, through the shipped rule | live at `seal/ledger.md` lines 767, 992 and 1619 |
| ten adversarial span shapes — shipped against blank-every-span against round 1's rule against an independently written interleaved reading | nine agree; the two-span shape reads live where the reading parks, and that shape is finding 1 |
| the two-span shape through `settle.coordinates` on a throwaway ledger | the parked draft's row filed under `1700000002-beta` |
| `folded_items` and `settle --retire` over finding 1's fixture, on a throwaway git repository | `{'1700000042-quoted'}`, exit 0, `removed seal/specs/1700000042-quoted/`, directory deleted |
| the same command over round 3's one-span shape and over a quotation-free draft, as controls | exit 1 *nothing to retire* for both, directories kept |
| the same five-line document through `comment_scan` — a pure HTML reading, no markdown at all | the marker line answers *began inside*; the shipped pipeline answers *began outside* |
| a 40,000-document fuzz against an independently written interleaved oracle, lines built from a random token run (at most one span a line in practice) | 0 expensive, 210 cheap lines — the fix pass's reported answer reproduces under this generator |
| the same 40,000-document fuzz with a generator that can put several spans on one line | **16 documents, 21 lines expensive**; 2,281 documents, 3,758 lines cheap |
| the proposed patch — the stop moved from the span to the line — against the same structured fuzz | **0 expensive**; 3,156 documents, 5,287 lines cheap |
| the proposed patch against the two modules and the corpus | 178 passed exit 0; 761 not-live, 83 ids, the three markers live, 0 lines differing |
| three mutations, each applied alone and restored, against the units the `New units` row names | dropping the stop → the new case red alone, 1 failed of 62; `CLOSER` misspelled → the new case red alone; round 1's rule → round 2's case red alone. `tests/test_unverified_rows_close.py` 116 passed under all three |
| the ground census — a tree-wide sweep for the HTML ground the fix range removed | one live site, `overview.md:44`, which carries the phrase only to call it false; every other match is a round record |
| `git merge-base --is-ancestor 281308c7 7f2d6f1c` | exit 1 — `round-2.md`'s stamp postdates its own `Target SHA` |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it, and what stands between it and that spawn is finding 1 |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 | the orchestrator |
