# 1788411058-the-mode-is-two-shell-lines-in-a-readme — review round 3

<!-- The verifying round for round 2's fixes (target: the diff
e3d71b2..62805af). Asked one question — did those fixes create a fourth member
of the class — and the answer was yes. Round 4 verifies. Written by the review
orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from e3d71b2, reviewed at 62805af; d5ad9a3 is round 2's record and carries no code |
| PR | none yet |
| Broad gate | not yet — a 🔴 was open |
| Fixes checked by | round-4 |
| Contract changes | none — one pathspec prefix, two message strings |
| New units | three test cases |
| Needs a fix | yes — 🔴 1 (the way back exits 0 having unstaged nothing outside the repository root), 🟡 2 (two of round 2's five cases were empty), 🟡 3 (the version-mismatch message calls this plugin's own file somebody else's) |

- [x] Pass

## What this round was asked to attack

One question and a five-item list, and nothing else — the orchestrator had
already re-derived the closures, run the suite and lint, mutation-tested every
unit, and checked every document, so the prompt told the round not to repeat
any of it and not to read the documents at all.

The question: **rounds 1 and 2 both found the previous fix pass aimed at the
coordinate rather than the class — a path this command touches whose guard was
reasoned about a different member. Did round 2's five fixes create a fourth?**

Where to look was named: `plugin_workflow()`'s swallowed failures, the
discarded `"unstaged"` status, every remaining `git()` caller, the pathspec in
the two sentences, and `refusals` refusing on `None`. Plus: are the five
planted cases empty?

## The answer

Yes, and it is the fourth in a row.

`git reset -- seal .github/workflows/hygiene.yml` is read from the current
directory. Run anywhere but the repository root it exits 0, prints nothing,
and unstages nothing — so the switch back refuses over the changes the switch
itself staged. The bare `git reset` it replaced worked from anywhere. **Round
2 fixed the member where a bare reset unstages too much and broke the member
where a person is not standing at the root.**

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 🔴 1 | the workflow's failed stage | `#install_workflow` | answered — but its case was empty, which is 🟡 2 | reviewer executed with `.github/` ignored |
| r2 🔴 2 | `seal mode reset` | `changelog.md` | answered | reviewer read |
| r2 🟡 3 | the way back left the workflow | `#remove_workflow` | answered; the message is 🟡 3 | reviewer executed the sequence, and the version-mismatch shape |
| r2 🟡 4 | the submodule guard's fail-open | `#gitlinks_under_root` | answered — reproduced, and the message reaches a person | reviewer forced the failure and checked it does not misfire: `git ls-files --stage -- seal` exits 0 with no path, no commit, and a separate git directory |
| r2 🟡 5 | the untracked note | `#switch` | answered — but its case was empty, which is 🟡 2 | reviewer reverted it: nothing reddened |
| r2 🟡 6 | `git reset` unstages everything | two sentences | **answered at that member and broken at another** — 🔴 1 | reviewer executed from a subdirectory: exit 0, index unchanged, then the switch back refuses |
| 🔴 1 | the pathspec is relative to the working directory. From a subdirectory the named command exits 0 having unstaged nothing, and `seal mode local` then refuses over what the switch staged | `skills/implement/scripts/seal.py:1884`, `:2004` | fixed at abb6319 — `:/` on both paths, in both sentences and three documents, with the reason in the sentence | reviewer executed the whole sequence from `docs/`; orchestrator reproduced it and confirmed `:/` unstages from there. The planted case runs the command the output names, from the subdirectory it was printed in |
| 🟡 2 | two of round 2's five cases redden nothing. The workflow-staging case ignores `seal/`, so it covers the ROOT's staging — the fix before it — and never the workflow's. The untracked-note case plants a genuinely untracked file, so both readings of `indexed` pass it | `tests/…` | fixed at abb6319 — `.github/` ignored, and a TRACKED `config.md` | reviewer ran all five mutations: three reddened one case each, two reddened nothing across five test files |
| 🟡 3 | `plugin_workflow()` pins to the version installed now, so upgrading the plugin between the two switches leaves the file unmatched — and the message then calls this plugin's own file *not what this plugin writes*. The direction is safe; the sentence is not | `skills/implement/scripts/seal.py:1600` | fixed at abb6319 — the message says the file is pinned to the version that wrote it | reviewer executed with the version moved 0.5.0 → 0.6.0: `removed`, then `kept` |
| 🟢 4 | `plugin_workflow()` returning `""` | — | pass — `remove_workflow` compares only after `PLUGIN_CLONE in text`, so `text` is never empty and `"" != text` keeps the file, which is the safe direction | reviewer read |
| 🟢 5 | the discarded `"unstaged"` status | — | pass — the exit code is unchanged and matches the root's own failure path; a person can tell, a script cannot. No grounds found to overturn round 2's deferral | reviewer read and executed |
| ❓ 6 | four `git()` callers still report a failure as a success, and `seal.py:947`'s is the sharp one: an empty `remote.origin.url` switches off the whole other-repository check, so a zip from elsewhere merges without a word. All four are `seal export`/`import`, none moves or removes anything, so none is a member of this diff's class | `skills/implement/scripts/seal.py:322`, `:323`, `:947`, `:1476` | deferred — an issue, since it belongs to #81's command pair rather than to this work item | reviewer read each consumer |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `seal mode shared` from `docs/`, then the command it named, then `seal mode local` | exit 0 / index unchanged / exit 1 "not clean" — 🔴 1 |
| reviewer: the named reset from the root, with one path staged, with no commits, with a separate git directory | all exit 0 and correct |
| reviewer: `git reset -- :/seal :/…` from `docs/` | exit 0, index unstaged |
| reviewer: five mutations, one per round-2 fix | three reddened one case each; two reddened nothing across five test files — 🟡 2 |
| reviewer: the plugin version moved between install and remove | `removed`, then `kept` — 🟡 3 |
| reviewer: `git ls-files --stage -- seal` with no path, no commit, a separate git directory | exit 0 each — the `None` refusal does not misfire |
| orchestrator: the subdirectory sequence, before and after | index unchanged; then unstaged and the switch back succeeds |
| orchestrator: three mutations, one per fix | each reddens its own case and no other |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | 1595 passed · 1 skipped; clean; 435 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–2 | `#indexed`, `#install_workflow`, `#remove_workflow`, `#gitlinks_under_root`, `#switch` | five units changed in every round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Four `git()` callers in `seal export`/`import` report a failure as a success, one of them switching off the other-repository check | a new issue | the repository owner |
| Whether `chain_check.py`'s step should carry `if: always()`; whether the workflow status strings should be read or dropped | round 2's record | the repository owner |
| `bin/seal`'s example list, `--check` with both roots, `config.md` as a directory, the Windows pathspec spelling | round 1's record, `questions.md` Q2, `overview.md`, the windows leg | the repository owner |
