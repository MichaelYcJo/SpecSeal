# 1790550713-what-the-last-rounds-deferred — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. Written at phase 3 from what phases 1 and 2 recorded as they went. -->

📋 implement applied
· spec:     spec.md, plan.md, questions.md of this work item; `CLAUDE.md` (fragments, ledger rows, a merge's ledger conflicts); `skills/agent-contract/SKILL.md` §1, §2, §3, §5, §7, §9, §12, §14, §15; `docs/review-chain-spec.md` §*What the sweep reads* (a released entry is not rewritten); issues #625, #626; `seal/specs/1790381328-…/spec.md` *Part 2*
· evidence: two rows in `seal/ledger/1790550713-what-the-last-rounds-deferred.md`; corrected in place: S8–S12 (`0.15.5.md`); re-read and re-stamped: `0.15.4.md` `MALFORMED`, `0.10.0.md` S13, `0.11.4.md` ×3, `0.12.1.md` R2, `0.13.1.md` (the section row), `0.14.0.md` G5, `0.15.5.md` C3 and C5, `0.4.0.md` (the fix-pass-checker row), `0.5.0.md` S7, `0.8.1.md` R2, `0.9.3.md` R1
· verified: executed — each phase's narrow modules, every new parameter and the completeness case seen red, round 3's three mutants and the named examples' branches, S7's tightened assertion and a `close`-only ready mutant, the re-wrap probe and `--help` byte comparison, `evidence-check`, the phase-3 sweeps; read — the enumerations' non-instances; unverified — the full suite (the sealer's)

## Why this work exists

Two items 0.15.5's rounds deferred. `evidence-check`'s statement of rule (a)
left out that the `@` must follow the `#`, and three of its examples had lost
their case (#626). Two test comments stated an exit `close` cannot produce
where they run, and the #623 range left ragged docstring lines (#625). Each is
closed as a class, and a case now holds every example the rules give.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The completeness case's reach | spec.md §*Scope*: five shapes lack a case; `chart.js@4`, `org/repo#299's`, `@lru_cache  # memoized` are "in the docstring's first paragraph … outside the rules section". The case, red against the old dicts, named nine: those three and `Makefile#"all: build"` also stand in the rules section | all nine are parameters now, 21 in all | the case reads the section as spec.md S5 defines it. Excluding four of its examples would make the case weaker than its own definition, and older cases already hold their verdicts (`phases/phase-1.md`) |
| S4's mutants | spec.md S4: each named example is seen red "with the named branch it relies on disabled" | each was seen red with two branches off | measured: `docs/a.md#1장@abcdef12` is named by the glued marks and by the path its `@` follows; `src/a.py#handler @abcdef12` by the path test and the dotless-name test. One branch alone leaves each green (`phases/phase-1.md`) |
| S7's mutant and wording | spec.md S7: "With `run_check`'s draft payload removed (a mutant), the `fixed` parameter exits 1"; the comment says "exit 1 only at a ready pull request" | the mutant judges `close` alone as ready; the comment says all three exit 1 as ready | removing the payload made `new` inside the fixture fail first. Judged as ready, `answered` and `deferred` also exit 1, on the fixture's `Broad gate: not yet`, so "only `fixed`" would be false (`phases/phase-2.md`) |
| #625's ragged lines | spec.md: five sites | six | `tests/test_the_rules_have_one_owner.py`'s "pull request — a reader" is a mid-paragraph line the same range left (`phases/phase-2.md`) |
| `TAKEN_UP`'s case name | spec.md / plan.md: `TAKEN_UP`, "or a sibling the builder names" | `TAKEN_UP`, its case renamed `test_what_the_rules_still_name_is_named_and_says_so` | Q1 measured `MALFORMED <shape>  ` for both named examples, so no sibling dict was needed. The old name said "dotless openers" and the case now holds more (`phases/phase-1.md`) |
| Phase 3's `gather_changelog.py --check` | plan.md phase 3: "exits 0" | exits 1, naming this work item's fragment | a fragment is ungathered until release preparation, and only the release pull request runs the check (`seal/releases/0.4.0.md`: "no other pull request runs the check"). The criterion cannot hold on a feature branch (`phases/phase-3.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the format check (the broad gate) | the sealer, once, after the review rounds settle |

## Not done

- **`CHANGELOG.md` §0.15.5 and 1790381328's gathered fragment are not
  rewritten.** `docs/review-chain-spec.md` says a released entry is not
  rewritten. This work item's fragment carries the correction, as the framer
  decided.
- **The 22 other `assert code in (0, 1)` after `close`** in
  `tests/test_the_fixes_close_the_record.py` are left. No sentence beside any
  of them claims an exit (spec.md *Out*); the orchestrator decides whether
  they get an issue.
- **No width check for Python prose.** It would be a new gate, and this is a
  patch release (spec.md *Out*; the repository owner answers).

## Fed back into the spec

none
