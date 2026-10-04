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
- **Routing, decided at the start** — **first, if this repository has `seal/` at neither `<repo>/seal/` nor `$(git rev-parse --git-common-dir)/seal/`: stop and follow the Bootstrap section of `skills/implement/orchestration.md`, the `implement` skill's orchestrator half.** Writing the file below is what CREATES that directory, creating it is what opts the repository in, and WHERE it lands — committed with the repository, or under the git directory and on this machine only — is the user's decision and not yours. Then, before the first edit, write `seal/specs/<work-item-id>/routing.md` from `templates/sdd-routing.md` and commit it — the write **in a command of its own**, never batched with the commit. The gate reads that file from the working tree, so a declaration on disk silences the very commit that adds it and no first-commit waiver is needed; but in a clone whose git hooks slot is somebody else's the gate is a `PreToolUse` hook that denies the WHOLE Bash call, so `write && git add && git commit` in one call writes nothing and the declaration the gate then reports missing is the file that was lost. Where this plugin's git hooks run, git judges the commit itself and the write goes through, so the separate command costs nothing there and is the one shape both readings accept. This is the one place the batching rule above misleads. **Ask it as two questions in ONE `AskUserQuestion` call**, never one axis at a time. Question 1, single-select: `automation` — every party runs and nothing stops to ask again · `per axis` — the boxes below are the answer · `no work item` — no frame, no review, no seal, no `routing.md`, this session writes the change, and every commit needs `[no-review]` in front of it. Question 2, a `multiSelect` of exactly four boxes and meaningful only under `per axis`, in this order: run end to end without stopping to ask (`Automation` = `yes`; unchecked is `no`, meaning this run may stop to ask, NOT that a person did it by hand) · implement with `smith` (unchecked, `the session` writes the code) · review with `warden` (`through the review chain`; unchecked, `straight to the PR`, and nothing reviews this code before the pull request) · open the pull request (unchecked, `stop before the pull request`, and the branch is handed back committed and unpushed). Four options is the cap and it is fully spent — a fifth box breaks the shape. What is checked is the answer, and each box is a row of that file; the file also records WHICH answer was pressed, because a pressed preset and four ticks by hand are otherwise the same bytes. You ask it whether or not a `framer` runs: a subagent in this harness has no `AskUserQuestion`, so a framer cannot ask and is told to report a missing declaration rather than write one. Asking the reviewer in the middle and the pull request at the end is three waits for one decision. The commit gate reads that file, so a declared work item commits silently for either review answer, and CI reads the same file at the pull request. For a change belonging to no work item, `[no-review]` still waives one command (`[no-parity]` too where a migration config is declared) — in front of the command, quotes included, `: '[no-review]'; git commit …`, because after `git commit` a bare word is a pathspec and git rejects it; `git -c specseal.waive=review commit …` is the same waiver in git's own spelling. Deciding at the commit is what stops a release mid-run.
<!-- specseal:end -->

<!-- Above: a generated copy of templates/claude-md-block.md, the block
     install.sh distributes. Edit the template, then
     `python3 .github/scripts/claude_block.py --write` regenerates this copy;
     the hygiene workflow fails a pull request where the two differ.
     Below: repo-local development rules for SpecSeal itself. -->

## The goal a design is chosen against — verification that runs unattended

**Verification through an automated workflow is this project's first goal.**
Between two designs that catch the same defect, the one that stops to ask a
person is the more expensive, and the difference has to be argued rather than
assumed. Time and stability are what the argument is being made for.

This is a goal, not a rule, which is why it sits above them: it decides
between options where no rule is broken either way. `CONTRIBUTING.md`'s *What
a change to a gate must carry* turns it into something a pull request has to
answer. `skills/implement/SKILL.md` §*1. Read the spec before the code* holds
the rule this goal produces for a session, with its reasoning: whatever needs
a person is asked once, together, before the first edit, and nothing comes
back mid-run.

## Repo rule — the merge method is fixed per direction, and it is not a preference

`docs/branch-and-release.md` §*Work accumulates on a release branch* states
this rule in its *Which button, for each direction* table and holds the
reasoning; this row is the link, and it is here because a session about to
merge a pull request has no other reason to open that file. A pull request
into `release/vX.Y.Z` is squashed and one into `main` takes a merge commit,
whichever button a page happens to offer first.

## Repo rule — no real identifiers in examples or fixtures

`CONTRIBUTING.md` §*House rules* states this rule in its *No real
identifiers* bullet and holds the reasoning; this row is the link, and it is
here because a session writing an example, a fixture or a document has no
other reason to open that file. A domain written there is `example.com` and a
user path is `/Users/x/`, never a real domain, path or organisation name.

## Repo rule — a thing more than one party can have is named with whose

`skills/writing-style/SKILL.md` §*여럿이 가질 수 있는 것은 누구 것인지
밝힌다* states this rule and holds the reasoning; this row is the link, and
it is here because a session rewording an agent definition or a skill has no
other reason to open that file. The concept and its format names stay bare —
the Seal Test, a seal block — and a reference to one instance says whose.

The word that bought it is `seal`: it named the warden's review mark, the
sealer's stamp and the smith's proof block at once, two of them in files a
reader opens together. `tests/test_one_word_one_meaning.py` is the check, and
it holds one word per conversation somebody had — writing the rule down is
not the repair, the check is.

## Repo rule — commit early; on a declared branch it costs nothing

`skills/implement/SKILL.md` §*2. Implement, and feed evidence back where you
verified it* states the commit cadence and holds the reasoning, and it tells a
reader to check two conditions against their own repository; this row is that
check for this one, and it is here because a session reaches the question
after every edit without opening that file. Both conditions hold here: a
feature branch squashes into its release branch, and every work item commits
its `routing.md` before the first edit. So commit as soon as a step stands on
its own.

**Commit freely: a ledger row names no commit for a squash to orphan.** How a
coordinate names code, how a released row is read again, and what to do when
a ledger file conflicts live in `docs/the-evidence-ledger.md` §*A row is a
content anchor, and it names no commit*, §*A released row is read again in
the branch's fragment* and §*A correction a merge dropped*.

## Repo rule — a change writes fragments, never the shared file

Which file a change writes — its changelog entry, its ledger rows, and its
re-reads and corrections of a released ledger row — is
`docs/the-record-layout.md` §*A change writes fragments, never a shared
file*. This repository declares `Ledger frozen from` in `seal/config.md`, so
its released ledger files never change; `docs/the-evidence-ledger.md` §*A
released row is read again in the branch's fragment* holds what that means
for a branch. The release gathers and folds the fragments with the commands
in `docs/release-checklist.md` §*2. Gather, fold, bump*.
