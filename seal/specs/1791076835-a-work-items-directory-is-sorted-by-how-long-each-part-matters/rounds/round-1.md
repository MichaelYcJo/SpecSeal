# 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters — review round 1

| Field | Value |
|---|---|
| Target SHA | 5830d41f2dc2e2c30621f5664af9054c971718e7 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #768 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the fold procedure does not say where the SDD set's references into the removed process record resolve), 🟡 2 (cites_a_process_record misses four prose shapes of citation), 🟡 3 (the README cheat sheet omits the arm in both editions) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item `1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters` (#729, PR #768). Target `5830d41f`, against `release/v0.18.1` at `edee5ca2`.

**Spec compliance first.** Check `settle --retire-process` against D1–D6:
- the allowlist of process files;
- the guards, which leave a directory with an open todo row or a ledger row pointing into it whole;
- the refusal in local mode;
- the dry-run preview;
- what stays, which is `routing.md` and the SDD set.

The risk to weigh is a removal that loses something a reader still needs after release. Enumerate every reader of the removed paths by construction: `chain_check`, `survivor_check`, `unverified_check`, `release_seal`, `settle`, the records arm, and anything a grep finds. Check that each one accepts the drop.

**Then the frame correction the build made.** It added `PULL_REQUEST_FILES` and `written_for_a_pull_request` to `survivor_check.py`, so a pull-request file the range deleted whole leaves the sweep. Judge whether this can now hide a real survivor.

**Quality second.**

**What the orchestrator already verified at the target:** the changed modules and hygiene modules (524 passed), and ruff on the changed Python files. The release head carries 10 drifted rows from the wave-one squashes. #766 re-reads them; they are not this item's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The SDD set that stays names its own rounds and phases files on 400 lines in 51 released items; the arm lists none of them, and the fold procedure does not say they now resolve at the release tag | `skills/settle/SKILL.md:110` | open | read and measured: `citations` skips `seal/specs/`, and the references are relative; the documents say the process record is read by nothing |
| 🟡 2 | `cites_a_process_record` does not list a citation ending in `.`, `,`, `:N` or `#anchor`, or naming `rounds` with no slash | `skills/settle/scripts/settle.py:1347` | open | executed: four shapes run through the target's own regex and predicate, each unlisted; controls listed |
| 🟡 3 | The README cheat-sheet row in both editions does not mention `settle --retire-process` or the dry-run section | `README.md:288` | open | read; the same row is `README.ko.md:280`, and the test module calls it the row a reader types from |
| ⬜ 4 | The survivor filter hides the survivor of a pull-request file moved out with a sentence reworded | `skills/code-review/scripts/survivor_check.py:1452` | open | executed at base and target: reported at `edee5ca2`, silent at `5830d41f`; the same exception rounds, phases and retired directories already carry, so it is not counted as needing a fix |
| 🟢 | The arm, run over the real corpus, removes exactly the allow-list from 54 released items and the three pull-request readers pass the drop | `skills/settle/scripts/settle.py:1381` | confirmed | executed in a scratch clone: 525 files, 0 kept; chain, survivor and unverified checks exit 0 |
| 🟢 | No corpus-reading test module pins a removed file of a released item | `tests/conftest.py` | confirmed | executed after the drop: nine corpus modules 582 passed, 1 skipped; `test_release_hygiene.py` 50 passed |
| 🟢 | The arm's allow-list and the survivor sweep's two predicates agree entry by entry | `skills/code-review/scripts/survivor_check.py:928` | confirmed | executed: the two new modules, 50 passed |

## Paste-ready fixes

```markdown
**The SDD set that stays still points into what left.** A released item's
`overview.md`, `questions.md` and `spec.md` name its own `rounds/round-N.md`
and `phases/phase-N.md` by relative path — 400 lines across 51 items when
this arm shipped — and nothing lists them, because the files that hold them
are not removed. Each resolves at the tag of the release that shipped the
item: `git show v<X.Y.Z>:seal/specs/<id>/phases/phase-2.md`. The fold reads
them there.
```
```markdown
Where a released item's SDD set cites one of its own round or phase records,
`settle --retire-process` may already have taken it: read it at the tag of
the release that shipped the item, `git show v<X.Y.Z>:<path>`.
```
```python
def test_the_skill_says_where_a_reference_into_the_process_record_resolves():
    with open(SKILL, encoding="utf-8") as f:
        text = flat(f.read())
    assert "The SDD set that stays still points into what left." in text
    assert "git show v<X.Y.Z>:seal/specs/<id>/phases/phase-2.md" in text
```
```python
# What ends a file name in prose: an anchor or a line number. A sentence's
# closing punctuation is stripped after it.
NAME_END_RE = re.compile(r"[#:]")


def cites_a_process_record(rest):
    """Whether the path after a cited directory's name lands in a file the
    process arm takes — `citations`' `inside` for this arm.

    The first segment is read as prose writes it: `handoff.md:40`,
    `survivors.md#…` and a sentence's closing `.` or `,` name the file before
    them, and `rounds` with no slash names the directory."""
    first, slash, _ = rest.partition("/")
    first = NAME_END_RE.split(first, 1)[0].rstrip(".,;")
    if not first:
        return False
    return is_process_record(first, bool(slash) or first in PROCESS_DIRS)
```
```python
def test_a_citation_written_as_prose_is_listed(repo):
    """A citation outside backticks ends with the sentence's punctuation, a
    `path:line` ends with its line, and a directory is named with no slash.
    Each still names a file the arm takes."""
    write(
        repo / "docs" / "one-root.md",
        "# a policy\n\nA rule.\n\n"
        f"Measured in seal/specs/{ALPHA}/survivors.md.\n"
        f"See seal/specs/{ALPHA}/handoff.md:40 for it.\n"
        f"The `seal/specs/{ALPHA}/rounds` directory.\n"
        f"Decided in seal/specs/{ALPHA}/spec.md.\n",
    )
    git(repo, "add", "docs")
    git(repo, "commit", "-qm", "prose citations")
    code, text = run(repo, "--retire-process")
    assert code == 0, text
    for line in (5, 6, 7):
        assert f"        cited from docs/one-root.md:{line}" in text, (line, text)
    assert "docs/one-root.md:8" not in text, text
```
```markdown
 `settle --retire-process` is a removal of its own and runs first at every release, fold or no fold: it takes `rounds/`, `phases/`, `survivors.md` and the files written only for a pull request from every released work item and leaves `routing.md` and the SDD set, and `settle` with no flag ends with what it would take
```
```markdown
 `settle --retire-process` 는 따로 도는 삭제이고, fold 를 하든 안 하든 릴리스마다 가장 먼저 돕니다. 릴리스된 모든 작업 항목에서 `rounds/`, `phases/`, `survivors.md` 와 풀 리퀘스트 하나만을 위해 쓴 파일을 지우고 `routing.md` 와 작업의 기록은 남깁니다. 플래그 없이 돌린 `settle` 은 이 삭제가 가져갈 것을 마지막에 보여 줍니다
```
```python
    with open(os.path.join(ROOT, edition), encoding="utf-8") as f:
        row = f.read().split("`settle [--retire]`")[1].split("\n")[0]
    assert "`settle --retire-process`" in row, (
        f"{edition}'s cheat-sheet row does not name the process arm"
    )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the two new modules at the target | 50 passed |
| `settle` dry run over the real corpus, `--released-at origin/main` | exit 0; section reads 525 files in 54 released work items |
| `settle --retire-process` over the real corpus in the scratch clone | exit 0; 525 files from 54 items, 0 kept, 7 citations of 4 items listed |
| `chain_check.py --baseline 5830d41f` on the committed drop | exit 0, nothing declared, nothing judged |
| `survivor_check.py --range 5830d41f..HEAD` on the committed drop | exit 0, 0 removed sentences, 712 files examined |
| `unverified_check.py --baseline 5830d41f seal/specs/` on the committed drop | exit 0, 58 overviews |
| `bin/test` on nine corpus-reading modules after the drop | 582 passed, 1 skipped |
| `bin/test` on the release hygiene module after the drop | 50 passed |
| `bin/evidence-check --ledger` on this item's fragment | exit 0, 112 ok, 0 drifted, 0 broken |
| Survivor sweep, base copy against target, on a moved-and-reworded `handoff.md` and a `phases/` control | base reports 1 place, target 0; the control is silent at both |
| The target's own citation regex and predicate on six prose shapes | four unlisted shapes, two controls listed |
| The full suite, lint and typecheck (the broad gate) | not yet, and not this round's; the sealer runs it once the rounds settle |

```
handoff moved+reworded | base edee5ca2 | exit 1 | 1 place(s) still carry wording this range removed
handoff moved+reworded | target 5830d41f | exit 0 | against 0 sentence(s) the range removed
phase moved+reworded (control) | base edee5ca2 | exit 0 | against 0 sentence(s)
phase moved+reworded (control) | target 5830d41f | exit 0 | against 0 sentence(s)
```
```
'see seal/specs/1700000001-alpha/survivors.md.'          rest='survivors.md.'      listed=False
'see seal/specs/1700000001-alpha/handoff.md:40 for it'   rest='handoff.md:40'      listed=False
'the `seal/specs/1700000001-alpha/rounds` directory'     rest='rounds'             listed=False
'in seal/specs/1700000001-alpha/pr.ko.md, which'         rest='pr.ko.md,'          listed=False
'seal/specs/1700000001-alpha/rounds/round-1.md.'         rest='rounds/round-1.md.' listed=True
'`seal/specs/1700000001-alpha/survivors.md`'             rest='survivors.md'       listed=True
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
