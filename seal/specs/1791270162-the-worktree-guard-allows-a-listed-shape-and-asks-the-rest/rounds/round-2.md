# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — review round 2

| Field | Value |
|---|---|
| Target SHA | 274e29bb4101086a6f66cb945238e3c1b63b2131 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #850 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `3c9a11617fe794c8420dbbf920d8a67179f2c9db..a3164380d609e568dbeee219247bd60150284918`, 7 commits |
| Contract changes | stop_unrecognised → main, round-1-report.md, round-1.md, round-2-report.md, spec.md |
| New units | TREES_EN (depth 1); TREES_KO (depth 1); test_the_stop_names_each_tree_that_matters_in_both_languages (depth 1); CUT_GROUPS (depth 1); test_a_cut_group_is_judged_in_the_tree_its_own_c_names (depth 1); test_a_broken_reader_judges_a_cut_in_the_tree_before_it (depth 1) |
| Fix of a fix | first — 🔴 1 at hooks/worktree-guard.py#_rebase_names_a_branch, a unit round-1's fixes added; 🔴 2 at hooks/worktree-guard.py#main, a unit round-1's fixes changed; 🟡 3 at hooks/worktree-guard.py#_cut_unread, a unit round-1's fixes added; 🟡 4 at hooks/worktree-guard.py#main, a unit round-1's fixes changed |
| Needs a fix | yes — 🔴 1, 🔴 2, 🟡 3 and 🟡 4: `git rebase - <branch>` switches while listed, a git cut by an `&` is judged in the tree of its last part and so is silent over an ACTIVE `-C` tree, the broken-reader path places a cut the same way, and the stop hides an IDLE or unreadable second tree behind the first tree's changes |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #826, the verifying round for round 1's fixes at `4de95fa7..5ba5e51a`, at 274e29bb. The reviewer was asked to open each fix and judge whether it closes its class. It was also asked to treat round 1's `New units` as a finding surface: `_OPERATORS`, `_rebase_names_a_branch`, `_cut_unread`, `FORMS`, `SWITCHING`, the git-binding case and the new cases. In particular it judged:
- the cost and the reason text of reading every tree on the line;
- `_OPERATORS` against bash's redirection grammar, `<<<-` and `<>-` included;
- `_rebase_names_a_branch` against forms with options before the upstream;
- the git-binding case's spawn cost.

It also read every workflow of `gh pr checks 850`, and it did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `_rebase_names_a_branch` drops a lone `-`, so `git rebase - feature/x`, which git runs as a switch to `feature/x`, is listed and silent in an ACTIVE tree | `hooks/worktree-guard.py:2235` | **fixed** `6b4bcec5` | fixed at 6b4bcec5 — `_rebase_names_a_branch` counts a lone `-` and every word after `--` as a revision; `@{-N}` already counted; six rebase rows, three listed rows and a `SWITCHING` form added; executed: HEAD moved under git 2.50.1; the build silent in an ACTIVE tree; the base silent too |
| 🔴 2 | a git cut by an `&` is placed by its last part's tokens, so `2>&1 git -C W switch feature/x` and `git -C W worktree &>/dev/null add ../wt b` are silent with `W` ACTIVE | `hooks/worktree-guard.py:2941` | **fixed** `8cd9fea6` | fixed at 8cd9fea6 — `_merged_findings` returns the cut's first part and its glued tokens, and `main` places the tree from the first part's directory with them; nine `CUT_GROUPS` rows; executed against the build and the base: silent where the base asked; a regression |
| 🟡 3 | `_cut_unread` places a cut by the later part, so with the reader missing `git -C W worktree 2>&1 add ../wt b` is silent with `W` dirty | `hooks/worktree-guard.py:2393` | **fixed** `f117ccfb` | fixed at f117ccfb — `_cut_unread` places a broken reader's cut by the part before it; a `-C` after the cut is named in §Known limits and pinned; executed: silent; the trial fix asks |
| 🟡 4 | the stop describes the first tree that matters unless a later one is ACTIVE, so an IDLE or unreadable second tree is never shown in the `ask` | `hooks/worktree-guard.py:2981` | **fixed** `53e0c547` | fixed at 53e0c547 — the stop names every tree that matters with its own reason, or the ACTIVE ones alone; English and Korean texts pinned; executed: the IDLE and unreadable rows name only the session tree's changes; the new case pins that text |
| ⬜ 5 | the git-binding case passes a `FORMS` row git refused, since it checks no return code | `tests/test_worktree_guard.py:1772` | **fixed** `6e93ff94` | fixed at 6e93ff94 — the git-binding case asserts every git it runs exited as expected; executed: every form ran under git 2.50.1; a refusal elsewhere would pass unmeasured |
| ⬜ 6 | `spec.md` Data & interfaces gives `stop_unrecognised` its pre-round-1 signature | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md:312` | answered | corrected at 503dfa60 — `spec.md` Data & interfaces gives `stop_unrecognised`'s current signature, and In 1, In 2 and In 4 take round 2's fixes back, each marked inferred; read; a paperwork correction, not counted in `Needs a fix` |
| 🟢 | round 1's blocking finding 1 is closed — a switch beside the stop, or an ACTIVE second tree, makes the stop a deny | `hooks/worktree-guard.py:2775` | confirmed | executed: the new case passes, and the probe's ACTIVE-second-tree row denies |
| 🟢 | round 1's blocking finding 2 is closed — a closed, moved or `-`-named target takes no next word | `hooks/worktree-guard.py:2155` | confirmed | executed: eight forms under bash, each a creation or a switch, ask in a dirty tree and deny in an ACTIVE one |
| 🟢 | round 1's blocking finding 3 is closed for the three forms it named | `hooks/worktree-guard.py:2226` | confirmed | executed through the new cases; the lone `-` is 🔴 1 of this round |
| 🟢 | round 1's finding 4 is closed for the four rows it measured | `hooks/worktree-guard.py:2383` | confirmed | executed through the new case; the `-C` placement is 🟡 3 of this round |
| 🟢 | round 1's finding 5 is closed — a string's `-C` is named in §*Known limits* and §A | `docs/worktree-guard-spec.md` | confirmed | read; pinned by `test_the_guard_policy_says_nothing_is_read_past_the_base` |
| 🟢 | round 1's notes 6 and 7 are closed — the module comment and the `branch` clause | `hooks/worktree-guard.py:157` | confirmed | read; ledger row F6 carries the `branch -m` fact |
| 🟢 | reading every tree before the stop costs one read per distinct tree on the line, and nothing more | `hooks/worktree-guard.py:2971` | confirmed | read; `placed` and `seen` bound it, and the early exit's removal at `d594eb81` costs only reads that change nothing |
| 🟢 | `_OPERATORS` follows bash for `<<<-`, `<>-`, `>-` and the spaced `>& -`, `<& -`, `2>& 1-` | `hooks/worktree-guard.py:2155` | confirmed | executed under bash; `<<-` correctly keeps its delimiter |
| ❓ | the git-binding case's cost on the Windows shards | `tests/test_worktree_guard.py:1772` | ❓ out of verified scope | 2.80 s on macOS under xdist (executed); 56 copies and about 62 git processes; the Windows shards were pending; the orchestrator reads the durations when they finish |
| ❓ | five of #850's pytest workflows at 274e29bb: macOS and Windows shards 1, 3 and 4 | `gh pr checks 850` | ❓ out of verified scope | pending at the end of the round; `lint`, `ledger`, both `arm-check-grammar` legs, `release`, Ubuntu and Windows shard 2 passed; the orchestrator reads them again before the next round |

## Paste-ready fixes

```python
# hooks/worktree-guard.py, _rebase_names_a_branch: git reads a lone `-` as
# `@{-1}`, so it is a word that can name the upstream (`git rebase -
# feature/x` switches to feature/x; git 2.50.1, round 2 of 1791270162).
    plain = [w for w in _plain_words(args) if w == "-" or not w.startswith("-")]
    return len(plain) >= (1 if "--root" in args else 2)
```
```python
# tests/test_worktree_guard.py, test_a_rebase_naming_a_branch_is_unrecognised:
# two more parameters.
        "git rebase - feature/x",
        "git rebase -i - feature/x",
```
```markdown
seal/ledger/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest.md,
row F3, the claim's first clause becomes:

a `rebase` with two words that are not options, a lone `-` counted as a
word, or `--root` and one, is unrecognised
```
```python
# hooks/worktree-guard.py, _merged_findings: each finding carries the group's
# own words and its first part, so main judges the group in the tree its
# `-C` names rather than the tree of its last part.
                if finding is not None:
                    out.append((parts[-1], finding, toks, parts[0]))
                continue
            if _wide_git(toks):
                out.append(
                    (parts[-1], Finding("hidden", _spoken(toks)), toks, parts[0])
                )

# hooks/worktree-guard.py, _first_finding_in:
    for _index, finding, _toks, _first in _merged_findings(items):
        return finding

# hooks/worktree-guard.py, main:
    for index, finding, toks, first in _merged_findings(items):
        wheres = walked[first][1]
        unrecognised.append((index, finding, toks, wheres[0] if wheres else cwd))
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py, _read_by_the_guard:
    found += [merged[1] for merged in wg._merged_findings(items)]
```
```python
# tests/test_worktree_guard.py
def test_a_cut_group_is_judged_in_the_tree_its_own_c_names(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of work item 1791270162, red 2. A git an `&` cut was judged
    in the tree of the group's last part, which carries no `-C`: silent at
    274e29bb with W ACTIVE, where the base asked."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    monkeypatch.setattr(
        wg,
        "sessions_in_tree",
        lambda top, own="": (ACTIVE, [], True) if top.endswith("W") else ([], [], True),
    )
    for command in (
        f"2>&1 git -C {w} switch feature/x",
        f"git -C {w} worktree &>/dev/null add ../wt b",
        f"git -C {w} stash &>/dev/null branch y",
    ):
        assert verdict(monkeypatch, capsys, repo, command)[0] == "deny", command
```
```python
# hooks/worktree-guard.py, _cut_unread: hand back the part before the cut,
# where the frozen reading finds a `-C` (`git -C W worktree 2>&1 add …`).
            if _holds_git(text):
                before = items[index - 1][1]
                out.append((index, Finding("unread", text), before, index - 1))
```
```python
# tests/test_worktree_guard.py
def test_a_broken_reader_judges_a_cut_in_the_tree_its_c_names(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of work item 1791270162, yellow 3. Silent at 274e29bb."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    (w / "f.txt").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(wg, "wide", None)
    command = f"git -C {w} worktree 2>&1 add ../wt b"
    assert verdict(monkeypatch, capsys, repo, command)[0] == "ask", command
```
```markdown
docs/worktree-guard-spec.md §Known limits, after the string bullet:

- Where `hooks/cmdline.py` did not load, a git an `&` cut is judged in the
  tree the part before the cut names: `git -C W worktree 2>&1 add …` is
  judged in `W`, and `2>&1 git -C W switch x`, whose `-C` comes after the
  cut, in the tree it was typed from.
```
```python
# hooks/worktree-guard.py, beside stop_unrecognised:
def _weight(state):
    """How much STATE, `(active, idle, reliable, entries)`, says, by §A's
    rows: an ACTIVE session over an IDLE one, over detection unusable, over
    tracked changes. The stop describes the tree that says the most."""
    active, idle, reliable, _entries = state
    return 3 if active else 2 if idle else 1 if not reliable else 0


# hooks/worktree-guard.py, main, the tree loop:
            here_state = (active, idle, reliable, entries)
            if matters and (state is None or _weight(here_state) > _weight(state)):
                state = here_state
```
```python
# tests/test_worktree_guard.py, test_no_approval_runs_a_line_past_an_active_tree,
# the IDLE half of the second loop becomes:
            else:
                assert decision == "ask", (command, decision, reason)
                assert "none of them can be shown to be working" in reason, reason
```
```markdown
docs/worktree-guard-spec.md §A, after "Every tree on the line is read
before the stop is taken, …":

The stop's reason describes the tree that says the most: an ACTIVE session,
then an IDLE one, then detection unusable, then tracked changes.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py -q --durations=8` in the round's clone at 274e29bb | 222 passed; `test_no_listed_form_moves_head_under_git` 2.80 s, `test_no_approval_runs_a_line_past_an_active_tree` 1.16 s |
| a deleted `test_tmp_*` probe driving bash and git 2.50.1 in copies of the `repo` fixture | the bash table above; `git rebase - feature/x` moved HEAD; every `FORMS` row ran, `check-ignore` with exit 1 |
| the same probe loading 274e29bb's guard and the base's (`git show 86cbd9a2:hooks/worktree-guard.py`, kept outside `hooks/`; the four readers it imports are unchanged since the base), with `sessions_in_tree` stubbed per tree | the build and base columns of 🔴 2; the reason texts of 🟡 4; the shapes of the option forms |
| the paste-ready fixes below applied in the clone, the probe rerun, then `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_the_guard_asks_once_per_session.py -q` | every probe row as each fix's section says; 299 passed, 1 failed: `test_no_approval_runs_a_line_past_an_active_tree`'s IDLE assertion, the text 🟡 4 changes. The clone was reverted and the probe deleted afterwards |
| `gh pr checks 850`, three times | first read: `lint` passed, the rest pending. Second read: `lint`, `ledger`, `arm-check-grammar (3.13)`, `arm-check-grammar (3.14)` and `release` passed, the seven pytest legs pending. Third read: `pytest (ubuntu-latest, 3.12, 15)` and the Windows shard `--group 2` passed too; macOS and Windows shards 1, 3 and 4 pending. No job log can be read until the run ends, so no Windows duration was seen. The previous head's `tests` run (edd35c56) concluded success |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. It is not due while 🔴 1, 🔴 2, 🟡 3 and 🟡 4 are open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:2699` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/worktree-guard.py:2161` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2086` | round 1's 🔴 3 — fixed |
| round-1 | `hooks/worktree-guard.py:2321` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree-guard.py:2397` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/worktree-guard.py:157` | round 1's ⬜ 6 — fixed |
| round-1 | `hooks/worktree-guard.py:2056` | round 1's ⬜ 7 — fixed |
| round-1 | `hooks/worktree-guard.py:2878` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | round 1's 🟢 — confirmed |
| round-1 | `docs/worktree-guard-spec.md` | round 1's 🟢 — confirmed |
| round-1 | `gh pr checks 850` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| P5 — whether an unrecognised shape in an ACTIVE tree is denied whatever the press | `questions.md` P5, already deferred in round 1 | the repository owner, at the pull request |
