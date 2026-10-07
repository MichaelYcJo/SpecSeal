# 1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | the records commit whose subject begins `docs: the records of #854's phase 1` — `plan.md`'s Status cell carries its hash |
| Ran by | smith on Opus 5.5 (named by the spawn prompt) |

## What this phase was asked

Implement the plan's one phase from round 3's report of work item 1791270162:

- fix 🟡 1 by the paste-ready fix and close its class, enumerating `git rebase -h`'s long options against the installed git and checking each prefix that could be read as a branch-taking or branch-changing option;
- plant S1–S5, each new case seen red at `3d78c220` first, and extend the git-binding case with the new switching forms;
- run `bin/mutation-check` on each changed unit;
- write ⬜ 2 and ⬜ 3 into `docs/worktree-guard-spec.md` with their pins;
- write the changelog fragment, the ledger rows, `overview.md` and this record, and fill `plan.md`'s Status;
- `bin/evidence-check --strict .` and `survivor-check --range origin/release/v0.20.0...HEAD` exit 0; only the guard modules and the touched slices run, no full suite, no push.

## What this phase found

**The frame held.** Every coordinate the spawn and `spec.md` named exists as described: `_rebase_names_a_branch` at `3d78c220` ended options at `--` only and asked `"--root" in args`, `SWITCHING` and the git-binding case were where `plan.md` put them, and the §A and §*Known limits* sentences round 3 quoted were there.

**The class, measured on git 2.50.1.** `git rebase -h` lists one long option that changes how many words name a branch, `--root`. git took `--ro` and `--roo` as `--root` and moved HEAD; `--r` was refused as ambiguous, `--roots` as unknown and `--root=x` as taking no value, each with exit 129. `--end-of-options` is taken only spelled whole: `--end-of`, `--end-of-option` and `--end` are unknown options. `--o` and `--on` read as `--onto`, whose value the guard already counts as a word. So the fix reads `--root` from `--ro` rather than from round 3's `--r`, which only git's refusal separates.

**One more spelling in the class.** The base read `--root` off `args`, before redirections are taken off, so `git rebase --root>/dev/null feature/x`, which bash runs as `--root feature/x`, was listed. Reading it off the plain words closes it; the case is red under the old reading.

**Three breaks survived the first cases, and each took a listed case.** Taking `--r` as a prefix, reading `--root` past the end of the options, and dropping the prefix check all passed the rebase cases. `git rebase --r feature/x`, `git rebase --end-of-options --ro` and `git rebase --roots feature/x` now pin each, because git switches on none of them.

**The git-binding case needed a branch whose name starts with `-`.** `git branch -- -x` refuses the name (exit 128); `git update-ref refs/heads/-x HEAD` makes it. With it in the template, the case runs `rebase --end-of-options <start> -x` and `rebase -- <start> -x` against git, so a wrong end-of-options reading goes red there and not only in a stub.

**The ledger.** The fix moved the anchors of eight rows in 1791270162's fragment and of the K6 and G17 re-reads. Each was read and still holds, so `evidence-check --reverify --into` re-stamped them in place and wrote no `Re-read ·` row; F3's claim is short of the two new spellings but not false, and R1 carries them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `_rebase_names_a_branch`'s exact-match reading of `--root` off `args` | the prefix reading off the plain words, in the same function, and R1 |
