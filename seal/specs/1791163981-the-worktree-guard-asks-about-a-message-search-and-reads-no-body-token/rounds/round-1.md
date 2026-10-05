# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — review round 1

| Field | Value |
|---|---|
| Target SHA | 3a07c6075c5488e4c9c9f7fa2d9d445265a9919d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #803 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `85e77dc8cfd35b2e8f4e9f82d52a1fbcce84215f..22563bc6a730a30fc94b30ae352ec656f107e709`, 5 commits |
| Contract changes | tracked_in_any_remote → round-1-report.md, round-1.md; classify → classify, merge, main, 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md, questions.md, overview.md, round-1-report.md, round-1.md, check_text, family_view, released_drift, pytest |
| New units | _OBJECT_NAME (depth 1); _object_named (depth 1); _refs (depth 1); _fetched_as (depth 1); _the_bases_lookup (depth 1); _no_guess (depth 1); _a_dirty_clone_beside (depth 1); test_a_newly_read_checkout_in_front_takes_no_question_away (depth 1); _a_repository (depth 1); _where_git_checkout_lands (depth 1); test_a_message_search_holding_two_dots_is_read_as_a_switch (depth 1); test_the_object_lookup_reads_a_word_rev_parse_reads_as_a_range (depth 1); test_a_guess_through_any_fetch_refspec_is_read_as_a_switch (depth 1); test_the_first_newly_read_checkout_is_the_one_judged (depth 1) |
| Needs a fix | yes — 🟡 1 (a message search holding `..`), 🟡 2 (the guess through a fetch refspec), 🟡 3 (candidate C subtracts a hidden switch, against the changelog's claim) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Spec compliance first against `spec.md` (#790 alternative J: the base lookup kept and the new lookups OR-ed after it, the guess across every remote; #780 alternative I: a token read only where the raw command and the body-stripped command both carry it, with the frozen fallback; `hooks/cmdline_base.py` byte-frozen), then quality: the never-quieter property path by path including the error paths; #790's class against gitrevisions(7) and checkout's resolution paths, by construction; #780's readers and body-stripping failures; the overview's five divergences.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A message search whose text holds `..` (both halves resolving) reads as no branch: `rev-parse` splits it as a range; git checkout detaches | `hooks/worktree-guard.py:1044` | **fixed** `3909e1ca` | fixed at 3909e1ca; executed: git detached, base and build `None`; fix executed green |
| 🟡 2 | The guess matches `refs/remotes/*/<name>` by name; git maps through each remote's fetch refspec. A destination outside `refs/remotes/` or a partial glob is silent, and §*Known limits* says "never the other way" | `hooks/worktree-guard.py:1101` | **fixed** `3909e1ca` | fixed at 3909e1ca; executed: git created and switched on both shapes, base and build `None`; fix executed green |
| 🟡 3 | Candidate C subtracts a hidden switch once a newly read checkout is the judged switch, so a command the base asked about is silent; the changelog says nothing goes quiet | `hooks/worktree-guard.py:2699` | **fixed** `3909e1ca` | fixed at 3909e1ca; executed through `main()`: base `ask`, build silent |
| ⬜ 4 | Module-level `tokens` beside many `tokens` parameters | `hooks/worktree-guard.py:162` | answered | no defect ships: `_without_bodies` is the only reader of the module-level `tokens`, and no function whose `tokens` parameter shadows it reads the module; renaming the import would move every test that patches it for no change in behaviour; read; no defect today |
| 🟢 | The base lookup is asked first and unchanged; the new steps only add a yes (`classify` monotone) | `hooks/worktree-guard.py:1084` | confirmed | read, and A4's case passes at the target in the orchestrator's run |
| 🟢 | `has_token` ANDs the raw read with the body-free read, and falls back to the frozen reader on any failure | `hooks/worktree-guard.py:755` | confirmed | read; executed: 17 bash-checked shapes and 9 fallback shapes, no typed token lost |
| 🟢 | Every behavioural case the phases call red at `a3aa139a` is red there | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | executed: 37 failed, 57 passed with the base's guard, `tokens.py`, policy and READMEs put back |
| 🟢 | `hooks/cmdline_base.py` and its pin are untouched | `hooks/cmdline_base.py` | confirmed | executed: empty diff over the range |
| 🟢 | The `KINDS` comment takes the round-2 words and agrees with `classify` | `tests/test_guard_resolves_the_tree_it_judges.py:1395` | confirmed | read against `classify`'s `after` arm |
| 🟢 | `:/!-<text>` and `^<rev>` are stated honestly | `phases/phase-1.md`; `hooks/worktree-guard.py:1084` | confirmed | read |

## Paste-ready fixes

```diff
--- a/hooks/worktree-guard.py
+++ b/hooks/worktree-guard.py
@@ def _commit_named(name: str, cwd: str):
     found = _verified(f"{name}^{{commit}}", cwd)
     if found is None:
-        named = _verified(name, cwd)
+        named = _verified(name, cwd) or _object_named(name, cwd)
         if named is not None:
             found = _verified(f"{named}^{{commit}}", cwd)
     return found

+
+def _object_named(name: str, cwd: str):
+    """The object NAME names, read through git's object lookup alone, or None.
+
+    `rev-parse` reads a `..` in any argument as a range before it reads a
+    name, so a message search holding `..` is two revisions to it whenever
+    both halves resolve, and one message search to `git checkout`.
+    `cat-file --batch-check` hands its line to the lookup `git checkout`
+    uses, with no range read in front of it."""
+    if "\n" in name:
+        return None
+    try:
+        r = subprocess.run(
+            ["git", "cat-file", "--batch-check=%(objectname)"],
+            input=name + "\n",
+            cwd=cwd or None,
+            capture_output=True,
+            encoding="utf-8",
+            errors="replace",
+        )
+    except Exception:
+        return None
+    word = r.stdout.strip()
+    if r.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", word):
+        return None
+    return word
+
+
+def _guessed_refs(name: str, cwd: str) -> set:
+    """The refs `git checkout NAME`'s guess looks for: `refs/heads/NAME`
+    mapped through every remote's fetch refspec, as git maps it."""
+    try:
+        r = subprocess.run(
+            ["git", "config", "--get-regexp", r"^remote\..*\.fetch$"],
+            cwd=cwd or None,
+            capture_output=True,
+            encoding="utf-8",
+            errors="replace",
+        )
+    except Exception:
+        return set()
+    source = "refs/heads/" + name
+    found = set()
+    for line in r.stdout.splitlines():
+        spec = line.partition(" ")[2].strip().lstrip("+")
+        if spec.startswith("^") or ":" not in spec:
+            continue
+        src, dst = spec.split(":", 1)
+        if "*" not in src:
+            if src == source:
+                found.add(dst)
+            continue
+        head, _, tail = src.partition("*")
+        if (
+            len(source) > len(head) + len(tail)
+            and source.startswith(head)
+            and source.endswith(tail)
+        ):
+            found.add(dst.replace("*", source[len(head) : len(source) - len(tail)], 1))
+    return found
+
+
 def _one_merge_base(name: str, cwd: str) -> bool:
@@ def tracked_in_any_remote(name: str, cwd: str) -> bool:
     try:
         r = subprocess.run(
-            ["git", "for-each-ref", "--format=%(refname)", "refs/remotes/"],
+            ["git", "for-each-ref", "--format=%(refname)"],
             cwd=cwd or None,
             capture_output=True,
             encoding="utf-8",
             errors="replace",
         )
     except Exception:
         return False
     # A failed listing prints nothing, so it finds nothing.
-    return any(ref.endswith("/" + name) for ref in r.stdout.splitlines())
+    refs = r.stdout.splitlines()
+    if any(ref.startswith("refs/remotes/") and ref.endswith("/" + name) for ref in refs):
+        return True
+    guessed = _guessed_refs(name, cwd)
+    return any(ref in guessed for ref in refs)
```
```python
def test_a_message_search_holding_two_dots_is_read_as_a_switch(tmp_path):
    """`rev-parse` reads `..` as a range before it reads a name, so a message
    search holding it, both halves resolving, read as no branch while `git
    checkout` detached on it (round 1 of 1791163981, 🟡 1)."""
    d = tmp_path / "r"
    subprocess.run(["git", "init", "-q", str(d)], check=True, capture_output=True)
    _git(d, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(d, "config", "user.email", "t@t")
    _git(d, "config", "user.name", "t")
    _commit(d, "a.txt", "notes for v1..v2")
    _git(d, "tag", "v1")
    _commit(d, "b.txt", "second")
    _git(d, "tag", "v2")
    for carrier, make in CARRIERS.items():
        tokens = ["git", *make(":/v1..v2")]
        assert wg.classify(tokens, str(d)) == "switch", carrier


@pytest.mark.parametrize(
    "fetch", ["+refs/heads/*:refs/fork/*", "+refs/heads/*:refs/remotes/fork/x-*"]
)
def test_a_guess_through_any_fetch_refspec_is_read_as_a_switch(tmp_path, fetch):
    """git's guess maps `refs/heads/<name>` through each remote's fetch
    refspec; a destination outside `refs/remotes/<remote>/<name>` was silent
    (round 1 of 1791163981, 🟡 2)."""
    subprocess.run(
        ["git", "init", "-q", "--bare", str(tmp_path / "f.git")],
        check=True,
        capture_output=True,
    )
    d = tmp_path / "r"
    subprocess.run(["git", "init", "-q", str(d)], check=True, capture_output=True)
    _git(d, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(d, "config", "user.email", "t@t")
    _git(d, "config", "user.name", "t")
    _commit(d, "README.md", "initial commit")
    _git(d, "remote", "add", "fork", str(tmp_path / "f.git"))
    _git(d, "config", "--replace-all", "remote.fork.fetch", fetch)
    _git(d, "branch", "onfork")
    _git(d, "push", "-q", "fork", "onfork")
    _git(d, "branch", "-D", "onfork")
    _git(d, "fetch", "-q", "fork")
    for carrier in ("checkout N", "checkout N --"):
        tokens = ["git", *CARRIERS[carrier]("onfork")]
        assert wg.classify(tokens, str(d)) == "switch", (fetch, carrier)
```
```text
and where a remote-tracking branch of any remote ends in it, or where a
remote's fetch refspec maps `refs/heads/<name>` to a ref that exists, which is
git's guess
```
```text
The guess reads tracking refs named `refs/remotes/<remote>/…<name>`, so a
remote whose fetch refspec puts its branches elsewhere, or renames them with a
partial glob, is guessed from by git and not by the guard.
```
```text
The old lookup is still asked first, so no `checkout` name the guard read as a
branch before reads as anything else now.
```
```text
- A switch only the wider reading finds (a git behind a redirection, a zsh
  precommand word, a spaced `--config-env`) is asked only where the frozen
  reading judged no switch in the same command, whichever tree each names
  (#630). Since #790 more `checkout` names are a switch the frozen reading
  judges, so a message search, a merge-base shorthand or a guessed branch in a
  clean single-session tree now takes that question away from a hidden switch
  written beside it, which the base asked. A plain `git -C <dir> switch …` is
  the spelling the guard reads.
```
```python
    assert (
        "Since #790 more `checkout` names are a switch the frozen reading "
        "judges, so a message search, a merge-base shorthand or a guessed "
        "branch in a clean single-session tree now takes that question away"
    ) in _policy_text()
```

## Executed probes

| What was run | Result |
|---|---|
| The five narrow modules, with fixes 1 and 2 applied in the clone (not at the target) | 585 passed, 1 skipped |
| The new cases with the base's guard, `tokens.py`, policy and READMEs put back | 37 failed, 57 passed; every behavioural red the phases claim |
| `git checkout` of a message search holding `..` in a scratch repository, base and build `classify` | git detached; base `None`, build `None`; with fix 1, `switch` |
| `git checkout` guessing through a fetch refspec outside `refs/remotes/`, and through a partial glob | git created and switched on both; base and build `None`; with fix 2, `switch` |
| `main()` on a newly read checkout beside a hidden switch in a second dirty tree | base `ask`, build silent; plain branch in front: silent in both; nothing in front: `ask` in both |
| `has_token` on 17 opener shapes, checked against bash, and 9 with `tokens` None | the typed token was read wherever bash runs its line |
| `bin/evidence-check --strict .` in the worktree, with this report on disk | exit 0 |
| The full suite, the repository-wide lint and the typecheck (the broad gate) | not yet run by anyone; this round ran none of it, and the sealer answers it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |
