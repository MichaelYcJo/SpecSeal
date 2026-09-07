# Implementation Plan: a git call that fails reads as no remote

<!-- seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/plan.md — HOW, in phases.
This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Summary

`git()` answers `""` for a failure, and four of its five call sites read that
as a fact. One helper — `git_asked`, returning `(text, "")` or `(None, why)` —
is promoted out of `git()`, two command-specific readers sit on it, the
manifest omits what it could not read, and the import refuses an unanswerable
remote behind a flag of its own.

Approval: the repository owner answered the ticket's one open judgment and
this work item's routing in one batch before the first edit
(`routing.md`, `spec.md` §*The judgment the owner made*). The flag's name and
message were left to this session and are argued in `spec.md`.

## Technical context

All coordinates in `skills/implement/scripts/seal.py` at `86e140f`.

- `:139 git` — the unit. `:154-155` swallows `OSError`/`SubprocessError`,
  `:159-160` swallows a non-zero return code. Both return `""`.
- `:322`, `:323` — `manifest_of`'s `remote` and `head`.
- `:947`, `:953` — `import_`'s read of this clone's remote, and a second
  read of the same thing for the refusal message.
- `:949` — `if here and there and here != there and not args.allow_other_repo`.
  An empty `here` short-circuits the whole condition.
- `:1476` — `other_worktrees`, the one safe member of the class.
- `:1365 porcelain`, `:1395 indexed`, `:1745 gitlinks_under_root` — the
  precedent. Each runs `subprocess.run` itself and carries a `why`.

Constraints:

- `git config --get` exits **1** for an unset key (measured, `spec.md`
  §*The rule the new helper applies*), so "non-zero is a failure" is not the
  rule for that command alone.
- Existing hand-built fixtures write `"remote": ""` into their manifests —
  twenty-two of them in
  `tests/test_the_records_can_be_carried_out_and_in.py`. The design keeps
  `""` meaning *no remote*, so every one of them keeps passing without an
  edit. Making `""` the unreadable state instead would have touched all
  twenty-two, and each edit would have been a chance to change what a case
  was pinning.

**What breaks in six months.** The refusal is new, so the first person it
stops will be someone whose git failed transiently and who did not know the
flag existed. The message carries git's own text and names the flag, which is
the whole mitigation. The second risk is `git config --get`'s exit 1: if a
future git changes that code, an unset remote starts reading as unanswerable
and every remote-less repository is refused. That fails in the safe
direction — a refusal with a flag, not a silent merge — and the case for a
repository with no remote (S3) is what would catch it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A fourth `subprocess.run` body inside a new `remote_url`, matching `gitlinks_under_root` line for line | One idea in four places. A fix to the encoding argument or the timeout lands in three of them and the fourth is found by a reviewer, which is how `head` got the return-code check in #81 and `remote` beside it did not | rejected |
| Promote the shape into `git_asked`, make `git()` a wrapper | `git()`'s contract is unchanged, one `subprocess.run` for the general case, and the callers that need `why` ask for it. The cost is one more name in a file that already has several git helpers | **chosen** |
| Change `git()` itself to return a pair | Every one of its call sites has to change, including the two that are right to ignore the distinction, and `other_worktrees` grows a branch it does not need | rejected |
| `--default ""` so unset exits 0, removing the special case | Requires git ≥ 2.18. Nothing else this plugin runs does, so an old git would start refusing a path that works today | rejected — argued in `spec.md` |
| Warn instead of refusing | The ticket's own judgment, answered by the owner: warning is what happens today, except silently, and a warning in a command that then proceeds is read past | rejected by the owner, before the first edit |
| Route the escape through `--allow-other-repo` | Merges the two facts at the only place a user acts on the distinction | rejected by the owner |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `git_asked`, `git()` as its wrapper, `remote_url`, `head_sha`; `manifest_of` omits what it could not read | S7, S8, S9 + the existing export cases, `bin/test tests/test_the_records_can_be_carried_out_and_in.py -q` | 64aa0c6 |
| 2 | `import_` refuses an unanswerable remote; `--allow-unreadable-remote`; the message names git's cause; `:953`'s second call goes; `other_worktrees`' sentence | S1, S2, S3, S4, S5, S6, S10, S11 | 4a6e7d4 |
| 3 | Both READMEs; the changelog and ledger fragments | S12 + the record- and document-scanning modules | |

S11 moved from phase 3 to phase 2 while the work ran. It is a docstring in
`seal.py`, so committing it with the READMEs would have put part of a phase's
delivery in the previous phase's commit — the Status column's whole value is
that the commit it names contains what the row claims.

## Operational impact

**One compatibility break, and it is the point of the ticket.** `seal import`
now exits 1 where it used to exit 0, on a clone whose remote git cannot read.
The remedy is in the message: run it again, or pass
`--allow-unreadable-remote`.

**A manifest written by this build may omit `remote` or `head`.** The format
number does not move: no field was renamed or repurposed, and format 1's only
reader of those fields already goes through `manifest.get`. A zip from an
older build — which always writes both keys — imports unchanged, because
`""` still means *no remote*.

No migration, no new environment variable, no new dependency.
