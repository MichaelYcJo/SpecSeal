# Round 3 report — 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token

| Field | Value |
|---|---|
| Round | 3, the verifying round over round 2's fixes, and the last round this item gets |
| Target SHA | 61e59b42 |
| Fix range checked | f659c466..e3cd4dc4 (round 2's record names it) |
| Base | `release/v0.18.3` at a3aa139a |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 61e59b42, under the session scratchpad (`<scratchpad>/<id>/round-3/clone`), removed at hand-over |

## Summary

Round 2's 🟡 1 is closed. Reading the fetch config NUL-separated is correct
by construction for every key and value shape git can hold, and it is
correct by execution over 26 config shapes against git's own `checkout`.
Round 2's ⬜ 2 and ⬜ 4 are closed, and ⬜ 3 stands as answered. The two new
policy sentences match what `main()` does at the target and at the base. The
`phases/phase-4.md` selection rule reproduces both of its counts exactly.

The whole-item pass found no shape quieter at the target than at the base:
29 command shapes in 4 session states, 116 runs through `main()` at three
versions.

There is one new finding, 🟡 1, and it is the class round 2's 🟡 1 belonged
to, one step further along. Two lines in units this run created read git's
output with Python methods that act on more characters than git does.
`_fetched_as` runs `str.strip()` over each fetch value, and `_refs` splits
`for-each-ref` output with `str.splitlines()`. Python strips and splits at
Unicode spaces and line separators, and git keeps them inside a ref name.
So a fetch refspec whose destination ends in one of them maps to a ref that
does not exist. git still guesses through it, and the guard is silent.

The finding is **not a regression against a3aa139a**. The base is silent on
every one of these shapes too, because it guessed from `origin` alone. Its
cost is that the policy's "never the other way" and ledger row R5's "as
git's guess does" are false for this shape. That is the same ground round 2
rated 🟡. Its reach is narrower than round 2's: a ref name has to end in a
non-ASCII space or line separator. The fix is two tokens, and it was
executed in the clone: red at the target, and the module green with it.

One ⬜ correction is about the run's paperwork. `phases/phase-4.md` states
"no recorded command holds a `checkout` that only #790's lookups read"
without the bound the paragraph above it states: 449 of the 972 pairs name a
directory that is gone, where nothing is read.

## How round 2's verdicts were checked

The fix range changes one hunk of `hooks/worktree-guard.py`, which is
`_fetched_as`'s read of the config (read: `git diff 1eaccfc7..61e59b42 --
hooks`). `classify`, `main`, `_commit_named`, `_object_named` and
`_one_merge_base` are byte-identical to 1eaccfc7. So round 2's 🟢 rows about
those units carry as coordinates, and this round re-derived them by
execution anyway: the refspec and `main()` probes below ran at a3aa139a,
1eaccfc7 and 61e59b42, each version's `hooks/` taken by `git archive` and
loaded in a process of its own.

- **🟡 1 (a remote whose name holds a space) — confirmed fixed.** Executed:
  git lands on the guess; a3aa139a and 1eaccfc7 answer `None` under both
  carriers; 61e59b42 answers `switch`. The new case
  `test_a_guess_through_a_remote_whose_name_holds_a_space` was run with
  f659c466's guard put back in the clone: it fails on `checkout N`, `None ==
  'switch'`. Its docstring's "Red at `f659c466`" is true.
- **⬜ 2 (the placement limit unstated) — confirmed fixed.** Both sentences
  are in the policy. The pin's first new assertion fails against f659c466's
  policy text (executed), and the second sentence is absent from that text
  (read, whitespace-normalised). What the sentences claim is checked through
  `main()` below.
- **⬜ 3 (the two-pass read's git calls) — stands as answered.** The fix
  range does not touch `main` (read).
- **⬜ 4 (a docstring calling two controls red) — confirmed fixed.** The
  docstring now says the two `:/base` cases were red at 85e77dc8 and the two
  `:/nomatch` cases are controls. That is what round 2 executed (read).
- **❓ (the M3 replay's counts) — now verified.** See the section on
  `phases/phase-4.md` below.

## Findings from execution

### 🟡 1 — A refspec destination that ends in a Unicode space or line separator maps to a ref that does not exist, and git guesses through it

Coordinates: `hooks/worktree-guard.py:1195` (`_fetched_as`, the
`.strip()` on each value) and `hooks/worktree-guard.py:1170` (`_refs`, the
`splitlines()`). The claims this falsifies are at
`docs/worktree-guard-spec.md:792` ("so it guesses where git would not, never
the other way") and in ledger row R5 ("maps `refs/heads/<name>` through every
remote's `remote.<remote>.fetch` refspec as git's guess does").

git's config reader strips only ASCII whitespace from an unquoted value, and
a ref name may hold any byte above 0x7f. Python's `str.strip()` also removes
U+00A0, U+0085, U+3000 and the other Unicode spaces. Python's
`str.splitlines()` also splits at U+0085, U+2028 and U+2029. So a fetch
value such as `+refs/heads/*:refs/ws/*` followed by a no-break space behaves
like this:

- git fetches `onfork` into `refs/ws/onfork` plus that trailing character.
- `git checkout onfork` creates the branch and switches through that ref.
- `_fetched_as` strips the character and maps `refs/ws/onfork`, which does
  not exist, so `tracked_in_any_remote` answers no.
- For U+0085 and U+2028 the `.strip()` is not the only cause. With it
  removed, `_refs` still splits the listed ref at the character, so the
  exact-match test still misses it.

Executed, git 2.54.0, scratch repositories:

| Destination ends in | git | a3aa139a | 1eaccfc7 | 61e59b42 |
|---|---|---|---|---|
| U+00A0 (no-break space) | lands | None | None | None |
| U+3000 (ideographic space) | lands | None | None | None |
| U+0085 (next line) | lands | None | None | None |

The same characters at the front of the value make git refuse, and every
version answers `None`.

Why it matters: this is a silent switch of #790's class C3, in two units
round 1's fix pass created (`_fetched_as` and `_refs`, both depth 1 in round
1's record). In a dirty or shared tree, the tree moves without a question.

Is it a regression? **No.** a3aa139a is silent on every row above, so the
guard is never quieter than the base here. It is pre-existing in what it
does, and new in what the policy now promises. Its reach is narrower than
round 2's 🟡 1: a person has to hand-write a refspec whose destination ends
in a non-ASCII space or separator. A config pasted from a formatted page is
the plausible route.

The fix is two tokens and adds no unit. Drop `.strip()` from `_fetched_as`
and split `_refs`'s output at `"\n"` alone. A ref name cannot hold a newline,
and a `-z` value carries no trailing one. Executed in the clone:

- the four-parameter case below is red at 61e59b42 (4 failed);
- with only the `.strip()` dropped, the U+0085 parameter is still red, which
  is what showed `_refs` belongs to the class too;
- with both lines, `tests/test_guard_resolves_the_tree_it_judges.py` passed
  423;
- with both lines, the 26 config shapes below were re-run. No shape git lands
  on reads less. Two shapes git refuses move from `switch` to `None`: a
  quoted value with surrounding spaces, and a value ending in an escaped
  newline. Both now match git.

**§12, the class enumerated.** The class is a unit this run created that
reads git's text output with a Python string method acting on more
characters than git separates on. The new units' reads of git output were
enumerated from `git diff a3aa139a..61e59b42 -- hooks/worktree-guard.py`:

| Unit | Read | Verdict |
|---|---|---|
| `_verified` | `stdout.strip()` of an object name | hex only, safe |
| `_object_named` | `stdout.strip()`, then a full match against an object name | hex only, safe |
| `_one_merge_base` | `stdout.split()` of merge bases | hex only, safe |
| `_refs` | `stdout.splitlines()` of ref names | **in the class** |
| `_fetched_as` | `split("\0")`, `partition("\n")`, `.strip()` | **in the class (`.strip()`)** |

`_refs` also feeds `tracked_in_any_remote`'s first test, a remote-tracking
ref ending in `/<name>`. A ref there holding U+2028 is split into two names.
That can only add a match git would not make, so it is louder, not quieter.
The split-at-`"\n"` fix removes it as well.

### `_fetched_as`'s `-z` parsing, by construction and by execution

`git config -z --get-regexp` prints each entry as the key, a newline, the
value and a NUL. A key with no value (`fetch` with no `=`) prints as the key
and a NUL.

- **A NUL** cannot sit in a key or a value. git holds both as C strings.
- **A newline in a key** is refused by git. Executed: `git config` rejects
  the key ("invalid key (newline)"), and a config file holding a quoted
  subsection with a newline is a fatal parse error for every git command.
  So the key always ends at the first newline, and `partition("\n")` cuts
  there.
- **A newline in a value** (an escaped `\n` in a quoted value) stays inside
  the value. git refuses such a refspec ("invalid refspec") and dies before
  it guesses. Executed in three shapes. Where the newline sits inside the
  only value naming the branch, every version answers `None`. Where a valid
  refspec stands beside it, the target answers `switch` while git refuses.
  That is louder.
- **An empty value** (`fetch =`) yields an empty spec with no `:`, skipped.
  git lands through the refspec beside it, and the target says `switch`.
  Executed.
- **A key with no value** yields an entry with no newline, so an empty
  spec, skipped. git refuses the whole config ("bad config variable"), and
  the target says `switch` through the valid refspec beside it. That is
  louder. Executed.
- **Several `fetch` keys on one remote** are several entries. With the third
  of three mapping the name through a middle-`*` glob, git lands and the
  target says `switch`. Executed.
- **A remote name with `.`, with `/`, with both and a `.fetch` inside it**,
  with two spaces and a tab, an empty subsection (`[remote ""]`), and the
  deprecated `[remote.Name]` form. The key is never read, only the value, so
  none of these can move the parse. Executed: git lands on all of them and
  the target says `switch`. A section with no subsection (`[remote]`) is not
  matched by the regexp, and git does not guess through it either.
- **A key in mixed case** (`[REMOTE "Up"]` with `FeTcH`). git prints it as
  `remote.Up.fetch`, the section and variable lowercased and the
  subsection kept. The regexp's first and last components are already lower
  case, so it matches. Executed: git lands, and the target says `switch`.

### The 26 config shapes at three versions (round 2's re-run, then this round's)

Each shape was built in a scratch repository with one bare remote holding a
branch nobody has locally. git's own `git checkout <name>` is the reference.
Both carriers, `checkout N` and `checkout N --`, answered alike in every row.

| Fetch config | git | a3aa139a | 1eaccfc7 | 61e59b42 |
|---|---|---|---|---|
| destination outside `refs/remotes/` | lands | None | switch | switch |
| partial glob inside `refs/remotes/` | lands | None | switch | switch |
| a negative refspec excluding the name, beside a mapping one | lands | None | switch | switch |
| two `fetch` lines, the second mapping the name exactly | lands | None | switch | switch |
| `*` in the middle of the destination | lands | None | switch | switch |
| whole-namespace mirror into a private prefix | lands | None | switch | switch |
| no destination, a ref left by an earlier fetch | refused | None | None | None |
| the refspec only in a config reached by `include.path` | lands | None | switch | switch |
| remote name holding a `/` | lands | None | switch | switch |
| a legacy remotes file under the git directory | refused | None | None | None |
| remote name holding a space (round 2's 🟡 1) | lands | None | None | **switch** |
| remote name holding two spaces and a tab | lands | None | None | **switch** |
| remote name holding a `.` | lands | None | switch | switch |
| remote name holding `.`, `/` and `.fetch` | lands | None | switch | switch |
| mixed-case section and variable, mixed-case subsection | lands | None | switch | switch |
| deprecated `[remote.Name]` section | lands | None | switch | switch |
| three `fetch` keys, the third mapping | lands | None | switch | switch |
| an empty value beside a mapping one | lands | None | switch | switch |
| a key with no value beside a mapping one | refused (bad config) | None | switch | switch |
| a value holding a newline, beside a mapping one | refused (invalid refspec) | None | switch | switch |
| the only mapping refspec after a newline inside one value | refused | None | None | None |
| a value ending in an escaped newline | refused | None | switch | switch |
| a quoted value with surrounding spaces | refused (invalid refspec) | None | switch | switch |
| a spaced remote, beside another remote's newline value | refused | None | None | switch |
| empty subsection, `[remote ""]` | lands | None | switch | switch |
| no subsection, `[remote]` | refused | None | None | None |

No row git lands on reads `None` at the target. No row moves toward `None`
between 1eaccfc7 and the target. Every row where the target says `switch` and
git refuses is the louder direction: the guard asks about a command that
would not run.

### The two new policy sentences, through `main()` at the target and the base

The sentences are at `docs/worktree-guard-spec.md:340-342` ("Since #790 the
first switch is the first the base's lookups read, and a `checkout` only
#790's lookups read takes the place only where they read none") and
`:797-802` (a newly read `checkout` in a second, dirty tree, written before a
switch the frozen reading reads in a clean tree, goes unasked, as at the
base).

The shape they describe was run through `main()` in five spellings: the
newly read `checkout` reaching the dirty tree through `-C`, through a `cd`
in a subshell, as a merge-base shorthand behind a `;`, written after the
switch, and through a guess on a spaced remote. All of them are rows P1 to
P4 and R14 below. In the single-session state each one is silent at
a3aa139a, at 1eaccfc7 and at 61e59b42, and the tree judged is the clean
session tree. In the idle, unusable and active states each one gets the
same deny at all three versions, about that same tree. So the sentences are
true. The second is also not specific to "before": written after the switch
(P2), the checkout goes unasked as well. The first clause, "judged only
where the frozen reading read no switch in the command", already covers
that, so this is not a finding.

### The whole-item pass of the never-quieter property

A probe test in the clone's `tests/` ran `main()` with the test module's
harness rebuilt for one version per process, on a fresh repository per case.
That keeps every version's choice marker apart. It covered 29 command shapes
× 4 session states (single-session, detection unusable, an idle session, an
active session), at a3aa139a, 1eaccfc7 and 61e59b42. Decisions were ranked
silent < ask < deny.

| Shape (mechanism, not spelling) | a3aa139a | 61e59b42 |
|---|---|---|
| P1–P4: newly read in a dirty second tree, base-read switch in the clean session tree, in four spellings | silent / deny ×3 | same |
| P5: newly read in a dirty second tree, then a switch only candidate C reads in the clean tree | ask (C) ×4 | ask (dirty tree) / deny ×3 |
| R1, R7–R9: newly read in the clean tree beside a C-only switch in a dirty tree, either order, `;`, subshell | ask (C) ×4 | ask / deny ×3 |
| R2, R12: newly read beside a base-read switch in a dirty second tree | ask / deny, second tree | same |
| R3, R4: newly read alone, dirty tree, through `-C` or not | silent ×4 | ask / deny ×3 |
| R5, R6: two newly read, either tree first | silent ×4 | silent or ask / deny ×3, the first one's tree |
| R10, R11: newly read with a creation, either order | ask (active) / deny | deny ×4 |
| R13: guess through a spaced remote in a dirty tree | silent ×4 | ask / deny ×3 |
| R14: the same, then a base-read switch in the clean tree | silent / deny ×3 | same |
| N1–N6: no newly read checkout (base switch, C-only switch, restore, search matching nothing, creation, dirty switch) | — | identical in all 24 runs |
| T1, T2: a token only a here-document body carries | silent (T1) or ask (T2) where the base read the body's token | deny |
| T3: a token typed beside a body | — | identical |
| T4: newly read, `[shared-tree-ok]` only in a body | silent ×4 | silent / deny ×3 |

**No run is quieter at 61e59b42 than at a3aa139a, 0 of 116.** The target
also equals 1eaccfc7 in every run except R13, where it is louder (round 2's
🟡 1 fix). Where the base asked candidate C's question and the target asks
through the ladder (P5, R1, R7–R9 in the single-session state), the
decision is the same `ask`. The ladder's every silent exit still goes
through `quiet()`, with `judged` empty when `past_the_base` is set, so C
keeps its question wherever the ladder says nothing (read:
`hooks/worktree-guard.py:2821-2829`, `:2961`, `:3004`, `:3138`).

## Findings from reading, checked by execution

### `phases/phase-4.md`'s selection rule reproduces both counts

Executed over every `*.jsonl` under this repository's Claude Code project
directory: 635 transcripts, 34 of them main sessions. Bash uses were read
from assistant tool calls, with each record's `timestamp` and `cwd`.

- **Cut 1.** Before 2026-10-03T11:06:22+09:00 there are 25,913 uses and
  25,741 distinct pairs, as phase 1 says. Of those, 581 contain `checkout`,
  `[worktree-ok]` or `[shared-tree-ok]`, which is exactly the record's
  figure.
- **Cut 2.** The corpus has grown since. Replayed in time order, it held
  36,937 pairs at exactly one moment, 2026-10-05T12:01:21+09:00, and 1,044
  of them were selected then. That moment falls between round 1's record
  (85e77dc8, 11:52) and the fix pass's last commit (22563bc6, 12:29). The
  record's pair of figures is consistent, and its "when the fix pass
  extracted the corpus" is true.

So the selection rule says what the replay selected. The counts are
re-checkable after all. The record says they are not, which is now
understated but harmless.

### ⬜ 2 — The replay paragraph's "no recorded command holds" has no bound

`seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/phases/phase-4.md:63-64`.

The paragraph says "no recorded command holds a `checkout` that only #790's
lookups read". I executed this over the 972 pairs containing `checkout` up to
the fix pass. Each `checkout` segment was read at 61e59b42 through
`walk_command`, `judgeable` and `classify` with and without `base_only`:
0 of 982 segment readings are newly read. But 449 of the 972 pairs name a
directory that is gone, where neither reading finds a ref. The paragraph
above it states that bound for the same corpus ("counted as unchanged, not
as measured"), and this sentence drops it. It is a statement in the run's
paperwork, so it is a correction and not a fix. One clause would close it.

## Regression tests to plant

- `tests/test_guard_resolves_the_tree_it_judges.py`: the four-parameter case
  in the paste-ready fix below. It ends the module, beside
  `test_a_guess_through_a_remote_whose_name_holds_a_space`. Seen red at
  61e59b42 (4 failed), and green with the two-line fix. The U+0085 parameter
  stays red with only the `.strip()` dropped.

## Facts for the evidence ledger

- R5: the new case and the two lines it pins, if 🟡 1 is fixed. The
  executed line: git 2.54.0 fetched into, and guessed through, a ref ending
  in U+00A0, U+3000 or U+0085, which `_fetched_as`'s `.strip()` and `_refs`'s
  `splitlines()` read as a ref that does not exist. If 🟡 1 is answered by
  narrowing the claim instead, R5's "as git's guess does" and §*Known
  limits*' "never the other way" need the same bound.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A fetch refspec whose destination ends in a Unicode space or line separator maps to a ref that does not exist: `_fetched_as` strips the value with `str.strip()` and `_refs` splits ref names with `str.splitlines()`, both at characters git keeps in a ref name, so git guesses and the guard is silent; "never the other way" and R5 are false for it. Not a regression: a3aa139a is silent too | `hooks/worktree-guard.py:1195` | open | executed: git lands on U+00A0, U+3000 and U+0085, and three versions answer `None`; the case is red at 61e59b42 (4 failed) and the module passes 423 with the two-line fix; 26 config shapes re-run with the fix, none git lands on reads less |
| ⬜ 2 | The replay paragraph says no recorded command holds a newly read `checkout`, without the gone-directory bound the paragraph above it states (449 of 972 pairs) | `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/phases/phase-4.md:63` | open | executed: 0 of 982 readings newly read at 61e59b42, 449 pairs' directories gone; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | round 2's 🟡 1 is closed — a remote whose name holds a space maps its refspec | `hooks/worktree-guard.py:1184` | confirmed | executed at three versions against git's own `checkout`, with 15 further key and value shapes; the case is red with f659c466's guard |
| 🟢 | round 2's ⬜ 2 is closed — the walk's paragraph and §*Known limits* state the placement limit, and both are pinned | `docs/worktree-guard-spec.md:340` | confirmed | executed: the pin is red against f659c466's policy; the described shape is silent at a3aa139a, 1eaccfc7 and 61e59b42 in five spellings |
| 🟢 | round 2's ⬜ 3 stays answered — the fix range does not touch `main` | `hooks/worktree-guard.py:2791` | confirmed | read: the fix range's one `hooks/` hunk is in `_fetched_as` |
| 🟢 | round 2's ⬜ 4 is closed — the docstring names which two cases were red | `tests/test_guard_resolves_the_tree_it_judges.py:2424` | confirmed | read, against round 2's executed 2 failed and 2 passed at 85e77dc8 |
| 🟢 | round 2's ❓ is answered — the replay's selection rule reproduces 581 of 25,741 and 1,044 of 36,937 | `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/phases/phase-4.md:49` | confirmed | executed over the 635 transcripts; cut 2's pair of figures holds at one moment inside round 1's fix pass |
| 🟢 | no shape is quieter at 61e59b42 than at a3aa139a — whole-item pass | `hooks/worktree-guard.py:2778` | confirmed | executed: 116 runs through `main()` at three versions, 0 quieter; 26 config shapes through `classify`, none quieter |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |

## Paste-ready fixes

### 🟡 1

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

### ⬜ 2 (optional, the run's paperwork)

```text
nothing more: no recorded command holds a `checkout` that only #790's lookups
read, of the pairs whose directory still exists (449 of the 972 `checkout`
pairs up to the fix pass name one that is gone, where neither reading finds a
ref; counted at round 3), so the replay never reached the reordering in
`main` that round 1's 🟡 3 added.
```

Needs a fix: yes — 🟡 1 (a refspec destination ending in a Unicode space or line separator is read as a ref that does not exist, in `_fetched_as` and `_refs`; not a regression against a3aa139a)
Loses a record or crashes: no

## Proof block

Files opened this round: `hooks/worktree-guard.py` (`_commit_named` through
`classify`, `_the_bases_lookup`, `_no_guess`, `already_asked`, `choose`,
`main` and its ladder to `quiet()`),
`tests/test_guard_resolves_the_tree_it_judges.py` (the harness `run`, the
helpers, `CARRIERS`, `MOVES`, every round 1 and round 2 case),
`tests/conftest.py` (`load_hook_module`, `_build_repo`, `repo`),
`docs/worktree-guard-spec.md` (§*Which tree*, the walk paragraph, §*Known
limits*), `phases/phase-4.md`, `phases/phase-1.md` (the corpus section),
`rounds/round-2.md`, `rounds/round-2-report.md`, the fix range's diff
including the ledger fragment, and `bin/test`.
