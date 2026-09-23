# 1790119502-four-shipped-work-items-wait-unfolded — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | dcbe48a |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Fold `1790076060` by putting its marker on the sentences
`docs/review-chain-spec.md` already carries — the item wrote its rules as the
sections themselves — plus L6's sentence, and re-read and re-verify the rows
that drift. Fold `1790076080` into `docs/measuring-a-run.md` §*Where a reading
goes*, with L10's default as the rule, and one sentence in
`docs/the-agent-set.md`. Leave `docs/issues-and-milestones.md` unmarked
(`spec.md` O6).

## What this phase found

**`1790076060` — what was folded, and how.** No second copy: three marker
lines on the item's own sentences — at the head of *The cap bounds rounds, and
not the fixes of the round it stopped*, above *Two bounds end a run `capped`*,
and above the ladder's opening rule in *Where a leftover goes*. Each rule was
read against the tree first and nothing later overturns it: the ownership test,
`New units` as the evidence (with the prose-path exception the section already
states), the two exits apart, `Fixes checked by` reading `round-N` on a capped
record that wrote fixes, and the four rungs with `Who answers it` as the test.
L6 became one paragraph under its own marker after the rung-4 cost: the two
messages, what each says, why they lag, and that the repository owner decides
the pair. Both constants were opened before it was written —
`chain_check.py#CAPPED_EXIT` says *every finding still open becomes an issue*
and `round_record.py#DEPTH_EXIT` is *deferred with a named answerer, or
becomes an issue*.

**`1790076060` — what was dropped.** The 89 / 43 / 48% measurement stays where
the section already dates it and was not re-stated; the `from-review`
paragraph in `docs/issues-and-milestones.md` is not marked (O6); the spec's
Out items (no lookup, no checker change, no new field, no cap change) are
constraints on that build rather than standing rules, and the moratorium they
lean on already has its own section.

**The same wording stands in prose places the fold did not touch.** A line
grep for `becomes an issue` over `docs/`, `agents/` and the skills found four,
and that count was short: **corrected 2026-09-23 in round 2's fix pass**, a
whitespace-collapsed search for *or becomes an issue* also finds
`templates/sdd-round.md`, and not every carrier points at the ladder, so the
claim that each did was wrong. L6's paragraph now names the search instead of
a list. Not rewritten here: this is a fold, and those are carriers of a rule
the owner is asked to decide in L6's sentence — changing them first would
decide it. Named in `overview.md` §*Not done*.

**`1790076080` — what was folded.** Two paragraphs in `docs/measuring-a-run.md`
§*Where a reading goes*, each under the marker: the command, its refusal
without `--says`, every state of the label lookup, that it never opens a log,
and that a command does not make anybody run it; then L10's default as the
rule — a network write only a person's typing starts is not a hook, the hook
list's conditions are hook-shaped, and what that bullet forbids still binds it.
One paragraph in `docs/the-agent-set.md` after *A section marked for one role
reaches that role and no other*: the orchestrator's acts are tabled against
their delivery, held by a test that reads the marker and not the meaning.

**The code has one state more than the spec.** `spec.md` of `1790076080`
names four states; `session_cost.py#post` answers five — `UNREADABLE`, a
machine where `gh` cannot run, also posts nothing and exits 0. The newest
statement is the code's, so the paragraph says *no issue has ever carried it,
or `gh` cannot run*. The basename claim was checked too: `session_cost.py`
takes `os.path.basename` of the transcript for the posted body, pinned by
`tests/test_session_cost_post.py#test_the_posted_body_does_not_carry_the_transcripts_path`.

**`1790076080` — what was dropped.** The two acts the ticket listed that were
already closed (the broad gate, the routing question) — their own documents
state them; the nineteen/twenty count and the 8/5/5/2 split — a moment, and
the table in `skills/implement/orchestration.md` is the live count; the three
enumeration gaps — #506 owns them (L11); the rejected `PostToolUse` notice and
*command per act* — alternatives, not rules.

**Ledger.** `bin/evidence-check --strict .` after the prose: `1466 ok · 2
drifted`, both on `docs/review-chain-spec.md` — the cap subsection (rows C1
and C3 of the `1790076060` section) and the ladder subsection (row C4). Each
row was re-read against the edited unit — only marker lines and the L6
paragraph were added, and every sentence each claim cites is unchanged — and
given a dated `Re-read` note. `bin/evidence-check --reverify .` rewrote three
hashes: `cd25543f → 3e7be78c` twice and `0973dd22 → 4a6c56fa`. After it:
`1468 ok · 0 drifted · 0 broken`, exit 0. `docs/measuring-a-run.md` and
`docs/the-agent-set.md` drifted nothing, as G1 said.

**Run for this phase, each exit read directly.** `./bin/settle`: `0 work items
in 0 segments, 11 ungrouped`, and all four under *folded already, waiting to be
retired* (A1). `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`,
`tests/test_one_word_one_meaning.py`,
`tests/test_the_release_tail_does_not_end_at_the_tag.py`,
`tests/test_the_rules_have_one_owner.py`, `tests/test_a_segment_feeds_the_flow_log.py`,
`tests/test_every_orchestrator_act_names_its_delivery.py` and
`tests/test_session_cost_post.py`: `223 passed`, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
