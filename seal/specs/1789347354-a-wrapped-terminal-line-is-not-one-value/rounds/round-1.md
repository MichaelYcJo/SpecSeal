# 1789347354-a-wrapped-terminal-line-is-not-one-value — review round 1

| Field | Value |
|---|---|
| Target SHA | 7f47eed |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 392 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1, 2 and 3. The pin the plan named in place of the shared constant does not exist, an **Executed** count in the ledger row that folds into `seal/ledger.md` is one short of the tree, and the prompt budget is absent from the only place `CONTRIBUTING.md` says it is answered. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the branch's first review, against the whole diff `release/v0.11.4...7f47eed` with nothing inherited. Spec compliance first against the work item's own `spec.md`, `plan.md`, `questions.md`, `overview.md` and five phase records, then quality.

Five places were named to attack, in this order, each because a claim rests on it rather than because a defect was known to be there.

1. **The narrowed pattern itself**, because it is the whole change. What it now cuts that it should not, and what it now joins that it should not, against real report shapes this repository writes. Two facts were handed over rather than left to find: only two of the four shapes `spec.md` predicted were actually red in this tree, and one of the build's own mutations found nothing until a further case was planted for it.
2. **The two-rules split answering Q3** — the protocol owning the conformance statement, the warden the operative instruction, the template linking both. `tests/test_the_rules_have_one_owner.py` exists because a rule spread across eight carriers cost three rounds, so the round was asked to judge whether what landed is two rules or one rule written twice, which is the finding a later reader would open.
3. **The sibling `survivor_check.py#BLOCK`**, added to scope on contract §12 grounds: whether it is genuinely the same class, and whether its module's pre-existing alternatives are still pinned.
4. **The gate-change burden.** `CONTRIBUTING.md` §*What a change to a gate must carry* applies because #339 is a gate's guard.
5. **The scope fence.** `round_record.py#fix_table` and #309's two `close` defects belong to #391; `seal/ledger.md:89` anchors on `templates/sdd-round.md`'s `Needs a fix` row, which `spec.md` excludes for that reason.

One act of the build's was named for the round's own judgement rather than for acceptance: it edited `spec.md:252`, a framer-written file, because a `…` abbreviation in a coordinate made `evidence-check` exit 2 once the ledger fragment brought the directory into the records arm. The build says the claim is unchanged and only the spelling was unfolded; the round was asked to verify that rather than take it.

What the orchestrator had already executed at `7f47eed`, handed over so the round would not repeat it: five modules — `test_the_record_is_generated.py`, `test_a_corrected_sentence_survives_elsewhere.py`, `test_the_rules_have_one_owner.py`, `test_docs_line_wrap.py` and `test_a_document_that_names_a_script_says_how_to_reach_it.py` — 269 passed, 8 skipped, exit 0; `bin/evidence-check .` exit 0; `ruff check` on the two changed scripts and three changed test modules, exit 0.

The broad gate was withheld by name as the sealer's single act after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The case that was to replace the rejected shared constant does not exist; the two spellings can drift apart green | `skills/code-review/scripts/round_record.py:1252-1258` | open | `plan.md` §*Alternatives considered* and `spec.md` §*Scope* both name a case; executed — an alternative added to the model leaves both modules green, 167 passed |
| 2 | An **Executed** count in the ledger row is 117 where the tree is 118, over ten new cases where there are eleven | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` row 1 | open | Executed — 107 at `34b556a`, 118 at `7f47eed`; the row names the eleventh arm in the sentence that counts ten |
| 3 | The prompt budget is absent from the pull request body, which `CONTRIBUTING.md` names as the only place it is answered | PR #392 §*Operational impact* | open | `CONTRIBUTING.md` §*What a change to a gate must carry*: *It is answered in the pull request body or it is not answered* |
| 4 | The warden enumerates the owner's three-shape exception list; four carriers hold it and no case compares any two | `agents/warden.md:409` | open | Read — `docs/review-handoff-protocol.md:305`, `round_record.py:1243` and `:1296` carry the same list; grep finds no case pinning them together |
| 5 | `BLOCK`'s whole-line alternative is unpinned inside a constant phase 4 rewrote whole | `skills/code-review/scripts/survivor_check.py:384` | open | Executed — mutated to match nothing, the module stays 49 green; disclosed by the build and handed to this round |
| 6 | The claim that the setext underline comes back covers `=` at every length and `-` only from three | `skills/code-review/scripts/round_record.py:1247`, `docs/review-handoff-protocol.md:302` | open | Executed — `--` and `-` join under all three patterns; the model module states the caveat and these two do not |
| — | The narrowed pattern is the model's plus the two fence openers and nothing else | `skills/code-review/scripts/round_record.py#BLOCK_START` | answered | Executed — patterns printed side by side; removing the fence alternative leaves the model's spelling exactly |
| — | §15: the new cases were seen red | `tests/test_the_record_is_generated.py` | answered | Executed — the constant mutated to its `5e09345` spelling turns exactly seven arms red, and they are the seven the ledger names |
| — | `spec.md:252` — the framer's file edited, claim unchanged | `seal/specs/1789347354-…/spec.md:252` | answered | Executed — the verdict cell is byte identical, the anchor hash is unchanged, and the unfolded spelling matches `seal/ledger.md:89` |
| — | The scope fence — `fix_table`, the two `close` defects, `seal/ledger.md`, the template's `Needs a fix` row | `skills/code-review/scripts/round_record.py`, `templates/sdd-round.md` | answered | Read — two hunks in the script, neither near `fix_table`; `seal/ledger.md` absent from the diff; the template row unedited at line 43 |
| — | Q3 — is the split two rules or one rule twice | `agents/warden.md`, `docs/review-handoff-protocol.md` | answered | Two rules. Different audiences, and three assertions make the split falsifiable. The residue is finding 4 |
| — | The sibling is the same class | `skills/code-review/scripts/survivor_check.py#BLOCK` | answered | Executed — the old bare `[-*+>#]` split a line opening `#120`; the new spelling joins it, and the consequence differs as the build says |

## Paste-ready fixes

```python
def test_the_two_spellings_differ_only_by_the_fence_openers():
    """`plan.md` §*Alternatives considered* rejected one shared constant.

    What it named in place of the coupling is a case asserting the two
    spellings accept and reject the same shapes. A comment at each constant
    cannot do that: an alternative added to one and not the other leaves
    both modules green. The two script roots ship on different paths and
    neither imports the other, so this is the pin that replaces the import.
    """
    model = _load(
        "issue_claims_check",
        os.path.join(ROOT, ".github", "scripts", "issue_claims_check.py"),
    )
    ours = generator_module().BLOCK_START.pattern
    theirs = model.BLOCK_START.pattern
    assert ours.replace(r"|```|~~~", "", 1) == theirs, (
        "the two spellings have drifted apart. They are kept alike on "
        "purpose and differ only by this module's two fence openers.\n"
        f"  this module: {ours}\n"
        f"  the model:   {theirs}"
    )
```
```
Seven of the eleven new cases were seen red against the constant at
`5e09345` before it was replaced; the module went 107 → 118 green
```
```
| How many cases the record module holds | `plan.md` and `spec.md` both say 104 | 107 at the base, 118 after | Measured by running it. No consequence beyond the number |
```
```
| The generator's own module | **executed** — 107 green before, 118 after |
```
```
**Prompt budget: zero added.** The generator puts no question in front of a
person — it refuses or it writes, and both go to a log. The one option that
would have added one was refusing the ambiguity instead of joining it, which
would stop a run whose report omitted a blank line at whatever minute the
record is generated, with nobody at the keyboard. It was put to the owner
before the first edit and declined, on this project's first goal.
```
```
**Either line may wrap, and a wrapped line is one value.**
`round_record.py new` joins it across the wrap, and the guard deciding where
that join stops does not reach every shape a continuation can begin with. So
**leave a blank line under the pair**, which markdown wants anyway and which
is the one stop nothing can read wrong. Where the join stops, and which
shapes it cannot reach, is stated once in
`docs/review-handoff-protocol.md` §*The Needs a fix field — the answer a run
ends on*; this line is the instruction, that section is the rule. The
generator used to keep the first physical line and drop the rest without
saying so, and a round record shipped ending mid-clause.
```
```python
# The alternative that predates this branch and that phase 4 retyped without
# pinning. Mutated to match nothing, the whole module stayed green.
@pytest.mark.parametrize("rule", ["---", "___", "***", "==="])
def test_a_whole_line_of_one_marker_ends_the_segment(rule):
    """A thematic break and a setext underline are blocks in their own right.

    Without this alternative a claim above a horizontal rule and an
    unrelated claim below it land in one segment, which is the false
    positive `.github/scripts/issue_claims_check.py` spends its own
    whole-line alternatives to avoid."""
    reader = module()
    text = f"the claim above the rule.\n{rule}\nan unrelated claim below it."
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert not any("above the rule" in k and "below it" in k for k in keys), (
        f"{rule!r} is a block of its own and the segment ran straight "
        f"through it: {keys!r}"
    )
```
```
# requirement then takes the run-of-three markers out of the class, so a
# thematic break and a setext underline come back as whole-line alternatives
# of their own; `\r*$` on each is what makes a CRLF checkout read like an LF
# one. A `-` underline shorter than three characters is not among them and is
# joined, which is the model module's trade and stated in its comment.
```

## Executed probes

| What was run | Result |
|---|---|
| `python3 .github/scripts/run_tests.py tests/test_the_record_is_generated.py -q` at `7f47eed` | 118 passed, exit 0 |
| The same module with `skills/code-review/scripts/round_record.py` and the test module checked out at `34b556a` | 107 passed, exit 0 — the base count |
| The same module with `BLOCK_START` alone mutated to its `5e09345` spelling | 7 failed, 111 passed — the two `base` arms and all five of `STOPS_THE_JOIN` |
| `python3 .github/scripts/run_tests.py tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_the_rules_have_one_owner.py -q` at `7f47eed` | 97 passed, exit 0 |
| The sibling module with `[-*_=]{3,}\s*$` mutated to match nothing | 49 passed, exit 0 — the alternative is pinned by nothing |
| The record module and `tests/test_a_body_naming_two_issues_claims_one.py` with an alternative added to the model's pattern and not to this module's | 167 passed, exit 0 — the two spellings can diverge green |
| The three patterns loaded and matched against 29 line shapes | This module's spelling is the model's plus the two fence openers, character for character |
| The broad gate — the full suite, repository-wide `ruff check`, and the typecheck | Not run by this round, and not yet run by anybody at this SHA. It is the sealer's single act, and this report leaves findings open, so it is not yet due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py#file_units` reads a `##` line inside a fenced block as a heading, so a ledger anchor on such a section stops at the fence. Three of thirty-six anchored markdown files affected; `seal/ledger.md` R7 under-covered by 81 lines | `overview.md` §*Not verified*, and it is a change to a gate | the repository owner — carried forward unchanged; this round did not reopen it |
| `#309`'s two `close` defects | `#391`, in the `release: 0.11.4` milestone | the third work item of this release. Verified out of this branch: `fix_table` was not opened |
| Whether `survivor-check` over this branch's own range reports anything | `overview.md` §*Not verified* | the review orchestrator at the first fix pass — there was no fix pass to run it over, and there is one now |
