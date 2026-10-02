# 1790913304 — handoff

Written 2026-10-02 by the orchestrating session. The owner is moving the run to another machine, so this file is the state of the work as it stopped. Read it with `routing.md`, `questions.md` and `overview.md`. Nothing here overrides them.

## Where it stopped

| | |
|---|---|
| Issue / pull request | #717 / PR #719, draft, into `release/v0.17.0` |
| Branch head | the commit that adds this file, which follows `83612ae1` (round 2 closed) |
| Base | `origin/release/v0.17.0` @ `e4399b65`, merged in at `2bf10c9e` |
| Review chain | round 1 closed: 3 fixed, 1 answered, 1 deferred to #720. Round 2, a verifying round, closed: 4 fixed, 1 answered. Its fix range is `0bef982a..483c3770` |
| What is owed next | **round 3, a verifying round** over round 2's fix range. Then the sealer |
| Broad gate | not yet run on this branch |

Round 2 closed on fixes, so it used the run's one reopening. `round-record new` will say that **round 3's record ends the run whatever it finds**. Anything round 3 leaves open is deferred to an issue, and the pull request takes `chain: capped` if the generator says capped.

## The next steps, in order

1. On the new machine, check out `fix/717-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner` and pull it. Check that `git config user.email` is the owner's SpecSeal address, the one this branch's commits carry.
2. If `origin/release/v0.17.0` has moved past `e4399b65`, which it will once PR #705 lands, merge it with `--no-ff` and resolve hunk by hunk. Earlier merges conflicted only in `seal/releases/*.md` rows, and each row was taken from the side that edited it. Run `bin/evidence-check --strict .` and `bin/correction-check --range origin/release/v0.17.0...HEAD` afterwards.
3. Spawn `specseal:warden` for **round 3, verifying**. Give it:
   - the target as the branch head;
   - the diff to verify as round 2's fix range `0bef982a..483c3770`;
   - the finding surface as nothing new, since round 2's `New units` reads none;
   - the ⬜ verdicts 6–10 in `rounds/round-2.md`.

   Forbid it `claude -p` and any settings file, and point it at the hook-direct probes rounds 1 and 2 used. Then write the record with `bin/round-record new` (its paragraph in a file, `--ran-by "specseal:warden on <model>"`, `--pr 719`), commit it, and close it with `bin/round-record close` if anything needs closing.
4. Run `python3 skills/verify/scripts/broad_gate.py --preflight --base release/v0.17.0`. It must pass, `seal`'s refusals included.
5. Spawn `specseal:sealer`, running `bin/broad-gate --base release/v0.17.0 --record seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner`. Then commit the `Broad gate` cell it writes.
6. Update PR #719's body with a *Review chain* section (rounds 1–3) and a *Broad gate* section, then push. Wait for CI on every leg, Windows included, and mark the PR ready.

## Decided, and by whom

- **The design**, by the owner from rendered prototypes, 2026-10-02: a letter on parchment, with the seal at 0.90 pressed over its bottom and right edges. The rope and the outer light-red band are removed, and the lily is pressed in red. The panel drops the rows that can only say "passed", and the workflow row reads `CI also  <n> more steps`. #717's body records it.
- **Several seals in one turn**, by the owner, 2026-10-02 (`questions.md` Q6): draw as many of the oldest as fit with their disc. The rest wait for the next `Stop`, and the disc is never dropped for sharing a turn.
- **The limit**, measured by the build with a scratch `Stop` hook through `claude -p`: 10,000, counted in UTF-16 units. A character outside the BMP counts as two.

## Open, and who answers

- **The owner, at the first real seal on 0.17.0:**
  - whether the stamp arrives whole;
  - how the parchment reads on a light terminal, where its contrast against white is 1.02;
  - what the installed 0.16.0 hook does with this branch's values file.

  These are the `overview.md` *Not verified* rows.
- **The orchestrator:** a user-defined exception with a very long type name can pass the reserve, because `record` does not cap the type name. This predates #717. Round 2's fix pass left it for the round record and the PR body.
- #720: a wide character in a branch name shifts the disc's row. This predates #717.

## The rest of 0.17.0

- PR #705 (#692) is the other open item. Its own `handoff.md` holds its state.
- **Release preparation** comes after both items land, on branch `chore/the-fragments-become-0.17.0`:
  - `gather_changelog.py --version 0.17.0` and `fold_ledger.py --version 0.17.0`, in one commit;
  - the `plugin.json` bump;
  - the full checks;
  - the release pull request into `main`, as a merge commit;
  - the `v0.17.0` tag, which is the owner's to push.
- **After the tag publishes the release note**, attach one release-wide seal by hand: `gh release upload` the PNG, and `gh release edit` it into the place of the note's `At a glance` table, with that table's two counts kept beneath it as text. #718 holds the plan and automates it for 0.18.0.
- **Model split for this release:** framers on Fable, and smith, warden and sealer on Opus.
