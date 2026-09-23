# survivors.md silences what it quotes — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/review-chain-spec.md` §*The survivor sweep — a corrected sentence standing somewhere else*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `CLAUDE.md` §*a change writes fragments*; `spec.md`, `plan.md`, `questions.md`, `routing.md` of this work item; `seal/follow-up.md`'s row on the range half; #507, #308, #460, #304 with their comments; `survivor_check.py`'s docstring §*What is excluded* and §*The escape*
· evidence: `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` rows E1–E5; `seal/ledger.md` rows re-stamped with `--reverify` and re-read: `corrected` (S3 of `1788873640`, S1 of `1789211172`), `corpus` (S6 of `1788873640`), `OWNER_DIR` (G5 of `1788912166`), the docstring section and its case (S3 of `1789211172`), the path-list case (S2 of `1789211172`)
· verified: executed — the module's 69 cases at each phase boundary (70 after round 1's fix), eleven red runs over ten cases seen red first (6 + 4 + 1 across the phase records, the docstring case counted once per extension) and both arms of the parametrised pool case red in the round-1 fix pass, 8 mutations red, the three pull-request ranges measured three times with and without `--exempt` and with the file deleted in a scratch clone, the branch's own sweep, `evidence-check --strict`, `unverified-check --baseline`, ruff on the touched files; read — the four tickets, the review-chain spec's folded statements, the module's other readers of a path (S8); unverified — the table below

## Why this work exists

A `survivors.md` row was supposed to be read against the survivor it quotes and printed with its grounds; instead, committing the file removed the survivor from the search on both sides, and on three pull requests 29 of 36 rows were never consulted. Now the file, a phase record and a round record are all out of the search by the shape of their path, a row is consulted and printed, and a deeper exemption file has an owner to be refused against.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Q3's instrument | `questions.md` Q3: *blank those files' quoting sentences in a probe commit and compare* / measured in-process, the module's predicate widened for one run to also exclude the range's `overview.md`, `changelog.md` and ledger fragment on both sides | in-process | A probe commit inside the range turns the blanked sentences into removed wording, so the comparison is between two different ranges rather than two readings of one. `phases/phase-1.md` §*Q3* |
| S6's pool half, red direction | `spec.md` S6: *for the pool half, a phase record reported as a survivor* / seen red at exit 0 with nothing reported | the case pins both, on two pool sizes | A fourth carrier halves the weight of every phrase it quotes, so on the frame's own four-file fixture the record dilutes rather than reports, and the `named` assertion could never be the one that failed there (round 1, finding 1). The case is parametrised over 4 and 33 files: the first arm goes red at exit 0, the second by naming the record beside `guide.md`. `phases/phase-2.md` |
| The frame's read claim about #528 | `spec.md` §*The measured state*: *#528's round-2 report measured its four rows printing under `exempt` against a tip without the file* / over the squash range the four rows match nothing in any state, and nothing clears `--floor 1.0` | the measurement | The report's reading was over the branch's own range at the time; the squash range is the range the table measures. Nothing in the fix turns on it. `phases/phase-1.md` §*Q2* |

## Not verified

| Item | Who must answer |
|---|---|
| The broad gate — `bin/test -q`, and the repository-wide `uvx ruff check .` and `uvx ruff format --check .` (`seal/config.md`'s `Broad gate` row); only the touched module and the two edited files were run here | the sealer, once the review rounds settle |
| ✅ The `Ran by` cell of `phases/phase-1.md` through `phase-4.md`, written `unknown` because the spawn prompt handed over no agent or model name | filled by the orchestrating session at `bc38c8f3`; round 1's ⬜ a, closed in the round-1 fix pass |
| Whether a branch already open against the release branch that carries a `survivors.md` sees new `exempt` lines or new reports at its next CI run, now that the file stops silencing what it quotes — `plan.md` §*Operational impact* names the effect and no such branch was run here | the orchestrating session, at each such branch's next pull-request run |

## Not done

- **Five places on #525's range vanish through a live file the range wrote.** With its `overview.md`, `changelog.md` and ledger fragment also out of the sweep, `docs/review-chain-spec.md:392` and `:845`, `skills/code-review/SKILL.md:210`, `skills/code-review/orchestration.md:263` and `tests/test_the_last_rounds_fixes_are_checked.py:8` are reported and are not otherwise; #528 and #527 have none. `spec.md` §*Out* keeps those files in on purpose — they are live statements, and #423's pass found one false fact standing in three of them — so the count is recorded here for the repository owner, who decides whether that class is ever worth a different answer.
- **`RANGE_CELL` reads a path cell spelled `a/../b.md` as a range**, found by S8's enumeration; it prints under `unresolved`, silences nothing, and no row in the tree is spelled that way. Left where it stands, named in `phases/phase-3.md` and ledger row E4.
- **#366** goes to work item A (`questions.md` Q1, answered); nothing for it here.
- **`OWNER_DIR` and the pre-0.4.0 top-level `specs/` root**: left out, as `spec.md` §*Out* decides; the comment above the pattern now says so.

## Fed back into the spec

- *Inferred during implementation*: S6's pool half fails by dilution on a small pool rather than by naming the record, and a case for it has to refuse both directions (`phases/phase-2.md`).
- *Inferred during implementation*: the predicate's name is `records_a_past_state`, one function calling `records_a_past_round`, and the test's `PREDICATE` follows it (Q4, `phases/phase-1.md`).
