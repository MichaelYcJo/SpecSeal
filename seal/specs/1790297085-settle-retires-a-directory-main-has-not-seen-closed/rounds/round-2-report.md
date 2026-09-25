# 1790297085 — review round 2 report (verifying round)

Target: `6576a226622cf1faed896ee164dcde435bdc5743`. Fix range read:
`32993c08..9b5f7be9` (c5e06d26, 51564382, becf6b12, 9b5f7be9), plus the
record-closing commit 6576a226. The surface is that diff, the units round 1's
`New units` row names, and the three corrections the fix pass widened beyond
round 1's list.

## Summary

Round 1's five fixed or answered findings hold in the code: the moved-base
heading, the shallow-clone sentence, the report's no-base refusal and the
per-sibling purpose case are each right, and each case goes red when its fix
is taken out. Two things are not closed, and both are the class round 1
opened: what `settle` says about where CI asks.

- The correction of "CI asks where `--released-at` and `HEAD` meet" reached
  the changelog, the ledger, the policy, plan.md and questions.md, but not
  the two README cheat-sheet rows or `skills/settle/SKILL.md`. Those are the
  shipped documents a person reads, and they still say it (🟡 1).
- The fix pass added a new guarantee in its place: past the fork, `settle`
  "keeps more and never less" than CI. An executed probe breaks it. If the
  base adds an open record file to the directory after the fork, `settle
  --retire` removes the directory at exit 0, and `unverified-check` on the
  pull request's merge ref exits 1 (🟡 2). The same sentence is in four
  paperwork files (⬜ 3).

## Findings

### 🟡 1 — The README rows and the skill still say CI asks where `--released-at` and `HEAD` meet

`README.md`'s `settle [--retire]` row ends *"still open where `--released-at`
and `HEAD` meet, because that is where CI asks"*. `README.ko.md` ends its row
the same way (*"CI 가 그 지점에서 확인하기 때문입니다"*). `skills/settle/SKILL.md`
§1 says the CI readers ask *"of the merge base of that pull request's base and
`HEAD`"* and goes straight on to *"So `settle` asks the predicate of the merge
base of `--released-at` and `HEAD`"*, which reads as one revision. Neither
document says what to do when the base has moved.

Once `--released-at` has moved past the fork, CI's merge base is the base's
tip and not the fork. `.github/workflows/hygiene.yml` checks out the merge
ref and has no `ref:` line, and round 1 measured the merge base there. The
fix pass corrected this claim at the changelog fragment, ledger M2, 0.14.0
D3, plan.md, questions.md and `docs/the-evidence-ledger.md`. The two
cheat-sheet rows and the skill are the same claim in shipped documents, and
they were not in either list. That is `agent-contract` §12: a class fixed at
the coordinates it was pointed at. It is 🟡 rather than ⬜ because the
sentence is false in the moved case, not just badly worded. The skill is
also the procedure a session follows, and it names no merge.

Found by reading (a grep for the claim across the files this branch touches).

### 🟡 2 — "Keeps more and never less" is false; a file the base added after the fork is retired here and refused by CI

`skills/settle/scripts/settle.py`'s module docstring (the #602 paragraph) and
the comment above `main`'s no-merge-base refusal both say that past the fork,
asking at the merge base of `--released-at` and `HEAD` *"keeps more and never
less"* than CI. The claim holds only for a closure the base took after the
fork. It fails when the base adds a record file to the directory after the
fork. The branch never had that file and deletes nothing that conflicts with
it, so the merge ref carries it cleanly into a directory CI then reads.

Executed, in a one-file probe (deleted): a released spec-less directory,
closed. `work` forks, and `main` then adds an `evidence-todo.md` with an open
row to that directory. On `work`, `settle --retire --released-at main`
removed the directory at exit 0 (*"retired by the rule, with no marker"*).
Merging `work` into `main` (what the pull request's merge ref is) succeeded
with no conflict and left only `evidence-todo.md` in the directory. The
merge base of `main` and that merge was `main`'s tip. `retired_by_rule` there
was False. `unverified_check.py --baseline main seal/specs/` on the merge
exited 1, because `overview.md` is present at `main` and not at the merge. A
`spec.md` added on the base behaves the same way through `wrote_a_spec`
(read, not run).

This was already true of the design, so the code has no new bug. But plan.md's
rejected-alternative row says the fork point keeps more, never less, only *"in
every flow this repository uses"*. The fix pass dropped that limit and wrote
the guarantee without it into the code and the changelog, where the next editor
will rely on it and not add a guard. The paste-ready fix states the
asymmetry. Making the guarantee true is a different change: past the fork,
also ask the predicate at `--released-at`'s own commit and retire only where
all three say yes. plan.md's rejected row weighed that choice, and this round
leaves it there.

### ⬜ 3 — Paperwork: the same two claims under `seal/`

The same two claims appear in the work item's own files and the ledger.
These are corrections, outside `Needs a fix`.
- *never less*: `changelog.md` #602 entry (*"keeps more, never less, when it
  has"*, which ships as `CHANGELOG.md` prose), plan.md's chosen row
  (*"`settle` keeps more and never less"*), `seal/releases/0.14.0.md` D3's
  correction note, and ledger fragment M2's *"A stale `origin/main` keeps
  more than it must, never less"*. A stale ref has the same asymmetry.
- *where CI asks*: `spec.md` §*Data & interfaces*, first bullet: *"the same
  revision `unverified_check.py --baseline` and `chain_check.py --baseline`
  compare against"*. It is uncorrected, while questions.md's twin sentence
  was corrected.

### ⬜ 4 — The moved heading waits for a closure that commit can never gain

`RULE_MOVED_HEADING` opens *"kept until the closure reaches the merge-base of
main and HEAD (abc1234)"*. The summary line `report` prints says the same.
In the moved case that commit is fixed in the past, so no closure ever
reaches it. What lets the directory go is the merge base moving, which is
what the heading's second sentence says to do. The remedy is right and the
opening words are not. Nothing to paste. A later edit could open with
*"kept: the closure has not reached {base}"* in both headings, which would
move the `*kept until the closure reaches <base>*` phrase that SKILL.md and
the documents case pin.

### ⬜ 5 — The documents case reads the README "row" after flattening, so it checks the rest of the file

`tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base`
takes ``document(edition).split("`settle [--retire]`")[1].split("\n")[0]``.
`document` already returns `flat(...)`, so the text has no `\n` left, and
`row` is everything after the row's start. The assertion that the row names
`--released-at` and `HEAD` would pass if the row dropped both, as long as any
later line of the README carried them. This predates the fix range; the fix
pass edited the case and kept the loop. The fence under 🟡 1 reads the raw
file for its new assertions.

## Round 1's verdicts, answered

- **Finding 1 (moved base):** verified. `survey` sets `base_moved` from
  `base != ref_commit`. `commit_of` and `merge_base` both return
  `rev-parse`/`merge-base` stdout, a full SHA, so the comparison is sound, and
  it is the comparison `base_label` makes. `base_moved` is True exactly when
  the ref has commits `HEAD` lacks, so *"{ref} has moved past that commit"*
  is true whenever it prints. Merging the ref in moves the merge base to its
  tip, which is the remedy that works. Executed: the case is green, and red
  with `base_heading` ignoring `base_moved`.
- **Finding 2 (paperwork, CI asks at the fork):** answered at the four
  coordinates listed. Each now says when the fork is CI's revision and when
  it is not. Read. The *never less* clause the fix pass added beside them is
  ⬜ 3.
- **Finding 3 (shallow clone):** verified. The sentence names both states
  and `git fetch --unshallow`. The docstring still counts seven exit-2
  states, with the shallow clone folded into the second. The case builds a
  depth-1 clone with `--no-single-branch` and is green in this round's run.
- **Finding 4 (`report` on a base-less survey):** verified. The guard
  returns 2 before any key is read and prints `NO_BASE_SAYS`, the same
  sentence `retire` prints. Executed: red with the guard taken out
  (`KeyError`).
- **Finding 5 (per-sibling purpose):** verified. The case reads
  `settle.READER`, `CHECKER` and `OPTIN` from the module, and its phrases are
  `PURPOSES`' values word for word. Read. The fix pass's ledger row records
  the swap mutation as red, and this round did not repeat that.
- **Finding 6 (`seal.py` copied alone):** deferred to #610. spec.md §Scope
  *Out* names it, and #610 is open and names `seal.py` and
  `payload_meter.py`.

**The three widened corrections:** the sentence in
`docs/the-evidence-ledger.md` is true. It says `settle` asks where CI looks
until the base moves past the fork, and earlier after that. The questions.md
note is true. plan.md's chosen row is true in its first clause and false in
*never less*, which is ⬜ 3. The rejected row's *"in every flow this
repository uses"* limits the same claim, and the probe's flow (the base
adding a record file to a released directory) is not one this repository is
known to use. It stands as the frame's judgment.

**51564382 (Windows):** read. `str(OSError)` quotes the filename with `repr`,
so `names_path` accepting `repr(path)[1:-1]` matches the doubled backslashes.
On POSIX, `repr` leaves a plain path unchanged, so the assertion is no weaker
there. The new case shows by itself that the plain substring check misses (its
first assertion). Whether the windows-latest leg goes green is not settled
here: that leg was pending at 6576a226 when this round read `gh pr checks
605`.

**New units, read as code:** `NO_BASE_SAYS`, `base_heading`,
`RULE_MOVED_HEADING` (⬜ 4), `names_path`, and the five new cases. Apart
from ⬜ 4 each is correct. The shallow case's `file://` URL with a Windows
drive path is one git parses (its connect code takes a DOS drive prefix after
`file://` as the path).
That is read, not run, and the same pending Windows leg answers it.

**Read, not a finding:** the `release` check on PR #605 at 6576a226 is red.
`chain_check.py` refuses `Pass` ticked beside `Fixes checked by: nobody`,
which is the state this round's record exists to change.

**The broad gate:** not yet. The full suite, lint and typecheck belong to the
sealer, once, after the rounds settle. It is not due yet, because this round
leaves 🟡 1 and 🟡 2 open.

## Regression tests to plant

- `tests/test_settle_reads_before_it_removes.py`: the README and skill
  assertions in the 🟡 1 fence. They read the raw files, which also closes ⬜ 5.
- 🟡 2 is a comment and a changelog sentence, so `agent-contract` §14 asks
  for no pin. If the orchestrator takes the three-way design instead, the
  probe above is the case to plant: base adds an open `evidence-todo.md`
  after the fork, and `--retire` keeps it.

## Facts for the evidence ledger

- The merge ref of a branch that removed a released directory, and a base
  that later added a file to that directory, merges without conflict. The
  directory survives at the merge ref holding only the added file. Executed
  2026-09-25.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Both README cheat-sheet rows and the settle skill still say CI asks where `--released-at` and `HEAD` meet, which is false once the base has moved past the fork; the skill names no merge for that case | `README.md` settle row; `README.ko.md` settle row; `skills/settle/SKILL.md#"### 1. Read what is waiting"` | open | Read; same class as round 1's paperwork finding, missed by both the original and the widened correction lists |
| 🟡 2 | settle.py says asking at the fork keeps more and never less than CI; a record file the base adds to the directory after the fork is retired here and refused by CI on the merge ref | `skills/settle/scripts/settle.py` module docstring #602 paragraph; `skills/settle/scripts/settle.py#main` | open | Executed: settle --retire exit 0 and removed; clean merge; `unverified_check.py --baseline main` exit 1 on the merge |
| ⬜ 3 | The same two claims under seal: never less in the changelog fragment, plan.md chosen row, 0.14.0 D3 and ledger M2; CI compares at the fork in spec.md | `changelog.md` #602 entry; `plan.md` Alternatives chosen row; `seal/releases/0.14.0.md` D3; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2; `spec.md` Data and interfaces | open | Paperwork correction, outside Needs a fix |
| ⬜ 4 | The moved heading opens with waiting for the closure to reach a fixed past commit, which never happens; the remedy sentence after it is right | `skills/settle/scripts/settle.py#RULE_MOVED_HEADING` | open | Read; nothing to paste |
| ⬜ 5 | The documents case splits a flattened README on a newline, so its row is the rest of the file and the row assertion pins nothing | `tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base` | open | Read; predates the range, closed by the 🟡 1 fence |
| 🟢 | round 1's finding 1 is closed — a moved base prints the heading that names merging the ref into this branch | `skills/settle/scripts/settle.py#base_heading`, `#survey`, `#report`, `#retire` | verified | Executed: case green at 6576a226, red with `base_heading` ignoring `base_moved`; `base_moved` compares two full SHAs |
| 🟢 | round 1's finding 2 is closed at its four coordinates — each now says when the fork is CI's revision | changelog fragment #602; ledger M2; 0.14.0 D3; plan.md Alternatives | answered | Read; the never-less clause added beside them is finding 3 of this round |
| 🟢 | round 1's finding 3 is closed — the no-merge-base refusal names a too-shallow clone and the unshallow fetch | `skills/settle/scripts/settle.py#main` | verified | Executed: shallow case green in this round's run |
| 🟢 | round 1's finding 4 is closed — `report` refuses a base-less survey at 2 with the retire sentence | `skills/settle/scripts/settle.py#report`, `#NO_BASE_SAYS` | verified | Executed: case green, red with the guard removed |
| 🟢 | round 1's finding 5 is closed — each real sibling's purpose is pinned from the module's own table | `tests/test_settle_reads_before_it_removes.py#test_each_sibling_is_refused_with_its_own_purpose` | verified | Read against `PURPOSES`; green in this round's run |
| carried | round 1's finding 6, seal.py and payload_meter.py copied alone | `spec.md` Scope Out | deferred #610 | already deferred in round 1; #610 is open and names both scripts |
| 🟢 | the widened corrections in the evidence-ledger policy and questions.md are true | `docs/the-evidence-ledger.md`; `questions.md` first answered item | verified | Read against `.github/workflows/hygiene.yml` and `unverified_check.py#merge_base` |
| 🟢 | the re-read notes and re-stamped anchors in 0.13.0, 0.14.0 and the fragment hold | `seal/releases/0.13.0.md`; `seal/releases/0.14.0.md`; ledger fragment M1, M2, M3, M5 | verified | Executed: evidence-check exit 0 on each of the three files; each note read against the diff of its unit |
| ❓ | 51564382 turns the windows-latest leg green | `tests/test_a_script_copied_alone_exits_2.py#names_path` | ❓ out of verified scope | Read: the logic matches how OSError quotes a path; the leg was pending at 6576a226; answered by PR 605's windows-latest leg |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on `tests/test_settle_reads_before_it_removes.py` and `tests/test_a_script_copied_alone_exits_2.py`, in this round's clone at 6576a226 | exit 0, 131 passed across the two modules |
| The same settle module with `-k` on the moved-base and report-no-base cases, against the clone with `base_heading` ignoring `base_moved` and `report`'s guard removed; the file restored after | exit 1, both cases failed |
| Probe (one file, run once, deleted): the base adds an open `evidence-todo.md` to a released spec-less directory after the fork; `settle.retire` at `--released-at main` from the branch; the branch merged into `main` as the merge ref | retire exit 0, directory removed; merge clean, the directory keeps only `evidence-todo.md`; merge base equals `main`'s tip; `retired_by_rule` there False; `unverified_check.py --baseline main seal/specs/` exit 1 |
| `./bin/evidence-check --ledger <file> .` on the work item's ledger fragment, `seal/releases/0.13.0.md` and `seal/releases/0.14.0.md` | exit 0 on each |
| The broad gate: the full suite, lint and typecheck | not yet. That run is the sealer's, once, after the rounds settle; this round ran two modules only |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal.py` and `payload_meter.py` die with a traceback when copied alone (already deferred in round 1) | #610 | the repository owner, who holds #610 |

## Paste-ready fixes

### 🟡 1

`README.md`, the end of the `settle [--retire]` row (the row stays one line):

```
A directory a ledger row anchors into stays, and so does one whose record was closed on this branch but is still open where `--released-at` and `HEAD` meet. CI asks there too until `--released-at` moves on past that commit, and once it has, `settle` names the merge that brings the closure here |
```

`README.ko.md`, the end of the same row:

```
이 브랜치에서는 기록의 열린 행을 닫았어도 `--released-at` 과 `HEAD` 가 갈라진 지점에서 아직 열려 있으면 그 디렉터리도 남겨 둡니다. `--released-at` 이 그 지점보다 앞으로 나아가기 전까지는 CI 도 그 지점에서 확인하고, 나아간 뒤라면 `settle` 이 무엇을 이 브랜치로 병합해야 하는지 알려 줍니다 |
```

`skills/settle/SKILL.md` §1, the paragraph opening *Merged first means merged to
the branch the release merges to*:

```markdown
**Merged first means merged to the branch the release merges to, and `settle`
holds you to it.** The CI readers on the release pull request ask the rule of
the merge base of that pull request's base and its merge ref, which is the
base's tip. A closure merged only into the release branch is not there yet, so
a retirement in the same release turns the release pull request red. That is
what happened in 0.15.3 (#602). So `settle` asks the predicate of the merge
base of `--released-at` and `HEAD` as well as of the working tree. That is the
same commit as CI's until `--released-at` moves past the commit this branch
forked from. Once it has, the heading says so, and where `--released-at`
already holds the closure, merging it into this branch and running `settle`
again is what lets the directory go. A directory whose record is closed in the
tree and open at that base is listed under *kept until the closure reaches
<base>*, with every row open there, and `settle --retire` keeps it and exits 1.
It goes in a later pull request, once the closure has reached the branch
`--released-at` names, which for a closure made on a release branch is the
next release. A `--released-at` that shares no commit with `HEAD` has no merge
base, and both arms refuse it at exit 2 rather than asking the tree alone.
```

`tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base`,
replacing the README loop (it reads the raw file, so the row is the row):

```python
    for edition, phrase in (
        ("README.md", "until `--released-at` moves on past that commit"),
        ("README.ko.md", "앞으로 나아가기 전까지는"),
    ):
        with open(os.path.join(ROOT, edition), encoding="utf-8") as f:
            row = f.read().split("`settle [--retire]`")[1].split("\n")[0]
        assert "`--released-at`" in row and "`HEAD`" in row, (
            f"{edition}'s cheat-sheet row does not say the base is asked"
        )
        # Round 2, 🟡 1: CI's revision is the fork only until the base moves.
        assert phrase in row, row
        assert "because that is where CI asks" not in row, row
    assert "which is the base's tip" in text, text
    assert "merging it into this branch and running `settle`" in text, text
```

### 🟡 2

`skills/settle/scripts/settle.py`, module docstring, the #602 paragraph:

```python
the merge base of `--released-at` and `HEAD` (#602). A CI reader on a pull
request stands on the merge ref, so its merge base is the base branch's tip:
the same commit as this one until the base moves past the fork, and a later
one after. Past the fork the two can disagree either way. A closure the base
took after the fork is read by CI and not here, so this keeps a directory CI
would pass. A record file the base added to the directory after the fork, an
open `evidence-todo.md` or a `spec.md`, is read by CI and not here, so this
retires a directory CI refuses. A row closed on the working
branch and still open at that base is kept, under a heading of its own
naming the base and, where the base has moved, the merge that moves it.
```

`skills/settle/scripts/settle.py#main`, the comment above the no-merge-base
refusal:

```python
    # #602: the rule arm asks its predicate of the merge base of the ref and
    # `HEAD`. The CI readers compute the same merge base from their own
    # `HEAD`, which on a pull request is the merge ref, so theirs is the
    # base's tip: the same commit while the base has not moved since the
    # fork, and a later one when it has, where the two can disagree in either
    # direction (the module docstring says how). Two histories that share no
    # commit have none, and neither does a clone too shallow to reach the
    # commit they share; the predicate asked of nothing would be asked of the
    # working tree alone — the answer that let a closure the base had not
    # seen retire its directory. Refused in both arms, so the report never
    # lists what the retirement then refuses.
```

### ⬜ 3

The changelog fragment's #602 entry, the sentence that ships:

```markdown
  into `main` then failed. `settle` now asks where the branch forked from
  `--released-at` as well, which is the same commit as the base's tip unless
  the base has moved since. A directory closed here and still open there is
  listed under its own heading, naming the base and the rows open there, and
  `--retire` keeps it and exits 1. Where the base has moved, the heading says
  to merge it into this branch.
```

Needs a fix: yes — 🟡 1 (both README rows and the settle skill still say CI asks where `--released-at` and `HEAD` meet) and 🟡 2 (settle.py's "keeps more and never less", broken by an executed counter-case)
Loses a record or crashes: no

## Proof block

Files opened this round:
`seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/rounds/round-1.md`;
the fix-range diff of `skills/settle/scripts/settle.py`,
`tests/test_a_script_copied_alone_exits_2.py`,
`tests/test_settle_reads_before_it_removes.py`, `docs/the-evidence-ledger.md`,
`seal/releases/0.13.0.md`, `seal/releases/0.14.0.md`, the ledger fragment,
and the work item's `changelog.md`, `plan.md`, `questions.md` and `spec.md`;
`skills/settle/scripts/settle.py` (`survey`, `report`, `retire`, `main`,
`load`, `PURPOSES`, the module docstring);
`skills/verify/scripts/unverified_check.py` (`commit_of`, `merge_base`,
`base_label`, `retired_by_rule`); `skills/code-review/scripts/chain_check.py`
(its loader refusal); `.github/workflows/hygiene.yml` (triggers, the two
reader steps); `skills/settle/SKILL.md` §1; the `settle [--retire]` rows of
`README.md` and `README.ko.md`;
`tests/test_settle_reads_before_it_removes.py` (fixture, `moment`, `at`,
`document`, `flat`, the documents case); `gh pr checks 605`; the failed
`release` job log; `gh issue view 610`.
