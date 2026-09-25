# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — review round 2

| Field | Value |
|---|---|
| Target SHA | 6576a226622cf1faed896ee164dcde435bdc5743 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 605 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (both README rows and the settle skill still say CI asks where `--released-at` and `HEAD` meet) and 🟡 2 (settle.py's "keeps more and never less", broken by an executed counter-case) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790297085 is the verifying round over round 1's fixes (32993c08..9b5f7be9) at 6576a226. It asks, for each round-1 verdict closed as fixed or answered, whether it is actually closed. It reads the units the fixes created as a finding surface, and also the three corrections the fix pass widened under section 12 and the Windows case at 51564382.

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

## Paste-ready fixes

```
A directory a ledger row anchors into stays, and so does one whose record was closed on this branch but is still open where `--released-at` and `HEAD` meet. CI asks there too until `--released-at` moves on past that commit, and once it has, `settle` names the merge that brings the closure here |
```
```
이 브랜치에서는 기록의 열린 행을 닫았어도 `--released-at` 과 `HEAD` 가 갈라진 지점에서 아직 열려 있으면 그 디렉터리도 남겨 둡니다. `--released-at` 이 그 지점보다 앞으로 나아가기 전까지는 CI 도 그 지점에서 확인하고, 나아간 뒤라면 `settle` 이 무엇을 이 브랜치로 병합해야 하는지 알려 줍니다 |
```
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
```markdown
  into `main` then failed. `settle` now asks where the branch forked from
  `--released-at` as well, which is the same commit as the base's tip unless
  the base has moved since. A directory closed here and still open there is
  listed under its own heading, naming the base and the rows open there, and
  `--retire` keeps it and exits 1. Where the base has moved, the heading says
  to merge it into this branch.
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on `tests/test_settle_reads_before_it_removes.py` and `tests/test_a_script_copied_alone_exits_2.py`, in this round's clone at 6576a226 | exit 0, 131 passed across the two modules |
| The same settle module with `-k` on the moved-base and report-no-base cases, against the clone with `base_heading` ignoring `base_moved` and `report`'s guard removed; the file restored after | exit 1, both cases failed |
| Probe (one file, run once, deleted): the base adds an open `evidence-todo.md` to a released spec-less directory after the fork; `settle.retire` at `--released-at main` from the branch; the branch merged into `main` as the merge ref | retire exit 0, directory removed; merge clean, the directory keeps only `evidence-todo.md`; merge base equals `main`'s tip; `retired_by_rule` there False; `unverified_check.py --baseline main seal/specs/` exit 1 |
| `./bin/evidence-check --ledger <file> .` on the work item's ledger fragment, `seal/releases/0.13.0.md` and `seal/releases/0.14.0.md` | exit 0 on each |
| The broad gate: the full suite, lint and typecheck | not yet. That run is the sealer's, once, after the rounds settle; this round ran two modules only |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/settle/scripts/settle.py#RULE_BASE_HEADING`, `#report`, `#retire`, `#main` | round 1's 🟡 1 — fixed |
| round-1 | `changelog.md` #602 entry; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2; `seal/releases/0.14.0.md` D3; `plan.md` §*Alternatives considered* | round 1's ⬜ 2 — answered |
| round-1 | `skills/settle/scripts/settle.py#main` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/settle/scripts/settle.py#report` | round 1's ⬜ 4 — fixed |
| round-1 | `tests/test_settle_reads_before_it_removes.py#test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback` | round 1's ⬜ 5 — fixed |
| round-1 | `spec.md` §Scope *Out* | round 1's ⬜ 6 — deferred |
| round-1 | `fold_check.py#load`, `settle.py#load`, `round_record.py#load` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/gather_changelog.py#main`, `#section_lines` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.12.2.md`, `0.13.0.md`, `0.14.0.md`, `0.15.0.md`, `0.15.1.md`, `0.15.3.md` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal.py` and `payload_meter.py` die with a traceback when copied alone (already deferred in round 1) | #610 | the repository owner, who holds #610 |
