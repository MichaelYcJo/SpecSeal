# 1788789330-the-update-notice-names-the-expensive-move — round 2 fixes

Target reviewed `279628b`. One fix commit, `db5b9cd`, plus the records commit
that carries this file.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `db5b9cd`. `README.md:325` now says `see above` and `README.ko.md:317` says `위 문단 참고`. Verified by construction rather than by reading the diff: the load paragraph sits at `README.md:314-319` and `README.ko.md:305-311`, and the fenced block that points at it opens at `README.md:323` and `README.ko.md:315` |
| 2 | fixed | `db5b9cd`, and NOT with the report's paste-ready block. That block pins by naming four adversatives, so it closes a name rather than a class — executed: the same mutation with `yet` in place of `but` (M8) passes it, `1 passed`, exit 0. What shipped pins by POSITION: wherever a sentence names the newly installed version, the clause carrying that mention has to be the clause that calls the pairing unmeasured. Seen red against M6, M7 and M8 and against both controls, `1 failed` and exit 1 each time, baseline green |
| 3 | fixed | `db5b9cd`. `README.md:182` reads *"shows a short notice naming `/specseal:update` and the two moves that load a release"*. The count is removed rather than corrected, so there is no number left to go stale — and what the sentence now claims is the fact `test_the_warning_names_the_cheap_move_before_the_expensive_one` already pins. `README.ko.md:178` carries no count and is left alone, which is the reviewer's own reading of the class |

## The mutations, run against the shipped assertions

Five, one at a time, each applied to `notice()` in place and reverted from
bytes held in the mutating script — never from `HEAD`, because the fixes were
uncommitted while this ran. `tests/__pycache__` and `hooks/__pycache__` were
cleared between every run.

| # | The mutation | Against the round-1 body | Against what shipped |
|---|---|---|---|
| M6 | the gap keeps its negation for two axes and hands the third back: *`hooks or agent definitions is unmeasured, but the version you just installed is picked up`* | **survived** (round 2's own probe) | **killed** — `exit=1`, *the gap names the newly installed version in a clause that does not call that pairing unmeasured* |
| M7 | the reload's own claim keeps its subject and scope and gains *`and out of the one you just installed`* | **survived** (round 2's own probe) | **killed** — `exit=1`, the same assertion naming *the reload's claim* |
| M8 | M6 with `yet` in place of `but` — written here, not by the round | not run | **killed** — `exit=1`. This is the one the report's paste-ready block lets through |
| C1 | the scope qualifier alone dropped | killed | **killed** — `exit=1`, the round-1 scope assertion |
| C2 | the third axis deleted from the gap | killed | **killed** — `exit=1`, *the gap leaves installed to silence* |

Baseline, unmutated: `exit=0`. After the loop, `hooks/version-check.py` was
compared byte for byte against the pre-mutation copy and is identical.

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

What shipped keeps the loop and the `install` guard and replaces the two
assertions with:

- the clause running from the word `install` to the next `,`, `;` or `.` must
  itself carry the negation — so M6, M7 and M8 all fail, because in each of
  them that clause says the new install *is picked up* or says nothing;
- the adversative check is kept, because a sentence can pass the first
  assertion and still hand the axis back afterwards — *`installed is
  unmeasured, but it is picked up`*.

The sentence-wide negation assertion at `:126-129` is now implied by the
first of those. It is kept for its own failure message, and the comment above
the new block says so rather than leaving a reader to work it out.

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

One near-hit, checked and left: `tests/test_version_check.py` says the
docstring sits *"130 lines above"* the string a user reads, in a docstring and
in an assertion message. Measured — the scoping sentence is at `:18-19` and
the notice's reload sentence at `:154-157`, so the true distance is 135. It
was ~133 when this branch wrote it and the branch's own edits moved it by two.
A rounded distance reading *far enough apart that the contradiction is silent*
is not the kind of claim finding 3 was about, and rewriting it would widen a
fix pass into prose no finding names. **Answerer if it is ever worth pinning:
the orchestrator.**

**What this pass introduced.** No new unit and no new mechanism. The diff
extends one existing case, corrects one docstring to say which half of the
agreement it checks, and changes three sentences of documentation. Nothing in
it is a fix to a unit an earlier round's fixes created, so the depth rule is
not reached.

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
| the five mutations above, one at a time, `bin/test <the case> -q` | baseline `exit=0`; five mutants, five `exit=1`. Hook restored byte-identical |
| `bin/test tests/test_tmp_round2_reviewer_block.py -q` — the report's block verbatim against M8 | `exit=0`, `1 passed`. **The proposed block does not catch M8.** Probe deleted; `tests/` holds no `tmp` file |
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
