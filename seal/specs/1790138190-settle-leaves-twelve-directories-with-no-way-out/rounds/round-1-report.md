# Round 1 report — settle leaves twelve directories with no way out

| Field | Value |
|---|---|
| PR | MichaelYcJo/SpecSeal#525 (draft), closes #517 and #511 |
| Target SHA | 4d19cc0418c97dd341f886b4d11c728bff8033d9 |
| Base | `release/v0.14.0` at f8f1c9d |
| Reviewed | `git diff f8f1c9d..4d19cc0`, 21 commits, in a `git clone --no-local` at the target SHA |
| Round | 1 — a first round: no earlier `round-N.md` exists, so nothing is carried |

## How the findings relate

The branch adds one question, *was this directory retired?*, and four readers
ask it. Every finding below is a place where two parties that must agree
about a removal still read different populations.

```
settle --retire  (working tree)          CI readers (merge base)          evidence-check (whole ledger)
       |                                         |                                  |
       |-- F2: row closed on the branch -------->| still open at the base -> red    |
       |-- F3: spec.md gone in an earlier PR --->| spec-less at the base -> green   |
       |-- F1: guard reads live lines only ---------------------------------------->| reads every line -> BROKEN
                                   survivor sweep: F4 — any `*/specs/<x>/` counts as a work item
```

F1 is #511's own failure, one step narrower. F2 makes the documented fold
procedure end red in CI. F3 lets a spec leave with no marker across two pull
requests. F4 widens the survivor exclusion past the `seal/` root. F5 is one
report line that reads wrong.

Stage 1 (spec compliance) found the owner's D1, D2 and D3 followed as
`spec.md` records them. D1's choice of *outside the chain* is grounded in the
tree, and no document still says a fold is a work item or that *Nothing in
`seal/ledger.md` moves* — read, below. The findings are all Stage 2.

## Findings

### 🟡 1 — The #511 guard skips anchors that evidence-check still reads, so a retirement can still leave a row BROKEN

`skills/settle/scripts/settle.py:459-471` (`anchored_rows`) reads each ledger
line through `unverified_check.py#live_lines` and skips every line that is not
live. `evidence_check.py#check_text` does not skip anything. It runs
`ANCHOR_RE.finditer` over the whole ledger text, fenced blocks and HTML
comments included (`skills/evidence-check/scripts/evidence_check.py:1207`).
The guard also reads two of evidence-check's three addresses. It never reads
`docs/**/_evidence.md`, the pre-0.10 address `evidence_check.py#default_patterns`
still reads (`evidence_check.py:919-946`).

`live_lines` settles an ambiguous line by calling it *not live*, which its
docstring says is *resolved toward keeping a work item's directory*. That is
true for the marker reader. For this guard, *not live* means the row is not
seen and the directory is removed, so the same bias points the other way.

**Executed.** In a fixture holding three folded directories, one anchored by a
fenced ledger row, `settle --retire` removed the fenced row's directory and
exited 1 over the other two. evidence-check then reported
`seal/specs/1700000003-fence/spec.md#"fence"  file not found`. That is #511's
defect: a BROKEN row found after the directory is gone. On this repository's
ledger today both readers see 1938 anchors and none is on a non-live line, so
nothing breaks now. The gap stays open for any later ledger and for every user
repository.

`tests/test_settle_reads_before_it_removes.py:365`
(`test_a_quoted_anchor_is_not_a_row`) pins the skipping. `spec.md` G3
prescribed `live_lines`, so the defect is in the frame as well as in the
code. The fix goes to the rule the guard reads, not to one test.

Class, enumerated: every ledger the checker reads is an input the guard needs
too. Those are `seal/ledger.md`, `seal/ledger/*.md` and `docs/**/_evidence.md`,
and every line of each. The prose saying *every live row* has to change with
the code in three places: `docs/the-evidence-ledger.md` (the paragraph
beginning *A retirement would break*), `skills/settle/SKILL.md:196`, and the
fragment's G3 row.

### 🟡 2 — Closing an open memo row and retiring its directory in one pull request is refused in CI, and the skill tells a fold to do exactly that

`skills/settle/SKILL.md:92-95` says an open row *leaves by being closed … or
re-homed … Once it has, the next `settle --retire` takes the directory.*
`docs/the-evidence-ledger.md:184` and `settle.py`'s `RULE_KEPT_HEADING` say
the same thing. `settle` asks the predicate of the working tree, where the row
is now ✅. The three CI readers ask it of the merge base, where the row is
still open. `unverified_check.py#retired_by_rule`'s own docstring names this as
the failure it was built to prevent: *a fold pull request red in CI after
`settle --retire` said the removal was fine.*

**Executed.** In a fixture, a released spec-less directory had an open row.
The branch closed the row in one commit, and `settle --retire` removed the
directory and exited 0 (*retired 1 work item; 0 kept*). Against the base,
`unverified_check.py --baseline` then exited 1 (*present at base and not
here*) and `chain_check.py --baseline` exited 1 (*git does not carry this file
at HEAD*).

Asking the merge base is correct: it is what makes the rule about what the
work item was. What is missing is the order. The closure has to merge before
the pull request that retires the directory. `spec.md` A14 describes the
post-release fold as closing the seven open rows and then running `settle
--retire`. Read that way, one pull request cannot meet it. Re-homing has the
same problem, and a worse one: a row deleted from `overview.md` is refused by
`--baseline` on any pull request. So a re-homed row is also a ✅ naming where
it went.

### 🟡 3 — A spec deleted in one merged pull request lets its directory go in the next with no marker

`skills/verify/scripts/unverified_check.py:1115` refuses the rule arm only when
`spec.md` is present at the ref it asks. `settle` asks the working tree.
`released` checks only that the directory was on the release branch, never
whether it held a spec there. `docs/review-chain-spec.md:755` and the
predicate's docstring (`unverified_check.py:1107`) claim that *a branch that
deletes a `spec.md` in one commit and the directory in the next is still a
deletion*. That holds inside one pull request and fails across two.

**Executed.** A fixture work item had a `spec.md`, a routing declaration, a
closed memo and no marker anywhere. As a control, deleting it whole in one
pull request is refused by `unverified_check` and `chain_check` (exit 1).
Pull request 1 deletes only `spec.md`, and all three readers exit 0 — nothing
refuses it. After it merges, pull request 2 runs `settle --retire`, which
removes the directory *retired by the rule, with no marker*. All three readers
exit 0 with `retired: by the rule`.

This is the loss the module docstring ranks worst: *a directory deleted with
nothing absorbing it, which nobody can [see]*. D3's words are *a released work
item that wrote no `spec.md`*, and "wrote none" is a question about history.
Asking history instead changes nothing on this tree. Read with `git log`: none
of the eleven spec-less directories ever held a `spec.md` under any root, and
`.github/workflows/hygiene.yml:30` checks out with `fetch-depth: 0`.

### 🟡 4 — The survivor sweep treats any directory under any `specs/` as a work item

`skills/code-review/scripts/survivor_check.py:522` defines `WORK_ITEM_DIR` as
`^((?:[^/]+/)*?specs/[^/]+)/`. That matches `docs/specs/login-flow/`,
`examples/specs/x/` and any other `specs/` segment. `retired_directories` then
asks `retired_by_rule` about it. A directory with no `spec.md` and no
`overview.md` has nothing open, so it counts as retired and leaves the range
on both sides.

**Executed.** In a fixture, a range deleted `docs/specs/login-flow/` whole.
`retired_directories` returned `{'docs/specs/login-flow'}`, and `corrected()`
measured 0 sentences from the removed file. A user repository that keeps
design notes under `docs/specs/<name>/` loses the sweep for every whole
deletion there, and the sweep prints nothing to say so. Nothing in this
repository tracks such a path today (`git ls-files` read). `survivor-check`
ships under `bin/`.

### ⬜ 5 — The report says `settle --retire` removes a spec-less directory that a ledger row is keeping

`skills/settle/scripts/settle.py:614` appends every spec-less directory that
passes the predicate to `survey["rule"]` before the anchored guard is applied.
`report` (`settle.py:765`) then prints it under the heading *`settle --retire`
removes these with no marker*, while the *anchored* heading above says the
same directory is kept. `retire()` behaves correctly and keeps it, which
`test_a_row_anchored_inside_a_rule_arm_directory_keeps_it` pins. Only the
listing contradicts itself.

## What was checked and holds

These are the judgments the spawn asked to attack. Each is labeled with how
it was established.

- **One predicate, four readers — read.** `settle.py#survey` and
  `settle.py#retire`, `unverified_check.py#main`, `chain_check.py#main` and
  `survivor_check.py#retired_directories` all call `retired_by_rule` on the
  one loaded module. None re-spells the spec or open-row test. Each CI reader
  adds its own *directory is gone* test (disk for two, `tree_at(b)` for the
  sweep). That is a precondition, not a second predicate. The evidence-todo
  rule moved into `todo_open_rows`, and `settle.open_rows` delegates to it.
  `.github/scripts/fold_ledger.py#open_rows` stays a copy on purpose, and the
  docstrings say so.
- **A partial removal is still a deletion — read.** Both CI arms require the
  whole directory to be gone. A memo removed from a directory that stays
  falls through to the old refusal.
- **An open row at the base is still refused — executed** (finding 2's
  fixture). A `spec.md` at the base is still refused inside one pull request
  (finding 3's control).
- **The #511 guard sees rows above the first marker and every
  `seal/ledger/*.md` — read and executed.** Two of the fixture's three rows
  were caught, including one in a line opening with an HTML comment opener. Finding 1 is the
  population outside that.
- **REMOVED and narrow against `CLAUDE.md` — read.** `REMOVED_SAYS` states
  *REMOVED, not re-pointed* in `CLAUDE.md`'s words. `NARROW_SAYS` names the
  multi-anchor answer as the owner's, which is `questions.md` Q2's default and
  `seal/ledger.md`'s S12 reservation.
- **Floors were moved, not lowered — read.** In every G8 case the diff
  touches, a floor of one (`assert listed`, `assert records`, `assert items`,
  `assert found`, `assert mirrors`, `assert with_rounds`, `assert paths`) is
  replaced. The replacement is either an independent listing that holds at
  any size (`conftest.committed_round_records_on_disk`, a disk walk plus `git
  cat-file -e`, or a second filesystem listing compared for equality) or a
  property moved into a corpus built in `tmp_path` (`assert teeth`, the
  optional-row count, the `kr` mirror). No literal got smaller.
  `test_release_hygiene.py`'s replacement asserts something stronger than
  what it removed.
- **No document still says the retired sentences — read.** `git grep` finds
  *Nothing in `seal/ledger.md` moves*, *kept by name* and the fold's range row
  only in the tests that pin their absence, in `CHANGELOG.md`, and in the
  dated 2026-09-22 row of `docs/one-root-by-lifetime.md`. That row is a record
  of a moment and is superseded by the new dated section rather than edited.
  The Korean edition carries the same four rows.
- **The empty root is settled, and nothing else is — executed.**
  `unverified_check.py seal/specs/` under a present `seal/` with no `specs/`
  exits 0 with the settled sentence. Adding a mistyped second path exits 2.
- **Windows path handling — read, not run.** Every new comparison works on
  `/`-joined git paths. `ntpath.dirname` keeps them and `under_root` splits on
  `/`. Nothing here assumes `os.sep`. Execution is the Windows leg's, as
  `overview.md` says.
- **A10's divergence — read.** An emptied clone whose removal takes three
  directories with a `spec.md` and no marker, and one with open rows, is the
  deletion G5 refuses. Exit 1 is the right answer.
- **`98e1183` was committed red — executed.** The narrow module
  `tests/test_no_document_names_the_old_roots.py` is 1 failed and 15 passed at
  `98e1183`, and 16 passed at `bc7a869`. The branch squashes, so this changes
  nothing at the target SHA.
- **The survivor-count drop from 15 to 7 was not caused by this branch —
  executed.** f8f1c9d's `survivor_check.py` and 4d19cc0's give identical
  counts over the same three ranges. The count is 15 at `e463a4c`, 7 at
  `4d19cc0`, and 15 at 4d19cc0 with this work item's `survivors.md` removed.
  `wanted` is unchanged on this branch and subtracts every n-gram the range
  writes, a committed `survivors.md`'s quotes included. The mechanism is
  f8f1c9d's. Run the way CI runs it (every `survivors.md` passed as
  `--exempt`), the sweep exits 0 and prints 7 `exempt` lines. The other 8
  quoted rows vanish without a line. It goes under Deferred rather than as a
  finding here.

## Regression tests to plant

Each one has to be seen red against the target SHA before it is committed
(`agent-contract` §15). Every proposed case name below is new.

- `tests/test_settle_reads_before_it_removes.py` — replace
  `test_a_quoted_anchor_is_not_a_row` with a case in which a fenced ledger row
  anchored inside a folded directory keeps that directory at exit 1, plus a
  second fixture for `docs/sub/_evidence.md` (finding 1). Red today: the
  directory is removed.
- `tests/test_unverified_rows_close.py` and
  `tests/test_chain_check_at_the_pull_request.py` — a case in which a spec
  deleted by an earlier merge is not a rule retirement: base history holds a
  `spec.md` that a merged commit deleted, and the branch removes the
  directory. Expect exit 1 from both readers (finding 3). Red today: both exit
  0.
- `tests/test_a_corrected_sentence_survives_elsewhere.py` — a case in which a
  `docs/specs/<name>/` directory deleted whole stays in the range
  (finding 4). Red today: `retired_directories` returns it.
- `tests/test_settle_reads_before_it_removes.py` — a case pinning the
  skill's sentence that a closed row merges before its directory goes
  (finding 2, §14).

## Facts for the evidence ledger

- The #511 guard's population is `seal/ledger.md` plus `seal/ledger/*.md`,
  live lines only. evidence-check's population is those two plus
  `docs/**/_evidence.md`, every line. Once finding 1 is fixed, the fragment's
  G3 row (*`settle` names every live ledger row*) is false and needs
  `--reverify` against the new unit.
- `survivor_check.py#wanted` subtracts n-grams written anywhere in the range,
  a `survivors.md` included. Measured the same at f8f1c9d and 4d19cc0 (15, 7,
  and 15 without the file).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the #511 guard reads live lines of two ledger addresses; evidence-check reads every line of three, so a fenced or `_evidence.md` anchor is removed and reported BROKEN afterwards | `skills/settle/scripts/settle.py:459` | open | executed: fenced row's directory removed, then `file not found` from evidence-check; `evidence_check.py:1207` scans the whole text; `evidence_check.py:919` lists the third address |
| 2 | 🟡 a memo row closed and its directory retired in one pull request passes `settle --retire` and fails `unverified_check` and `chain_check` at the merge base; the skill prescribes that order | `skills/settle/SKILL.md:94` | open | executed: settle exit 0, then both readers exit 1; also `docs/the-evidence-ledger.md:184` and `RULE_KEPT_HEADING` |
| 3 | 🟡 a spec deleted in one merged pull request lets the next retire its directory with no marker, and every reader passes both pull requests | `skills/verify/scripts/unverified_check.py:1115` | open | executed: the one-PR control is refused; PR 1 and PR 2 each exit 0 in all three readers; the claim at `docs/review-chain-spec.md:755` holds only inside one pull request |
| 4 | 🟡 `WORK_ITEM_DIR` matches any `*/specs/<x>/`, so a whole deletion under `docs/specs/` is dropped from the survivor range | `skills/code-review/scripts/survivor_check.py:522` | open | executed: `retired_directories` returned `docs/specs/login-flow`; `corrected()` measured 0 sentences |
| 5 | ⬜ the report lists an anchored spec-less directory under *`settle --retire` removes these* | `skills/settle/scripts/settle.py:614` | open | read: `survey["rule"]` is filled before `holding` is applied; `retire()` keeps it correctly |
| 🟢 | one predicate asked by four readers, not re-derived | `skills/verify/scripts/unverified_check.py:1090` | not a defect | read: each reader calls `retired_by_rule` on the loaded module |
| 🟢 | a partial removal or a memo removed from a directory that stays is still a deletion | `skills/verify/scripts/unverified_check.py:1384` | not a defect | read: both CI arms require the directory gone |
| 🟢 | the guard reads rows above the first marker and every fragment | `skills/settle/scripts/settle.py:435` | not a defect | read and executed (P1: two of three rows caught) |
| 🟢 | REMOVED and narrow wording matches `CLAUDE.md` and Q2's default | `skills/settle/scripts/settle.py:374` | not a defect | read |
| 🟢 | G8 floors moved to independent listings or `tmp_path` corpora, none lowered | `tests/conftest.py` | not a defect | read, the diff of every re-pointed case |
| 🟢 | no document still says a fold is a work item or that the ledger does not move | `skills/settle/SKILL.md:211` | not a defect | read, `git grep` outside `seal/specs/` and `CHANGELOG.md` |
| 🟢 | an absent `seal/specs/` under a present root is exit 0, and a mistyped path is still exit 2 | `skills/verify/scripts/unverified_check.py` | not a defect | executed |
| 🟢 | the A10 divergence: exit 1 for a hand removal of non-retirable directories | `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/overview.md` | not a defect | read |
| 🟢 | `98e1183` committed with the old-roots module red, fixed at `bc7a869` | `tests/test_no_document_names_the_old_roots.py` | not a defect | executed, narrow: 1 failed at `98e1183`, 16 passed at `bc7a869` |
| 🟢 | the survivor drop from 15 to 7 is not this branch's code | `skills/code-review/scripts/survivor_check.py:641` | not a defect | executed: the base and head scripts agree on all three ranges; see Deferred |
| 🟢 | Windows path handling in the new comparisons | `skills/code-review/scripts/survivor_check.py:612` | not a defect | read only; execution unverified, answered by the Windows leg at this pull request |

## Executed probes

| What was run | Result |
|---|---|
| fixture: three folded directories, anchored by a fenced row, a comment-line row and a row after a stray backtick; `settle --retire`, then `evidence-check .` | settle exit 1, fenced directory removed and the other two kept; evidence-check then reports that anchor `file not found` |
| this repository's ledger at 4d19cc0: `ANCHOR_RE` over every line vs `COORDINATE_RE` over live lines | 1938 and 1938; no non-live anchor under a `specs/` path |
| fixture: open memo row closed on the branch, then `settle --retire`, then the three readers against the base | settle exit 0; `unverified_check` exit 1; `chain_check` exit 1; `survivor_check` exit 0 |
| fixture: spec plus declaration plus closed memo; one-PR delete (control), then PR 1 deletes only `spec.md`, merged, then PR 2 runs `settle --retire` | control: `unverified_check` 1, `chain_check` 1; PR 1: all three exit 0; PR 2: settle removes by the rule, and all three exit 0 |
| fixture: range deletes `docs/specs/login-flow/` whole; `retired_directories` and `corrected()` | `{'docs/specs/login-flow'}`; 0 sentences measured |
| `survivor_check.py` from f8f1c9d and from 4d19cc0, over `f8f1c9d...e463a4c`, `f8f1c9d...4d19cc0`, and 4d19cc0 with `survivors.md` removed | 15 / 7 / 15 for both scripts, all exit 1 |
| head `survivor_check.py --range f8f1c9d...4d19cc0` with every `survivors.md` passed as `--exempt`, as `hygiene.yml` passes them | exit 0; 7 `exempt` lines printed |
| `unverified_check.py seal/specs/` under a present `seal/`, no `specs/`; then with a second mistyped path | exit 0 with the settled sentence; exit 2 *no such path* |
| `bin/test tests/test_no_document_names_the_old_roots.py` at `98e1183` and at `bc7a869` | 1 failed and 15 passed; 16 passed |
| `bin/settle` and `bin/evidence-check --strict .` on the clone at 4d19cc0 | settle exit 0 (8 to retire by the rule, 2 kept, 2 ungrouped); evidence-check exit 0 |
| the full suite, the repository-wide lint and the typecheck (the broad gate) | not yet — not run by this round, and not this agent's to run; the sealer's single run after the rounds settle |

The fixtures were built by one Python probe script under the session
scratchpad, which drove git through `subprocess`, ran once, and was deleted.
So were a second script and a copy of the base `survivor_check.py`. The
scratch clone was deleted after the report was written.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a committed `survivors.md` silences the survivors it quotes by subtraction in `survivor_check.py#wanted`, with no `exempt` line printed, with or without `--exempt`; mechanism present at f8f1c9d, so it predates this branch | not filed yet — `overview.md` §*Not done* hands it to the repository owner to file as an issue | the repository owner, who files the issue |

## Paste-ready fixes

Finding 1 — `skills/settle/scripts/settle.py`, in `anchored_rows`, in place of
the block from `live_lines = load(...)` to `if not live: continue`. The
docstring paragraph that names `live_lines` changes with it. Precondition:
`root` is the repository root, and `docs/` is read from disk the way the
checker reads it.

```python
    sources = []
    if os.path.isfile(under(root, LEDGER)):
        sources.append(LEDGER)
    for path in sorted(glob.glob(os.path.join(under(root, FRAGMENTS), "*.md"))):
        sources.append(f"{FRAGMENTS}/{os.path.basename(path)}")
    # evidence-check's third address, still read for a repository that never
    # moved it (`evidence_check.py#default_patterns`). A row there anchored
    # inside a retiring directory is BROKEN after the removal all the same.
    for path in sorted(
        glob.glob(os.path.join(root, "docs", "**", "_evidence.md"), recursive=True)
    ):
        sources.append(os.path.relpath(path, root).replace(os.sep, "/"))
    found = []
    for rel in sources:
        with open(under(root, rel), encoding="utf-8") as f:
            lines = f.read().split("\n")
        # Every line, fenced and commented ones included. evidence-check reads
        # an anchor wherever it stands (`check_text` scans the whole file), and
        # a guard that reads fewer lines than the checker keeps fewer
        # directories than the checker will report BROKEN. `live_lines` biases
        # an ambiguous line toward "not live", which keeps a directory for the
        # marker reader and would remove one here.
        for number, line in enumerate(lines, start=1):
```

Finding 1 — `tests/test_settle_reads_before_it_removes.py`, in place of
`test_a_quoted_anchor_is_not_a_row`:

```python
def test_a_fenced_anchor_still_keeps_the_directory(tree):  # NAME NOT IN TREE
    """evidence-check reads an anchor inside a fence as a coordinate like any
    other, so the guard has to as well: a fenced row's directory removed is a
    BROKEN row found after the fact, which is #511."""
    fold(tree, "1700000001-alpha")
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + f"\n```markdown\n{INSIDE_ROW}\n```\n",
        encoding="utf-8",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text


def test_a_row_at_the_old_evidence_address_keeps_the_directory(tree):  # NAME NOT IN TREE
    fold(tree, "1700000001-alpha")
    old = tree / "docs" / "area" / "_evidence.md"
    old.parent.mkdir(parents=True)
    old.write_text(INSIDE_ROW + "\n", encoding="utf-8")
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert "docs/area/_evidence.md:1" in text, text
```

Finding 2 — `skills/settle/SKILL.md:94-95`, in place of *Once it has, the next
`settle --retire` takes the directory.*:

```markdown
**Close it in a pull request of its own, and let that one merge first.** The
CI readers ask the rule of the merge base, so a row closed and its directory
retired in one pull request is still open where they look, and
`unverified-check` and `chain-check` refuse the removal that `settle --retire`
just made. A row re-homed is closed the same way — ✅ naming where it went —
because a row deleted from `overview.md` is refused on any pull request. Once
the closure has merged, the next `settle --retire` takes the directory.
```

Finding 2 — `skills/settle/scripts/settle.py`, `RULE_KEPT_HEADING`. The same
sentence goes into `docs/the-evidence-ledger.md:184` (*closing each row or
re-homing it, in a pull request merged before the retirement, is what lets
the next retirement take the directory*):

```python
RULE_KEPT_HEADING = (
    "kept by the rule — no `spec.md`, but the record still holds an open "
    "row, which\nleaves by being closed (✅ with what closed it) in a pull "
    "request merged before the\none that retires the directory, never with it:"
)
```

Finding 2 — the §14 pin, in `tests/test_settle_reads_before_it_removes.py`:

```python
def test_the_skill_says_a_closed_row_merges_before_its_directory_goes():  # NAME NOT IN TREE
    text = flat(skill())
    assert "merge first" in text, (
        "the skill lets a fold close a row and retire its directory in one "
        "pull request, which the CI readers refuse at the merge base"
    )
```

Finding 3 — `skills/verify/scripts/unverified_check.py`, a helper beside
`retired_by_rule` and one changed line inside it. Precondition: history
reaches back past the deletion. `hygiene.yml` checks out with `fetch-depth:
0`. In a shallow clone that cut it off, the helper answers *never*, which is
today's behaviour. A git failure answers *wrote one*, which keeps the
directory.

```python
def wrote_a_spec(root, ref, directory):  # NAME NOT IN TREE
    """Whether any commit reachable from `ref` (HEAD when None) touched
    `directory/spec.md` — D3 names a work item that WROTE no spec, which is a
    question about history, not about the tree the branch left. Asked of the
    merge base alone, a spec deleted by an earlier merge read as never written.
    """
    r = subprocess.run(
        ["git", "-C", root, "log", "-1", "--format=%H", ref or "HEAD", "--",
         f"{directory}/{SPEC}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode != 0 or bool(r.stdout.strip())
```

```python
    if f"{directory}/{SPEC}" in paths or wrote_a_spec(root, ref, directory):  # NAME NOT IN TREE
        return False
```

Finding 3 — `docs/review-chain-spec.md:755`, the sentence's end:

```markdown
the merge base rather than of the tree the branch left, and asked whether the
directory ever held one, a spec deleted in one commit — or in an earlier
pull request — and the directory in the next is still a deletion.
```

Finding 3 — the regression case, in
`tests/test_chain_check_at_the_pull_request.py`, using that module's `repo`,
`write`, `commit`, `git`, `declaration` and `run`, with the same shape in
`tests/test_unverified_rows_close.py`:

```python
def test_a_spec_deleted_by_an_earlier_merge_is_not_a_rule_retirement(repo):  # NAME NOT IN TREE
    item = "seal/specs/1787700001-a-spec"
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration())
    write(repo, f"{item}/spec.md", "# a spec\n\nA rule nobody folded.\n")
    commit(repo, "a work item that stated a rule")
    (repo / item / "spec.md").unlink()
    commit(repo, "an earlier pull request drops the spec")
    git(repo, "switch", "-q", "feature")
    git(repo, "merge", "-q", "base")
    shutil.rmtree(repo / item)
    commit(repo, "the directory, removed with no marker")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "retired: by the rule" not in out, out
```

Finding 4 — `skills/code-review/scripts/survivor_check.py:520-522`.
Precondition: a committed root is `seal/specs/` or the legacy top-level
`specs/`. Local mode is never committed, so it never reaches a range.

```python
# A work item's directory, read off a path: the `seal/` root's `specs/`, or
# the legacy top-level `specs/` a repository from before 0.4.0 still carries.
# Anchored at the start, so `docs/specs/<name>/` is a directory of prose
# like any other and stays in the range.
WORK_ITEM_DIR = re.compile(r"^((?:seal/)?specs/[^/]+)/")
```

```python
def test_a_specs_directory_outside_the_seal_root_stays_in_the_range(tmp_path):  # NAME NOT IN TREE
    # Build with this module's fixture helpers: a base commit holding
    # docs/specs/login-flow/design.md, and a range that deletes the directory whole.
    ...
    assert survivor.retired_directories(root, a, b, ["docs/specs/login-flow/design.md"]) == set()
```

Needs a fix: yes — findings 1, 2, 3 and 4 (🟡); finding 5 is ⬜ and not counted
Loses a record or crashes: no

The broad gate has not come due, because this round leaves four 🟡 open. The
sealer's spawn waits until a later round closes them.

## Proof block

Files opened in this round, all at 4d19cc0 in the scratch clone unless noted:

- `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/spec.md`, `overview.md`, `questions.md`, `survivors.md`, and the ledger fragment `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md`
- #517's body and both owner comments (`gh issue view 517 --comments`, in the user's checkout)
- `skills/settle/scripts/settle.py` (the diff, plus `COORDINATE_RE` and `work_items`)
- `skills/verify/scripts/unverified_check.py` (the diff, `main`'s baseline block, `check_text`, `overviews`, `live_lines`'s docstring)
- `skills/code-review/scripts/chain_check.py` (the diff, `main`, `pull_request_state`, `declared_for_this_branch`)
- `skills/code-review/scripts/survivor_check.py` (the diff, `wanted`, the `--exempt` argument)
- `skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE`, `check_ledger`, `check_text`, `default_patterns`, `claim_lines`)
- `skills/settle/SKILL.md`, `docs/the-evidence-ledger.md`, `docs/review-chain-spec.md`, `docs/release-checklist.md`, `docs/one-root-by-lifetime.md`, `README.md`, `seal/README.md` (their diffs); `docs/one-root-by-lifetime.ko.md` lines 584 and 598
- `tests/test_settle_reads_before_it_removes.py` (fixtures and the guard cases), `tests/test_chain_check_at_the_pull_request.py` (the diff and fixture helpers), and the diffs of `tests/conftest.py`, `tests/test_a_finding_id_is_a_bare_integer.py`, `tests/test_the_reopening_is_one.py`, `tests/test_release_hygiene.py`, `tests/test_routing_is_recorded.py`, `tests/test_the_pull_request_language_is_the_repositorys.py`, `tests/test_chain_hooks_hardening.py`, `tests/test_handoff_outlives_the_merge.py`, `tests/test_a_corrected_sentence_survives_elsewhere.py`
- `.github/workflows/hygiene.yml` (the survivor step and `fetch-depth`), `.github/scripts/run_tests.py` (its docstring), `bin/evidence-check`
- the plugin's `skills/code-review/SKILL.md` §*Findings format*
