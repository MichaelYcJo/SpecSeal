# the file said to delete it when the last box was ticked — overview

<!-- The closing memo (implement skill, step 4). -->

📋 implement applied
· spec:     `seal/specs/1789100139-…/spec.md` (Grounding, Scope, S1–S7),
            `plan.md` (Technical context, Phases 1–6), `questions.md`
            (Q1–Q5), `routing.md`; `CLAUDE.md` §*a change writes fragments,
            never the shared file*, §*The goal a design is chosen against*,
            §*a thing more than one party can have is named with whose*;
            `docs/issues-and-milestones.md`, `docs/release-checklist.md`,
            `docs/one-root-by-lifetime.md` §*Order* and its Korean edition;
            `skills/code-review/scripts/survivor_check.py` §*A deletion is
            one row*; `templates/sdd-phase.md`, `templates/sdd-overview.md`,
            `templates/ledger.md`
· evidence: three rows in
            `seal/ledger/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked.md`
            (S1, S3, S5b); three existing rows in `seal/ledger.md` re-read
            and re-verified — R1 and R3 of the release-hygiene item, S15 of
            the sealer's — with their Checked dates moved to 2026-09-11
· verified: **executed** — the two moved cases seen red (3 failed, exit 1)
            and green (45 passed, exit 0); then the modules that read a file
            this branch changed, **named rather than counted**, each run on
            its own and exit 0 — `test_the_rules_have_one_owner` 45,
            `test_release_hygiene` 32, `test_docs_line_wrap` 23,
            `test_a_corrected_sentence_survives_elsewhere` 43,
            `test_one_word_one_meaning` 13,
            `test_no_document_names_the_old_roots` 11,
            `test_no_real_identifiers` 2, `test_unverified_rows_close` 86,
            `test_a_section_marked_for_one_role_reaches_only_that_role` 9,
            `test_a_record_states_what_the_tree_has` 58,
            `test_a_rider_reaches_its_file` 29, `test_routing_is_recorded` 31,
            `test_the_seal_is_taken_once_by_the_sealer` 65 — and 447 passed,
            exit 0, over the thirteen together. `bin/evidence-check --strict`
            1121 ok · 0 drifted · 0 broken, exit 0; `bin/survivor-check
            --range origin/release/v0.11.1...HEAD` 32 places, all 32 excused,
            exit 0 — **at `ae2d0ac`, the tree this line describes**; the
            figure moves with the range and with what the exemption file
            quotes (#308), and it reads 36 at the branch tip; `uvx ruff check .` and `uvx ruff format --check .` exit 0;
            Q5's enumeration over every tracked loaded file. **Read** — the
            milestone/tracker divergence below, from the handoff.
            **Unverified** — the full suite, the orchestrator answers (see
            `## Not verified`)

## Why this work exists

`docs/flow.md` was the third file every branch appended to, and it cost a
merge conflict at the worst moment for no compensating benefit; deleting it
moves the order a ticket runs in to the skill that owns starting one, and
puts the release plan where the tracker already held it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many places use `FLOW` | `plan.md` §Technical context: *`tests/test_the_rules_have_one_owner.py:61,500` · 2 hits*. Three usages exist — line 141 is rule 6's link carrier, spelled as the constant | The third moved with the other two | The count came from `grep "flow\.md"`, which sees a path and not a name bound to one. The module failed to COLLECT with the constant renamed and the carrier left behind, so this was never optional |
| How many fixture usages | `spec.md` §Data & interfaces: *two cases use that path as a fixture*, naming `test_a_record_of_a_moment_keeps_every_version_it_names` **and** the assertion around line 574 | One | Those are the same site — line 574 is the first assertion inside that case. The module holds three `"docs/flow.md"` literals in total: the entry, the docstring and that fixture |
| When the exemption entry comes out | `plan.md` phase 3 | Phase 4, with the deletion | Measured: seven offending lines remain with the entry dropped, all seven in the file being deleted. A commit that removes the entry while the file is tracked leaves the module red, and `skills/implement/SKILL.md` §2 refuses a commit that does not stand on its own |
| What survives the grep | `spec.md` S6: *the only remaining hits are in `CHANGELOG.md` and `seal/specs/`* | `seal/ledger.md` survives too, with four mentions | `plan.md` §Technical context names all three and calls the ledger a record; the more specific reading was taken. All four are dated observations about a past state, and none is an anchor |
| What `fold_ledger.py --check` should say | `plan.md` phase 6: *the fragments exist and `fold_ledger.py --check` is clean* | Both fragment checks exit 1, naming only this work item's fragments | That IS the correct pre-release state: `--check` reports every fragment not yet gathered, so a branch that writes one cannot make it exit 0. The release preparation commit is where it goes clean, and the hygiene workflow runs it on pull requests into `main`, which this is not |
| Step 0's first bullet | `spec.md` scope: the four steps are **lost**. The first attempt replaced one with a milestone-based equivalent | Deleted | The bullet above it already checks that every work item merged with green CI, so the replacement stated one check twice, and a step nobody asked for reaches review as an unreviewed instruction |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck — `bin/broad-gate`. The thirteen modules named in `· verified` above and a repository-wide `ruff check` / `ruff format --check` were run and are green; the suite as a whole was not | the orchestrator, by spawning `sealer` after the rounds settle (contract §2) |
| `docs/flow.md`'s `## 0.11.1` section listed #331, #335, #339 and #149 as this release's, and the milestones put #331 and #335 in 0.11.3, #339 and #149 in 0.11.2. The file was already stale against the tracker when it was deleted, so nothing was lost by deleting it — but nothing here re-checked the milestones either | the repository owner; the handoff states the milestones are the authority and phase 5 wrote the descriptions from them |

## What phase 5's tracker writes read back as

**Q6 is closed, answered 2026-09-11 by the repository owner: (a), the
narrowing stands.** Issue #351's table sends two standing rules to
`docs/issues-and-milestones.md`; this work item moves the sizing rule and ends
*a branch writes its own rows*, because that one was about keeping
`docs/flow.md` mergeable while every branch appended to it and has no subject
once the file is gone. It reached review as round 1's finding 3, and round 2's
finding 14 was that the deferral had reached no file at all.

**S5 is closed, executed 2026-09-11 by the orchestrating session.** The four
scheduled release milestones were read back through `gh api
repos/:owner/:repo/milestones/<n>` and each opens with the purpose sentence
phase 5 wrote — 40 `release: 0.11.1`, 42 `0.11.2`, 43 `0.11.3`, 44 `0.12.0`.
The two comments were read back by id and both open *Carried over from
`docs/flow.md`, which #351 deletes*.

## Not done

**No marker was left in any file the deletion removed text from**, which is
the owner's call of 2026-09-11 and the reason Q3 resolved to (c) rather than
(b). Both editions of the 0.4.0 design record simply lose the clause. The
changelog fragment is the single record of the removal, and it is written to
carry that weight — all four parts of the file and where each one went,
including the clause dropped from that record.

**The four ledger Notes cells that still name the deleted path were left
standing.** Each is a dated observation about a past state — the subject of a
commit, a corpus count taken at `86e140f`, what the file held on 2026-09-08 —
and a dated observation does not stop being true when its subject is deleted.
The fifth was corrected, because it quoted a sentence this branch repaired in
`broad_gate.py` and was therefore a survivor rather than an observation.

**The 33 survivors were excused as one range row rather than 33 rows.** The
four that sit in loaded files were each opened and named in `survivors.md`;
all four state, about the code they are written in, the fact the deleted row
only pointed at. Correcting any of them would delete a true sentence from the
file that owns it.

## Fed back into the spec

`questions.md` Q4 and Q5 are closed with their answers — Q4 *repaired in
place*, with what each of the three repairs did, and Q5 *remove the entry*
with the seven-line enumeration behind it. Both were the work's and a
measurement's rather than a person's, so neither blocked.

Nothing was added to `spec.md`. The six divergences above are recorded here
rather than written back into it, because a scope row edited to match what
was built stops being a contract.
