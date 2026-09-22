# 1790076080-every-orchestrator-rule-is-a-sentence — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `c58a05b4` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Name the command in `skills/verify/SKILL.md` §*Measure the segment, and feed
the flow log*, in place of the steps it replaces. Flip the phase-1 table's row
for that act to the command **and** keep the sentence that nothing makes it
run — *do not let phase 3 turn that row into a closed-looking one*. Write
`changelog.md` and the ledger fragment. Read the ledger the unscoped way to
learn what the branch falsified, keep the narrowing for the write, and answer
the survivor sweep. Acceptance A10 and A11.

## What this phase found

**There is no row to flip, and finding that out is what the phase-1 table is
for.** The act #330 measured — posting a segment's reading to the flow log —
lives in `skills/verify/SKILL.md` under a heading carrying no
`Orchestrator:` marker, in a file the row rule does not read. `spec.md` and
`plan.md` both speak of *the phase-1 table's row for that act*; the row set
they specify, *every `##` heading whose text begins `Orchestrator:` in either
orchestration file, plus every `###` heading directly beneath one*, does not
reach it, and `tests/test_every_orchestrator_act_names_its_delivery.py`
refuses a row naming a heading no file carries. So a row for it could not be
written without either breaking the rule or special-casing the test.

**This is the table's own blind spot arriving on its first instance**, which
the phase-1 section states in the paragraph before the table: an act written
for the orchestrator under a heading carrying no marker has no row and nothing
notices. Nothing was invented to cover it. What was done instead:

- **Marking the heading was considered and rejected.** `skills/verify` is in
  no agent's `skills:` list, so a marker there would not turn
  `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` red —
  checked, the five definitions list `agent-contract`, `implement`,
  `code-review`, `writing-style` and `legacy-parity` and nothing else. It is
  refused on this repository's own one-word-one-meaning rule: the marker means
  *this section must not reach an agent's payload*, and asserting that about a
  file no payload holds gives the marker a second meaning. The other cost is
  the citations. **Corrected 2026-09-22 in round 1's fix pass:** this said
  *eight documents* and nothing had been counted. **Corrected twice, and the
  second time is what fixed the method.** Round 1's fix pass wrote
  *thirty-three files* and did not say what the count was over: it was a
  single-line search with this work item's own files dropped, so it
  understated in the same direction as the claim it was repairing. Round 2
  re-derived it both ways.

  The count that does not drift is the live one. **Twelve files outside
  `CHANGELOG.md` and `seal/specs/` name the heading**, four of them test
  modules that would go red on a rename, and `seal/ledger.md` carries nine
  live rows anchored on the heading text. **Two of the twelve are reachable
  only by tolerating a line wrap** — `.github/scripts/roll_flow_measurement_issue.py`,
  which names the section inside a message a person reads on the tracker, and
  `skills/commit-pr-convention/SKILL.md` — so the single-line search that
  produced *thirty-three* would have missed both.

  The whole-tree total moves as this work item's own records accumulate, so
  it is stated with its tree and its method. Re-derived through `git show` at
  four commits, without checking anything out:

  | Commit | What it is | Single-line | Wrap-tolerant | Live |
  |---|---|---|---|---|
  | `238dbeaf` | round 1's target | 37 | 47 | 12 |
  | `73e71c1a` | round 2's target | 39 | 48 | 12 |
  | `39732781` | round 2's record commit | 40 | 49 | 12 |
  | `54198d71` | round 3's target | 40 | 49 | 12 |

  **Corrected 2026-09-22 after round 3, and it is the third correction to
  this one number.** The sentence here read *the round that raised this read
  48 and 37 at `73e71c1a`, four commits earlier*, and both halves were wrong.
  48 is right at `73e71c1a` and 37 is not — 37 is `238dbeaf`'s figure, the
  commit round 1 reviewed. And `git rev-list --count 73e71c1a..39732781` is
  **1**; four is the length of round 2's own fix range, `238dbeaf..da35172f`,
  which is a different distance between a different pair of commits.

  A reader who re-derived 37 at `73e71c1a` would get 39 and conclude the whole
  correction had drifted, when one clause had — in the paragraph whose own
  subject is that a count has to say what tree it was taken over. The **live**
  column is the one that has not moved at any of the four commits, which is
  why the number above the table is the one stated first.

  The conclusion is unchanged and gets stronger, and the reason it rested on
  was an aggregate nobody had opened — contract §5, in the record that states
  it, three times over.
- **The requirement was met where it could be met.** The table's section
  carries a paragraph naming the act, its file, its delivery
  (`session-cost … --post`) and the sentence that **nothing makes it run** —
  written as the row that act would have, at the place the blind spot put it.
  A reader of the table is told the act exists, where it is, and that it is
  not closed.

**It is a candidate for an issue rather than a fix here**, and it is named in
the hand-back: either the row rule widens to a named list of sections outside
the two files, or the marker splits into one that means *keep this out of a
payload* and one that means *this is the orchestrator's act*. Both are
mechanism, both are larger than this branch, and choosing between them is a
person's.

**A10 is met, and the edit is smaller than *in place of* suggests.** Three
things in that section are pinned verbatim by
`tests/test_a_segment_feeds_the_flow_log.py`: `gh issue list --label
flow-measurement --state open`, `gh issue list --label flow-measurement
--state all`, and `gh issue comment` with `--body-file`. Removing them would
have turned that module red, and they are also what a session doing this by
hand needs. So the command was put **in front** of them and the by-hand forms
kept beneath it, labelled as such. The four readings stay, because they are
what the command's exits mean and a session that meets a refusal has to know
which one it hit.

**One sentence was taken back out for a ledger row.** The first draft said
*what #330 measured*, and `seal/ledger.md`'s F5 holds that the shipped skill
names no tracker state existing in this repository alone — a clause its own
notes record as already dented by a `(#300)` in the same section. Adding a
second issue number would have deepened a disclosed defect knowingly. The
sentence now reads *what was measured*, and the only `#N` in the section is
still that `(#300)`.

**The unscoped read found one drifted anchor and nine rows behind it.**
`evidence_check.py .` with no `--ledger` reported
`skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"` as
drifted; nine rows of `seal/ledger.md` cite it — F5, R3, G5 and six more. Each
was opened and read against the edit, and **all nine still hold**: eight are
about step 1, the run-level table, the orchestrator-boundary paragraph or the
word `segment`, none of which this edit touches, and F5's state is unchanged
for the reason above. So each carries a `Re-read 2026-09-22` note and the
`Checked` column moved to that date, which is the practice those same cells
already record from four earlier branches. The re-stamp was
`--ledger seal/ledger.md --reverify .`: only drifted rows are rewritten, and
the one drifted anchor is the nine rows this phase read, so the blanket-write
objection those cells raise does not apply. Verified by diff — nine lines
changed, and the only change in each is the hash.

**The work item's own six rows are in its fragment**, never appended to
`seal/ledger.md`. They were written with `@00000000` placeholders and stamped
with `--ledger <the fragment> --reverify .`; a hash that is not eight hex
characters is dropped silently, which `seal/follow-up.md` already records, and
`@00000000` is the placeholder that survives that.

**Nothing survived, and nothing to exempt.** `survivor-check --range
origin/release/v0.13.1...HEAD` examined 1203 files against the 29 sentences
the range removed and reported none still standing, so this work item has no
`survivors.md`. `correction_check.py` over the same range reports no merge
commit in it, so no correction could have been dropped.

**A11 is met.** `git diff --stat origin/release/v0.13.1...HEAD -- hooks
.github/workflows` is empty: nothing this work ships lands under either, so
`CONTRIBUTING.md` §*What a change to a gate must carry* was read and found not
to apply, as `spec.md` §Grounding records.

**Q3 ships as the framer's default (a)**, with the grounds in `overview.md`
where a reviewer can overturn them by opening the section, and stated in
`plan.md` §*Operational impact*, which already carried them. `CONTRIBUTING.md`
is edited not at all.

**What was run**, executed, output read: the fourteen modules that read either
edited document or the ledger (520 passed, 7 skipped); `evidence_check.py .`
unscoped, exit 1 before the re-stamp and exit 0 after, 1448 rows ok and 0
drifted; `survivor_check.py` and `correction_check.py` over the branch range,
both exit 0; `unverified_check.py --baseline origin/release/v0.13.1
seal/specs/`, exit 0, this work item's three open rows read back. The full
suite, the repository-wide lint and the typecheck are `unverified` and are the
sealer's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The instruction to find the log by hand as the first step, and the bare `gh issue comment` step 2 | `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*, one paragraph further down. Neither sentence left the tree: both `gh` forms and their reasoning stand beneath the command, labelled as the by-hand route, because a session working without the plugin on its PATH still needs them and three cases pin them verbatim. The survivor sweep over the branch range reports nothing still standing |
