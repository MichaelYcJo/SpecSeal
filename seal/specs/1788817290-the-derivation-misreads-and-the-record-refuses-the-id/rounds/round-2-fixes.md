# Round 2 — fixes · `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (#211, #194, #227)

The fix pass is four commits from `59dc0e4`: `69a3967` for finding 1,
`df9a3d0` for finding 2, `1742dcf` for findings 3 and 4 and the riders, and
this record last. No terminal SHA is written here, because the commit carrying
this line cannot name itself.

Every finding was reproduced against the tree as it stood before anything was
edited, and every case was seen red before its fix.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `69a3967` |
| 2 | fixed | `df9a3d0` |
| 3 | fixed | `1742dcf` |
| 4 | fixed | `1742dcf` |

## The red I saw before each fix

**Finding 1 — the class is wider than the two placements the round named.**
The shipped predicate at `59dc0e4`, over a repository built for it:

    src/conftest.py         a_nested_fixture      runner_reached=True
    a/b/conftest.py         deep_fixture          runner_reached=True
    vendor/pkg/conftest.py  pytest_vendored_hook  runner_reached=True
    examples/conftest.py    example_fixture       runner_reached=True
    examples/conftest.py    pytest_addoption      runner_reached=True
    tests/vendor/conftest.py  vendored_under_tests  runner_reached=True

Seven members, not two, and the last one is the important one: a conftest
**inside** `tests/` with nothing collected under it. It reaches the arms on
the `tests/` gate rather than on the name, so a repair written as *under
`tests/`, OR a loaded conftest* — which is the shape the round's paste-ready
fix takes — leaves it saying `pytest only` where pytest imports nothing.
Executed against that shape as a sixth mutation below: it is killed by
`test_the_directory_decides_inside_tests_as_well` alone.

Then both new cases against the shipped predicate, `round_record.py` swapped
for `HEAD`'s bytes and restored from bytes kept in the script:

    test_a_conftest_nothing_is_collected_under_is_not_loaded  pytest only, wanted no call site found
    test_the_directory_decides_inside_tests_as_well           pytest only, wanted no call site found

`2 failed, 13 deselected`, exit **1**, `restored byte-identical: True`.

**Finding 2 — three of the four things adding `tests` uncovers were not the
two the round named.** `RIDER_ROOTS` widened by one word and nothing else:

    test_every_rider_carries_the_date_and_sha_it_was_verified_at   FAILED
    test_every_rider_stamp_names_a_commit_this_branch_can_reach    FAILED
    AssertionError: tests/test_a_rider_reaches_its_file.py: a rider with no verification stamp

The first offender is the check's OWN file: the moment `tests` joins the
roots, this file's prose about the marker enters the corpus it walks, and
`block.split("# RIDER:")` reads each mention as a rider. With the split
anchored on a comment line that opens with the marker, the next one is
`test_the_records_can_be_carried_out_and_in.py`, which carries a rider with no
stamp in any form. With that stamped, the next is
`test_the_printed_ledger_name_is_the_file_that_was_read.py`, stamped
`4581fe1`. Executed: `git merge-base --is-ancestor 4581fe1 HEAD` → **1**, and
against `origin/release/v0.9.1` → **1**. The round named neither of the last
two as unresolvable and named the first not at all.

**Findings 3 and 4 — both re-derived rather than taken from the round.** The
enumeration: **3052 top-level defs in 114 tracked `.py` files at `59dc0e4`**,
and **0 verdicts move** between the shipped predicate and the repaired one.
The `OLD_COORD_RE` timing, over all 1520 lines of `seal/ledger.md` and the
`seal/ledger/*.md` fragments, three runs each: the worst is **0.000533 s** on
the longest row in the corpus, 8831 characters at `seal/ledger.md:1356`, and
the 19 rows of 1150–1280 characters top out at **0.000178 s**. The round's
0.000537 s and 0.000172 s reproduce within noise. The rider's own
`0.009 s on a 1213-character row` is neither the worst row nor a time within a
factor of fifty of one.

## The boundary now, in a sentence the code implements

**A conftest is loaded by NAME, and the DIRECTORY decides whether pytest loads
it at all.** pytest imports a `conftest.py` for the test files collected at or
below its own directory — rootdir down to each collected file, `confcutdir`
defaulting to rootdir — so one with nothing collected under it is imported by
nobody and its fixtures and hooks are injected into nothing.

`conftest_is_loaded` asks exactly that of the tracked file list, and the
conftest arm **replaces** the `tests/` gate rather than sitting beside it. One
rule, at every placement:

| Placement | Loaded | Why |
|---|---|---|
| `conftest.py` at the root, tree has tests | yes | everything collected is below it |
| `tests/conftest.py`, tests under `tests/` | yes | the collected modules are its own directory's |
| `pkg/conftest.py`, tests at `pkg/tests/` | yes | colocated layout, and pytest loads it |
| `src/conftest.py`, tests under `tests/` | no | segregated layout, nothing collected under `src/` |
| `tests/vendor/conftest.py`, nothing collected below | **no** | inside `tests/` changes nothing pytest does |
| `other/conftest.py` beside a colocated `pkg/` | no | a sibling is not below |

That is `conftest_is_loaded`'s docstring, `runner_reached`'s third paragraph
and `docs/review-chain-spec.md` §*The fix surface* word for word.

**What is NOT repaired, and it is the same class one gate over.** A fixture in
an uncollected non-conftest module under `tests/` — `tests/helpers.py` holding
an `@pytest.fixture` — still reads `pytest only`, executed. Deciding it means
asking whether a conftest or a collected module imports the name, which is a
third question with an argument of its own, and this tree holds no instance:
measured over all 3052 defs, **0**. It is in `overview.md` §*Not verified*
with the repository owner named.

## The re-enumeration

`runner_reached`, shipped and repaired, over every top-level def in every
tracked `.py` file at `59dc0e4` — **3052 defs in 114 files**:

    verdicts that move: 0
    conftest.py in the tree: 1 -> ['tests/conftest.py'], conftest_is_loaded=True
    fixtures in an uncollected non-conftest module under tests/: 0

The conftest class in this repository is one file and it stays where it was.

## The mutation run

`conftest_is_loaded` is the only unit this pass added. Six mutations, one at a
time, `tests/__pycache__` cleared between, bytes kept in the mutating script
and restored from those bytes — never from `HEAD`, which would take the
uncommitted record edits with it. `restored byte-identical: True`.

| Mutation | First run | After |
|---|---|---|
| always loaded — the pre-fix behaviour | killed by 3 | killed |
| never loaded | killed by 3 | killed |
| drops `collected`, so any `.py` under the directory counts | killed by 3 | killed |
| the prefix loses its trailing slash | **SURVIVED** — 15 passed | killed by 2 |
| the gate stops asking, so the name alone lets a conftest through | killed by 3 | killed |
| the conftest arm sits BESIDE the `tests/` gate instead of replacing it | killed by 1 | killed |

The survivor is this fix's own blind spot and it is the same shape as round
1's: no two directories in the fixture repository had names where one extends
the other, so nothing was holding the difference between *below `src/`* and
*starts with `src`*. `src_extra/test_in_a_sibling.py` and
`test_a_sibling_whose_name_extends_the_directory_is_not_below_it` close it.

The last row is the round's own paste-ready fix, run as a mutation. It is
killed by `test_the_directory_decides_inside_tests_as_well`, which is why the
gate here is restructured rather than pasted.

## Finding 2 — what I changed, and how it merges with #239

Three parts, and the third is a judgment the round did not ask for.

1. `RIDER_ROOTS` gains `tests`.
2. The split anchors on a comment line that OPENS with the marker, so an
   assertion mentioning it is not read as a stamp-less rider. The marker is
   therefore never spelled out in a comment anywhere in that file — deliberate,
   because #239 opens a block at any comment line CONTAINING it, and prose
   about the convention would be a stamp-less rider there while passing here.
   Executed: without that care, #239's checker reports one BROKEN rider at my
   own explanatory comment.
3. `STAMP` accepts `against <anchor>@<hash>` beside `at <sha>`, and the
   ancestry case skips anchors.

**Part 3 is there because parts 1 and 2 walk into a wall without it.** Two of
the four riders `tests` uncovers cannot be given a commit-form stamp that
resolves: `3f8f846` and `4581fe1` are ancestors of neither `HEAD` nor
`origin/release/v0.9.1`, having been discarded by the squashes of the branches
that wrote them. That is #239 arriving as a corpus rather than as an argument
— the roots hole and the stamp-form defect are one defect seen from two sides,
which is why the same release opened both.

So the ancestry case gains an assertion that the corpus still holds at least
one commit-form stamp, and says in its own message what to do when that stops
being true: delete the case and let #239's checker own the rule. A check that
skips everything is a check that cannot fail.

**How it merges.** `fix/239-a-stamp-names-content-not-a-commit` moves the walk
to `.github/scripts/rider_check.py` over six roots — `.github` and `tests`
both — replaces `RIDER_ROOTS`, `STAMP` and `rider_stamps` in this file
wholesale, and migrates every stamp in the tree. Every hunk I wrote is inside
the block it replaces, so **whichever of the two branches merges second takes
#239's version**, and the resolution is one decision rather than a merge. What
is written here is the smaller change that keeps this branch's own rider
watched in the meantime, in the form the release ends in.

Cross-checked rather than assumed. #239's own `rider_check.py`, loaded from
its branch and run against this working tree:

    #239's checker over this working tree: ok=4 drifted=0
    problems on riders this branch touched: none

The four are exactly the four stamped here. The 18 remaining problems are
pre-#239 `at <sha>` stamps in `hooks/`, `agents/`, `templates/` and elsewhere,
every one of them migrated on that branch and none of them this branch's.

## The rider form, and where the round's paste-ready lines are wrong

Both riders now read `Verified <date> against <anchor>@<hash>`, and the two
lines the round supplied would not have parsed.

The round gives `…#floor_record@bba5c7a1` and
`…#OLD_COORD_RE@1ca5aff0`, with the path in front. The pattern on that branch
is `NEW_STAMP` · NAME NOT IN TREE, and it reads
`Verified <date> against <locator>@<hash>` where the locator is a dotted
symbol or a quoted line — **no path**, and its module docstring says so: *the
path the ledger writes is left off, and that is the only departure*, because a
rider IS the coordinate. The correct lines, and what is in the tree:

    # Verified 2026-09-08 against floor_record@bba5c7a1
    # Verified 2026-09-08 against OLD_COORD_RE@1ca5aff0

The two hashes reproduce. Computed here with that branch's own
`region_hash` · NAME NOT IN TREE, which
takes every rider block out of the anchored region before hashing it, against
this tree after the rider text was edited: `bba5c7a1` over the three lines of
`floor_record` and `1ca5aff0` over the four of `OLD_COORD_RE`. Both riders sit
above their regions rather than inside them, so correcting their prose moved
neither hash.

Two more stamps came from #239 rather than from me, because it had already
computed them and a second answer would be a second convention:
`test_a_manifest_field_of_the_wrong_type_does_not_raise@6afd8f9c` and
`test_the_refusal_above_can_actually_fail@8e0a246a`. Both recomputed against
this tree and both match.

**One thing the round said that does not hold, and it is worth correcting
because the reasoning is reusable.** The prompt gives as grounds that
`00e63c3` *is an ancestor of `origin/release/v0.9.1` and not of `main` — it
will be wrong again*. It will not: `CLAUDE.md`'s merge table fixes
`release/vX.Y.Z` → `main` as a **3-way merge commit**, which keeps every
commit the release branch holds, and `00e63c3` is one of them. The round's own
report says the same thing. The reason to move to a content anchor is the
convention the release is adopting and the two riders that cannot carry a
commit at all — not that this particular stamp decays.

## Findings 3 and 4 — every place that carries a number

**The enumeration.** 3052 is now what `round-1-fixes.md`, the ledger fragment
R2 and the `floor_record` rider all say, each with the per-commit counts
beside it so the number can be checked rather than believed: `ffd1d05` 3003 ·
`824bfca` 3051 · `4dfde1d` 3052 · `a283e64` 3052 · `59dc0e4` 3052. `3051` was
true at `824bfca`, where the enumeration ran, and stopped being true one
commit later; `3048` in that commit's message is in history the squash
discards and is not rewritten. The correction names WHEN each count was taken,
because a bare number with no tree beside it is what went stale.

**The measurement.** The `OLD_COORD_RE` rider carries the reproduced numbers
and says what it used to carry. The judgment not to repair is untouched and is
now stated with the margin it actually has.

## What no finding named

**The rider's own re-derivation claim was false, in two ways at once.** It
said the repaired predicate had been re-run over the tree and still found
`floor_record` the only unit reading `no call site found` for the
value-passing cause. Executed, per commit:

| Ref | `floor_record` | `timed_out` |
|---|---|---|
| `ba22b28` | `no call site found` | — not in the tree |
| `ffd1d05` | `no call site found` | — not in the tree |
| `824bfca` | `round-1-report.md, round-1.md` | `no call site found` |
| `59dc0e4` | `round-1-report.md, round-1.md` | `no call site found` |

Two independent things happened between round 1's target and its fix commit.
`floor_record` gained two call sites — this work item's own `round-1.md` and
`round-1-report.md`, which quote its `def` line verbatim in a paste-ready fix,
and `call_sites` greps every tracked file rather than the Python ones. And
`timed_out` arrived with the merge of `release/v0.9.1` as a new member of the
class.

**That a committed record quoting code invents a call site is a defect of
`call_sites`, and it is deferred rather than closed.** Closing it means a rule
about which files a reach walk may name, and a fix pass that adds a rule ships
it unread. It is in the rider, in the ledger fragment's R2 Notes, and in
`overview.md` §*Not verified* with the repository owner named.

**Every other sentence this branch wrote about its predicates, checked against
what they do.** Three more were false and are corrected: `round-1-fixes.md`'s
boundary paragraph and its cost paragraph, both of which said a conftest is
the runner's *wherever it sits*; `test_a_conftest_at_the_repository_root_is_
still_a_conftest`'s docstring, which said the `tests/` gate lets a conftest
through *from anywhere*; and `phases/phase-2.md`'s *one unit bounds the rule*,
which was true of the tree that phase ran against and is not true of the
branch. `plan.md`'s statement is about MEMBERSHIP rather than about the reach
value, and it is still true. A stale count in
`test_the_fixture_repository_changes_five_signatures_and_nothing_else` · NAME NOT IN TREE, renamed here.
It said five where round 1's own fix pass had taken it past five, which is
finding 3 one file over; the name now carries no number.

## What I ran

Every exit code was read with `; echo $?`, never through a pipe.

| What was run | Result |
|---|---|
| The shipped predicate over 13 built placements in two layouts | 7 conftest members read `pytest only` where pytest imports nothing — finding 1, five placements wider than the round named |
| The repaired predicate over the same | all 7 correct; the colocated `pkg/conftest.py` still `True`, the sibling `other/conftest.py` `False` |
| The two new cases against the shipped predicate, restored from bytes | **2 failed, 13 deselected**, exit **1**; `restored byte-identical: True` |
| `runner_reached` shipped and repaired over 3052 top-level defs in 114 tracked files at `59dc0e4` | **0 verdicts move**; 1 conftest in the tree, loaded |
| Fixtures in an uncollected non-conftest module under `tests/`, whole tree | **0** — the residual has no instance here |
| Six mutations of `conftest_is_loaded`, one at a time | 1 survived, then 0; `restored byte-identical: True` |
| `RIDER_ROOTS` widened by one word, nothing else | **2 failed** on the check's own file — a third offender the round did not name |
| `git merge-base --is-ancestor` for `3f8f846` and `4581fe1` against `HEAD` and `origin/release/v0.9.1` | **1** every time — neither can carry a commit-form stamp |
| `git merge-base --is-ancestor 00e63c3 origin/release/v0.9.1` | **0** — and `main` takes the release by 3-way merge, so it does not decay |
| #239's `rider_check.py` over this working tree | **ok=4 · drifted=0**; no problem on any rider this branch touched |
| #239's `region_hash` · NAME NOT IN TREE, for all four anchors | `bba5c7a1`, `1ca5aff0`, `6afd8f9c`, `8e0a246a` — all four reproduce |
| `OLD_COORD_RE` over 1520 real ledger lines, three runs each | worst **0.000533 s** at 8831 characters; the 19 rows of 1150–1280 top out at **0.000178 s** |
| `call_sites` for `floor_record` and `timed_out` at five refs | the survivor changed identity at `824bfca`; see the table above |
| `bin/test` — the reach, rider, reopening, printed-ledger and root-migrate modules | `120 passed, 1 skipped`, exit **0** |
| `bin/test` — the five generator modules | `227 passed`, exit **0** |
| `bin/test` — evidence-check, docs wrap, real identifiers, record-states, release hygiene, review axes | `142 passed`, exit **0** |
| `bin/test tests/test_the_records_can_be_carried_out_and_in.py` | `96 passed`, exit **0** |
| `bin/evidence-check` after re-verifying four drifted anchors | `815 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit **0** |
| `bin/deferral-check` | resolves, exit **0** |
| `uvx ruff check` and `uvx ruff format --check`, the seven changed `.py` | exit **0** and exit **0** |

**The four anchors that drifted were re-read before `--reverify` ran**, which
is what the repository rule asks: `round_record.py#runner_reached` and
`docs/review-chain-spec.md`'s fix-surface heading are this pass's own edits;
`docs/review-chain-spec.md`'s review-arm heading holds a claim about two opt-in
headings that the added paragraph names neither of; and
`test_the_refusal_above_can_actually_fail` holds a claim about a case that
cannot pass vacuously, where only a rider stamp inside its body moved.

## What is open, and who answers it

| Item | Who must answer |
|---|---|
| **The full suite, the repository-wide `ruff check` and the typecheck — unverified.** `skills/agent-contract/SKILL.md` §2 reserves the broad gate for one run after the rounds settle. What ran is the table above, narrowly | the orchestrator |
| **Which of `fix/239-a-stamp-names-content-not-a-commit` and this branch rewrites the other's rider block.** Both touch `tests/test_a_rider_reaches_its_file.py` on the same release; #239's version is strictly wider and every hunk here sits inside the block it replaces, so the resolution is to take #239's | the orchestrator |
| A committed record quoting a `def` line invents a call site for that unit, because `call_sites` greps every tracked file | the repository owner — `overview.md` §*Not verified* and the `floor_record` rider |
| A fixture in an uncollected non-conftest module under `tests/` still reads `pytest only` | the repository owner — `overview.md` §*Not verified*; no instance in this tree |
| Whether the four content-anchor stamps hold the hash they claim, on a later edit | `fix/239-a-stamp-names-content-not-a-commit` — its checker is what recomputes them; nothing in this tree does |
| `OLD_COORD_RE`'s cubic path half, carried as a `# RIDER:` with the corrected measurement | the repository owner |
| Whether `Contract changes` wants the narrowing to non-string literals | the repository owner — `questions.md` Q3 |
| Whether the two committed records that miscount their finding ids are corrected in place | the repository owner |

Nothing in the prompt asked for a check §2 excludes, so there is no declined
instruction to name.
