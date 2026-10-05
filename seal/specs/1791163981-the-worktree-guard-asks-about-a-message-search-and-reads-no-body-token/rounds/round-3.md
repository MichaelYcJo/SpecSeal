# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — review round 3

| Field | Value |
|---|---|
| Target SHA | 61e59b4277e659e0707174c19f4e3bc337e56e52 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #803 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `92aeaebbbdbcf65b102eef3b636767e5e2ced2ed..92aeaebbbdbcf65b102eef3b636767e5e2ced2ed`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a refspec destination ending in a Unicode space or line separator is read as a ref that does not exist, in `_fetched_as` and `_refs`; not a regression against a3aa139a) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round over round 2's fixes (f659c466..e3cd4dc4), and the last round this item gets: rounds 1–2's verdicts inherited and checked; `_fetched_as`'s `-z` parsing judged by construction over the key and value shapes git allows; the two new policy sentences and their pins against `main`; the M3 replay's stated selection rule; one whole-item never-quieter pass through `main()` at the base and the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A fetch refspec whose destination ends in a Unicode space or line separator maps to a ref that does not exist: `_fetched_as` strips the value with `str.strip()` and `_refs` splits ref names with `str.splitlines()`, both at characters git keeps in a ref name, so git guesses and the guard is silent; "never the other way" and R5 are false for it. Not a regression: a3aa139a is silent too | `hooks/worktree-guard.py:1195` | deferred #811 | #811 — the run is capped; fixed post-review on this branch, and #811 is what that fix closes; executed: git lands on U+00A0, U+3000 and U+0085, and three versions answer `None`; the case is red at 61e59b42 (4 failed) and the module passes 423 with the two-line fix; 26 config shapes re-run with the fix, none git lands on reads less |
| ⬜ 2 | The replay paragraph says no recorded command holds a newly read `checkout`, without the gone-directory bound the paragraph above it states (449 of 972 pairs) | `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/phases/phase-4.md:63` | deferred #811 | #811 — the replay paragraph's bound goes in with the same post-review fix; executed: 0 of 982 readings newly read at 61e59b42, 449 pairs' directories gone; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | round 2's 🟡 1 is closed — a remote whose name holds a space maps its refspec | `hooks/worktree-guard.py:1184` | confirmed | executed at three versions against git's own `checkout`, with 15 further key and value shapes; the case is red with f659c466's guard |
| 🟢 | round 2's ⬜ 2 is closed — the walk's paragraph and §*Known limits* state the placement limit, and both are pinned | `docs/worktree-guard-spec.md:340` | confirmed | executed: the pin is red against f659c466's policy; the described shape is silent at a3aa139a, 1eaccfc7 and 61e59b42 in five spellings |
| 🟢 | round 2's ⬜ 3 stays answered — the fix range does not touch `main` | `hooks/worktree-guard.py:2791` | confirmed | read: the fix range's one `hooks/` hunk is in `_fetched_as` |
| 🟢 | round 2's ⬜ 4 is closed — the docstring names which two cases were red | `tests/test_guard_resolves_the_tree_it_judges.py:2424` | confirmed | read, against round 2's executed 2 failed and 2 passed at 85e77dc8 |
| 🟢 | round 2's ❓ is answered — the replay's selection rule reproduces 581 of 25,741 and 1,044 of 36,937 | `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/phases/phase-4.md:49` | confirmed | executed over the 635 transcripts; cut 2's pair of figures holds at one moment inside round 1's fix pass |
| 🟢 | no shape is quieter at 61e59b42 than at a3aa139a — whole-item pass | `hooks/worktree-guard.py:2778` | confirmed | executed: 116 runs through `main()` at three versions, 0 quieter; 26 config shapes through `classify`, none quieter |

## Paste-ready fixes

```diff
--- a/hooks/worktree-guard.py
+++ b/hooks/worktree-guard.py
@@ def _refs(patterns, cwd: str):
     except Exception:
         return []
-    return r.stdout.splitlines()
+    # A ref name holds no newline, and may hold U+0085, U+2028 or U+2029,
+    # which `splitlines` also splits at (round 3 of 1791163981).
+    return r.stdout.split("\n")
@@ def _fetched_as(name: str, cwd: str) -> set:
     source = "refs/heads/" + name
     mapped = set()
     for entry in r.stdout.split("\0"):
-        spec = entry.partition("\n")[2].strip().lstrip("+")
+        # No strip: git's reader has already taken the ASCII whitespace off,
+        # and a ref name may end in a Unicode space `str.strip` would remove
+        # (round 3 of 1791163981).
+        spec = entry.partition("\n")[2].lstrip("+")
         src, colon, dst = spec.partition(":")
```
```python
@pytest.mark.parametrize(
    "space",
    ["\u00a0", "\u3000", "\u0085", "\u2028"],
    ids=["nbsp", "ideographic", "nel", "line separator"],
)
def test_a_guess_through_a_destination_ending_in_unicode_whitespace(tmp_path, space):
    """Round 3 of 1791163981. git's config reader strips only ASCII
    whitespace, so a fetch refspec whose destination ends in another space
    character fetches into a ref that ends in it, and git guesses through
    that ref. A map that ran `str.strip()` over the value, or split the ref
    list with `str.splitlines()`, read a ref that does not exist. Red at
    `61e59b42`."""
    bare = tmp_path / "f.git"
    subprocess.run(
        ["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True
    )
    d = tmp_path / "r"
    _a_repository(d)
    _commit(d, "README.md", "initial commit")
    _git(d, "branch", "onfork")
    _git(d, "push", "-q", str(bare), "onfork")
    _git(d, "branch", "-D", "onfork")
    _git(d, "config", "remote.fork.url", str(bare))
    _git(d, "config", "remote.fork.fetch", "+refs/heads/*:refs/ws/*" + space)
    _git(d, "fetch", "-q", "fork")
    assert _where_git_checkout_lands(d, "onfork")
    for carrier in ("checkout N", "checkout N --"):
        tokens = ["git", *CARRIERS[carrier]("onfork")]
        assert wg.classify(tokens, str(d)) == "switch", carrier
```
```text
nothing more: no recorded command holds a `checkout` that only #790's lookups
read, of the pairs whose directory still exists (449 of the 972 `checkout`
pairs up to the fix pass name one that is gone, where neither reading finds a
ref; counted at round 3), so the replay never reached the reordering in
`main` that round 1's 🟡 3 added.
```

## Executed probes

| What was run | Result |
|---|---|
| The five narrow modules at 61e59b42 in the clone | 600 passed, 1 skipped (the orchestrator's 712 includes the hygiene modules) |
| 26 fetch-config shapes through `classify` at a3aa139a, 1eaccfc7 and 61e59b42, against git's own `checkout` | 17 git lands on: 61e59b42 `switch` on all 17; 1eaccfc7 `None` on the two spaced remotes; a3aa139a `None` on all. 9 git refuses: `None` or the louder `switch` |
| A newline in a config key, through `git config` and through a hand-written file | refused by `git config`; a fatal parse error for every git command |
| A refspec destination ending in U+00A0, U+3000 or U+0085, and the same at the front | trailing: git lands, all three versions `None` (🟡 1); leading: git refuses, all `None` |
| The 🟡 1 case planted in the clone, at 61e59b42, with the `.strip()` dropped, then with both lines | 4 failed; U+0085 still red; module 423 passed. Reverted with the clone |
| The 26 config shapes through the two-line fix | none git lands on reads less; two shapes git refuses move from `switch` to `None` |
| `test_a_guess_through_a_remote_whose_name_holds_a_space` with f659c466's guard | failed on `checkout N`, `None == 'switch'` |
| `test_the_guard_policy_says_what_it_reads_past_the_base` against f659c466's policy text | failed on the first round 2 assertion |
| `main()` over 29 shapes × 4 session states at three versions, a fresh repository per run | 0 of 116 quieter than a3aa139a; 61e59b42 equals 1eaccfc7 except R13, louder |
| The M3 replay's selection rule re-derived from 635 transcripts | cut 1: 25,913 uses, 25,741 pairs, 581 selected; 36,937 pairs and 1,044 selected at 2026-10-05T12:01:21+09:00 |
| The 972 recorded `checkout` pairs up to the fix pass, each segment through `classify` with and without `base_only` at 61e59b42 | 0 of 982 readings newly read; 449 pairs name a directory that is gone |
| `bin/evidence-check --strict .` in the worktree, with this report on disk | exit 0; 5,670 ok, 0 drifted, 0 broken; records: 0 refused |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this round ran none of it, and the sealer answers it once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:1044` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/worktree-guard.py:1101` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2699` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/worktree-guard.py:162` | round 1's ⬜ 4 — answered |
| round-1 | `hooks/worktree-guard.py:1084` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:755` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/cmdline_base.py` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py:1395` | round 1's 🟢 — confirmed |
| round-1 | `phases/phase-1.md`; `hooks/worktree-guard.py:1084` | round 1's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:1192` | round 2's 🟡 1 — fixed |
| round-2 | `docs/worktree-guard-spec.md:339` | round 2's ⬜ 2 — fixed |
| round-2 | `hooks/worktree-guard.py:2786` | round 2's ⬜ 3 — answered |
| round-2 | `tests/test_guard_resolves_the_tree_it_judges.py:2412` | round 2's ⬜ 4 — fixed |
| round-2 | `hooks/worktree-guard.py:1072` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:1173` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2801` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:1302` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:831` | round 2's 🟢 — confirmed |
| round-2 | `phases/phase-4.md` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |
