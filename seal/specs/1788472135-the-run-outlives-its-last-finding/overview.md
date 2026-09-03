# the run outlives its last finding — overview

<!-- The closing memo. Opened at the first unverified item, closed when
implementation ends. Only what the diff cannot show goes here. -->

📋 implement applied
· spec:     seal/specs/1788472135-the-run-outlives-its-last-finding/{spec.md, plan.md, questions.md, routing.md};
            issues #110, #117, #97 (the parent this was split from), #82 rounds 1–4 and #81 rounds 1–7 (the measurements);
            docs/review-chain-spec.md §The review run has a bound, and an end;
            skills/code-review/SKILL.md §Orchestrator: the run ends with a verifying round;
            agents/warden.md, agents/smith.md, templates/{sdd-round.md, sdd-phase.md, config.md};
            CLAUDE.md §fragments, §merge method, §the goal a design is chosen against
· evidence: <phase 4 writes seal/ledger/1788472135-the-run-outlives-its-last-finding.md>
· verified: <filled when implementation ends>

## Why this work exists

A review run had a ceiling and no floor, so it spent the ceiling: three of
#81's seven rounds found nothing that loses a record and nothing that crashes.
The rounds that removing them would remove are also the rounds that were
reading the units each fix pass created, which is why the bound on those units
lands in the same branch rather than after it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which direction the template-fields test can go red | The plan said to watch `ROUND_RECORD_FIELDS` fail before adding the row to the list | The row went into the LIST first, and the red was watched with the TEMPLATE still empty | `test_the_round_template_carries_the_fields_it_is_expected_to` is parametrized over the list, so a row absent from the list cannot be run at all. The check has one direction — list → template — and the plan named the other |
| Where the reviewer's report line lives in `agents/warden.md` | The plan named `:93-99`, the passage that carries the grounds | Both that passage and the `## Report` format block | The format block is what a reviewer copies while writing the report; a line only in the prose is a line nobody types |
| Whether `Needs a fix` is the run's terminal condition | Three files said it was the only one | All three amended | A second terminal condition two paragraphs away turns a single file into two answers at once, which is the contradiction-inside-one-file these records already refuse |

## Not verified

| Item | Who must answer |
|---|---|
| The full test suite, repository-wide lint, and typecheck | The sealer's single broad run, after the review rounds settle |
| That `chain_check.py` refuses what phases 1–2 wrote down | Phase 3, which is where the refusals are built |
| That the two new record rows survive a real round record written against them | The first `round-N.md` this work item's own review chain writes |

## Not done

`CAP_BACKWARDS` in `tests/test_the_last_rounds_fixes_are_checked.py:1005`
forbids a set of strings across three files by substring, and phase 1's new
prose collided with it on a sentence whose subject was different. The prose was
reworded rather than the guard widened: loosening an existing pin so a new
sentence fits is how a pin stops being one. Whether that guard should read
subjects rather than substrings is left open, and nothing here depends on it.

#97's three remaining levers are untouched by design — each changes pins that
already exist and each needs its own question batch, which is why #117 was
split out of it.

## Fed back into the spec

none
