# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `templates/config.md` §*Broad gate* (§*What is refused, and what stays allowed*, §*Choosing a value — the criterion*); `skills/verify/SKILL.md` §*The broad gate*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file*; `skills/agent-contract/SKILL.md` §6, §12, §14, §15
· evidence: `seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md` — B1–B4, `Corrected · S5`, and 44 `Re-read ·` rows
· verified: executed — the slice cases of each phase, the three touched modules whole (696 passed, 79 skipped), 61 mutations (`phases/phase-1.md` to `phase-4.md`), `evidence-check --strict` and `survivor-check`; read — pytest 9.1.1's `_pytest/terminal.py`, and every released row whose coordinate this work drifted

## Why this work exists

A lint-first `Broad gate` row made every failing test read `new` whatever the
base did, and the word read as measured; now a word is given only from a run
at the base that printed pytest's summary, and the row may put its runner
anywhere a cut can reach.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What counts as a run that stopped early | `spec.md` Scope 3: "neither pytest's collection-interrupt banner nor its maxfail banner" / the code reads any `!` rule pytest writes | the `!` rule | `_pytest/terminal.py` in pytest 9.1.1 writes a `!` separator for `shouldfail`, for `shouldstop` and for an interrupt, and otherwise only under `--collect-only`. The two measured banners are both such rules, and so is xdist's `xdist.dsession.Interrupted: stopping after 1 failures`, which the spec's two texts would have missed (`phases/phase-3.md`) |
| The files that pin rule 3 | `spec.md` Scope 5 lists eight prose files / `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` also pinned the old title and the old reason | updated those pins, and they now hold the new title, the new reason and that rule 3 picks no order | spec silent; the pins would have gone red against the approved rewrite |
| Cases beyond A1–A9 | the spec lists A1–A9 and B1 / three more cases were added | kept | each holds a branch a mutation showed nothing else held: the runner-first single run, the `;` cut chosen by the shell, and pytest's measured `ERROR` shapes under xdist (`phases/phase-3.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The `cmd.exe` grammar end to end: every new end-to-end case runs on `windows-latest`, and `test_a_row_is_cut_at_the_semicolon_its_shell_reads` skips there. Only the scanner's `cmd.exe` branch was driven, as a pure function, from macOS | CI's `windows-latest` leg on the pull request |
| This repository's own lint-first row (`uvx ruff check . && uvx ruff format --check . && bin/test -q`) through a real failing seal. The fixtures stand in for ruff with two `python -c` lines | the sealer, at the first seal of a branch whose suite fails; the orchestrator reads its `suite-at-base-<k>.txt` files |
| The full suite, the repository-wide lint and the typecheck after this work | the sealer, spawned by the orchestrator after the rounds settle |

## Not done

The frame's *Out* table, carried as it stands. A file the branch reports only
as `ERROR` (a collection or setup error, no `FAILED` line) still gets no
comparison at the base, because `failing_files` decides which files are asked
about and this work is about whether the answer is measured. Whether to file
it is the repository owner's call.

`{ …; }` brace groups, a `${…}` holding an operator, and a `#` comment are not
modelled by `row_prefixes`. A cut they misplace costs a measurement and fakes
none, and `row_prefixes`'s docstring names all three.

## Fed back into the spec

- *Inferred during implementation:* a run at the base stopped early when its
  output carries any `!` rule, not only the two banner texts Scope 3 names.
- *Inferred during implementation:* each run tried at the base is kept as
  `suite-at-base-<k>.txt`, and `NO_RUNNER`'s reason names that pattern so a
  `new?` reader knows where to look.
