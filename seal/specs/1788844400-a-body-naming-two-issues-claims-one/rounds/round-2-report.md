# Round 2 — the verifying round over `2fae791..8f09a77`

Round 1 recorded seven verdicts: five fixed, one answered, one deferred. This
round opened the fix range and asked, for each, whether the finding is closed
rather than whether a change was made. It also judged the nine test functions
the fixes added, which nobody has reviewed.

**All seven are closed.** Nothing in the range needs a fix, and nothing in it
loses a record or crashes. What the round did find is three record and
document corrections, none of which changes what the release ships.

## How the parts relate

The five code fixes sit in two disjoint regions of one module, and the review
splits along that seam.

- `9dc02ac` widened `BLOCK_START` so a thematic break ends a segment, and
  reworded the document that teaches the rule so the document stops being an
  instance of it. Findings 1, 2 and 3 hang off that commit.
- `b5945dc` strengthened the one case that was itself defective when written.
- `7da891e` added the per-number `seen` set in `read()`, closing findings 6
  and 7 — the two the fixer was not commissioned to touch.
- `5bec650` and `8f09a77` are record work: the answerer split in `overview.md`,
  and two content anchors in the ledger fragment.

The three corrections this round opens are all paperwork, and they are
independent of each other.

---

## The five `fixed` rows are closed, and each is pinned by a case that goes red

I did not take the fixer's mutation numbers. I re-ran every one of them and
added the ones the record did not claim, clearing both `tests/__pycache__` and
`.github/scripts/__pycache__` between each. Every one of the nine new units
goes red under a mutation aimed at the behaviour it names — the full table is
under *Executed probes*.

**Finding 1 — the thematic break.** `BLOCK_START` at
`.github/scripts/issue_claims_check.py:116` gained four whole-line
alternatives. Removing all four turns
`test_a_horizontal_rule_ends_the_segment` red at all four of its shapes, so
the case genuinely pins the widening rather than passing beside it. The
widening does not open a false-negative door: a line of one `-` was already a
list marker, `a --- b` and `-x` are rejected at the marker level, and `#22` at
the start of a line — the shape the module exists to see — matches none of the
four.

**Finding 2 — the document that taught the rule broke it.** The acceptance run
now reports `claimed: none`, seven mentioned numbers, and the no-warning line,
at exit 0. Reverting the one narration sentence in
`docs/issues-and-milestones.md` back to its pre-fix wording turns
`test_the_document_that_teaches_the_rule_carries_no_instance_of_it` red, so
the case observes the document rather than merely reading it.

**The move of #153 from claimed to mentioned is the right outcome, not a step
too far.** The section's teaching is carried by three code spans, and all
three survive: the failing shape itself, the corrected form, and the statement
that a fenced or spanned quotation is not an instance. What the fix reworded
is the narration of what happened at the 0.8.0 release, which is history
rather than teaching. Nothing in the paragraph's subject required the prose to
use the verb, and the check reading the document as `claimed: none` costs
nobody anything — the document is not a pull request body, and only the case
reads it that way.

**The paragraph the fixer added holds.** It asserts that a past-tense
narrative keyword is still a keyword. `KEYWORDS` in
`close_issues_on_release.py:49` carries `closed`, `fixed` and `resolved`
alongside the present tense, and `CLOSING` is built from that tuple
case-insensitively, so the assertion is true of the code the check imports.
The paragraph is also the only place in the tree that states the rule for
prose rather than for spans, which is the gap round 1 named.

**Finding 3 — the four strings a person reads.** All four are now pinned
independently. Dropping the `::warning::` prefix, rewording either list line,
and deleting the clean-body line each turn exactly one case red and leave the
rest green, which is what §14 asks for. The fixer also improved on the
paste-ready form: round 1's snippet used a nested-tuple unpacking to assert
"exactly one annotation", and the committed version uses an explicit length
assertion with the captured lines as the failure message. Same guarantee,
readable failure.

**Findings 6 and 7 — the per-number set.** Removing the `seen` membership test
turns `test_the_same_number_twice_in_one_sentence_is_one_warning` red.
Hoisting `seen` out of the segment loop turns
`test_the_same_number_in_two_sentences_earns_a_warning_each` red — I had to
run this twice, because my first attempt added a second `seen` rather than
moving the existing one and proved nothing. The corrected mutation kills the
case. The interaction with the nearest-claim rule is sound: `seen.add` sits
inside `if before:`, so a number appearing before the claim is not consumed
and still earns its warning when it reappears after one.

## `7da891e` was outside the commission, and taking it was the right call

The fixer's grounds are that `seal/follow-up.md` sends a coordinate-bound item
to a `# RIDER:` comment at the line rather than into that file, so deferring
findings 6 and 7 would have cost two riders plus two verification stamps. I
read `seal/follow-up.md` and it says exactly that, in its third rule. The cost
comparison is therefore factual rather than a preference.

The commit is clean on all three claims the fixer made for it.

- **It reverts alone.** `git revert --no-commit 7da891e` applies without
  conflict against the target, and the reverted tree runs 46 passed — exactly
  the 49 minus its own three cases, with nothing else going red.
- **Its hunks do not overlap the others.** It touches the inner segment loop
  of `read()`; `9dc02ac` touches the module docstring and `BLOCK_START`. The
  two regions are disjoint.
- **It adds no mechanism beyond one set.** The diff adds `seen = set()`, one
  membership test and one `seen.add`. There is no new function, constant or
  branch.

## The `answered` row is genuinely answered, and the two moved rows genuinely cannot be

Round 1's finding 4 was that `overview.md` named CI as the answerer for two
facts that run cannot settle. `5bec650` split the row into three.

The row it closed — that the step behaves on a real runner at all — is settled
by the run at `38cea82`, which round 1 measured through `gh pr checks` and the
check-run annotations API: the step ran first in the job, printed both lists,
and exited 0. That is the whole of what the row claims, so the ✅ is earned.

The two it moved to the repository owner cannot be answered by any run of this
pull request, for the reason the rows now state. The annotation row needs a
body that carries the warning shape, and #261's body claims one number and
names none beside it. The empty-body row needs a pull request with no
description, and #261 has one. Neither is a fact a rerun would produce.

**The shape is the sanctioned one, not an improvisation.**
`skills/verify/scripts/unverified_check.py` defines `CLOSED` as the ✅ marker
and reads a marked row as closed, which I confirmed by running it: the work
item reports 4 open · 1 closed, and the two moved rows appear as open against
the repository owner. A reader and the tool agree on the record.

## The deferred row's reasoning is right and its home is not

Round 1 deferred finding 5 — whether `FENCE` and `SPAN` should cover tilde
fences, indented blocks, fences inside list items, HTML comments and
double-backtick spans. **The reason for deferring holds.** Those two patterns
are imported from `close_issues_on_release.py`, so widening them changes what
a release closes and not only what this check reports. That is a different
change with a different blast radius, and it does not belong in this branch.

**Where it went is the problem.** The verdict cell reads `deferred` followed by
this round record's own path, and the record's Deferred table answers "where it
went" with "finding 5 above". Each cell points at the other, so the pair names
no destination outside the file. `docs/review-chain-spec.md:177` gives one home
for a finding neither fixed nor answered — `seal/follow-up.md`, named in the
pull request body — and `seal/follow-up.md` in turn sends anything tied to a
coordinate to a `# RIDER:` comment at that line. Finding 5 is tied to two
coordinates.

Nothing reads a round record's Deferred table looking for open work.
`unverified_check.py` reads `## Not verified` sections in overviews;
`grep -rn "RIDER:"` is the repository-wide list of coordinate-bound items;
`fold_ledger.py --check` reads `evidence-todo.md`. A round record is read by
the next round of the same run, and this run ends here.

`chain_check.py` will not catch it. Its own docstring at line 1378 says the
check on a `deferred` verdict is "the only thing: is there anything after it",
so a self-referential home passes. That shallowness is deliberate — it is why
the verifying round is the one that looks at the home.

## Two smaller corrections in what the fixes wrote

**The plan's caveat still stops short of the behaviour.** Round 1's finding 7
named `plan.md`'s bullet as the thing that describes the URL-fragment case in
terms of the mention list alone. The fix put the reasoning in a code comment
at `.github/scripts/issue_claims_check.py:224` and pinned the behaviour with a
case, and I judge the finding closed on that: the code comment is where the
behaviour durably lives, and the bullet's closing sentence is still literally
true. But a reader of `plan.md` alone learns that a fragment lands in the
mention list and does not learn that one beside a claim earns a warning.

**A pointer in the new document paragraph lands on the wrong paragraph.** The
paragraph added at `docs/issues-and-milestones.md:130` says "the paragraph
above says a release *acted on* one number". The paragraph immediately above
it is the one about the hygiene workflow reporting the split; the paragraph
that says "acted on" is three blocks up. A reader checking the claim looks in
the wrong place.

## What was carried rather than re-derived

Round 1's coordinates for all seven findings, and the orchestrator's executed
facts for the target SHA. Every verdict below is my own.

The orchestrator's carried refusal is unchanged and did not widen: the narrowed
ledger check reports 9 ok · 0 drifted · 0 broken, and the records arm still
refuses exactly one line — `round-1-report.md:228`, for a name the fixes
deleted (`claimed_at` — NAME NOT IN TREE). No file the fix range touches adds
another.

## Out of verified scope

The full suite, the repository-wide lint and the typecheck. `agent-contract`
§2 forbids them to this round; I ran the changed module and three siblings
narrow, and `ruff` on the two changed `.py` files only. The prompt narrowed my
scope rather than widening it, and I followed it. **Answerer: the review
orchestrator, once the rounds settle.**

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A thematic break or setext underline was not a segment boundary | `.github/scripts/issue_claims_check.py:116` | answered | Closed. Executed: removing the four whole-line alternatives turns `test_a_horizontal_rule_ends_the_segment` red at all four shapes; the widening opens no false negative — `#22` at line start matches none of the four |
| 2 | The section teaching the rule wrote the failing shape in bare prose | `docs/issues-and-milestones.md:117` | answered | Closed. Executed: the acceptance run over that document reports `claimed: none` and the no-warning line at exit 0; reverting the narration sentence turns `test_the_document_that_teaches_the_rule_carries_no_instance_of_it` red. The teaching survives in three code spans, and the added paragraph's premise is true — `KEYWORDS` carries `closed`, `fixed`, `resolved` |
| 3 | Nothing pinned the four strings the check prints | `.github/scripts/issue_claims_check.py:240` | answered | Closed. Executed: dropping the `::warning::` prefix, rewording either list line, and deleting the clean-body line each turn exactly one case red. The committed assertion improves on the paste-ready form's nested unpacking |
| 4 | Two facts the record handed to CI are not answerable by that run | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/overview.md:27` | answered | Closed. The ✅ row is earned by the measured run at `38cea82`; the two moved rows need a body carrying the warning shape and a pull request with no description, neither of which #261 is. Executed: `unverified_check.py` reads the record as 4 open · 1 closed, and ✅ is its own `CLOSED` marker |
| 5 | The masking gives up four well-formed shapes the plan does not enumerate | `.github/scripts/issue_claims_check.py:130` | answered | The deferral reasoning is right and unchanged — `FENCE` and `SPAN` are imported, so widening them changes what a release closes. `prose_only` is untouched by the fix range. The home is wrong, and that is row 8 |
| 6 | A repeated unclaimed number printed the identical annotation twice | `.github/scripts/issue_claims_check.py:229` | answered | Closed. Executed: removing the `seen` membership test turns `test_the_same_number_twice_in_one_sentence_is_one_warning` red. `seen.add` sits inside `if before:`, so a number appearing before the claim is not consumed |
| 7 | A numeric URL fragment beside a claim earns a warning; the caveat named only the mention list | `.github/scripts/issue_claims_check.py:224` | answered | Closed on the code comment plus `test_a_numeric_url_fragment_beside_a_claim_is_a_warning`. Executed: adding the rejected URL-character exclusion turns that case red, so the chosen behaviour is pinned rather than merely current. The plan bullet is row 9 |
| 8 | ⬜ The deferred finding's home is the round record's own Deferred table, and the two cells point at each other rather than at a destination | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/rounds/round-1.md` §Deferred | open | Record correction, not a code defect. `docs/review-chain-spec.md:177` gives `seal/follow-up.md` named in the pull request body; `seal/follow-up.md` sends a coordinate-bound item to a `# RIDER:` comment instead, and this one is tied to `FENCE` and `SPAN`. Nothing reads a round record's Deferred table for open work, and `chain_check.py:1378` checks only that something follows the word |
| 9 | ⬜ `plan.md`'s caveat still describes the URL fragment in terms of the mention list alone | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/plan.md:81` | open | Record correction. The bullet's closing sentence is literally true and the behaviour lives durably in the code comment, so finding 7 is closed — but a reader of the plan alone does not learn that a fragment beside a claim earns a warning |
| 10 | ⬜ The added paragraph's "the paragraph above" points at the wrong paragraph | `docs/issues-and-milestones.md:130` | open | Document correction. The paragraph immediately above is the hygiene-workflow one; the paragraph that says *acted on* is three blocks up. Behaviour and fact are right, so the release ships nothing defective |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_a_body_naming_two_issues_claims_one.py -q` in a fresh `--no-local` clone at `5f2a18c` | 49 passed, exit 0 |
| `python3 .github/scripts/issue_claims_check.py --body-file docs/issues-and-milestones.md` | `claimed: none` · `mentioned only: #179, #155, #153, #162, #150, #136, #30` · `no sentence claims one number and names another beside it` · exit 0 — the fixer's account reproduced |
| Mutation: drop the `$` anchor from each of the four whole-line alternatives, one at a time, both `__pycache__` directories cleared between | each turns `test_a_run_of_markers_inside_a_line_is_still_prose` red; the `=` alternative turns it red at two parameters. The strengthened case reaches the anchor |
| Reach analysis: which of that case's ten parameters match the pattern with `\r*$` removed | five reach the anchor (`--- not a rule`, `*** not a rule`, `___ not a rule`, `=== not an underline`, `= x`); the other five are rejected at the marker level, as the case's own comment states |
| Mutation: remove all four whole-line alternatives from `BLOCK_START` | `test_a_horizontal_rule_ends_the_segment` red at all four shapes |
| Mutation: remove the `seen` membership test | `test_the_same_number_twice_in_one_sentence_is_one_warning` red |
| Mutation: hoist `seen` out of the segment loop — run twice, the first attempt added a second set rather than moving it and survived | corrected mutation turns `test_the_same_number_in_two_sentences_earns_a_warning_each` red |
| Mutation: add the rejected alternative, excluding a `#N` preceded by a non-space character | `test_a_numeric_url_fragment_beside_a_claim_is_a_warning` red |
| Mutation: drop the `::warning::` prefix · reword the claimed list · reword the mentioned list · delete the clean-body line | one case red each, and only one: the annotation case, the two-lists case twice, the clean-body case |
| Mutation: restore the pre-fix narration sentence in `docs/issues-and-milestones.md` | `test_the_document_that_teaches_the_rule_carries_no_instance_of_it` red |
| `git revert --no-commit 7da891e` against the target, then the module | applies without conflict; 46 passed, exit 0 — its own three cases and nothing else |
| `git show --stat` on `9dc02ac`, `b5945dc`, `7da891e` | the regions are disjoint: `7da891e` is inside `read()`'s segment loop, `9dc02ac` is the docstring and `BLOCK_START` |
| `python3 skills/verify/scripts/unverified_check.py` on the work item | exit 0 · 4 open · 1 closed; the ✅ row reads closed and the two moved rows name the repository owner |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict --ledger seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md .` | 9 ok · 0 drifted · 0 broken; records arm refuses exactly one line, `round-1-report.md:228`, unchanged from the orchestrator's carried reading |
| `uvx ruff check` and `uvx ruff format --check` on the two changed `.py` files | exit 0 each — all checks passed, 2 files already formatted |
| `./.venv/bin/python -m pytest tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_release_hygiene.py -q` | 51 passed, exit 0 |
| `deferral_check.py . --kind all` at the branch and at `bcf48b8` | identical at both: tests and lint resolve, typecheck does not. Pre-existing and outside this range. My first run of it was mis-scoped to the work item directory and reported all three unresolved |
| `git rev-parse HEAD` before and after every long step | `5f2a18c` throughout; the clone ended clean with 0 modified files |

## Paste-ready fixes

Row 8 — give the deferred finding a home outside the record. Either open a
tracker issue and rewrite the verdict cell of round 1's finding 5 as
`deferred #N`, or write the rider at both coordinates in
`.github/scripts/close_issues_on_release.py` and point the cell at it:

```python
# RIDER: read 2026-09-08, at the FENCE pattern and the SPAN pattern just
# below it. Review round 1 of work item 1788844400 found five
# well-formed shapes these two give up: a tilde fence, a four-space indented
# block, a fence indented inside a list item, an HTML comment, and a
# double-backtick span. Widening them changes what a RELEASE closes, not only
# what issue_claims_check.py reports, so it was left out of that branch. If
# you open these two patterns, decide that question here.
```

Row 8, the record half — replace the self-referential cell in round 1's
Deferred table:

```markdown
| Whether `FENCE` and `SPAN` in `close_issues_on_release.py` should cover tilde
fences, four-space indented blocks, fences indented inside a list item, HTML
comments and double-backtick spans — which changes what a release closes, not
only what this check reports | a `# RIDER:` comment at both patterns in
`.github/scripts/close_issues_on_release.py` | the repository owner |
```

Row 9 — finish the plan bullet so a reader of the plan alone learns the
behaviour, at `plan.md:81`:

```markdown
- **A trailing `#N` in a table cell or a URL fragment.** A markdown table row
  starts a segment (rule 3) and `#L45`-style anchors do not match `#\d+`, but
  a six-digit hex colour outside a code span would read as issue `#123456` in
  the mention list. A numeric fragment sitting in the same segment as a claim
  earns a warning rather than a mention, which is the same syntax read the
  same way: the alternative, excluding a `#N` preceded by a URL character,
  would be a second syntax to be wrong about.
```

Row 10 — point at the paragraph that carries the wording, at
`docs/issues-and-milestones.md:130`:

```markdown
The prose around those spans keeps its keywords out for the same reason. A
past-tense narrative keyword is still a keyword, so the opening paragraph of
this section says a release *acted on* one number rather than using the verb
this section is about, and a sentence that used it with a second number beside
it would earn the warning like any body.
```

## Proof

Files opened: `.github/scripts/issue_claims_check.py`,
`.github/scripts/close_issues_on_release.py`,
`tests/test_a_body_naming_two_issues_claims_one.py`,
`tests/test_docs_line_wrap.py`, `docs/issues-and-milestones.md`,
`docs/review-chain-spec.md`, `bin/test`, `bin/unverified-check`,
`bin/deferral-check`, `skills/verify/scripts/unverified_check.py`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`, `seal/follow-up.md`,
`seal/ledger/1788844400-a-body-naming-two-issues-claims-one.md`, and the work
item's `round-1.md`, `overview.md`, `plan.md`, `questions.md`, `spec.md` and
`changelog.md`.

Probes ran outside the repository, against a `--no-local` clone at `5f2a18c`
in a path unique to this round. Nothing was written into the clone that
survived: it ended with a clean working tree at the same SHA it started at.

Needs a fix: no
Loses a record or crashes: no
