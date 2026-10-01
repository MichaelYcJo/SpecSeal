# Implementation Plan: the reading segments batch again, and the opening lives in a file

<!-- seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

Two edits and one meter. `agents/framer.md` gains the anti-stall opening,
reworded to bound the burst (a skeleton `spec.md` first, batches of about six
reads, large files by range), and the framer's own §10 number (1.4).
`docs/review-handoff-protocol.md`'s bars table gains a `framing` row and its
tying paragraph says `--segments` applies the bars by kind.
`session_cost.py --segments` then prints, under its table, every named row
whose kind has a bar and whose tools per turn sits under it, with the counts
and the protocol's caveats, and `--json` rows carry `kind` and `bar`. The
plain reading, `--spawns` and every number on the segments page are
unchanged. The ledger is kept true, and the frame's own transcript is the
first real reading the grade takes.

## Technical context

**The row already carries the kind.** `measure_segments`
(`skills/verify/scripts/session_cost.py` 1790–1800) labels each row with
`agent` = the spawn's `subagent_type` (`specseal:warden`, `specseal:smith`,
`specseal:framer`) and `named` = whether a spawn was joined; an unnamed row
and an own-file row (1839–1849) carry `agent ""`. `segment_slices`
(1634–1728) builds the row dicts and `numbers` = `analyse` with
`tools_per_turn` and `calls`, or `None` for a file that paired no call.
`segment_label` (2331–2355) is how a row is printed; the kind lookup takes
the basename of `agent` after its last `:`, so a plugin-prefixed name and a
bare one are one kind.

**Where the block goes.** `report_segments` (2449–2657): counts header,
column legend, the resumed and idle notes, the table loop ending at 2600,
`report_breaches` at 2601, then the token-column and three comparability
lines. The grade block is printed between the table loop and
`report_breaches`. Nothing above it changes, and no number anywhere on the
page does, so the three comparability lines gain nothing (#377's and #642's
lines exist because a NUMBER moved; here none does).

**The plain reading stays.** `report` (2098–2113) prints the blanket
advisory at `< 1.2`, and `tests/test_the_handoff_before_round_one.py`
438–452 reads that literal by regex against the protocol's sentence
*batching advisory below 1.2 and stays there*. Both stay as they are.

**The bars today.** `docs/review-handoff-protocol.md` 622–651: the table
(reviewing ≥ 1.8, implementing on `repeats = 0`, verifying exempt), the
small-round paragraph, the tying paragraph, the two-instruments paragraph.
`tests/test_the_handoff_before_round_one.py#test_the_protocol_names_a_bar_per_segment_kind`
(272–286) asserts the three rows by phrase and *never a refusal threshold*;
`bars_section` (300–315) scopes the two-instruments case to the section.

**The definitions today.** `agents/warden.md` 357–362 holds 1.89 and
*Independent reads and probes go out together* (pinned at 229–237 of the
same test module); `agents/smith.md` 273–276 holds 1.08–1.17 against
1.29–1.89 and *never obliged to fake a batch* (pinned at 240–269).
`agents/framer.md` holds no number and no opening; its §*What you read, and
how widely* (130–162) is where reading is described, and the new section
follows it.

**What constrains the wording.** `tests/test_a_moved_rule_leaves_its_definition.py`
refuses any 15 consecutive words of a contract section appearing in a
definition (`WINDOW = 15`, line 79; `copied`, 119–122), so the section is
written in the framer's own words and cites §10 by number.
`tests/test_chain_hooks_hardening.py#test_the_questions_are_collected_before_the_work_not_during_it`
(1110–) refuses a batching phrase inside a window that names a person
answering — the opening section is about reads, and keeps *ask*, *answer*
and *person* out of the sentences that say *batch*.
`tests/test_docs_line_wrap.py` holds `agents/framer.md` at 88 columns
(`LIMIT`, line 42; the file is listed at 134).
`tests/test_one_word_one_meaning.py` sweeps `session_cost.py`,
`skills/verify/SKILL.md` and `tests/test_session_cost.py` for *segments are
spawn cycles* and *orchestrator's segments* (396–404): the block's prose
uses neither.

**The sentence as it was typed.** The 0.12.3 routing files, folded by #497
and read at `8ff0ac59`: *told not to open with a parallel read burst and to
write a skeleton `spec.md` inside its first few calls*. #478's reading adds
the third: *read large files through `sed -n '<range>p'` rather than whole*.

**The confound, as far as the tree answers it.** #456 (read): the 0.12.2
framers — 1.48 and 1.64, and the two that stalled at 1.56 and 1.80 — ran on
`claude-opus-5[1m]`; #478's first framer with the prohibition read 1.00 on
the next release. So the prohibition, not a model change, is what separates
the 0.12.2 band from the 0.12.3 floor. The 0.15.1 framers on Fable 5.1 read
2.3–3.1 (#548, opened), and the 0.15.3+ readings at 1.04–1.12 are on Opus
5.5 with the prohibition. What no reading in the tree gives is a framer on
the current model WITHOUT the prohibition — until this frame, which is that
reading (`questions.md` Q1), and the first framer after this ships, with the
bounded opening in the file (Q2).

**Failure scenario of the chosen approach, six months out.** The bars live in
three places — the protocol's table, the definitions' numbers, the script's
constants — and one moves alone. The cross-pin case (S12) reads the script
and the protocol; the definition-to-protocol tie is the existing pair of
cases (warden 1.89 beside the protocol's 1.8 are different numbers on
purpose: the measurement and the bar). A fourth kind arrives with no bar and
reads as ungraded: the block prints the ungraded count and the kinds it
knows, so the silence is counted rather than silent. A harness renames the
`subagent_type` values: every row reads ungraded and the counts say so on
the page.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Leave the opening in spawn prompts (the state the sweep found) | A rule kept only in whoever last wrote a prompt goes missing without a trace (#107); the sweep found it in no file, which is this ticket | rejected — protocol §*What every spawn prompt used to carry* |
| Carry the 0.12.3 sentence into the file as typed (*do not open with a parallel read burst*) | Every framer reading at 1.00–1.12 carried it; the readings without it on the same model line were 1.48–1.64 (#456). Writing the prohibition into the file fixes the floor at 1.00 | rejected — the ticket's recommendation 1 rewords it, and the grounds are the readings |
| No opening at all, and trust the watchdog not to fire | The only framers without the sentence on this harness since 0.12.2 are this frame's run, unmeasured at framing time; two spawns were lost before it. A bound costs one sentence | rejected — bound, and measure (Q1, Q2) |
| Put the bound as a hard number nobody measured (e.g. *at most three*) | The 0.15.1 framers batched 2.3–3.1 and finished; a bound under what finished is the prohibition by another name | rejected — about six, overturnable (A1), with Q1 reading what this frame actually sent |
| Grade in the plain reading too, by reading the agent off the file | A lone transcript carries no `subagent_type`; the kind is in the parent's spawn. And the plain reading is the comparability baseline since 0.9.4 | rejected — ticket's recommendation 2, last clause |
| Replace `report`'s `< 1.2` with a per-kind threshold | Same as above, and the `1.2` cross-pin case and its protocol sentence would both move for a reading that still cannot tell kinds | rejected |
| A `bar` column in the table | `test_the_printed_segment_table_names_each_agent_and_its_own_span` pins the row shape by regex, and every posted page would change shape for a value most rows do not have | rejected — a block under the table, additive |
| Exempt a verifying warden round by reading `description` for *verif* | Free text the orchestrator types; a grade keyed to prose (§5). A round described differently would be graded, one described that way would not, and nothing on the page says which happened | rejected — print the exemption, a reader applies it |
| Bars read from `docs/review-handoff-protocol.md` at run time | The script runs from the installed plugin cache in repositories that have no such document | rejected — constants, with a cross-pin case |
| Warden bar at 1.89 (the definition's number) | 1.89 is the one measured round the bar came from; the bar is the protocol's 1.8, and policy outranks a definition | rejected — 1.8 |
| Framer bar from the Fable band (≥ 2.3) | One release, one model, three spawns, and the ticket's own target is 1.4 under the five-release band | rejected — 1.4 (A2) |
| Bars for `sealer` and `scribe` | No band measured for either; a number nobody produced is the counterfeit `agents/framer.md` refuses | rejected — ungraded, counted, named |
| A non-zero exit when a row is under its bar | *Never a refusal threshold* (protocol); and the 23-call round that read 1.64 doing everything right | rejected |
| Touch `agents/warden.md` | Nothing in the ticket asks; its number and bullet are listed as the state to keep | rejected — out of scope |
| Bump the protocol's draft to 1.3 | The one case reading the draft requires only that the two lines agree; #639's edit to the same table bumped nothing | rejected — no bump; the smith may overturn if the document's own convention says a row bumps (Q5) |
| Skip the SKILL.md and README clauses | The documents describing the page would then describe a page that prints one line fewer than it does — the first frame of `agents/framer.md` omitted both READMEs and phase 1 hit it | rejected — I8 |

## Phases

Vertical slices — each phase ends with something runnable and verified.

Each phase runs the module it edits and the modules that read what it
edited, named in its row; each new case is seen red first (contract §15) —
against the base, or with the sentence it pins deleted — and the phase record
says which. No phase runs the full suite, lint or typecheck (contract §2); the
sealer owns that. Items A (#641) and B (#638) run as parallel chains on the
same release branch. Phase 4 merges `origin/release/v0.17.0` in only where
one of them has landed there and touches what phase 4 reads, and then takes
`evidence-check` at the merged tip. **Never a rebase** — every round record
names this branch's commits by `Target SHA` (`docs/release-checklist.md` §0;
corrected by the orchestrator before approval, where the frame said rebase).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The opening and the number, in `agents/framer.md`** (spec I1, I2): one section after §*What you read, and how widely* — skeleton `spec.md` inside the first few calls; a read batch of about six reads or ranges, never the whole list, with §10 cited by number and in the framer's own words; a large file by range; the bar 1.4 and the band 1.46–1.79 with the flow-log coordinates; no prohibition on parallel reads. The changelog fragment is opened with the entry | `tests/test_the_handoff_before_round_one.py`: new cases for S1 and S2, each seen red with the sentence it pins deleted; the existing three batching cases green. Then the definition-reading modules, green unchanged: `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_chain_hooks_hardening.py`, `tests/test_docs_line_wrap.py`, `tests/test_the_rules_have_one_owner.py`, `tests/test_a_question_says_who_can_answer_it.py`, `tests/test_one_word_one_meaning.py` | |
| 2 | **The policy and the documents** (I3, I4, I8): the `framing` row and the rewritten tying paragraph in `docs/review-handoff-protocol.md`; the step-1 clause in `skills/verify/SKILL.md` §*Measure the segment*; the `session-cost --segments` cell in `README.md` and `README.ko.md` | `tests/test_the_handoff_before_round_one.py`: `test_the_protocol_names_a_bar_per_segment_kind` extended for the `framing` row (red at the base), a case that the tying paragraph names `--segments` (red at the base), `test_the_advisory_and_the_tying_paragraph_name_one_value` and the draft case green unchanged; `tests/test_a_segment_feeds_the_flow_log.py` green; the README-reading cases green (`grep -l README tests/` at the tip names them) | |
| 3 | **The grade** (I5, I6, I7): the kind-and-bar constants beside `LABEL_WIDTH`, the lookup by basename, `kind` and `bar` on every row, the block under the table with the counts, the exemption line, the three caveats, and the cross-pin. Mutants, each killed: smith rows graded; a row at exactly its bar named; an unknown kind graded as warden; the counts line printed while a row is under its bar; the verifying sentence deleted; the bar read as `>` instead of `>=` | `tests/test_session_cost.py`: cases S4–S11, each red before the block exists; every existing `--segments`, `--spawns`, own-file and plain-reading case green unchanged, `test_the_printed_segment_table_names_each_agent_and_its_own_span` and `test_the_report_names_batching_when_every_turn_sent_one_call` named. `tests/test_the_handoff_before_round_one.py`: the cross-pin case (S12), seen red by moving the script's constant alone. `tests/test_one_word_one_meaning.py` green | |
| 4 | **The ledger and the reading** (I10, I11): merge the release branch in where A or B has landed (never a rebase); `evidence-check` at the tip names the drifted rows and each is re-read and re-stamped where it stands; the `seal/releases/0.4.0.md` row corrected in place with a `Corrected 2026-10-..` note; new rows in `seal/ledger/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file.md`. Then the tip's `--segments` over the orchestrating session's transcript (the path the spawn prompt hands over, or `~/.claude/projects/<slug of the worktree>/<session>.jsonl` found by newest): this frame's row on the page, graded against 1.4, and its largest batch (the most calls in one turn, read with `--json`) go into `phases/phase-4.md` and the changelog entry, labelled executed and as one reading. No probe file is left; a transcript path in any record is written `/Users/x/…` | S14: `evidence-check`'s exit code read directly (`cmd >/dev/null 2>&1; echo $?`), no un-re-read DRIFTED row of this work's; `tests/test_a_merge_cannot_silently_drop_a_correction.py` and `tests/test_no_real_identifiers.py` green. S15: the page and the two numbers in `phases/phase-4.md` | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

None that a deployer meets: no migration, no environment variable, no
dependency. Two things a reader of readings meets:

- `--json` segment rows gain `kind` and `bar`; nothing is removed or renamed,
  so a consumer reading the old keys is unaffected.
- A `--segments` page posted to the flow log with `--post` now carries the
  grade block inside its fenced reading. Readings posted before this release
  carry none, which is a line present or absent and not a number moved, so
  no comparability line is added for it.
