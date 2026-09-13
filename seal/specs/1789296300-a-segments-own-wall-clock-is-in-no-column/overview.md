# a segment's own wall clock is in no column — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/{spec,plan,questions,routing}.md`; `skills/agent-contract/SKILL.md` §§2, 3, 4, 6, 7, 9, 10, 14, 15; `skills/implement/SKILL.md` §§1–4; `CLAUDE.md` §*a change writes fragments, never the shared file* and §*a thing more than one party can have is named with whose*; `CONTRIBUTING.md` §*Running the checks* and *Both READMEs move together*; `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*; `docs/review-handoff-protocol.md` §*After the run — the per-segment bars*
· evidence: nine rows in `seal/ledger/1789296300-a-segments-own-wall-clock-is-in-no-column.md`; seven existing `seal/ledger.md` rows re-read and re-stamped for the section anchor this work drifted
· verified: executed — `bin/test tests/test_session_cost.py -q` (104 after round 1's fix pass; 100 at the handoff, which the proof block recorded as 98), `tests/test_a_segment_feeds_the_flow_log.py` (32), `tests/test_one_word_one_meaning.py` (15), `tests/test_no_real_identifiers.py` (2), `tests/test_docs_line_wrap.py` (23), `tests/test_a_script_says_which_interpreter_it_needs.py` (12), `tests/test_a_rider_reaches_its_file.py` (29), `evidence_check.py .` (1158 ok · 0 drifted), `ruff check`/`format --check` on every changed Python file, and the mode itself over all 43 real runs on this machine. Not executed — the full suite, the repository-wide lint and the typecheck (contract §2)

## Why this work exists

Every other kind of chain segment could be measured and a spawned agent's own
wall clock could not: on this harness the `Agent` result is written when the
spawn is accepted, so `--spawns` reports seconds for an agent that ran twenty
minutes, and the real interval sat between two rows and inside none of them.
`session-cost --segments` opens each segment's own transcript and prints it —
and the same walk answers #343, because an `Agent` call made inside a segment
is in that file too.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The name of the join function | `plan.md` phase 1: "`segment_rows()` matching each transcript under `subagents/` to a spawn result within the tolerance". Built as `measure_segments()` | the code's name | The behaviour `plan.md` describes is exactly what was built; only the name moved. `measure_segments` is parallel with the `measure_cycles` this file already had, and that pairing is what tells a reader the two modes are siblings. `plan.md` and `phases/phase-1.md` are corrected, and the phase record keeps the proposed name behind a `NAME NOT IN TREE` marker so the rename is not silent |
| What makes a segment unnamable | `spec.md`: "a nested transcript under another segment's directory, with no `Agent` call in the parent". Measured: this harness writes **every** segment flat under `subagents/`, subagents of subagents included — zero files below depth one across all 349 | the measurement | The spec's picture bundled two things that turned out to be independent. The join infers *unnamed* from the match failing, never from the path, so nothing needed repairing — and `subagent_transcripts` walks rather than lists, so the nested shape stays covered either way. Recorded because the frame's sentence would otherwise mislead the next reader. **Why this one was not corrected in place while the row above it was**, since a reader meets both here: what decides it is what the divergence IS, not which file carries it. A name that is not in the tree sends the next reader to a symbol that does not exist, so it was corrected wherever it appeared — `plan.md` and `phases/phase-1.md` both. A picture of the harness that measurement killed changes no instruction anyone follows: the join infers *unnamed* from the match failing and never from the path, and the nested case still ships. So it stands where it was written, in `spec.md` and in `plan.md` alike (`spec.md` :11, :111, :132, :155 and `plan.md` :20, :41, :100, :103), and this table is the correction |
| Whether a resumed file's slices each carry their own token figure | `plan.md` phase 3 is silent; the natural reading of "one row per slice" is that every column is per slice | the file's figure rides its first slice; later slices print a dash | Re-deriving tokens per slice means duplicating `token_totals`' keep-the-largest-per-message-id rule, and a streamed message whose rows straddled a boundary would be counted in both — which is #202's own failure shape rebuilt one reader over. Widening `token_totals` to take a time window would drift three ledger rows to refine a column this work item is not about |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Contract §2 makes them one act with one owner and this segment ran none of them; every narrow run it did take is listed in the proof block above | the sealer, spawned by the orchestrator after the review rounds settle |
| Every harness fact this mode rests on was measured on **one machine's harness**: that a segment transcript opens at its spawn's result within a second, that segments are written flat, and that a resume is marked by the literal sentence `The coordinator sent a message while you were working:`. Whether any of it holds on another harness is unmeasured. The mode is built to fail loudly rather than quietly — it prints the tolerance, both unmatched counts, and the idle gap it could not split — but nobody has seen it meet a second harness | the repository owner, whether a second harness is worth measuring or whether the loud-failure design is the whole answer |
| ✅ Which parity cases read the two READMEs' cheat-sheet rows — the framer's own named `unverified` item, answered by this segment 2026-09-13 | **None do.** The only case that reads the sheet is `test_the_cheat_sheet_does_not_offer_the_runner`, which reads `README.md` alone and asserts an absence. Nothing compares the two editions' rows. The parity requirement is `CONTRIBUTING.md` §*Both READMEs move together* plus `survivor-check` at the pull request, so both editions were edited |

## Not done

**The §6 line is not a gate, and making it one is left open on purpose.** It
notices and stops nothing, because the evidence is a transcript under the home
directory of the machine that ran the agent — in no commit, on no CI runner.
A later work item can turn the line into an exit code, and it will then be
choosing against readings rather than against a guess. Of the 43 runs on this
machine 13 already carry the line, and 12 of those name an agent this plugin
spawns, so those readings now exist — and the thirteenth is the reading that
says an exit code would have to tell the two apart.

**`delegated_s` is untouched.** The owner answered `questions.md` Q1
deliberately: it keeps the `Agent` call's own tool_use-to-tool_result
interval, so every `--spawns` reading published so far keeps the meaning it
was taken with. The owner may revisit it now that there is a per-segment
reading to compare against; #145's Q4 is where that row lives.

**A per-slice token column** — the divergence table above says why, and the
reason is a defect class rather than effort.

**`survivor-check` has no cheat-sheet row either**, noticed while answering
the README question and deliberately not fixed here: it is a different
command, and adding it would put a change outside this work item's scope into
a diff a reviewer is reading for something else.

## Fed back into the spec

- **The unnamable segment is unnamable because the parent made no `Agent`
  call, not because it is nested** — inferred during implementation, measured
  over 349 transcripts, and recorded as a ledger row. `spec.md`'s and
  `plan.md`'s wording about "a nested transcript" is the frame's picture of a
  shape this harness does not produce; a planner may overturn the emphasis,
  but the measurement stands.
- **The resume marker is a literal sentence rather than a row shape** —
  inferred during implementation. `skills/verify/SKILL.md` had prescribed the
  split in prose since #145 and nothing had ever asserted it against a file.
  The same row shape also carries two things that are not resumes, which is
  why the marker is narrower than the prose suggested.
