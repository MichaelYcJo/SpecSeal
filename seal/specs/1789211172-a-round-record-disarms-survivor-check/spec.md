# Feature Specification: a round record disarms survivor-check

<!-- seal/specs/1789211172-a-round-record-disarms-survivor-check/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

Issue #365 · milestone `release: 0.11.2`, which holds this issue alone.

`skills/code-review/scripts/survivor_check.py` filters a work item's round
records out of the **pool** it searches and does not filter them out of the
**range** it measures. A round record quotes the defective wording verbatim,
because that is what a review report is for, so the record counts as wording
the fix wrote, `wanted` subtracts the survivor's n-grams, and the gate reports
success having measured nothing — on exactly the branches that went through
review.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | This is a change to a gate's verdict. Its four demands — a test seen red, a stated failure direction, a prompt budget, platform honesty — are the acceptance below, not a paraphrase of it. The prompt budget is the one a passing suite cannot report on, so it is answered in the pull request body or it is not answered |
| `skills/agent-contract/SKILL.md` §12 | A defect belongs to a class. The class here is *a path list this module derives from git and then reads as prose*, and it is enumerated by construction below rather than by reading around the module |
| `skills/agent-contract/SKILL.md` §15 | The new case is seen red before it is planted, and the handover says how it was shown |
| `skills/agent-contract/SKILL.md` §14 | The module docstring states which side the exclusion applies to, in the same commit, with a case pinning the sentence |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry goes to `seal/specs/<id>/changelog.md` and the evidence rows to `seal/ledger/<id>.md`. `seal/ledger/` does not exist in the tree — 0.11.1's fold removed it — so this work item creates it |
| `CLAUDE.md` §*Changing cited code is the case the rule has to answer* | Editing `corrected` drifts `seal/ledger.md` row S3, which cites `#corrected@65b199e3`. The claim survives the edit, so the row is re-read and `evidence-check --reverify` is run; it is not removed and not re-pointed |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED* | Row S6's claim — *a work item's `rounds/` records are outside the corpus* — stays true and becomes an understatement. It is not widened in place. The wider claim is a new row in this work item's own fragment |
| `seal/config.md` | No `Record language` row, so these records are English |
| `docs/branch-and-release.md` | A feature branch squashes into its release branch, so this branch's own commits do not survive the merge. Nothing this work item ships may be anchored on one of them |

## The class, enumerated by construction

The defect was missed because the pool and the range are computed by different
functions. So the class is not *round records* — it is **every place this
module turns a git-derived path list into a judgment about prose**, and there
are exactly three. They are found by reading the module's own calls to `git`
for path lists, not by searching for the predicate's name.

| # | Call site | What it computes | Filters `records_a_past_round`? | In scope |
|---|---|---|---|---|
| 1 | `tracked()` at `:279`, through `corpus()` at `:469` | the **pool** — the candidates searched, and the document frequency every rarity weight is divided by | yes | no change |
| 2 | `git diff --name-only -z` at `:493`, in `corrected()` | the **range** — which sentences the range removed, and which n-grams it wrote | **no** | **yes — this is the defect** |
| 3 | `git diff --name-only -z` at `:833`, in `whole_range()` | whether the range touched the directory a `\| Range \| Grounds \|` declaration lives in | no | no — see *Out of scope*, item 1 |

Outside the module, nothing else computes either. `bin/survivor-check` and
`bin/survivor-check.cmd` pass `argv` through, and
`.github/workflows/hygiene.yml:229-244` invokes the script. `--migrate` is
`skills/evidence-check/scripts/evidence_check.py`'s one-shot ledger writer: it
resolves ledger coordinates against a tree and builds no sentence pool and no
removed-wording range, so the asymmetry has no instance there.

## Scope

**In.**

1. `corrected()` applies `records_a_past_round` to `paths`, the whole list,
   before the before-and-after blobs are read. Both sides, not the added side
   alone: a sentence *removed* from a round record is not corrected wording
   either, and the pool already refuses a round record as a candidate, so
   filtering one side would leave the module able to name a coordinate nobody
   should be asked to correct.
2. The module docstring §*What is excluded, by construction rather than by
   list* at `:63-79` says which sides the exclusion applies to. Today it says
   *Everything under a work item's `rounds/` is out* and a reader cannot tell
   the pool from the range in it — which is the sentence that was true of the
   design and false of the code.
3. A case in `tests/test_a_corrected_sentence_survives_elsewhere.py` that is
   red against the module as it stands today.
4. A case that holds the enumeration above, so a fourth call site added later
   cannot silently miss the predicate. The reason this defect existed is that
   a docstring asserted the intent and nothing measured it.
5. The records: `changelog.md`, `seal/ledger/<id>.md`, `overview.md`, the
   re-read of `seal/ledger.md` S3, and the one sentence in
   `seal/follow-up.md`'s `survivors.md` row that describes `rounds/` as
   *left out of the corpus* — touched to leave it true, the way #361 touched
   another work item's fragment row S10.

**Out, each with why.**

1. **`whole_range()`'s range at `:833`.** It asks a different question —
   *does this range belong to the work item this declaration was written in* —
   and a round record committed under `seal/specs/<id>/rounds/` is genuine
   evidence of that ownership, not wording the fix wrote. Filtering there
   makes the ownership test stricter and can turn a legitimate declaration
   into `foreign`, which is the direction that function's own docstring at
   `:802-807` says must not happen: a row that quietly stops applying is the
   one failure a rotting anchor must not have.
2. **`evidence-check --migrate` and the other checkers.** Named above: no
   sentence pool, no removed-wording range, so there is nothing for the
   asymmetry to be an instance of. This is the issue's *check every other
   caller before closing*, answered by construction rather than by reading
   around.
3. **The second silencing path — `seal/specs/*/survivors.md`.** An exemption
   row quotes the standing text, so once the commit adding it is inside the
   range, that quote counts as wording the range wrote and subtracts the
   survivor it was written to excuse. It is the same class in kind and a
   different mechanism, and the repository has reserved the judgment for a
   person twice: `seal/follow-up.md`'s own row for the added side, and #361's
   round 3 deferral table at `rounds/round-3.md:221` for the corpus side,
   which it records as having no row at all. Deciding it here would settle a
   question the repository set aside. It is **Q1**, with a default that does
   not hold the build up.
4. **Rewriting #361's round records.** The invalidated evidence was already
   repaired in the work item that found it, at `01a0437`, in the places a
   reader meets first: `survivors.md`'s header now opens *Every row below
   excuses nothing today*, `overview.md`'s `## Not verified` row reads *No
   reading this work item has of that check is evidence*, and
   `rounds/round-3.md:85-89` records the disclosure and the four files it
   corrected. What stays as written is `rounds/round-1.md:68` and `:291`,
   *exit 0, every survivor excused* — a round record states a past state at
   its Target SHA, and round 2's report corrects it at `:52-55` where the next
   reader meets it. Rewriting it would falsify the account of a review that
   happened, which is the ground `survivors.md`'s own rows give for not
   rewriting a shipped phase record.
5. **A third `fixture/*` tag.** The symmetric real-commit case is
   `b46ff77..a0f0e9a`, whose only added files are round 1's record and report;
   it resolves today only because the local branch `docs/361-…` still exists.
   Making it durable is a tag push, and `skills/agent-contract/SKILL.md` §6
   withholds pushing from every agent. A case anchored there ships skipping,
   and `test_the_measured_commits_are_still_here` gains a third way to go red
   for a reason nobody caused. The real range is re-derived as a recorded
   measurement instead; the planted case is constructed.
6. **The floor, the scoring, the two exemption row shapes, the report's
   text.** Untouched. A gate change is judged by what it does when it is
   wrong, and widening the diff widens what has to be judged.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · the range's own review paperwork no longer subtracts the survivor it quotes | **Given** a range whose only added file is a round record quoting a sentence the range removed elsewhere, **when** `survivor-check` runs over it, **then** the survivor is reported and the exit code is **1** | A constructed-repository case in `tests/test_a_corrected_sentence_survives_elsewhere.py`, driven through git from Python (§8). Seen red against the module as it stands **before** the fix; `phases/phase-1.md` quotes that run. Green after |
| A2 · the removed-sentence count does not move, and no round record becomes a source | **Given** the same range, **when** the filter is applied to `paths` rather than to the added side alone, **then** the number of removed sentences the report names is unchanged, and no reported source sits under a `rounds/` directory | The same case asserts the count and the sources. Re-derived once on the real range `7e17f5e..941dab5` while those refs resolve: round 2 measured 16 removed sentences before and after, and the survivor at `seal/specs/1789100139-…/changelog.md` reported again at 2.00 (`rounds/round-2-report.md:160-163`). Recorded in the memo as an **executed measurement**, not as a planted case |
| A3 · the docstring says which sides, and the sentence is pinned | **Given** §*What is excluded, by construction rather than by list*, **when** a reader asks which side `rounds/` is excluded from, **then** the text names the pool **and** the range | A case that turns red when the sentence is deleted and when it is reworded to name one side only. `agent-contract` §14 — the fix changes a verdict a person reads and acts on |
| A4 · every path list this module derives from git is filtered or named | **Given** the module's source, **when** the enumeration case runs, **then** each of the three call sites is either filtered by `records_a_past_round` or named in the case with its grounds, and a fourth unfiltered, unnamed call site turns it red | The case seen red two ways: the filter removed from `corrected`, and a new unfiltered path-list call added to the module. Precedent for the shape: `tests/test_a_row_points_by_content.py:994-1025`, which enumerates `content_at`'s callers the same way |
| A5 · the gate change carries what `CONTRIBUTING.md` asks of one | **Given** `CONTRIBUTING.md` §*What a change to a gate must carry*, **when** the pull request body is read against its four bullets, **then** each is answered: **red** — the case and how it was shown; **direction** — stricter, and the wrong answer is a false positive, a record's quotation reported as a survivor, which is the cheap mistake because `records_a_past_round` keeps records out of the pool so the report lands on the real coordinate and `survivors.md` is the escape; **prompt budget** — **zero**, nothing asks anybody anything at run time or at commit time; **platform honesty** — `-z`-separated paths and blob reads only, `records_a_past_round` already normalises `\` to `/`, and no Windows run is claimed | A reader opens the body against that section. Nothing in the suite reports the budget, which is why it is a pull-request clause |
| A6 · the records claim only what was measured | **Given** that #361's round 3 measured the prediction *#365 re-arms the exemptions* **false** (`rounds/round-3.md:144`, `:183`), **when** this work item's changelog fragment and memo are read, **then** they say the exemption path is still open and name where it is tracked, rather than repeating the prediction | `grep` the fragment for the claim; `bin/unverified-check` on the memo, whose `## Not verified` table carries the row with its answerer |

## Data & interfaces

No schema, no endpoint, no flag. One list comprehension, one docstring
section, two test cases, and the records.

The evidence ledger coordinates this touches, referenced rather than
duplicated:

| Row | Anchor | What happens to it |
|---|---|---|
| `seal/ledger.md` S3 | `survivor_check.py#corrected@65b199e3`, `#score@0b214b20` | **DRIFTED** by the edit. The claim — a sentence is corrected where the file holds it fewer times at `b` than at `a`, counted rather than tested for membership — is untouched by adding a filter to the path list. Re-read, dated, and `bin/evidence-check --reverify .` |
| `seal/ledger.md` S6 | `survivor_check.py#records_a_past_round@356dd3ce`, `#corpus@cfdd6a91` | Neither body changes, so no drift. Its claim stays true and becomes narrower than the behaviour. Not widened in place — the wider claim is a new row in this work item's fragment |
| `seal/ledger/1789211172-….md` | new | Rows for the range-side exclusion and for the enumeration case. The directory does not exist and is created here |

## Open questions → questions.md

One row, **Q1**, a person's, with a default that lets the build run:
whether `seal/specs/*/survivors.md` joins `rounds/` in the by-construction
exclusion, and on which sides. Its full text, both options and what each
measured are in `questions.md`.

**Answered 2026-09-12, before the first edit: *out*.** This work item ships the
`rounds/` filter alone. The exemption path is #371, which carries round 3's
two-run measurement and the argument against. Plan phase 4 closes as
`deferred #371`; phases 1, 2, 3 and 5 are unaffected, which is what the
default was chosen to guarantee.
