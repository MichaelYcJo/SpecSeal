# Round 2 report — 1790260564-a-moved-file-counts-as-written

The verifying round. Target SHA `cd5f2dcd`; the surface is round 1's fix
range `1839acd6..065ab7b6` (c315e8c3, 0313a669, 065ab7b6) and the units its
`New units` row names: `OPTIN`, `hook`, and the O6 case. Base
`origin/release/v0.15.3` = `c52e8350`.

Worked in a `git clone --no-local` of the worktree at the target SHA, under
this round's scratchpad directory. Carried from round 1 without re-deriving:
the coordinates of `on_its_branch`, `whole_range`, `local_specs` and the O-series
fixtures, and `f7ac2a24` as the branch's routing commit. Every verdict below
is re-derived.

## What the fix pass claimed, and what the code does

| Claim (fix pass and round 1's record) | Found |
|---|---|
| `on_its_branch` refuses the stacked-child case | Read `survivor_check.py:1431-1439`: a tip that is also on another local head which is itself an ancestor of the declared branch is refused. Executed: O6 red against `1839acd6`'s script, green at the target. Confirmed |
| It returns a reason sentence for each of five refusals, and `whole_range` prints it | Read `:1413-1440` and `:1606-1637`. Five returns, five sentences; shared mode keeps its default sentence. Executed: O4's three parameters red against `1839acd6`'s script. Confirmed |
| O4 gains `unknown-branch`; O6 is added | Read both cases. Executed: 4 failed on the pre-fix script, all green at the target. Two mutations, each killed (below). Confirmed |
| The #439 paragraph and `report`'s docstring now describe both modes | Read `:1583-1592` and `:1686-1697`. Both name `on_its_branch`. The parentheticals written beside it state the rule as it was before the cut (⬜ 1) |
| The docstrings name both fragment spellings; C2 in 0.15.1 corrected | Read `:159-161`, `:856-858`, and the C2 word diff. Grep of the module and `docs/review-chain-spec.md` finds no other one-spelling carrier. Confirmed |
| `local_specs` uses `hooks/optin.py#git_common_dir` through a new `hook(path, name)` | Read `:1355-1386` and `hooks/optin.py:99-127`. Confirmed. Round 1's second half of the same note, `routing.py` executed once per declaration, is unchanged (⬜ 2). The `hook` refusal sentence is routing-specific but now serves `optin.py` too (⬜ 3) |
| `survivors.md` row for `hooks/review-skill-gate.py:104` | Read `hooks/review-skill-gate.py:98-110`: the comment describes that gate's own `rev-parse --git-dir` reader and is true of it. Executed the fix range with and without the row: exit 0 excused, exit 1 standing. Confirmed |
| The overview divergence row corrected | Read: it names the five refusals and O6. Confirmed |
| ⬜ 4 deferred to #592 after a probe reproduced it | Not in the fix diff; carried as deferred |

## Findings

### ⬜ 1 — Two parentheticals the fix pass wrote still state the ancestor-only rule

`skills/code-review/scripts/survivor_check.py:1589`, in `whole_range`'s #439
paragraph, and `:1688-1689`, in `report`'s docstring.

**What is wrong.** The #439 paragraph says an unresolved declaration owned by
a work item this range touches, *(in local mode, whose branch holds the
tip)*, prints under `unresolved`. After the cut, a stacked child's row on
its parent's run is one whose branch holds the tip, and it prints nothing.
`report`'s docstring says the one that never arrives is *(in local mode,
one whose branch the range's tip is off)*. That is one of the five refusals.
Ledger row U1 in 0.15.1 was given the cut clause in the same fix pass. These
two docstring carriers of the same sentence were not.

**Executed.** A probe built O6's stack and added an unresolved row
`origin/gone..HEAD` to A's `survivors.md`. On B's checkout the unresolved row
printed nothing, although A's branch holds B's tip. On A's checkout it
printed under `unresolved`. The behaviour is what U1 states; the docstring
is what is wrong.

Two smaller carriers of the same class:
- The same paragraph's line `:1590` is 121 characters: a rewrap left the rest of the sentence on one line.
- `tests/test_a_corrected_sentence_survives_elsewhere.py:3491-3493`, the #554 section comment, still says *the row holds over a range whose tip is on that branch*.

**Why it is ⬜.** The behaviour is right and pinned by O6. Only prose
describing it is incomplete.

### ⬜ 2 — `routing.py` is still executed once per declaration

`skills/code-review/scripts/survivor_check.py:1413`.

Round 1's note 6 had two halves. The first, `local_specs` restating the
common-dir reader, is closed. The second, *`on_its_branch` executes
`routing.py` afresh for every declaration it is asked about*, is unchanged:
`hook(ROUTING, "specseal_routing")` is the first line of `on_its_branch`, so
every local-mode declaration that resolves onto the range re-reads and
re-executes the file. Round 1's record marks the whole note `fixed`, which
overstates the fix. The cost is small, which is why this stays ⬜.

### ⬜ 3 — The `hook` refusal says `optin.py` decides whose a declaration is, and nothing pins it

`skills/code-review/scripts/survivor_check.py:1366`, the new unit `hook`.

**What is wrong.** `hook` was generalised from `on_its_branch`'s routing
check, but its sentence was not. A missing `hooks/optin.py` now refuses with
*cannot read …/optin.py, which says whose a local-mode declaration is*.
`optin.py` says where local mode's root is; `routing.py` says whose a
declaration is.

**Executed.** A probe loaded the module with `OPTIN` pointed at a missing
file and ran `whole_range` over a shared-mode `survivors.md`. It raised
`Refused` with the sentence above.

**Two things the probe also showed, neither of them a defect.**
- Shared mode now needs `hooks/optin.py`. `local_specs` runs for every
  declaration under `seal/specs/`, in either mode, so a copy of the script
  with no `hooks/` beside it refuses at exit 2 in shared mode as well. Before
  the fix, shared mode needed nothing from `hooks/`. Every shipped layout
  carries `hooks/` beside the script, including `hygiene.yml`'s checkout and
  the plugin cache, and exit 2 is the loud direction.
- No case pins the `optin.py` refusal. O5 pins the routing one only.

**Why it is ⬜.** In no shipped layout is `optin.py` missing, so the sentence
is one no user reads today. Under `agent-contract` §14 the sentence and a
case that pins it belong together.

### ⬜ 4 — A parent run from a detached HEAD, with no local head, is still excused by the child's row

`skills/code-review/scripts/survivor_check.py:1432`.

**Executed.** Round 1's stacked shape, with B's checkout switched to a
detached HEAD at B's tip and the local `work-item-b` branch deleted. A's
`release...HEAD` row excused B's run at exit 0, printing `every survivor is
excused by a row above (1)`.

**Why it is ⬜ and not a fix.** When no ref names the parent, this range is
the same range as a fix-pass range whose tip is an older commit of A. That
is the shape the ancestry test exists to accept (round 1's grounds, still
true). Widening the search to `refs/remotes` does not separate them either.
Once A is pushed, a remote head for A that sits between an older tip and A's
local head would refuse A's own fix-pass run. The docstring (`:1398`) and
ledger O1 both say *no local branch*, so the code does what it documents.
The case left open is that sentence's bound. It is not recorded as a
residual anywhere. **Who answers it:** the orchestrator, who decides
whether O1's residual cell names it.

## Regression tests to plant

- `tests/test_a_corrected_sentence_survives_elsewhere.py`: a case for the `optin.py` refusal beside O5 (⬜ 3's fence). Optional, and only if ⬜ 3's sentence is changed.

## Facts for the evidence ledger

- O1's residual: a parent run from a detached HEAD whose parent has no local head is excused by a stacked child's relation-spelled row, because it is the same range as the child's own older-tip run (⬜ 4, executed). Whether to write it is the orchestrator's call.

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
| ⬜ 1 | two parentheticals in `whole_range` and `report` state the pre-cut rule, a 121-character line, and the #554 test comment | `skills/code-review/scripts/survivor_check.py:1589` | open | executed: an unresolved stacked-child row prints nothing on the parent's run although its branch holds the tip; behaviour matches U1, the prose does not |
| ⬜ 2 | `routing.py` is still executed once per declaration; round 1's note 6 is recorded fixed as a whole | `skills/code-review/scripts/survivor_check.py:1413` | open | read: `hook(ROUTING, …)` is `on_its_branch`'s first line |
| ⬜ 3 | the `hook` refusal says `optin.py` decides whose a declaration is, and no case pins the `optin.py` refusal | `skills/code-review/scripts/survivor_check.py:1366` | open | executed: `OPTIN` pointed at a missing file refuses with that sentence, in shared mode too |
| ⬜ 4 | a parent run from a detached HEAD with no local head is excused by a stacked child's row | `skills/code-review/scripts/survivor_check.py:1432` | open | executed: exit 0, excused; the same range as the child's own older-tip run, so the documented *no local branch* bound; the orchestrator answers whether O1's residual names it |

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

The probe file was one throwaway file in the clone's `tests/`, run and
deleted; each mutation and the script swap were restored with `git checkout`,
and the clone's status was clean afterwards.

## Paste-ready fixes

None of these is owed: every finding this round is ⬜. They are here so a
smith who takes one does not rebuild it from prose.

### ⬜ 1

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

### ⬜ 2

```python
# survivor_check.py -- load each hook once per process; a missing file still
# refuses every time, because lru_cache does not cache an exception.
import functools


@functools.lru_cache(maxsize=None)
def hook(path, name, what):
    ...
```

### ⬜ 3

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

Needs a fix: no

Loses a record or crashes: no

The fix range opened nothing that needs a fix. Every earlier finding the
round was asked about is closed or already deferred, and the four notes
above are ⬜. Nothing is left open that blocks, so the broad gate has come
due: the next act is the sealer's spawn.

## Proof block

Files opened this round, all in the clone at `cd5f2dcd` unless named:

- `skills/code-review/scripts/survivor_check.py` — `:156-161`, `:234-237`, `:345-369`, `:853-858`, `:1350-1440`, `:1548-1697`, and the fix-range diff
- `tests/test_a_corrected_sentence_survives_elsewhere.py` — `:3484-3706` and the fix-range diff; the `module`, `run`, `build` and `probe_git` helpers
- `hooks/optin.py` — `:31-46`, `:99-127`
- `hooks/routing.py` — `:137-177`
- `hooks/review-skill-gate.py` — `:95-110`
- `bin/test`
- `seal/specs/1790260564-a-moved-file-counts-as-written/changelog.md` — `:18-29`; `spec.md` — `:198-206`; `survivors.md`, `overview.md`, `plan.md` (word diffs)
- `agents/smith.md` — `:220-229`; `skills/code-review/orchestration.md` — `:91-98`
- `docs/review-chain-spec.md`, `seal/ledger/1790260564-a-moved-file-counts-as-written.md`, `seal/releases/0.9.5.md`, `0.13.1.md`, `0.15.0.md`, `0.15.1.md` — the fix-range word diffs
- in the worktree: `rounds/round-1.md` and `rounds/round-1-report.md`
