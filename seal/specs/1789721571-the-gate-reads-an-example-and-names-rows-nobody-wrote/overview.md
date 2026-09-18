# the gate reads an example and names rows nobody wrote — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     `seal/specs/1789721571-…/spec.md` (§Grounding, §Scope, §The two classes enumerated → #429 and #430, §User scenarios A1–A11, §Data & interfaces), `plan.md` (§Technical context, §Alternatives considered, §Phases, §Operational impact), `questions.md` (Q1–Q4), `routing.md`, `phases/phase-1.md`; `CLAUDE.md` §*a change writes fragments, never the shared file*, §*no real identifiers*, §*a thing more than one party can have is named with whose*, §*commit early*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `agent-contract` §1, §2, §7, §9, §12, §14, §15; `skills/implement/SKILL.md` §§1–5
· evidence: R1–R7 in `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`
· verified: executed — phase 1: `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q` (109 passed, 3 skipped), the four site cases seen red against their own unfixed arms first, two mutations of `rows_read`, `bin/test` over the five modules that read `skills/config/SKILL.md` plus `test_no_real_identifiers.py` and `test_one_word_one_meaning.py`, `uvx ruff check`/`format --check` on the two changed Python files, `survivor-check --range 9d13934..59c750a` (exit 0). Phase 2: `bin/test` over the three modules `plan.md` names (266 passed, 3 skipped before the change; 275 passed, 3 skipped after), every new case seen red first with the fence rule absent or switched off, five mutations of `unfenced` and `fenced_row` each seen red, `bin/test` over the ten neighbouring modules that read the changed units and documents (401 passed, 7 skipped), `uvx ruff check`/`format --check` on the six changed Python files, `survivor-check --range 35a9638..354c09d --exempt …/survivors.md` (exit 0), and `evidence_check.py` over a scratch ledger carrying a fenced example row (Q1). Read — `spec.md`'s wording contract, `hooks/config.py#refusal`'s and `table_span`'s docstrings, CommonMark's fenced-code-block rules. Unverified — the full suite, lint and typecheck across the repository (the sealer's, after the rounds)

## Why this work exists

A refusal a person debugs from told them rows below a line were lost without
asking whether any row was below it, and the file it was likeliest to be wrong
about is the one this plugin's own template ships.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which value site 1 — `missing_row`'s `stopper is None` arm — reads to decide what the quoted line cost | `plan.md` §*Alternatives considered* → *#430*, the chosen row: *"**Each arm asks `below` as well as `stopper`**, and every sentence that speaks about what lies below a line has a subject"*. The spawn prompt repeats it and adds *"`missing_row` already holds `below` — it is the second element it unpacked"*. The code reads `rows_read(home)` in that arm instead, and `below` in the other three | `rows_read` for site 1, `below` for sites 2, 3 and 4 | `hooks/config.py#refusal`'s own docstring: *"below — the rows written under the STOPPING line, which never arrived"*, filled under `if stopper is not None`. Site 1 is the arm where `stopper is None`, so `below` is empty there whatever the file holds — measured 2026-09-18 over the arm reached with the quoted line as the table's only row and with `\| Mode \| shared \|` written under it, `[]` both times. Keying that arm on `below` would print *nothing was written below it* over a file whose rows all arrived, which is #415 round 1 🟡 1 returning one sentence over. The substitute is safe in that arm alone and structurally so: a row parsed ABOVE the quoted line would have set `stopper` to that line, which is site 2's arm |
| What this repository's own `seal/config.md` carries | The phase 2 spawn prompt, labelled **read**: *"`seal/config.md` is ten lines with no backticks, so A11 asserts that nothing in this repository's own answers moves."* The file is ten lines and it does carry backticks — single ones, in the header comment that points at `templates/config.md` | A11 pins *no run of three backticks and no run of three tildes*, not *no backtick* | Written as the prompt said it, the assertion was red against the real file. Nothing about the rule changes, because a fence is a run of three and the comment's single backticks open nothing; what changes is what the pin is about. A pin on *no backtick* would go red the next time somebody names a file in that comment, which is not the event A11 exists to catch — the event is this repository's own config growing a fence, which is the one thing that would make every other assertion in that case stop being about a file without one |
| The wording of the three sentences that say what a refused line cost | `spec.md` §*Data & interfaces* → *What the changed sentences say*: *"The wording below is the contract"*, and for site 2 *"— and nothing was written below it, so nothing else was lost with it: this one line is the whole of what changes"*. The code says *"— and no row was written below it, so nothing else was lost with it"*, and where a further refused line stands below, *"There are more lines below it this reader will not take as rows either, so fixing this one moves the stopping place down rather than clearing the table"* instead of the closing clause | the code's wording | The reader answers with two lists and the contract's sentence can only be built from one of them: `below` holds what parsed as a row, and `refused` holds the lines somebody wrote as rows that this reader will not take. A second malformed line below the first is in neither `below` nor nothing — so *nothing was written* is false wherever one stands, measured at all four sites, and site 2's closing clause is a prediction the file does not keep: fixing the quoted line moves the stopping place to the next refused line rather than clearing the table. The escape hatch is that section's own — *A builder who diverges records the divergence in `overview.md` with both sides quoted* — and the clause the spec was missing is in §*Fed back into the spec*. Round 1's 🟡 3, and this row is round 2's ⬜ correction: the reasoning was written into that section alone, which `templates/sdd-overview.md` defines as clauses this work ADDED |
| Whether phase 1 rewrites existing cases | `plan.md` §*Phases* row 1 names new cases only; `questions.md` Q4 asks the fixture question of phase 2 | Two existing assertions rewritten, both keeping their case's subject | `test_a_second_refused_line_is_what_decides_what_a_first_one_cost` and `test_the_gate_reads_every_refused_line_and_not_only_the_first` each asserted `every row written BELOW that line is lost` over a fixture whose refused line is the LAST row of its table — #430's own instance, pinned as a case. The first does it four lines under a docstring paragraph saying that such a line *loses nothing below it, because there is nothing below it*. `skills/implement/SKILL.md` §5: a fixture whose answer moves is either a case that was pinning the defect, which the phase rewrites and says so, or a regression. Both are the first. The arm each case exists to pin is unchanged, and still pinned by the assertion beside the rewritten one |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle (`agent-contract` §2) |
| ✅ Q1 of `questions.md` — whether `evidence_check.py`, `round_record.py` and `chain_check.py` read a table inside a code fence as a live table | measured 2026-09-18 for `evidence_check.py` and the answer is **they do**; the row is in `seal/follow-up.md` with the repository owner as its answerer, since a session may not open the issue. The other two were not measured and the row says so |
| ✅ Q3 and Q4 of `questions.md`, and #429's three shapes of the fence class | phase 2 — `phases/phase-2.md` §*What this phase found* holds Q3's eight decided shapes, Q4's before-and-after measurement, and all three shapes reached by a case seen red |

## Not done

`tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_measured_commits_are_still_here`
failed while the build ran and does so no longer. **Nothing in the repository
was wrong and nothing was changed to fix it: the two tags were on `origin` the
whole time and this clone had never fetched them.** Reported from the build as
a repository defect out of scope, it is corrected here rather than rewritten,
because a record that says what the tree does not is what the work item before
this one was about.

What was measured, by the orchestrator on 2026-09-18: `git rev-parse --verify`
returned 128 for `7bcf36a` and `ad6f81a` and `git tag -l 'fixture/*'` was
empty — both true, and neither says where the tags are. `git ls-remote --tags
origin 'fixture/*'` names them both. After
`git fetch origin 'refs/tags/fixture/*:refs/tags/fixture/*'` the module is
`55 passed`, where it had been `1 failed, 47 passed, 7 skipped` — the seven
skips were the cases the missing commits had disarmed, which is the state the
failing case exists to catch.

So the repair the failure names — *push those tags back, or replace the
commits* — is addressed to a repository that has lost them, and this one has
not. The sealer meets a green module.

**The mechanism this paragraph first gave was wrong, and round 1 caught it.**
It said a fresh clone starts in the state this one was in because `git clone`
fetches tags reachable from the fetched branches. `git clone` copies EVERY tag
by default; it is `git fetch` without `--tags`, and `clone --no-tags`, that
take only the reachable ones. Executed after the finding: a plain
`git clone --no-local` of this repository carries both `fixture/*` tags, 48
tags in all, with `remote.origin.tagOpt` unset.

What actually produces the state is the clone that already existed. These two
tags point at commits no branch reaches, so a plain `git fetch` never brings
them — a clone made before they were pushed, kept current the ordinary way,
stays without them for as long as nobody runs `git fetch --tags`. This clone is
that clone. A fresh one is not, so the case does not fire on a new machine, and
the sentence that said it would was naming the wrong command. It is corrected
here rather than deleted, because the record of a wrong claim is what the work
item before this one was about.

`templates/config.md` §*What is refused, and what stays allowed* said a line
that does not parse *still takes every row below it*, conditioned on a row
having parsed above. Phase 2 was where `plan.md` put that document, and the
sentence now carries the last-row case too: written LAST in its table the line
takes nothing, because nothing is under it to take.

**A table can now span a fenced block, where the fence's own delimiter line
used to end it.** The fence rule filters lines in FRONT of the walks rather
than editing them, so a fenced block between two rows is invisible rather than
table-ending. Nothing in the three walks changed to allow it; it is what *the
line is not shown to the walk* means, and it runs in the same direction as the
rest of the rule — more of a person's live table is read, not less.

The `else` arm of `missing_row` — *every row from there down is lost — this
one included* — was examined and left. `spec.md` §*Out, each with why*
records why: the clause *this one included* gives the sentence a subject in
every reachable state, so it is not a member of the class.

## Fed back into the spec

**Which of the reader's two answers a sentence about what was WRITTEN may be
built from** — *inferred during implementation*, round 1's fix pass, and a
planner may overturn it.

`refusal` answers with two lists. `below` holds what parsed as a row under
the stopping line; `refused` holds the lines somebody wrote as rows that this
reader will not take. A sentence about what was **written** below a line is
about both, and `below` alone cannot carry it: a second malformed line below
the first is in neither `below` nor nothing, and it is what the reader stops
at next. So a sentence built from `below` may say *no ROW was written*, and
anything stronger — *nothing was written*, or a prediction that one edit
finishes the file — has to consult `refused` too.

#430's class is *a sentence about what lies below a line, computed without
asking what is there*. Asking `below` narrowed *what is there* to *what
parsed as a row*, which closes the shape the tickets named and leaves this
one, so the clause is the class's own second half rather than a new rule.
The wording it moved is a divergence and is in the table above with both
sides quoted.

**And the sentence a refusal prints has to survive being followed.** Round 2
found the one arm where it did not: where the rows below the quoted line were
read, repairing that line is what lets the stop rule stop, and it then stops
at the next line the reader will not take — so rows arriving today go with
the repair. A refusal that names a cost has to name that one too, which is
the clause that arm now carries.

`spec.md`'s enumeration of #430's four sites stands as written and all four
were reachable as framed; what moved in phase 1 is the method one of them
uses, and that is a divergence from `plan.md` rather than a clause `spec.md`
was missing.
