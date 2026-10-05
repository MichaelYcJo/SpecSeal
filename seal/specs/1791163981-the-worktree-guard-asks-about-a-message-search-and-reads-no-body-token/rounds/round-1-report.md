# Round 1 report — 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 3a07c607 |
| Base | `release/v0.18.3` at a3aa139a |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 3a07c607, under the session scratchpad (`<scratchpad>/<id>/round-1/clone`), removed at hand-over |

## Summary

Stage 1 (spec compliance) holds for what the spec enumerated: the base lookup
is asked first and unchanged, resolve-then-peel and the one-merge-base rule are
OR-ed after it, the guess reads every remote, `has_token` ANDs the raw read with
a body-free read and falls back to the frozen reader, `hooks/cmdline_base.py`
and its pin are untouched, and the policy, docstrings and both READMEs say what
the code does. Every behavioural case the smith says is red at `a3aa139a` is red
there (executed).

Three findings come from judging the class by construction rather than by the
spec's list. Two are members of #790's own class that the build still leaves
silent, because the lookup goes through `git rev-parse` and through a naming
convention where `git checkout` goes through neither. The third is a shape on
which the build is silent where the base asked: not in `classify`, which is
monotone as claimed, but one reader over, in candidate C. All three are 🟡; none
loses a record or crashes.

## Findings from execution

### 🟡 1 — A message search whose text holds `..` still reads as no branch

`hooks/worktree-guard.py:1044` (`_commit_named`), claimed at `:1088` and in
`docs/worktree-guard-spec.md:610`.

`git rev-parse` reads its argument through a range parser before it reads a
name, so a message search whose pattern holds `..` is split into two revisions
whenever both halves resolve. The left half always resolves where any message
matches the text before the dots, and the right half resolves where it is a
branch or tag name. Neither of the build's two `rev-parse` calls can then read
the name, while `git checkout` hands the whole word to the object lookup, finds
the message, and detaches.

Executed in a scratch repository (git 2.54.0): a commit whose message holds
`v1..v2` and two tags `v1` and `v2`; `git checkout` of the message search for
`v1..v2` detached HEAD (exit 0); `rev-parse --verify` exited 1 printing two
revisions; the base `classify` and the build `classify` both answered `None`.

Why it matters: it is #790's mechanism (a word whose syntax the lookup reads
differently from `checkout`) in a second spelling, so a dirty or shared tree
moves unasked. The docstring says "every single-revision expression of
`gitrevisions(7)` that peels to a commit" and the policy says "as every
single-revision form does", and both are false for it. By reading, not
executed: `rev-parse`'s parent shorthands (`^@`, `^!`, `^-<n>` at the end of a
word) are read the same way, so a search pattern ending in one of them is the
same class.

The fix reads the name through `git cat-file --batch-check`, which hands its
line to the object lookup `git checkout` uses with no range parsing in front of
it. It is OR-ed after the existing step, so it can only add a yes. Executed:
with it applied, the shape answers `switch`.

### 🟡 2 — The guess reads a naming convention, and git's guess reads each remote's fetch refspec

`hooks/worktree-guard.py:1101` (`tracked_in_any_remote`, docstring `:1103`),
and `docs/worktree-guard-spec.md:784`.

`git checkout <name>` guesses by mapping `refs/heads/<name>` through every
remote's `remote.<remote>.fetch` refspec and looking for the destination. The
build instead looks for any ref under `refs/remotes/` that ends in
`/<name>`. The two agree only for the default refspec.

Executed, two shapes, each in a scratch repository with one bare remote holding
a branch nobody has locally:

- a fetch refspec whose destination is outside `refs/remotes/` (a remote's
  branches fetched under `refs/fork/`): `git checkout <name>` created the
  branch and switched (exit 0); base and build `classify` both `None`;
- a fetch refspec with a partial glob inside `refs/remotes/` (destination
  `refs/remotes/fork/x-*`): git created and switched; base and build both
  `None`, because the tracking ref ends in `/x-<name>`, not `/<name>`.

Why it matters: a silent switch in #790's class C3. The policy sentence at
`:784` says the guard "guesses where git would not, never the other way", which
is the false half. The overview's first divergence row argues against reading
git config ("a second call and a read of git config, which the guard does not
do"), but that config is what git's guess reads, so the superset it chose is
not a superset.

The fix maps `refs/heads/<name>` through the fetch refspecs the way git does
and checks the destinations against the ref listing, OR-ed after the existing
match, so it can only add a yes. Executed: with fixes 1 and 2 applied, both
shapes answer `switch`, and the five narrow modules ran green (row below).
Justifying instead means rewording `:784` to say which refspecs the guess
reads.

### 🟡 3 — Candidate C now subtracts a hidden switch the base asked about

`hooks/worktree-guard.py:2699` (`main`'s `quiet`, which hands `judged` to
`wider_only_kinds`); the claims are
`seal/specs/1791163981-…/changelog.md:12-13` ("so nothing the guard asked about
before goes quiet") and `overview.md:14` ("Both now move only towards a
question").

`quiet` hands candidate C the kinds the frozen loop judged, and C subtracts a
kind as a whole: once the loop judged any switch, a switch only the wider
reading finds is not asked about, whichever tree it names. At the base, a
`checkout` naming a message search, a merge-base shorthand or a branch guessed
from a non-`origin` remote was no switch, so a hidden switch beside it reached
C's question. In the build that checkout is the judged switch. The ladder
judges its tree, finds it clean and single-session, exits through `quiet`, and
C then subtracts the hidden one.

Executed through `main()` with the module's own `run` helper: in a clean
single-session tree, a `checkout` naming a message search, followed in the same
command by a `switch` in a second, dirty tree, written with `-C` behind a
stderr redirection. Base: `ask` (C's question). Build: silent. The same command
with a plain branch name in front is silent in both, and with no checkout in
front it is `ask` in both.

Why it matters: the dirty second tree is switched without a word, on a
command the base asked about. The mechanism is older than this work: it is
#630's "judged on the first" limit meeting C's subtraction by kind. #790 widens
which segments are a "first", and the changelog line states the opposite to
users. `classify` itself is monotone, and A4's case proves exactly that; the
property the changelog states is about the guard.

Fix or justify. The paste-ready fix below is the justification route: say what
holds, and name the residual in §*Known limits*. A code fix would keep
`"switch"` out of `judged` where only the #790 lookups made the segment a
switch. That needs `classify` to report which lookup answered, which is the
smith's call, so I do not fence it.

## Findings from reading

### ⬜ 4 — A module named `tokens` beside dozens of parameters named `tokens`

`hooks/worktree-guard.py:162`. `import tokens` binds a module-level name that
`classify(tokens, cwd)`, `segment_cwd`, `judgeable` and `main`'s walk loop all
shadow with a word list. `_without_bodies` reads the global and is correct
today. But a later edit that calls `tokens.without_bodies` from inside any of
those functions gets a list. No defect ships, so this is ⬜. Importing the module
under a name of its own would end the shadowing, and the tests that patch the
name would move with it.

## What the prompt asked, answered

**The never-quieter property, path by path (by construction):**

- `is_ref`: the base's call runs first with the same arguments. Every later
  call runs only after it said no. Read: `_verified` returns None only where
  the base's call would have returned non-zero or raised.
- The `)` peel and the `origin/` guess both keep the base's lookups in the same
  order and add an OR. Read.
- `switch_kind` is unchanged; the diff does not touch it.
- `classify`'s new OR adds only `switch` verdicts. Candidate C is where a new
  `switch` verdict turns into silence: 🟡 3, executed.
- Error paths: a git call that fails or raises in the new steps answers no,
  which hands the name back to the base's own next lookup. No new call sits in
  front of a base lookup except `_commit_named`'s second and third, which run
  before the base's `origin/` lookup. A hang there would delay that lookup, but
  no timeout exists on either side (`spec.md` §*Out*), and a hung guard is the
  same outcome at the base. Read; not executed.

**#790's class against `gitrevisions(7)` and checkout's resolution paths:**
`checkout` takes a name through git's merge-base-aware object lookup (`...`
split, then the plain object lookup), then the guess. The build covers the `...` split exactly (split at the
first `...`, empty side `HEAD`, one merge base), and covers the object lookup
through `rev-parse`, which differs from it by the range and parent-shorthand
pre-parse (🟡 1). It covers the guess by a naming convention, which differs
from it by the refspec mapping (🟡 2). The smith's two irregular cases are
stated honestly. `:/!-<text>` answering yes at the base by accident is in
`phases/phase-1.md` with its mechanism. `^<rev>` read as a ref though git
refuses is in `is_ref`'s docstring and in §*Known limits*.

**#780's reader (enumerated from where the two literals are read in `hooks/`):**
two production reads, both `has_token` (`judge_creation` and `main`'s switch
ladder). `hooks/tokens.py#given` is already body-free. `hooks/worktree_consent.py`
and `hooks/answers.py` read neither guard token as consent; they name them in
prose only. On body-stripping failure, executed:

- 17 shapes of heredoc openers that bash parses differently from a naive
  reader, each followed on a later line by a creation with a typed
  `[worktree-ok]`, checked against bash's own run of the line;
- the same nine of them again with `tokens` set to None (the frozen fallback).

The typed token was read in every shape where bash runs the line, and in every
one the base read it. An unterminated body puts the typed line inside the body
for bash too, so that command never runs, and nothing the user consented to is
denied. I found no shape that loses a typed token. That is a sample, not a
proof: the "text the reader takes for a body and the shell does not" row of
`spec.md` stays a residual, as the spec says.

**The overview's five divergences:**

1. Guess reach: the direction (louder on a name that ends a longer remote
   branch) is right. The grounds "naming the remotes exactly takes … a read of
   git config" are the half 🟡 2 contradicts.
2. A2's guess clause: confirmed. The base did the same for `origin`, and
   `spec.md` §*Out* accepts it.
3. A8's fallback on any exception: confirmed by reading and by the fallback
   probe above.
4. The milestone wording: confirmed by reading, against the release-hygiene
   rule the overview cites. The test itself was not run.
5. The extra §*Which tree* sentence (`Corrected · K7`): confirmed by reading the
   paragraph against `has_token` and `wider_only_kinds`.

**P1:** the default (a) is implemented as `tracked_in_any_remote` OR-ed beside
the base's `origin/` lookup in both the name and the `)` peel arms. That is
correct for the default convention, and 🟡 2 is where it falls short of git's
guess.

**Broad gate:** not yet. This report leaves three 🟡 open, so the sealer's
spawn has not come due.

## Regression tests to plant

All three go in `tests/test_guard_resolves_the_tree_it_judges.py`, beside the
#790 block. The first two are fenced under their findings below; each is red at
3a07c607 by the probes above (executed against the same shapes, not as these
exact cases). The third is the pin of the Known-limits sentence in fix 3.

## Facts for the evidence ledger

- `git rev-parse` reads `..` and the parent shorthands in an argument before it
  reads a name, so it cannot verify a message search that carries them.
  `git cat-file --batch-check` can (executed, git 2.54.0).
- `git checkout`'s guess maps `refs/heads/<name>` through each remote's fetch
  refspec, so a tracking ref outside `refs/remotes/<remote>/<name>` is guessed
  from (executed, git 2.54.0, two refspec shapes).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A message search whose text holds `..` (both halves resolving) reads as no branch: `rev-parse` splits it as a range; git checkout detaches | `hooks/worktree-guard.py:1044` | open | executed: git detached, base and build `None`; fix executed green |
| 🟡 2 | The guess matches `refs/remotes/*/<name>` by name; git maps through each remote's fetch refspec. A destination outside `refs/remotes/` or a partial glob is silent, and §*Known limits* says "never the other way" | `hooks/worktree-guard.py:1101` | open | executed: git created and switched on both shapes, base and build `None`; fix executed green |
| 🟡 3 | Candidate C subtracts a hidden switch once a newly read checkout is the judged switch, so a command the base asked about is silent; the changelog says nothing goes quiet | `hooks/worktree-guard.py:2699` | open | executed through `main()`: base `ask`, build silent |
| ⬜ 4 | Module-level `tokens` beside many `tokens` parameters | `hooks/worktree-guard.py:162` | open | read; no defect today |
| 🟢 | The base lookup is asked first and unchanged; the new steps only add a yes (`classify` monotone) | `hooks/worktree-guard.py:1084` | confirmed | read, and A4's case passes at the target in the orchestrator's run |
| 🟢 | `has_token` ANDs the raw read with the body-free read, and falls back to the frozen reader on any failure | `hooks/worktree-guard.py:755` | confirmed | read; executed: 17 bash-checked shapes and 9 fallback shapes, no typed token lost |
| 🟢 | Every behavioural case the phases call red at `a3aa139a` is red there | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | executed: 37 failed, 57 passed with the base's guard, `tokens.py`, policy and READMEs put back |
| 🟢 | `hooks/cmdline_base.py` and its pin are untouched | `hooks/cmdline_base.py` | confirmed | executed: empty diff over the range |
| 🟢 | The `KINDS` comment takes the round-2 words and agrees with `classify` | `tests/test_guard_resolves_the_tree_it_judges.py:1395` | confirmed | read against `classify`'s `after` arm |
| 🟢 | `:/!-<text>` and `^<rev>` are stated honestly | `phases/phase-1.md`; `hooks/worktree-guard.py:1084` | confirmed | read |

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

## Paste-ready fixes

### 🟡 1 and 🟡 2

The code was applied in the clone and the narrow modules ran green with it.
The docstring lines were not run.

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

The cases, for `tests/test_guard_resolves_the_tree_it_judges.py` after the #790
block. Each was red at 3a07c607 by the probes; show it red again before
planting it (contract §15):

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

The policy sentences that move with them (§14), for `docs/worktree-guard-spec.md`.
In §*Which tree*, replace "and where a remote-tracking branch of any remote
ends in it, which is git's guess" with:

```text
and where a remote-tracking branch of any remote ends in it, or where a
remote's fetch refspec maps `refs/heads/<name>` to a ref that exists, which is
git's guess
```

In §*Known limits*, the sentence "never the other way" stands once fix 2 is in.
If fix 2 is declined, it is replaced with:

```text
The guess reads tracking refs named `refs/remotes/<remote>/…<name>`, so a
remote whose fetch refspec puts its branches elsewhere, or renames them with a
partial glob, is guessed from by git and not by the guard.
```

### 🟡 3

The justification route. Replace `changelog.md`'s sentence at lines 12-13:

```text
The old lookup is still asked first, so no `checkout` name the guard read as a
branch before reads as anything else now.
```

Add a bullet to `docs/worktree-guard-spec.md` §*Known limits*, after the
`checkout`-name bullet, and pin it beside
`test_the_guard_policy_says_what_it_reads_past_the_base`:

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

And `overview.md:14`, the builder's: "Both now move only towards a question,
except a hidden switch beside a newly read checkout (§*Known limits*)."

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |

Needs a fix: yes — 🟡 1 (a message search holding `..`), 🟡 2 (the guess
through a fetch refspec), 🟡 3 (candidate C subtracts a hidden switch, against
the changelog's claim)

Loses a record or crashes: no

## Proof block

Opened in this round, in the clone at 3a07c607 unless noted:
`seal/specs/1791163981-…/spec.md`, `overview.md`, `questions.md`,
`changelog.md`, `phases/phase-1.md`; the full diff of `hooks/worktree-guard.py`,
`hooks/tokens.py`, `README.md`, `README.ko.md`, `docs/worktree-guard-spec.md`
and `tests/test_guard_resolves_the_tree_it_judges.py` over a3aa139a..3a07c607;
in `hooks/worktree-guard.py`, the units `classify`, `switch_kind`,
`wider_only_kinds`, `ask_what_only_the_wider_reading_finds`, `judge_creation`
and `main`; `hooks/tokens.py`; `hooks/one_heredoc.py` (its matcher);
`hooks/cmdline_base.py#drop_heredoc_bodies`; `docs/worktree-guard-spec.md`
§*Known limits*; `tests/conftest.py#repo`; `bin/test`. The base's `hooks/` was
read from `git archive a3aa139a`. Not opened: `plan.md`, `routing.md`,
`phases/phase-2.md` to `phase-4.md`, the ledger fragment; the claims this report
quotes from the overview were checked against the code, not against those
files.
