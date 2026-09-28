# 1790635415-a-gate-that-fails-to-load-says-so — review round 1

| Field | Value |
|---|---|
| Target SHA | d8e14048f04d2665c75573a967e1af0c09929b8a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #660 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the report names one group for a gate that failed to load in two) and 🟡 2 (`hooks/ledger-migrate.py` still says the skip is silent) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1, the first finding round, over the whole branch `551c7967...d8e14048`. Asked to review the frame's decisions against the owner's pre-edit answer (fail open, but say so), with the isolation property, a healthy group's output, a broken git directory, a repository that has not opted in, and the silent path's cost named as where a defect would leave the root. Q1, the on-screen render, was withheld as the orchestrator's measurement.

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

## Paste-ready fixes

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
```python
crash isolation a raising hook is skipped, and the skip is said once per
session at the end of the turn (#28); here that loses one migration attempt,
and the OLD-FORMAT failure still speaks.
```
```python
        # Caught here rather than raised at the gates. A hook that raises is
        # rendered as an allow by `hooks/dispatch.py` for the call it raised
        # on, and said only once, at the end of the turn, as a gate that
        # failed (#28). Propagating this would turn a nameable state into
        # that, which is the opposite of what `_ordered` refuses it for.
        # `rounds_unreadable` is how a caller asks which of the two happened.
```
```python
    # Asked only for a gate not yet written down. In an opted-in main checkout
    # a gate that stays broken then costs one `stat` pair per call after its
    # first; a linked worktree also pays `common_dir`'s `git rev-parse` on
    # every such call, and a repository not opted in, where nothing is ever
    # written, loads `optin.py` again on every such call.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
