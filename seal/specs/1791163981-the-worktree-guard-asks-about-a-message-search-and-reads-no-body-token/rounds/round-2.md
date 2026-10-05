# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — review round 2

| Field | Value |
|---|---|
| Target SHA | 1eaccfc765b8641700df4d6683e15f4c819c23f0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #803 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `f659c46626e6e26b33a9af7e39e62a00315c3603..e3cd4dc46f0ede51eb5d24b0ad297703ad455cb4`, 2 commits |
| Contract changes | none |
| New units | test_a_guess_through_a_remote_whose_name_holds_a_space (depth 1) |
| Needs a fix | yes — 🟡 1 (a remote whose name holds a space is read as no remote by `_fetched_as`, and git guesses through it) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round over round 1's fixes (85e77dc8..22563bc6): round 1's probes re-run at the target, the base and 3a07c607; 🟡 3's base-only reading and `main`'s ordering judged by construction over command shapes, never quieter than the base; 🟡 2's refspec mapping over refspec and config shapes; 🟡 1's object lookup against names git refuses; how the M3 replay selected its pairs.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_fetched_as` splits each `git config --get-regexp` entry at its first space, so a remote whose name holds a space maps nothing while git guesses through it; the policy's "never the other way" and R5's "every remote" are false for it | `hooks/worktree-guard.py:1192` | **fixed** `8a92c8c2` | fixed at 8a92c8c2; executed: git created and switched, a3aa139a, 3a07c607 and 1eaccfc7 `None`, with a `-z` read `switch`, 11 other refspec shapes unchanged; the case red at 1eaccfc7 and green with the fix, module 419 passed |
| ⬜ 2 | A newly read checkout in a dirty second tree before a switch the base reads in a clean tree is silent (as at the base; 3a07c607 asked); §*Which tree* states the rule, §*Known limits* and the "keeps the first switch" paragraph do not | `docs/worktree-guard-spec.md:339` | **fixed** `8a92c8c2` | fixed at 8a92c8c2; executed through `main()` at three versions; no behaviour or fact wrong |
| ⬜ 3 | `main` runs the full `classify` after the base-only one, repeating its two calls, and runs it even after `newly_read` is set; 10 git calls where the base made 2 on an unresolvable name | `hooks/worktree-guard.py:2786` | answered | the extra git calls arise only for a `checkout` whose name nothing resolves, a bounded handful per segment; reordering the lookups would put new code into the last round's range to save a cost, not to fix a defect; executed: subprocess count 2 base-only, 8 full |
| ⬜ 4 | `test_a_newly_read_checkout_in_front_takes_no_question_away` says "Red at `85e77dc8`", and its two `:/nomatch` cases pass there | `tests/test_guard_resolves_the_tree_it_judges.py:2412` | **fixed** `8a92c8c2` | fixed at 8a92c8c2; executed: 2 failed, 2 passed with 85e77dc8's guard |
| 🟢 | round 1's 🟡 1 is closed: a message search holding `..` reads as a switch, and the object lookup adds no yes git refuses across 12 non-commit and ambiguous names | `hooks/worktree-guard.py:1072` | confirmed | executed at three versions against git's own checkout |
| 🟢 | round 1's 🟡 2 is closed for its two shapes and eight more (negative, multi-line, middle `*`, mirror, include, `/` in the name, no destination, legacy file); the one shape it misses is 🟡 1 above | `hooks/worktree-guard.py:1173` | confirmed | executed at three versions against git's own checkout |
| 🟢 | round 1's 🟡 3 is closed: round 1's probe is `ask` again, and no command of 31 is quieter than a3aa139a | `hooks/worktree-guard.py:2801` | confirmed | constructed path by path; executed through `main()` at three versions |
| 🟢 | `classify(..., base_only=True)` is a3aa139a's `classify`, so a command with no newly read checkout reads exactly as at a3aa139a and 3a07c607 | `hooks/worktree-guard.py:1302` | confirmed | read: the function's diff against the base; executed: 8 such commands unchanged at three versions |
| 🟢 | round 1's ⬜ 4 stays answered | `hooks/worktree-guard.py:831` | confirmed | read; the fix range touches no shadowing function |
| ❓ | The M3 replay's 581 and 1,044 pairs, and how they were selected | `phases/phase-4.md` | ❓ out of verified scope | the probe was deleted; by construction the corpus holds no shape the reorder touches, so its 0 tests nothing about the reorder; the smith answers the counts |

## Paste-ready fixes

```diff
--- a/hooks/worktree-guard.py
+++ b/hooks/worktree-guard.py
@@ def _fetched_as(name: str, cwd: str) -> set:
     `remote.<remote>.fetch` refspec, as git's checkout guess maps it: an
     exact source names its destination, a source with one `*` matches what it
     stands for and puts it in place of the destination's `*`, and a refspec
-    with no `:` maps nothing (a negative refspec has none)."""
+    with no `:` maps nothing (a negative refspec has none). The entries are
+    read NUL-separated, because a remote's name can hold a space that `git
+    remote add` refuses and git's fetch and guess still read (round 2 of
+    1791163981)."""
     try:
         r = subprocess.run(
-            ["git", "config", "--get-regexp", r"^remote\..*\.fetch$"],
+            ["git", "config", "-z", "--get-regexp", r"^remote\..*\.fetch$"],
             cwd=cwd or None,
             capture_output=True,
             encoding="utf-8",
             errors="replace",
         )
     except Exception:
         return set()
     source = "refs/heads/" + name
     mapped = set()
-    for line in r.stdout.splitlines():
-        spec = line.partition(" ")[2].strip().lstrip("+")
+    for entry in r.stdout.split("\0"):
+        spec = entry.partition("\n")[2].strip().lstrip("+")
         src, colon, dst = spec.partition(":")
```
```python
def test_a_guess_through_a_remote_whose_name_holds_a_space(tmp_path):
    """Round 2 of 1791163981, 🟡 1. `git remote add` refuses a name holding a
    space, but git fetches and guesses through one the config names, and
    `git config --get-regexp` prints that key with the space in it, so a map
    split at the first space read no refspec. Red at `1eaccfc7`."""
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
    _git(d, "config", "remote.a b.url", str(bare))
    _git(d, "config", "remote.a b.fetch", "+refs/heads/*:refs/spaced/*")
    _git(d, "fetch", "-q", "a b")
    assert _where_git_checkout_lands(d, "onfork")
    for carrier in ("checkout N", "checkout N --"):
        tokens = ["git", *CARRIERS[carrier]("onfork")]
        assert wg.classify(tokens, str(d)) == "switch", carrier
```
```text
so it guesses where git would not, and the other way only for a remote whose
name holds a space, which `git remote add` refuses and a config can still
name.
```
```text
- A `checkout` only #790's lookups read as a switch is judged only where the
  frozen reading read no switch in the command (§*Which tree*), so one in a
  second tree, written before a switch the frozen reading reads, goes unasked
  as it did at the base. Judging it first instead took the question from the
  frozen reading's switch, which the base asked (round 1 of 1791163981, 🟡 3).
```
```diff
--- a/hooks/worktree-guard.py
+++ b/hooks/worktree-guard.py
@@ def main():
             found = classify(tokens, here, base_only=True)
             if not found and not creates:
-                found = classify(tokens, here)
-                if found and newly_read is None:
-                    newly_read = (found, target)
+                if newly_read is None:
+                    found = classify(tokens, here)
+                    if found:
+                        newly_read = (found, target)
                 continue
```

## Executed probes

| What was run | Result |
|---|---|
| The five narrow modules at 1eaccfc7 in the clone | 599 passed, 1 skipped |
| Round 1's fix cases with 85e77dc8's guard put back in the clone | 11 failed, 3 passed: the two `:/nomatch` controls and the first-newly-read case, whose docstring claims only a mutation red |
| Round 1's two-dots probe through `classify` at three versions | git detaches; a3aa139a and 3a07c607 `None`; 1eaccfc7 `switch` |
| 12 fetch-refspec shapes through `classify` at three versions, against git's own `checkout` | 9 that git lands on read `switch` at 1eaccfc7 and `None` before; 2 git refuses read `None` everywhere; the spaced remote `None` everywhere (🟡 1) |
| 12 object-name shapes through `classify` at three versions | git refuses 11, all `None`; the tag on a commit lands and reads `switch` everywhere |
| `main()` over 31 command shapes at three versions, the choose state kept apart per version | no target row quieter than a3aa139a; two quieter than 3a07c607 (⬜ 2); the 8 rows with no newly read checkout identical at all three |
| A `-z` read of the fetch config over the 12 refspec shapes | the spaced remote moves to `switch`; no other answer moves |
| A fetch refspec given only with `-c` | git refuses the guess; `classify` `None` |
| The 🟡 1 case planted in the clone, then the fix, then the module | red at 1eaccfc7; with the fix, module 419 passed; both reverted |
| Subprocesses one `classify` spawns for an unresolvable `checkout` name | 2 base-only, 8 full |
| `bin/evidence-check --strict .` in the worktree, with this report on disk | exit 0 |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |
