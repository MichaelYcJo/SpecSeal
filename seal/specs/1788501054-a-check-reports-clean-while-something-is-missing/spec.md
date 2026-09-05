# Feature Specification: a check reports clean while something is missing

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-handoff-protocol.md:385` | The handoff carries *"the runner incantation"*, and says nothing about which form of a command that takes a narrowing flag. The narrowing that makes `--reverify` safe to write is the same one that makes the read blind |
| `templates/sdd-round.md` | *"written by the review orchestrator right after it posts"* — and nothing observes it. Measured twice in this release, four minutes and two minutes late |
| `CLAUDE.md` §*a ledger coordinate names content* | *"A row whose anchor a change removes is REMOVED"* … *"A branch that removes code an existing `seal/ledger.md` row cites must touch that file"*. Nothing tells a branch that it did |
| `docs/review-chain-spec.md` | Owns every refusal `chain_check.py` makes at the pull request, with a subsection each. A new refusal owes one |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget |

## Scope

**In — #153.**

- The handoff names **two forms and what each is for**: the unscoped read, which is what tells a segment what it broke, and the scoped `--ledger` write, which is what keeps `--reverify` off a row somebody else owns.
- `evidence_check.py` **says what it did not read** when narrowed. Guidance binds a session that reads the guidance; a session that narrows on its own initiative still gets a silent partial answer.

**In — #150.**

- `chain_check.py` refuses a round record whose **adding** commit descends from a commit its own verdict cells name as the fix, grandfathered by work-item id.
- Whether *the record carries what it says it verified* is checkable at all — **stated either way**, not assumed. A probe row naming a proposed fix with no fix in the file is the shape; whether that is machine-readable is the phase's question.
- `docs/review-chain-spec.md` gains the subsection, beside the seven it has.

**Out.**

- Changing what `--ledger` scopes. It is right for writing and this work makes reading the default rather than narrowing the flag.
- The pull-request job. It already runs the unscoped check and warns at one drifted row; nothing here changes it, and whether a round should run a check CI runs better is answered by the guidance rather than by moving the gate.
- #152's four findings, and S8.

## The risk this work item carries, stated before it is discovered

**This release has three times seen a branch break the rule it was adding** — the floor refused the only legal end to a run, the roll's guard broke the invariant it exists to keep, and the `Ran by` row removed the coverage of its own grandfathering arm. `seal/ledger.md`'s observation 5 records it and calls the mechanism structural: the branch writing a rule is the first code written under it.

**Two rules on one branch doubles the exposure**, and this is the first thing the rounds are told to attack. Specifically: a `chain_check` refusal added here is one whose own round records must satisfy it, and a guidance change here is one this branch's own spawn prompts should already obey.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A segment learns what it broke | Given a branch that falsifies a row in the shared ledger · When a round runs the check the handoff names · Then the row is reported | the handoff names the unscoped read; a case pins the sentence |
| A narrowed read announces itself | Given `--ledger` on a repository that also has `seal/ledger.md` · When the check runs · Then it says which ledgers it did not read | a case on the output |
| Writing stays narrow | Given `--reverify` on a work item's own fragment · When it runs · Then no row outside that fragment is re-stamped | the existing behaviour, pinned |
| A record written late is refused | Given a `round-N.md` added by a commit descending from the commit its own verdicts name as the fix · When the pull request runs · Then it fails, naming the row | a case seen red, mirroring the four cutoffs |
| A record updated in place is not | Given a record added with `open` cells and updated to `fixed at <sha>` when the fixes landed · When the same check runs · Then it passes | the distinction is the **adding** commit; a case for each direction |
| Old records are not made red | Given a work item begun before the cutoff · Then the refusal prints | a cutoff case at the boundary second |
| Nobody is asked anything | Given the whole change · Then no step puts a question in front of a person | the prompt budget: zero |

## Data & interfaces

A fifth cutoff, keyed to this work item's own id, in the shape `STRICT_FROM`, `SURFACE_FROM`, `NEEDS_FROM`, `DEPTH_FROM` and `RUNNER_FROM` already take.

## Open questions → questions.md

None open. The one worth recording is settled by evidence rather than by choice: whether the guidance alone is enough. It is not — a session that narrows on its own initiative reads the guidance nowhere — which is why the tool announces its own narrowing.
