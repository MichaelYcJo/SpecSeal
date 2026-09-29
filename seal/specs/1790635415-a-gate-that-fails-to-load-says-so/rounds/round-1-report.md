# Round 1 report — a gate that fails to load says so

Target: branch `fix/28-a-gate-that-fails-to-load-says-so` at `d8e14048`, base
`release/v0.16.0` at `551c7967`, the whole branch (`git diff 551c7967...d8e14048`).
Reviewed in a `git clone --no-local` of the worktree at the target SHA. No
earlier rounds exist, so nothing was carried except what the ledger rows
point at.

## How the findings relate

The mechanism holds. A failing gate is recorded, the group's stdout is
unchanged, and the `stop` group says it once. Two things around it are wrong,
and both are about what a person is told:

1. The line the report prints names one group per gate. A gate registered in
   two groups that fails to load fails in both, but only the first is named.
   For `worktree-guard.py` that hides the Agent-spawn path, which is the
   scenario the removed rider and the changelog both cite.
2. The words this work makes false were corrected in three files and missed
   in a fourth, `hooks/ledger-migrate.py`, which still says a raising hook is
   skipped silently.

The third item is a comment that understates what a gate that stays broken
costs per call.

## Spec compliance

Every claim in `overview.md` and the phase records was checked against the
code, not adopted.

- **Claimed: a healthy group prints what it printed before.** Executed. All
  eight groups, run through the base `dispatch.py` and the branch's in two
  identical opted-in repositories, gave byte-identical stdout and exit 0
  (probe P1). `hooks/dispatch.py#main` calls `report` only when `FAILED` is
  non-empty or the group is `stop`, and `report` returns `merged` unchanged
  when nothing is pending.
- **Claimed: the isolation property stands, and both existing cases pass
  unedited.** Executed and read. The diffstat does not touch
  `tests/test_dispatch.py` or `tests/test_the_implementer_is_recorded.py`,
  and both modules pass.
- **Claimed: S1 and S7 were seen red against the old dispatcher.** Executed.
  With `hooks/dispatch.py` checked out at `551c7967` in the clone, both cases
  fail (2 failed); the file was restored and `git status` was clean after.
- **Claimed: a broken git dir or an unwritable one is today's silence.**
  Executed. A `.git` file pointing at a missing directory, and a `.git`
  directory with mode 555, each gave exit 0, the same stdout as the gate
  absent, no record and a silent `stop` (probe P2).
- **Claimed: the silent `stop` costs little and starts no process in a main
  checkout.** Executed. Median 21.0 ms at base and 22.0 ms at the branch over
  25 runs each (probe P4), in line with the ledger's G4.
- **Claimed: the report path runs under 3.9.** Executed. `/usr/bin/python3`
  3.9.6 recorded and said a broken commit gate with empty stderr (probe P5).
- **Claimed: a broken `optin.py` is said rather than read as not opted in.**
  Executed. In a repository that never opted in, the four expected gates were
  recorded and said (probe P6). This matches `spec.md` §*Scope* item 2 and
  the policy paragraph.
- **The `FAILED` global instead of a return value** (`overview.md`'s first
  divergence). Read. `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`
  line 375 does replace `run_gate` with a string-returning lambda, so the
  grounds stand. In-process tests load a fresh module each time, so the list
  does not leak between cases.
- **No gate calls `sys.exit` at module level.** Read, by grep over `hooks/`,
  so catching a load-time `SystemExit` reclassifies no gate that exits there
  on purpose.

## Findings

### 🟡 1 — The report names only the first group a gate failed in, so a broken worktree guard reads as a Bash-only problem

`hooks/dispatch.py#describe`, and the per-gate key in `hooks/dispatch.py#record`.

A record is keyed by session and gate, and `record` skips a gate that
already has a `.pending` or `.reported` file. So a gate that sits in two
groups is written down by whichever group fails first, and `describe` names
that group alone. Three gates sit in two groups: `worktree-guard.py`
(`pre-bash`, `pre-agent`), `session-lease.py` (`post-bash`, `post-edit`) and
`worktree_consent.py` (`post-bash`, `post-agent`).

A load failure is a property of the file, so it fails in every group that
loads it. Probe P3 broke `cmdline.py`, ran `pre-bash`, then `pre-agent` with
`isolation: "worktree"`, then `stop`. The `pre-agent` call printed nothing,
so the spawn went unguarded, and the report said:

```
worktree-guard.py failed to load in pre-bash (SyntaxError: invalid syntax (cmdline.py, line 1)); calls went ahead without it, and the other gates in pre-bash still decided.
```

Why it matters: this is the exact scenario the removed rider in `run_gate`
named ("the Agent `isolation: "worktree"` path goes undefended with nobody
told"), and the changelog fragment opens by citing it. After this branch the
person is told, but told that Bash calls went ahead. Nothing in the line says
Agent spawns were unguarded too.

The fix names every group that loads the file when the phase is `load`. A
`run` failure depends on the payload, so it keeps the one group it was seen
in. Every existing case keeps its expected text, because none of them plants
a load failure of a two-group gate and then asserts the group.

### 🟡 2 — `hooks/ledger-migrate.py` still says a raising hook is skipped silently

`hooks/ledger-migrate.py` module docstring, line 51–53: "Under
`dispatch.py`'s crash isolation a raising hook is skipped silently; here that
loses one migration attempt, and the OLD-FORMAT failure still speaks."

After this branch that is false in an opted-in repository. `ledger-migrate.py`
runs in `session-start`, and a raise there is recorded and said at the end of
the first turn. The branch corrected the same sentence in
`hooks/evidence-advisor.py` ("skipped silently" became "skipped and the skip
is said once per session at the end of the turn") and in
`hooks/implementer.py`, and `spec.md` §*Scope* item 6 commits the work item
to correcting the words it makes false. `survivors.md` lists one survivor
only, because `survivor-check` matched the phrasing it was given, and this
sentence is phrased differently. Contract §12 asks for the class, and this is
its missed instance.

One neighbour was read and judged: `hooks/routing.py` line 395–398 says a
raise "is rendered as an allow by `hooks/dispatch.py`, so propagating this
would turn a nameable state into a silent one". The first half is still true
for the call. The second half is now only true for the call, since the raise
would be said at turn end. It is included in the fix below as an optional
second edit, and the fixer decides it. `hooks/commit-review-gate.py` line 831
and `hooks/routing.py` line 263–269 are past tense and still accurate.

### ⬜ 3 — The cost comment in `record` understates what a gate that stays broken costs

`hooks/dispatch.py#record`, the comment "a gate that stays broken costs one
`stat` pair per call after its first".

That holds in a main checkout of an opted-in repository. Two other places
cost more:

- In a linked worktree, `common_dir` runs `git rev-parse` on every call that
  has a failure, before the `stat` pair. That is one extra process per tool
  call for the rest of the session (read).
- In a repository that is not opted in, no record is ever written, so every
  call is a fresh gate and loads `optin.py` again. Probe P7 counted six
  executions of `optin.py`'s module body over three `pre-bash` calls, one
  from the gates and one from the report each time (executed).

Both are small, and both happen only while a gate is broken, so the behaviour
is acceptable. The comment is what is wrong, and the next reader will trust
it when measuring.

## Regression tests to plant

- **`tests/test_a_gate_that_fails_says_so.py`** — the case in 🟡 1's fence:
  a broken `cmdline.py`, one `pre-bash` call, and the worktree guard's line
  must name `pre-bash and pre-agent`. It must be seen red against
  `d8e14048` first (contract §15). Against that SHA the line reads `in
  pre-bash (`, so the assertion fails.

## Facts for the evidence ledger

- `hooks/dispatch.py#describe` names every group that loads a gate's file
  when the failure was at load, and the recorded group alone when it was at
  run. This belongs as a new row in this work item's fragment once 🟡 1 is
  fixed, anchored at `describe` and the new case. G2's `describe` hash
  drifts with the fix and is re-read in place.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A gate registered in two groups that fails to load is named in only the first group, so a broken worktree guard is reported as a `pre-bash` failure while `pre-agent` spawns also went unguarded | `hooks/dispatch.py#describe`, `hooks/dispatch.py#record` | open | Probe P3, executed: `pre-agent` printed nothing and the report named `pre-bash` alone. The rider this branch removed and the changelog fragment both cite the `pre-agent` path |
| 🟡 2 | The words this work makes false survive in `hooks/ledger-migrate.py`: "a raising hook is skipped silently" | `hooks/ledger-migrate.py` module docstring, lines 51–53 | open | Read. The same sentence was corrected in `hooks/evidence-advisor.py`; `spec.md` §*Scope* item 6 commits to the correction; contract §12 |
| ⬜ 3 | The comment in `record` says a gate that stays broken costs one `stat` pair per call; a linked worktree adds a `git rev-parse` and a repository not opted in reloads `optin.py` every call | `hooks/dispatch.py#record` | open | Probe P7, executed: six `optin.py` loads over three calls. The linked-worktree half is read |
| 🟢 | A group whose gates all ran prints what it printed before, in all eight groups | `hooks/dispatch.py#main`, `hooks/dispatch.py#report` | confirmed | Probe P1, executed: base and branch dispatchers byte-identical, exit 0, no failure directory created |
| 🟢 | The isolation property holds and the two existing cases pass unedited | `tests/test_dispatch.py`, `tests/test_the_implementer_is_recorded.py` | confirmed | Executed in the narrow run; the diffstat does not touch either file |
| 🟢 | A dangling or unwritable git dir leaves today's silence, with exit 0 and nothing raised | `hooks/dispatch.py#record`, `hooks/dispatch.py#draw` | confirmed | Probe P2, executed |
| 🟢 | S1 and S7 are red against the base dispatcher | `tests/test_a_gate_that_fails_says_so.py` | confirmed | Executed: 2 failed with `hooks/dispatch.py` at `551c7967` |
| ❓ | How the report renders beside the stamp on screen (`questions.md` Q1) | `hooks/dispatch.py#report` | ❓ out of verified scope | The spawn prompt assigns it to the orchestrator, the only session that hosts `Stop`; the orchestrator answers it |
| ❓ | The Windows render of a `Stop` `systemMessage`, and this module's cases on Windows | `tests/test_a_gate_that_fails_says_so.py` | ❓ out of verified scope | Nothing here runs Windows. CI's `windows-latest` leg answers the cases; the owner answers the render, as `overview.md` §*Not verified* says |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_gate_that_fails_says_so.py`, `tests/test_dispatch.py`, `tests/test_the_implementer_is_recorded.py`, `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_console_is_not_utf8.py` at `d8e14048` | exit 0, 125 passed |
| The S1 and S7 cases with `hooks/dispatch.py` checked out at `551c7967`, then restored | exit 1, 2 failed; `git status` clean after the restore |
| P1: all eight groups, base dispatcher against the branch's, in two identical opted-in repositories | byte-identical stdout, exit 0 in every group, no failure directory |
| P2: a `.git` file pointing at a missing directory, and a `.git` directory with mode 555, each with a broken commit gate | exit 0, stdout equal to the gate absent, nothing recorded, silent `stop`, empty stderr |
| P3: `cmdline.py` broken, then `pre-bash`, `pre-agent` with `isolation: "worktree"`, and `stop` | `pre-agent` printed nothing; the report named `worktree-guard.py` in `pre-bash` only (🟡 1) |
| P4: silent `stop`, main checkout, 25 runs each | median 21.0 ms at base, 22.0 ms at the branch |
| P5: a broken commit gate under `/usr/bin/python3` 3.9.6 | recorded and said, exit 0, empty stderr |
| P6: `optin.py` broken in a repository that never opted in | four gates recorded and said, as `spec.md` S6b specifies |
| P7: a broken commit gate in a repository not opted in, three `pre-bash` calls, counting `optin.py` module-body executions | 6 (⬜ 3) |
| `bin/evidence-check --ledger <file> .` on this work item's fragment, `seal/releases/0.4.0.md` and `seal/releases/0.15.7.md` | exit 0 for each |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once, after the rounds settle, and it has not come due while 🟡 1 and 🟡 2 are open |

The probes P1 to P7 ran from one probe script in the round's scratch
directory, run once and deleted with the clone.

## Paste-ready fixes

### 🟡 1

In `hooks/dispatch.py`, replace `describe`:

```python
def describe(gate, body):
    """The line said for one gate. A gate that failed to LOAD fails in every
    group that loads its file, so each of those groups is named, not only the
    one whose call wrote the record first: a broken `worktree-guard.py` is
    also an unguarded `pre-agent`. A failure while running depends on the
    payload, so it names the group it was seen in."""
    group = flat(body.get("group"))
    phase = body.get("phase")
    how = {"load": "failed to load", "run": "failed while running"}.get(
        phase, "failed"
    )
    error, message = flat(body.get("error")), flat(body.get("message"))
    cause = f"{error}: {message}" if error and message else error or message
    groups = [group] if group else []
    if phase == "load" and group in GROUPS:
        groups += [g for g, gates in GROUPS.items() if gate in gates and g != group]
    where = " and ".join(groups)
    others = any(g != gate for name in groups for g in GROUPS.get(name, ()))
    return "".join(
        [
            gate,
            f" {how}",
            f" in {where}" if where else "",
            f" ({cause})" if cause else "",
            "; calls went ahead without it",
            f", and the other gates in {where} still decided" if others else "",
            ".",
        ]
    )
```

And add to `tests/test_a_gate_that_fails_says_so.py`, seen red at `d8e14048`
before it is planted:

```python
def test_a_gate_that_fails_to_load_names_every_group_that_loads_it(repo, tmp_path):
    """A load failure belongs to the file, so it fails wherever the file is
    loaded. `worktree-guard.py` sits in `pre-bash` and `pre-agent`, and the
    `pre-agent` half is the `isolation: "worktree"` spawn the removed rider
    named: one `pre-bash` failure must not report it as a Bash-only gap."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"cmdline.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    lines = said(stop(hooks, repo, "s-x"))
    guard = [line for line in lines if line.startswith("worktree-guard.py ")]
    assert len(guard) == 1, lines
    assert guard[0].startswith(
        "worktree-guard.py failed to load in pre-bash and pre-agent ("
    ), guard
    assert guard[0].endswith(
        "and the other gates in pre-bash and pre-agent still decided."
    ), guard
```

### 🟡 2

In `hooks/ledger-migrate.py`'s module docstring, replace the last sentence:

```python
crash isolation a raising hook is skipped, and the skip is said once per
session at the end of the turn (#28); here that loses one migration attempt,
and the OLD-FORMAT failure still speaks.
```

so that the whole sentence reads "Under `dispatch.py`'s crash isolation a
raising hook is skipped, and the skip is said once per session at the end of
the turn (#28); ...". Optional, for the fixer to judge, in `hooks/routing.py`
inside `rounds`' `except NotADirectoryError`:

```python
        # Caught here rather than raised at the gates. A hook that raises is
        # rendered as an allow by `hooks/dispatch.py` for the call it raised
        # on, and said only once, at the end of the turn, as a gate that
        # failed (#28). Propagating this would turn a nameable state into
        # that, which is the opposite of what `_ordered` refuses it for.
        # `rounds_unreadable` is how a caller asks which of the two happened.
```

### ⬜ 3

In `hooks/dispatch.py#record`, replace the comment above the `opted_in` call:

```python
    # Asked only for a gate not yet written down. In an opted-in main checkout
    # a gate that stays broken then costs one `stat` pair per call after its
    # first; a linked worktree also pays `common_dir`'s `git rev-parse` on
    # every such call, and a repository not opted in, where nothing is ever
    # written, loads `optin.py` again on every such call.
```

Needs a fix: yes — 🟡 1 (the report names one group for a gate that failed to load in two) and 🟡 2 (`hooks/ledger-migrate.py` still says the skip is silent)
Loses a record or crashes: no

## Proof

Files opened in the clone at `d8e14048`: `hooks/dispatch.py`,
`hooks/hooks.json`, `hooks/sealer-stamp.py`, `hooks/optin.py` (lines 31–32,
99–224), `hooks/ledger-migrate.py` (lines 44–60), `hooks/routing.py` (lines
255–268, 388–402), `hooks/commit-review-gate.py` (lines 824–840),
`tests/test_a_gate_that_fails_says_so.py`, `tests/test_dispatch.py` (lines
105–170), `tests/conftest.py` (lines 470–510),
`tests/test_console_is_not_utf8.py` (lines 74–100),
`tests/test_gate_judges_the_repo_it_commits_to.py` (lines 1655–1672),
`seal/specs/1790635415-a-gate-that-fails-to-load-says-so/overview.md`,
`seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md`,
`seal/specs/1790635415-a-gate-that-fails-to-load-says-so/changelog.md`,
`seal/specs/1790635415-a-gate-that-fails-to-load-says-so/survivors.md`,
`CONTRIBUTING.md` (grep for the runner), and the branch diff of `README.md`,
`README.ko.md`, `docs/commit-review-gate-spec.md`,
`hooks/evidence-advisor.py`, `hooks/implementer.py`,
`skills/implement/scripts/seal.py`, `seal/releases/0.4.0.md`,
`seal/releases/0.15.7.md`, `seal/ledger/1790635415-a-gate-that-fails-to-load-says-so.md`
and the three edited test modules. Not opened: `plan.md`, `questions.md`,
`routing.md`, and `phases/phase-1..3.md` beyond what `overview.md` and the
ledger fragment quote from them.
