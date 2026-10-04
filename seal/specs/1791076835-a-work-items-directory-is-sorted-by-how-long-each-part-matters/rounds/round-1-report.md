# Round 1 report — 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters (#729, PR #768)

Target `5830d41f`, against `release/v0.18.1` at `edee5ca2`. Reviewed in a
`git clone --no-local` scratch clone at the target. The worktree under
review was only read, and this file is the one write in it.

## What was asked, and the answer in four lines

- **Spec compliance (D1 to D6).** The arm does what D3 and D4 say. That covers
  the allow-list, the per-item guards, the local-mode refusal, the dry run,
  and leaving `routing.md` and the SDD set in place. Run over the real corpus
  in the scratch clone, the drop removed 525 files from 54 items. The three
  pull-request readers then passed it, and so did nine corpus-reading test
  modules. Nothing is lost that git history at the release tag does not
  still hold.
- **The readers.** The machine readers the spec enumerated accept the drop. I
  re-derived that list with a grep of my own. One reader class was not
  enumerated: the SDD set that stays. It names its own `rounds/` and
  `phases/` files 400 times, in 165 files of 51 released items. Nothing lists
  those references, and five documents now say the process record is "read
  by nothing" (🟡 1).
- **The survivor-sweep correction.** Yes, it can hide a real survivor, and I
  ran the case. The case is a pull-request file present at the base, moved
  out with one sentence reworded on the way. The base sweep reports the
  reworded sentence's other copy and the target sweep does not. `phases/` and
  `rounds/` already carry the same exception, and so does a retired directory.
  I judge it ⬜ and not a release defect (⬜ 4).
- **Quality.** The new citation narrowing misses four prose shapes of
  citation (🟡 2). The README cheat sheet, the row "a reader actually types
  from", does not mention the new arm in either edition (🟡 3).

## Findings

### 🟡 1 — The SDD set that stays still points into the process record, and nothing says where those references now resolve

**Where.** `skills/settle/SKILL.md:91` and `:110-114` (the arm's section), and
`skills/settle/SKILL.md:188-192` (fold step 1). The same claim, "read by
nothing after the release", is at `docs/the-record-layout.md:147` and `:209`,
`skills/settle/scripts/settle.py:1239` and `:1386`.

**What is wrong.** The arm removes part of a directory, which is new. `--retire`
always took the whole directory, so a reference from `overview.md` to its own
`phases/phase-4.md` went with it. Now the referring file stays and the target
goes. Measured with `git grep` at `origin/main` (`e141980a`), the SDD files of
released items still name a process-record file on 400 lines in 165 files
across 51 items. A typical one is `overview.md`'s "closer, which
`phases/phase-4.md` records" in 1790260566, and every `questions.md` answer
that cites `phases/phase-N.md` as the measurement behind it.

`citations` reads only files outside `seal/specs/` (`tracked_text` skips that
prefix). Even if it read them, `CITATION_RE` needs the `specs/<id>/` prefix,
and these references are relative. So the run lists none of them. This is
the spec's choice in D4 ("Paths outside `seal/specs/`"). The framer's readers
table enumerated scripts, hooks and workflows, and did not count the SDD set
as a reader of the process record.

**Why it matters.** The fold is the reader that comes after the release. Its
session reads `spec.md`, `overview.md` and `questions.md` to write the
standing statement, and the procedure sends it nowhere when a reference does
not open. The spec names the risk as "a removal that loses something a reader
still needs after release". Nothing is lost: git keeps every file at the
release tag. What is lost is the pointer, and the documents tell the reader
nothing reads that part at all. `agents/framer.md` got the sentence that
answers this ("read at the release tag after that"), but the fold's own
procedure did not.

**Why 🟡 and not 🔴.** No record is lost and nothing crashes. The shipped
defect is a procedure that leads its reader to dead references with no
instruction. The smith can answer this one with grounds instead, if the
owner's position is that the fold session reads git history by default.

### 🟡 2 — `cites_a_process_record` does not list a citation that ends in punctuation, a line number or an anchor, or that names `rounds` with no slash

**Where.** `skills/settle/scripts/settle.py:1347`, with `CITATION_RE` at `:859`.

**What is wrong.** The lookahead's `rest` stops only at whitespace, quotes,
brackets, `|`, `<`, `>` and `*`. So it keeps a sentence's closing `.`, a `,`,
a `:40` line number and a `#anchor`. `cites_a_process_record` then compares
the whole first segment to the list. I ran four prose shapes through the
target's own `CITATION_RE` and `cites_a_process_record`:

| `rest` read from the line | listed |
|---|---|
| `survivors.md.` (end of sentence, no backticks) | no |
| `handoff.md:40` (`path:line`, the shape this repository's prose uses) | no |
| `rounds` (a citation of the directory, in backticks, no trailing slash) | no |
| `pr.ko.md,` | no |
| `rounds/round-1.md.` and `` `survivors.md` `` (controls) | yes |

**Why it matters.** "Listed and never refused" is the only protection D4 gives
a citation into a removed file. A citation this misses stops resolving with
nothing printed. On today's corpus the miss is latent. I compared the run's
listing with a `git grep` of every citation into a process-record file of a
standing item, and all eight were listed. Every one of them happens to sit in
backticks or to continue past the file name. `--retire` does not have this
gap, because it lists any citation into the directory.

### 🟡 3 — The README cheat sheet, in both editions, does not mention `settle --retire-process`

**Where.** `README.md:288` and `README.ko.md:280`.

**What is wrong.** The row `` `settle [--retire]` `` describes everything
`settle` prints and removes. It does not say that `settle` with no flag now
ends with the process arm's dry run, and it does not name the new removal.
`tests/test_settle_reads_before_it_removes.py#test_both_cheat_sheets_carry_the_command`
calls that row "the row a reader actually types from". The release checklist
names the arm, but this repository is the only one that reads the checklist.
A plugin user's repository builds up the same process record, and its README
row is where that user would learn the arm exists. §14 of the agent contract
asks that output a person acts on be documented where they look for it, and
here that was done in `skills/settle/SKILL.md` alone.

**Constraint on the fix.** Three cases in
`tests/test_settle_reads_before_it_removes.py` split on the literal
`` `settle [--retire]` `` (lines 813, 1090, 1519). The fix below adds a
sentence at the end of each row and leaves that spelling alone.

### ⬜ 4 — The survivor sweep's new filter hides the survivor of a pull-request file moved out with a sentence reworded (measured), the same exception rounds, phases and retired directories already carry

**Where.** `skills/code-review/scripts/survivor_check.py:1452`, and
`written_for_a_pull_request` at `:928`.

**What I ran.** Two scratch repositories, each with a base commit and one
work commit. I ran the sweep from the target `survivor_check.py` and from
`edee5ca2`'s copy, placed beside it in the scratch clone.

- `seal/specs/<id>/handoff.md` holds a sentence. A paraphrase of it stands
  in `docs/another.md`. The range deletes `handoff.md` and writes its text to
  `docs/handoff-notes.md`, with that sentence reworded. At the base: exit 1,
  "1 place(s) still carry wording this range removed". At the target: exit 0,
  "against 0 sentence(s)".
- Control: the same move out of `phases/phase-1.md` is silent at both base
  and target, because `records_a_past_state` has excluded it since #365.

**Why ⬜.** The filter fires only for a file present at the left end of the
range and absent at the right. On a branch that is a file some earlier pull
request merged. Its own item's in-flight `handoff.md` is never at the base.
The hidden shape needs such a file to be moved, with a reword, into a file
that stays. That is #551's shape (released row R1 in 0.15.1). This item's
fragment re-reads R1 as "the cited row's claim holds", which is true for
every file outside the process record, and was already untrue for `rounds/`
and `phases/` before #729. I found no ranged reading of the filter (one
keyed to `written`, for instance) that keeps a release pull request quiet
when the drop rides along in it. So I leave the trade as the author drew it,
and record that it was measured.

### Confirmed (each checked against the code, not against the account)

- **D4's allow-list and the sweep's list agree entry by entry.**
  `is_process_record` and `records_a_past_state` or `written_for_a_pull_request`
  give the same answer for all nineteen entries the parametrized case holds,
  `pr.d/notes.md` and `notes/handoff.md` included. Read, and executed in the
  module run below.
- **Guards.** A todo file is kept whole when `todo_open_rows` finds an open
  row. The `tests-todo.md` format (✅ rows and `drained`, read from a
  historical file of 1788272986) is the shape that function reads. A ledger
  anchor holds an item only when it lies in a file the arm takes
  (`process_anchored`, by `taken_by`). Executed on the real corpus: 0 kept,
  which matches the spec's measurement of 0 anchors.
- **Symlinks.** A link named `rounds` reads as not a directory, so it is
  listed as not a process record and kept. A link named `handoff.md` is
  removed as the link. A symlinked work item directory is never released,
  because `ls-tree -r` lists it with no `/` after the id. Read.
- **Local mode.** It returns 2 in `main` before `survey`, so no arm is
  reached. Pinned by the S8 case, which I read and which passed.
- **Release seal.** `chain_counts` maps a pull request to an item through
  `item_dir`, by the head branch named in `routing.md`. The drop's own pull
  request declares no item, so it maps to none, and a released item's
  `routing.md` stays. Read.
- **Readers I re-derived** with a grep of scripts, hooks and workflows:
  `fold_ledger.py` reads `evidence-todo.md`, which the arm takes only once it
  is closed. `release_completeness_check.py`, `rider_check.py`, `arm_check.py`
  and `worktree-guard.py` name these paths in prose only. `review-history-guard.py`
  only reminds and cannot block. `root-migrate.py` marks an item by
  `routing.md`, which stays.
- **D6's carriers.** The class grep turned up no carrier still saying the
  process record waits for the fold or stays for good. I grepped D6's seven
  phrases and a wider pattern over `docs/`, the skills, the agents, the
  templates and both READMEs.
- **The account's Q4 and Q5.** Q4 (no corpus module pins a removed file) is
  corroborated by the nine modules I ran after the drop. Q5 (no shipped
  `survivors.md` row excused another range's survivor) I read and did not
  re-run.

## Regression tests to plant

| Finding | Destination | What it asserts |
|---|---|---|
| 🟡 2 | `tests/test_settle_retires_the_process_record.py` | a `docs/` line citing a removed file as `…/survivors.md.`, as `…/handoff.md:40`, and as `` `…/rounds` `` is listed under the cited heading, and a `…/spec.md.` citation is not |
| 🟡 3 | `tests/test_settle_reads_before_it_removes.py` | both editions' cheat-sheet row names `settle --retire-process` |
| 🟡 1 | `tests/test_settle_retires_the_process_record.py` | `skills/settle/SKILL.md` says where a reference from the SDD set into the process record resolves after the arm |

Show each one red first: against the target's code for 🟡 2, and with the new
sentence deleted for 🟡 1 and 🟡 3.

## Facts for the evidence ledger

- Executed 2026-10-04, scratch clone at `5830d41f` with `--released-at
  origin/main` (`e141980a`). The arm removed 525 files from 54 released items
  and kept 0, exit 0. It listed seven citations of four items from outside
  `seal/specs/`, which matches a `git grep` of every such citation into a
  standing item.
- Executed, same drop committed on a probe branch. `chain_check.py --baseline
  5830d41f` exited 0 and examined nothing. `survivor_check.py --range
  5830d41f..HEAD` exited 0, against 0 removed sentences over 712 files.
  `unverified_check.py --baseline 5830d41f seal/specs/` exited 0 over 58
  overviews.
- Measured 2026-10-04 at `e141980a`: released items' SDD files name a
  process-record file on 400 lines in 165 files across 51 items (🟡 1).

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

### ⬜ 4

```
handoff moved+reworded | base edee5ca2 | exit 1 | 1 place(s) still carry wording this range removed
handoff moved+reworded | target 5830d41f | exit 0 | against 0 sentence(s) the range removed
phase moved+reworded (control) | base edee5ca2 | exit 0 | against 0 sentence(s)
phase moved+reworded (control) | target 5830d41f | exit 0 | against 0 sentence(s)
```

### 🟡 2

```
'see seal/specs/1700000001-alpha/survivors.md.'          rest='survivors.md.'      listed=False
'see seal/specs/1700000001-alpha/handoff.md:40 for it'   rest='handoff.md:40'      listed=False
'the `seal/specs/1700000001-alpha/rounds` directory'     rest='rounds'             listed=False
'in seal/specs/1700000001-alpha/pr.ko.md, which'         rest='pr.ko.md,'          listed=False
'seal/specs/1700000001-alpha/rounds/round-1.md.'         rest='rounds/round-1.md.' listed=True
'`seal/specs/1700000001-alpha/survivors.md`'             rest='survivors.md'       listed=True
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1

In `skills/settle/SKILL.md`, after the paragraph that ends "After that they
are in git history, at the release tag." (line 114):

```markdown
**The SDD set that stays still points into what left.** A released item's
`overview.md`, `questions.md` and `spec.md` name its own `rounds/round-N.md`
and `phases/phase-N.md` by relative path — 400 lines across 51 items when
this arm shipped — and nothing lists them, because the files that hold them
are not removed. Each resolves at the tag of the release that shipped the
item: `git show v<X.Y.Z>:seal/specs/<id>/phases/phase-2.md`. The fold reads
them there.
```

And in §*1. Read what is waiting*, after "released directory (§4)." (line 192):

```markdown
Where a released item's SDD set cites one of its own round or phase records,
`settle --retire-process` may already have taken it: read it at the tag of
the release that shipped the item, `git show v<X.Y.Z>:<path>`.
```

The case that pins it, in `tests/test_settle_retires_the_process_record.py`:

```python
def test_the_skill_says_where_a_reference_into_the_process_record_resolves():
    with open(SKILL, encoding="utf-8") as f:
        text = flat(f.read())
    assert "The SDD set that stays still points into what left." in text
    assert "git show v<X.Y.Z>:seal/specs/<id>/phases/phase-2.md" in text
```

### 🟡 2

`skills/settle/scripts/settle.py`, replacing `cites_a_process_record`:

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

The case, in `tests/test_settle_retires_the_process_record.py`:

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

### 🟡 3

`README.md:288`, the end of the `` `settle [--retire]` `` row's last cell,
before its closing `|`:

```markdown
 `settle --retire-process` is a removal of its own and runs first at every release, fold or no fold: it takes `rounds/`, `phases/`, `survivors.md` and the files written only for a pull request from every released work item and leaves `routing.md` and the SDD set, and `settle` with no flag ends with what it would take
```

`README.ko.md:280`, the same place:

```markdown
 `settle --retire-process` 는 따로 도는 삭제이고, fold 를 하든 안 하든 릴리스마다 가장 먼저 돕니다. 릴리스된 모든 작업 항목에서 `rounds/`, `phases/`, `survivors.md` 와 풀 리퀘스트 하나만을 위해 쓴 파일을 지우고 `routing.md` 와 작업의 기록은 남깁니다. 플래그 없이 돌린 `settle` 은 이 삭제가 가져갈 것을 마지막에 보여 줍니다
```

The pin, added to `test_both_cheat_sheets_carry_the_command` in
`tests/test_settle_reads_before_it_removes.py`:

```python
    with open(os.path.join(ROOT, edition), encoding="utf-8") as f:
        row = f.read().split("`settle [--retire]`")[1].split("\n")[0]
    assert "`settle --retire-process`" in row, (
        f"{edition}'s cheat-sheet row does not name the process arm"
    )
```

Needs a fix: yes — 🟡 1 (the fold procedure does not say where the SDD set's references into the removed process record resolve), 🟡 2 (cites_a_process_record misses four prose shapes of citation), 🟡 3 (the README cheat sheet omits the arm in both editions)
Loses a record or crashes: no

## Proof block

Files I opened at `5830d41f` in the scratch clone: `skills/settle/scripts/settle.py`
(diff, `main`, `survey`, `released`, `open_rows`, `anchored_rows`,
`citations`, `tracked_text`, the whole process arm),
`skills/code-review/scripts/survivor_check.py` (diff, `corrected`),
`skills/verify/scripts/unverified_check.py` (`todo_open_rows`,
`open_record_rows`, `retired_by_rule`, `tree_at`),
`.github/scripts/release_seal.py` (`chain_counts`, `seal_release`),
`hooks/review-history-guard.py` (head), the work item's `spec.md` and
`questions.md`, its ledger fragment rows L5, Re-read S1, R1 and P2,
`seal/releases/0.15.1.md` row R1, the two new test modules and the diff of
`tests/test_settle_reads_before_it_removes.py` with its README pins (lines
800-822, 1080-1095, 1510-1525), the diff of every changed document,
`skills/settle/SKILL.md` lines 108-114 and 182-200,
`docs/the-evidence-ledger.md` lines 400-415,
`docs/review-handoff-protocol.md` lines 511-520, `README.md:288`,
`README.ko.md:280`, and the head of two corpus tests that cite a released item
(`tests/test_no_shape_the_base_stops_reads_silent.py`,
`tests/test_the_hook_surface_git_offers.py`).
