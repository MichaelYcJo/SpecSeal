# 1791384156-config-rows-coordinates-and-headings-have-one-reader — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     (filled when the build closes)
· evidence: (filled when the build closes)
· verified: (filled when the build closes)

## Why this work exists

Three formats the repository owns — a `seal/config.md` row, the ledger
coordinate and a markdown heading — were each read by several copies that
answered one file differently; each now has one reader, so a doubled row, an
unreadable config, a fenced `##` and a `#NNN`-led line get one answer
everywhere.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which phase built `seal mode`'s refusal | `plan.md` phase 2: "`seal.py#table_span`/`with_row` refusing two `Mode` rows naming both lines" / built in phase 1 | phase 1 | `seal.py` re-exports `declared_mode`, and its report fell through to the *they disagree* arm on the new `refused` kind the moment phase 1 landed; splitting it would have left a commit whose `seal mode` misreports |
| An unreadable `config.md` under `seal mode` | S2c of #104 (`tests/test_the_mode_is_a_row_and_a_command.py::test_a_row_that_cannot_be_written_still_reports`): exit 0, *could not be written* / exit 2, the path named, the folder still reported | exit 2 | `spec.md` §*Scope* 1: "a command a person runs (… `seal mode` …) prints it and exits 2 with nothing judged". The case's own reason — the report does not need the write — still holds: the folder line is printed |
| Two `Mode` rows under `seal mode` | round 1 🟡 5 of #104 (`test_two_mode_rows_converge`, NAME NOT IN TREE since phase 1): two runs reach agreement by setting the first row / refused, both lines named | refused | `spec.md` S2; and `docs/the-pact.md` §*How a signer names the pact*: "a row written twice, has no value at all: its first row is not the answer" |
| Which readers of the freeze refuse | `plan.md` phase 2 names `frozen_from`, `cutoff_at` and the commands / `settle.py#anchored_rows` and `hooks/evidence-advisor.py#main` read `frozen_from` too | both read a refusal as frozen | `spec.md` §*What this delivers*: "The freeze arm never turns off because the file could not be read." Neither refuses (a guard that only advises, and a hook) |
| What `evidence-check` refuses on | `spec.md` S1, S3: "`evidence-check` … exits 2" / only `--reverify` refuses | `--reverify` | the plain check reads no config row at all; refusing it on a config it does not read would stop every CI run on an unrelated file |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds settle |
| The unreadable fixtures (a directory named `config.md`, bytes that do not decode as UTF-8) on Linux and the Windows shards | CI at the pull request |

## Not done

`reference_roots` reads a refusal as the default rather than refusing: its
callers, `unverified-check` and the survivor sweep, are not among the commands
`spec.md` names as refusing, and the default is what an unreadable file always
read there.

## Fed back into the spec

- Inferred during implementation: `settle` and the commit advisor read a
  refused freeze row as frozen (fragment row K12).
- Inferred during implementation: `correction-check` reads `seal/config.md` at
  a commit with `git cat-file`, so a tree or an undecodable blob there is
  refused naming the cause (fragment row K9).
