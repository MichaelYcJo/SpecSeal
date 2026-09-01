<!-- specseal:start -->
## Tooling
- Python: prefer uv · Node.js: prefer pnpm (always respect the project's existing manager).

## Safety
- **3+ Fix Rule** — same bug, 3 failed fix attempts → STOP. Re-examine the architecture, then ask.
- **Verification Gate** — no "done / fixed / passes" claim without running the check that proves it and reading its full output.
- **Verification Scope** — narrow and often, broad once. A slice runs what you just wrote; the handoff to review runs nothing broad; the full suite, lint, and typecheck run once, after the rounds settle. A broad run with an edit after it was spent, not banked.

## Session cost
- **Batch independent reads and runs** — every coordinate a task names in one call, every case from one file in one command. Round-trips are most of a round; cut the trips, never the investigation.

## Git
- Run lint/format/typecheck before committing.
- Worktrees only for concurrent sessions on the same tree — single-session work uses `git switch` (worktree-guard hook enforces this).
- **Routing, decided at the start** — before the first edit, write `specs/<work-item-id>/routing.md` from `templates/sdd-routing.md` and commit it — the write **in a command of its own**, never batched with the commit. The gate reads that file from the working tree, so a declaration on disk silences the very commit that adds it and no first-commit waiver is needed; but the gate is a `PreToolUse` hook that denies the WHOLE Bash call, so `write && git add && git commit` in one call writes nothing and the declaration the gate then reports missing is the file that was lost. This is the one place the batching rule above misleads. **Ask all three axes as one `multiSelect` question with three checkboxes**, never one at a time: implementation (`smith` · `the session` — an optional row), review (`through the review chain` · `straight to the PR`) and destination (`open the pull request` · `stop before the pull request`). What is checked is the answer, and each box is a row of that file — asking the reviewer in the middle and the pull request at the end is three waits for one decision. The commit gate reads that file, so a declared work item commits silently for either review answer, and CI reads the same file at the pull request. For a change belonging to no work item, `[no-review]` still waives one command (`[no-parity]` too where a migration config is declared) — in front of the command, quotes included, `: '[no-review]'; git commit …`, because after `git commit` a bare word is a pathspec and git rejects it. Deciding at the commit is what stops a release mid-run.
<!-- specseal:end -->

<!-- Below: repo-local development rules for SpecSeal itself.
     install.sh distributes only the marker block above. -->

## The goal a design is chosen against — verification that runs unattended

**Verification through an automated workflow is this project's first goal.**
Between two designs that catch the same defect, the one that stops to ask a
person is the more expensive, and the difference has to be argued rather than
assumed. Time and stability are what the argument is being made for.

This is a goal, not a rule, which is why it sits above them: it decides
between options where no rule is broken either way. `CONTRIBUTING.md`'s *What
a change to a gate must carry* turns it into something a pull request has to
answer, and `skills/implement/SKILL.md` §1 holds the reasoning — the cost of a
question is not its difficulty, it is when it arrives, and a question a
document could have answered was never a question.

Questions a person genuinely has to answer go in **one batch before the first
edit**. Coming back mid-run is the failure this exists to prevent.

## Repo rule — the merge method is fixed per direction, and it is not a preference

| From | To | How |
|---|---|---|
| `main` | `release/vX.Y.Z` | cut a branch |
| `release/vX.Y.Z` | a feature branch | cut a branch |
| a feature branch | `release/vX.Y.Z` | **squash** |
| anything | `main` | **3-way merge commit** |

Never choose one of these on your own, and never pick a method because a
button was convenient. Squashing the last row discards every commit the
release branch wrote, and two things point at those commits by SHA: the
`Verified … at <sha>` stamp on every `# RIDER:` comment, and the `Target SHA`
in every `round-N.md`. That happened once, `tests/test_a_rider_reaches_
its_file.py` went red, and a patch release exists to fix one line of it.

Two rulesets enforce this, so the wrong button is not offered: `main` allows
`merge` alone and `release/*` allows `squash` alone. Both require a pull
request and have no bypass actors, which means the release-preparation commit
needs a branch and a pull request too — it used to be pushed straight onto the
release branch. `docs/branch-and-release.md` holds the same table, the release
sequence around it, and the reasoning.

## Repo rule — no real identifiers in examples or fixtures

Examples, fixtures, and docs use neutral values only: `example.com` for
domains, `/Users/x/` for user paths. Enforced by
`tests/test_no_real_identifiers.py` in CI — extend its allowlist consciously;
never make a test pass by inlining a real domain, path, or org name.
(Both incidents that forced a history rewrite entered exactly this way.)

## Repo rule — commit early; on a declared branch it costs nothing

A feature branch squashes into its release branch, so every commit it writes
stops existing at the merge. A committed `routing.md` keeps the commit gate's
review arm silent, for either review answer. A review round records the
`Target SHA` it read, so anything still uncommitted is invisible to the
reviewer.

So commit at the smallest step that stands on its own rather than waiting for
"done enough". The wait buys nothing here, and it leaves a dirty tree for the
worktree guard to ask about. That question offers to bring the changes along
to the other branch or to leave them behind, and the answer that is usually
right, *commit them here first*, is neither button.

**A ledger coordinate names content, never a position:** `path#anchor@hash`.
The anchor is a symbol name where the language has one and a distinctive line
of text otherwise; the hash covers the anchored region. A row carries no line
number and no commit SHA, and `evidence-check` calls git for nothing.

That removes a whole chain rather than a rule from it. A line number moves for
edits unrelated to the claim, so the coordinate rotted, so the row was
re-anchored, so its baseline reset, so a stamp was needed, so a squash orphaned
the stamp. Three review rounds went on the links of that chain.

The `Checked` column holds the date somebody read the code. Re-verifying is
re-reading and then running `evidence-check --reverify`, which recomputes the
hash and names what it changed.

**A row whose anchor a change removes is REMOVED, not re-pointed.** Its claim
went with the code. Write the new claim as a new row in the work item's own
fragment.

## Repo rule — a change writes fragments, never the shared file

Two files used to take an append from every branch, and both cost a conflict
at the worst moment — after the broad gate has run, which forces it to run
again.

| Instead of | Write |
|---|---|
| an entry under `CHANGELOG.md`'s `## Unreleased` | `specs/<work-item-id>/changelog.md` |
| rows appended to `.specseal/map.md` | `.specseal/map/<work-item-id>.md` |

No two work items share an id, so no two branches share a file.

**Appended is the word, and a removal is not one.** A branch that removes code
an existing `.specseal/map.md` row cites must touch that file to leave the
ledger true — the row is removed there, and the new claim is written into the
branch's own fragment. `CONTRIBUTING.md` carries the same sentence, and the two
used to disagree: one forbade editing the file at all while the other forbade
appending to it, which left a branch in this position with no reading that
permits the only correct act.

This overrides the `implement` skill and `agents/smith.md`, which tell a
session to let the entry accumulate unreleased. That is the
plugin's answer for a repository with no fragment convention; this repository
has one, and the fragments are where an entry accumulates here. Neither
document names a heading any more; the override is about WHERE, not about a
sentence they no longer carry.

**The changelog fragments are gathered; the ledger fragments never are.**
Release preparation runs `.github/scripts/gather_changelog.py --version X.Y.Z`,
which concatenates every ungathered fragment into the released section. A
ledger fragment stays where it is forever — a row is checked against the code
it cites rather than concatenated, and the checker already reads the whole
`.specseal/map/*.md` glob.

A ledger fragment needs no header of its own. Every row in it carries its own
anchor and hash, so there is nothing for a header to declare.
