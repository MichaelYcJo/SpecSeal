# 1790690762-arm-check-reads-every-supported-ast — overview

📋 implement applied
· spec:     `spec.md` (Grounding, M1–M7, Scope, S1–S7, C1–C3, Failure direction), `plan.md` (Technical context, Alternatives, Phases, Ledger), `questions.md`, `routing.md`; `CONTRIBUTING.md` §*Running the checks*; `CLAUDE.md` §*Repo rule — a change writes fragments*
· evidence: `seal/ledger/1790690762-arm-check-reads-every-supported-ast.md` L1–L3 added; `seal/releases/0.9.5.md`'s totality row corrected in place and re-read
· verified: executed — `tests/test_arm_check.py` on 3.12.11, 3.13.9 and 3.14.3, each S case red and each mutant red (`phases/phase-1.md`), neighbour modules, ruff, C2 on 3.9.6, 3.12 and 3.14, `evidence-check --strict`; unverified — S7 and the whole suite

## Why this work exists

`arm-check` refused any module holding a t-string on Python 3.14, and its
node-type tables were checked only on the interpreter that ran them, which in
CI was 3.12 alone. It now reads t-strings, and CI checks the tables at every
Python where they differ.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which interpreter "3.14" is | Spec M5 and §*User scenarios*: "'3.14' is the `.venv` that `bin/test` builds in this worktree". The worktree already had a 3.13.9 `.venv`, and the spawn said to keep it | `uv run --isolated --no-project --python 3.14 --with pytest` for every 3.14 run, on 3.14.3 | The spawn prompt: "The worktree's `.venv` is Python 3.13.9 — leave it; do not let `bin/test` rebuild it on 3.14." The interpreter is the same one the spec meant, reached by the form the spec already uses for 3.12 and 3.13 |

## Not verified

| Item | Who must answer |
|---|---|
| S7: the `arm-check-grammar` job's two legs pass on GitHub's runners | CI, on this item's pull request |
| `questions.md` Q1: the whole suite on 3.14. A broad gate through `bin/test` here runs on the 3.13 `.venv` and does not answer it | the sealer, who chooses how to run it on 3.14 |
| The whole suite, lint and typecheck on this branch | the sealer's broad gate, after the review rounds |

## Not done

Nothing within reach was left. The spec keeps Python 3.15, a floating leg,
the whole suite on 3.14 in CI, and `run_tests.py`'s interpreter choice out of
scope, and each has its grounds there.

## Fed back into the spec

None.
