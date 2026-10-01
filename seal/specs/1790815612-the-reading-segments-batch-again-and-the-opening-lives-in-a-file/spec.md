# Feature Specification: the reading segments batch again, and the opening lives in a file

<!-- seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Ticket #640, release 0.17.0's item C. Two things, and they are one ticket
because one meter has to read what the other changes.

1. The framer's anti-stall opening — typed into spawn prompts since 0.12.3
   and in no file — goes into `agents/framer.md`, reworded to bound the
   opening burst rather than to forbid batching. The definition also gains
   §10's number for its own kind, as `agents/warden.md` and `agents/smith.md`
   already carry theirs.
2. `session-cost --segments` grades each row's tools per turn against the
   bar of the row's kind — warden and framer have one, smith is exempt — in
   place of nothing: today the per-kind bars exist only in
   `docs/review-handoff-protocol.md` and the one advisory the script prints
   is the plain reading's blanket `< 1.2`, which the ticket quotes #197 on:
   it reads 1.00 on every well-behaved implementer forever, so nobody acts
   on it. The plain reading does not change.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-handoff-protocol.md` §*After the run — the per-segment bars* | The bars are per kind and are a lens, *never a refusal threshold*: reviewing ≥ 1.8, implementing on `repeats = 0` and never tools per turn, verifying exempt. This work adds a `framing` row and rewrites the tying paragraph, which today says the script *cannot tell a reviewer's transcript from an edit-test loop*. For `--segments` that is no longer true: a row's kind is the `subagent_type` of the spawn it was joined to. The plain reading still cannot tell, so its advisory sentence stays as it is |
| `docs/review-handoff-protocol.md` §*What every spawn prompt used to carry* | A rule kept only in whoever last wrote a prompt goes missing without a trace (#107). *Nothing that was a rule here reaches an agent by being typed any more.* The anti-stall opening is exactly such a rule, found by the 2026-09-28 sweep in no file. This is the ground for recommendation 1 and for why its home is `agents/framer.md` rather than `skills/implement/orchestration.md` |
| `skills/agent-contract/SKILL.md` §10 *Batch independent reads and runs* | The rule is the contract's; *the numbers that judge each are in that agent's definition*. The framer has no number today (read at `cd24f516`). The wording this work adds to `agents/framer.md` is the framer's own application and must not carry §10's sentences: `tests/test_a_moved_rule_leaves_its_definition.py` refuses any 15-word run copied from a contract section |
| `agents/framer.md` §*Why the frame is not the builder's to draw* — *Do not promise a saving* | Nothing here promises the next flow log's medians rise. The ticket's *How to verify* (warden ≥ 1.3, framer ≥ 1.4 medians) is a reading the 0.17.0 log takes after the release; it is a measurement row in `questions.md`, not an acceptance criterion |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Neither change is a gate: the grade refuses nothing and exits 0, and the opening is prose an agent reads. No prompt budget changes — zero questions before, zero after. Stated so a reviewer does not look for the four items |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* · §*a removal is not one — nor is an edit* | New ledger rows go to `seal/ledger/<work-item-id>.md`. One existing row's grounds go false — `seal/releases/0.4.0.md` row *The bars are written beside the meter they interpret* says *the script cannot tell segment kinds apart, the orchestrator can* — and is corrected in place with a `Corrected <date>` note. Rows anchored on units this work edits are re-read and re-stamped where they stand |
| `CLAUDE.md` §*Repo rule — no real identifiers* | Fixtures and the definition's examples use neutral values. A transcript path quoted anywhere in a record is written `/Users/x/…` |
| `skills/implement/SKILL.md` §3 (the SDD ladder) | Both halves alter what somebody reads and acts on — an agent's instructions and a report's text — and the second names a value a segment is judged against. Top rung, hence this frame |

## Scope

### In

**I1. The opening, in `agents/framer.md`.** A section of its own, placed after
§*What you read, and how widely* (the smith may move it; the content is
fixed), saying three things in the framer's own words:

- **The first write is early.** A skeleton `spec.md` — the template, with the
  title and the mark line filled — is written inside the first few calls.
  It is the one progress signal the harness's no-progress watchdog reads
  from a framer that is otherwise only reading, and it is what a spawn lost
  to that watchdog leaves behind instead of nothing (0.12.2 lost two spawns
  and both wrote nothing — #456, read).
- **A read batch is bounded, and batching is not forbidden.** The files one
  coordinate names go out together, as §10 says; what is bounded is the
  size of one call — about six reads or ranges, never the whole reading
  list in the opening call. The number is a default a person may overturn
  (`questions.md`, assumption A1); its grounds are this frame's own run,
  which sent batches of five to seven on every turn of its gather and did
  not stall (a measurement, Q1), and the 0.15.1 framers at 2.3–3.1 tools
  per turn that finished (#548, opened).
- **A large file is read by range.** The `Read` tool pages and says when a
  view is partial; `sed -n '<a>,<b>p'` is the shell form. A file is opened
  whole only where its size is known to fit a page.

What the section must NOT say: *do not open with a large parallel read
burst*, or any sentence that reads as a prohibition on parallel reads. The
rewording is the ticket's recommendation 1, and the grounds are the readings:
every framer reading at 1.00–1.12 since 0.12.3 (#478, #601, #619, #629) was a
spawn whose prompt carried that prohibition, and the 0.12.2 framers without
it — on the same model line, `claude-opus-5[1m]` (#456, read) — read
1.48–1.64.

**I2. §10's number for the framer, in `agents/framer.md`.** One bullet or
sentence in the same section: the bar is **1.4 tools per turn**, and the band
it comes from is 1.46–1.79 over 0.11.2–0.12.2 (#370 1.46 and #456 1.48 and
1.64 opened; #376 and #385 read from the ticket), with 2.3–3.1 on 0.15.1
(#548 opened). The sentence says the bar is a lens and names no saving.

**I3. A `framing` row in the protocol's bars table**
(`docs/review-handoff-protocol.md` §*After the run — the per-segment bars*):
`| framing | tools per turn **≥ 1.4** | <grounds> |`, grounds in the same
shape as the reviewing row's — a frame is a wide read of independent
documents (#263), the band, and that the readings under it each carried the
prohibition. The existing three rows do not change.

**I4. The tying paragraph of that section is rewritten in place.** It keeps
the sentence `tests/test_the_handoff_before_round_one.py#test_the_advisory_and_the_tying_paragraph_name_one_value`
pins — the plain reading *prints its batching advisory below 1.2 and stays
there* — because the plain reading is unchanged and a lone transcript carries
no kind. It adds that `--segments` applies the bars above by kind, because a
row's kind is the `subagent_type` of the spawn it was joined to, and that a
row with no kind is not graded. The sentence *the script cannot tell a
reviewer's transcript from an edit-test loop* is narrowed to the plain
reading. No draft bump: the one case reading the draft number requires only
that the title and the Status line agree, and the earlier edit to this
table's `verifying` row (#639) bumped nothing.

**I5. The grade on the `--segments` page.** Under the table and before the
§6 block, a block headed by one line in the page's own voice, printing:

- one line per **named** row whose kind has a bar and whose
  `tools_per_turn` sits under it: the row's label, its ratio, the bar, and
  the kind — e.g. `specseal:warden  1.07 tools per turn against the
  reviewing bar of 1.8`;
- when no graded row is under its bar, one line saying so with the counts —
  graded, exempt, ungraded — because every count prints even when they
  agree (`report_segments`' own rule);
- one line naming the exemption and the ungraded: smith rows are not graded
  (an edit-test loop is serial; the protocol judges it on `repeats = 0`),
  and a row with no bar — a kind the table does not know, a row the parent
  could not name, an own-file row — is ungraded and counted;
- the protocol's caveats, once: the bar is a lens for rounds of ordinary
  size and never a refusal threshold; a small round has few independent
  batches to rise on; and a warden's verifying round is exempt by the
  protocol, which this page cannot tell from a finding round, so a reader
  applies that exemption by hand.

A row with `numbers` at null (no paired call) is ungraded. Nothing on the
page above the block, and no number anywhere on it, changes. The exit code
stays 0.

**I6. The kinds and bars are constants in the script**, keyed by the
basename of `subagent_type` after its last `:` (`specseal:warden` and
`warden` are one kind): `warden` 1.8, `framer` 1.4, `smith` exempt. The
values match the protocol's table and a case reads both files so that one
moving alone turns red (the shape of the existing `1.2` cross-pin).

**I7. `--json` rows gain two keys**, `kind` (the basename, `""` where
unnamed) and `bar` (the number, or `null` for exempt and unknown kinds).
Every existing key and value is unchanged.

**I8. The three documents that describe the page say what it now prints**:
one sentence in `skills/verify/SKILL.md` §*Measure the segment, and feed the
flow log*, step 1 (the row columns list gains *and, under the table, which
rows sit under their kind's bar*), and the `session-cost --segments` row of
`README.md` and `README.ko.md`. Each is a clause added, not a rewrite.

**I9. Tests.** Every new sentence or line a person reads is pinned, and
every case is seen red first (contract §14, §15):

- `tests/test_the_handoff_before_round_one.py`: the framer's definition
  carries the opening (skeleton first, the bound, ranged reads) and its
  number; the protocol's `framing` row; the tying paragraph names
  `--segments`; the cross-pin between the script's constants and the
  protocol's table values.
- `tests/test_session_cost.py`: a warden row under 1.8 is named with the
  bar; a framer row under 1.4 is named; a smith row at 1.00 is never named
  and the exemption line prints; a row meeting its bar is not named; a run
  whose graded rows all meet their bars prints the counts line; an unknown
  kind, an unnamed row and an own-file row are ungraded and counted; the
  `--json` keys; the plain reading of the same transcript prints the
  existing advisory unchanged; `--spawns` output unchanged.
- Existing cases that must stay green unchanged: the three batching cases
  at `tests/test_the_handoff_before_round_one.py` lines 229–282 (warden's
  `1.89`, smith's ranges, the protocol's `≥ 1.8`), the `1.2` cross-pin
  (lines 438–452), `tests/test_session_cost.py#test_the_printed_segment_table_names_each_agent_and_its_own_span`
  (the row regexes), and the definition-reading modules named in
  `plan.md`'s phases.

**I10. The ledger.** The 0.4.0 row corrected in place; every row
`evidence-check` names at the tip re-read and re-stamped; new rows for I1,
I5–I7 and the cross-pin in `seal/ledger/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file.md`.

**I11. The measurement the ticket's item 3 asks for, as far as this item
can take it.** The tip's `--segments` is run over the orchestrating
session's transcript, so that this frame's own row — Fable 5.1, prompt
without the prohibition, definition without the opening — is the first real
reading of the grade block and the control for the model confound. Its tools
per turn and its largest batch go into `phases/phase-4.md` and the changelog
entry. No claim is drawn from it beyond what one reading supports.

### Out

- **`agents/warden.md`'s wording.** Its number (1.89) and its batching
  bullet stand; the ticket lists them under *Where it lives* as the state to
  keep. The warden medians' drop has no sentence attributed to it; the grade
  is what surfaces it per round.
- **The plain reading's advisory** (`session_cost.py#report`, `< 1.2`) and
  `--spawns`. Comparability with every reading published since 0.9.4; the
  ticket's recommendation 2 says so in its last clause.
- **A refusal, an exit code, or a gate on the bar.** The protocol says
  *never a refusal threshold*.
- **Bars for `sealer` and `scribe`.** No band has been measured for either;
  they print as ungraded, by name, which is the counted silence rather than
  the silent one.
- **Exempting a verifying warden round by reading the spawn's
  `description`.** It is free text the orchestrator types; a rule keyed to
  it is a rule keyed to prose (§5). The page prints the exemption for a
  reader to apply.
- **Removing the sentence from spawn prompts.** It lives in no file in the
  tree, so there is nothing to edit; the protocol already says a prompt
  repeating a rule a definition carries is redundant rather than wrong.
- **The orchestrator's own floor** (1.00 over 953 calls, #51). Context in
  the ticket, not a recommendation in it.
- **The cause of the 0.12.2 stalls.** #478 calls it one observation; this
  item bounds the burst and measures, it does not explain.
- **The next flow log's medians** (`questions.md` Q3).

## User scenarios & acceptance *(mandatory)*

One row per scenario — these become the review's stage-1 checklist and the
regression tests' skeleton.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the opening is in the definition | Given `agents/framer.md` at the tip, when read whole, then a section says a skeleton `spec.md` is written inside the first few calls, a read batch is about six reads or ranges and never the whole list, and a large file is read by range; and no sentence forbids parallel reads or names a *read burst* as a thing not to do | a case in `tests/test_the_handoff_before_round_one.py` asserting the three claims by phrase and the absence of the prohibition; `tests/test_a_moved_rule_leaves_its_definition.py` green (no §10 run copied); `tests/test_chain_hooks_hardening.py#test_the_questions_are_collected_before_the_work_not_during_it` green (no batching phrase inside a window naming a person answering); `tests/test_docs_line_wrap.py` green at 88 |
| S2 the framer carries its number | Given the same file, then it names 1.4 tools per turn as the bar for its kind and the band 1.46–1.79 it comes from, and promises no saving | the same module; `tests/test_the_rules_have_one_owner.py` green |
| S3 the protocol has a framing bar | Given `docs/review-handoff-protocol.md`, then the bars table carries a `framing` row at `tools per turn **≥ 1.4**` with grounds, the other three rows unchanged, and the tying paragraph still says the plain reading's advisory is below 1.2 and now says `--segments` applies the bars by kind | `test_the_protocol_names_a_bar_per_segment_kind` extended; `test_the_advisory_and_the_tying_paragraph_name_one_value` green unchanged; `test_the_title_and_the_status_section_agree_on_the_draft` green |
| S4 a warden row under the bar is named | Given a run with a warden segment at 1.07 tools per turn, when `--segments` prints, then a line under the table names that row, 1.07, the reviewing bar 1.8 | `tests/test_session_cost.py`, a fixture built from `run_with_segments`' shape with a warden file of several single-call turns |
| S5 a framer row under the bar is named | Given a framer segment at 1.00, then a line names it against the framing bar 1.4 | same module |
| S6 a smith row is never graded | Given a smith segment at 1.00, then no line names it, and the exemption line says why | same module; the mutant that grades smith rows turns it red |
| S7 a row meeting its bar is silent, and the counts print | Given a warden row at 1.89 and a framer at 1.64, then no row line prints and one line says every graded row meets its bar with the three counts | same module |
| S8 no kind, no grade | Given a row the parent could not name, an own-file row, and a `specseal:scribe` row, then none is named under a bar and the ungraded count holds all three | same module, reusing the unnamed and own-file fixtures |
| S9 the caveats are on the page | Given any `--segments` page with at least one row, then it says the bar is a lens and never a refusal, that a small round has few batches to rise on, and that a verifying round is exempt and cannot be told apart here | same module; one case per sentence's deletion seen red |
| S10 nothing else moves | Given the fixtures every existing `--segments`, `--spawns` and plain-reading case uses, then every existing assertion passes unchanged, and the plain reading of a 1.00 transcript still prints the `batching` advisory | the existing cases, run at the tip; `test_the_report_names_batching_when_every_turn_sent_one_call` green |
| S11 `--json` carries kind and bar | Given `--json`, then each segment row has `kind` and `bar`, the page's named rows are exactly the rows with a non-null `bar` and `tools_per_turn` under it, and every previously present key is unchanged | same module; extends `test_an_own_files_json_carries_the_rows_the_page_prints`' pattern |
| S12 the constants and the policy agree | Given the script's per-kind constants and the protocol's table, then the warden value equals the reviewing row's and the framer value equals the framing row's, read out of both files by regex | a cross-pin case in `tests/test_the_handoff_before_round_one.py`; moving either alone is seen red |
| S13 the documents describe the page | Given `skills/verify/SKILL.md` step 1 and both README rows, then each says the page names rows under their kind's bar | `tests/test_a_segment_feeds_the_flow_log.py` and the README-reading cases green; a phrase assertion for the new clause |
| S14 the ledger stays true | Given the tip, then `evidence-check` exits 0 with no un-re-read DRIFTED row of this work's, the 0.4.0 row carries a `Corrected 2026-10-..` note, and the fragment holds the new rows | `evidence-check` exit code read directly (§1) |
| S15 the frame is measured | Given the orchestrating session's transcript, when the tip's `--segments` reads it, then this frame's row is graded against 1.4 on the page, and its ratio and largest batch are in `phases/phase-4.md` | executed in phase 4 and recorded; no claim beyond the one reading |

## Data & interfaces

- `skills/verify/scripts/session_cost.py`: new module constants for the
  kinds and bars beside `LABEL_WIDTH` (line 2328); a kind-and-bar lookup
  from `row["agent"]`; two keys added to each row `segment_slices` builds
  (lines 1673–1727), or added where `measure_segments` assembles labels
  (lines 1790–1800), so an own-file row (agent `""`) reads `kind ""`,
  `bar null`; a block in `report_segments` after the table loop (line 2600)
  and before `report_breaches` (line 2601). `report` (lines 2098–2113) and
  `report_spawns` untouched.
- `--json`: `segments.rows[*].kind`, `segments.rows[*].bar`. Additive.
- `docs/review-handoff-protocol.md` lines 622–651: one table row, one
  paragraph rewritten.
- `agents/framer.md`: one new section.
- `skills/verify/SKILL.md` §*Measure the segment*, step 1 (the column list
  at *the agent, its own span, calls, tools per turn, mean gap and
  tokens*); `README.md` line 280 and `README.ko.md` line 272, the
  `session-cost --segments` cell.
- Ledger anchors that drift and are re-read: every row on
  `session_cost.py#report_segments`, `#main`, `#segment_slices` or
  `#measure_segments` (`seal/releases/0.15.7.md` rows at lines 13, 15, 16,
  33); every row on `skills/verify/SKILL.md#"## Measure the segment, and
  feed the flow log"` (`0.8.0.md` 104, `0.8.2.md` 41 and 145, `0.9.5.md` 12,
  16, 45, 54, `0.15.7.md` 17, 33); every row on
  `docs/review-handoff-protocol.md#"### After the run — the per-segment
  bars"` (`0.4.0.md` 114, `0.8.2.md` 42, `0.15.7.md` 41); `0.6.0.md` L9 on
  §10 re-read (the framer now holds its own number, which is the claim).
  Counted at `cd24f516`; items A and B land in parallel and the tip decides
  (`questions.md` Q4).

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

Framed 2026-10-01 by framer, before the build.
