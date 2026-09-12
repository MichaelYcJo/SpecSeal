# a round record disarms survivor-check — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1789211172-…/spec.md`, `plan.md`, `questions.md` (Q1, answered *out*), `routing.md`; `CONTRIBUTING.md` §*What a change to a gate must carry*; `CLAUDE.md` §*a change writes fragments, never the shared file*, §*A ledger coordinate names content, never a position*; `skills/agent-contract/SKILL.md` §§2, 6, 8, 9, 12, 14, 15; `seal/config.md` (no `Record language` row → English); `seal/follow-up.md`'s `survivors.md` row; `seal/ledger.md` rows S3 and S6 for `survivor_check.py`
· evidence: three rows added in `seal/ledger/1789211172-a-round-record-disarms-survivor-check.md` (S1 the range-side exclusion, S2 the enumeration, S3 the docstring sentence); `seal/ledger.md` S3 re-read, re-dated and re-verified
· verified: **executed** — the two new cases seen red against the unedited module and green after; the docstring case and the enumeration case each seen red under two mutations with the module restored byte-identical; `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` 47 passed; `bin/survivor-check --range 7e17f5e..941dab5` before and after; `bin/evidence-check .` and `--reverify .`; `bin/unverified-check` on this file; the narrow module set phase 5 names; `uvx ruff check` and `uvx ruff format --check` on the changed files. **read** — `whole_range`'s ownership argument, which is the grounds for the one named exception rather than a run. **unverified** — the table below

## Why this work exists

`survivor-check` reported success on every branch that went through review,
because the review chain's own round records quote the wording a fix removed
and the check read them as wording the fix wrote; it now excludes them from
the range as it already did from the pool, so the gate measures the branches
it was built for.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many cases the acceptance rows need | `spec.md` §Scope in-item 3 says *A case* (singular) for A1/A2, and A2 folds the removed side into *no reported source sits under a `rounds/` directory* | **Two cases.** A1's range cannot put a record in the source position — the record it adds removes nothing — so A2's clause is trivially true there. A second case supplies a range that edits a round record and touches nothing else | The spec's own in-item 1 argues for both sides of the list: *a sentence removed from a round record is not corrected wording either*. With only A1's case planted, a later narrowing of the fix to the added side alone passes the suite, which is the failure the case exists to prevent |
| The spec's quotation of two ledger anchors | `spec.md` §*Data & interfaces* wrote rows S3 and S6's anchors inline in a table, each spelled with the bare file name — `survivor_check.py` rather than its path under `skills/code-review/scripts/` — and carrying the row's stamp | The two stamped anchors moved into a **fence** above the table, with the sentence saying why; the cells now name the unit alone | `evidence_check.py`'s `claim_lines`: a stamp in a fence is a quoted anchor, not a claim about the tree. The spelling was invisible until this work item's ledger fragment existed — `unread_items` only reads a work item's records once it has one — and it then made `bin/evidence-check .` exit 2 with `2 refused`. Corrected the way `8ce7f70` corrected the identical spelling in #361's spec, and the content of both rows is untouched |

## Not verified

| Item | Who must answer |
|---|---|
| The broad gate — the full suite, the repository-wide lint and the format check. `agent-contract` §2 makes it one act and `agents/smith.md` does not assign it here | the sealer, spawned by the orchestrator after the review rounds settle |
| The model each phase ran on. The four `phases/phase-N.md` records carry `Ran by: specseal:smith on unknown`, because the spawn prompt named no model and `templates/sdd-phase.md` forbids a segment to source that value from its own idea of what it is | the orchestrating session, which chose the spawn-time argument |
| Windows. The change adds a list comprehension over `-z`-separated paths and reads blobs; `records_a_past_round` already normalises `\` to `/`, and no Windows run is claimed. Nothing platform-specific was added and nothing platform-specific was executed | CI, or whoever next runs the check on Windows |
| **The exemption path — writing a `seal/specs/<id>/survivors.md` row still silences its own survivor through the diff.** Q1 answered *out*, so this work item did not touch it and did not measure its reach at the gate. #361's round 3 measured the prediction *#365 re-arms the exemptions* **false**, and nothing here re-arms them: a `survivors.md` written before this release is not armed by this change | the repository owner, on issue **#371**, which carries round 3's two-run measurement and the argument against |
| Whether any branch now in flight reports a survivor it did not report before. The operational direction is known — stricter — and which branches it lands on was not enumerated | the first pull request into a release branch after this merges |
| The real-range measurement `7e17f5e..941dab5` is reproducible only while the local branch `docs/361-a-release-is-sized-by-a-count-and-cut-by-urgency` exists. It was executed and recorded in `phases/phase-2.md`; nothing in the tree depends on it, and no third `fixture/*` tag was pushed because `agent-contract` §6 withholds pushing | the repository owner, if the measurement is ever wanted again — it is a tag push, not a rerun |

## Not done

**Phase 4 was not built.** Q1 was answered *out* by the owner before the first
edit, so `seal/specs/*/survivors.md` stays inside `corrected`'s path list and
inside the corpus. `plan.md`'s phase 4 row reads `deferred #371`. The
narrowing was deliberate: the repository had reserved that judgment for a
person twice, and a gate change is judged by what it does when it is wrong.

**`whole_range()`'s path list at `:833` is left unfiltered**, named as the one
exception with its grounds in the enumeration case rather than silently
skipped. It asks whether a range belongs to the work item that wrote a
declaration, and a round record committed under `seal/specs/<id>/rounds/` is
evidence of that ownership. Filtering there makes the ownership test stricter
and can turn a legitimate declaration into `foreign` — a row that quietly
stops applying, which is the one failure a rotting anchor must not have.

**#361's round 1 record still reads *exit 0, every survivor excused*.** It is
not rewritten. A round record states a past state at its Target SHA, and round
2's report corrects it where the next reader meets it. The repair that was
owed happened in the work item that found the defect, at `01a0437`.

**No third `fixture/*` tag.** The symmetric real-commit range `b46ff77..a0f0e9a`
adds only round 1's record and report and would be the natural anchor for a
case, but making it durable is a tag push. A case anchored there would ship
skipping, and `test_the_measured_commits_are_still_here` would gain a third
way to go red for a reason nobody caused. The real range was re-derived once
and recorded as a measurement instead.

## Fed back into the spec

**One clause, inferred during implementation: a work item's records are read
by `evidence-check`'s records arm only once the work item has a ledger
fragment.** `unread_items` answers *whose records are not read*, and a
directory with no fragment is in that set. So a spelling defect in a
`spec.md` — a coordinate the arm refuses — is latent from the moment the spec
is written and surfaces at the moment the fragment lands, which is phase 5 of
the build and after the frame has been approved. Recorded here because a
framer cannot check its own spec against that arm, and the builder is the
first party who can.

**Nothing was fed back into `docs/`.** The judgment this work rests on —
which side of a path list an exclusion holds on — is the module's own and
lives in its docstring, pinned by a case. A policy clause would be a second
home for a fact one document already owns.
