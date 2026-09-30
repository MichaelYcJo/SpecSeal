# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — round 3 report

| Field | Value |
|---|---|
| Round | 3, verifying and last (the run's one reopening is spent, so the run is capped) |
| Target SHA | `e2321cc5` |
| Ranges verified | round 2's fixes `6a5afede..c18d8a56`; the Q7 fix `1f55007a..e2321cc5` |
| Base compared against | `86256492`, and `1f55007a` (the hooks before the Q7 fix) |
| Ran by | specseal:warden on claude-opus-5-5 |

Every executed row below ran in a `git clone --no-local` at `e2321cc5` and in
exported trees of `86256492`, `1f55007a`, `c18d8a56` and `e2321cc5`. Each tree
paired its own `hooks/` with the target's `tests/`. A further copy of the
target carried the fix proposed here. The fix pass's account (the prompt, the
ledger rows I13–I15, `questions.md` Q7) was read as claims, and each claim was
checked against the code or by execution.

## What this round found, in the order one causes the next

**The commit gate's invariant holds at the target.** The per-segment walk
comparison and a corpus through `main()` in three session kinds both show it.
The corpus loses none of the base's stops and adds 14, all of them `cd`s
landed past a redirection. The I15 exception (a segment only the second
reading unplaces) is truly no loss. The base's `parse_git` reads `git` only
where the as-written reading's first word is `git`, and that is exactly when
`placed` is true.

**The guard and the consent writer do not always get the base's tree.**

- **Cause.** The Q7 fix orders each segment's directories by one test: the
  walk's lead when the walk names any readable one, and the base thread's lead
  otherwise. Its comment equates "names none" with the collapse past
  `STATE_CAP`. But a walk that has collapsed can name a readable directory
  again. `cd /abs/Y || git switch` gives the collapsed walk `Y` on the skipped
  branch, the one tree the switch does not run in.
- **Effect on the guard.** For `cd w; <nine 2>/dev/null cd nosuch;> cd <missing>
  || git switch feature/x` from a clean session tree with a dirty nested `w`,
  bash switches in `w`. `86256492` asks and names the dirty file. The target
  is silent. The walk's unresolved directory leads, and the guard reads it as
  the session's own clean tree.
- **Effect on the consent writer.** For the same chain with `git worktree add`,
  it files the creation under the missing directory. The clone the creation
  ran in gets no record.
- **The Q7 fix did not cause it.** `1f55007a` fails the same shapes. The fix's
  own sentence, *the worktree guard, which judges the first, judges the tree
  the base did*, holds only for a collapsed walk that names nothing afterwards.
- That is yellow 1. A flag that records the walk's first collapse, and puts
  the base thread first from then on, closes it. Executed with that flag: the
  shapes ask again, the order comparison differs from the base in 0 segments
  where the cap is the cause, and the consumer modules pass.

**Two paperwork and wording items, none a loss.**

- I15's exception list is incomplete (white 2). The zsh short loop `for i (1 2)
  git commit` is unplaced by the target's first reading and was not unplaced
  by the base's. The base read no commit there.
- A quoted `cd` operand shaped like a redirection now lands at `$HOME` in front
  (white 3). The tokens cannot tell `cd '>x'` from `cd >x`.
- The deny for a collapsed chain names a directory the shell never reached
  (white 4). It is a stop at both SHAs.

## Findings from execution

### Yellow 1 — past the walk's cap, a readable directory on a skipped branch leads the base's

`hooks/cmdline.py#walk_directories`, the ordering added by `879df3b4`:

```python
        if any(not isinstance(w, Unresolved) for w in wheres):
            ordered = wheres + base_wheres
        else:
            ordered = base_wheres + wheres
```

After the walk's thread collapses, `states` is one unresolved directory and
`parked` is empty. A later `cd /abs/Y` lands the walk in `Y` and parks the
unresolved one. Behind `||` the walk's `running` is that unresolved directory
and its `skipped` is `Y`, so `wheres` is `(unresolved, Y)`. It holds a
readable directory, so it goes in front of the base's `(w, S, Y)`.

- The guard (`hooks/worktree-guard.py` `main`, through `judgeable`) takes the
  first directory that classifies, and it reads an unresolved one as the
  session's own. It judges `S` where `86256492` judged `w`.
- The consent writer (`hooks/worktree_consent.py#creation_directory`) takes
  the first readable one, `Y`, where `86256492` took `w`.
- The commit gate judges every directory, so its verdict is unchanged.

Executed through the guard's `main()` and `creation_directory`. The session
is a clean `git init`, `w` is a copy of the `repo` fixture with `f.txt`
changed, `<missing>` is never created and `O` is a fresh repository. bash ran
each chain with `pwd` in place of the switch.

| Shape | bash runs the switch in | `86256492` | `1f55007a` | `e2321cc5` | with the fix |
|---|---|---|---|---|---|
| `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `cd <missing> \|\| git switch feature/x` | `w` | ask, names `f.txt` | silent | silent | ask, names `f.txt` |
| the same with `cd w && ` in front | `w` | ask | silent | silent | ask |
| the same with 8 in the chain | `w` | ask | silent | silent | ask |
| control: `cd w; ` + 9 in the chain + `git switch feature/x` | `w` | ask | silent | ask | ask |
| consent: `cd w; ` + 9 in the chain + `cd <missing> \|\| git worktree add ../wt` | creation in `w` | filed under `session/w` | under `<missing>` | under `<missing>` | under `session/w` |
| consent: the same with `cd O \|\|` | no creation (`cd O` succeeds) | `session/w` | `O` | `O` | `session/w` |

The control row is the fix's own case (`tests/test_guard_resolves_the_tree_it_judges.py#test_a_chain_past_the_walks_cap_keeps_the_tree_the_base_judged`).
It joins the last `cd` with `&&`, so the walk after the collapse names no
readable directory. One operator away, the case the fix was written for is
open again.

Across the generated walk comparison below, the cap alone changes the
consent writer's first readable directory from the base's in 126 segments,
and the guard's first directory in 52 segments. 12 of those are a `git switch`
or `git worktree add` segment. With the fix both counts are 0.

Why it matters: the guard is silent on a switch into a dirty tree that
`86256492` asked about. The consent writer files a record in a clone nobody
consented for, and leaves the clone the creation ran in with none. Round 2
counted that same consent effect as *Loses a record*.

### The commit gate keeps every base directory

A generated corpus of 4,036 commands and 68,578 segments was built from 41
segment shapes and 6 operators, at lengths 1 to 40, with the cap-then-`||`
shapes added by hand. Each segment's directories at the target were compared
with `86256492`'s walk.

- A base directory is missing at the target in 1,225 segments.
- 608 are I15's stated exception, all `2>/dev/null nice -n 5 git commit -m x`.
- 617 are the zsh short loop `for i (1 2) git commit -m x`, which I15 does not
  name (white 2).
- At `c18d8a56`'s hooks, before the Q7 fix, 17,452 segments miss one.

The claim of "0 segments" over 16,128 commands does not reproduce, because
this corpus holds a shape that one did not.

For neither exception can the missing directory cost a stop:

- **The base finds no commit there.** Its `parse_git` returns None when the
  as-written first word is not `git`: `2>/dev/null` and `for`.
- **The other finders take no directory.** The `eval` and `string` kinds build
  their base with `_unresolved_base`, the same unresolved directory
  `_unplaced` makes.
- **The walk moves on intact.** The base thread's `states` are computed apart
  from `base_wheres`, so no later segment is affected.
- **The thread is the base's walk.** `understood(tokens, redirections=False)`
  is `86256492`'s body, so `as_written` equals the base's `known`, and the
  environment the thread reads is the base's. `_cd_target`, `_land`,
  `_expanded`, `_bind`, `_forget`, `_unseen`, `_nesting` and the splitter are
  unchanged since `86256492`, by an AST comparison of every top-level unit.

Through `main()`, a corpus of 1,013 commands (seeded, from 27 segment shapes
with real directories) ran in three session kinds:

- `[no-review]` over a parity arm;
- a directory that is not opted in, reaching an opted-in `u2`;
- an opted-in, undeclared session.

The base stopped 572, the target lost 0 of them and added 14. All 14 are in
the not-opted-in kind and hold a `cd u2` behind a redirection.

### White 3 — a quoted operand shaped like a redirection lands at `$HOME`

`cd '>x' && git worktree add ../wt` is filed under `$HOME`. `86256492` filed
it under `<cwd>/>x`, where bash's `cd` goes. shlex drops the quotes, so the tokens are `['cd', '>x']`, the same as
`cd >x`, where bash does go home. So the landing is right for one spelling and
wrong for the other. The commit gate judges both directories. No fix is owed
at this layer, because nothing downstream of the splitter can tell the two
spellings apart.

### White 4 — the deny for a collapsed chain names a directory the shell never reached

In an opted-in, undeclared repository, `2>/dev/null cd nosuch; ` × 9 +
`git commit -m x` denies at both SHAs.

- `86256492` gives the ordinary no-review reason for the session repository.
- The target gives the construct reason. It names `<session>/nosuch/…` nine
  levels deep as *the last directory it could name*, and then says one further
  repository stopped for the ordinary reason.

Every `cd nosuch` fails in bash. The named directory is therefore a landing no
shell reached, and it comes from the collapse taking its name from the first
state. It stops at both SHAs.

## Round 2's four verdicts

- **Yellow 1 is closed.** The landing past a `cd`'s redirections is added in
  front of the as-written answer. In the corpus above it is where the 14 added
  stops come from. Round 2's guard and consent case passes. White 3 above is
  the one spelling where the landing leads wrongly.
- **Yellow 2 is closed.** The rule now sits in the base thread. The 608 excused
  segments are exactly the shape it names, and none costs a stop.
- **White 3 is closed.** `commit_invocations` reads `"git>x" commit -m x` and
  `git">"/dev/null commit -m x` as one invocation each at the target and as
  none at `86256492`, as the corrected `seal/ledger.md` row says.
- **White 4 is closed.** The split-twice cost is recorded at
  `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/overview.md:53`.

## The Q7 fix's claims, opened

| Claim | What this round found |
|---|---|
| 7 cases red at `1f55007a`, green at base and fix | Executed: 7 failed at `1f55007a`'s hooks, and they passed at `86256492`'s and `e2321cc5`'s (8 selected by `-k cap`) |
| 11 mutants killed | Two spot-checked, both killed. Without the reordering, the guard's cap case fails. Without the base's directories, 8 cases fail |
| 0 segments missing a base directory over 16,128 commands | Not reproduced on this corpus: 617 zsh short-loop segments outside the stated exception, none a loss (white 2) |
| W1 corpus 8,064: 0 lost, 74 added | Not re-run. This round's own corpus of 1,013 through `main()` lost 0 and added 14 |
| `cd x;` × 5,000 at 4.02 s against 1.89 s | Executed through `commit_invocations`, with other probes running beside it: 5.44 s against 2.68 s. The worst chain measured is `cd x ; git commit -m x ;` × 5,000 at 9.19 s against 5.16 s at the base. All are far inside 600 s, and the proposed fix costs nothing measurable |

## The class (§12)

**Every bound or collapse in the readers.** The diff `1f55007a..e2321cc5`
touches `walk_directories` and three new helpers (`_branches`, `_unplaced`,
`_capped`) and nothing else in `hooks/`. So the other bounds (`NESTING_READ`,
`HEADERS_READ`, the depth bound) are unchanged in both ranges, and this round
did not re-run them. The one collapse the Q7 fix touches is `STATE_CAP`. It
now runs once per thread, and its consumers are below.

**Every reader that consumes `walk_directories`.** Found by grep over `hooks/`:

- the commit gate's `commit_invocations`, which judges every directory, so
  order does not matter to its verdict;
- the worktree guard's `main`, which takes the first directory that
  classifies (yellow 1);
- the guard's creation allow-list check, which ignores the directories;
- the consent writer's `creation_directory`, which takes the first readable
  directory (yellow 1).

No other hook reads the walk. The notice the prompt names is taken here to be
the gate's reason text. White 4 is its one change.

## Regression tests to plant

Destination: `tests/test_guard_resolves_the_tree_it_judges.py`, beside the
fix's cap case. The block under `## Paste-ready fixes` is verbatim, except
that it takes `run` and `wg` from this module. Seen red (executed): the probe
copy fails at `e2321cc5`'s and `1f55007a`'s hooks with `('silent', '')`, and
passes at `86256492`'s and with the fix.

## Facts for the evidence ledger

- I15, correcting its exception list. The walk names every directory the
  base's walk named for a segment, except in two segment shapes where the base
  read no commit. One is where only the reading past redirections unplaces it
  and the as-written reading found no `git` (`2>/dev/null nice -n 5 git
  commit`). The other is the zsh short loop, which the target's first reading
  unplaces (`for i (1 2) git commit`). Executed 2026-09-30: over 68,578
  generated segments, those two shapes are all 1,225 misses, and 1,013 commands
  through `main()` in three session kinds lose 0 of the base's 572 stops.
- With yellow 1's fix: from the walk's first collapse on, the base's thread
  leads each segment's directories. Executed: the guard and the consent writer
  answer as `86256492` on the six rows above, and on every one of the
  126 + 52 cap-caused segments.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | past `STATE_CAP`, a readable directory the collapsed walk regains on a skipped branch leads the base's, so the worktree guard judges the session's own tree and the consent writer files the creation under the `cd` target the `\|\|` skipped | `hooks/cmdline.py#walk_directories` | deferred #689 | Executed: `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `cd <missing> \|\| git switch feature/x` asks at `86256492` and is silent at `e2321cc5` while bash switches in the dirty `w`; its creation twin is filed under `<missing>`. Present at `1f55007a` too. The Q7 fix's ordering test equates "names no readable directory" with the collapse. Fixed by a first-collapse flag, executed green |
| ⬜ 2 | I15's exception list omits the zsh short loop, which the target's first reading unplaces and `86256492`'s did not | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` (I15) | deferred #689 | A correction to the run's paperwork. Executed: 617 segments outside the stated exception, none costs a stop, because the base's `parse_git` reads the first word `for` |
| ⬜ 3 | a quoted `cd` operand shaped like a redirection (`cd '>x'`) is landed at `$HOME` in front, so the guard and the consent writer take `$HOME` | `hooks/cmdline.py#walk_directories` | deferred #689 | Executed: filed under `$HOME` at the target, under `<cwd>/>x` at `86256492`. The tokens equal `cd >x`'s, where `$HOME` is right, so no fix is owed at this layer |
| ⬜ 4 | the deny for a chain past the cap names a directory no shell reached as the last one it could name | `hooks/cmdline.py#_capped` | deferred #689 | Executed: deny at both SHAs. The collapse names its first state, a landing every `cd nosuch` failed to reach |
| 🟢 | round 2's yellow 1 is closed — a `cd` with a redirection among its words lands, in front of the as-written answer | `hooks/cmdline.py#walk_directories` | confirmed | Executed: 14 added stops in the corpus, all such landings; 0 lost; round 2's guard and consent case passes |
| 🟢 | round 2's yellow 2 is closed — the second reading's unplace no longer replaces a directory the base judged | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the 608 excused segments are its shape alone, and the base finds no commit in any |
| 🟢 | round 2's white 3 is closed — the `seal/ledger.md` quoted-`>` row is corrected | `seal/ledger.md` | confirmed | Executed: 1 invocation each at the target, 0 at `86256492` |
| 🟢 | round 2's white 4 is closed — the split-twice cost is recorded | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/overview.md:53` | confirmed | Read |
| 🟢 | the Q7 fix keeps every directory the base judged for the commit gate | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the comparison and the `main()` corpus above; the seven Q7 cases red at `1f55007a` and green at the base and the target |

## Executed probes

| What was run | Result |
|---|---|
| The 7 Q7 cases (`-k cap` over the two changed modules) against the hooks of `86256492`, `1f55007a` and `e2321cc5` | 8 passed, 7 failed and 1 passed, 8 passed |
| Per-segment walk comparison, 4,036 generated commands and 68,578 segments, `86256492` against `e2321cc5`, `c18d8a56` and an uncapped `e2321cc5` | Target: 1,225 segments miss a base directory, 608 the I14/I15 shape and 617 the zsh short loop. `c18d8a56`: 17,452. Cap-caused order changes at the target: 126 for consent, 52 for the guard. With the fix: 0 and 0 |
| The guard's `main()` and `creation_directory` on the six shapes of yellow 1, at four hook trees and with the fix, and bash on each chain | The table under yellow 1 |
| The planted case for yellow 1, at four hook trees and with the fix | Red at `1f55007a` and `e2321cc5` (`('silent', '')`), green at `86256492` and with the fix |
| 1,013 commands through the commit gate's `main()` in three session kinds, at `86256492` and `e2321cc5` | 572 base stops, 0 lost, 14 added |
| The gate's reason text on four shapes, at `86256492` and `e2321cc5` | Deny on all four at both. The wording changes on three (white 4) |
| `creation_directory` on `cd '>x'`, `cd "2>x"`, `cd 'a>b'` at both SHAs | Target: `$HOME`, `$HOME`, `<cwd>/a`. Base: the quoted names |
| `commit_invocations` on round 2's white 3 shapes at both SHAs | 1 and 1 at the target, 0 and 0 at the base |
| Two mutants of the target (no reordering; the base's directories never added), over the two changed modules | 1 failed and 8 failed |
| Seven modules that consume the walk, at the target and with the fix | 897 passed and 1 failed at each. The failure is the release-comparison case, which needs a tag, and the exported tree has none. That case passed in the tagged clone at the target |
| 5,000-segment chains through `commit_invocations` at `86256492`, `e2321cc5` and with the fix | `cd x;` 2.68 / 5.44 / 4.64 s; `cd x 2>/dev/null;` 2.70 / 7.02 / 6.03 s; `2>/dev/null cd x;` 0.31 / 4.31 / 3.88 s; `cd a \|\| cd b \|\|` 0.47 / 0.66 / 0.56 s; `2>/dev/null cd x \|\|` 0.27 / 0.36 / 0.35 s; `cd x ; git commit -m x ;` 5.16 / 9.19 / 9.35 s; `2>/dev/null cd x; git commit -m x;` 0.58 / 5.74 / 6.23 s |
| The four hooks the walk feeds, parsed at the target under `/usr/bin/python3` 3.9.6 with feature version 3.9 | They parse |
| `ruff check` and `ruff format --check` on the Q7 fix's files | Not run: the runner's virtualenv carries no ruff. It is the sealer's, with the rest of the broad gate |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It belongs to the sealer, once the rounds settle, and it is not due while yellow 1 is open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The guard reads an unresolved directory as the session's own and judges only a segment's first directory. Yellow 1's silence goes through that fallback too, but it is not the finding here: `86256492` gave the guard a readable first directory in those shapes, and the target does not. Already deferred in round 2 | #686, in no milestone | the owner, who decides whether the guard asks on an unresolved directory |

## Paste-ready fixes

### Yellow 1 — `hooks/cmdline.py#walk_directories`

Beside `base_states`:

```python
    base_states, base_parked = [(cwd, None)], []
    # Whether the walk's own thread has collapsed. Until it has, its
    # directories hold every one the base's thread holds, and the ones in
    # front of them are where the shell went. After it has, a readable
    # directory it regains is not that: `cd /abs/Y || git switch` past the
    # cap names Y, the one tree the switch does not run in. So from the first
    # collapse on, the base's thread leads (round 3 of 1790660768).
    collapsed = False
```

The ordering:

```python
        # The base's directories go behind the walk's, since the worktree
        # guard and the consent writer take the first one -- and in front of
        # a walk that names none, or that has collapsed past `STATE_CAP` at
        # any segment so far. Behind it the guard would read the session's
        # own tree, or a branch the `||` skipped, where `86256492` judged the
        # base's first directory.
        if not collapsed and any(not isinstance(w, Unresolved) for w in wheres):
            ordered = wheres + base_wheres
        else:
            ordered = base_wheres + wheres
```

The walk's collapse:

```python
        carried = _dedup(carried)
        collapsed = collapsed or len(carried) + len(parked) > STATE_CAP
        states, parked = _capped(carried, parked)
```

`docs/commit-review-gate-spec.md`, the Q7 paragraph (§14):

```markdown
thread's. Where the walk names none, and on every segment after the walk
first collapses, the base's come first, and the worktree guard, which judges
the first, judges the tree the base did (question Q7 of work item
1790660768, and round 3's yellow 1: a collapsed walk regains a readable
directory on the branch a `||` skips).
```

`tests/test_guard_resolves_the_tree_it_judges.py`:

```python
def test_a_skipped_cd_past_the_walks_cap_keeps_the_tree_the_base_judged(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 3 of 1790660768, yellow 1. Past `STATE_CAP` the walk's thread
    collapses, and `cd <missing> ||` then gives it a readable directory on the
    branch the `||` skips. That directory put the walk in front of the base's
    thread, so the guard read the collapsed walk's unresolved directory as the
    session's clean tree, and the consent writer took the skipped branch.
    bash fails every `cd` after `cd w`, so the switch runs in the dirty `w`,
    which is the tree `86256492` judged."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    missing = tmp_path / "nosuch-either"
    chain = "cd w; " + "2>/dev/null cd nosuch; " * 9 + f"cd {missing} || "
    decision, reason, _ = run(
        monkeypatch, capsys, chain + "git switch feature/x", session
    )
    assert decision == "ask", (decision, reason)
    assert "f.txt" in reason, reason
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted
```

### White 2 — the ledger fragment's I15 row

```markdown
… except where only the reading past redirections unplaces it and the
as-written reading found no `git` (`2>/dev/null nice -n 5 git commit`, I14),
and in zsh's short loop, which the as-written reading unplaces since round 1
of 1790660768 and `86256492`'s did not (`for i (1 2) git commit`): in both
the base read no commit
```

Needs a fix: yes — 🟡 1 (past the walk's cap, a readable directory on a skipped branch leads the base's, so the worktree guard is silent on a switch into the dirty tree `86256492` asked about, and the consent writer files the creation under the skipped `cd` target)
Loses a record or crashes: yes — 🟡 1: `creation_directory` files a creation behind nine failing `cd`s, a `cd` to a missing directory and an or-operator under that missing directory, so `w`, where the creation ran, gets no record. The same effect counted as yes in round 2, and it is present at `1f55007a` as well

## Proof block

Files opened this round, all read at `e2321cc5` unless another SHA is named:

- `hooks/cmdline.py` — `walk_directories` and `_branches`, `_unplaced`,
  `_capped`, `command_word`, `understood`, `parse_git`, `unglued`,
  `_without_redirections`, `_past_leading_redirections`,
  `_unreadable_past_leading_redirections`, `_is_the_program`,
  `redirection_width`, `_cd_target`, `split_segments_with_separators`,
  `Unresolved`, `_dedup`, `_directories`, `RUNNERS`; and at `86256492`
  `walk_directories`, `command_word`, `understood`, `parse_git`,
  `UNPLACED`, `LIST_OPENERS`, `RUNNERS`
- `hooks/commit-review-gate.py` — `commit_invocations`,
  `_segment_invocations`, `commit_targets`'s docstring
- `hooks/worktree-guard.py` — `walk_command`, `judgeable`, the creation
  allow-list loop, `main`'s switch and creation loop
- `hooks/worktree_consent.py` — `creation_directory`
- `tests/test_no_shape_the_base_stops_reads_silent.py` — its harness,
  `CAP_CHAINS` and the Q7 cases
- `tests/test_guard_resolves_the_tree_it_judges.py` — `run`, the round 2
  landing case and the Q7 cap case
- `tests/conftest.py` — its isolation and the `repo` fixture;
  `tests/test_the_guard_asks_once_per_session.py` — the transcript helpers
- `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/rounds/round-2.md`,
  `rounds/round-2-report.md` (its layout), `questions.md` (Q7), and
  `overview.md` and `changelog.md` through the Q7 diff
- `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md`
  (I13–I15), `seal/ledger.md` (round 2's corrected row), and
  `docs/commit-review-gate-spec.md` and `docs/worktree-guard-spec.md` through
  the two diffs
