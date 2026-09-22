# Round 2 — the verifying round, over round 1's fixes

Target SHA `5a6ad96bfc8ac923dc4e6d55cf99195cf094df2b`, branch
`feat/458-the-shipped-specs-are-sediment-no-check-reads`, base
`origin/release/v0.13.0`, pull request 486. The surface is the fix range
`73ca11d14adffc688100bbc3a191e8a92ca8faa6..f27f7e864fe144597e16510601e1d5958d0ab2f5`
— `d5ea1d4a` carrying every fix and `f27f7e86` the ledger re-stamps — plus the
eleven units `close` recorded as new. Reviewed in a `git clone --no-local` at
the target SHA. HEAD was at the target SHA and the tree was clean.

## How this round came out

**Six of the seven fixes are right, including all three the fix pass departed
from the reviewer's patch on.** The departures were the sharpest thing to
check and each one holds: the reuse of `blank_fences` covers every fence shape
a policy document can carry, the rejection of `readable()` is correct by
measurement, refusing local mode is the better of the two readings, and
`retire` deriving its own candidate set is what keeps a destructive act
guarded by the tree rather than by a printed list.

**What is not closed is the other half of round 1's 🔴.** Round 1 named two
shapes under finding 1 — a marker inside a fenced block, and *a marker inside
a longer HTML comment block, a commented-out draft section*. The fix closed
the first and left the second, and the second still removes a work item's
directory at exit 0 with nothing absorbed. That is finding 1 below and it is
why this round's floor answer is yes.

The rest are what the fixes now tell a reader. One new sentence is false
(finding 2), one new refusal is undocumented (finding 3), one code comment
claims a reachability the code contradicts (finding 4), and two docstrings
have gone stale against the code beneath them (findings 6 and 7). Finding 5 is
the remaining instance of the class finding 1 belongs to, one function over in
the same feature.

---

## 🔴 1 · A marker in a commented-out draft still removes the directory

`skills/verify/scripts/unverified_check.py:668` — `folded_items`, which
`skills/settle/scripts/settle.py:468` loads and `:497` acts on with
`shutil.rmtree`.

**Executed.** A fixture repository with one released work item and a top-level
`docs/one-root.md` holding this:

```markdown
# a policy

A rule that IS agreed.

<!-- the draft section's opening marker, on a line of its own -->
Draft, not agreed yet — do not publish:

<!-- specs/1700000001-alpha -->
A sentence nobody signed off.
<!-- and its closing marker -->
```

`settle --retire` printed `removed seal/specs/1700000001-alpha/` and exited 0.
The directory is gone and the only prose that named the work item was
commented out.

**Why the fix does not reach it.** The fix routes every read through
`blank_fences`, which is the right reader for a fence and is blind to a
comment by construction. The constant's own comment at `:97-99` explains why
`readable()` was rejected — it blanks HTML comments and the marker is one —
and that reasoning is correct (confirmed below). What it does not say is that
declining `readable()` leaves the comment half of round 1's finding open.

**The two are one class, not two shapes.** `FOLD_MARKER` anchors the marker to
its own line and says nothing about whether the line is *live*. A fence is one
way a line stops being live; an enclosing comment is the other. Round 1 wrote
the second down — *the regex has no fence awareness anywhere, so a marker
inside a longer HTML comment block is also read on its own line* — under the
heading *Related, same reader*, and the record closed the finding `fixed`.

**What `strip_comments` cannot answer, and what can.** `readable()` blanks a
genuine marker to the empty string, so it really would erase every fold
record — measured, and quoted in the confirmations below. But the state
`strip_comments` tracks is exactly what tells the two apart: a genuine marker
line *begins* outside a comment, a marker in a commented-out draft begins
inside one. The fix below reads that state and nothing else, so it keeps the
fold record the marker is.

**Reachability is lower than the fenced shape and it is not nil.** Nothing in
this tree carries it today, and no shipped example shows it, which is the one
respect in which it is weaker than the shape the skill's own §2 demonstrates.
A session drafting a fold and commenting the section out until the wording is
agreed produces it in one keystroke.

---

## 🟡 2 · `The fold is complete.` is printed with the directory still there

`skills/settle/scripts/settle.py:482-490`.

**Executed.** A repository with `seal/specs/1700000001-alpha/` on disk, its
fold recorded in `docs/one-root.md`, and a release ref that does not hold the
directory:

```
nothing left to retire: docs/ records the fold of 1 work item, and none of
them still has a directory under seal/specs/. The fold is complete.
```

Exit 0, and `seal/specs/1700000001-alpha/` is still there.

**The condition does not match the sentence.** The arm fires on `if marked:`,
which asks only whether `docs/` records any fold at all. The sentence it
prints asserts something narrower — that none of the marked items still has a
directory — and nothing checked that. `candidates` was empty for a different
reason: the item is not released at the ref.

**This is round 1's finding 5 one step over.** That finding was *the report
telling a reader something the tree does not say*, and the repair for it
introduced a second sentence with the same defect. A reader who acts on *the
fold is complete* stops looking, and the directory the marker named stays in
the tree.

The state is reachable whenever a marker is written for a work item that is
not present at `--released-at`: a policy absorbing work that has not merged to
the release branch yet, or a run pointed at an older ref than the one the
items merged to.

---

## 🟡 3 · The new local-mode refusal is documented nowhere a reader looks

`skills/settle/scripts/settle.py:52-54` and `skills/settle/SKILL.md`.

**Read.** The module docstring enumerates what exit 2 means:

> Exit codes: 0 the report was produced, or the retirement ran · 1 a
> retirement was asked for and something refused it · 2 the arguments or the
> tree were unusable, which includes a `--released-at` ref that does not
> resolve, a root with no `seal/specs/`, and an interpreter below the floor.

The fix added a fourth exit-2 cause — a `seal/` root in local mode — and the
list still names three. `grep -n -i "local mode" skills/settle/SKILL.md`
returns nothing, so the one document a session reads before it folds does not
say that `settle` refuses to run at all in local mode.

**Why it matters more here than in an ordinary docstring.** §16 of the agent
contract makes local mode a first-class layout that every shipped script
resolves, and this command is now the one that refuses it. A person whose root
sits under the git directory meets a refusal that no document predicted, and
the enumerated list two screens up tells them their case is not one of the
three that exit 2. The message itself is good — it names the state and gives
`seal mode shared` as the way out, and that subcommand is real
(`bin/seal:12`). §14 asks for the other half.

---

## 🟡 4 · The comment says the local-mode sentence is reachable at last; it is not

`skills/settle/scripts/settle.py:552-560` against `:585-587`.

**Read.** The new block's comment closes with:

> So the state is named here, which is also what makes the sentence written
> for it reachable at last.

The sentence written for it is the clause inside the `--released-at` refusal
at `:585-587`: *In local mode the root is never committed, so no ref holds the
directories and there is nothing this can call released.* That branch fires
only when `released()` returns None, which is a ref that does not resolve. A
local-mode run now returns 2 at `:563`, before `survey` is ever called. The
clause is therefore **more** unreachable than it was, not less: round 1 found
it shadowed by a check that fired first, and the fix added a second check that
also fires first.

**Two things to correct and they are separable.** The comment states a fact
about the code that the code contradicts, and the clause at `:585-587` is dead
text inside a message about a different failure. A reader who hits a bad
`--released-at` is told about local mode for no reason, and a reader of the
comment is told the old sentence now prints.

---

## 🟡 5 · The same unfenced marker read is still in `coordinates`

`skills/settle/scripts/settle.py:299` — `MARKER_LINE_RE.match(line)` inside
`coordinates`, reading `seal/ledger.md` line by line.

**Read.** `coordinates` sections `seal/ledger.md` by marker line with no fence
tracking, which is the same reader shape finding 1 closed in `folded_items`.
A fenced example in `seal/ledger.md` carrying a marker opens a section, and
every coordinate after it is attributed to the id in the quotation until the
next marker or `## ` heading. The segment grouping the report prints is then
wrong for both work items.

**Not live, and cheap to close.** `seal/ledger.md` carries 94 marker lines and
zero fences today, so nothing is mis-sectioned. The sibling reader one
directory over already does it correctly: `.github/scripts/fold_ledger.py:158-170`
tracks a fence while scanning for headings, with a comment saying the work
item that wrote it measured the case.

§12 is the reason this is in the report rather than left out. Finding 1's
cause is *a line anchor is not a test that the line is live*, and this is the
second place in the same feature that produces it.

---

## 🟡 6 · `survey`'s docstring still claims the retirement is derived from it

`skills/settle/scripts/settle.py:354-359`.

**Read.** The docstring reads:

> Everything the report and the retirement are both derived from.
>
> One walk, so the two halves can never disagree about which work item is in
> which state — the failure mode a second traversal produces is a retirement
> removing a directory the listing had just called foldable.

`retire` now performs exactly the second traversal this warns against, and
says so in its own docstring at `:454-465`. The two docstrings contradict each
other, and the one that is wrong is the one a reader meets first.

**The behaviour is fine and the note is not.** The two do agree today, because
both derive the same intersection within one process. What the stale sentence
costs is the next edit: a session reading *everything the retirement is
derived from* has been told that `retire` may be simplified back to
`found["folded"]`, which is precisely the mutation that reopens the
unreachable-refusal defect. I reverted `retire` to that form and
`test_retire_refuses_an_item_the_guard_is_holding` went red, so the pin is
there — but the pin is not what a reader consults before editing.

While that sentence is being rewritten: `present` in the intersection at
`:472` is inert. `found["released"]` is already `[i for i in present if i in
on_base]`, so `released_at_base` is a subset of the `present` captured during
`survey`, and the only thing the third term can catch is a directory removed
between the two calls in the same process.

---

## 🟡 7 · An opted-out repository is told it has no work items

`skills/settle/scripts/settle.py:545-550`.

**Executed.** A repository with `seal/specs/1700000001-alpha/` in the tree and
the opt-out file `specseal-scratch` under its git common directory:

```
settle: <root> has no seal/specs/ at either place — nothing was read. This
command folds work items, and a repository with none has nothing to settle.
```

Exit 2. The directory is right there.

**The fix routed the resolution through `home_at`, which folds two states into
one return value.** `hooks/optin.py#home_at:200-201` returns `""` for the
opt-out as well as for a repository with no root, and the new `if not home:`
arm gives both the same sentence. Before the fix, `under(root, SPECS)` was
tested directly, so an opted-out repository with a shared root ran normally.

Refusing is defensible — the opt-out means this repository's gates are off —
but the sentence has to say which state it is in. Telling someone their
repository has no work items when it has ninety-eight is the defect finding 3
was, reached through the other door.

---

## ⬜ · The ledger fragment's S1 row counts eight parametrised shapes; there are seven

`seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3`
— *eight shapes are parametrised*.
`tests/test_unverified_rows_close.py:1352-1364`'s `parametrize` list has seven
entries, `x-1` through `x-7`, and the run confirms seven parametrised cases.
A correction rather than a fix: the row is paperwork, and every other claim in
it checks out.

---

## What I checked and found sound

**The reuse of `blank_fences` covers every shape, including the five named for
this round.** Executed, through the case's own parametrisation and through
mutation:

| Shape | `folded_items` returns |
|---|---|
| a ``` inside a ```` block | nothing — the inner fence does not close the outer |
| a `~~~` fence | nothing |
| an unclosed fence | nothing — the blanking runs to the end of the file |
| an indented fence | nothing; and an indented marker cannot match `FOLD_MARKER` anyway |
| a marker after a closed fence | the id, so the fix is not *find nothing ever* |

Reverting the call to `FOLD_MARKER.findall(text)` turns six cases red, four of
them parametrised shapes.

**The rejection of `readable()` is correct.** Executed against a genuine
marker: `readable()` returns `['', 'A standing statement.']` and
`blank_fences` returns `['<!-- specs/1780000000-work -->', 'A standing
statement.']`. Using `readable()` would erase every fold record there is,
exactly as the constant's comment says.

**Refusing local mode is the right reading, and the refusal is reachable.**
Resolving the root and proceeding would have left the second quiet zero the
fix pass names: `released` asks `git ls-tree` for `seal/specs/…` paths, an
uncommitted root has none in any tree, and every work item would read as
unreleased. The remedy the message names is real. Executed from a real
local-mode layout — `git init`, the root at `.git/seal/specs/<id>/`, nothing
in the tree — exit 2 with *which is local mode*, and reverting the resolution
turns two cases red.

**`retire` deriving its own candidate set is the right departure, and the
proof is a case the fix pass did not touch.** The prompt handed over that
`test_retire_refuses_an_item_the_guard_is_holding` was corrected. It was not:
`git log -L` over that function shows two commits, the feature commit
`b3ddd2b7` that wrote it and `d5ea1d4a` whose only edit in that hunk is the
docstring of the *next* function. The case stands as written, and reverting
`candidates` to `sorted(found["folded"])` — with the new guard-first ordering
in `survey` kept — turns it red. That is the reviewer's own patch failing
against an untouched case, which is the strongest form the grounds could take.

**The correction to `test_an_interrupted_run_resumes` is a repair, not a
weakening.** It changed `code == 1` / `"nothing to retire"` to `code == 0` /
`"The fold is complete."`. The old assertion pinned the conflation round 1's
finding 5 named — two markers still in `docs/`, both directories retired by
the run two lines above, and the command saying nothing had ever been folded.
The case still asserts an exit code and a specific sentence, and the state it
covers is unchanged; and the sibling case
`test_an_untouched_tree_still_says_nothing_has_been_folded` was planted to
hold the arm the edit vacated. Making the new arm unconditional turns that
sibling red.

**Every one of the eleven new units has a mutation that reddens it.**
Re-derived rather than carried; nine mutations, each reverted before the next:

| Mutation | Red |
|---|---|
| `folded_items` reads the raw text again | the fenced-block case, four parametrised shapes, the pasted-skill case |
| the `docs/` walk goes back to `os.walk` | the below-the-top-level case |
| the space before the comma returns | the printed-sentence case |
| `survey` asks the fold record before the guard | the skipped-and-named case |
| the complete-fold arm is removed | the interrupted-run case and the complete-retirement case |
| the complete-fold arm fires unconditionally | the untouched-tree case (and a pre-existing quoted-marker case) |
| the root resolution and the local-mode refusal are removed | the local-mode case and the no-root-at-either-place case |
| `retire` takes its candidates from `survey` | the guard-is-holding case |
| the raised-floor fixture copies the script alone | the above-the-floor interpreter case |

`OPTIN`, the eleventh new unit, is a constant and is covered by the root
resolution mutation.

**The five ledger re-stamps are real re-reads.** The three `seal/ledger.md`
rows all cite `unverified_check.py#main`, and the hash moved `b7493a67` →
`da6df86a`, so none of them is a bare re-stamp of an unchanged unit. Each note
names what actually changed in `main` — one space out of a printed line, and a
narrower fold record for the presence loop — and I checked that against the
diff: those are the only two changes reaching `main`. All three claims are
about the entry points, the missing-path arm and the merge-base resolution,
and a whitespace change touches none of them. The fragment's S1 and S4 both
moved their hashes too (`folded_items` `72d7e0e4` → `c8b16bbf`, `retire`
`0003e2b4` → `7fbbc05c`) and both notes carry the round's own evidence rather
than a re-stamp, including the mutations. The one thing wrong in the five is
the count in the ⬜ above.

**The third `## Not verified` row is true and the count holds.** Executed:
`unverified-check` over the work item, exit 0, `3 open · 1 closed`. The
corrected row no longer claims local mode's refusal was read from the code; it
says round 1 disproved that, names the fix, names the case that pins it, and
leaves *a second real repository* as what is still untried — which is true and
is what its answerer cell already named.

**The survivor judgement holds, with one nuance.** Executed:
`survivor-check --range origin/release/v0.13.0...HEAD` exits 0, so CI is
satisfied, and that is the range CI reads. Over the narrower fix range the run
reports eleven places, and I opened each. Eight are matches against the
`os.walk` loop the fix removed from `folded_items`, and the shared phrases are
`in os walk`, `sorted d for d in` and `if d not in skip dirs` — the generic
recursive-walk idiom in `evidence_check.py`, `rider_check.py`, `seal.py`,
`worktree-guard.py` and a test. The correction was about `docs/` being flat,
not about walking, so none of them carries a corrected statement. Two more
share only the variable name `found`. The eleventh is `settle.py:433`,
`report` still reading `found["folded"]` — and that one is not the idiom. It
survives correctly, because printing the survey's classification is what
`report` is for, but it is the seam finding 6 is about.

**The two deferrals were the right call.** #487 is a new mechanism — a walk
comparing two functions' source — that pins nothing findings 1 to 5 wrote, and
#488 is a rule change to two files one of which is the repository owner's; a
fix pass adding either would have been writing policy under a review round's
cover. Both findings hold as round 1 stated them and neither is reopened here.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A marker inside a commented-out HTML block still satisfies the removal guard — the half of round 1's finding 1 the fence fix does not reach | `skills/verify/scripts/unverified_check.py:668` · `skills/settle/scripts/settle.py:497` | open | executed — `settle --retire` removed `seal/specs/1700000001-alpha/` at exit 0 with the only prose naming it commented out |
| 🟡 2 | `retire` prints *The fold is complete.* at exit 0 while a marked work item still has its directory; the arm fires on `if marked:` and the sentence asserts something narrower | `skills/settle/scripts/settle.py:482` | open | executed — the message printed and the directory was still on disk |
| 🟡 3 | The new local-mode refusal is in neither the module's exit-code list nor `skills/settle/SKILL.md`; §14's other half | `skills/settle/scripts/settle.py:52` · `skills/settle/SKILL.md` | open | read — the list names three exit-2 causes and there are now four; a grep for *local mode* in the skill returns nothing |
| 🟡 4 | The new comment claims the local-mode sentence is *reachable at last*; that clause sits behind the `--released-at` refusal, which local mode now returns before | `skills/settle/scripts/settle.py:559` · `:585` | open | read — `:563` returns 2 before `survey` is called, so `released()` never returns None in local mode |
| 🟡 5 | `coordinates` sections `seal/ledger.md` by marker line with no fence tracking — the remaining instance of finding 1's class, where `fold_ledger.py` tracks one | `skills/settle/scripts/settle.py:299` | open | read — 94 marker lines and 0 fences in `seal/ledger.md` today, so it is reachable and not live |
| 🟡 6 | `survey`'s docstring still says the retirement is derived from it and warns against the second traversal `retire` now performs | `skills/settle/scripts/settle.py:354` | open | read — `retire:454-465` documents the opposite; `present` at `:472` is also inert |
| 🟡 7 | An opted-out repository is told it has no `seal/specs/` at either place; `home_at` returns `""` for the opt-out and for no root alike | `skills/settle/scripts/settle.py:545` · `hooks/optin.py:200` | open | executed — exit 2 with that sentence against a tree holding a work item directory |
| ⬜ 8 | The S1 row says *eight shapes are parametrised*; the list has seven | `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3` | open | read — `x-1` through `x-7`, and the run reports seven parametrised cases |
| 🟢 confirmation | Round 1 finding 1, the fenced shape: closed, across every fence shape named for this round | `skills/verify/scripts/unverified_check.py:668` | confirmed closed | executed — five shapes, and reverting the reader turns six cases red |
| 🟢 confirmation | The rejection of `readable()`: it really would erase every fold record | `skills/verify/scripts/unverified_check.py:97` | confirmed | executed — `readable()` blanks a genuine marker to the empty string |
| 🟢 confirmation | Round 1 finding 2, the recursive `docs/` walk: closed | `skills/verify/scripts/unverified_check.py:658` | confirmed closed | executed — the below-the-top-level case reddens on revert |
| 🟢 confirmation | Round 1 finding 3, and refusing local mode is the right reading of the two | `skills/settle/scripts/settle.py:545` · `:563` | confirmed closed | executed from a real local-mode layout; proceeding would leave the second quiet zero |
| 🟢 confirmation | Round 1 finding 4, and `retire` deriving its own candidate set is sound | `skills/settle/scripts/settle.py:376` · `:472` | confirmed closed | executed — reverting the candidate set reddens `test_retire_refuses_an_item_the_guard_is_holding`, a case the fix pass did not touch |
| 🟢 confirmation | Round 1 finding 5, and the correction to `test_an_interrupted_run_resumes` is a repair | `skills/settle/scripts/settle.py:482` · `tests/test_settle_reads_before_it_removes.py:244` | confirmed closed | executed — the vacated arm was planted as its own case, red when the new arm fires unconditionally; see finding 2 for what the repair introduced |
| 🟢 confirmation | Round 1 finding 7, the space before the comma | `skills/verify/scripts/unverified_check.py:894` | confirmed closed | executed — the case reddens on revert |
| 🟢 confirmation | Round 1 finding 8, the `Ran by` row | `overview.md:83` | confirmed closed | read — the row is ✅ and `unverified-check` counts it closed |
| 🟢 confirmation | Every one of the eleven new units reddens under a named mutation | `tests/test_settle_reads_before_it_removes.py` · `tests/test_unverified_rows_close.py` · `tests/test_a_script_says_which_interpreter_it_needs.py` | confirmed | executed — nine mutations, re-derived rather than carried |
| 🟢 confirmation | The five ledger re-stamps are real re-reads against the edit that drifted each row | `seal/ledger.md` · `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md` | confirmed | read — `main` moved `b7493a67` → `da6df86a`; every note names what changed and it matches the diff |
| 🟢 confirmation | The corrected `## Not verified` row is true and the count still passes | `overview.md:82` | confirmed | executed — `unverified-check` exit 0, 3 open · 1 closed |
| 🟢 confirmation | The orchestrator's survivor judgement over the fix range | the eleven places the fix-range run names | confirmed | executed — branch-range run exit 0; eight are the `os.walk` idiom, two are the name `found`, the eleventh is `report` reading `found["folded"]`, which is correct |
| ⬜ | Round 1 finding 6, deferred to #487 — the deferral was the right call | `skills/settle/scripts/settle.py:218` | deferred #487 | already deferred in round 1; a walk comparing two functions' source pins nothing findings 1–5 wrote |
| ⬜ | Round 1 finding 9, deferred to #488 — the deferral was the right call | `CLAUDE.md` §*a change writes fragments, never the shared file* | deferred #488 | already deferred in round 1; a rule change to the repository owner's file |
| ❓ scope | The broad gate | whole tree | ❓ out of verified scope | §2 gives it to the sealer and the prompt withholds it; the orchestrating session answers |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_settle_reads_before_it_removes.py tests/test_unverified_rows_close.py -q` at the target SHA | `145 passed`, exit 0 read directly — the baseline the mutations run against |
| nine revert-mutations, each restored before the next, against the module that should catch it | every one red; the table above names which case each reddened |
| `settle --retire` against a fixture whose top-level `docs/` document carries the marker inside a commented-out draft block | `removed seal/specs/1700000001-alpha/`, exit 0 — finding 1 |
| `folded_items` over a `docs/` holding a commented-out marker, a genuine marker and a fenced marker | `{'1780000000-work'}` from the comment as well as the genuine one — finding 1 |
| `readable()` and `blank_fences` over a genuine marker line | `readable()` → `['', 'A standing statement.']`; `blank_fences` → the marker intact — the rejection is correct |
| `settle --retire` against a fixture with a marked work item present on disk and absent at the release ref | `The fold is complete.`, exit 0, directory still present — finding 2 |
| `settle` against a fixture with `seal/specs/` in the tree and `specseal-scratch` under the git common directory | exit 2, *has no seal/specs/ at either place* — finding 7 |
| both proposed fixes applied together, then the two modules re-run | the two shapes close, exit 1 in each, and `145 passed` holds — the patches below are what was run |
| `unverified-check seal/specs/1790027178-…` | exit 0, `1 overviews · 3 open · 1 closed · 0 unreadable` |
| `survivor-check --range origin/release/v0.13.0...HEAD` | exit 0, *no removed wording is still standing* |
| `survivor-check --range 73ca11d1..f27f7e86` | exit 1, eleven places; each opened and judged — the orchestrator's reading upheld |
| `git log -L` over `test_retire_refuses_an_item_the_guard_is_holding` | two commits, neither changing the case — the prompt's claim that it was corrected does not hold |
| the four modules the fixes touched plus `test_chain_hooks_hardening.py` | not run in this round — the orchestrator executed them at this SHA, `216 passed`, and handed the result over |
| the broad gate — full suite, repository-wide lint and typecheck | not yet. §2 assigns it to the sealer, after the rounds settle |

Every probe ran in a `git clone --no-local` at the target SHA, against
throwaway fixture repositories built and removed by the probe scripts. The
probe files are deleted and the clone's working tree was restored to the
target SHA after every mutation.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `open_rows` duplicated with nothing holding the two copies in step | already deferred in round 1 to #487 | the work item #487 opens |
| `CLAUDE.md`'s ledger exception naming removal only | already deferred in round 1 to #488 | the repository owner |
| `settle` against a second real repository | already deferred in `overview.md` §*Not verified* | the repository owner, the next time the plugin is used elsewhere |
| whether the six population floors are still six after a fold | already deferred in `overview.md` §*Not verified* | the work item that folds this repository's own 97 |

## Paste-ready fixes

Finding 1 — tell a live marker from one inside a commented-out block, in
`skills/verify/scripts/unverified_check.py`. Add above `readable` at `:201`:

```python
def opens_outside_a_comment(lines):
    """True for each line that BEGINS outside an HTML comment.

    `strip_comments` cannot answer this, and `readable` is why it cannot be
    used here: it blanks a comment's content, and a fold marker IS a comment,
    so a genuine record and a marker inside a commented-out draft both come
    back empty. What tells the two apart is the state the line STARTED in.
    Measured 2026-09-22: a `docs/` document with a draft section commented out
    around a real marker retired the directory at exit 0, nothing absorbed.
    That is the other half of the shape the fence blanking closed — a fence is
    one way a line stops being live and an enclosing comment is the other."""
    out, inside = [], False
    for line in lines:
        out.append(not inside)
        rest = line
        while rest:
            if inside:
                end = rest.find("-->")
                if end == -1:
                    rest = ""
                else:
                    rest, inside = rest[end + 3 :], False
            else:
                start = rest.find("<!--")  # -->
                if start == -1:
                    rest = ""
                else:
                    rest, inside = rest[start + 4 :], True
    return out
```

The quotation of a comment opener in the patch above carries a closing
marker in a trailing Python comment. Without it that quotation opens a
comment in this report itself and blanks everything below — finding 5's own
class, met in a third reader while writing this round's record.

and replace the read at `:668`, inside `folded_items`:

```python
        lines = blank_fences(text.splitlines())
        for bare, line in zip(opens_outside_a_comment(lines), lines):
            if bare:
                found.update(FOLD_MARKER.findall(line))
```

The blanking runs first, so a comment opener inside a fenced example cannot
open a comment that hides a real record after it.

Finding 2 — make the condition match the sentence, in `retire` at `:482-490`:

```python
        stranded = sorted(marked & present)
        if marked and not stranded:
            out.write(
                f"nothing left to retire: docs/ records the fold of "
                f"{len(marked)} work item{plural(len(marked))}, and none of "
                f"them still has a directory under {SPECS}/. "
                "The fold is complete.\n"
            )
            return 0
        if stranded:
            # The sentence above asserts that no marked item still has a
            # directory, and the arm used to fire on `if marked:`, which never
            # asked. An item marked in `docs/` and still on disk reaches here
            # when it is not present at `--released-at` — a policy absorbing
            # work that has not merged yet, or a run pointed at an older ref.
            out.write(
                f"nothing to retire: docs/ records the fold of "
                f"{len(stranded)} work item{plural(len(stranded))} whose "
                f"directory is still under {SPECS}/, and none of them is "
                f"present at the release ref, so nothing here reads as "
                "released:\n"
            )
            for work_item_id in stranded:
                out.write(f"    {work_item_id}\n")
            return 1
```

Finding 3 — name the fourth cause, in the module docstring at `:52-54`:

```python
Exit codes: 0 the report was produced, or the retirement ran · 1 a retirement
was asked for and something refused it · 2 the arguments or the tree were
unusable, which includes a `--released-at` ref that does not resolve, a root
with no `seal/specs/` at either place, a `seal/` root in local mode, and an
interpreter below the floor.

**Local mode is refused rather than reported on.** The root under the common
git directory is never committed, so no ref holds the work item directories,
nothing in them reads as released, and nothing removed from them could be
recovered. `seal mode shared` moves the root into the tree.
```

and a row in `skills/settle/SKILL.md` beside the command forms, so the one
document a session reads before it folds says the same thing.

Finding 4 — correct the comment at `:557-560` and drop the dead clause at
`:585-587`:

```python
    # named here. The sentence written for local mode lives behind the
    # `--released-at` refusal below, and it stays unreachable — that branch
    # fires only for a ref that does not resolve, and this returns first. So
    # the clause is removed from there and the state is stated here instead.
    # It is the right answer as well as the honest one: nothing removed from a
    # root git never held can be recovered.
```

```python
            f"settle: --released-at {args.released_at} does not resolve in {root} — nothing was "
            "read. Without it every work item reads as unreleased and this "
            "would report nothing to fold, which is the one answer it must "
            "not give by accident.\n"
```

Finding 5 — track the fence in `coordinates` at `:296-305`, the way
`fold_ledger.py:158-170` does:

```python
    if os.path.isfile(ledger):
        with open(ledger, encoding="utf-8") as f:
            current, fence = None, None
            for line in f:
                head = line.lstrip()
                run = re.match(r"^(`{3,}|~{3,})", head)
                if fence is None and run:
                    fence = run.group(1)
                    continue
                if fence is not None:
                    if run and run.group(1)[0] == fence[0] and len(run.group(1)) >= len(fence):
                        fence = None
                    continue
                # A fenced example is a quotation, so a marker inside one opens
                # no section. `fold_ledger.py#section` already reads the file
                # this way; this is the same rule, and it is the shape round 1
                # found in `folded_items` one function over.
                marker = MARKER_LINE_RE.match(line)
```

Finding 6 — say what the two halves now are, in `survey`'s docstring at
`:354-359`:

```python
def survey(root, ref):
    """What the report is derived from, and where the retirement gets released.

    One walk for the listing, so no work item appears in two of its lists.
    The retirement does NOT take its candidates from here: `retire` reads the
    markers, the directories and the guard from the tree again, because a
    classification made for a printed list is not a guard on a destructive
    act — see its docstring. What it does take from here is `released`, which
    only git can answer and which this has already asked.
    """
```

and drop the inert third term at `:472`:

```python
    candidates = sorted(marked & released_at_base)
```

Finding 7 — tell the opt-out apart from an absent root, at `:545-550`:

```python
    home = load(OPTIN, "specseal_optin").home_at(root)
    if not home:
        # `home_at` returns "" for two states: no root at either place, and a
        # repository that opted out with the scratch marker. They used to
        # share one sentence, and a repository holding ninety-eight work items
        # was told it had none.
        common = load(OPTIN, "specseal_optin").git_common_dir(root)
        if common and os.path.isfile(os.path.join(common, "specseal-scratch")):
            sys.stderr.write(
                f"settle: {root} has opted out — the scratch marker is under "
                "its git directory, so every gate in this plugin is off here "
                "and this command will not remove anything. Delete the marker "
                "to turn them back on.\n"
            )
            return 2
        sys.stderr.write(
            f"settle: {root} has no {SPECS}/ at either place — nothing was "
            "read. This command folds work items, and a repository with none "
            "has nothing to settle.\n"
        )
        return 2
```

The ⬜ takes no patch: *eight shapes* becomes *seven shapes* in the S1 row.

Needs a fix: yes — findings 1 through 7. Finding 1 is the fold's only safety
property and is round 1's own 🔴 half-closed; 2, 3, 4 and 7 are what the new
code tells a reader; 5 is the same class one function over; 6 is the docstring
that invites the next editor to undo finding 4's repair.
Loses a record or crashes: yes — finding 1 removes a work item's directory
under `seal/specs/` with no policy document having absorbed it, measured at
exit 0, which is the one loss `skills/settle/SKILL.md` §4 says nothing can
undo.

## Proof block

Opened in this round:
`seal/specs/1790027178-…/rounds/round-1.md` and `rounds/round-1-report.md`;
`seal/specs/1790027178-…/overview.md`;
`seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`;
the fix range's diff of `seal/ledger.md`;
`skills/settle/scripts/settle.py` in full;
`skills/verify/scripts/unverified_check.py:78-120`, `:151-215`, `:630-700`,
`:880-900`;
`hooks/optin.py:155-206`;
`.github/scripts/fold_ledger.py:130-180`;
`tests/test_settle_reads_before_it_removes.py`;
`tests/test_unverified_rows_close.py:1325-1434`;
the fix range's diff of `tests/test_a_script_says_which_interpreter_it_needs.py`;
`seal/config.md`; `bin/seal:1-20`; `CONTRIBUTING.md:25-145`.

Not opened: `skills/settle/SKILL.md` beyond a grep for *local mode* and its
marker example; `phases/*.md`; `spec.md`; `plan.md`; `questions.md`;
`changelog.md`; `.github/scripts/gather_changelog.py`;
`tests/test_chain_hooks_hardening.py`.
