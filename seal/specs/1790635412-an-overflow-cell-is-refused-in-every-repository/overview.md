# 1790635412-an-overflow-cell-is-refused-in-every-repository — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's `spec.md`, `plan.md` and `questions.md`; `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* (the cell-count paragraph) and §*What the checker refuses, and what it says while refusing*; `skills/evidence-check/SKILL.md` §*Which reader graded your tree*, §*Verdicts and what to do*, §*Known limits*; `CONTRIBUTING.md` §*What a change to a gate must carry* and §*House rules*; `CLAUDE.md`'s fragment and ledger-edit rules
· evidence: `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` rows O1–O6, V1, C2, L1 added; 29 released rows re-read in place (two corrected) and C2 and L1 removed from `seal/releases/0.15.1.md` and `0.15.3.md`
· verified: executed — every new case seen red before it was planted, a mutation of each new unit, the narrow modules of each phase, the 28 modules that drive the checker or the advisor, `bin/evidence-check .` and `--strict .` unscoped (exit 0 both), `survivor-check` over the branch (exit 0); read — the README rows and the table cells' rendering

## Why this work exists

A ledger row split by a stray `|` hid whatever fell past its last column,
and only this repository's own test said so; the shipped checker now names
it `OVERFLOW` in every repository that installs the plugin.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Test modules touched | `spec.md` *Data & interfaces*: "Test modules touched: `tests/test_release_hygiene.py`, `tests/test_evidence_check.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_dispatch.py`, and one new module". The build did not touch `tests/test_evidence_check.py`, and did touch `tests/test_the_ledger_fragments_fold_at_release.py` | the code | the vendored case the spec expected in `test_evidence_check.py` sits in the new module beside the arm's other cases; the fold fixture wrote a Notes cell with an unescaped pipe, which the arm names, and escaping it keeps what the fixture was for (`phases/phase-3.md`) |
| Where A1–A13 were seen red | `plan.md` phase 1: "seen red at `11e3104c`'s checker, run from a saved copy" | against the unedited file in place | the checker at the branch's base was byte-identical to `11e3104c`'s (`git diff --stat 11e3104c HEAD` printed nothing), so no saved copy was needed |
| The reader table's shape | `plan.md` *Technical context*: "Either the case generalises over both columns, or the page states both verdicts in one column" | a column of its own, `OVERFLOW is` | one shared column would have made the advisor's cell false between phase 1 and phase 2 |
| A removed name on a frame line | `plan.md` *Technical context*: "The names phase 3 removes sit on lines carrying the `NAME NOT IN TREE` marker" | the builder added the marker to `plan.md`'s *Alternatives* row naming `overwide_rows` | the records arm refused that line once the fragment existed; the plan's own sentence says the line should carry it |
| `Checked` on a re-read row | spec silent | today's date, appended after a `·` where the cell already held several | `templates/ledger.md`: "The **Checked** column carries the date somebody read the code" |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck at the branch's tip | the sealer, spawned by the orchestrator after the review rounds settle |
| A10's `os.sep` normalisation and the advisor's path on Windows | CI's `windows-latest` leg at the pull request |
| the README command rows, which no case holds | the review chain (warden) |
| how GitHub renders the escaped pipes in `SKILL.md`'s new verdict row and Known-limits bullet | the review chain, on the pull request's rendered file view |

## Not done

A row with fewer cells than its header is not refused anywhere now,
including this repository's own case, which used to compare with `!=`. No
ledger here has one (Q2), and `spec.md` *Out* gives the grounds. The
`reverify` rider's question about the `Checked` column was read and left:
it is work item C's (#387), sequenced after this squash, and the rider is
re-stamped rather than answered.

## Fed back into the spec

none — the three interface names and the verdict word are the ones
`spec.md` states.
