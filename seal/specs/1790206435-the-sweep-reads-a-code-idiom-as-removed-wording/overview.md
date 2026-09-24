# the sweep reads a code idiom as removed wording — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/review-chain-spec.md` §*The survivor sweep*; `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `seal/specs/1790206435-…/spec.md` (Grounding, Scope, The measured state, User scenarios S1–S16, Data & interfaces, Judgments 1–9), `plan.md` (Technical context, Alternatives, Phases, Operational impact), `questions.md` Q1–Q6, `routing.md`; `docs/review-handoff-protocol.md` §*The handoff before round 1*; `templates/sdd-phase.md`, `templates/sdd-overview.md`
· evidence: rows P1–P3, C1–C3, U1–U2 in `seal/ledger/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording.md`; nine `seal/ledger.md` rows re-read and re-stamped with a dated note (S3 and S6 of `1788873640`, G5 and G6 of `1788912166`, S1 of `1789211172`, the 12,100-survivors row of `1790076070`, G5 of `1790138190`, E1 and E4 of `1790174139`)
· verified: executed — `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` at each phase (70 → 81 → 89 → 91 passed), the four real-range sweeps at every phase, the founding-case sweeps, twenty mutations from Python with the file restored byte-identical, Q5's three probes, the branch's own sweep with every `survivors.md`, `bin/evidence-check --reverify .` then `--strict .`, `bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/`, `uvx ruff check` and `uvx ruff format --check` over the edited files, and the other modules that read `survivor_check.py`; read — the ten `survivors.md` files' grounds cells for Q3's count. Not run: the full suite, lint and typecheck (the sealer's)

## Why this work exists

The survivor sweep read a line of code as a sentence, a released changelog
entry as prose somebody could correct, and a shipped work item's dead
declaration as a line for every run; now a `.py` file's prose is what it
says, a released section and a gathered fragment are records, and an
unresolved declaration prints only to the run it addresses.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S6's count for B's range after phase 1 | *B 9 → 9, prose coordinates unchanged* / 9 → 8: `seal/ledger.md:2053` was scored at 2.47 against a docstring joined to three assert literals by code, and one literal per sentence its best source is one run at 1.00 | the case pins the new set | `questions.md` Q2's *Moved* option: *the case pins the new set and `phases/phase-1.md` names each moved coordinate with its score before and after* |
| S12's count for B's range after phase 2 | *B 9 → 8* (7 from phase 1's 8) / 8 → 8: `CHANGELOG.md:2090` gone and `survivor_check.py:142` joined at 1.61, 1.51 before with nine gathered fragments in the pool | the case pins the new set | `plan.md` §*Operational impact*: *none can see a new one from phases 1–3 except through the weighting*; the same Q2 option |
| S4's shape | *a case over a range that removes a sentence whose words are `first half second half`* / the case reads the sentence keys of the line directly | the reader case | the spec's own line reads `first half name second half` under the whole-file reading, so no range removing `first half second half` was ever answered by it and a range case would have been green before; the end-to-end shape is S1 (`phases/phase-1.md`) |
| `STRUCTURE_TOKENS` | `plan.md`: *the kept kinds are read off the module by name*, and by implication every other kind blanked without a sentence end / five line-structure kinds are not in the set | the measured set | `NL`, `NEWLINE`, `DEDENT`, `ENDMARKER` and `ENCODING` changed no output under mutation, because the position guard writes nothing past a line's text; a member that cannot change the answer misplaces where the joining lives (`phases/phase-1.md`) |
| Ledger rows the design drifts | `spec.md` §*Data & interfaces* lists S3 of `1789211172` and E2, E5 of `1790174139` on the docstring section / the heading anchor did not drift when a paragraph was added under it; nine rows on `corrected`, `corpus` and `whole_range` did | re-read and re-stamped the nine that drifted | `bin/evidence-check --strict .` at `c44bcf61`: 3 drifted anchors, 9 rows |

## Not verified

| Item | Who must answer |
|---|---|
| S15 and S16 at the seal: the `survivors` arm over the finished branch prints zero `unresolved` lines and the `ledger` arm is clean, on the tree the sealer reads | the sealer, in the last round record's `Broad gate` cell |
| the full suite, `uvx ruff check .` and `uvx ruff format --check .` over the whole tree | the sealer (`agent-contract` §2) |
| the rename shape found under Q5 — a whole file moved as a rename with one sentence reworded is silent — reaches an issue with the paste-ready repair in `phases/phase-3.md` | the orchestrator, who can post; this agent cannot (`agent-contract` §6) |

## Not done

- **`--no-renames` on the two `git diff --name-only` calls.** Q5's third
  probe showed a file moved as a rename (`R096`) with one sentence reworded
  is silent: the old path never enters `corrected`'s list, so the reworded
  sentence is never removed and its copy elsewhere stands unreported. It
  changes what the range reads — a gate change with its own row in the gate
  table and a case seen red first — and it is outside this item's three
  tickets, so it is handed back rather than taken. `seal/ledger/…` row U2
  and `phases/phase-3.md` carry the measurement.
- **Joining a `#` comment block into one paragraph**, and **code in files
  that are not `.py`** — `spec.md` §*Out*, both the repository owner's.
- **The twenty `survivors.md` rows of the two classes** — 17 code-idiom, 3
  released-changelog, of 56 path rows in seven files (Q3, read 2026-09-24).
  Each now silences nothing, and each stays: a dead row is not edited
  (spec judgment 8), and the directories retire with their work items.

## Fed back into the spec

- *inferred during implementation*: a sentence in a `.py` file starts at
  its first literal, so a coordinate the sweep names for a `.py` file is
  the literal's own line rather than the head of the code block around it
  (#269's pin: 447 → 450).
- *inferred during implementation*: the joining of two literals across a
  line break lives in `python_prose`'s position guard, not in a list of
  line-structure token kinds; the five such kinds change no output.
- *inferred during implementation*: a verbatim move between files is silent
  by git's rename detection before `wanted` is reached, and a rename with a
  small rewording is silent for the same reason — judgment 7's mechanism
  holds for a split, where both files remain, and not for a rename.
