# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 3

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Target SHA | 66dca36133d1b4cb589b7880a2602ddc385daaa3 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | not yet |
| Fixes checked by | round-4 |
| Fix range | `b202171cb6d44f21022119797b37dbf034b12225..dbe8006cfe9786693e861efa960a190b7673d4aa`, 3 commits |
| Contract changes | none |
| New units | CLOSER (depth 1); test_an_opener_after_a_quoted_closer_still_parks_the_marker_below (depth 1) |
| Needs a fix | yes — finding 1, a marker inside a parked draft read as a fold record so `settle --retire` removes the directory at exit 0, new at `281308c7`; and finding 2, the clause four live documents ground that direction on. The run is capped, so both are `deferred #N` candidates rather than fixes to commission. |
| Loses a record or crashes | yes — finding 1, a work item's SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway repository at both ends of the fix range. |

- [x] Pass

## What this round was asked

The last round the cap allows, against the diff of round 2's fixes —
`9e61df97..68a023af`, two commits — rather than the branch. Round 2's record
read `Fixes checked by: nobody`, and closing that is the job.

Finding 2's repair changed the rule a third time on this branch, from *blank
the span that holds an opener* to *blank the opener occurrences inside the
span*, so the round was asked to re-derive the corpus invariant that every
formulation must preserve and then to break the new one on four named shapes,
hunting in both directions: a real section marker losing liveness, and a
parked marker regaining it.

Two acts of the orchestrator's were handed over to be judged rather than
accepted: the `spec.md` §*Grounding* G3 clause it wrote, because the fix pass
refused to write a grounding clause that judges its own build; and five stamps
it moved after re-reading them, the third pass on this branch to chase one
coordinate. Whether a stamp on a round report should be tracked as a live
claim at all was asked as an observation for the record.

The class to enumerate was round 2's one new unit and the `c-8` shape, each
against the mutation that should redden it, with `c-8` checked for vacuity
because it is green by construction. And both of the fix pass's class
enumerations were re-checked, because a census run against the wrong target is
the miss this work item has already paid for once.

The broad gate was withheld — the sealer's, and nothing but this round's
findings stands between it and that spawn.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A span holding a closer and then an opener has the opener blanked, so a marker inside a parked draft reads as a fold record and `settle --retire` removes the directory at exit 0 with nothing having absorbed it | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `a8648f33` | fixed at a8648f33 — the blanking stops at the span's first closing delimiter, so an opener after it still re-opens the draft it sits in; New at `281308c7`. Executed: `folded_items` answers `set()` at `9e61df97` and `{'1700000042-quoted'}` here, and `settle --retire` goes from exit 1 *nothing to retire* to exit 0 `removed seal/specs/1700000042-quoted/`. Both earlier formulations park the marker. Fuzzed over 40,000 documents against a character-by-character HTML reading, the shipped rule reads live where HTML parks on 5 lines and parks where HTML reads live on 0; all 5 are this class. No instance in the corpus today — 0 lines answer differently from the rule that blanked every span. The run is capped, so this is a `deferred #N` candidate rather than a fix to commission |
| 2 | 🟡 The docstring, `spec.md` G3, `plan.md` §*Operational impact* and `overview.md` each ground the new direction on *that is what the HTML rule says*; the reasoning covers only the spans the predicate spares, and the change in this range is about the spans it does not | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `a8648f33` | fixed at a8648f33 — `d5d6e879` for the three sites the fix pass owns, and `dbe8006c` for `spec.md` §*Grounding* G3, which is the orchestrator's: a grounding clause is what judges the build, so the builder rewriting it is the split this work runs under. The HTML ground is gone from all four; what stands in its place is the direction the rule guarantees and the one it gives up, with the fuzz behind each; Read, and re-derived: monotonic non-decrease against the unnarrowed rule holds — every opener inside every span is blanked under both and the shipped rule additionally spares closers — but HTML-faithfulness does not, for finding 1's shape. The sentence needs an edit whichever way finding 1 is answered, because the paste-ready fix is faithful to the cheaper mistake rather than to HTML. G3's other three items are true and it judges the build rather than excusing it |
| ⬜ 3 | The `OPENER` constant's comment says no reader of the module blanks a span holding a closing delimiter, and one now writes into such a span | `skills/verify/scripts/unverified_check.py:107-110` | **fixed** `a8648f33` | fixed at a8648f33 — the `OPENER` constant's comment no longer claims no reader blanks into such a span, and the closing delimiter is a constant beside it; Read. The comment also forbids the closing delimiter as a constant, which finding 1's fix requires. Carried in the paste-ready fix below |
| ⬜ | A stamp on a round report is read as a live claim, so one coordinate has been rewritten three times across five files, and a record now states a value that did not exist at its own `Target SHA` | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | confirmed | Executed: reverting `round-1-report.md:191` to `661d041f` makes `evidence-check --strict .` report DRIFTED at exit 2, so the rewrite is forced rather than chosen. The observation the prompt asked for: a stamp quoting history has no way to say so. A home for the decision is `seal/follow-up.md`, not this branch |
| 🟢 confirmation | Round 2's finding 1 is closed — the direction is declared in every live site and pinned | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Read all five declaring sites — the docstring, `spec.md` G3, `plan.md` §*Operational impact* and §*What breaks in six months*, `overview.md`'s correction row — and each states both halves. Executed: `c-8` is red under the unnarrowed rule and green under both the round-1 and shipped rules, so it pins the direction round 1's predicate bought. The disclosure and the pin are what the fix owed, and both landed. What finding 2 above opens is one clause inside them, not their absence |
| 🟢 confirmation | Round 2's finding 2 is closed — a span quoting a complete comment keeps its closer | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Executed: `test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in` is red under the round-1 rule (blank the whole span that holds an opener) and under the unnarrowed rule, green as shipped. The fixture's marker is HTML-correct — inside a draft the quoted closing delimiter really does end it. The residue finding 1 names is one delimiter further along the same span, not this shape |
| 🟢 confirmation | Round 2's finding 3 is closed — all three false grounds corrected, and the census of eleven holds | `skills/settle/scripts/settle.py#coordinates` | **fixed**, verified | Re-derived the census rather than carrying it: eleven citations of `reader_blanking_passes` outside past work items' records. Three asserted it refuses a widened fence reader — `settle.py#coordinates`'s docstring, `test_an_indented_example_row_is_counted_and_the_reader_says_so`, and `overview.md:87` — and all three now name `test_a_continuation_that_looks_like_an_opener_is_still_joined` instead. Eight assert it refuses a pass added to `readable`; Executed, that is true: composing the span pass into `readable()` reddens `test_a_closing_word_a_reader_blanks_is_not_a_closing_note` at both parametrisations, 2 failed exit 1 |
| 🟢 confirmation | The corpus invariant survives the third formulation | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed over `seal/ledger.md`, every `seal/ledger/*.md` fragment and every top-level `docs/` document: 761 not-live lines against the naive rule's 789; 94 live marker occurrences and **83** unique section ids, the same 83 the fence-only reading gives; the three named markers live at `seal/ledger.md` lines 767, 992 and 1619; and **0** lines answering differently from the rule that blanked every span or from round 1's rule. `bin/settle` prints `released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped` at exit 0, exactly as S3's stamp claims |
| 🟢 confirmation | Every unit the `New units` row names is red under a mutation, and `c-8` is not vacuous | both test modules and `skills/verify/scripts/unverified_check.py` | confirmed | Executed, three mutations each applied alone and restored, tree clean after each. `test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in` (depth 1) reddens under reverting to the round-1 rule and under the unnarrowed rule. `c-8` reddens under the unnarrowed rule alone, which is the door it pins; it is green at `9e61df97` by construction and its proof is by mutation rather than by the old code, which is sound for a case pinning a direction. A third mutation — blanking nothing inside a span that holds the delimiter — reddens `c-7` instead, which is the neighbouring half |
| 🟢 confirmation | The five moved stamps are true at the stamped content | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:30` | confirmed | Opened all five and reconstructed the anchor hash at eight commits of this branch with the checker's own `resolve_unit` and `content_hash`. `settle.py#coordinates` is `315a83c0` from `281308c7` onward and was `a1c78799` at round 1's target, which is precisely what `round-1-report.md:192` claims. `folded_items` has been `7a8d3c99` since round 1's target and is unmoved. Executed: both ledger fragments report 0 drifted, 0 broken |
| 🟢 confirmation | The fold gate's failure-direction census reached everything | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Operational impact* | confirmed | Re-derived over the work item and the shipped files: `spec.md` G3, `plan.md` §*Operational impact*, `plan.md` §*What breaks in six months*, `overview.md`'s correction row and `blank_code_spans`'s docstring are the live sites, and all five state both halves. The phase records and round 1's records carry the superseded sentence as history, which is what a record is for (NAME NOT IN TREE) |
| ❓ out of verified scope | Whether the repository's full suite, `ruff check .` and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports the four narrow modules, the lint over the changed files, `evidence_check.py --strict .` and `survivor-check` as executed at or near this SHA; this round did not re-run them and does not certify them. The caller answers it |

## Paste-ready fixes

```python
# The opening delimiter of an HTML comment, and the only one `live_lines` asks
# `blank_code_spans` to look for. Its pair is a constant only because the pass
# has to know where a span's quotation STOPS: inside a parked draft the first
# closing delimiter really ends it, so an opener after that point is ordinary
# text and a real opener. Nothing blanks a closing delimiter — see
# `blank_code_spans`'s docstring for why a surviving one is the safe half.
OPENER = "<!--"
CLOSER = "-->"
```
```python
            else:
                # The DELIMITER, not the span around it — and only the
                # openers this span can still be quoting. The pass runs before
                # `comment_scan` and has no comment state, so it cannot know
                # whether these backticks are a code span at all. Inside a
                # parked draft they are not: the first closing delimiter ends
                # the draft, and an opener after it re-opens one. Blanking
                # that opener made a parked marker read as a fold record and
                # `settle --retire` removed the directory at exit 0 (round 3,
                # finding 1). Outside a draft the whole run really is a span
                # and the surviving opener parks the lines below it instead —
                # fewer lines live, a fold reported as a deletion, which is
                # the direction this module has already chosen to be wrong in.
                stop = span.find(CLOSER)
                stop = len(span) if stop == -1 else stop
                for m in re.finditer(re.escape(holding), span):
                    if m.end() <= stop:
                        chars[start + m.start() : start + m.end()] = " " * len(holding)
```
```python
def test_an_opener_after_a_quoted_closer_still_parks_the_marker_below(tree):
    """The residue of the shape above, in the expensive direction. The span
    pass has no comment state, so it cannot know that inside a parked draft
    the backticks are not a span at all: the first closing delimiter ends the
    draft and the opener after it re-opens one. Blanking that opener read a
    parked marker as a fold record, and `settle --retire` removed the
    directory at exit 0 with nothing having absorbed it. So the pass blanks
    only the openers a span can still be quoting — those before its first
    closing delimiter."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the span below ends it and re-opens it
        + "prose that quotes `--> and then <!--` on one line\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n"
        + "-->\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" not in rows.get("1700000002-beta", []), dict(rows)
```
```
    Deliberate, and non-decreasing against the unnarrowed rule — but not the
    HTML rule itself, which no state-free pass can be. Where a span quotes a
    closing delimiter and then an opening one, the HTML reading re-opens the
    draft and this pass does not read that far; it stops at the span's first
    closing delimiter and leaves the rest alone, which parks the marker
    instead. Fewer lines live is the direction this module is wrong in on
    purpose. `c-8` of
    `tests/test_unverified_rows_close.py#test_every_comment_shape_a_policy_document_can_carry`
    pins the gain and
    `tests/test_settle_reads_before_it_removes.py#test_an_opener_after_a_quoted_closer_still_parks_the_marker_below`
    pins the stop.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the two affected modules, pristine, in the clone | 177 passed, exit 0 |
| the corpus under four liveness rules — naive, blank-every-span, round 1's, shipped | 761 not live under all three span rules against the naive rule's 789; 0 lines disagree between shipped and either earlier rule |
| unique section ids in `seal/ledger.md` under the shipped rule against the fence-only reading | 83 and 83, from 94 marker occurrences |
| the three named markers, by id, through the shipped rule | live at `seal/ledger.md` lines 767, 992 and 1619 |
| `bin/settle --root .` in the clone | `released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped`, exit 0 |
| fifteen adversarial span shapes — shipped against blank-every-span against round 1's rule against a character-by-character HTML reading | fourteen agree with HTML; the closer-then-opener shape reads live where HTML parks |
| a 40,000-document fuzz over comment delimiters and backtick runs, shipped against the HTML reading | 5 lines live where HTML parks, 0 lines parked where HTML reads live; all 5 are finding 1's class |
| the same fuzz with the paste-ready fix applied | 0 live where HTML parks, 40 parked where HTML reads live — the cheap direction |
| `folded_items` and `settle --retire` over finding 1's fixture, at `9e61df97` and at the target, on a throwaway git repository | `set()` / exit 1 *nothing to retire* against `{'1700000042-quoted'}` / exit 0 `removed seal/specs/1700000042-quoted/` |
| the same fixture with the paste-ready fix applied | exit 1 *nothing to retire*, directory kept |
| the paste-ready fix against the two modules and the corpus | 177 passed exit 0; 761 / 83 unchanged; the three markers still live |
| three mutations, each applied alone and restored, against the named units | round-1 rule → the new unit red alone; unnarrowed rule → the new unit, `test_a_closer_quoted_in_prose_still_closes_a_parked_draft` and `c-8` red; blank nothing in a holding span → `c-7` red |
| the span pass composed into `readable()`, `tests/test_chain_hooks.py` | 2 failed, exit 1 — `test_a_closing_word_a_reader_blanks_is_not_a_closing_note` at both parametrisations |
| the anchor hash of `settle.py#coordinates` and `unverified_check.py#folded_items` at eight commits of this branch | `73b46b7e` → `a1c78799` → `661d041f` → `315a83c0`; `folded_items` `7a8d3c99` throughout since round 1's target |
| `evidence-check --strict .` in the clone with `round-1-report.md:191` reverted to `661d041f` | DRIFTED at that line, exit 2 — a report's stamp is read as a live claim |
| the two ledger fragments through `evidence-check --ledger … --strict` | 18 ok and 13 ok, 0 drifted, 0 broken, exit 0 |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it, and what stands between it and the spawn is finding 1 and finding 2 |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A comment delimiter inside a code span that crosses a line break | already deferred in round 1, finding 2, to `overview.md` §*Not done* and the docstring's dated census | the same, and this round agrees with the decision |
| Markdown's indented code block as a third quotation | already deferred in round 1, finding 3, to `settle.py#coordinates`'s docstring and `test_an_indented_example_row_is_counted_and_the_reader_says_so` | the decision stands; round 2 corrected the one false ground in it and this round confirms the correction |
| `evidence_check.py`'s own readers are the same class one module over | already deferred in round 1 to `seal/follow-up.md`, two rows, and before that by `spec.md` §*Scope*, Out | the answerers those rows already name |
| `.github/scripts/fold_ledger.py#demote`'s fence tracking | already deferred in `spec.md` §*Scope*, Out — not shipped, and its own rider says what it misreads | the same, unchanged by this round |
| A stamp quoting a past state has no way to say so, so every move of the unit rewrites the records | ⬜ 4 above proposes `seal/follow-up.md` | not this branch's — the orchestrator decides where it lands |
