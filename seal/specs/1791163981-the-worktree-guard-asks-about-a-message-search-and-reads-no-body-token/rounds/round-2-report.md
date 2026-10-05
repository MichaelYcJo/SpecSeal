# Round 2 report — 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token

| Field | Value |
|---|---|
| Round | 2, the verifying round over round 1's fixes |
| Target SHA | 1eaccfc7 |
| Fix range checked | 85e77dc8..22563bc6 (round 1's record names it) |
| Base | `release/v0.18.3` at a3aa139a |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 1eaccfc7, under the session scratchpad (`<scratchpad>/<id>/round-2/clone`), removed at hand-over |

## Summary

All three of round 1's 🟡 are closed for the shapes round 1 named, and round
1's ⬜ 4 stands as answered. The largest fix, 🟡 3, holds by construction and
by execution. The guard is never quieter than the base on any command, and it
behaves exactly like the base on every command that holds no newly read
checkout. A newly read checkout is one only #790's lookups read as a switch.

There is one new finding. It sits inside `_fetched_as`, a unit round 1's fix
pass created, and it is the class 🟡 2 was about, met one config shape further
along. `_fetched_as` splits `git config --get-regexp` output at its first
space. So a remote whose name holds a space maps nothing, while git fetches
and guesses through it. Its reach is narrow: `git remote add` refuses such a
name, and only a config written by hand or through `git config` holds one.
But it falsifies the policy sentence round 1's fix made true ("never the other
way") and ledger row R5's "every remote". The fix changes two lines and was
executed in the clone, red before and green after. This is 🟡, and it would
be the item's one reopening.

The rest is ⬜: a placement trade against 3a07c607 that the policy states but
§*Known limits* does not list, the extra git calls the two-pass read costs,
and one test docstring that calls two control cases red.

## How round 1's verdicts were checked

Round 1's record lists 🟡 1–3 as fixed and ⬜ 4 as answered. Each answer
below is re-derived at 1eaccfc7. Round 1's three probes were re-run at
a3aa139a, at 3a07c607 (round 1's target) and at 1eaccfc7, through each
version's `hooks/` taken by `git archive` and loaded in a process of its own.
I carried coordinates from round 1's report and the ledger fragment, and no
verdicts.

## Findings from execution

### 🟡 1 — A remote whose name holds a space is read as no remote, and git guesses through it

`hooks/worktree-guard.py:1192` (`_fetched_as`, the line reading each config
entry). The claims it falsifies are at `docs/worktree-guard-spec.md:787-790`
("The guard reads each remote's fetch refspec, as git's guess does … never the
other way") and in ledger row R5 ("maps `refs/heads/<name>` through every
remote's `remote.<remote>.fetch` refspec as git's guess does").

`git config --get-regexp` prints each entry as the key, one space, then the
value. A subsection keeps its case and its spaces. `_fetched_as` takes the
value as everything after the first space. For a remote named with a space,
that slice starts inside the key, the source half no longer starts with
`refs/heads/`, and the refspec maps nothing. The first check in
`tracked_in_any_remote` (a ref under `refs/remotes/` ending in `/<name>`)
does not reach this case either, because the destination is outside
`refs/remotes/`.

Executed (git 2.54.0, scratch repository). `git remote add` refuses the name
("not a valid remote name"). After it was written with `git config`,
`git fetch` of that remote succeeded and `git checkout <name>` created the
branch and switched. The shipped `classify` answered `None` for that shape,
and so did a3aa139a and 3a07c607. With the entries read through
`git config -z`, it answered `switch`. That read was checked on all 12
refspec shapes in the probe table below, and no other answer moved.

Why it matters: this is a silent switch of #790's class C3, in a unit this
run's fixes created. In a dirty or shared tree, the tree moves without a
question. The policy sentence that round 1's 🟡 2 was about is an absolute,
and this shape makes it false again. The reach is narrow, as stated above.
That reach is the ground for weighing the reopening, and the orchestrator's
call. It does not lower the severity. The defect ships if this stands.

Fix: read the entries NUL-separated, where the key ends at the first newline.
That is two lines of `_fetched_as` and no new unit. The paste-ready block is
below, with a case that was planted in the clone, seen red at 1eaccfc7, and
seen green with the fix. The whole module ran at 419 passed with it. The
justification route is to bound the §*Known limits* sentence and R5 instead.

### What 🟡 3's fix does, path by path (construction, then execution)

`classify(..., base_only=True)` is a3aa139a's `classify`. The function's diff
against the base changes only the `checkout` arm, where the lookups run
through `_the_bases_lookup` and `_no_guess`. `_the_bases_lookup` makes the
base's single `rev-parse --verify --quiet <name>^{commit}` call and answers
yes on exit 0, which always prints an object name. Every other arm is
byte-identical, so a creation segment (only `base_only` is asked of one) reads
as it did.

`main`'s loop (`hooks/worktree-guard.py:2775-2803`) has two cases.

- **The base read a switch somewhere in the command.** `switch_reason`,
  `switch_at`, `creation_at` and the early exits are the base's, step for
  step. `newly_read` is only recorded and is never used, because
  `past_the_base` is false. So `judged` is the base's, and the verdict is the
  base's.
- **The base read no switch.** The first newly read checkout takes the slot.
  `judged` keeps "switch" out, so candidate C gets the same `judged` set the
  base gave it. Every exit of the ladder is now one of three: a `respond`
  (louder than the base), a `choose` (louder), or `quiet()` with the base's
  `judged` (C asks the base's question). A creation is still judged at every
  one of them: by the ladder's call above row 3, by `choose`'s `before_ask`,
  or on the `not top` branch with `repo_paths(creation_at)[0]`, which are the
  base's arguments.

So the guard is never quieter than the base. On a command with no newly read
checkout, `base_only` and the full read agree on every (segment, directory)
pair, because `classify` is monotone. The target then reads such a command
exactly as a3aa139a and 3a07c607 did.

Executed through `main()`, with the test module's harness rebuilt for three
versions, over 31 shapes. The axes were: one or two newly read checkouts; a
switch the base reads written before it, after it, or nowhere; a switch only
C reads, or none; the session's tree clean and a second tree dirty, or the
reverse; single-session, idle-shared and active-shared; a creation in front or
behind; `&&`, `;`, a subshell and a `cd`. The probe kept each version's
`choose` state apart. The first run shared it and showed three false moves
in the shared-tree rows, which this report does not count.

| Shape (mechanism, not spelling) | a3aa139a | 3a07c607 | 1eaccfc7 |
|---|---|---|---|
| Round 1's probe: newly read checkout in the clean session tree, then a C-only switch in a dirty tree | ask (C) | silent | ask (C) |
| newly read checkout in the clean tree, then a base-read switch in a dirty tree | ask, dirty tree | silent | ask, dirty tree |
| newly read checkout in a dirty tree, then a base-read switch in the clean tree | silent | ask, dirty tree | silent |
| the same, plus a C-only switch in the dirty tree | silent | ask | silent |
| newly read checkout in a dirty tree, alone, through `-C` or a `cd` | silent | ask | ask |
| two newly read checkouts, the clean tree's first, then a C-only switch | ask (C) | silent | ask (C) |
| the C-only switch written first, the newly read checkout after | ask (C) | silent | ask (C) |
| newly read checkout, then the C-only switch, after a `;` or inside a subshell | ask (C) | silent | ask (C) |
| idle-shared session tree, newly read checkout alone or before a C-only switch | silent / ask | deny | deny |
| active session, newly read checkout before a base-read switch in a dirty tree | deny, dirty tree | deny, session tree | deny, dirty tree |
| newly read checkout with a worktree creation, either order | deny | deny | deny |
| eight commands with no newly read checkout (base switches, C-only switches, a file restore, a search matching nothing, a creation) | — | same as base | same as base |

No row of the target is quieter than the base. Two rows are quieter than
3a07c607: a newly read checkout in a dirty second tree, written before a
switch the base reads in a clean tree. ⬜ 2 below answers what that means.

### 🟡 2's mapping, by enumeration (executed)

Each shape was built in a scratch repository with one bare remote holding a
branch nobody has locally. git's own `git checkout <name>` was the reference.

| Fetch config | git | a3aa139a | 3a07c607 | 1eaccfc7 |
|---|---|---|---|---|
| destination outside `refs/remotes/` | lands | None | None | switch |
| partial glob inside `refs/remotes/` | lands | None | None | switch |
| a negative refspec excluding the name, beside a mapping one | lands | None | None | switch |
| two `fetch` lines, the second mapping the name exactly | lands | None | None | switch |
| `*` in the middle of source and destination | lands | None | None | switch |
| `*` at the end of the source, in the middle of the destination | lands | None | None | switch |
| whole-namespace mirror into a private prefix | lands | None | None | switch |
| no destination, a ref left behind by an earlier fetch | refused | None | None | None |
| the refspec only in a config reached by `include.path` | lands | None | None | switch |
| remote name holding a `/` | lands | None | None | switch |
| a legacy remotes file under the git directory | refused | None | None | None |
| remote name holding a space | lands | None | None | **None** (🟡 1) |

So git ignores a negative refspec in its guess, and the guard matches that.
A refspec given with `-c` on the command line was also tried, and git does
not guess through it, so no miss lives there. The mapping adds no yes that
git refuses in any shape tried. The two refused shapes answer `None`. The
louder extras the policy lists (a name ending a longer remote branch, two
remotes, `--detach`) come from the older name match and are unchanged.

### 🟡 1's object lookup: what `cat-file --batch-check` accepts (executed)

`_object_named` runs only after `rev-parse` has failed on the name, and its
answer is peeled by `<oid>^{commit}`. Twelve names were tried: a blob path
(`HEAD:f.txt`), the root tree (`HEAD:`), `HEAD^{tree}`, a subtree path, a full
tree object name, a full blob object name, a short tree object name, an
annotated tag on a tree, an annotated tag on a commit, two index-path forms,
and a four-character prefix two blobs share. git refused every one except the
tag on a commit. All three versions answered `None` on every refusal and
`switch` on the tag. An ambiguous prefix prints `ambiguous`, which is not an
object name, and a tree or blob fails the peel. Round 1's two-dots probe now
answers `switch` (a3aa139a and 3a07c607: `None`).

No extra yes comes from `cat-file`. The extra yes on a short prefix that a
commit and another object share comes from the base's own `^{commit}` call,
which disambiguates toward the commit where `git checkout` refuses. That
predates #790, and its direction is louder (read, not executed).

### ⬜ 2 — The placement trade against 3a07c607 is stated in §*Which tree* and missing from §*Known limits*

`hooks/worktree-guard.py:2801` (`past_the_base`); `docs/worktree-guard-spec.md:339`
and §*Known limits*.

A newly read checkout in a dirty second tree, written before a switch the base
reads in a clean tree, is silent at the target and at a3aa139a, and was asked
at 3a07c607 (executed, two rows above). This is the cost of 🟡 3's fix, and
it is the only choice that never goes quieter than the base. Judging the
newly read checkout first, as 3a07c607 did, is the mirror of this case: it was
silent where the base asked about the second tree. Judging both trees is
#630's limit. §*Which tree* states the rule ("it is judged only where the base
read no switch at all"). But the paragraph at `:339` still says the walk
"keeps the first switch", and the §*Known limits* bullet on `checkout` names
does not say that a newly read one in another tree goes unasked behind a
switch the base reads. No behaviour or fact is wrong, so this is ⬜. One
sentence in §*Known limits* would close it.

### ⬜ 3 — The two-pass read costs up to five times the base's git calls on a name nothing resolves

`hooks/worktree-guard.py:2786-2791`.

Executed, by counting the subprocesses one `classify` spawns for a
`checkout` name that neither a file nor a ref matches: 2 with `base_only`
and 8 without. `main` runs both, so the hook now spawns 10 where a3aa139a
spawned 2. Two parts of that are waste. The full read repeats both of the
base's calls. And the full read still runs after `newly_read` is set, when
its answer is thrown away. A `newly_read is None` test in front of the second
`classify` removes the second part. Having `classify` report which lookup
answered would remove the first, and round 1 named that shape as the
smith's call. Each extra call costs only time. No verdict moves, so this is
⬜.

### ⬜ 4 — One test's docstring calls its two control cases red

`tests/test_guard_resolves_the_tree_it_judges.py:2412`
(`test_a_newly_read_checkout_in_front_takes_no_question_away`).

The docstring says "Red at `85e77dc8`". Executed with 85e77dc8's guard put
back in the clone: the two `:/base` cases fail and the two `:/nomatch` cases
pass. `:/nomatch` matches no commit, so it is a switch in no version, which
makes those two cases controls. The docstring should say which two are red.
`test_the_first_newly_read_checkout_is_the_one_judged` passes at 85e77dc8
too, and its docstring claims only a mutation red ("seen red with the last
one taking it"), which is honest.

## Findings from reading

### The M3 replay the smith reports (0 moved, 0 quieter, over 581 and 1,044 pairs)

The probe was deleted, so its selection cannot be opened. Its counts do not
match phase 1's selection (347 and 563 pairs holding a `checkout` segment, and
56 and 77 carrying a token). They are larger, which fits a substring
selection rather than the frozen walk's. Either selection holds every pair
the reorder can touch. The reorder acts only where a newly read checkout
exists, and that takes a `checkout` subcommand word. A spelling whose raw text
lacks the substring, such as a quoted or escaped piece of the word, would slip
a substring selection, but only if it also named a newly read checkout.

The stronger point is that the replay cannot test the reorder at all. Phase 1
measured no recorded `checkout` naming a message search or a merge-base
shorthand, and phase 4 measured no name resolving only through a remote other
than `origin`. So the corpus holds no shape the 🟡 3 fix reorders, and
"0 moved" was the only possible result, whether the reorder is right or
wrong. The replay confirms the no-newly-read half, which the construction
above already gives. The reordered half rests on the construction and the 31
executed shapes, not on the replay. The counts themselves are unverified.

### Round 1's ⬜ 4, carried

`_without_bodies` is still the only reader of the module-level `tokens`
(`hooks/worktree-guard.py:831`), and the fix range touches none of the
functions whose parameter shadows it. Answered, as the record says.

## Regression tests to plant

The case for 🟡 1 goes in `tests/test_guard_resolves_the_tree_it_judges.py`,
after `test_a_guess_through_any_fetch_refspec_is_read_as_a_switch`. Its
fenced block is under *Paste-ready fixes* below. It was planted in the clone,
failed at 1eaccfc7, passed with the fix, and was reverted.

## Facts for the evidence ledger

- `git config --get-regexp` prints a subsection with its spaces, and git
  fetches and guesses through a remote named with a space although
  `git remote add` refuses one (executed, git 2.54.0).
- git's checkout guess ignores a negative fetch refspec, and does not guess
  through a refspec given only with `-c` (executed, git 2.54.0).
- git refuses a guess through a remote defined only by a legacy remotes file
  under the git directory (executed, git 2.54.0).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_fetched_as` splits each `git config --get-regexp` entry at its first space, so a remote whose name holds a space maps nothing while git guesses through it; the policy's "never the other way" and R5's "every remote" are false for it | `hooks/worktree-guard.py:1192` | open | executed: git created and switched, a3aa139a, 3a07c607 and 1eaccfc7 `None`, with a `-z` read `switch`, 11 other refspec shapes unchanged; the case red at 1eaccfc7 and green with the fix, module 419 passed |
| ⬜ 2 | A newly read checkout in a dirty second tree before a switch the base reads in a clean tree is silent (as at the base; 3a07c607 asked); §*Which tree* states the rule, §*Known limits* and the "keeps the first switch" paragraph do not | `docs/worktree-guard-spec.md:339` | open | executed through `main()` at three versions; no behaviour or fact wrong |
| ⬜ 3 | `main` runs the full `classify` after the base-only one, repeating its two calls, and runs it even after `newly_read` is set; 10 git calls where the base made 2 on an unresolvable name | `hooks/worktree-guard.py:2786` | open | executed: subprocess count 2 base-only, 8 full |
| ⬜ 4 | `test_a_newly_read_checkout_in_front_takes_no_question_away` says "Red at `85e77dc8`", and its two `:/nomatch` cases pass there | `tests/test_guard_resolves_the_tree_it_judges.py:2412` | open | executed: 2 failed, 2 passed with 85e77dc8's guard |
| 🟢 | round 1's 🟡 1 is closed: a message search holding `..` reads as a switch, and the object lookup adds no yes git refuses across 12 non-commit and ambiguous names | `hooks/worktree-guard.py:1072` | confirmed | executed at three versions against git's own checkout |
| 🟢 | round 1's 🟡 2 is closed for its two shapes and eight more (negative, multi-line, middle `*`, mirror, include, `/` in the name, no destination, legacy file); the one shape it misses is 🟡 1 above | `hooks/worktree-guard.py:1173` | confirmed | executed at three versions against git's own checkout |
| 🟢 | round 1's 🟡 3 is closed: round 1's probe is `ask` again, and no command of 31 is quieter than a3aa139a | `hooks/worktree-guard.py:2801` | confirmed | constructed path by path; executed through `main()` at three versions |
| 🟢 | `classify(..., base_only=True)` is a3aa139a's `classify`, so a command with no newly read checkout reads exactly as at a3aa139a and 3a07c607 | `hooks/worktree-guard.py:1302` | confirmed | read: the function's diff against the base; executed: 8 such commands unchanged at three versions |
| 🟢 | round 1's ⬜ 4 stays answered | `hooks/worktree-guard.py:831` | confirmed | read; the fix range touches no shadowing function |
| ❓ | The M3 replay's 581 and 1,044 pairs, and how they were selected | `phases/phase-4.md` | ❓ out of verified scope | the probe was deleted; by construction the corpus holds no shape the reorder touches, so its 0 tests nothing about the reorder; the smith answers the counts |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |

## Paste-ready fixes

### 🟡 1

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

Ledger row R5 then carries this case among its coordinates and the spaced
remote in its Executed cell. The policy sentence at
`docs/worktree-guard-spec.md:787-790` stands as written once the fix is in.
If the fix is declined, the justification route replaces "never the other
way" with:

```text
so it guesses where git would not, and the other way only for a remote whose
name holds a space, which `git remote add` refuses and a config can still
name.
```

### ⬜ 2 (optional)

A bullet for `docs/worktree-guard-spec.md` §*Known limits*, after the
`checkout`-name bullet:

```text
- A `checkout` only #790's lookups read as a switch is judged only where the
  frozen reading read no switch in the command (§*Which tree*), so one in a
  second tree, written before a switch the frozen reading reads, goes unasked
  as it did at the base. Judging it first instead took the question from the
  frozen reading's switch, which the base asked (round 1 of 1791163981, 🟡 3).
```

### ⬜ 3 (optional)

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

Needs a fix: yes — 🟡 1 (a remote whose name holds a space is read as no
remote by `_fetched_as`, and git guesses through it)

Loses a record or crashes: no

## Proof block

Opened in this round, in the clone at 1eaccfc7 unless noted:
`rounds/round-1-report.md` and `rounds/round-1.md` (in the worktree); the diff
of `hooks/`, `docs/`, `tests/`, `changelog.md` and `overview.md` over
85e77dc8..22563bc6; the diff of `hooks/worktree-guard.py` over
a3aa139a..1eaccfc7; `classify` at a3aa139a and at 1eaccfc7 side by side;
a3aa139a's `is_ref`; at 1eaccfc7, `_verified`, `_commit_named`,
`_object_named`, `_one_merge_base`, `is_ref`, `tracked_in_any_remote`, `_refs`,
`_fetched_as`, `_the_bases_lookup`, `_no_guess`, `main` from the walk to the
end of the switch ladder, `quiet`, the head of `wider_only_kinds`, and
`choose`'s signature; `hooks/cmdline_base.py#adds_a_worktree`;
`docs/worktree-guard-spec.md` around `:339` and `:770-800`; ledger rows R4,
R5 and R6; `phases/phase-1.md` M3 and `phases/phase-4.md`; spec rows A1, A2
and A4; the round 1 test block and the `run`, `_git` and `_commit` helpers in
`tests/test_guard_resolves_the_tree_it_judges.py`; `tests/conftest.py`'s
`load_hook_module`, `repo` and autouse fixtures; `bin/test`. Not opened:
`plan.md` beyond its M3 rows, `routing.md`, `questions.md`, `phases/phase-2.md`
and `phase-3.md`, and the rest of the ledger fragment.
