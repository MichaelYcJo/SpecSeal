# 1790260564-a-moved-file-counts-as-written — review round 2

| Field | Value |
|---|---|
| Target SHA | cd5f2dcd18c2c5530450b3e3a8268cda2f516d31 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 589 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `34bee5dbe22315fbeb947778b96019ef6e16b58d..cc0a2c7cbc5c26b203c6f058a175fcdf3cb32a6c`, 2 commits |
| Contract changes | hook → round-2-report.md, round-2.md, local_specs, on_its_branch, pytest |
| New units | test_a_missing_common_dir_reader_refuses_rather_than_placing_nothing (depth 1) |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790260564 is the verifying round: the diff of round 1's fixes, 1839acd6..065ab7b6, at cd5f2dcd. Its job is whether round 1's verdicts are closed, and whether the units the fixes created (OPTIN, hook, the new cases) are correct.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's yellow finding 1 is closed — a stacked child's local row no longer excuses its parent branch's run | `skills/code-review/scripts/survivor_check.py:1431` | confirmed | executed: O6 fails against `1839acd6`'s script and passes at `cd5f2dcd`; mutation dropping the declared head's exclusion turns O1's three parameters red; read the loop |
| 🟢 | round 1's yellow finding 2 is closed — each local-mode refusal prints its own reason | `skills/code-review/scripts/survivor_check.py:1413` | confirmed | executed: O4's three parameters fail against `1839acd6`'s script and pass at `cd5f2dcd`; mutation giving the cut refusal the tip-off sentence turns O6 red; O2 still pins the tip-off sentence |
| 🟢 | round 1's note 3 is closed — both docstrings name the local-mode test | `skills/code-review/scripts/survivor_check.py:1587` | confirmed | read; the parentheticals beside the name are this round's ⬜ 1 |
| carried | round 1's note 4 — the `corrected` line can name a move's origin | `skills/code-review/scripts/survivor_check.py:1140` | deferred #592 | already deferred in round 1; not in the fix diff and not re-opened |
| 🟢 | round 1's note 5 is closed — both docstrings and ledger C2 name both spellings | `skills/code-review/scripts/survivor_check.py:857` | confirmed | read `:159-161`, `:856-858` and the C2 word diff; a grep of the module and `docs/review-chain-spec.md` finds no other carrier; evidence check strict exit 0 |
| 🟢 | round 1's note 6, first half, is closed — `local_specs` reads the common directory through `hooks/optin.py` | `skills/code-review/scripts/survivor_check.py:1382` | confirmed | read against `hooks/optin.py:99-127`; O1 main, linked and symlinked pass; the second half is this round's ⬜ 2 |
| 🟢 | the fix pass's `survivors.md` row for `hooks/review-skill-gate.py:104` | `seal/specs/1790260564-a-moved-file-counts-as-written/survivors.md` | confirmed | read the comment, true of `git_dir`; executed the fix range: exit 1 without the row, exit 0 with it |
| ❓ | round 1's question on the settle fold's verbatim arrival in `docs/` | `skills/code-review/scripts/survivor_check.py:1047` | ❓ out of verified scope | carried from round 1: not in the fix diff and not answered by the fix pass; the orchestrator answers whether it is #563's class and where it goes |
| ⬜ 1 | two parentheticals in `whole_range` and `report` state the pre-cut rule, a 121-character line, and the #554 test comment | `skills/code-review/scripts/survivor_check.py:1589` | **fixed** `d81e801f` | fixed at d81e801f — cc0a2c7c; executed: an unresolved stacked-child row prints nothing on the parent's run although its branch holds the tip; behaviour matches U1, the prose does not |
| ⬜ 2 | `routing.py` is still executed once per declaration; round 1's note 6 is recorded fixed as a whole | `skills/code-review/scripts/survivor_check.py:1413` | answered | no code change; round 1's sixth verdict was corrected in the record at 34bee5db, and routing.py's per-declaration load stays as instructed; read: `hook(ROUTING, …)` is `on_its_branch`'s first line |
| ⬜ 3 | the `hook` refusal says `optin.py` decides whose a declaration is, and no case pins the `optin.py` refusal | `skills/code-review/scripts/survivor_check.py:1366` | **fixed** `d81e801f` | fixed at d81e801f; executed: `OPTIN` pointed at a missing file refuses with that sentence, in shared mode too |
| ⬜ 4 | a parent run from a detached HEAD with no local head is excused by a stacked child's row | `skills/code-review/scripts/survivor_check.py:1432` | answered | no code change; overview.md's Not done names the detached-HEAD parent run as the documented no-local-branch bound, added at d81e801f; executed: exit 0, excused; the same range as the child's own older-tip run, so the documented *no local branch* bound; the orchestrator answers whether O1's residual names it |

## Paste-ready fixes

```text
survivor_check.py, whole_range's #439 paragraph, from "asked of an
unresolved declaration" to the end of the docstring:

    asked of an unresolved declaration before it is printed, by the same
    test a resolved one gets -- the lazily computed `changed` list in shared
    mode, `on_its_branch` in local mode: one with no owner -- an `--exempt`
    file passed from anywhere -- or owned by a work item this range touches
    (in local mode, one `on_its_branch` accepts) is a declaration this run
    could have used, and prints under `unresolved` as before. The wrong
    allow is empty, because an unresolved row excuses nothing whether
    printed or not.

survivor_check.py, report's docstring:

    item the range touches nothing of (in local mode, one `on_its_branch`
    refuses) never arrives (#439); they silence

tests/test_a_corrected_sentence_survives_elsewhere.py, the #554 comment:

# item's `routing.md` `Branch` row: the row holds over a range whose tip is on
# that branch and on no local branch that one was cut from. Shared mode is
# unchanged.
```
```python
# survivor_check.py -- load each hook once per process; a missing file still
# refuses every time, because lru_cache does not cache an exception.
import functools


@functools.lru_cache(maxsize=None)
def hook(path, name, what):
    ...
```
```python
def hook(path, name, what):
    """A module under `hooks/`, loaded by path, or `Refused` saying which.

    The hooks ship beside this script in the plugin; a copy without one
    cannot place a local-mode declaration, and that is unusable input
    rather than a judgment. `what` is what the missing file answers."""
    if not os.path.isfile(path):
        raise Refused(
            f"cannot read {path}, which {what}. "
            "This script ships beside it in the plugin."
        )
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# local_specs:
    common = hook(
        OPTIN, "specseal_optin", "says where local mode's seal/ root is"
    ).git_common_dir(root)

# on_its_branch:
    routing = hook(
        ROUTING, "specseal_routing", "says whose a local-mode declaration is"
    )
```
```python
# tests/test_a_corrected_sentence_survives_elsewhere.py, beside O5
def test_a_missing_common_dir_reader_refuses_rather_than_placing_nothing(tmp_path):
    """O5's twin for `hooks/optin.py`: a copy without it cannot say where
    local mode's root is, and refuses (exit 2's `Refused`) naming that."""
    loaded = module()
    loaded.OPTIN = str(tmp_path / "gone" / "optin.py")
    with pytest.raises(loaded.Refused, match=r"optin\.py, which says where"):
        loaded.local_specs(str(tmp_path))
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `cd5f2dcd` | exit 0, 121 passed |
| the O1, O2, O4, O5 and O6 cases against `1839acd6`'s `survivor_check.py` (script swapped in the clone, restored) | exit 1: O6 and O4 ×3 failed, 5 passed |
| mutation: `on_its_branch` no longer subtracts the declared head from `--contains` heads | exit 1: O1 main, linked, symlinked failed |
| mutation: the cut refusal returns the tip-off sentence | exit 1: O6 failed |
| probe: O6's stack, B detached at its tip and the local `work-item-b` deleted, A's row | exit 0, B's survivor excused by A's row |
| probe: O6's stack plus an unresolved row in A's `survivors.md`, run on B and on A | on B: no `unresolved` line; on A: printed under `unresolved` |
| probe: `OPTIN` pointed at a missing file, `whole_range` over a shared-mode declaration | `Refused`: *cannot read …/optin.py, which says whose a local-mode declaration is* |
| `survivor_check.py --range 1839acd6..065ab7b6 --root .`, with and without the work item's `survivors.md` | with: exit 0, 35 sentences, 1 excused; without: exit 1, `hooks/review-skill-gate.py:104` |
| `survivor_check.py --range c52e8350...cd5f2dcd --root . --exempt` the work item's `survivors.md`, and the same from `f7ac2a24` | exit 0 both, 73 sentences, no removed wording standing |
| `bin/evidence-check --strict .` | exit 0, 0 drifted, 0 broken in every section |
| `.github/scripts/rider_check.py` | exit 0, 25 ok · 0 drifted · 0 broken |
| Broad gate: full suite, repository-wide lint, typecheck | not yet — not run by this round; the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:1404` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1594` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1547` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1140` | round 1's ⬜ 4 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:856` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1353` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1120` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:544` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1566` | round 1's 🟢 — confirmed |
| round-1 | `docs/review-chain-spec.md:867` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1047` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
