# 1791076834-the-changelog-is-one-file-per-release — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/the-record-layout.md` F2, §*Every kind of record*, §*The size a reader takes whole*, §*A change writes fragments*, §*The root records*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `docs/review-chain-spec.md` §*What the sweep reads*; this work item's `spec.md`, `plan.md`, `questions.md`
· evidence: `seal/ledger/1791076834-the-changelog-is-one-file-per-release.md` — 6 new rows, 57 `Re-read ·` rows and 10 `Corrected ·` rows citing released rows
· verified: executed — the S1 and `section_body` probes, the modules each phase names, every new case against the base code, the mutations listed in `phases/`, `evidence-check --strict .`, `survivor-check` over the build range; unverified — the full suite (the sealer)

## Why this work exists

A reader who wanted one release read or grepped an 8,891-line file; each
release's notes are now `changelog/<X.Y.Z>.md`, `CHANGELOG.md` is the index,
and every reader and writer of the sections moved with them (#728, F2).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The pact grep's exclusion | D8: *Excludes or classifies `changelog/` as well — the moved text carries the same drawings* / `git grep -l` for a tree line naming `parity.md` finds nothing in `CHANGELOG.md` at `e141980a` and nothing under `changelog/` | the exclusion is added, as a guard | the old `CHANGELOG.md` exclusion was equally inert; a later entry quoting a tree would need it. Its mutation survives by construction (phase 1) |
| Which files `--check` reads | Scope 3: *`--check` reads the markers of every `changelog/*.md` file* / reads `changelog/<X.Y.Z>.md` only | version-shaped names | the survivor sweep's predicate reads the same shape (D5), and a `README.md` beside the release files is not a release; pinned by `test_the_check_reads_the_markers_of_every_release_file` |
| `gathered_fragments`'s signature (Q8) | Spec silent; Q8 asked whether the monkeypatch keeps its shape / it takes an optional `paths` | the listing is the caller's where it has one | `corpus` already lists the tree; the two cases that stubbed `read_blobs` pass `paths` and hold for both shapes |
| `seal/follow-up.md` row 72 | Q4: *coordinate only, the decision text unchanged* / its quote of `CONTRIBUTING.md`'s rule was brought to the rule's new wording too | the quote follows the rule | it is a citation of a rule this work reworded, not the row's decision; the decision and the answerer are unchanged |
| The index's paragraph and printed lines (Q7) | the work's to write | as `phases/phase-1.md` and `phase-4.md` record them | each is pinned by the case that reads it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck on the final tree | the sealer, once, after the review rounds settle |
| The update into 0.18.1 by 0.18.0's update skill: step 2b reads the index's first heading (S12, held by S2 and S3 in the tree) and step 3 meets the index (D7) | the first `/specseal:update` into 0.18.1, by whoever runs it |
| Why `evidence-check --strict .` reads 10 drifted rows at `origin/release/v0.18.1` itself (`templates/config.md`, `VERSIONS_OF_ANOTHER_PRODUCT`, `fake_venv`), which this branch inherits by its merge and did not cause | the orchestrator, for work items 1791076832 (#758) and 1791076833 (#756), whose fragments hold the readings |
| The real gather and note on this repository: `gather_changelog.py --version 0.18.1` writing `changelog/0.18.1.md` and the index line at release preparation, and `publish-release.yml` publishing from that file at the tag | release preparation for 0.18.1, and the tag push |

## Not done

nothing beyond `spec.md` §*Out*

## Fed back into the spec

- *Inferred during implementation:* release preparation stages
  `git add -A changelog/ CHANGELOG.md seal/ .claude-plugin/plugin.json`
  before the suite (D9's line, as `docs/release-checklist.md` §2 now carries
  it).
- *Inferred during implementation:* `a_changelog` reads
  `changelog/v?<major>.<minor>[.<patch>].md` at the root, the
  `VERSION_HEADING` shape with its optional `v` and two-part form.

## The by-construction greps, after the build

Every hit of `git grep -n CHANGELOG` outside the records, `changelog/`, the
0.4.0 design record and the sweep's one-file fixtures names the index for
what it still is — its first heading (`skills/update/SKILL.md` step 2b,
`tests/test_release_hygiene.py`, `test_chain_hooks_hardening.py`), its release
dates (`docs/issues-and-milestones.md`), the file the gather heads, the
`## Unreleased` it forbids — or names both shapes. `survivor_check.py`'s
`CHANGELOG` constant stays because a test monkeypatches it, and its note
about #293's 153 places is a measurement of that range.
