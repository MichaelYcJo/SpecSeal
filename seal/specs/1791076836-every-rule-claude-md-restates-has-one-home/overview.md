# 1791076836-every-rule-claude-md-restates-has-one-home — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md` (Grounding, Scope 1-8, O1-O7, D1-D8, S1-S10), `plan.md`, `questions.md` Q1-Q4; `docs/the-record-layout.md` lead and §*What is decided and not built yet*; `docs/branch-and-release.md` §*Work accumulates on a release branch*; `CONTRIBUTING.md` §*House rules* and §*What a change to a gate must carry*; `skills/implement/SKILL.md` §1, §2; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `tests/test_the_ledger_rules_have_one_home.py`, `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_a_shrunken_corpus_declines_to_judge.py`
· evidence: `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md` O1-O6 added, five `Re-read ·` rows for `seal/releases/0.18.0.md` and `0.4.0.md`; #757's E5 row re-stamped in place in its fragment
· verified: executed — both new modules seen red against plants and every unit broken once with `mutation-check`, the baseline measured twice, the narrow module set, `claude_block.py --check`, `fold-check`, `evidence-check --strict`, `survivor-check`; read — the ledger rows the merge drifted, before they were re-stamped

## Why this work exists

Four rows of `CLAUDE.md` restated rules other files hold, and one copy had
already gone false; each now links its home, and a ratchet stops the next
paste anywhere in the rule documents.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S5's grep | Spec S5: "`git grep -n 'CLAUDE.md. §\*no real identifiers'` returns nothing". Tree: it returns one line, in work item `1790993139`'s `spec.md` Grounding table | the grep outside `seal/`, which is empty, and the module's `LINKED` rows for the four comments | Scope 2 took its four comments from a grep "outside the records". A record cites what was read at its time and is not rewritten (`phases/phase-1.md`) |
| The D4 module's reach | Spec D4: "`LINKED`: `CLAUDE.md` must name each home's path and section"; S4 "the D4 module if the builder pins it". Code: a fourth rule, the question batch, and `LINKED` rows for the four code comments too | pinned | S4 left it to the builder, and S5 is then held by a case rather than only by a grep (`phases/phase-1.md`) |
| The baseline's numbers | Spec §*The method and its result* and Q1: 99 debt pairs and 219 runs at `07aec0f2`. Code: 104 pairs after round 1's fix pass, whose counts of shared windows sum to 2,104 over 1,210 distinct windows (round 1's ⬜ 4 corrected *2,091 distinct windows*, which was the merge's per-pair sum) | the build's measurement | Q1's default: "The numbers measured at build time win". The framer's probe was deleted, and the corpus moved with #756 (`phases/phase-2.md`) |
| The unit counted | Spec D5: "count the distinct `WINDOW`-word windows the two files share"; the result section reports runs | distinct windows | D5's own unit; a window count rises under every paste where a run count can stay flat (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |
| Ten ledger rows drifted on `origin/release/v0.18.1` before this branch merged it, on `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#fake_venv`, `tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT` and `templates/config.md`, files this branch never touched; `evidence-check --strict .` exits 2 on them | the orchestrator, who decides which of #756, #757 and #758 re-reads them |

## Not done

**The lead sentence of §*What is decided and not built yet*** (*F1 is built;
the other three are not yet*) was left, as spec O5 and `questions.md` Q3
say: it is the last of #728, #729 and #730 to land that corrects it.

**The paraphrase pass (spec D6) was not re-run.** Its result is the framer's,
recorded in `spec.md`, and #755 carries it. It is a one-off by design.

**Two pairs the merge added to the baseline** (`docs/the-pact.md` with
`templates/pact-review.md`, and with `skills/evidence-check/SKILL.md`) came
from #756 and were recorded as measured rather than judged here.

## Fed back into the spec

none
