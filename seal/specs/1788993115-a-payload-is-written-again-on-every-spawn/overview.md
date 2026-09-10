# 1788993115-a-payload-is-written-again-on-every-spawn — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal a design is chosen against; fragments, never
             the shared file), `CONTRIBUTING.md` §What a change to a gate must
             carry, `docs/flow.md` §0.10.0, issue #292, this work item's
             `spec.md`, `plan.md`, `questions.md`, `routing.md` and the three
             phase records; `skills/code-review/orchestration.md` §The check a
             round runs reads everything, and only a write is narrowed
· evidence: `seal/ledger/1788993115-a-payload-is-written-again-on-every-spawn.md`,
             eight rows — the eight `seal/ledger.md` rows anchored on the
             Bootstrap section, removed there and re-stated at
             `skills/implement/orchestration.md`'s coordinate; five rows left in
             `seal/ledger.md` — over six anchors, the README row carrying two —
             re-read and re-verified. Unscoped read at
             `26e4236`: 1,059 ok · 0 drifted · 0 broken, records arm 0 refused
· verified: executed — the meter's module 17 passed with three mutations each
             turning its own case red; the plan's narrow set plus every module
             the branch touched, 553 passed and the one overview case this memo
             closes; `evidence-check .` exit 0; `survivor-check --range
             0bd135f..HEAD --exempt survivors.md` exit 0; `rider_check.py` and
             `claude_block.py --check` exit 0; ruff clean on the four Python
             files touched. read — every pointer coordinate the phase-4 prompt
             named. unverified — the table below

## Why this work exists

Every spawn of an agent paid for its whole startup payload again and nothing
said what that payload was made of; this work ships the meter that says so
with a basis on every token figure, and moves the first 13,727 bytes it
found addressed to a role that never acts on them out of the `smith`'s.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The after-number "from the same transcript" | `spec.md` item 9 and `plan.md`'s phase-4 row say `payload-after.json` comes from the same transcript as the before-run; run that way at `ff71c51`'s parent, the meter put the smith at 2.49 B/token against the 2.87 its spawn paid and reported +979 tokens on `agents/smith.md`, whose bytes had not moved | the meter was fixed in phase 4 (`6ddfa69`): with `--baseline` given, an agent whose smallest spawn is the one the baseline was calibrated from, over a different byte count, keeps the baseline's ratio, is labelled estimated throughout and says to take a spawn after the change; and a delta whose two totals rest on different bases sums the per-file token deltas. `payload-after.json` is then taken from the same transcript | `spec.md` §Scope item 1: *every token figure carries a basis … never a bare number*. A ratio derived by dividing a spawn's measured tokens by bytes it never read, and a row calling those bytes *the bytes the spawn read*, is a bare number wearing a label. The phase-4 row names no code, so this is recorded rather than assumed; both cases were seen red first and each mutation turned exactly its own case red |
| S3's sum clause | *the check's sum over the two `implement` files equals the file before the split* | left as measured and recorded: `skills/implement/SKILL.md` 32,522 B + `skills/implement/orchestration.md` 16,545 B = 49,067 B against 46,249 B before | the excess is the new file's 25-line header, the pointer section `SKILL.md` opens with, and the bullet this phase reworded; phase 2 measured the moved TEXT at 14,949 of `orchestration.md`'s characters, which is what the clause meant. Nothing was removed on the way |
| Which pointers phase 4 had to fix | `spec.md` item 5 and the phase-4 prompt name `agents/smith.md`, `templates/*.md`, `docs/*.md`, `README*.md` | none of those four pointed at a moved section: `agents/smith.md:127` names §3, `docs/review-chain-spec.md:704` §5, `CONTRIBUTING.md:84` §1's cost-of-a-question paragraph, `templates/sdd-round.md:68` the past-state reasoning in §3 — all of which stayed. The three that did point wrong were `hooks/mode-gate.py` (twice), a docstring in `tests/test_the_mode_question_is_asked_once.py`, and the moved Bootstrap bullet *the feedback rule below*, now naming `SKILL.md` §2 | each opened (§5); a docstring is read by a person the same as a document |
| Where the READMEs name the meter | the prompt said `session-cost` is named in the commands table *and the `bin/` wrappers paragraph* | one row after `session-cost --latest` in each edition; no wrappers paragraph names `session-cost` (`grep -n session-cost README*.md` returns the table row alone) | measured before editing |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite and the repository-wide lint and format check (this repository carries no typecheck step, so none is owed) | the orchestrator, once, after the review rounds settle |
| A measured after-number for the smith's payload — no spawn was taken after the cut, so `payload-after.json`'s smith figures are estimates at the before-ratio 2.87 | the orchestrator, with one `specseal:smith` spawn told *use no tools, reply with one word* and `payload-meter --calibrate` on that session's transcript |
| The exact token count of one file, and whether `general-purpose`'s built-in prompt is small enough to sit inside the harness constant (phase 1) | Q4's probe, in the next session started in this repository |

## Not done

- **`agents/smith.md`'s own routing paragraph stays.** Q7: it moves with the
  design gate in #84, so it moves once.
- **Without `--baseline` the meter cannot tell a stale transcript from a
  fresh one.** A spawn read the tree as it stood when it was made and
  nothing in a transcript says which tree that was; the detection this phase
  added compares the baseline's `over_bytes` for the same spawn file, which is
  the one fact the meter has. Q8 carries whether a stronger check belongs in
  the meter; the docstring says the rule.
- **A `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763`** (an
  escaped backtick in a docstring) prints on every run of that module. It
  predates this branch, the file is not in this work item's scope, and it is
  named here for the repository owner rather than fixed in passing.

## Fed back into the spec

Two clauses this work added that `spec.md` did not decide, each marked
**inferred during implementation**.

| Clause | Where it now lives | Inferred from |
|---|---|---|
| **A calibration belongs to the bytes the spawn read.** With `--baseline`, the same spawn over a different byte count keeps the earlier ratio and is estimated throughout | `skills/verify/scripts/payload_meter.py`'s docstring and `_same_spawn_over_other_bytes`; `tests/test_the_payload_meter_says_what_it_measured.py#test_calibrating_the_same_spawn_over_a_changed_tree_keeps_the_ratio_it_read` | the first after-run: 2.49 B/token and +979 tokens on an unchanged file |
| **A delta between two bases is summed over the files, never subtracted.** Bytes are exact either way | `payload_meter.py#delta_against`; `…#test_a_delta_between_a_measured_total_and_an_estimated_one_sums_the_files` | the same run: −6,773 tokens where the files summed to −4,691 |
