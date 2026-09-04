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
· evidence: seven rows in seal/ledger/1788472135-the-run-outlives-its-last-finding.md (F1–F7), 18 coordinates, all OK.
            F1–F6 are the claims inside chain_check.py that the two new test modules do not already say; F7 replaces
            a count this branch moved in a row seal/ledger.md carries. What deliberately earns no row is written into
            the fragment's own header comment. Fifteen rows in seal/ledger.md re-verified and re-dated, their regions
            re-read first; two rows left DRIFTED on purpose — see Not verified
· verified: executed — `.venv/bin/python -m pytest tests/test_the_record_is_held_to_the_floor_and_the_depth.py
            tests/test_the_run_stops_at_the_last_finding.py tests/test_a_fix_pass_may_add_a_unit.py
            tests/test_the_fixes_name_their_surface.py tests/test_the_last_rounds_fixes_are_checked.py -q` → 154
            passed, exit 0; `tests/test_the_pull_request_language_is_the_repositorys.py` → exit 0;
            `evidence-check .` → 465 ok · 2 drifted · 0 broken, exit 1 (drift is CI's warning, and both rows are
            named below); `evidence-check --ledger seal/ledger/1788472135-…md .` → 18 ok, exit 0;
            `fold_ledger.py --version 0.8.0 --dry-run` → all seven rows move, exit 0, nothing written;
            `bin/unverified-check` → exit 0. read — the diff under every ledger anchor this branch moved, before
            any row was re-dated. unverified — the full suite, repository-wide lint and typecheck, per §2

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
| How many shapes the depth refuses | The plan and the spec name two — an entry with no depth, and a depth of 2 or above | Three: a depth below 1 is refused as well, with a message of its own | `(depth 0)` parses, and read permissively it sits UNDER the bound and passes. The documents define depth 1 and depth 2; nothing is added at depth 0, so the tolerant read is the one this file refuses everywhere else. The message differs from the depth-2 one because the exits differ — there is nowhere to send a level that does not exist |
| What proves the two fragments are the shapes the release gathers | The plan's phase 4 row names `fold_ledger.py --check` | `fold_ledger.py --version 0.8.0 --dry-run` | `--check` reports an unfolded fragment, which is what an in-flight work item is supposed to look like, and `.github/workflows/hygiene.yml` skips the step unless the base is `main`. The dry run is what actually reads the fragment: it moves all seven rows, writes nothing, exits 0 |
| Whether keeping `seal/ledger.md` true is this work item's job | The plan gives phase 4 two fragments and nothing else | Fifteen rows in `seal/ledger.md` re-read and re-dated, two left DRIFTED on purpose | The branch moved ten anchors that four earlier work items cite, and a tree built from the base commit `10b0017` reports 451 ok and 0 drifted, so all ten are this branch's. Drift is CI's warning rather than its failing exit, which is how three phases passed their own checks without meeting it. `phases/phase-4.md` holds the per-row judgment |
| What may follow a record that met the floor | `plan.md`'s Alternatives table rejected *a record that met the floor is the last record* because it contradicts the verifying round, and chose *refuse more than one later record* instead | The count stops at the first later record whose `Needs a fix` says the run reopened, that record included | The chosen alternative was wrong one step further out, for the reason it gave against the other. A verifying round that opens something IS a finding round (`skills/code-review/SKILL.md`), so its own fixes need a reader and a third record is the run behaving correctly — the plan's bound refused it. Round 1's 🔴 1, and the first instance was this work item's own `round-1.md`, which answers the floor `no` and `Needs a fix: yes`. `Needs a fix` becomes a row a check reads, which is what makes the two cases distinguishable at all |
| Whether phase 3 writes prose | The phases table gives phase 3 the refusals and phases 1–2 the prose | `docs/review-chain-spec.md` gained a subsection for each new refusal | The gate's verdict is what a person reads and acts on, and that document already carries a `The row \| The check` table for every other refusal in this checker. Two of its facts exist nowhere else: that a malformed row is refused at any age, and that a run past its floor is grandfathered for a different reason than an absent row is |

## Not verified

| Item | Who must answer |
|---|---|
| The full test suite, repository-wide lint, and typecheck | The sealer's single broad run, after the review rounds settle |
| ✅ That `chain_check.py` refuses what phases 1–2 wrote down | 34 executed cases in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`. The 29 that existed before the code did were run at `f01f394` and 19 were red; 21 mutations of the units phase 3 added, none surviving |
| ✅ That the two new record rows survive a real round record written against them | `rounds/round-1.md`, written by the review orchestrator, carries both and `chain_check.py --baseline main` reports nothing about either. It also found the one shape that had no honest spelling — a run whose verifying round produces fixes — which is round 1's 🔴 1 and is fixed |
| That a depth declared wrong — `(depth 1)` on a unit that is really second-level — is caught | Nothing in the check can see it; the verifying round reading the `New units` surface is the reader, and `docs/review-chain-spec.md` records the limit |
| That a repository setting `Record language` leaves the floor's `no` and `yes` in English | The repository owner, on the first repository that sets the row. The exclusion list says so and CI derives it from the module's constants, but no repository has been run in another language |
| ✅ That both fragments this branch writes are the shapes the release gathers | `fold_ledger.py --version 0.8.0 --dry-run` moves all seven ledger rows and writes nothing, exit 0; `evidence-check` reports 18 ok on the fragment, exit 0. `gather_changelog.py --check` and `fold_ledger.py --check` both report the fragments as ungathered, which is the state a feature branch is meant to be in — the hygiene workflow runs neither unless the base is `main` |
| ✅ Whether row *r3 3 / r4 2* of `seal/ledger.md`, which said *the eleven fields* while this branch made the list twelve, should be rewritten | Round 1's 🔴 3 decided it: the claim no longer carries a count, the census sentence beside it is dated to the day it was taken and to the eleven entries it counted, and the row is re-verified. F7 of this work item's fragment carries what the count is now |
| Row *S8* of `seal/ledger.md` says the config template's first row is `Pull request language`, which its own work item renamed before this branch existed. This branch drifted its anchor and left the hash where it was rather than re-stamping a claim that is false — so `evidence-check --strict` still exits 2 on this tree, and that is the release-preparation step | The repository owner. Round 1 deferred it there by name, and correcting *r3 3 / r4 2* alone does not clear the check — which round 1 asked to be reported rather than worked around |

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
