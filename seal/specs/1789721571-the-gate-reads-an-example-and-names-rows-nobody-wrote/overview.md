# the gate reads an example and names rows nobody wrote — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     `seal/specs/1789721571-…/spec.md` (§Grounding, §Scope, §The two classes enumerated → #430, §User scenarios A8–A11, §Data & interfaces), `plan.md` (§Technical context, §Alternatives considered → #430, §Phases, §Operational impact), `questions.md` (Q2, Q4), `routing.md`; `CLAUDE.md` §*a change writes fragments, never the shared file*, §*no real identifiers*, §*a thing more than one party can have is named with whose*, §*commit early*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `agent-contract` §1, §2, §7, §9, §12, §14, §15; `skills/implement/SKILL.md` §§1–4
· evidence: R1–R4 in `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`
· verified: executed — `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q` (109 passed, 3 skipped), the four site cases seen red against their own unfixed arms first, two mutations of `rows_read`, `bin/test` over the five modules that read `skills/config/SKILL.md` plus `test_no_real_identifiers.py` and `test_one_word_one_meaning.py`, `uvx ruff check`/`format --check` on the two changed Python files, `survivor-check --range 9d13934..59c750a` (exit 0). Read — `spec.md`'s wording contract, `hooks/config.py#refusal`'s docstring. Unverified — the full suite, lint and typecheck across the repository (the sealer's, after the rounds)

## Why this work exists

A refusal a person debugs from told them rows below a line were lost without
asking whether any row was below it, and the file it was likeliest to be wrong
about is the one this plugin's own template ships.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which value site 1 — `missing_row`'s `stopper is None` arm — reads to decide what the quoted line cost | `plan.md` §*Alternatives considered* → *#430*, the chosen row: *"**Each arm asks `below` as well as `stopper`**, and every sentence that speaks about what lies below a line has a subject"*. The spawn prompt repeats it and adds *"`missing_row` already holds `below` — it is the second element it unpacked"*. The code reads `rows_read(home)` in that arm instead, and `below` in the other three | `rows_read` for site 1, `below` for sites 2, 3 and 4 | `hooks/config.py#refusal`'s own docstring: *"below — the rows written under the STOPPING line, which never arrived"*, filled under `if stopper is not None`. Site 1 is the arm where `stopper is None`, so `below` is empty there whatever the file holds — measured 2026-09-18 over the arm reached with the quoted line as the table's only row and with `\| Mode \| shared \|` written under it, `[]` both times. Keying that arm on `below` would print *nothing was written below it* over a file whose rows all arrived, which is #415 round 1 🟡 1 returning one sentence over. The substitute is safe in that arm alone and structurally so: a row parsed ABOVE the quoted line would have set `stopper` to that line, which is site 2's arm |
| Whether phase 1 rewrites existing cases | `plan.md` §*Phases* row 1 names new cases only; `questions.md` Q4 asks the fixture question of phase 2 | Two existing assertions rewritten, both keeping their case's subject | `test_a_second_refused_line_is_what_decides_what_a_first_one_cost` and `test_the_gate_reads_every_refused_line_and_not_only_the_first` each asserted `every row written BELOW that line is lost` over a fixture whose refused line is the LAST row of its table — #430's own instance, pinned as a case. The first does it four lines under a docstring paragraph saying that such a line *loses nothing below it, because there is nothing below it*. `skills/implement/SKILL.md` §5: a fixture whose answer moves is either a case that was pinning the defect, which the phase rewrites and says so, or a regression. Both are the first. The arm each case exists to pin is unchanged, and still pinned by the assertion beside the rewritten one |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle (`agent-contract` §2) |
| Q1 of `questions.md` — whether `evidence_check.py`, `round_record.py` and `chain_check.py` read a table inside a code fence as a live table | a measurement, out of this work item's scope by `spec.md` §*Out, each with why*; it opens a follow-up issue or nothing |
| Q3 and Q4 of `questions.md`, and #429's three shapes of the fence class | phase 2 |

## Not done

`templates/config.md` §*What is refused, and what stays allowed* still says a
line that does not parse *still takes every row below it*. It is already
conditioned on a row having parsed above, and `plan.md` puts that document in
phase 2, so it was left where the plan put it rather than edited from here.

The `else` arm of `missing_row` — *every row from there down is lost — this
one included* — was examined and left. `spec.md` §*Out, each with why*
records why: the clause *this one included* gives the sentence a subject in
every reachable state, so it is not a member of the class.

## Fed back into the spec

None. `spec.md`'s enumeration of #430's four sites stands as written and all
four were reachable as framed; what moved is the method one of them uses, and
that is a divergence from `plan.md` rather than a clause `spec.md` was missing.
