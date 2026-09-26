# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — overview

📋 implement applied
· spec:     `spec.md`, `plan.md` and `questions.md` of this work item; `questions.md` Q1 and `survivors.md` of work item 1790297087; issue #614 and round 3's report it carries; `skills/evidence-check/SKILL.md` §*Run*, §*Which reader graded your tree*, §*Verdicts and what to do*, §*What the region is*; `skills/evidence-ci/SKILL.md` step 4; `CLAUDE.md` §*a change writes fragments*; `docs/` read for `MALFORMED` and found silent, as `spec.md` says
· evidence: six new rows in `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`; two rows corrected in place (`seal/releases/0.11.3.md`, the notice's claim; `seal/releases/0.15.4.md`, `MALFORMED`'s claim) and eight more re-read with a dated note (`0.11.3.md` ×2, `0.15.4.md` ×2, `0.4.0.md`, `0.8.3.md`, `0.9.0.md`, `0.13.1.md`)
· verified: executed — the four reader modules (215 passed), every new or moved case red before its change, seventeen mutants one at a time, `evidence-check --strict .` exit 0, `survivor-check` exit 0 with one exemption; read — the vendored template's comment, the trades' wording in the docstrings

## Why this work exists

A 0.15.4 update turned lenient `evidence-check` runs red on prose and on a
malformed coordinate alike; now prose is silent at #614's four edges, one
missed coordinate shape is named, and `MALFORMED` fails only a `--strict` run,
which is what the owner answered for #606's Q1.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The glued-marks guard | `spec.md` §*Must still be named*: `` `src/a.py#"x = 1  # c"@0` `` is named "through the quoted string"; `plan.md`'s alternatives say `#"a b"@0` has "no path for the per-word rule to catch". Both are named word by word whatever `GLUED_MARKS_RE` does (`phases/phase-1.md`) | the guard kept, and three path-less parameters added that only the quoted string names | a unit with nothing red behind it is not pinned; each new parameter is red under one mutant of `GLUED_MARKS_RE` |
| `exit_code`'s shape | `plan.md`: a branch of its own or the drift branch, "the ordering below `BROKEN` is what is required" | the drift branch's condition | the plan left it open; one condition says the two are graded alike |
| Pins beyond item 9 | `spec.md` item 9 names two new pins | a third: `test_letting_drift_warn_takes_both_halves` runs `evidence-ci`'s recipe over a malformed row | step 4's new sentence is text a reader acts on (contract §14), and it was red on the phase-1 checker |
| `SKILL.md` §*Which reader graded your tree* | `spec.md` item 4 names the lead sentence, the table and the verdict rows | a paragraph more, after "the disagreement is the design", giving `MALFORMED`'s different reason | the paragraph explains drift's leniency by a branch mid-flight, which is not why `MALFORMED` is lenient; left alone it reads as the reason for both |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, repository-wide lint and format at this branch's tip (`unverified`) | the sealer, once the review rounds settle |
| the `windows-latest` leg over the new non-ASCII parameters (`org/repo#299에서`, `“org/repo#299”`, `docs/a.md#1장` in docstrings) | CI at the pull request |

## Not done

- `README.md`, `README.ko.md`, `CONTRIBUTING.md` and
  `docs/the-evidence-ledger.md` state drift's grading and not `MALFORMED`'s;
  each stays true and was left, as `spec.md` §*Out* decides.
- The empty-`Code grounds` question of work item 1790297087's round 3 stays
  with the repository owner, as `spec.md` §*Out* says.

## Fed back into the spec

none
