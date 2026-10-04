# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md` §*The shape* clauses A–F, §*Why this shape*, §*#739's three refusals*, S1–S10; `plan.md` phases 1–3 and alternatives B–H; `questions.md` Q1–Q5; `docs/commit-review-gate-spec.md` §*A file edit goes through the `Edit` tool*, §*Two readings that prompted that run stay as they are*, §*Only what the shell would EXECUTE is read as commands*; `skills/agent-contract/SKILL.md` §9
· evidence: `seal/ledger/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data.md` — six `Re-read ·` rows (E1, E2, E6, E17, E18, G8) and three `Corrected ·` rows (E3, E7, I10)
· verified: executed — the reader, gate, agreement and hygiene modules narrow, each new case red against a mutation; read — I10's generated corpus, not re-run

## Why this work exists

A pull request body or a note that only mentions a commit, written through
one exact heredoc shape, no longer costs an unattended run a refused Bash call,
and no other command reads any differently.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| An `Enforced by:` line in contract §9 | S10: "Each carries an `Enforced by:` line naming S1, S4 and S6's cases". The contract carries no `Enforced by:` line anywhere, and no checker reads one there | §9 names the policy statement that carries the grammar, and `tests/test_edits_go_through_the_edit_tool.py::test_the_rule_names_the_one_heredoc_shape_it_does_not_read` pins both carriers; the policy statement's `Enforced by:` line names S1, S4 and S6's cases | `skills/agent-contract/SKILL.md` has no section in that shape, and `fold-check` reads `docs/` only. A line nothing reads would be a pin that cannot fail |
| The reader's body form | Spec silent on whether the body carries its last newline | Each line with its newline | An empty body and a body of one empty line are otherwise the same string, and the shell writes them differently (`phases/phase-1.md`) |
| A program terminator followed only by newlines | Clause F: "where a suffix exists, a newline and the suffix" | Newlines alone are no suffix | A run of newlines runs nothing, and keeping them would make the reduced text differ from a sink's for no reading |

## Not verified

| Item | Who must answer |
|---|---|
| Q3 for bash 5.x: whether bash 5 cuts every admitted string where the reader does, directly and through `eval` | the ubuntu leg of the test workflow at the pull request (`tests/test_one_heredoc_shape_agrees_with_the_shell.py`) |
| Q4: whether the moved row reaches the shape on the Windows leg, where `shlex.quote` gives a single-quoted path with backslashes | the Windows leg of the test workflow at the pull request (`tests/test_no_shape_the_base_stops_reads_silent.py::test_the_moved_row_reads_silent`) |
| The agreement test on the Windows leg, where `bash` is Git Bash or is skipped by `shell_probe` | the Windows leg of the test workflow at the pull request |
| How many commands of I10's generated corpus (11,393) and recorded sessions are the one shape | nobody can without re-running `1790660768`'s generator; the correction says so and is labelled read |
| The full suite, repository-wide lint and typecheck | the sealer, after the review rounds |

## Not done

- The ten ledger rows still drifted (`templates/config.md`,
  `tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT`,
  `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#fake_venv`) drift
  on `release/v0.18.1` at `edee5ca2` and are not this branch's to re-read.
- Lifting the CR and backslash-newline bans. Both shells here keep those
  bytes literal in a single-quoted body (`phases/phase-1.md`), which is a
  measurement for `plan.md`'s alternative H, not a decision this work makes.

## Fed back into the spec

none
