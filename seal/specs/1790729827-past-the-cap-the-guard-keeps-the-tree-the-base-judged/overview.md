# 1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged — overview

## Why this work exists

Past the walk's `STATE_CAP`, a `cd` on the branch an `||` skips led the base
thread's directories, so the worktree guard was silent on a switch into a
dirty tree and the consent writer filed the creation elsewhere. The walk now
leads only where its own first directory is readable.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The fix | The spawn prompt: "The report's fix: record the walk's first collapse in a `collapsed` flag, and put the base thread first from then on." | The walk leads where its first directory is readable (`plan.md` B) | Measured against the flag on the same cases and corpus. The flag leaves `cd w; 2>/dev/null cd nosuch \|\| (cd O) && git worktree add` filed under `w/nosuch` with no cap reached, and stops a `cd` landed past its redirections from leading past the cap, which makes I13's claim false there. B closes every row the flag closes and both of those, in one condition |
| The invariant | The spawn prompt: "nothing `86256492` asks or stops may read silent after the fix" | Read as the commit gate's stops, and the guard's where bash runs the switch in the tree the base judged | One guard shape reads silent that the base asked about: the capped chain then `2>/dev/null cd O && git switch`. The base asked about the dirty `w` because it never read that `cd`; bash switches in the clean `O`. The same shape before the cap has read so since round 2 of 1790660768 (I13), reviewed and accepted. `plan.md` §*Alternatives considered* holds the reasoning |
| When `spec.md` and `plan.md` were written | `skills/implement/SKILL.md` §3: "`spec.md` and `plan.md` **before** implementing" | Both were written after the fix's first commit, `81dfcbb1`, from the spawn prompt's frame | The fix was probed and committed first to measure the report's claims. Both files record this at their head, and `spec.md`'s foot line keeps the checker's fixed wording |

## Not verified

| Item | Who must answer |
|---|---|
| The whole suite, the repository-wide lint and the typecheck on this branch | the sealer's broad gate, after the review rounds |
| Whether the three deny texts that now name a different repository first as the one with no review recorded read right to a person (M2's 3 of 128) | the review round, which reads the texts; the stop is the same in each |

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
owns whether to add it there.

## Fed back into the spec

- `docs/commit-review-gate-spec.md`, the `STATE_CAP` paragraph: the base's
  directories come first where the walk's own first directory is unresolved.
  Inferred during implementation.
- `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*:
  the tree judged where the walk cannot name the running shell. Inferred
  during implementation.
