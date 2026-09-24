# 1790263216-the-older-statements-name-what-enforces-them — overview

📋 implement applied
· spec:     this work item's spec.md (Grounding, Scope, What a decision is, S1–S11, Data & interfaces), plan.md (phases 1–7, Technical context, Alternatives), questions.md Q1–Q4; skills/settle/scripts/fold_check.py (shape_problems, names_targets, numbered_statements, enforced_lines, bound); the fourteen documents under docs/ that the retrofit edits; the history of work item 1788826000's spec.md; CLAUDE.md §fragments, §commit early, §the merge method
· evidence: seal/ledger/1790263216-the-older-statements-name-what-enforces-them.md E1 added; seal/ledger/1790260563-…md F6 corrected; 29 release-file and shared-ledger rows re-read and re-stamped where they live (phases 1–6 name each)
· verified: executed — every phase's modules narrow (19, 38, 42, 60, 43, 37 and 32 modules), 24 mutations each seen red and restored, the editions cases red before their comparison existed, bin/fold-check and bin/fold-check --shape-from 0 at every phase end, evidence-check and survivor-check; read — the 83 decisions with targets not mutated, each opened and its assertion read against the breaking edit its phase record names; unverified — the full suite, lint and typecheck, which are the sealer's

## Why this work exists

115 folded statements were written before the fold's shape existed and named
nothing that reads them. Each now carries one `Enforced by:` line, and the
shape check binds every statement from then on.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A statement false against the code | `spec.md` §*Out, and why*: "No statement's meaning changes, except by `questions.md` Q1's route." `docs/branch-and-release.md` §*Work accumulates* said "two things point at those commits by SHA: the `Verified … at <sha>` stamp on every `# RIDER:` comment", and `test_no_rider_stamp_names_a_commit` holds that no stamp names a commit | Q1's route (a): the document is corrected to the code | The statement's own marker is work item `1788826000`, whose spec moved every stamp to content and kept `Target SHA`. So the document lagged a later work item's decision, which is the case Q1's default sends to (a). Phase 5's record (D89) quotes both sides |
| The same sentence outside any statement | `spec.md` scopes the retrofit to the 115 statements. `docs/one-root-by-lifetime.md` §*The dependency rule*, unmarked prose, and its Korean edition carried the same false half | corrected in both editions | `survivor-check --range e9dfe623..HEAD` named it as wording the range removed and still standing. Contract §12 owes the class, and the correction changes no rule |
| The decision numbering | the plan asks for one row per statement | 115 decisions, D1–D115, with each Korean decision sharing its English row in phase 6 | A Korean line is not a second decision. Its target is the English one byte for byte, and the editions test now holds the two lines to each other |

## Not verified

none — every decision is labelled `mutated` or `read` in the phase record that makes it, and the full suite, lint and format are the sealer's broad gate, recorded in the last round record's `Broad gate` cell.

## Not done

- **Nine lines say `nothing`**: 4 of case 1 (a person's or a session's
  act), 0 of case 2, 2 of case 3 (a record rather than a rule) and 3 of
  case 4 (no case reads it yet). Round 1's fix pass moved four lines from
  `nothing` to the pin on the rule's instruction (D6, D13, D14, D32) and one
  from a target to `nothing` (D33). `grep -rn '^Enforced by: nothing' docs/`
  lists them. The three of case 4 are the rules a check could hold, and each
  line names what would hold it:
  - `docs/the-evidence-ledger.md`: *A bound over the corpus is stated with
    its instrument and the moment it was taken*;
  - `docs/review-chain-spec.md`: *Three and five count rounds*. Rule 13 of
    `tests/test_the_rules_have_one_owner.py` pins the statement's third bold
    sentence and not this opening, which round 1 reworded with both cases
    green;
  - `docs/measuring-a-run.md`: *A network write only a person's typing
    starts is not a hook*.

  No issue was filed, by `questions.md`'s answered row.
- **`CLAUDE.md` carries a false sentence, and this work item does not edit
  it.** Its §*the merge method is fixed per direction* says *two things point
  at those commits by SHA: the `Verified … at <sha>` stamp on every
  `# RIDER:` comment, and the `Target SHA` in every `round-N.md`*. The rider
  half has been false since work item `1788826000`. `survivors.md` exempts it
  with that ground, and the repository owner is who corrects it.
- **`docs/branch-and-release.md`'s *A third reader points at those commits
  now*** counts the two readers the corrected sentence used to name, and only
  one of those still names a commit. It is the bold opening of a measured
  record (D90, case 3), and its claim about the plugin directory holds, so it
  was not reworded.
- **`CONTRIBUTING.md`'s pairing sentence is now narrower than the check.** It
  says the editions carry the same heading levels and fold markers. The
  editions test also pairs `Enforced by:` lines now. The sentence is not
  false, and a ledger row quotes it, so it was left as it is.
- **The stacked item's changelog fragment** (`seal/specs/1790260563-…/changelog.md`)
  says *This repository declares `1790154761`*. After this work item the row
  is `0`, and this work item's own fragment says so. The two fragments
  gather into one release section. That fragment belongs to the stacked work
  item, whose fix pass is running in parallel, so this work item did not
  edit it.
- **The milestone description of `release: 0.15.3` says 101.** Correcting a
  tracker text is a post, and posts are the orchestrating session's
  (`spec.md` §*The measured worklist*).

## Fed back into the spec

none
