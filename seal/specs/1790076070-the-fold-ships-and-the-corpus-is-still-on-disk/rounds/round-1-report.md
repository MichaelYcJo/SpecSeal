# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — round 1 report

Reviewed at `07b7dc1b0246fb838dc9826628badb36e2f662e5` against
`origin/release/v0.13.1` (`64036785`), in a `git clone --no-local` of the
checkout. First round, so there is nothing inherited. Spec compliance first,
then quality, in the order the prompt set.

## How the findings relate

```
the fold writes standing statements ──► two of them are false of the tree (1, 2)
the fold's own account of itself    ──► the changelog fragment ships three false facts (3)
the fold re-points the corpus readers ─► one re-point crashes on its only live arm (4)
                                      └► one new guard is red in an ordinary state (5)
the fold repairs five broken ledger rows ─► and writes a sixth of the same class (6)
```

Findings 1 to 3 are statements a reader of the release will act on. Findings 4
and 5 are test units this branch added. Finding 6 repeats the defect the branch
found in phase 11. Two ⬜ items follow.

## Findings from reading

### 🟡 1 — the folded statement about the terminal-line join says the opposite of the code

`docs/review-chain-spec.md:2081` says the markers that stop a join are "a line
beginning `#`, `**`, `<` or a horizontal rule". The code says the reverse.
`skills/code-review/scripts/round_record.py:1263-1270`, the comment above
`BLOCK_START`, says a continuation opening with `**bold**`, with an HTML tag or
with an indent is joined, not stopped. A `#` stops the join only when a space
follows it. The work item this paragraph folds (1789347354) wrote this change
itself. Its `spec.md` at `6d410023`, line 156, reads: "a continuation beginning
`#`, `**`, `<`, `1)` or an indent joins".

This matters because the paragraph closes by telling the next reader not to
widen the marker list. A reader who believes `**` and `<` are already on the
list will build on a list that does not exist. The folded prose restates the
state that 1789347354 was opened to remove.

### 🟡 2 — the folded statement about `bin/` wrappers omits the exception the tree carries

`docs/review-chain-spec.md:2004` says: "Every `skills/*/scripts/*.py` a document
names has a `bin/` wrapper pair". `skills/code-review/scripts/chain_check.py` is
named in shipped documents, for example `templates/sdd-round.md:19` and
`skills/code-review/SKILL.md:48`, and `bin/` has no `chain-check` wrapper. The
exception is deliberate. `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:67`
classifies `chain_check.py`. The folded item's spec, 1789338080 at `6d410023`,
lists "A `bin/chain-check` wrapper" under Out, with its reasons.

The statement now sits in a document that outranks the SDD set, and the tree
contradicts it. A reader can conclude one of two wrong things: that
`chain_check.py` is a defect to fix by adding a wrapper, or that the
classification case is wrong.

### 🟡 3 — the changelog fragment ships three facts phase 11 already proved false, and leaves out a changed check

`seal/specs/1790076070-…/changelog.md` is gathered into `CHANGELOG.md` at the
release.

- **Line 11: "`seal/ledger.md` is byte-identical at the end of this branch."**
  Phase 11 (`phases/phase-11.md`, the step 3 table) records "25 insertions,
  28 deletions. A7 does not hold". `overview.md`'s divergence table says the
  same.
- **Line 7: "become 12 and 38".** Phase 11 measured 51 files after the fold, and
  explained why 38 was only `plan.md`'s projection.
- **Line 26: "Ten checks … that the fold turns red, and every one of them was
  re-pointed".** Phase 1's table has nine floors that turned red (F1–F5,
  F7–F10). F6 was measured green and declined, which the same paragraph says
  four sentences later. "Two more moved to fixtures" undercounts too: F3, F7
  and F8 are three floors.
- **Left out:** `chain_check.py`, which ships to plugin users, now prints
  `retired: …` and passes a deleted `routing.md` that it used to refuse. That
  is a change in a shipped check's behaviour. The fragment mentions only the
  wrap-limit change.

A released changelog entry is never corrected afterwards (`survivors.md` says
so itself), so these facts have to be fixed before the release gathers them.

### 🟡 6 — the branch writes a new ledger row of the class it just repaired

Phase 11 found five permanent rows anchored inside a work item directory that
`settle --retire` removed. It repaired them and recorded the finding.
`seal/ledger/1790076070-….md` row 4 then anchors
`seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/survivors.md#"## Whole ranges"`.
This row moves into `seal/ledger.md` at the release. The next fold then retires
this work item's directory, and the row comes back BROKEN. That is exactly
what happened to the five rows.

A grep for `` `seal/specs/…# `` anchors across `seal/ledger.md` and
`seal/ledger/*.md` finds three hits. The first is line 78, whose directory
this branch kept on purpose. The second is row 3's own prose example. The
third is this row, and it is the only new instance.

The cause is still in place. `skills/settle/scripts/settle.py#coordinates`
reads ledger coordinates only to group work items. Nothing refuses to retire a
directory that a ledger row anchors into. None of #499–#510 covers this.
Fixing the instance is this branch's job. Whether the cause gets a fix or an
issue is for the orchestrator to decide.

## Findings from execution

### 🟡 4 — the memo re-point in 07b7dc1b crashes on the one arm it kept

`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:315` calls
`read(os.path.relpath(memo_path, ROOT))`. Inside this test, `read` is a local
list (line 253, `read = [str(proj / "seal" / "ledger.md")]`). The comment at
line 288 of the same function warns about exactly this, and the line the
branch replaced used `flat` for that reason. At HEAD the memo is gone, so the
test returns before it reaches the call and stays green.

**Executed:** I restored 1788501054's `overview.md` from `6d410023` in the
clone and ran the case, and it failed with `TypeError: 'list' object is not
callable` at line 315. With the file removed again it passed.

The commit message and the new `Re-read 2026-09-23` note on ledger row R3 both
say the memo "is read only while it exists". No one has run that arm, and it
cannot pass. The same commit's five-copies case asserts `folded_items` before
it skips the memo. This case skips the memo with no guard at all.

### 🟡 5 — `_the_corpus_covers_every_work_item_that_has_rounds` fails on an uncommitted round record

`tests/test_a_finding_id_is_a_bare_integer.py:733` treats any work item with a
`round-N.md` on disk and none in `committed_records()` as a listing that lost
it. A round record that has been written but not yet committed is exactly that
shape. The sibling guard in `tests/test_chain_check_at_the_pull_request.py:2207`
calls this "the ordinary state of a review round mid-flight" and allows it.

**Executed:** I planted an uncommitted
`seal/specs/1790076070-…/rounds/round-1.md` in the clone and ran
`test_the_committed_records_only_lose_a_miscount`. It failed with "1 work
item(s) hold a round record on disk and contributed nothing to the committed
corpus … The listing or the filter above lost them". Without that file the
case passed. The failure message blames the listing, which is not at fault.
The first `round_record.py new` of every work item puts the tree in this state
until the record is committed.

## Lower severity

### ⬜ 7 — the wrap skip matches the stripped line and the reader matches the raw one

`tests/test_docs_line_wrap.py:168` runs `FOLD_MARKER.fullmatch(stripped)`.
`skills/verify/scripts/unverified_check.py#FOLD_MARKER` is anchored
`^…$` on the unstripped line. So an indented or trailing-space marker gets
past the wrap check and is still not a fold record. The comment at line 43
promises that the two match exactly. Nothing breaks today, because all 88
markers start at column 0.

### ⬜ 8 — `gathered_entry` stops at any line that starts with `#`

`tests/conftest.py#gathered_entry` treats `line.startswith("#")` as a heading.
A gathered body line at column 0 that begins with an issue number would cut
the block short. The only effect is a false red, because callers look for a
phrase in the block. `round_record.py#BLOCK_START` requires a space after the
`#` for the same reason.

## What was checked and found sound

- **The chain check's retirement arm (prompt item 2).** `chain_check.py`
  builds `retired` from `reader.folded_items(root)`, and that function reads
  only through `live_lines`. A marker inside a fence, inside a comment or
  inside a code span therefore never counts. A directory removed with no marker
  still reaches the original refusal:
  `test_a_deleted_declaration_with_no_marker_is_still_refused` plants that case
  and asserts no `retired:` line. I ran it with the three other new cases (see
  probes).
- **The ledger removals (prompt item 3).** The three removed rows had a
  retired `spec.md` as their only anchor. Each claim was about that spec's
  prose or a measurement made at that time. Removing them follows `CLAUDE.md`'s
  rule. The two narrowed rows re-point nothing: no new anchor was written, and
  the surviving anchor is a code anchor that was already in the row. Whether a
  multi-anchor row should instead be removed whole is the owner's question,
  which `overview.md` already names. I am not raising it again.
- **The four merge notes (prompt item 4).** S9: the fold added the update-notice
  marker and one paragraph under `## 6. After the merge`, and
  `grep -c "on the tag" docs/release-checklist.md` returns 0. R3 (releases):
  `## A milestone answers *when*` gained exactly one marker line. The opt-in
  headings note: both headings and the parity arm's silence row are unchanged.
  R3 (inode): accurate about what changed, but it describes an arm that
  crashes (finding 4). The prompt says every re-verified row got a dated note.
  That is not what the diff shows. Most rows changed only their hash. That is
  still a correct re-verify, since `CLAUDE.md` asks for a re-read and
  `--reverify`, not a note.
- **The re-points (prompt item 4).** The five-copies case asserts
  `folded_items(ROOT) >= {item}` before it accepts the gathered block, so it
  lowers nothing. The dogfood case accepts the `CHANGELOG.md` marker that
  `gather_changelog.py` writes, and a hand edit would not leave that marker. It
  is not a lowering. The memo case is the exception (finding 4).
- **The survivors Range cell (prompt item 5).** The cell holds only
  `origin/release/v0.13.1...HEAD`. It matches
  `survivor_check.py#RANGE_CELL` once the backticks are stripped, and it is
  the literal range `hygiene.yml` builds for a pull request into
  `release/v0.13.1`. There is no parenthetical.
- **Other folded statements I checked against code and found true:** the
  finding-id rule (`FINDING_ID_RE`), the report path `new` reads by default
  (`REPORT_NAME`), `--written-late`, the interpreter floor (3.12 in both
  `round_record.py` and `.github/scripts/run_tests.py`), `new`/`close` running
  `chain_check --worktree`, the order in which the broad gate resolves its base,
  the lenient-ledger exit-1 notice, correction-check's tie to the first parent,
  the unverified-check merge base and its exit 2, the survivor step printing why
  it skips on a `main` base, the three timer exemptions, the two language rows
  in `templates/config.md`, and the marker count (88 markers, 88 distinct, one
  89 columns wide).

## Regression tests to plant

| Destination | Case |
|---|---|
| `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py` | restore the memo into a `tmp_path` copy (or monkeypatch `ROOT`) and assert the memo arm runs, so the arm has been seen both green and red (§15) |
| `tests/test_a_finding_id_is_a_bare_integer.py` | plant an uncommitted `round-1.md` in a work item that has no committed record and assert the corpus guard does not fail |
| `tests/test_evidence_check.py`, or the ledger-hygiene module | no row of `seal/ledger.md` or `seal/ledger/*.md` anchors under `seal/specs/<id>/` except an id that `spec.md` G3 keeps by name |

## Facts for the evidence ledger

- `round_record.py#BLOCK_START` joins a continuation that opens with `**`, `<`
  or an indent, and it stops at `#` only when a space follows. This is the
  fact that finding 1's corrected paragraph should be anchored to.
- `chain_check.py` is the one `skills/*/scripts/*.py` with no `bin/` wrapper,
  and `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`
  classifies it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The folded terminal-line paragraph says `#`, `**` and `<` stop a join, and the code joins `**` and `<` and stops `#` only before a space | `docs/review-chain-spec.md:2081` | open | `round_record.py:1263-1270`, and 1789347354's own spec line 156 at `6d410023` |
| 🟡 2 | The folded wrapper paragraph says every named script has a `bin/` pair, and `chain_check.py` has none by classification | `docs/review-chain-spec.md:2004` | open | `ls bin`, and `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:67` |
| 🟡 3 | The changelog fragment says the ledger is byte-identical, gives 38 files and ten re-pointed floors, and leaves out the `retired:` change to `chain_check` | `seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/changelog.md:7` | open | the phase 11 step 3 table and before/after table, and the phase 1 floor table |
| 🟡 4 | The memo arm calls the local list `read`, so it raises `TypeError` whenever the memo exists, and it has no fold guard | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:315` | open | executed: memo restored, TypeError; memo removed, pass |
| 🟡 5 | The corpus guard fails on an uncommitted round record and blames the listing | `tests/test_a_finding_id_is_a_bare_integer.py:733` | open | executed: planted an uncommitted round-1.md, got 1 failed; without it, 1 passed |
| 🟡 6 | A new ledger fragment row anchors inside this work item's directory, which the next retirement removes | `seal/ledger/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk.md:6` | open | the same class as the five rows phase 11 repaired; `settle.py#coordinates` refuses nothing |
| ⬜ 7 | The wrap skip matches the stripped line, while the reader matches the raw line | `tests/test_docs_line_wrap.py:168` | open | `unverified_check.py:107` |
| ⬜ 8 | `gathered_entry` treats any line starting with `#` as a heading | `tests/conftest.py#gathered_entry` | open | `round_record.py#BLOCK_START` requires a space |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_narrowed_ledger_read_says_what_it_skipped.py::test_an_inode_of_zero_does_not_fold_two_files_into_one`, with 1788501054's `overview.md` restored from `6d410023` | exit 1: `TypeError: 'list' object is not callable` at line 315. With the file removed again: 1 passed |
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py::test_the_committed_records_only_lose_a_miscount`, with an uncommitted `rounds/round-1.md` planted under this work item | exit 1: "1 work item(s) hold a round record on disk and contributed nothing". Without the file: exit 0, 1 passed |
| `bin/test tests/test_chain_check_at_the_pull_request.py tests/test_docs_line_wrap.py -k "retired or no_marker or fold_marker or marker_that_is_not"` | exit 0, 4 passed |
| The broad gate (`bin/test -q`, `uvx ruff check .`, `uvx ruff format --check .`) on the folded tree | not yet. It is the sealer's run, after the rounds settle, and this round did not run it |

Every probe ran in the clone. The planted files were removed afterwards, and
`git status --short` in the clone is empty.

## Paste-ready fixes

🟡 1 — replaces the paragraph under the 1789347354 marker in `docs/review-chain-spec.md`:

```
**A wrapped terminal line is one value, and the join stops at a blank line.**
A terminal row a narrow window wrapped is still one value, so a continuation
is joined to it. A line that opens a new markdown block stops the join too —
a heading marker with a space after it, a list or quote marker, a fence, a
thematic break or a setext underline — and a continuation opening with an
issue number, `**bold**`, an HTML tag or an indent is joined, because its
first characters cannot tell it from prose. The blank line is the only stop
that covers every shape, and that sentence is the one that keeps the next
reader from widening the marker list instead of trusting the blank line.
```

🟡 2 — replaces the paragraph under the 1789338080 marker in `docs/review-chain-spec.md`:

```
**A script a shipped document tells an agent to run is reachable by a
command.** Every `skills/*/scripts/*.py` a shipped document names either has
a `bin/` wrapper pair or is classified, with its reason, in the case that
pins this rule — `chain_check.py` is classified, because CI runs it by path
and no shipped document shows it as a command to type. Every document naming
a script also names a form that can be typed: the wrapper, or the script's
repository-relative path. A document that names a script and no way to reach
it is an instruction with no executable spelling.
```

🟡 3 — `seal/specs/1790076070-…/changelog.md`. Replace lines 6–11 with:

```
  `settle --retire` removes the directories the prose now covers. Measured
  before and after: 99 directories and 1,379 files under `seal/specs/`
  become 12 and 51, and the round-record corpus goes from 263 to 7. Eleven
  directories are kept by name — ten because they wrote no `spec.md` and so
  state no rule, and one because a permanent `seal/ledger.md` row anchors
  into its round record and the repository's own rule refuses a re-point.
  Five other `seal/ledger.md` rows anchored into a retired `spec.md`: the
  three whose only anchor that was are removed, and the two with a live code
  anchor keep it and drop the dead one.
```

Replace the opening of the floors paragraph with:

```
  **No floor literal was lowered.** Nine checks carried a population floor
  over `seal/specs/` that the fold turns red, and every one of them was
  re-pointed rather than reduced — `assert len(records) > 200` becomes *the
```

Replace "Two more moved to fixtures" with "Three more moved to fixtures".
Then add this paragraph before the wrap-limit paragraph:

```
  **The pull request's chain check now tells a retirement from a
  deletion.** A `routing.md` that `settle --retire` removed prints
  `retired: …` where a top-level `docs/` file carries the work item's
  `<!-- specs/<work-item-id> -->` marker on a live line, and is still refused
  where none does. The first fold put 88 such declarations in one diff, and
  the check had failed every one.
```

🟡 4 — `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:315`. Read
through `flat`, the module-level reader, as the old line did:

```python
    if not os.path.exists(memo_path):
        return
    memo = flat(os.path.relpath(memo_path, ROOT))
```

Seen red and green (§15) by restoring the memo from `6d410023` in a scratch
checkout, first as it is (green) and then with one pinned phrase edited (red).

🟡 5 — `tests/test_a_finding_id_is_a_bare_integer.py`. A work item counts as
lost only when at least one of its records is at HEAD:

```python
def _committed_at_head(specs_dir, item):
    """Whether any round record `item` holds on disk is also at HEAD.

    A record written and not yet committed is the ordinary state of a round
    mid-flight, which `_the_walk_found_every_committed_record` already
    allows; a work item whose records are all uncommitted was not lost by
    the listing, because the listing is of HEAD.
    """
    rounds = os.path.join(specs_dir, item, "rounds")
    for name in os.listdir(rounds):
        if not re.fullmatch(r"round-\d+\.md", name):
            continue
        spec = f"HEAD:seal/specs/{item}/rounds/{name}"
        probe = subprocess.run(
            ["git", "-C", ROOT, "cat-file", "-e", spec], capture_output=True
        )
        if probe.returncode == 0:
            return True
    return False
```

```python
    missed = sorted(
        d for d in with_rounds - covered if _committed_at_head(specs, d)
    )
```

🟡 6 — `seal/ledger/1790076070-….md` row 4. Anchor the claim at the code that
makes a range row excuse a range, and keep the measurement in the Verified
behavior cell. Then run `bin/evidence-check --reverify` to write the hash:

```
| A range that retires 88 work items reports 12,100 survivors, and one range row excuses every one of them | `skills/code-review/scripts/survivor_check.py#whole_range@<hash --reverify writes>` | …unchanged… | 2026-09-22 | …unchanged, plus: anchored at the checker rather than at this work item's `survivors.md`, which the next fold retires … |
```

Needs a fix: yes — 🟡 1 to 🟡 6: two folded statements the tree contradicts, a
changelog fragment with three false facts and one change left out, a re-point
whose remaining arm crashes, a new guard that goes red in an ordinary state,
and a ledger row that the next retirement breaks
Loses a record or crashes: no — finding 4's TypeError is in a test, on an arm
HEAD cannot reach, and finding 6's row breaks only at a later fold; nothing
shipped leaves the root or crashes

## Proof block

Files opened in this round (clone at `07b7dc1b`, unless the line says so):

- `seal/specs/1790076070-…/spec.md`, `overview.md`, `survivors.md`, `changelog.md`,
  `routing.md`, `phases/phase-11.md`; phase 1's and phase 2's floor tables (grep)
- `skills/code-review/scripts/chain_check.py` (main, 3990–4140)
- `skills/verify/scripts/unverified_check.py` (`FOLD_MARKER`, `live_lines`, `folded_items`)
- `skills/code-review/scripts/round_record.py` (`BLOCK_START`, `terminal_value`, floor, report path, `--written-late`, `run_check`)
- `skills/code-review/scripts/survivor_check.py` (exempt reader, `RANGE_CELL`, `whole_range`)
- `skills/settle/scripts/settle.py#coordinates`, `.github/workflows/hygiene.yml` (the survivor step)
- `skills/*/scripts/broad_gate.py`, `evidence_check.py`, `correction_check.py` (grep and the base-resolution excerpts)
- `tests/conftest.py`, `tests/test_docs_line_wrap.py`, `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`,
  `tests/test_a_record_precedes_the_fixes_it_commissions.py`, `tests/test_the_changelog_is_gathered_at_release.py`,
  `tests/test_a_finding_id_is_a_bare_integer.py` (the corpus guard and `committed_records`),
  `tests/test_chain_check_at_the_pull_request.py` (`_the_walk_found_every_committed_record`),
  `tests/test_no_document_names_the_old_roots.py` (scope), `tests/test_release_hygiene.py` (timer exemptions)
- `docs/the-broad-gate.md`, `docs/the-evidence-ledger.md`, `docs/measuring-a-run.md`, `docs/the-agent-set.md`,
  and the branch's diff of `docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`,
  `docs/issues-and-milestones.md`, `docs/release-checklist.md`, `docs/one-root-by-lifetime.md`
- `seal/ledger.md` (the branch's diff, and the Notes of the rows with merge notes), `seal/ledger/1790076070-….md`
- `git show 6d410023:` 1789338080's and 1789347354's `spec.md`, and 1788501054's `overview.md`
- `templates/config.md` and `templates/sdd-round.md` (grep); `gh issue view` titles for #499–#510
