# 1788844400-a-body-naming-two-issues-claims-one — review round 2

| Field | Value |
|---|---|
| Target SHA | 5f2a18cbf8c751fc818f59e46f3753743faa1fb6 |
| Ran by | warden on claude-opus-5 |
| PR | 261 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

A verifying round, spawned after round 1's fixes were committed and targeted at
the diff of those fixes: `2fae791..8f09a77`. Its job was stated as the answers
rather than new findings — for each verdict round 1 recorded as closed, is it
actually closed — with one surface exempt, what the fixes themselves created.

Six checks, in the order the prompt set them.

1. **The five `fixed` rows, each at its own coordinate**, asking whether the
   finding is closed rather than whether a change was made.
2. **The acceptance case, re-run rather than read** — the branch's own checker
   against the document that teaches the rule. The round was asked to judge
   whether the outcome is right or a fix that went one step too far, since the
   paragraph's whole subject is what a keyword does in running prose and a
   paragraph that can no longer say the word may have lost what it teaches.
3. **The nine new units — named as the exempt surface and where the defects
   historically are.** One of them was itself defective when first written:
   its parameters were all rejected at the first character, so the anchor it
   was meant to pin was never reached and removing that anchor left 42 cases
   green. The round was asked to verify the strengthened version reaches the
   anchor, and to check the other eight for the same shape.
4. **Two fixes outside the scope the orchestrator gave** — rows 6 and 7, fixed
   at `7da891e`. Whether the grounds hold and whether that commit is clean,
   the fixer having stated it can be reverted alone with no overlapping hunks.
5. **The one `answered` row**, whether what it closed is genuinely answered by
   the run it names and whether the two facts it moved to the owner genuinely
   cannot be answered by CI.
6. **The one `deferred` row**, whether the durable home is right.

Facts carried as executed by the orchestrator at round 1's target: the module
at 28 passed exit 0, ruff clean on both changed files, and round 1's sharpest
finding reproduced — the checker reporting a claim and a warning against the
repository's own documentation.

Carried as not the round's to close: the remaining `NOT-IN-TREE` refusal in
round 1's own report, which the orchestrator takes at the closing commit. The
round was asked to say so if it saw the class widen.

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

## Paste-ready fixes

```python
# RIDER: read 2026-09-08, at the FENCE pattern and the SPAN pattern just
# below it. Review round 1 of work item 1788844400 found five
# well-formed shapes these two give up: a tilde fence, a four-space indented
# block, a fence indented inside a list item, an HTML comment, and a
# double-backtick span. Widening them changes what a RELEASE closes, not only
# what issue_claims_check.py reports, so it was left out of that branch. If
# you open these two patterns, decide that question here.
```
```markdown
| Whether `FENCE` and `SPAN` in `close_issues_on_release.py` should cover tilde
fences, four-space indented blocks, fences indented inside a list item, HTML
comments and double-backtick spans — which changes what a release closes, not
only what this check reports | a `# RIDER:` comment at both patterns in
`.github/scripts/close_issues_on_release.py` | the repository owner |
```
```markdown
- **A trailing `#N` in a table cell or a URL fragment.** A markdown table row
  starts a segment (rule 3) and `#L45`-style anchors do not match `#\d+`, but
  a six-digit hex colour outside a code span would read as issue `#123456` in
  the mention list. A numeric fragment sitting in the same segment as a claim
  earns a warning rather than a mention, which is the same syntax read the
  same way: the alternative, excluding a `#N` preceded by a URL character,
  would be a second syntax to be wrong about.
```
```markdown
The prose around those spans keeps its keywords out for the same reason. A
past-tense narrative keyword is still a keyword, so the opening paragraph of
this section says a release *acted on* one number rather than using the verb
this section is about, and a sentence that used it with a second number beside
it would earn the warning like any body.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/issue_claims_check.py:107` | round 1's 1 — fixed |
| round-1 | `docs/issues-and-milestones.md:117` | round 1's 2 — fixed |
| round-1 | `.github/scripts/issue_claims_check.py:208` | round 1's 3 — fixed |
| round-1 | `seal/specs/1788844400-a-body-naming-two-issues-claims-one/overview.md:27` | round 1's 4 — answered |
| round-1 | `.github/scripts/issue_claims_check.py:123` | round 1's 5 — deferred |
| round-1 | `.github/scripts/issue_claims_check.py:199` | round 1's 6 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
