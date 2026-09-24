# 1790260564-a-moved-file-counts-as-written — review round 1

| Field | Value |
|---|---|
| Target SHA | 6e48cb5fca905d3806c3316691d288eb02f93206 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 589 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a stacked child's local declaration excuses its parent branch's run) and 🟡 2 (the local-mode `not yours` reason names a branch that `routing.md` does not name) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790260564 reviews the build at 6e48cb5f against spec.md and plan.md (frame 78422e7c): held moved text (#563), the gathered-text reading's three assumptions (#564), and local-mode ownership (#554). The classes enumerated are every way text reaches a range without the range writing it, every reader of a fragment path or the released region, every place ownership of a declaration is decided in both modes, and every carrier of the corrected sentences.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a stacked child's local-mode declaration excuses its parent branch's whole run, because the parent's tip is an ancestor of the child's branch | `skills/code-review/scripts/survivor_check.py:1404` | open | executed: the parent's run excused at exit 0 on `6e48cb5f`, and exit 1 without the row; O2 pins a sibling only; the proposed fix was run green over the whole module |
| 🟡 2 | the `not yours` reason in local mode is one fixed sentence for four refusals, and it names a branch that a missing or branchless `routing.md` does not name; O4 pins the false sentence | `skills/code-review/scripts/survivor_check.py:1594` | open | read, and executed: the three O4 parameters print the fixed sentence on `6e48cb5f` |
| ⬜ 3 | the unresolved arm's docstring carriers still describe ownership by the diff alone | `skills/code-review/scripts/survivor_check.py:1547` | open | read; ledger 0.15.1 U1 was corrected for the same sentence |
| ⬜ 4 | a key removed at two paths and arriving at one keeps the later path as the source, so the `corrected` line can name a move's origin | `skills/code-review/scripts/survivor_check.py:1140` | open | read, not probed; the survivor coordinate and the score are unaffected |
| ⬜ 5 | the predicate's docstring and the module docstring spell the gathered fragment's path one way while G7 pins the other | `skills/code-review/scripts/survivor_check.py:856` | open | read |
| ⬜ 6 | `local_specs` restates the common-dir reader in `hooks/optin.py`, and `routing.py` is executed once per declaration | `skills/code-review/scripts/survivor_check.py:1353` | open | read; the plan's technical context names the existing reader |
| 🟢 | #563 pairing: a moved sentence is neither removed nor written, pairing meets only across paths, and `wanted` only grows | `skills/code-review/scripts/survivor_check.py:1120` | confirmed | read the unit and the loop; executed the module, 119 passed |
| 🟢 | #564: CRLF at the read boundary, one region rule, and the fragment reader asking the predicate | `skills/code-review/scripts/survivor_check.py:544` | confirmed | read every reader of committed text in the module; executed G7-G10 within the module run |
| 🟢 | #554 local-mode ownership for the work item's own range, in the main and the linked worktree and through a symlink | `skills/code-review/scripts/survivor_check.py:1566` | confirmed | executed O1's three parameters within the module run |
| 🟢 | the branch's own prose carries no survivor, and its ledger rows and rider hold | `docs/review-chain-spec.md:867` | confirmed | executed survivor-check over the branch range, strict evidence and the rider check, all exit 0 |
| ❓ | the settle fold's verbatim arrival in `docs/` is written, since the retired side leaves the range before pairing | `skills/code-review/scripts/survivor_check.py:1047` | ❓ out of verified scope | read, not measured; the orchestrator answers whether it is #563's class and where it goes |

## Paste-ready fixes

```python
def on_its_branch(root, item, b):
    """None when the range's tip `b` is on the branch `item`'s `routing.md`
    names -- `refs/heads/<Branch>` or an ancestor of it -- and on no local
    branch that one was cut from; otherwise the reason it is not, as the
    `not yours` line prints it.

    Asked of the range's tip rather than of the checkout, because ownership
    is a question about the range: a detached HEAD at the branch's tip is
    the same range. A branch cut from another carries that branch's history,
    so a tip on it may be the other branch's tip, and that range is the
    other branch's run: a stacked child's row would otherwise excuse its
    parent's whole range. A `routing.md` that is missing, will not parse or
    names no branch, and a branch that does not resolve, each answer with
    their own reason -- the declaration then prints under `not yours`,
    which is the loud direction."""
    if not os.path.isfile(ROUTING):
        raise Refused(
            f"cannot read {ROUTING}, which says whose a local-mode declaration "
            "is. This script ships beside it in the plugin."
        )
    try:
        with open(os.path.join(item, "routing.md"), encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return "it has no routing.md this run can read"
    spec = importlib.util.spec_from_file_location("specseal_routing", ROUTING)
    routing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(routing)
    declared = routing.parse(text)
    if not declared:
        return "its routing.md is not a declaration naming a branch"
    ref = f"refs/heads/{declared['branch']}"
    tip = resolves(root, ref)
    if tip is None:
        return f"the branch its routing.md names, {declared['branch']}, is not here"
    if git(root, "merge-base", "--is-ancestor", b, ref) is None:
        return "this range's tip is not on the branch its routing.md names"
    # A branch cut from another carries that branch's history, so a tip on
    # it can be the tip of a branch it was cut from -- that branch's run, and
    # a stacked child's row would otherwise excuse its parent's whole range.
    heads = git(
        root, "for-each-ref", "--contains", b, "--format=%(objectname)", "refs/heads"
    )
    for head in set((heads or "").split()) - {tip}:
        if git(root, "merge-base", "--is-ancestor", head, ref) is not None:
            return (
                "this range's tip is on a branch the one its routing.md names "
                "was cut from"
            )
    return None
```
```python
# tests/test_a_corrected_sentence_survives_elsewhere.py, after O2
def test_a_stacked_childs_declaration_does_not_reach_its_parents_range(tmp_path):
    """O6. Work item A's branch is cut from work item B's, so B's tip is an
    ancestor of A's branch; on B's checkout A's `release...HEAD` row
    resolves onto B's own range. The tip being on A's branch is not enough:
    it is on B's, which A's was cut from, and the range is B's run."""
    repo = tmp_path / "probe"
    survivors = local_mode_items(repo)
    probe_git(repo, "switch", "-q", "work-item-b")
    probe_git(repo, "switch", "-qc", "work-item-a-stacked")
    item = os.path.dirname(survivors)
    with open(os.path.join(item, "routing.md"), "w", encoding="utf-8") as handle:
        handle.write(
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n"
            "| Destination | open the pull request |\n| Branch | work-item-a-stacked |\n"
        )
    build(repo, {"filler.md": "# filler\n\nA's own later change.\n"}, "A on top of B")
    root = checkout(repo, "work-item-b", linked=False)
    code, text = run("--range", "release...HEAD", "--root", root, "--exempt", survivors)
    assert code == 1, f"a stacked child's declaration excused its parent\n{text}"
    assert "b-notes.md" in text and "not yours" in text, text
    assert "was cut from" in text, text
```
```text
The sentences that say the row holds wherever the tip is on the branch
change with it:

docs/review-chain-spec.md:870-871
  local mode, where the owner is never in a range's diff, it is the `Branch`
  row of the work item's `routing.md`: the row holds where the tip is on that
  branch and on no local branch it was cut from.

survivor_check.py module docstring (the second-anchor paragraph) and the
local-mode paragraph of whole_range: add "and on no local branch that one was
cut from" after "whose tip is on that branch".

plan.md failure scenario for #554 and ledger row O1: the exposure is a reused
branch name only once the cut is refused; name the stacked case as measured
and closed.
```
```python
# whole_range, inside the loop -- replaces the `mine, item = True, None`
# block and the `why = (...)` expression under `if not mine:`
        owner = OWNER_DIR.match(source.replace("\\", "/"))
        mine, item, why = True, None, "this range touches nothing in it"
        if owner is not None:
            if local is None:
                local = local_specs(root)
            item = local_item(source, local)
        if owner is not None and item is not None:
            # Local mode: nothing under the root is committed, so the owner
            # is never in `changed`, and the work item's branch answers.
            why = on_its_branch(root, item, b)
            mine = why is None
        elif owner is not None:
            if changed is None:
                names = git(root, "diff", "--name-only", "--no-renames", "-z", a, b)
                changed = [path for path in (names or "").split("\0") if path]
            mine = any(path.startswith(owner.group(1) + "/") for path in changed)
        if left is None:
            if mine:
                unresolved.append((spec, grounds))
            continue
        if not mine:
            # The reason is the test that refused it, so a person reading
            # the line knows which file to open.
            foreign.append((spec, grounds, owner.group(1), why))
            continue
```
```python
# tests/test_a_corrected_sentence_survives_elsewhere.py, O4
@pytest.mark.parametrize(
    "routing, reason",
    [
        (None, "it has no routing.md this run can read"),
        (
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n",
            "its routing.md is not a declaration naming a branch",
        ),
        (
            "| Axis | Answer |\n|---|---|\n| Review | through the review chain |\n"
            "| Destination | open the pull request |\n| Branch | no-such-branch |\n",
            "the branch its routing.md names, no-such-branch, is not here",
        ),
    ],
    ids=["missing", "no-branch", "unknown-branch"],
)
def test_a_local_mode_declaration_nobody_can_place_is_not_yours(
    tmp_path, routing, reason
):
    # ... body unchanged down to the `not yours` assertion, then:
    # §14: the reason is what refused the row, never a branch nobody named.
    assert reason in text, text
    assert "tip is not on the branch" not in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `6e48cb5f` | exit 0, 119 passed |
| `survivor_check.py --range f7ac2a24..6e48cb5f --root .` | exit 0, 350 files, 68 sentences removed, no removed wording standing |
| `bin/evidence-check --strict .` | exit 0, 2082 ok · 0 drifted · 0 broken; 1 work item read, 0 refused |
| `.github/scripts/rider_check.py` | exit 0, 25 ok · 0 drifted · 0 broken |
| stacked-branch probe (one throwaway probe file, deleted): A cut from B, A's local `release...HEAD` row, run on B's checkout at `6e48cb5f` | exit 0, B's survivor excused by A's row; without `--exempt`, exit 1 naming `b-notes.md` |
| `git rev-parse --git-common-dir` from a subdirectory of a probe repository | `../.git` |
| 🟡 1 + 🟡 2 fixes applied in the clone, whole module | exit 0, 121 passed; reverted afterwards |
| the four new or changed cases against `6e48cb5f`'s script | 4 failed: O4 ×3 print the old sentence, O6 exits 0 excused |
| Broad gate: full suite, repository-wide lint, typecheck | not yet — not run by this round; the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
