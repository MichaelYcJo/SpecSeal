# 1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged — overview

## Why this work exists

Past the walk's `STATE_CAP`, a `cd` on the branch an `||` skips led the base
thread's directories, so the worktree guard was silent on a switch into a
dirty tree and the consent writer filed the creation elsewhere. The walk now
leads only where its own first directory is readable and a directory on disk.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The fix | The spawn prompt: "The report's fix: record the walk's first collapse in a `collapsed` flag, and put the base thread first from then on." | The walk leads where its first directory is readable (`plan.md` B) | Measured against the flag on the same cases and corpus. The flag leaves `cd w; 2>/dev/null cd nosuch \|\| (cd O) && git worktree add` filed under `w/nosuch` with no cap reached, and stops a `cd` landed past its redirections from leading past the cap, which makes I13's claim false there. B closes every row the flag closes and both of those, in one condition |
| The invariant | The spawn prompt: "nothing `86256492` asks or stops may read silent after the fix" | Read as the commit gate's stops, and the guard's where bash runs the switch in the tree the base judged | One guard shape reads silent that the base asked about: the capped chain then `2>/dev/null cd O && git switch`. The base asked about the dirty `w` because it never read that `cd`; bash switches in the clean `O`. The same shape before the cap has read so since round 2 of 1790660768 (I13), reviewed and accepted. `plan.md` §*Alternatives considered* holds the reasoning |
| When `spec.md` and `plan.md` were written | `skills/implement/SKILL.md` §3: "`spec.md` and `plan.md` **before** implementing" | Both were written after the fix's first commit, `81dfcbb1`, from the spawn prompt's frame | The fix was probed and committed first to measure the report's claims. Both files record this at their head, and `spec.md`'s foot line keeps the checker's fixed wording |
| Round 1's clause | Round 1's report, yellow 1: `lead in base_wheres or os.path.isdir(lead)` | `os.path.isdir(lead)` alone (M3) | `lead in base_wheres` lets the walk lead with a directory that does not exist wherever the base names it too, and `in` also matches an unresolved base entry of the same spelling. A mutant with only the base match survived no case, and one with the base match beside `isdir` survived every case, so nothing told the two apart; the stat costs one call per segment. `exists` in place of `isdir` was killed only after a `cd` into a file was planted |

## Not verified

| Item | Who must answer |
|---|---|
| The whole suite, the repository-wide lint and the typecheck on this branch | the sealer's broad gate, after the review rounds |
| ✅ Whether the three deny texts that now name a different repository first as the one with no review recorded read right to a person (M2's 3 of 128) | executed in round 1's fix pass: the corpus rebuilt from its seed gives 4 such texts against `542f920b` after M3, listed and judged under *What the deny names first* below; each reads right |
| The 4 guard and 4 consent answers M3 leaves, all `cd>/dev/null <missing> && 2>/dev/null cd O` and a newline | the orchestrator: a new finding in the class of round 1's yellow 1, closable only by a thread that marks a state dead through later segments, which a fix pass does not add (§*Not done*) |

## Not done

**⬜ 3 (`cd '>x' && git worktree add` filed under `$HOME`) is refused at this
layer.** The splitter hands every reader shlex's tokens, which drop the
quotes, so `cd '>x'` and `cd >x` both arrive as `['cd', '>x']`. bash goes
home for the second and into `./>x` for the first. Nothing downstream of the
splitter can tell them apart, and telling them apart means tokens that carry
quoting, a new interface for the commit gate, the guard, the consent writer
and the parity gate alike. What the wrong landing costs was executed: the
commit gate judges both `$HOME` and `<cwd>/>x`, so no commit goes unjudged.
The guard judges `$HOME`, which holds no repository, so it falls back to the
session's own tree (`docs/worktree-guard-spec.md` §*Which tree*). The consent
writer files the creation under `$HOME` (executed), not under the clone it
ran in, so the next creation there asks once, which is the side a guard should
fail on (§*Unknowns resolve conservatively*). The same holds for `cd 'a>b'`, which
lands `<cwd>/a` in front. The fix does not change any of this: the landing is
the walk's first directory, and it was first before.

**⬜ 4 (the capped deny names a directory no shell reached) is refused.** The
deny stands at `86256492`, `542f920b` and here. The directory it names is the
collapse's, taken from the walk's first state, which with a landing placed in
front is the walk's most recent landing: the last directory it could name, as
the text says. "No shell reached" is true of the fixture because the
`nosuch` directories do not exist, and the reader does not look.
`UNREADABLE_STATE` says so in the deny itself: "A path that simply does not
exist looks exactly the same from here." `86256492` does the same where it
lists what it followed: `2>/dev/null source /dev/null; ` + 16 × `cd nosuch; `
+ `git commit` denies there listing sixteen `nosuch` directories no shell
reached, executed. Any other of the 65 directories would be as arbitrary a
name, and changing it changes a message and every directory derived from the
collapse. What did change here is the order: past the cap the deny now lists
the base's directory first (M2, pinned by
`tests/test_no_shape_the_base_stops_reads_silent.py#test_past_the_cap_the_deny_names_the_directory_the_base_named_first`).

**What the fix leaves in the consent writer, for #686.** In 89 of 20,234
generated segments, 7 of them a creation, the cap still moves the consent
writer's answer from `86256492`'s. In every one of them the base thread names
no readable directory, so the writer's "first readable" reads through the
unresolved leading directories to one of the walk's. Round 3's flag leaves
the same class. Changing it is a change to how the writer reads an unresolved
first directory, which is #686's question for the guard; the orchestrator
owns whether to add it there. Round 1 deferred it to #686 as its yellow 2.

**A failed landing followed by `&&` and a landing that exists (round 1's fix
pass).** M3 leaves 4 of 3,920 commands where bash switches in the dirty `w`,
`86256492` asked, and the guard is silent, and the same 4 misfile the
creation. All are one shape, with and without the cap and behind `cd w;` or
`cd w &&`:

```
cd w; cd>/dev/null <missing> && 2>/dev/null cd <O>
git switch feature/x
```

bash's first `cd` fails, so `&&` skips the second, and the newline runs the
switch in `w`. The walk's lead is `<O>`, a directory that exists, reached only
through the failed landing. The test M3 adds reads the lead, not the route it
came by. The state's one-step `prev` is not enough either: a segment between
the two landings rewrites it. Closing it means marking a state dead from a
failed landing through every later segment, which is a thread of its own
beside `states` and `parked`, and a fix pass does not add one
(`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
it*). The orchestrator decides where it goes.

## What the deny names first

Round 1's ❓. The phase-1 corpus was rebuilt from its seed (1,216 commands,
3,648 jobs in three session kinds) and run through the commit gate's `main()`
at `542f920b` and here, after M3. No decision moved. The reason text moved in
140 jobs; 136 are the same list reordered. In the other 4, the gate's
ordinary no-review text names a different repository as "the repository this
commit lands in", because `hooks/commit-review-gate.py#main` takes the first
stopped repository, and the order put the base thread's first. All 4 are in the
session kind that is not opted in and ends `; cd u2 && git commit -m x`, and
all 4 deny at both SHAs.

| Job (its first segments; the fixture root is `T`) | `542f920b` names | here |
|---|---|---|
| `git worktree add ../wt && (cd T/O); env git commit -m x \| 2>/dev/null cd T/O && cd T/nosuch-either 2>&1 && …` | `T/O` | `T/k2/u2` |
| `git worktree add ../wt && env git commit -m x \|\| 2>/dev/null cd nosuch \|\| cd; cd '>x' …` | `T/k3/u2` | `T/k2/u2` |
| `2>/dev/null cd T/O` + newline + `cd nosuch; cd T/k3/u2 & git status; …` | `T/O` | `T/k3/u2` |
| `popd; 2>/dev/null cd T/O && X=T/O; git status \|\| cd - && 2>/dev/null cd T/O & …` | `T/O` | `T/k3/u2` |

Each reads right (read, from the commands and the fixture). Every repository
named on either side is one a segment of that command can commit into, and
the fixture records no review in any of them, so the deny's claim, "the
repository this commit lands in", is true of each. What moved is which one
the question leads with, and, read from `main`, which repository's
once-per-session budget the deny spends. Neither moves the decision. The
text was not compared with `86256492`'s for these jobs.

## Fed back into the spec

- `docs/commit-review-gate-spec.md`, the `STATE_CAP` paragraph: the base's
  directories come first where the walk's own first directory is unresolved.
  Inferred during implementation.
- `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*:
  the tree judged where the walk cannot name the running shell. Inferred
  during implementation.
- Both, in round 1's fix pass: a `cd` landed past its redirections leads only
  where its destination is a directory, and a relative `cd` after the collapse
  leaves the base's thread leading. Inferred during implementation.
