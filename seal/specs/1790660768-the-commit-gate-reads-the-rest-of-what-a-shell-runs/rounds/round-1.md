# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — review round 1

| Field | Value |
|---|---|
| Target SHA | befe53cdfe8a5810d7563fb8f6e3c0ba8aa97303 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #679 — https://github.com/MichaelYcJo/SpecSeal/pull/679 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `3b8522c38d4e400dab57eb86e70ec928ce1490ef..cd4a65d7529d92bd935f528659a7f1e5503982dc`, 8 commits |
| Contract changes | _segment_names_an_unknown_command → names_an_unknown_command, round-1-report.md, round-1.md; understood → _unreadable_past_leading_redirections, walk_directories, round-1-report.md, round-1.md, pytest |
| New units | unglued (depth 1); HEADERS_READ (depth 1); STILL_UNREAD (depth 1); test_a_shape_both_shas_read_as_no_commit_is_read (depth 1); UNSEEN_CD (depth 1); test_a_cd_the_walk_did_not_see_stops (depth 1); W1_PREFIXES (depth 1); test_w1_keeps_the_directory_the_base_judged_under_a_waiver (depth 1); test_w1_keeps_the_directory_a_parked_failure_came_from (depth 1); test_w1_keeps_the_directory_the_base_judged_outside_an_opted_in_session (depth 1); test_past_the_header_bound_the_reading_stops (depth 1); test_a_deep_header_nesting_keeps_the_commits_found (depth 1) |
| Needs a fix | yes — 🔴 1 (W1 replaces the directory the base judged, in the commit gate, the guard and the consent writer), 🔴 2 (the header readings recurse with no bound and drop the commits found), 🟡 3 (a `cd` behind a cut redirection), 🟡 4 (a redirection glued to a word's end), 🟡 5 (zsh's precommand words and short loop), 🟡 6 (a shell's string past `--` or an option behind a redirection) |
| Loses a record or crashes | yes — 🔴 1: at `befe53cd` the consent writer files a worktree creation made in a nested clone under the session's own clone, so the creation's own clone gets no record and the session's clone gets one nobody gave. 🔴 2 raises `RecursionError` out of the reader; `main` catches it and drops the commits found |

- [x] Pass

## What this round was asked

Round 1 over the branch `86256492..befe53cd`, complete, replacing a partial report that was cut off when the previous session ended (posted on #680, unverified). Asked the reviewer to re-execute each of the partial's six findings with its own probes: 🔴 1 W1's refusal replacing the base's directory, 🔴 2 the unbounded header recursion, and 🟡 3–6, which are silent at both SHAs while a real shell commits. Also asked it to run the partial's paste-ready fixes and write fixes for 🟡 3–6, and to cover what the partial did not: tests seen red, depth timing, the guard, consent, the notice, the docs, the ledger and changelog fragments, and the invariant over the recorded corpus.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | W1's refusal replaces the directory the base judged instead of adding one beside it, so a `[no-review]` over a parity arm, a session that is not opted in, the worktree guard's dirty-tree question and the consent record each lose what the base had | `hooks/cmdline.py#walk_directories`, `hooks/cmdline.py#understood` | **fixed** `502fce6a` | fixed at 502fce6a — with `b2cdab15`, `98a39af7` and `cd4a65d7`: the walk adds W1's `Unresolved(CONSTRUCT)` beside the directory it read without the redirection, and the moved shell, the parked failure and the three name-environment branches read that as-written answer; `understood` takes a `redirections` flag; the policy sentence says added beside. Red at 3b8522c3: the 10 waiver prefixes, the 4 not-opted-in shapes and a parked-failure case. The guard and `creation_directory` match 86256492 again; Executed through `main()`: 4,125 of 8,640 corpus commands the base stops are silent at head, and 0 with the fix. The guard is silent where the base asked on 4 switches, and the consent directory moves from `S/w` to `S`. bash commits. The `env` half was shown needed by a mutant |
| 🔴 2 | The header readings recurse once per header, so 1,200 nested headers raise past `_hides_a_commit` into `main`, which drops the commits found | `hooks/cmdline.py#_is_the_program`, `hooks/cmdline.py#_segment_names_an_unknown_command` | **fixed** `502fce6a` | fixed at 502fce6a — `_is_the_program` and `_segment_names_an_unknown_command` are loops bounded at `HEADERS_READ = 32` that answer in the stopping direction past it; the three 1,200-level cases red at 3b8522c3; a case pins 31 read and 32 stopped; Executed through `main()`: five shapes deny at base and are silent at head at 1,200 and 3,000 levels. The partial's unbounded loop is quadratic, 46.8 s on 10,000. The bounded loop takes 5.0 s |
| 🟡 3 | A `cd` behind a redirection the splitter cut is not read by the walk | `hooks/cmdline.py#walk_directories` | **fixed** `f2adb13d` | fixed at f2adb13d — the walk also asks the group `merged_view` glues back; 6 cd shapes red at 3b8522c3; 8 shapes silent at both SHAs from a declared session. bash and zsh commit in `U` |
| 🟡 4 | A redirection glued to the end of a word hides the program, the subcommand or a `cd` | `hooks/cmdline.py#_REDIRECTION` | **fixed** `f2adb13d` | fixed at f2adb13d — with `7344d127`: `unglued` cuts a redirection off a word's end into a view read beside the segment, `merged_view` reads an operator glued to a word's end, and the walk refuses a glued `cd`; 13 shapes red at 3b8522c3, nine mutants killed; 15 shapes silent at both SHAs. bash commits all 12 it was given, and zsh 3 |
| 🟡 5 | zsh's `noglob`, `nocorrect`, `repeat N` and `for i (…) cmd` hide the program or a `cd` | `hooks/cmdline.py#RUNNERS` | **fixed** `f2adb13d` | fixed at f2adb13d — `noglob`, `nocorrect` and `repeat` are runners and zsh's short `for` is read past; 10 shapes red at 3b8522c3; `for d in git commit; do :; done` stays silent; 11 shapes silent at both SHAs. zsh 5.9 commits all seven commit shapes |
| 🟡 6 | A shell's string is not found past `--` or an option behind a redirection after `-c` | `hooks/cmdline.py#command_strings` | **fixed** `f2adb13d` | fixed at f2adb13d — a shell's string is found past the options and `--` behind a redirection after `-c`; 5 shapes red at 3b8522c3; 5 shapes silent at both SHAs. bash commits all five |
| ⬜ 7 | `evidence-check` exits 2 at head on two refused names in this item's records | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md:43` | answered | `30c2899a` — NAME NOT IN TREE on `questions.md` Q1 and `phases/phase-6.md`'s removal row; 0 refused; Executed at `befe53cd`: 2 refused, lenient exit 2. The second is `phases/phase-6.md:167`. A correction to the run's paperwork, and it turns CI's `test.yml` red |
| ⬜ 8 | Five records state W1 as a replacement or say nothing was lost | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` | answered | `cbcc8acc` — corrected in place with dated notes: the spec's guard section, ledger I2 and I10, the changelog fragment, and E7 of 1790644505; False at head by 🔴 1. Also ledger rows I2 and I10 and the changelog fragment. The policy sentence is corrected inside 🔴 1's fix |
| ⬜ 9 | The P4 reading adds a stop on `find` with a quoted glob or `{}` inside a shell string: 3 of 27,935 recorded commands | `hooks/cmdline.py#_behind_a_runner` | answered | The 3 of 27,935 extra stops are spec class (b), accepted by ledger I5 by name, and none commits; `cbcc8acc` adds the figure to I5 as a re-read note; Executed over all 511 transcripts. It is `spec.md` class (b), accepted by ledger row I5. Recorded for the budget, and no fix is asked |
| 🟢 | #674's shapes are asked at head, and the new cases were seen red | `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py` | confirmed | 201 of 315 new cases fail against `86256492`'s hooks. The other 114 are controls and base-answer pins |
| 🟢 | The depth bound answers in seconds where the base took up to 48 s | `hooks/commit-review-gate.py#NESTING_READ` | confirmed | Through `main()`: 3.2–6.0 s at head against 24.2–47.8 s at base, all deny |
| 🟢 | The guard spec's three worktree examples read as written | `docs/worktree-guard-spec.md` | confirmed | Executed through `cmdline.adds_a_worktree` at both SHAs |
| ❓ | The mutants the phase records name for the 114 controls and pins | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-6.md` | ❓ out of verified scope | Read and not re-run. The smith's records answer for them |
| ❓ | The cases on Windows | `tests/test_no_shape_the_base_stops_reads_silent.py` | ❓ out of verified scope | CI's `windows-latest` leg at the pull request answers it |

## Paste-ready fixes

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def understood(tokens):
-def understood(tokens):
+def understood(tokens, redirections=True):
@@
-    if _unreadable_past_leading_redirections(tokens):
+    if redirections and _unreadable_past_leading_redirections(tokens):
         return False
@@ def walk_directories(items, cwd):
-        known = understood(tokens)
+        known = understood(tokens)
+        # W1 (#674) refuses a segment `86256492` accepted. The refusal is ADDED
+        # beside the base's reading and never replaces it: an unresolved target
+        # is waived whole by `[no-review]` and is silence from a session that
+        # is not opted in, so replacing a directory the base judged lost stops.
+        as_written = known or understood(tokens, redirections=False)
         if not known:
-            moved = [
+            refused = [
                 (Unresolved(str(here), Unresolved.CONSTRUCT), prev)
                 for here, prev in moved
             ]
+            moved = _dedup(moved + refused) if as_written else refused
@@
         if any(sep in ("||", ";") for sep, _ in items[index + 1 :]):
+            refused = [
+                (Unresolved(str(h), Unresolved.CONSTRUCT), p) for h, p in running
+            ]
             failed = (
-                running
-                if known
-                else [(Unresolved(str(h), Unresolved.CONSTRUCT), p) for h, p in running]
+                running if known else list(running) + refused if as_written else refused
             )
@@
-        elif joined in ("&&", "||") and known:
+        elif joined in ("&&", "||") and as_written:
@@
-        elif known and joined not in SUBSHELL and following not in SUBSHELL:
+        elif as_written and joined not in SUBSHELL and following not in SUBSHELL:
@@
-        elif known:
+        elif as_written:
             # A pipeline stage or a background job -- what is left once the
--- a/docs/commit-review-gate-spec.md
+++ b/docs/commit-review-gate-spec.md
@@ So each place a program word stands is read past what the shell takes off it:
   judged where the shell is, as the same commit without it is. A `cd`, a
-  relocator, a reserved word or an expanding word reached past one leaves the
-  directory unresolved, the answer a `cd` behind a prefix already had.
+  relocator, a reserved word or an expanding word reached past one adds an
+  unresolved directory beside the one the walk read without it, and never
+  replaces it: `[no-review]` waives an unresolved target whole, and a session
+  that is not opted in reads one as silence, so a replaced directory is a
+  stop lost. The same holds for zsh's `noglob`, `nocorrect` and `repeat N`,
+  for a redirection glued to a word's end (`cd>/dev/null W`), and for one the
+  splitter cut (`2>&1 cd W`).
@@
 The reading can only have gained stops by this. Every reader asks what it
-asked before first and adds what the new reading finds, `understood` only
-adds a refusal, and a generated corpus of 11,393 commands across these
-positions found none silent where the release base stopped. The one answer
+asked before first and adds what the new reading finds, `understood`'s
+refusal is added beside the directory the walk read before, and a generated
+corpus of 11,393 commands across these positions found none silent where the
+release base stopped. The one answer
```
```python
# tests/test_no_shape_the_base_stops_reads_silent.py, appended
W1_PREFIXES = [
    "2>/dev/null cd sub &&",
    ">/dev/null pushd sub &&",
    ">/dev/null source /dev/null;",
    "2>/dev/null eval true;",
    "2>/dev/null $CMD;",
    "<<<x cd sub &&",
    "X=1 2>/dev/null cd sub &&",
    "time 2>/dev/null cd sub &&",
]


@pytest.mark.parametrize("prefix", W1_PREFIXES)
def test_w1_keeps_the_directory_the_base_judged_under_a_waiver(
    monkeypatch, capsys, projects, tmp_path, prefix
):
    """Round 1 of 1790660768, red 1. W1's refusal REPLACED the directory the
    base judged with an unresolved one, and `[no-review]` waives an
    unresolved target whole -- so the parity arm the base judged in the
    session's directory went silent, while bash commits there."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "sub").mkdir(exist_ok=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    command = f": '[no-review]'; {prefix} {BODY}"
    for which, got in with_and_without_the_press(
        monkeypatch, capsys, projects, command, session
    ).items():
        assert "silent" not in got, (command, which, got)


@pytest.mark.parametrize(
    "shape",
    [
        ">/dev/null source /dev/null; cd u2 && {body}",
        "2>/dev/null eval true; cd u2 && {body}",
        "2>/dev/null cd .; cd u2 && {body}",
        'SB={u2}; 2>/dev/null source /dev/null; git -C "$SB" commit -m x',
    ],
)
def test_w1_keeps_the_directory_the_base_judged_outside_an_opted_in_session(
    monkeypatch, capsys, tmp_path, shape
):
    """Round 1 of 1790660768, red 1. From a directory that is not opted in, an
    unresolved target is silence, and a later relative `cd`, or a name bound
    before the refused segment, stays unresolved behind it. The base resolved
    `u2`, which is opted in, and bash commits there."""
    plain = tmp_path / "plain"
    plain.mkdir()
    u2 = make_repo(plain / "u2")
    command = shape.format(body=BODY, u2=q(u2))
    got = decisions(monkeypatch, capsys, command, plain, "s")
    assert "silent" not in got, (command, got)
```
```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ # What `header_end` answers for a header whose spelling it does not place.
 UNPLACEABLE = -1

+# How many compound headers, one inside the next, `_is_the_program` and
+# `names_an_unknown_command` read before the segment counts as one whose
+# program they cannot place -- the stopping direction, as `UNPLACEABLE` is
+# (round 1 of 1790660768, red 2). Unbounded, each header was one level of
+# recursion, and a thousand of them raised `RecursionError` past
+# `_hides_a_commit`'s catch into `main`, which dropped every commit found. A
+# loop without a bound rescans the rest of the segment per header: 47 s on
+# 10,000. The commit gate's `NESTING_READ` is the same number for bodies.
+HEADERS_READ = 32
+
@@ def _is_the_program(tokens, k):
-    for t in tokens[:k]:
-        if os.path.basename(t) in RUNNERS:
+    for _level in range(HEADERS_READ):
+        for t in tokens[:k]:
+            if os.path.basename(t) in RUNNERS:
+                return True
+            if not (
+                ("=" in t and not t.startswith("-"))
+                or t in LIST_OPENERS
+                or t in ("!", "(")
+            ):
+                break
+        else:
             return True
-        if not (
-            ("=" in t and not t.startswith("-")) or t in LIST_OPENERS or t in ("!", "(")
-        ):
-            break
-    else:
-        return True
-    if _is_the_program_past_redirections(tokens, k):
-        return True
-    h = header_end(tokens)
-    if h == UNPLACEABLE:
-        return True
-    if h is not None and 0 < h <= k:
-        return _is_the_program(tokens[h:], k - h)
-    return False
+        if _is_the_program_past_redirections(tokens, k):
+            return True
+        h = header_end(tokens)
+        if h == UNPLACEABLE:
+            return True
+        if h is None or not 0 < h <= k:
+            return False
+        tokens, k = tokens[h:], k - h
+    return True
@@ def _segment_names_an_unknown_command(toks, nested=False):
-    if not nested and _expands(command_word(toks)[0]):
-        return True
-    if _expands(command_word(toks, redirections=True)[0]):
-        return True
-    if any(_expands([t]) for t in _without_redirections(_behind_a_runner(toks))):
-        return True
-    h = header_end(toks)
-    if h == UNPLACEABLE:
-        return any(_expands([t]) for t in _without_redirections(toks[1:]))
-    return (
-        bool(h)
-        and h < len(toks)
-        and _segment_names_an_unknown_command(toks[h:], nested=True)
-    )
+    for _level in range(HEADERS_READ):
+        if not nested and _expands(command_word(toks)[0]):
+            return True
+        if _expands(command_word(toks, redirections=True)[0]):
+            return True
+        if any(_expands([t]) for t in _without_redirections(_behind_a_runner(toks))):
+            return True
+        h = header_end(toks)
+        if h == UNPLACEABLE:
+            return any(_expands([t]) for t in _without_redirections(toks[1:]))
+        if not h or h >= len(toks):
+            return False
+        toks, nested = toks[h:], True
+    return True
--- a/docs/commit-review-gate-spec.md
+++ b/docs/commit-review-gate-spec.md
@@
   from the program, a later word that expands counts. None of these three counts
-  a redirection's target.
+  a redirection's target. Past 32 headers, one inside the next
+  (`HEADERS_READ`), the program counts as one the reader does not place.
```
```python
# tests/test_no_shape_the_base_stops_reads_silent.py, appended
@pytest.mark.parametrize("header", ["case a in a) ", "f() { ", "coproc "])
def test_a_deep_header_nesting_keeps_the_commits_found(
    monkeypatch, capsys, projects, tmp_path, header
):
    """Round 1 of 1790660768, red 2. The header readings recursed once per
    header, so 1,200 of them raised `RecursionError` past `_hides_a_commit`
    into `main`, which dropped the commit already found in `u`."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    for command in (
        f"cd {q(u)} && {BODY}; sh -c '" + header * 1200 + "true'",
        f"git -C {q(u)} commit -m x; " + header * 1200 + "watch -g x",
    ):
        for which, got in with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        ).items():
            assert "silent" not in got, (command[:60], which, got)
```
```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def walk_directories(items, cwd):
     states, parked, walked, env = [(cwd, None)], [], [], {}
     stack, defined = [], set()
+    # A `cd` behind a redirection the splitter cut (`2>&1 cd W`) arrives as a
+    # part whose first word is the descriptor (yellow 3); its group, glued back,
+    # is asked beside it.
+    glued = {parts[-1]: toks for parts, toks in merged_view(items)}
@@
-        known = understood(tokens)
+        known = understood(tokens) and (index not in glued or understood(glued[index]))
```
```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def redirection_width(tokens, i):
     return j - i


+def unglued(tokens):
+    """TOKENS with a redirection glued to the END of a word cut into its own
+    word, or None where no word carries one (round 1 of 1790660768, yellow 4).
+
+    `_REDIRECTION` matches at the start of a word, and a shell ends a word at
+    `<` and `>` wherever they stand: `git>/dev/null commit` runs `git commit`,
+    and `commit>/dev/null` is the subcommand `commit`. A descriptor in front
+    (`2>f`) and bash 4.1's `{fd}>f` are the operator's own and stay whole. It
+    is read as a view BESIDE the segment, the way `merged_view` is, so every
+    answer the segment gave stands and the view only adds.
+    """
+    out, cut = [], False
+    for t in tokens:
+        k = min((t.find(c) for c in "<>" if c in t), default=-1)
+        if (
+            k > 0
+            and not t[:k].isdigit()
+            and not (t[0] == "{" and t[k - 1] == "}")
+            # A word holding a space was quoted, and is an argument's.
+            and not any(c.isspace() for c in t)
+        ):
+            out += [t[:k], t[k:]]
+            cut = True
+        else:
+            out.append(t)
+    return out if cut else None
+
+
@@ def merged_view(items):
             parts, toks = groups[-1]
-            m = _REDIRECTION.match(toks[-1])
-            if m and m.end() == len(toks[-1]):
+            # The operator may be glued to the end of a word (`git>&2`,
+            # yellow 4), so the last piece `unglued` cuts is the one asked.
+            last = (unglued(toks[-1:]) or toks[-1:])[-1]
+            m = _REDIRECTION.match(last)
+            if m and m.end() == len(last):
@@ def names_an_unknown_command(text):
     # The segments the splitter cut inside a redirection are asked again,
-    # glued back (#674, `merged_view`): `2>&1 $CMD` runs `$CMD`.
+    # glued back (#674, `merged_view`): `2>&1 $CMD` runs `$CMD`. A redirection
+    # glued to a word's end is cut off and asked again too (`unglued`).
+    views = [*segments, *merged_segments(text)]
     return any(
         _segment_names_an_unknown_command(toks)
-        for toks in [*segments, *merged_segments(text)]
+        for toks in [*views, *filter(None, map(unglued, views))]
     )
@@ def _unreadable_past_leading_redirections(tokens):
-    rest, passed = _past_leading_redirections(tokens)
-    if not passed:
+    cut = unglued(tokens)
+    rest, passed = _past_leading_redirections(cut or tokens)
+    if not passed and cut is None:
         return False
--- a/hooks/commit-review-gate.py
+++ b/hooks/commit-review-gate.py
@@ from cmdline import (
     substitution_bodies,
+    unglued,
     walk_directories,
 )
@@ def _reads_a_commit(text):
-    for toks in [*segments, *merged_segments(stripped)]:
+    views = [*segments, *merged_segments(stripped)]
+    for toks in [*views, *filter(None, map(unglued, views))]:
@@ def commit_invocations(command, cwd=None):
     for parts, toks in merged_view(items):
         seen = set().union(*(kinds[p] for p in parts))
-        for kind, invs in _segment_invocations(toks, walked[parts[-1]][1]).items():
-            if kind not in seen:
-                found += invs
+        for view in filter(None, (toks, unglued(toks))):
+            for kind, invs in _segment_invocations(view, walked[parts[-1]][1]).items():
+                if kind not in seen:
+                    found += invs
+                    seen.add(kind)
+
+    # A redirection glued to a word's end (`git>/dev/null commit`, round 1 of
+    # 1790660768, yellow 4) is cut off and the segment read again beside
+    # itself, adding only a kind the segment did not find.
+    for (toks, bases), seen in zip(walked, kinds, strict=True):
+        cut = unglued(toks)
+        if cut is not None:
+            for kind, invs in _segment_invocations(cut, bases).items():
+                if kind not in seen:
+                    found += invs
```
```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ RUNNERS = frozenset(
         "script",
+        # zsh (round 1 of 1790660768, yellow 5): precommand modifiers, and
+        # `repeat N`, whose count is an operand the stand-in reads past.
+        "noglob",
+        "nocorrect",
+        "repeat",
     }
 )
@@ def command_word(tokens, stand_in="git", redirections=False):
     if i < len(toks) and (
         toks[i] in UNPLACED
+        # zsh's short loop, `for i (1 2) git commit` (yellow 5): the word list
+        # in parentheses, and the command straight after it. `for d in git
+        # commit` has no parenthesis there and stays a word list.
+        or (
+            toks[i] in ("for", "foreach")
+            and i + 2 < len(toks)
+            and toks[i + 2].startswith("(")
+        )
         or toks[i].endswith(")")
@@ def _past_leading_redirections(tokens):
         tok = toks[i]
+        # zsh's precommand modifiers and `repeat N` run the command in this
+        # shell, and the base read them as the command word (yellow 5).
+        if tok in ("noglob", "nocorrect") or (tok == "repeat" and i + 1 < len(toks)):
+            passed, i = True, i + (2 if tok == "repeat" else 1)
+            continue
         if (
```
```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# three rows in WRAPPED after "nice" -- the every-wrapper pin requires them
    "noglob": (f"noglob {C}", HERE),
    "nocorrect": (f"nocorrect {C}", HERE),
    "repeat": (f"repeat 1 {C}", UNRESOLVED),
```
```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def command_strings(tokens):
             flag = next(j for j, t in enumerate(rest) if _hands_a_string(word, t))
-            tail, skip = rest[flag + 1 :], False
-            for at, t in enumerate(tail):
+            # A redirection is asked and read past, and the scan goes on past
+            # the options and `--` behind it (yellow 6): `bash -c 2>/dev/null
+            # -- "$CMD"` runs `$CMD`.
+            tail, skip, at = rest[flag + 1 :], False, 0
+            while at < len(tail):
+                t, width = tail[at], redirection_width(tail, at)
                 if skip:
                     skip = False
+                elif width:
+                    out.append(t)
+                    at += width
+                    continue
                 elif t in VALUED:
                     skip = True
                 elif t != "--" and not t.startswith(("-", "+")):
-                    out += _string_at(tail, at)
+                    out.append(t)
                     break
+                at += 1
```
```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py, appended
# Round 1 of 1790660768, yellows 3-6: shapes a real shell commits that read as
# no commit at both `86256492` and `befe53cd`. Each was run in bash 3.2.57 or
# zsh 5.9 and made a commit.
STILL_UNREAD = {
    # yellow 4: a redirection glued to the END of a word.
    "git>/dev/null": "git>/dev/null commit -m x",
    "commit>/dev/null": "git commit>/dev/null -m x",
    "git>&2, cut at &": "git>&2 commit -m x",
    "git<&0, cut at &": "git<&0 commit -m x",
    "(git>/dev/null": "(git>/dev/null commit -m x)",
    "nice>/dev/null": "nice>/dev/null git commit -m x",
    "env>/dev/null": "env>/dev/null git commit -m x",
    "eval>/dev/null": 'eval>/dev/null "$X"',
    "sh>/dev/null -c": 'sh>/dev/null -c "$CMD"',
    # yellow 5: zsh.
    "for i (1)": "for i (1) git commit -m x",
    "for i (1) { }": "for i (1) { git commit -m x }",
    "repeat 1 { }": "repeat 1 { git commit -m x }",
    "repeat 2 eval": 'repeat 2 eval "$X"',
    # yellow 6: the string past `--` and options behind a redirection.
    "bash -c 2>/dev/null --": 'bash -c 2>/dev/null -- "$CMD"',
    "bash -c 2>&1 --": 'bash -c 2>&1 -- "$CMD"',
    "bash -c 2>/dev/null -e": 'bash -c 2>/dev/null -e "$CMD"',
    "sh -c 2>/dev/null +x": 'sh -c 2>/dev/null +x "$CMD"',
    "bash -c 2>/dev/null -O extglob": 'bash -c 2>/dev/null -O extglob "$CMD"',
}


@pytest.mark.parametrize("name", sorted(STILL_UNREAD))
def test_a_shape_both_shas_read_as_no_commit_is_read(name, tmp_path):
    """Seen red at `befe53cd`, where each returned nothing."""
    assert found(STILL_UNREAD[name], tmp_path), name


# yellows 3-5 in the walk: a `cd` the shell runs that the walk read as
# staying put. From a declared session, the commit lands in U, which declares
# nothing, and each read silent at both SHAs.
UNSEEN_CD = [
    "2>&1 cd {u} && git commit -m x",
    ">&2 cd {u} && git commit -m x",
    ">|f cd {u} && git commit -m x",
    "<&0 cd {u} && git commit -m x",
    ">&- cd {u} && git commit -m x",
    "2>&1 pushd {u} && git commit -m x",
    "cd>/dev/null {u} && git commit -m x",
    "pushd>/dev/null {u} && git commit -m x",
    "noglob cd {u} && git commit -m x",
    "nocorrect cd {u} && git commit -m x",
    "repeat 1 cd {u} && git commit -m x",
]


@pytest.mark.parametrize("shape", UNSEEN_CD)
def test_a_cd_the_walk_did_not_see_stops(monkeypatch, capsys, shape, tmp_path):
    """Seen red at `befe53cd`, where each was silent."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    command = shape.format(u=u)
    assert say(monkeypatch, capsys, command, session) != "silent", command
```

## Executed probes

| What was run | Result |
|---|---|
| Target's two changed test modules at `befe53cd` | 525 passed |
| The same modules against `86256492`'s `hooks/` | 201 of the 315 new cases failed, and the 114 that passed are controls and base-answer pins |
| The targeted cases through `main()` at base, head and the fix: red 1 in three session kinds, red 2 at three depths, the yellows, and 7 controls | 🔴 1: 35 base stops silent at head, all restored. 🔴 2: 10 lost at 1,200 and 3,000, all restored. Yellows: 44 of 50 silent at both SHAs are stops with the fix. Controls unchanged |
| The W1 corpus through `main()`: 8,640 commands at base, head, the red fixes alone, and all fixes | Lost at head: 4,125. Lost with either fix set: 0. Added by all fixes over base: 0. Raised: 0 |
| Real bash 3.2.57 and zsh 5.9, one fresh pair of repositories per shape, 44 shapes | Every shape claimed in 🔴 1 to 🟡 6 committed. `if true { }` and `- git commit` in zsh, and `env -S` on macOS, did not, and are not claimed |
| Header nesting through `commit_invocations`, 400 to 10,000 levels, at base, head, the unbounded loop and the bounded fix | Head raises `RecursionError` from 1,200. The unbounded loop takes 46.8 s at 10,000. The bounded loop takes 5.0 s, against 4.5 s at base |
| The worktree guard and `creation_directory` on W1 shapes, at base, head and both fix clones | Head is silent on 4 switches the base asked about, and files 2 creations under `S` instead of `S/w`. Both fix clones match base |
| A mutant of the fix with the three `env` branches back on `known` | The 10 bound-name cases turn silent |
| 27,935 recorded commands from 511 transcripts through `commit_invocations` at base, head, the red fixes and all fixes | Head differs from base on 3, and the red fixes match head. All fixes add 3 more, each this round's own probe patch with a zsh loop in a heredoc body, the class the base already stops. 0 raised |
| 15 reader modules, which load the reader, both gates, the consent writer or the notice | Head: 1,099 passed. Red fixes: 1,099 passed. All fixes with the planted cases: 1,149 passed |
| The planted cases against `befe53cd`'s hooks | 50 failed and 525 passed |
| `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py` and `tests/test_no_real_identifiers.py`, with the policy edit | 58 passed |
| `ruff check` and `ruff format --check` on the four files the fix touches | Clean |
| `bin/evidence-check .` at head | 0 drifted and 2 refused, exit 2 (⬜ 7) |
| `bin/evidence-check .` with the fixes | 18 anchors drifted in the rows of I1 to I7 and the older fragments, all in units the fix edits. The fix's re-read owes them |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It belongs to the sealer, once the rounds settle, and it is not due while this round leaves findings open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
