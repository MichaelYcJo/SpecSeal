# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` (D1–D10, M1–M3, W1); `CLAUDE.md` §*The goal a design is chosen against*; `docs/commit-review-gate-spec.md` §*A `cd` the gate cannot read* (the #670 statement); `docs/worktree-guard-spec.md` §*Which tree*, §*Creation consent*, §*Unknowns resolve conservatively*, §*Known limits*
· evidence: `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K1–K7 added; 22 rows in `seal/releases/0.9.1.md`, `0.15.5.md`, `0.15.6.md`, `0.16.0.md` and `0.17.0.md` re-read and re-stamped, four of them corrected in place (I9, M1, M2, M3) and one corrected in its notes (M4)
· verified: executed — every new case red first, every unit broken once with `mutation-check`, phase 3's count, the timing; read — which reading each #716 shape reaches in a stubbed clone for `env -S`

## Why this work exists

Two commits the commit gate's reader did not find (#716) are found, and the
worktree guard's two silences (#686, #678's guard half) were each wired or
named as a limit by a count over the recorded runs: #678's question is wired,
#686's fallback is a known limit.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| M1's class | Spec: "every git global option that takes its value as a separate word". Code: the three git 2.54.0 accepts spaced and the reader lacked (`--config-env`, `--attr-source`, `--shallow-file`); `--super-prefix`, which older gits took spaced, is not added | the installed git's class | `questions.md` M1 names the measurement as running each option on the installed git; 2.54.0 refuses `--super-prefix` with exit 129 (`phases/phase-1.md`) |
| The guard's import of `hooks/cmdline.py` | Plan: "The guard imports `hooks/cmdline.py` under a separate name". Code: the import sits in a `try`, and a failed import leaves `wider_only_kinds` finding nothing | guarded | spec silent on a broken reader. Unguarded, a broken `hooks/cmdline.py` took the guard's ACTIVE deny down with the commit gate (`phases/phase-2.md`); `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* puts a wrong allow above a wrong deny, and losing the guard is every allow at once |
| `quiet`'s discards | Plan §*What phase 4 builds*, C step 1: "For each kind the frozen loop did NOT find". Code: `quiet` hands the kinds the loop judged to `wider_only_kinds`, which subtracts them, and a view counts as hidden only where the frozen parser reads its kind from none of the segments it was made from | the loop's verdicts | `classify` judges fewer kinds than `switch_kind` reads from the same words, so subtracting the words' kinds let a restore silence a hidden switch (round 1, yellow 3); comparing a cut view with the frozen parser silenced a glued subcommand (round 2, yellow 8) |
| `env -S`'s spellings | Spec §*Scope* 1: "every spelling of `env`'s split string". Code: `-S`, `-S<s>` and `--split-string[=<s>]` anywhere, and among env's own options a cluster ending in `S` and every prefix of `--split-string`; env's own options are read from one table, `ENV_OPTIONS`, built from GNU coreutils env's and BSD/macOS env's synopses, past a redirection anywhere among them and an abbreviated long option's value, and end at `--` | getopt's grammar, as one table | round 1, yellow 2, and round 2, yellows 9 and 10 and white 11: macOS `env` runs `-iS` and a cluster behind a redirection (executed by the rounds); GNU's getopt takes unambiguous prefixes (read, not run: GNU env is not installed on the machine this was built on) |

## Not verified

| Item | Who must answer |
|---|---|
| Which git global options take a separate value on the gits CI's Linux and Windows legs install (M1 ran on 2.54.0 only) | CI's legs, when the pull request runs |
| Whether this plugin's git hook stub sees a session for `env -S '-i git commit'` where a lease stands (`spec.md`'s table calls that half unverified and not needed by this build; the PreToolUse reading judges the shape either way) | the reviewer, if they want the stub's half; nothing here depends on it |

## Not done

**The guard does not read a string a shell is handed** — `sh -c 'git switch
x'`, `env -S 'git switch x'`, `bash -c 'git worktree add ../wt b'`. Neither
candidate reaches it: the frozen reading never read strings, and
`wider_only_kinds` reads the commit gate's views of the command line, which do
not include `reparsed_texts`. It is #670's class for the guard, wider than
either issue names, and it has no count behind it. `spec.md` §*Scope* left
it out, and the session that spawned this build decides where it is filed.

**The creation arm's unresolved directory** (an unresolved `cd` before `git
worktree add`) was left out by the frame (`questions.md` D2): without consent
every Bash creation already stops, and with it the owner's `automation`
press is the answer.

**`--exec-path` stays in `_git_options`'s set** although it takes no separate
value: the word it makes the reader skip is never run, because git prints its
path and exits.

## Fed back into the spec

none
