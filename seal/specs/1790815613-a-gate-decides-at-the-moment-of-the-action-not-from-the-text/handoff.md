# 1790815613 — handoff

Written 2026-10-02 by the orchestrating session. The owner is moving the run to another machine, so this file records the work's state at the point it stopped. Read it together with `routing.md`, `questions.md` (P1–P7) and `overview.md`. Nothing here overrides them.

## Where it stopped

| | |
|---|---|
| Issue / pull request | #692 / PR #705, draft into `release/v0.17.0`, labelled `chain: capped` |
| Branch head | the commit that adds this file, after `c644f719` |
| Base | `origin/release/v0.17.0` @ `e4399b65`, merged in at `2ac372ec` |
| Review chain | **ended**, `capped` at round 4. That round found nothing that needs a fix. No further round is owed. |
| Broad gate | `SEALED … @ 2ac372ec against e4399b65`. **It is stale.** Commits made after the chain followed it, so the branch must be sealed again before it can go ready. |
| CI | ubuntu and macOS were green at `a1f8709d`. Windows had never completed before `a793b9dc` and now completes **with 17 cases failing** (below). |

## What happened after the chain

None of these were read by any round, and each is a row in `overview.md`.

1. **The ceiling.** `docs/commit-review-gate-spec.md` passed 1,000 lines. On the owner's decision it is frozen until #715 (`seal/config.md`, `Over the ceiling`). Do not change its fold markers.
2. **Three cases failed in CI only** (`923ec630`). Both causes were in the cases:
   - one borrowed the machine's own `claude` process;
   - one modelled the Bash call as `bash -c CMD`, and bash 5.1 and later exec the last command.

   The fix was reproduced in a Debian bash 5.2 container.
3. **The Windows leg hung** (`18d4b5dc`, `a793b9dc`). The cause was the corpus row `until false; do <commit>; done`, which never ends when it is really run. A timeout that kills only the direct child left the loop holding the pipe. The row now `break`s, and a bounded runner names any row that does not end. Diagnostic runs 36974611769 and 36978391812 pinned it, and the diagnostic branch has been deleted.

   The stuck runs of this branch were cancelled: 36954085630, 36955541007, 36962188955, 36963419529 and 36973279841. The smith also killed 58 orphaned `until` loops on the old machine. On the new machine, check for none with `ps -ax | grep 'until false'`.

## What is owed next, in order

1. On the new machine, check out `feat/692-a-gate-decides-at-the-moment-of-the-action-not-from-the-text` and pull it. Check that the commit identity is `zenith.m.jo@gmail.com`.
2. **Fix the 17 Windows failures.** They are listed in `overview.md` §*Not verified*, in three groups. Work through them in this order:
   - **(3) First, because a person on Windows meets these, and they may be defects in the code:**
     - `test_s2_…[shape: stdbuf]`: a commit into `main` landed with the stubs installed.
     - `test_s4_under_the_press_the_refusal_names_no_question_tool`: the press was not read, so an automation run is told to ask.
     - `test_a_bash_creation_under_the_harness_path_buys_no_consent` and `test_an_answered_creation_runs_and_the_record_follows_it`: the guard counts other sessions starting from a `claude` ancestor. Git for Windows' `ps` takes no `-o`, so `hooks/hooksession.py#claude_ancestor` finds none there.
   - **(1) Documented Windows limits whose cases carry no skip.** These are the sequencer exemption (4), the mark keyed without the process (1), the old spelling that needs `ps` (3), and the s9 lease case (1). Skip each with the repository's own idiom, naming the known limit it rests on. Do not skip anything without that limit behind it.
   - **(2) Cases that assume POSIX paths or modes** (4): backslash separators, an MSYS `/c/…` path, the execute bit, and a Windows path inside a Python string literal. Fix the cases.
   - `test_the_shells_own_spelling_of_the_command_still_matches` is not deterministic on Windows: a different parameter failed in each of the two runs.

   Treat this as one more fix made after the chain. Record it in `overview.md`, and have every case seen red where it can be.
3. Run `python3 skills/verify/scripts/broad_gate.py --preflight --base release/v0.17.0`. If `origin/release/v0.17.0` has moved, merge it first with `--no-ff` and resolve hunk by hunk.
4. Spawn `specseal:sealer` with `bin/broad-gate --base release/v0.17.0 --record seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text`, then commit the cell it writes.
5. Update PR #705's body. Its *A fix after the chain* section names the ceiling only, so add the CI-only cases, the Windows hang and the Windows failures. Then push, wait for every CI leg including Windows, and mark it ready.

## Decided, and by whom

- **P1–P4** were decided by the owner, plus P3 by the build. The PR body's *Decided* section records all of them.
- **P5 (owner):** the text gate stays as the fallback.
- **P6 (owner):** creations go through the frozen reader too.
- **P7 (owner, 2026-10-02):** the text reading stands aside only for a plain shape (`hooks/tokens.py#is_plain`), because a deny-list of spellings did not converge across rounds 1–3.

## Open, and who answers

- #716, #678, #686, #715 and #718 are milestoned `release: 0.18.0`. #678 and #686 each carry a comment with their real status.
- The plain allowlist covers 38% of committing commands. Widening it is a later change.
- M5, the minimum harness version for the session variables, and CI's git version are the orchestrator's to settle.

## The rest of 0.17.0

- PR #719 (#717) is the other open item, and its `handoff.md` holds its state.
- Release preparation, the manual release seal (#718), and the per-agent model split are in that file's *The rest of 0.17.0*.
