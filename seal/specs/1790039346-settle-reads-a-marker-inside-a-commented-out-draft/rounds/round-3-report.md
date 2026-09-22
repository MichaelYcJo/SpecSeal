# Round 3 — the verifying round, against the diff of round 2's fixes

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

Target SHA `66dca36133d1b4cb589b7880a2602ddc385daaa3`, branch
`fix/489-settle-reads-a-marker-inside-a-commented-out-draft`, base
`origin/release/v0.13.0` at `3cdfd8ad`, PR 490. Fix range
`9e61df979b8793fa3f620e4e1840a54c8aaca0b1..68a023af504e0dd14a02656952af36b9e7e94300`.

Round 2's `Fixes checked by` read *nobody*. It reads somebody now. All three
of round 2's verdicts are closed on their own terms, and the round that closed
them opened one more.

## How the findings hang together

The third formulation of the span rule fixed the shape round 2 named and took
one further shape with it, in the direction this work item exists to prevent.

```
round 1  blank every span                  a quoted closer was lost
   ↓ narrowed
round 1's fix   blank the span HOLDING an opener    a quoted whole comment
                                                    lost its closer  (round 2's finding 2)
   ↓ narrowed again
round 2's fix   blank the opener OCCURRENCES        an opener that FOLLOWS a
                inside the span                     closer in the same span is
                                                    blanked too — and inside a
                                                    parked draft that opener is
                                                    real  (finding 1 below)
```

Finding 2 is the sentence finding 1 falsifies: four live documents now declare
the new direction and each one grounds it on *this is what the HTML rule says*.

---

## 🔴 1 · A span holding a closer and then an opener retires a directory nothing absorbed

`skills/verify/scripts/unverified_check.py:326-336` — `blank_code_spans`, (NAME NOT IN TREE)
the `else` arm added at `281308c7`.

The arm blanks **every** occurrence of the opener inside the span:

```python
            else:
                for m in re.finditer(re.escape(holding), span):
                    chars[start + m.start() : start + m.end()] = " " * len(holding)
```

The span pass runs before `comment_scan` and carries no comment state, so it
cannot know whether the backticks it is looking at are a code span at all.
When the line begins **inside** a parked draft they are not: inside an HTML
comment nothing is markdown, the first closing delimiter really does end the
draft, and whatever follows it on the line is ordinary text. An opener sitting
there is a real opener — and this arm has just blanked it.

**What goes wrong.** A parked draft, one line of prose that quotes a closing
delimiter and then an opening one, a real section marker under it:

```
<!-- a parked draft
prose `--> and <!--` here
<!-- specs/1700000042-quoted -->
still parked
-->
```

Read as HTML, the draft ends at the first closing delimiter on line 2, the
opening delimiter after it re-opens the draft, and line 3's marker is inside
it — not a fold record. The shipped pass blanks that second delimiter, so
nothing re-opens, line 3 reads live, and the marker becomes a fold record.

**Executed**, on a throwaway repository, against the fix range's two ends:

| | `9e61df97` (round 2's record) | `66dca361` (target) |
|---|---|---|
| `folded_items` | `set()` | `{'1700000042-quoted'}` |
| `settle --retire` | exit 1, *nothing to retire* | **exit 0, `removed seal/specs/1700000042-quoted/`** |

That is a work item's whole SDD set removed at exit 0 with nothing having
absorbed it — the outcome `plan.md` §*What breaks in six months* names as the
expensive one and `spec.md` G3 declares cannot happen.

**It is new in this fix range.** The same fixture at round 1's rule (blank the
whole span that holds an opener) and at the unnarrowed rule (blank every span)
both park the marker. Round 2's fix is what opened it.

**The class, enumerated.** Not the coordinate: the class is *a span whose
blanked opener would have re-opened a comment that a surviving closer in the
same span closed*. Fuzzed over 40,000 generated documents against a
character-by-character HTML reading, the shipped rule answers **live where
HTML parks** on 5 lines and **parks where HTML reads live** on 0. Every one of
the 5 is this shape. The corpus is clean today: over `seal/ledger.md`, every
`seal/ledger/*.md` fragment and every top-level `docs/` document, 0 lines
answer differently from the rule that blanked every span, so no instance
exists in the tree — the same standing round 2's own finding 2 had.

**The fix cannot be exact, and the choice is which way to be wrong.** With no
comment state the two readings genuinely conflict: outside a draft the whole
run is a code span and both delimiters are inert, inside a draft neither is.
The repository has already decided which mistake is cheaper — *fewer lines
live, a fold reported as a deletion* — so the opener after a closer is left
where it stands. Fuzzed, that rule answers live-where-HTML-parks on **0**
lines and parks-where-HTML-reads-live on 40, which is the cheap direction by
the project's own reckoning.

Executed with the fix below: the reproduction goes back to exit 1 *nothing to
retire*, `bin/test tests/test_settle_reads_before_it_removes.py
tests/test_unverified_rows_close.py -q` gives 177 passed exit 0, and the
corpus is unmoved at 761 not-live lines with the three named markers live.

---

## 🟡 2 · Four live documents ground the new direction on the HTML rule, and one shape does not obey it

`skills/verify/scripts/unverified_check.py:284-296` ·
`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39`
(G3) · `…/plan.md:195` §*Operational impact* · `…/overview.md:44`.

All four state the same thing, in the docstring's words:

> A span the predicate spares cannot hold an opener, so the only delimiter it
> can restore is a closing one, and a closing one can only end a comment
> sooner: liveness is monotonically non-decreasing … That is what the HTML
> rule says and it is deliberate.

Two halves, and only the first survives.

- **Monotonic non-decrease is true.** Every opener inside every span is
  blanked under both the shipped rule and the unnarrowed one, and the shipped
  rule additionally spares closers. More closers can only end comments sooner.
  Re-derived, and the corpus agrees on every line.
- **HTML-faithful is false.** The reasoning is about a span the predicate
  *spares*; the change in this fix range is about spans it does **not** spare,
  and there the surviving closer is not inert. Finding 1 is the shape.

The distinction matters because the direction is what a maintainer is told to
trust. `spec.md` G3 is the clause that judges the build, and its sentence
*It is deliberate and faithful to the HTML rule* is the one thing in it that
the code does not support. The rest of G3 holds: the red case, the prompt
budget of zero and the platform-honesty line are each true, and the four items
`CONTRIBUTING.md` §*What a change to a gate must carry* asks for are all
present rather than waved at. It judges the build; it does not excuse it.

The sentence needs an edit whichever way finding 1 is answered, because the
fix above is deliberately *not* HTML-faithful either — it is faithful to the
cheaper mistake.

---

## ⬜ 3 · The `OPENER` constant's comment no longer describes what the module does

`skills/verify/scripts/unverified_check.py:107-110`:

> Its pair, the closing delimiter, is deliberately NOT a constant here and no
> reader of this module blanks a span that holds one.

After `281308c7` the pass writes into a span that holds a closing delimiter —
it blanks the opener beside it. The sentence reads as a promise that such a
span is untouched, and the fix for finding 1 has to add the closing delimiter
as a constant, which the comment forbids in as many words. Both halves are
carried in the paste-ready fix below.

---

## ⬜ 4 · A stamp on a record of a past state is read as a live claim, and this is its third rewrite

`…/rounds/round-1-report.md:191` · `…/rounds/round-2-report.md:266` ·
`…/rounds/round-2-report.md:310` · `…/rounds/round-2.md:61` ·
`…/spec.md:30`.

This is an observation for the record, not a fix to commission.

`skills/settle/scripts/settle.py#coordinates` has hashed four values on this
branch, and three of them have been written into the records:

| | `coordinates` anchor |
|---|---|
| base `3cdfd8ad` | `73b46b7e` |
| round 1's target `7db75512` | `a1c78799` |
| round 1's fix tip `6d8ebaae` — and round 2's target `7f2d6f1c` | `661d041f` |
| round 2's fix pass `281308c7` onward | `315a83c0` |

Every claim at the five sites is true at the stamped content, and I checked
each: round 1's report says the row read `a1c78799` when round 1 read it,
which is exactly the value at round 1's target SHA; round 2's report says the
pair appears byte-identical in the parent's fragment, this work item's
fragment, `spec.md` and the report, and it does; `spec.md:30` names the two
parent rows and both sit where it says.

**The rewrites are forced, not optional.** Executed: putting `661d041f` back
into `round-1-report.md:191` makes `evidence-check --strict .` report
`DRIFTED … round-1-report.md:191 settle.py#coordinates content changed` and
exit 2. So the evidence arm reads a stamp in a round report as a live claim.

**The cost is the thing worth recording.** `round-2.md` carries
`Target SHA | 7f2d6f1c` and a stamp of `315a83c0`, a value that did not exist
at that SHA. A record of what a round read now states a value the round could
not have read. Round 1's report says so in its own next clause, which is the
honest shape available — but the shape exists only because the checker has no
way to say *this coordinate is quoted as history*. The next edit to
`coordinates` makes it a fourth pass over five files. A home for that decision
is `seal/follow-up.md` rather than this branch.

---

## What was verified and what was not

**Executed** — all of it in a `git clone --no-local` at the target SHA, never
in the working tree:

- The two affected modules, pristine: 177 passed, exit 0.
- The corpus under four liveness rules; four mutations against the named
  units; the fence-reader and `readable()` widenings; the 40,000-document
  fuzz; the end-to-end `settle --retire` fixtures at two SHAs; the reverted
  stamp against `evidence-check`.

**Read** — the five stamp sites and their claims, `spec.md` G3 against
`CONTRIBUTING.md` §*What a change to a gate must carry*, the two censuses,
round 1's and round 2's records and reports.

**Unverified** — the repository's full suite, the repository-wide lint and the
typecheck. §2 gives those to the sealer and this definition hands me none of
them. The orchestrator reports the four narrow modules (334 passed, exit 0),
`ruff check` over the four changed files (exit 0), `evidence_check.py
--strict .` (exit 0, 0 drifted) and `survivor-check` (exit 0) as executed at
or near this SHA; this round did not re-run them and does not certify them.
The caller answers it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A span holding a closer and then an opener has the opener blanked, so a marker inside a parked draft reads as a fold record and `settle --retire` removes the directory at exit 0 with nothing having absorbed it | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | New at `281308c7`. Executed: `folded_items` answers `set()` at `9e61df97` and `{'1700000042-quoted'}` here, and `settle --retire` goes from exit 1 *nothing to retire* to exit 0 `removed seal/specs/1700000042-quoted/`. Both earlier formulations park the marker. Fuzzed over 40,000 documents against a character-by-character HTML reading, the shipped rule reads live where HTML parks on 5 lines and parks where HTML reads live on 0; all 5 are this class. No instance in the corpus today — 0 lines answer differently from the rule that blanked every span. The run is capped, so this is a `deferred #N` candidate rather than a fix to commission |
| 2 | 🟡 The docstring, `spec.md` G3, `plan.md` §*Operational impact* and `overview.md` each ground the new direction on *that is what the HTML rule says*; the reasoning covers only the spans the predicate spares, and the change in this range is about the spans it does not | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | Read, and re-derived: monotonic non-decrease against the unnarrowed rule holds — every opener inside every span is blanked under both and the shipped rule additionally spares closers — but HTML-faithfulness does not, for finding 1's shape. The sentence needs an edit whichever way finding 1 is answered, because the paste-ready fix is faithful to the cheaper mistake rather than to HTML. G3's other three items are true and it judges the build rather than excusing it |
| ⬜ 3 | The `OPENER` constant's comment says no reader of the module blanks a span holding a closing delimiter, and one now writes into such a span | `skills/verify/scripts/unverified_check.py:107-110` | open | Read. The comment also forbids the closing delimiter as a constant, which finding 1's fix requires. Carried in the paste-ready fix below |
| ⬜ | A stamp on a round report is read as a live claim, so one coordinate has been rewritten three times across five files, and a record now states a value that did not exist at its own `Target SHA` | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | confirmed | Executed: reverting `round-1-report.md:191` to `661d041f` makes `evidence-check --strict .` report DRIFTED at exit 2, so the rewrite is forced rather than chosen. The observation the prompt asked for: a stamp quoting history has no way to say so. A home for the decision is `seal/follow-up.md`, not this branch |
| 🟢 confirmation | Round 2's finding 1 is closed — the direction is declared in every live site and pinned | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Read all five declaring sites — the docstring, `spec.md` G3, `plan.md` §*Operational impact* and §*What breaks in six months*, `overview.md`'s correction row — and each states both halves. Executed: `c-8` is red under the unnarrowed rule and green under both the round-1 and shipped rules, so it pins the direction round 1's predicate bought. The disclosure and the pin are what the fix owed, and both landed. What finding 2 above opens is one clause inside them, not their absence |
| 🟢 confirmation | Round 2's finding 2 is closed — a span quoting a complete comment keeps its closer | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Executed: `test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in` is red under the round-1 rule (blank the whole span that holds an opener) and under the unnarrowed rule, green as shipped. The fixture's marker is HTML-correct — inside a draft the quoted closing delimiter really does end it. The residue finding 1 names is one delimiter further along the same span, not this shape |
| 🟢 confirmation | Round 2's finding 3 is closed — all three false grounds corrected, and the census of eleven holds | `skills/settle/scripts/settle.py#coordinates` | **fixed**, verified | Re-derived the census rather than carrying it: eleven citations of `reader_blanking_passes` outside past work items' records. Three asserted it refuses a widened fence reader — `settle.py#coordinates`'s docstring, `test_an_indented_example_row_is_counted_and_the_reader_says_so`, and `overview.md:87` — and all three now name `test_a_continuation_that_looks_like_an_opener_is_still_joined` instead. Eight assert it refuses a pass added to `readable`; Executed, that is true: composing the span pass into `readable()` reddens `test_a_closing_word_a_reader_blanks_is_not_a_closing_note` at both parametrisations, 2 failed exit 1 |
| 🟢 confirmation | The corpus invariant survives the third formulation | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed over `seal/ledger.md`, every `seal/ledger/*.md` fragment and every top-level `docs/` document: 761 not-live lines against the naive rule's 789; 94 live marker occurrences and **83** unique section ids, the same 83 the fence-only reading gives; the three named markers live at `seal/ledger.md` lines 767, 992 and 1619; and **0** lines answering differently from the rule that blanked every span or from round 1's rule. `bin/settle` prints `released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped` at exit 0, exactly as S3's stamp claims |
| 🟢 confirmation | Every unit the `New units` row names is red under a mutation, and `c-8` is not vacuous | both test modules and `skills/verify/scripts/unverified_check.py` | confirmed | Executed, three mutations each applied alone and restored, tree clean after each. `test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in` (depth 1) reddens under reverting to the round-1 rule and under the unnarrowed rule. `c-8` reddens under the unnarrowed rule alone, which is the door it pins; it is green at `9e61df97` by construction and its proof is by mutation rather than by the old code, which is sound for a case pinning a direction. A third mutation — blanking nothing inside a span that holds the delimiter — reddens `c-7` instead, which is the neighbouring half |
| 🟢 confirmation | The five moved stamps are true at the stamped content | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:30` | confirmed | Opened all five and reconstructed the anchor hash at eight commits of this branch with the checker's own `resolve_unit` and `content_hash`. `settle.py#coordinates` is `315a83c0` from `281308c7` onward and was `a1c78799` at round 1's target, which is precisely what `round-1-report.md:192` claims. `folded_items` has been `7a8d3c99` since round 1's target and is unmoved. Executed: both ledger fragments report 0 drifted, 0 broken |
| 🟢 confirmation | The fold gate's failure-direction census reached everything | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Operational impact* | confirmed | Re-derived over the work item and the shipped files: `spec.md` G3, `plan.md` §*Operational impact*, `plan.md` §*What breaks in six months*, `overview.md`'s correction row and `blank_code_spans`'s docstring are the live sites, and all five state both halves. The phase records and round 1's records carry the superseded sentence as history, which is what a record is for (NAME NOT IN TREE) |
| ❓ out of verified scope | Whether the repository's full suite, `ruff check .` and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports the four narrow modules, the lint over the changed files, `evidence_check.py --strict .` and `survivor-check` as executed at or near this SHA; this round did not re-run them and does not certify them. The caller answers it |

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

## Paste-ready fixes

Finding 1, with finding 3's comment carried in the same patch. Replace the
`OPENER` constant's comment block:

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

and the `else` arm of `blank_code_spans`: (NAME NOT IN TREE)

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

The regression case, for `tests/test_settle_reads_before_it_removes.py`
beside `test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in`. Red
against the shipped arm — the row lands under `1700000002-beta` — and green
with the patch above:

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

Finding 2, the clause in `blank_code_spans`'s docstring. Replace *That is what (NAME NOT IN TREE)
the HTML rule says and it is deliberate* with:

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

`spec.md` G3, `plan.md` §*Operational impact* and `overview.md:44` each carry
the same clause and each needs the same correction: *faithful to the HTML
rule* becomes *non-decreasing against the unnarrowed rule, and wrong toward
fewer lines live where no state-free pass can be right*.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A comment delimiter inside a code span that crosses a line break | already deferred in round 1, finding 2, to `overview.md` §*Not done* and the docstring's dated census | the same, and this round agrees with the decision |
| Markdown's indented code block as a third quotation | already deferred in round 1, finding 3, to `settle.py#coordinates`'s docstring and `test_an_indented_example_row_is_counted_and_the_reader_says_so` | the decision stands; round 2 corrected the one false ground in it and this round confirms the correction |
| `evidence_check.py`'s own readers are the same class one module over | already deferred in round 1 to `seal/follow-up.md`, two rows, and before that by `spec.md` §*Scope*, Out | the answerers those rows already name |
| `.github/scripts/fold_ledger.py#demote`'s fence tracking | already deferred in `spec.md` §*Scope*, Out — not shipped, and its own rider says what it misreads | the same, unchanged by this round |
| A stamp quoting a past state has no way to say so, so every move of the unit rewrites the records | ⬜ 4 above proposes `seal/follow-up.md` | not this branch's — the orchestrator decides where it lands |

Needs a fix: yes — finding 1, a marker inside a parked draft read as a fold record so `settle --retire` removes the directory at exit 0, new at `281308c7`; and finding 2, the clause four live documents ground that direction on. The run is capped, so both are `deferred #N` candidates rather than fixes to commission.
Loses a record or crashes: yes — finding 1, a work item's SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway repository at both ends of the fix range.

## Proof block

Files opened: `skills/verify/scripts/unverified_check.py`,
`skills/settle/scripts/settle.py`,
`skills/evidence-check/scripts/evidence_check.py`,
`tests/test_settle_reads_before_it_removes.py`,
`tests/test_unverified_rows_close.py`, `tests/test_chain_hooks.py` (by name
only, through its cases), `CONTRIBUTING.md`, `CLAUDE.md`, `seal/config.md`,
`seal/ledger.md`, `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`,
`seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`,
and, under
`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/`:
`spec.md`, `plan.md`, `overview.md`, `questions.md`, `survivors.md`,
`rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-2.md`,
`rounds/round-2-report.md`.

Every command ran in a `git clone --no-local` of this repository at
`66dca36133d1b4cb589b7880a2602ddc385daaa3`. Probe files were named
`test_tmp_*`, ran once, and are deleted; the clone and its virtualenv go with
this round. Nothing was written, committed, pushed or posted in the working
tree except this report.
