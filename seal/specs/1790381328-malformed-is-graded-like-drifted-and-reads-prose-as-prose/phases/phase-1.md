# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 47f7c510 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Rule (a) reads prose as prose (#614), in `evidence_check.py` around
`refused_coordinate`: `PATH_HASH_RE` takes six or more hex characters;
`ISSUE_TAIL_RE` replaces `tail.isdigit()`; a dotless file name takes `_`, `"`
and `<` as locator openers; `GLUED_MARKS_RE`, searched, replaces
`"#" in s and "@" in s`; both docstrings state the rule and its trades. #614's
two functions with their eleven parameters, one function for the decorated
lines (`` `@lru_cache  # memoized` ``, `` `x = 1  # see @jane` ``), and one
guard parameter (`` `src/a.py#"x = 1  # c"@0` ``), each new case shown red with
the checker edit reverted and the guard green on both sides.

## What this phase found

- **No existing case changed verdict** (this work item's Q1). The row module
  went from 134 cases to 151 and every pre-existing case passed unchanged;
  the three other reader modules passed too (67, with
  `test_no_real_identifiers.py`). No prose shape an existing case pinned was
  refused, and no coordinate an existing case named went silent.
- **The guard the plan names does not guard the unit it is for.**
  `` `src/a.py#"x = 1  # c"@0` `` is named word by word through its path
  (`src/a.py#"x` is a `#` glued to a path) whether or not `GLUED_MARKS_RE`
  models a quoted string. The plan's alternatives table says the same of
  `#"a b"@0` ("no path for the per-word rule to catch"), and that is not
  right either: `#"a` is a path-less word opening with `"`, which the
  per-word rule names (probed: `refused_coordinate('#"a b"@0')` is true for
  that reason). Read, not executed: with only #614's cases and the guard, a
  mutant dropping the quoted-string alternative has nothing to turn red.
  The shapes only the quoted string names are path-less coordinates whose
  quoted locator holds a space and does not open the word. So three
  parameters joined the opener-list case, each green at 47e32d57 (the old
  both-marks rule named them) and each red under a mutant:
  `#handler>"a b"@abcdef12` (drop the quoted alternative),
  `#handler>"a \"b c\""@abcdef12` (drop the escape alternative, or the
  quoted one), and `see #handler>"a b"@abcdef12` (`.match` for `.search`).
  The guard parameter stays, and its docstring says it is a guard.
- **Every stated trade holds as `spec.md` states it**, probed through
  `refused_coordinate` directly: `src/a.py@abc`, `docs/a.md#1장`,
  `Makefile#1x` and `#handler @abcdef12` are silent;
  `src/a.py#f@abc`, `docs/a.md#1장@abcdef12`, `src/a.py#handler @abcdef12`,
  `org/repo@abcdef12`, `example.com/page#section` and a 40-character hash
  after a path are named.
- **The seal of each new case.** At a5c634bc's parent (47e32d57's checker),
  13 of the 13 new parameters of the three new functions failed and the 10
  opener-list parameters passed, the guard among them. Ten mutants of the
  added units, one at a time, each turned at least one case red:
  `PATH_HASH_RE`'s lower bound (3), `ISSUE_TAIL_RE` for `isdigit` (5), its
  lookahead anchored instead (5), each of the three openers (1 each),
  both-marks for glued marks (2), the quoted alternative (2), the escape
  (1), and `.match` for `.search` (1, after the last parameter joined).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the both-marks test `"#" in s and "@" in s` in `refused_coordinate` | `GLUED_MARKS_RE` in the same unit; `refused_coordinate`'s docstring states the path-less trade |
| `tail.isdigit()` as the issue-number test | `ISSUE_TAIL_RE` in the same unit |
