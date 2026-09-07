# 1788789330-the-update-notice-names-the-expensive-move — round 2 fixes

Target reviewed `279628b`. One fix commit, `db5b9cd`, plus the records commit
that carries this file.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `db5b9cd`. `README.md:325` now says `see above` and `README.ko.md:317` says `위 문단 참고`. Verified by construction rather than by reading the diff: the load paragraph sits at `README.md:314-319` and `README.ko.md:305-311`, and the fenced block that points at it opens at `README.md:323` and `README.ko.md:315` |
| 2 | fixed | Fixed twice; the second attempt is what shipped. **First, `db5b9cd`** — `db5b9cd`, and NOT with the report's paste-ready block. That block pins by naming four adversatives, so it closes a name rather than a class — executed: the same mutation with `yet` in place of `but` (M8) passes it, `1 passed`, exit 0. What shipped pins by POSITION: wherever a sentence names the newly installed version, the clause carrying that mention has to be the clause that calls the pairing unmeasured. Seen red against M6, M7 and M8 and against both controls, `1 failed` and exit 1 each time, baseline green **Then, `760ac3e`** — `760ac3e`, after the **orchestrator's own re-run** on `e678c47` — not a reviewer finding. A fourth mutation of the same shape survived the positional pin: `unmeasured, yet it is picked up`, appended inside the gap sentence. Reproduced here before anything was built on it — `bin/test tests/test_version_check.py -q` → `18 passed`, exit 0, with the notice telling a user the reload picks up the new install. The four predicates are deleted and `notice()`'s whole output is pinned as an exact string The first attempt's row is kept in the mutation table below rather than deleted, because the measurement that overturned it is what the ledger row records |
| 3 | fixed | `db5b9cd`. `README.md:182` reads *"shows a short notice naming `/specseal:update` and the two moves that load a release"*. The count is removed rather than corrected, so there is no number left to go stale — and what the sentence now claims is the fact `test_the_warning_names_the_cheap_move_before_the_expensive_one` already pins. `README.ko.md:178` carries no count and is left alone, which is the reviewer's own reading of the class |

## The mutations, and the positional pin `db5b9cd` first tried

Five, one at a time, each applied to `notice()` in place and reverted from
bytes held in the mutating script — never from `HEAD`, because the fixes were
uncommitted while this ran. `tests/__pycache__` and `hooks/__pycache__` were
cleared between every run.

**This table is the state at `db5b9cd`, kept because it is the measurement the
next section overturns.** The positional pin it records was itself replaced at
`760ac3e`; the table below the next heading is what stands.

| # | The mutation | Against the round-1 body | Against `db5b9cd` |
|---|---|---|---|
| M6 | the gap keeps its negation for two axes and hands the third back: *`hooks or agent definitions is unmeasured, but the version you just installed is picked up`* | **survived** (round 2's own probe) | killed — `exit=1`, *the gap names the newly installed version in a clause that does not call that pairing unmeasured* |
| M7 | the reload's own claim keeps its subject and scope and gains *`and out of the one you just installed`* | **survived** (round 2's own probe) | killed — `exit=1`, the same assertion naming *the reload's claim* |
| M8 | M6 with `yet` in place of `but` — written here, not by the round | not run | killed — `exit=1`. This is the one the report's paste-ready block lets through |
| C1 | the scope qualifier alone dropped | killed | killed — `exit=1`, the round-1 scope assertion |
| C2 | the third axis deleted from the gap | killed | killed — `exit=1`, *the gap leaves installed to silence* |

Baseline, unmutated: `exit=0`. After the loop, `hooks/version-check.py` was
compared byte for byte against the pre-mutation copy and is identical.

**Five killed is not the class closed, and this is the second time that
sentence has been written about this one case.** M9 below is the mutation none
of these five suggested.

## The third fix of one bug, and why the shape changed instead

The orchestrator re-ran the class on `e678c47` and found M9 alive. Reproduced
here first, on this tree, `hooks/version-check.py` restored byte-identical
afterwards:

| | Result |
|---|---|
| `bin/test tests/test_version_check.py -q` with M9 in place | `exit=0`, **`18 passed`** |
| the one case alone | `exit=0`, `1 passed` — **SURVIVED** |
| what a user then reads | *"…or the version you just installed is unmeasured, **yet it is picked up**, so restart for those."* |

It walks through both assertions because the negation sits on the NEAR side of
the adversative. The clause from `install` to the first comma is *installed is
unmeasured*, which carries the negation, and the hand-back happens in the next
clause that the split throws away. `yet` is not one of the four adversatives.
M6 and M8 both put the mention AFTER the adversative, which is the only reason
the split caught them.

**Counted on this work item, this is the third fix of one bug**, which is
where `CLAUDE.md`'s 3+ Fix Rule says to stop and look at the shape rather than
add to the list:

1. round 1 finding 2 — the case pinned words. Fixed by rewriting the case.
2. round 2 finding 2 — the rewrite pinned words one level down. Fixed by
   position plus a four-word adversative list.
3. this — the adversative list is word presence again, and the clause split is
   a fifth list wearing a different shape.

A predicate over English prose cannot enumerate the ways English has of
handing an axis back. So the notice is pinned as an **exact string** and the
four predicates are deleted. The pair of cases carries the guarantee together,
and the second half is what makes the pair work rather than the exact pin
alone: `test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads`
reads the module docstring, so an editor who updates the golden string
carelessly still has to contradict the file to overclaim. That is visible in
the table below — C1, the mutation that drops the scope phrase, is the one
mutation both cases kill.

**What this costs, accepted rather than discovered later:** a legitimate
rewording of the notice fails this case. The wording IS the contract here — it
is what a user reads about what was measured — so whoever rewords it states
the new text deliberately instead of satisfying a checker. The case docstring
says this in the file.

### The exact pin, seen red before it was committed

Six mutations, one at a time, `notice()` restored from bytes held in the
script. Baseline green on both cases first.

| Mutation | Exact pin | The docstring case |
|---|---|---|
| M6 — the gap hands the third axis back after `but` | `exit=1` killed | green |
| M7 — the reload's claim gains *and out of the one you just installed* | `exit=1` killed | green |
| M8 — M6 with `yet` for `but` | `exit=1` killed | green |
| **M9 — the orchestrator's, `unmeasured, yet it is picked up`** | `exit=1` **killed** | green |
| C1 — the scope qualifier alone dropped | `exit=1` killed | **`exit=1` killed** |
| C2 — the third axis deleted | `exit=1` killed | green |

Baseline: both cases `exit=0`. After the loop `hooks/version-check.py` is
byte-identical to the pre-mutation copy and `git status --porcelain` shows
only the test file.

## Why the paste-ready block was not taken as written

The report's block asserts two things about any sentence naming the new
install: that a negation word appears somewhere in it, and that none of
`" but "`, `" however"`, `" though "`, `" except "` appears. The second is a
list of four words standing in for a class, which is the shape
`agent-contract` §12 names — closing a class one name at a time.

Executed, in a `test_tmp_*` probe carrying the block verbatim and deleted after
one run: against M8 the block reports `1 passed`, exit 0. A notice telling a
user the reload picks up the new install would have shipped, one conjunction
over from the mutation the round found.

`db5b9cd` replaced the two assertions with a clause-position check and kept
the adversative list beside it. **Both are gone at `760ac3e`**, and the reason
they are gone is the section above: the clause split was a fifth list, and M9
went round it by moving the negation to the near side of the comma. This
section is kept because refusing the paste-ready block was right for a reason
that outlived the fix that replaced it — a list of four words cannot stand in
for a class — and the replacement made the same mistake in a different shape.

## Re-enumeration of this pass's own diff

Two classes, both re-derived by construction after the fixes landed.

**Finding 1's class — a direction word pointing at a passage this work item
moved.** Enumerated over every line the branch ADDS, not over every direction
word in the two READMEs: the branch only inserts, and an insertion cannot flip
a direction word unless the inserted text is itself the new referent. Three
shipping-file hits, all checked:

| Coordinate | Verdict |
|---|---|
| `README.md:325` | fixed here |
| `README.ko.md:317` | fixed here |
| `skills/update/SKILL.md:32` — *"neither move below is needed"* | **correct.** The two moves are the table at `:91-93`, below it |

Pre-existing direction words that point INTO a region this branch rewrote were
checked separately and both hold: `README.md:309` *"both commands below"* and
`README.ko.md:300` *"아래 두 명령"* name the fenced block at `:323-326` and
`:315-318`, still below them.

**Finding 3's class — a claim about the notice's shape that the branch made
more wrong.** `grep` for shape claims across `README.md`, `README.ko.md`,
`skills/update/SKILL.md`, `hooks/version-check.py`, `docs/flow.md` and
`CONTRIBUTING.md`. Three other *one line* claims exist and none is about this
hook: `README.md:178` is implementer-notice, `README.md:553` and
`README.ko.md:548` are `seal export`, `README.ko.md:342` and `:348` are the
commit gate and the 0.3.x move.

One near-hit was routed to the orchestrator and **the orchestrator answered
it**: `tests/test_version_check.py` said the docstring sits *"130 lines
above"* the string a user reads, in a docstring and in an assertion message.
Measured — the scoping sentence is at `:18-19` and the notice's reload
sentence at `:154-157`, so the true distance is 135. Answered the way
`README.md:182` was: **drop the number rather than correct it**, because the
sentence's point is distance and not arithmetic. Done at `760ac3e` — the
docstring now says the module docstring is at the top and the string a user
reads is near the bottom, so nobody editing one has the other on screen. The
assertion message carrying the other copy went with the predicates it lived
in. `grep -n '130' tests/test_version_check.py hooks/version-check.py` returns
nothing.

**What this pass introduced.** No new unit and no new mechanism. The diff
changes the assertion body of one existing case, corrects two docstrings, and
changes three sentences of documentation. Nothing in it is a fix to a unit an
earlier round's fixes created, so the depth rule is not reached — and
`760ac3e` **removes** four predicates rather than adding a fifth, which is the
whole of what it was for.

**A second consequence of deleting the predicates, also caught by a check
rather than by reading.** `reload_claim` was a local in the four predicates, <!-- NAME NOT IN TREE — this paragraph is about that local's removal, so it has to name it. -->
and round 1's report names it in prose. Deleting the local left a record
stating a name the tree no longer has, which `bin/evidence-check .` refused —
`exit=2`, `NOT-IN-TREE  …/rounds/round-1-report.md:162`. The record is not
rewritten, because it says what was true when round 1 wrote it; the line
carries `NAME NOT IN TREE` with the reason beside it, which is the second of
the two ways the checker itself names. `exit=0` after, `9 names read · 0
refused`.

**One defect this pass did introduce, caught by re-running the checks rather
than by reading the diff.** The first draft of the ledger Notes above cited
the load paragraph and the fenced blocks as `README.md:314-319` and
`README.ko.md:305-311`. `bin/evidence-check .` read those as coordinates and
returned `exit=2`, `2 old-format` — a ledger coordinate names content, never a
position, and the checker does not care that these sat in prose. Rewritten to
name the paragraph by its opening words in each edition; `exit=0`,
`776 ok · 0 drifted · 0 broken · 0 old-format`. The round-2 report itself
carries the same `path:line` form, which is correct there: round records are
not read by that checker.

## Verification

| What was run | Result |
|---|---|
| the five `db5b9cd` mutations, one at a time, `bin/test <the case> -q` | baseline `exit=0`; five mutants, five `exit=1`. Hook restored byte-identical |
| `bin/test tests/test_tmp_round2_reviewer_block.py -q` — the report's block verbatim against M8 | `exit=0`, `1 passed`. **The proposed block does not catch M8.** Probe deleted; `tests/` holds no `tmp` file |
| M9 reproduced against `e678c47`'s assertions | `exit=0`, **`18 passed`** — the orchestrator's claim holds |
| the six mutations against the exact pin at `760ac3e`, both cases each | baseline `exit=0` twice; six mutants, six `exit=1` on the pin. C1 also `exit=1` on the docstring case |
| `grep -n '130' tests/test_version_check.py hooks/version-check.py` | no output — the stale distance is gone from both copies |
| `bin/test tests/test_version_check.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py -q` | `exit=0`, `48 passed`, after every edit |
| `uvx ruff check` · `uvx ruff format --check` on `tests/test_version_check.py` | `exit=0` each. The one changed Python file, not a repository-wide lint |
| `bin/evidence-check .` | four rows DRIFTED before re-verifying — the two cases and the two README sections this pass edited — then `--reverify` and `exit=0` |

Read, not run: that `README.md:182`'s new wording is true of the rendered
banner. The claim it makes — that the notice names both moves — is what
`test_the_warning_names_the_cheap_move_before_the_expensive_one` asserts, so
it is derived from a pinned fact rather than pinned itself. No test opens a
README to check a sentence about a hook, and adding one would be mechanism a
fix pass may not add.

❓ out of verified scope: the full suite, the repository-wide lint and the
typecheck. `agent-contract` §2 reserves the broad gate to the orchestrator and
the spawn prompt ordered none. **The orchestrator answers it.**

## Nothing to drain

Round 2 deferred three items and this pass moves none of them. All three keep
the answerers `round-2.md` gives them.
