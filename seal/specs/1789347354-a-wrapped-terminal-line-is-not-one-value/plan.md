# Implementation Plan: a wrapped terminal line is not one value

<!-- seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-14 by the owner, when `smith` was spawned.

## Summary

Narrow one regular expression to the one this repository already ships and has
already measured, pin the direction nothing pins, make the four descriptions in
the tree true of what ships, give the conformance document and the record
template the sentence neither has, and close the same defect in the sibling
module that carries it.

Five phases. Phase 1 is the whole behaviour change and stands alone; phases 2
and 3 are the documents, which is where #339's correction and #340's addition
meet in the same paragraphs; phase 4 is `skills/agent-contract/SKILL.md` §12's
other instance; phase 5 is the fragments.

**Phase 1 depends on Q1.** If the owner answers *refuse* rather than *join*,
phase 1 is a different fix and phases 2 and 3 describe a different rule. Nothing
else in the plan moves.

## Technical context

**The defective constant**, `skills/code-review/scripts/round_record.py:1230`:

````python
BLOCK_START = re.compile(r"^\s*(#|\||>|[-*+]\s|\d+\.\s|```|~~~)")
````

Read as written, it is wrong in both directions at once. `#` carries no space
requirement, so `#120's parser is the one that matters.` matches and the value
is cut. `[-*+]\s` does carry one, so `---`, `___`, `***` and a setext underline
do not match and a thematic break under the terminal pair is joined into the
cell. `\d+\.\s` wants a literal dot, so `1) Proof.` passes. An indented line and
an HTML tag pass, and neither is reachable by any widening of a marker list.

**The corrected constant already exists in this repository**, at
`.github/scripts/issue_claims_check.py:116`, where its comment names the same
trap in the module written to catch it and `seal/ledger.md:1670` records it as
executed by mutation, one rule at a time. The paste-ready form for this module —
the same alternatives plus the two fence openers — is in
`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-4-report.md`
under finding 2, together with the measurement that all 108 cases of the record
module stayed green under it. That is a report's claim, not this session's
finding: **open it and re-run it** rather than carrying the number.

**What reads the value.** `terminal_value` is called twice in `build`, for
`chain.NEEDS` and `chain.FLOOR`, and nothing else in the report parse reads a
scalar field. Every other cell in the field table comes from argparse or from
git; the rest of the report reaches the record as a table, a fence, or a
verbatim section. **Read**: this closes #309's first Not-verified item — the arm
reads exactly two fields, and both are already joined.

**What the value feeds.** `chain.yes_or_no` takes the verdict word before the
first `chain.SEPARATORS` character, and `chain_check.py` computes the reopening
bound from it. A truncation after the word therefore costs a reader the reason
and costs the checker nothing, which is why no migration is proposed. The one
shape that would change that is a truncation to the bare word, which is Q5.

**The sibling.** `skills/code-review/scripts/survivor_check.py:365`:

```python
BLOCK = re.compile(r"^\s*(?:[-*+>#]|\d+[.)](?=\s)|[-*_=]{3,}\s*$)")
```

The whole-line run is already right. The bare `[-*+>#]` class is the same defect
as the middle row of `spec.md`'s table, one module over, and its consequence is
different: a sentence split at a false boundary is mis-scored rather than a
record cell truncated.

**Constraints the phases work inside.**

- `agents/warden.md` is in `tests/test_docs_line_wrap.py`'s `COVERED`, so its
  new prose wraps at the limit. `docs/review-handoff-protocol.md` and
  `templates/sdd-round.md` are not covered; wrap them anyway, because
  `tests/test_docs_line_wrap.py`'s own corpus is grown from files that arrived
  wrapped.
- `tests/test_the_rules_have_one_owner.py:563` pins three sentences of
  `agents/warden.md` §*Report* verbatim. Phase 2 edits that section. Read those
  three assertions before touching the paragraph above them.
- `seal/ledger.md:89` quotes `templates/sdd-round.md`'s `Needs a fix` row
  verbatim as an anchor. Phase 3 writes in the prose below it, never in the row.
- `tests/test_the_record_is_generated.py` holds 104 cases and is the module
  phase 1 runs. `bin/test` is the runner; the broad gate is the sealer's.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Widen `BLOCK_START`'s marker list** — add `---`, `___`, the setext underline and the HTML tag to the class it already has | Round 3's own bet, and it loses in six months the way it lost in four days. Every marker added is one more shape a genuine continuation may not begin with, in a repository whose reports open lines with `#N`, `**bold**` and `<div>` as a matter of course. The next reader adds one more marker and truncates one more shape, silently, because a truncated cell reads as a finished sentence | **Rejected.** The repair is a narrowing, and this repository already contains it |
| **Refuse the ambiguity instead of joining it** — `terminal_value` raises when the line under the terminal pair is non-blank | No swallow is ever possible again, which is the honest attraction. What it costs is a refusal arriving at the moment the record is generated, in a run nobody is watching, over a blank line the warden already asks for. *Verification through an automated workflow is this project's first goal*, and this trades that for a class of error that reads as wrong at a glance | **Deferred to a person — Q1.** Round 3's fix pass called it the decision it was least sure of and round 4 deferred it to the owner *at the release that revisits the join*. This is that release |
| **One shared pattern constant across the three modules** | `.github/scripts/` and `skills/*/scripts/` ship on different paths, neither imports the other, and the plugin's scripts are copied into installs where `.github/` does not follow. A shared module is a new cross-boundary coupling bought for three constants | **Rejected.** The pin that replaces it is a case asserting the two spellings accept and reject the same shapes, which goes red when either drifts and costs no coupling |
| **Land #340 as a docs-only follow-up** | Between the two merges, the document that defines a conforming tool describes a behaviour the shipped tool no longer has. A second implementation written from it truncates — the defect just closed, shipped as conformance. It is also the cheapest thing in the change, so the saving is the smallest one available | **Rejected.** `spec.md` §*The judgement the release asked for* holds the argument |
| **Restate the wrap rule in all four carriers** | `tests/test_the_rules_have_one_owner.py` exists because the last branch's count rule reached eight carriers and took three rounds to correct three at a time. Four statements of one rule is four places to disagree | **Rejected in that form.** One owner states it and the others link it — which file is the owner is Q3 |
| **Migrate the round records already truncated** | A round record asserts what a reviewer wrote at a past SHA. Rewriting a cell now makes it assert something nobody wrote, and the machine-read half was never lost | **Rejected**, with Q5 measuring the one shape that would reopen it |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `BLOCK_START` narrowed to the `issue_claims_check.py` form plus the two fence openers, and the truncation direction pinned at four shapes | Each new case seen red against the constant at `5e09345` first; then `tests/test_the_record_is_generated.py` whole — the existing swallow case and the four thematic-break shapes included | `1e91894` |
| 2 | The four descriptions made true of what ships, each naming what the guard does not cover and that the blank line is the only stop that covers every shape | A case pinning the warden's sentence, seen red with it stashed (§14, §15); `tests/test_the_rules_have_one_owner.py` green; `evidence-check --reverify` re-stamps `agents/warden.md#"## Report"` and names nothing else | `02e4436` |
| 3 | #340 — the conformance statement in its owner, linked from the other carriers, with `templates/sdd-round.md` gaining it in the prose about the same fields | A case in `tests/test_the_rules_have_one_owner.py`'s shape, both halves seen red; `evidence-check --strict` reports 0 broken, and `seal/ledger.md:89`'s template anchor hash is unchanged | `02e4436` |
| 4 | `survivor_check.py#BLOCK` brought to the same pattern, or the grounds for leaving it written into the module and into `overview.md` | A case at the `#N` shape, red against `BLOCK` as it stands; `tests/test_a_corrected_sentence_survives_elsewhere.py` whole | `ac49d7f` |
| 5 | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, and the re-stamps phases 2 and 3 earned | `evidence-check` over the fragment: every row resolves, nothing drifted, nothing broken | this phase's commit |

**Status is empty, or the commit that closed the phase.** A tick is refused and
so is `done`.

Phase 4 is last on purpose. It is the one phase whose scope came from §12 rather
than from a ticket, and it is the only one that can be dropped — to an issue,
with the measurement Q4 produced — without unpicking anything above it.

Write the ledger rows as they are settled and let the write ride phase 5's
commit. What a phase finds and the next one needs goes to
`seal/specs/<id>/phases/phase-N.md` from `templates/sdd-phase.md`.

## Operational impact

- **No migration**, and `spec.md` §*Scope* says why. Q5 is what would reopen it.
- **No new dependency, no new environment variable, no new file under
  `skills/*/scripts/`.** Nothing this change writes triggers
  `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`, which
  shipped at `34b556a` — no script is added or renamed, and the prose added in
  phases 2 and 3 names `round_record.py`, which already carries its locator and
  its `bin/round-record` wrapper.
- **Compatibility.** A record generated before this change is unaffected: the
  fields it carries are unchanged and `chain_check.py` reads them the same way.
  A record generated after it may hold a longer `Needs a fix` value than the
  same report would have produced before, which is the fix.
- **What a deployer must not miss.** Phase 2 changes text a reviewer reads and
  acts on, so `skills/agent-contract/SKILL.md` §14 applies: the sentence ships
  with the case that pins it, in the same commit.
