# a wrapped terminal line is not one value — questions for the planner

<!-- seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

Six rows. **Three need a person and they are Q1, Q2 and Q3**; Q4 and Q5 are a
command each and must not be queued behind anybody; Q6 is the work's and is
decided by the phase that meets it.

The routing batch is answered and is not re-asked here: review through the
review chain, destination the pull request, implementation `smith`, planning
the framer, answered 2026-09-14 by the owner in `routing.md`.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | **Does `terminal_value` keep joining a wrapped terminal line with a narrowed guard, or refuse a report whose terminal pair is not followed by a blank line?** Round 3's fix pass of #120 called this the decision it was least sure of, round 4 deferred it to *the repository owner, at the release that revisits the join*, and #339 closes by saying whoever takes it decides this too. This is that release, and the answer decides what phase 1 builds | **a person** | **(a) Join, narrowed** — `BLOCK_START` becomes the `issue_claims_check.py` pattern, both directions close, and the residual risk is a report that omits the blank line under the pair having its next line swallowed into the cell. That error reads as wrong at a glance, which is the axis round 2 decided the join on. **(b) Refuse** — `terminal_value` raises when the line under the pair is non-blank. No swallow is ever possible again, and a report that forgot a blank line stops the record from being generated at all, in a run with nobody at the keyboard. It adds one interruption per malformed report where today there are none | **(a) join, narrowed** — answered by the repository owner on 2026-09-14, in one batch with Q2 and Q3, confirming the default. *Verification through an automated workflow is this project's first goal*, and a refusal spends a prompt on a blank line `agents/warden.md` already instructs the reviewer to leave | ✅ |
| Q2 | **Do #309's two `close` defects travel with this work, or are they opened against the cells work item?** The comment on #309 reports that `close` reduces a `deferred` row's grounds to the home alone — discarding the paragraph the fix pass wrote — and that it writes an empty code span into a `fixed` row's grounds. The release cut assigns *which values each half accepts* to the third work item (#321, #323, #341, #273, #353). **Read** 2026-09-14: none of those five covers either defect, so excluding them here drops both from the release | **a person** | **(a) In** — this branch also opens `round_record.py#fix_table`, where the empty-code-span diagnosis already sits as a `# RIDER:` verified 2026-09-08, and #309's own comment argues all three are one seam. It grows the change by a second parse arm and a second failure direction. **(b) Out** — they belong to the cells work item and a ticket is opened for them there before this branch merges, or they fall through the release entirely. It keeps this change one seam wide, which is what `spec.md` §*The judgement the release asked for* argues for | **(b) out** — answered by the repository owner on 2026-09-14, confirming the default, and the half that made it unsafe alone is paid: **the two defects are opened as #391 against the cells work item, in the `release: 0.11.4` milestone**, so nothing falls through the release. The pull request body names it. The fence came from whoever cut the release, and re-cutting scope at framing time reopens the batch this phase exists to spend once | ✅ |
| Q3 | **Which file owns the wrap rule once three carriers state something about it?** `tests/test_the_rules_have_one_owner.py` holds ten rules to one owner and a linking sentence from every other carrier, because the last branch's count rule reached eight carriers and took three rounds to correct. After phase 3 the rule is stated in `docs/review-handoff-protocol.md`, `agents/warden.md` and `templates/sdd-round.md` | **a person** | **(a) One rule, protocol-owned** — the protocol states it and the warden and the template each carry a one-sentence link naming it. Correct by the registry's own shape, and it costs the reviewer a hop at the moment the instruction matters. **(b) Two rules, different audiences** — the protocol owns the **conformance** statement (a wrapped terminal line is one value, and here is where the join stops, which a second implementation is built from) and the warden keeps the **operative** instruction (leave a blank line under the pair). Not one rule twice, and neither needs a registry row; the risk is that a later reader reads them as one rule in two places and opens the finding | **(b) two rules** — answered by the repository owner on 2026-09-14, confirming the default. The audiences differ: one is read by whoever builds a tool, the other by whoever writes a report at minute forty of a review. The template links the protocol in either answer | ✅ |
| Q4 | **Is `survivor_check.py#BLOCK` the same class, and does the narrowed pattern keep its module green?** `spec.md` §4 establishes by reading that the bare `[-*+>#]` class matches `#120` at the head of a line. What is not established is whether substituting the corrected alternatives leaves `tests/test_a_corrected_sentence_survives_elsewhere.py` green, and whether that module has a case that would see the change at all | **a measurement** | One substitution and one module run, plus a case at the `#N` shape seen red first. If the module goes red, the sibling is a different judgement and phase 4 becomes an issue with the measurement attached | Phase 4 proceeds on the assumption that it is the same class and the module stays green; the plan puts it last so the other answer costs nothing above it | ⬜ |
| Q5 | **Do any round records already in the tree carry a terminal value truncated to the bare verdict word?** 337 terminal rows stand across `seal/specs/*/rounds/round-*.md`. A truncation after the word costs a reader the reason and costs `chain_check.py` nothing. A truncation *to* the word is the one shape that would leave a record the checker reads differently, and it decides whether the no-migration answer in `spec.md` §*Scope* holds | **a measurement** | One grep over the 337 rows for a value that is the bare word, then `chain.yes_or_no` on each hit. If there are none, `spec.md`'s exclusion stands as written. If there are, the migration question comes back and becomes a person's | No migration. A round record asserts a past state and the machine-read half survived the cut | ⬜ |
| Q6 | **Which of the four descriptions actually needs rewording once the pattern lands, and what does `evidence-check` say about the anchors that move?** `spec.md` §*Data & interfaces* predicts `agents/warden.md#"## Report"` DRIFTED and the three others unchanged. A prediction is not a reading | **the work** | Phase 2 runs `evidence-check --reverify` after its edit and records what actually moved. A BROKEN anchor where DRIFTED was predicted means the edit landed in the wrong paragraph, and `CLAUDE.md`'s rule then applies: a row whose anchor a change removes is REMOVED, not re-pointed — but none of these claims dies with its edit, so none of them should reach that | Re-read and re-stamp; write the divergence into `phases/phase-2.md` if the prediction was wrong | ⬜ |

## What was decided by reading and needs nobody

These were candidates for the batch and are not in it, because a different
answer would not change what gets built.

- **Whether `#309` is still a live defect.** It is, narrowly: the general join
  landed at `393da64` and `BLOCK_START` reopened it for the shapes this
  repository writes most. Nothing needs deciding; `spec.md` §1 records it.
- **Whether the seven soundness claims have to be retracted.** They are not in
  this tree. Four descriptions have to be made true of what ships, which is a
  smaller job than #339 states and the same job in kind.
- **Where the template's sentence goes.** #340 names the trap and this
  repository's own answer to a broken anchor settles it: the prose about the
  field, never the row `seal/ledger.md:89` quotes.
- **Whether to share one pattern constant across the three modules.** The two
  script roots do not import each other and one of them does not ship into an
  install. `plan.md` §*Alternatives considered* carries it.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
