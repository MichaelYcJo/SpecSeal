# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | eaba2dd1 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

#561, added at the resumption: land the release checklist's before-and-after
ledger count as the issue carries it (verified on #547's branch). That means
the before-readings in step 2's second block, and the glob-free
`find … -exec cat {} + 2>/dev/null | grep -c '^|'` in a fence at §3, with a
subject for the sentence after the fence. Then measure it in zsh on a scratch
copy: before the split, after `--split`, after `--version`, with equal
counts. It has to land before the 0.15.1 release runs step 2.

## What this phase found

**The fix is the issue's, with the sentence given a subject** (read against
`docs/release-checklist.md` as D left it). The issue's diff applied as it
stands; the sentence after the fence opens *This command prints here …*.
The `find` command is 100 columns, and the wrap check skips fenced blocks, which
is why it sits in a fence and not inline.

**Measured in zsh 5.9 on a scratch clone, first at `eaba2dd1`** (executed).
The table lines read 1047 before `--split`, after it (29 release files) and
after `--version 1.2.3`, which left no fragment. The old after-form printed
*no matches found: seal/ledger/\*.md* and `0`, which is the defect the issue
names. **`--strict` exited 2 at every step of that run**, and the reason was
this branch's own: the #561 edit drifted three rows anchored on the
checklist's §2 and §3 (R5 in `seal/ledger.md`, D's D1 and B's P3), which
nobody had re-read yet. The scratch reading was right. Those rows were
re-read and noted at `31937b9f`, and the run again gave 1047, 1047 and 1047
with strict exit 0 at each. The scratch clone was removed afterwards (the
script checks).

**The version the measurement folded under is `1.2.3`**, the illustrative
one, and it lived only in the scratch clone.

**What `CLAUDE.md` needs: nothing from this phase.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `cat seal/ledger.md seal/ledger/*.md \| grep -c '^\|'` and its after-split twin, inline in §3 | one `find` command in a fence at §3, and the same command in step 2 before `--split` |
