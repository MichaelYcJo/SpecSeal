# Round 1 report — 1790260564-a-moved-file-counts-as-written

Target SHA `6e48cb5f` (build closed at `896c787e`; `6e48cb5f` re-lines the
plan's approval only). Base `origin/release/v0.15.3` = `c52e8350`. Contract:
this work item's `spec.md` and `plan.md` at frame `78422e7c`; issues #563,
#564, #554. First round, so no earlier `round-N.md` to carry coordinates from.

Worked in a `git clone --no-local` of the worktree at the target SHA. The
shared session scratchpad was emptied by something outside this round between
two of its calls, clone included; the clone was re-made at the same SHA and
nothing read before the loss was reused without re-reading.

## What the account claimed, and what the code does

| Claim (smith's hand-back) | Found |
|---|---|
| #564: CRLF normalised in `read_blobs` | Read: `survivor_check.py:455`. Every committed text in the module goes through it; the other readers (`read_exemptions`, the `routing.md` read in `on_its_branch`, and `unverified_check.py`'s `folded_items`) open in text mode or split with `splitlines`, so none needs it. Confirmed |
| #564: one released-region helper | Read: `released_lines` at `:544` is behind both `blank_released` and `only_released`, and `newly_released` reads through the latter. Confirmed |
| #564: the fragment reader asks `a_gathered_fragment` | Read: `:1060-1064`, over `tracked(root, a)`. Confirmed. The predicate's own docstring and the module docstring still spell one path (⬜ 5) |
| #563: `paired_across_paths`, a moved sentence neither gone nor written | Read `:1120-1152` and `corrected`'s loop. Within one path a key is in `gone` or in `fresh` and never both, and that holds for `CHANGELOG.md` too: `counted` uses the unfiltered `moved`, `new` uses the filtered one. So pairing can only meet across paths. `wanted` only grows (a paired sentence's n-grams are exactly its fresh twin's). Confirmed |
| #563: S18 rewritten because M3's premise was wrong; M1, M2, M6, M7 added | Read the cases and `overview.md`'s divergence row. Executed: module green (below) |
| #554: `whole_range` reads `routing.md`'s `Branch` row in local mode (`on_its_branch`) | Read `:1378-1404`, `:1566-1584`. The ancestor test lets a stacked child's declaration excuse its parent's run (🟡 1, executed) |
| #554: the `not yours` reason names the refused check | Read `:1594-1599`. In local mode one fixed sentence is printed for four different refusals, three of them false (🟡 2) |
| The same sentence corrected in `agents/smith.md`, `skills/code-review/orchestration.md` and the module docstring; smith.md RIDER re-stamped | Read all three. Executed `rider_check.py`: 25 ok. Two docstring carriers of the unresolved half were missed (⬜ 3) |
| Two `docs/review-chain-spec.md` sentences corrected in place, no marker; 951 lines | Read `:867-871` and `:924-930`. Under `LINE_CEILING = 1000` in `tests/test_a_document_has_room_for_the_next_fold.py`. Confirmed |
| Many `seal/releases/*.md` rows re-read or corrected; R1 lost one anchor | Read the word diff. R1 dropped the old S18 name, and that claim moved to fragment row M1. Executed strict evidence: 0 drifted, 0 broken |
| `survivor-check --range f7ac2a24..HEAD` clean; module 119 passed | Executed both at `6e48cb5f`: same results |

## Classes enumerated (§12)

**Every way text reaches a range without the range writing it.**

- Move, meaning a file moved whole: held by `paired_across_paths` (M1). Executed through the module.
- Rename: held; it is a move under `--no-renames` (S18). Executed.
- Split: held (M2). Executed.
- Gather: held. The #557 filter predates this branch, and this branch extends it to the other path spelling (G7), a heading inside a fragment (G8) and CRLF (G10). Executed.
- The ledger fold (`.github/scripts/fold_ledger.py`) moves rows verbatim from `seal/ledger/<id>.md` into `seal/releases/X.md`. Read: that is now a paired move, so it removes nothing where it used to remove every row and write each one back. The outcome is still silence, and the count drops.
- Merge: not held, and this is older than the branch. Read: under `A...B` the left end is the merge base, so a merged sibling's text sits at `a` already. Under a two-dot `A..B` that spans a merge of another branch, the sibling's writing counts as the range's own. Not a finding for this branch.
- The settle fold, `spec.md` into `docs/`: **not held**. Read: `retired_directories` takes the retired directory out of `paths` before the pairing runs (`:1047-1050` against `:1115`). So a statement folded verbatim arrives with no removal to pair with and is written. This is the one move member left writing, and the outcome is unmeasured (❓ below).
- A copy (the source stays): written by design. M7 pins this, and `docs/review-chain-spec.md`'s rule sentence agrees.

**Every reader of a fragment path or of the released region.**

- Inside this module: `a_gathered_fragment`, used by `corpus`, `corrected`'s path filter and the fragment reader. `released_lines`, used by `blank_released`, `only_released` and `newly_released`. All read one rule.
- Outside it: `.github/scripts/gather_changelog.py` (it globs one spelling and ends a section at any `## `) and `publish_release_note.py#section_body`. Both are `spec.md` §*Out* and #586.
- Prose carriers of the one-spelling claim remain (⬜ 5).

**Every place ownership of a declaration is decided, in both modes.**

- `whole_range` decides it once, as `mine`, for both the resolved and the unresolved arm. `report` only prints it.
- `broad_gate.py#exemptions` and `hygiene.yml` hand files over and decide nothing.
- Shared mode keeps its diff test unchanged.
- Local mode uses `on_its_branch`, and its ancestor test is wider than the plan's failure scenario says (🟡 1).

**Every carrier of the sentences this branch corrected.**

- *Up to the next `## ` heading*: the module docstring is corrected, and so is 0.15.1 C1. The `CHANGELOG.md:37` line is a released entry and stays as written. `publish_release_note.py:144` describes that script's own reader, so it is true.
- *A pure move is silent because written back*: corrected in `docs/`, the docstring, the test comment and R1. `CHANGELOG.md:56-59` is released.
- *Never reaches a range that touches nothing in your own work item*: smith.md, orchestration.md, the module docstring and `docs/` are corrected. Two docstring paragraphs about the unresolved arm are not (⬜ 3).
- *#554, open*: replaced in `docs/`.

## Findings

### 🟡 1 — A stacked branch's local declaration excuses its parent branch's whole run

`skills/code-review/scripts/survivor_check.py:1404` (`on_its_branch`).

**What is wrong.** Ownership is *`b` is `refs/heads/<Branch>` or an
ancestor of it*. Every commit a branch was cut from is an ancestor of it.
Suppose work item A's branch is cut from work item B's branch, which is what
stacked branches are. Then B's tip is on A's branch. On B's checkout, A's
local row `release...HEAD` resolves onto B's own range, and the ancestor
test says it is A's.

**Executed.** In a probe at `6e48cb5f`, B's run with A's local
`survivors.md` exited 0 with `declared the whole range release...HEAD` and
`every survivor is excused by a row above (1)`. The same range with no
`--exempt` exited 1 and named `b-notes.md`.

**Why it matters.** This is the wrong allow the second anchor exists to
refuse. `docs/review-chain-spec.md:858`: *A declaration in `survivors.md`
speaks to its own work item's runs and to no other.* The plan's failure
scenario (`plan.md:63-68`) names only a reused branch name, and phase 3's
failure direction says the allow is *bounded by the branch-ancestor test
(O2)*. But O2 is a sibling, and a sibling's tip is never an ancestor.
Nothing pins the parent.

The account's grounds for choosing ancestry over equality are a fix-pass
range whose tip is an older commit of the same branch. That still holds
under the fix below, because such a tip is on no *other* local branch the
declared one was cut from.

**The fix.** After the ancestor test, refuse when `b` is also on another
local branch whose head is itself an ancestor of the declared branch. That
is the branch the declared one was cut from, and the range is its run. It is
one `for-each-ref --contains` call plus one `merge-base` per head it
returns, asked only of a declaration that would have matched.

Executed in the clone, then reverted:
- The whole module ran at 121 passed with the fix and the two case changes below.
- The new O6 case exited 0 (excused) on `6e48cb5f`.
- The fixture's `release` head, which also contains A's history, is not a strict ancestor of B's tip, so O1 main, linked and symlinked stayed green.

The docs sentence and both docstrings that say *holds over a range whose tip
is on that branch* change with it.

### 🟡 2 — The `not yours` reason names a branch that `routing.md` does not name

`skills/code-review/scripts/survivor_check.py:1594-1599`, and it is pinned by
`tests/test_a_corrected_sentence_survives_elsewhere.py:3650`.

**What is wrong.** `whole_range` prints *this range's tip is not on the
branch its routing.md names* for every local-mode refusal. `on_its_branch`
returns the same False for four different facts:

- `routing.md` is missing or unreadable.
- It does not parse, or names no branch.
- The branch it names is not a ref here.
- The tip is off that branch.

Only the last one is what the sentence says. O4 pins the sentence for the
first two, where no branch is named at all.

**Why it matters.** The reason clause is this branch's §14 change, and
`overview.md` justifies it by *names the wrong file to open*. For a missing
`routing.md` the line sends the reader to a file that does not exist, to
look for a branch it does not name. Under 🟡 1's fix the stacked-parent
refusal would also print this sentence, and there it is false outright,
because the tip *is* on that branch. So the reason has to come from the
function that knows which test refused.

**The fix.** `on_its_branch` returns `None` for *mine*, and otherwise
returns the reason sentence. `whole_range` prints what it returns. This is
executed with 🟡 1's fix, and the three O4 parameters, one of them new
(`unknown-branch`), each go red on `6e48cb5f` printing the old sentence.

### ⬜ 3 — Two docstring paragraphs still describe the unresolved arm by the diff test alone

- `survivor_check.py:1546-1549`, in the #439 paragraph of `whole_range`: *ownership is asked of an unresolved declaration … with the same lazily computed `changed` list*. In local mode it is asked through `on_its_branch`.
- `survivor_check.py:1650-1653`, in `report`: *one owned by a work item the range touches nothing of never arrives*. In local mode that is one whose branch the tip is off.

The ledger's 0.15.1 U1 row was corrected for exactly this, and the two
docstring carriers of the same sentence were not. The behaviour is right.
Correct both to name the local-mode test.

### ⬜ 4 — When one key leaves two paths and arrives at one, the move's origin can be named as where it was corrected

`survivor_check.py:1140-1145`. Pairing takes removed sentences in path order,
so the first removed copy pairs with the arrival. Take a range that corrects
a sentence at `docs/a.md` and moves the identical sentence from `docs/m.md`
to `docs/z.md` (read, not probed):

- The copy at `docs/a.md` is paired and held.
- The copy at `docs/m.md` stays as the source.
- The report's `corrected` line then names `docs/m.md`, which moved the sentence and corrected nothing.

The survivor coordinate (`docs/z.md`) and the score are right, and only the
`corrected` pointer misleads. It could be fixed by preferring to pair a
removal at a path the range deleted whole. That is a heuristic, and it does
not cover a split.

### ⬜ 5 — Two prose carriers still spell the gathered fragment's path one way

- `survivor_check.py:856`: the `a_gathered_fragment` docstring reads *True for `seal/specs/<id>/changelog.md`*.
- `survivor_check.py:160`: the module docstring's released-section paragraph spells the same path.

The predicate accepts any `<x>/specs/<id>/changelog.md`, and G7 now pins the
second spelling as held. #564 ⬜5 is about there being two spellings of one
path. The code reads one now, and these two sentences still describe the
other. Behaviour is right.

### ⬜ 6 — `local_specs` restates `hooks/optin.py#git_common_dir`

`survivor_check.py:1353-1365` against `hooks/optin.py:99`. The plan's
technical context names `git_common_dir` as the existing reader of where
local mode lives. `survivor_check.py` already loads `hooks/routing.py` by
path, so the same loader would reach `optin.py`, which also carries the
Windows `normpath` handling that `local_specs` gets from `realpath` instead.
Also, `on_its_branch` executes `routing.py` afresh for every declaration it
is asked about. Both cost little, and both are a second copy of a rule that
has one home.

### ❓ — The settle fold's arrival in `docs/` is still written as the range's own

`survivor_check.py:1047-1050` removes a retired directory's paths before the
pairing at `:1115`. So a statement a fold carries verbatim from `spec.md`
into `docs/` has no removal to pair with, and it is written. That is #563's
shape for the one move member the pairing cannot see. Whether it matters
depends on whether a fold ever carries the old wording of a claim the same
range corrects. That was read and not measured. **Who answers it:** the
orchestrator, who decides whether it belongs to #563's class and needs a
home.

## Regression tests to plant

- `tests/test_a_corrected_sentence_survives_elsewhere.py`: O6, a stacked child's local declaration refused over its parent's range, with the reason naming the cut. It is in 🟡 1's fence.
- The same file: O4's third parameter, `unknown-branch`, plus the per-parameter reason assertion that replaces the fixed sentence. It is in 🟡 2's fence.

Both were seen red on `6e48cb5f` and green with the fixes, in the review clone.

## Facts for the evidence ledger

- `git rev-parse --git-common-dir` run from a subdirectory of a main worktree answers relative to that subdirectory (`../.git`, executed). So `local_specs`' join onto `root` is right for a `--root` below the top level too.
- `on_its_branch`'s ancestor test admits the ranges of every local branch the declared branch was cut from (executed; 🟡 1). Row O1's failure scenario in `seal/ledger/1790260564-a-moved-file-counts-as-written.md` names only the reused branch name. It needs the stacked case, or the fix.

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

## Paste-ready fixes

### 🟡 1 — `on_its_branch` refuses a stacked parent's range, and says why

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

### 🟡 2 — `whole_range` prints the reason `on_its_branch` returns

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

Needs a fix: yes — 🟡 1 (a stacked child's local declaration excuses its parent branch's run) and 🟡 2 (the local-mode `not yours` reason names a branch that `routing.md` does not name)
Loses a record or crashes: no


## Proof block

Files opened this round, all in the clone at `6e48cb5f` unless noted:
`seal/specs/1790260564-a-moved-file-counts-as-written/spec.md`, `plan.md`,
`routing.md`, `questions.md`, `overview.md` (diff), `changelog.md` (diff);
`seal/ledger/1790260564-a-moved-file-counts-as-written.md` (diff);
`skills/code-review/scripts/survivor_check.py` (lines 150-250, 330-1796, and
the diff); `tests/test_a_corrected_sentence_survives_elsewhere.py` (the diff,
helpers at 46-100, 444-460, 534-545, 1512, 1601-1618, and 3215-3235,
3625-3651); `hooks/routing.py` (111-215); `hooks/optin.py` (99-160);
`skills/verify/scripts/broad_gate.py` (1245-1246);
`skills/verify/scripts/unverified_check.py` (903-960, 1090-1130, 1195-1225);
`docs/review-chain-spec.md` (845-940, and the diff); `agents/smith.md`
(215-236, and the diff); `skills/code-review/orchestration.md` (the diff);
`seal/releases/*.md` (the word diff); `templates/sdd-routing.md` (the Branch
row); `tests/test_a_document_has_room_for_the_next_fold.py` (1-80);
`bin/test`, `bin/evidence-check`.
