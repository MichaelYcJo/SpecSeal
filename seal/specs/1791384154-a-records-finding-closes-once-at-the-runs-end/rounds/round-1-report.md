# 1791384154 — review round 1

Target `7795f390014750b1a9917aa9d0e5dd0ff9ad0270`, diff
`origin/release/v0.21.0...7795f390`, PR #879 (draft). No earlier round. Probes
ran in a `--no-local` clone under `<scratchpad>/1791384154/round-1/`, which is
deleted.

## What this round found, in causal order

The mechanism is sound where it was built: `close`, `notes`, `seal` and
`chain-check` agree on what a note is and which run it belongs to, and the
landing change cannot hide an open 🔴 or 🟡. The problems sit at the edges of
the build.

1. The pull request is red today. The edit to `agents/smith.md` §*Phases*
   drifted a rider anchored on that section, and nothing on the branch
   re-stamped it (🔴 1).
2. The cutoff is this item's own id, but the siblings framed in the same
   batch carry later ids and run under the installed 0.20.0 `close`. One of
   them (#858, PR #875) already carries three ⬜ closed `fixed`, and the new
   arm fails all three once this lands (🟡 2).
3. A run stopped at a `second` whose notes were not closed there can never be
   closed afterwards. Nothing reads those notes again, and `notes` refuses
   them as outside the run (🟡 3).
4. The policy document that outranks the new owner still tells a reader to
   close a record-located finding in the fix table, which `close` now refuses
   (🟡 4).
5. Five of `notes`' refusal sentences are not pinned, and one case's
   docstring claims an assertion it does not make (🟡 5).
6. Three paperwork corrections: two ledger re-reads that should have been
   corrections, and two carrier sentences that disagree with the new rule
   (⬜ 6, ⬜ 7, ⬜ 8).

## 🔴 1 · The PR's test legs fail on a rider the smith edit drifted

`agents/smith.md:87` carries a rider stamped `Verified 2026-10-05 against
"## Phases"@1029389b`. The branch inserted the ⬜ paragraph at
`agents/smith.md:204`, inside that section, so the anchor's hash moved to
`0805cac3`.

- Executed in the clone: `bin/test tests/test_a_rider_reaches_its_file.py`
  gave 2 failed, 47 passed. `python3 .github/scripts/rider_check.py` exited 1
  with `19 ok · 1 drifted · 0 broken`.
- Read from CI: the ubuntu leg failed with exactly these two cases (2 failed,
  12766 passed). Windows group 1 failed with the same two cases. macOS was
  still pending when this report was written.

The rider guards the waiver example and is unrelated to the new paragraph, so
the fix is to read the rider and re-stamp it. The smith's hand-back listed
"the five text-hygiene modules", and the rider module was not one of them.
That is how the drift reached the pull request.

## 🟡 2 · The cutoff fails the 0.21.0 siblings, which ran under the old `close`

`NOTES_FROM = 1791384154` at `skills/code-review/scripts/chain_check.py:856`
follows the `STRICT_FROM` reasoning: *the first records held to it are the
ones written under it*. That premise does not hold for this release. The whole
batch was framed in one sitting with ids 1791384155 to 1791384162 (#866, #867,
#868, #869, #870, #860, #858, #864), every id after this one, and each runs its
rounds under the installed 0.20.0 `round-record close`. That `close` demands a
fix-table row for every open ⬜ and accepts `fixed`.

- Executed: `carried_notes` over #858's branch at `4e4eeff` (PR #875, into
  `release/v0.21.0`) returns 3 errors, at
  `seal/specs/1791384161-…/rounds/round-1.md` lines 33, 34 and 35. These are
  ⬜ 6, ⬜ 7 and ⬜ 8 closed `**fixed**`.
- Read: CI checks out the merge of head into base, and `chain_check.py` reads
  every work item the PR touches. So #875 goes red at its next run once #879
  is in `release/v0.21.0`, and the release PR into `main` goes red over every
  sibling that closed a ⬜ `fixed`.
- Read: this item's own rounds run under 0.20.0's `close` as well (the spawn
  prompt says so). Its id is the cutoff, so one ⬜ closed `fixed` in its own
  fix pass fails this PR.

The paste-ready fix moves the cutoff one past the batch. The other way out is
to rewrite each sibling's ⬜ rows to `answered`/`corrected at <sha>` before it
merges. That costs a pass per sibling and leaves the trap for the next batch,
so the constant is the cheaper fix. The value also appears in
`skills/code-review/orchestration.md:237`,
`skills/implement/orchestration.md:650`, the changelog fragment, ledger N2 and
the two test constants. All of them move with it.

**Until it lands, an orchestrator closing ⬜ rows in this run with the
installed `close` must not write `fixed`.**

## 🟡 3 · A stopped run's open note cannot be closed once the redesign starts

The owner file's reframe row (`skills/code-review/orchestration.md:293`) says
`notes` closes the stopped run's notes *before the framer is spawned*. Nothing
holds that. `overview.md` §*Not done* says the redesign stops reading them. It
does not say they then become unclosable.

Executed. The run stopped at round 3 (`second`) with round 1's ⬜ 1 open and
`notes` skipped, and a redesign record round 4 followed.

| What | Result |
|---|---|
| `run_of_last` | `[4]` |
| `open_notes` over that run, which `seal` and `carried_line` use | `[]` |
| `carried_notes` with strict on | `([], [])` |
| `notes` with a row for `round-1 \| 1` | exit 2, *names round 1, outside the run that ends at round-4.md* |

The note stays `open` in round-1.md for good. Seal passes, chain-check passes,
and no command can close it. The overview names the cheap closure itself, a
refusal in `new`. The paste-ready fix puts it beside the existing
`reframed_after` refusal, where the `second` is already known and `notes` can
still run.

## 🟡 4 · The policy document still sends a record-located finding to the fix table

`docs/review-chain-spec.md:246` reads *In the fix table such a row closes
`answered` with `corrected at <sha>` as its grounds*. "Such a row" is the
record-located finding that `agents/warden.md` tells the reviewer to grade ⬜,
and `close` now refuses a fix-table row for it. The docs outrank the skills,
so a reader who follows the higher document is refused by the tool.

`overview.md` §*Not done* says the document "does not contradict the new
rule". That is true of the *corrected in passing* clause and false of this
sentence. The 1,000-line ceiling does not block the fix: the replacement below
is three lines for three. The overview paragraph needs the matching
correction.

## 🟡 5 · Five `notes` refusals are unpinned, and one docstring claims a case it does not hold

§14 asks that a sentence a person reads is pinned in the commit that writes
it. The following refusals in `notes` are pinned by nothing in
`tests/test_a_note_closes_once_at_the_runs_end.py`:

- a round outside the run (`round_record.py:4920`)
- an id no record of the run holds
- a `Round` cell that names no round
- an `--at` that does not resolve
- a row for a note already closed

`test_a_row_for_a_finding_that_is_not_a_note_is_refused` says in its docstring
"and so is a row for a note already closed", but it asserts only the 🔴/🟡
case.

Executed in the probe: all five strings in the paste-ready case match what
`notes` prints, each exits 2, and no record changed. The case as written
below has not been run as a case. Showing it red (§15) means deleting each
sentence, which is the fix pass's to do.

## ⬜ 6 · Two ledger re-reads say "the claim holds" where the claim moved

`Re-read · S13` and `Re-read · S10` in
`seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:17-18`
re-read rows of 0.10.0.

- S13 states that *`close` ticks the box the moment a fix table applies*.
  `close` now leaves `Pass` unticked over a carried note.
- S13 and S10 both state that a capped run whose findings closed `deferred`
  seals. It no longer does while a note of the run is open.

These were owed `Corrected ·` rows, as S6 got. All 73 re-read rows carry the
same evidence sentence, so the sample suggests the bulk `--reverify --into`
was not read row by row against what this branch changed. I sampled the
others citing `close`, `seal`, `fix_table`, `reach_forward` and `build`:
0.8.1 R2, 0.11.4 *No verdict word…*, 0.11.5 *close --round N reaches
forward*, 0.17.0 R1. Each still holds.

## ⬜ 7 · `agents/warden.md` asks for an answer to every earlier finding and, 190 lines up, says not to re-report a note

`agents/warden.md:348` says *Every finding from an earlier round needs an
answer this round: fixed, still open, or no longer applicable*. The new
sentence at `agents/warden.md:161` says a carried ⬜ is *carried, not
re-reported*. A reviewer can follow only one of them for a note.

## ⬜ 8 · The owner file says "corrected in passing or not at all" one sentence before its new rule

`skills/code-review/orchestration.md:196` keeps *corrected in passing or not
at all* for record-located prose. The sentence added after it then says such a
finding closes once at the run's end. Read together, "in passing" no longer
names a moment the record can show, because a round's fix table refuses the
row.

## What was asked, and what this round answered

- **The `| Round | # |` key.** Only `fix_table(…, notes=True)` reads the notes
  table. `seal`, `carried_notes`, `close` and `notes` all read a note through
  `note_rows` on the record. They also cut the run alike: `runs_of` and
  `run_of_last` agree when the last record is a `second` and when it is the
  redesign's first (read). The `into=` reach writes every later record in
  memory before anything is written (read).
- **The landing.** `build` and `close` hand `landing_values` every word but
  an open note's, and `Pass` is still derived from every word. An open 🔴 or
  🟡 keeps the record at `nobody`, and an open note keeps `Pass` unticked
  (read). Neither failure the prompt names can happen.
- **The run's end, shared with `seal`.**
  - capped: closes as designed (read).
  - `second`: closes if `notes` runs before the redesign, and is lost if it
    does not (🟡 3, executed).
  - no records: `notes` refuses, `seal` takes its `broad-gate.md` path, and
    `carried_line` is silent (read).
- **`close` refusing a ⬜ row.** A person who wants a ⬜ filed mid-run has the
  reviewer's own `deferred #N` in the report. `notes` files it at the end with
  `deferred <home>`. Nothing is lost by the refusal (read). Over the tree's
  seven work items, `carried_notes` gives 0 errors and 24 notices (executed),
  which matches the smith's count. The siblings are the exception (🟡 2).
- **The 73 re-reads.** ⬜ 6.
- **The carriers.** SKILL, smith, template and implement say one rule. The
  owner's headline and each link are pinned by rule 17. Two sentences
  disagree (⬜ 7, ⬜ 8), and the higher document disagrees (🟡 4).

## Carried, not re-established

- The orchestrator's 326-passed run over five modules, and its ruff and
  `evidence-check --strict` results (read, from the spawn prompt).
- The smith's "30 mutations red" and Q2's 23-of-35 (read, from the hand-back
  and `questions.md`).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The ⬜ paragraph inserted into §*Phases* drifted the rider stamped on that section; two cases of the rider module fail and the PR's test legs are red | `agents/smith.md:87` | open | executed: rider module 2 failed, 47 passed; `rider_check.py` exit 1, 1 drifted. Read: CI ubuntu and Windows group 1 fail on the same two cases |
| 🟡 2 | `NOTES_FROM` is this item's id, but the batch's siblings (1791384155 to 1791384162) run under 0.20.0's `close`, which demands and admits ⬜ `fixed`; #858's records already fail arm A three times | `skills/code-review/scripts/chain_check.py:856` | open | executed: `carried_notes` over #858's branch at `4e4eeff` returns 3 errors at round-1.md:33-35. Read: CI checks the merge ref, and the release PR touches every sibling |
| 🟡 3 | A stopped run whose notes were not closed at the `second` leaves them open for good: `seal`, `carried_notes` and `carried_line` stop reading them, and `notes` refuses them as outside the run | `skills/code-review/scripts/round_record.py:4855` | open | executed: `run_of_last` gives `[4]`, `open_notes` gives `[]`, `carried_notes` gives `([], [])`, `notes` exits 2 *outside the run*; round-1's ⬜ 1 still reads `open` |
| 🟡 4 | The policy document says a record-located finding closes in the fix table, which `close` now refuses; the overview says the document does not contradict the rule | `docs/review-chain-spec.md:246` | open | read: the sentence against `close`'s ⬜ refusal and `agents/warden.md`'s instruction to grade such a finding ⬜ |
| 🟡 5 | Five of `notes`' refusal sentences are unpinned, and a case's docstring claims the already-closed refusal it never asserts | `tests/test_a_note_closes_once_at_the_runs_end.py:450` | open | executed: the five strings match `notes`' output, exit 2, records unchanged; read: no case asserts them |
| ⬜ 6 | `Re-read · S13` and `Re-read · S10` say the claim holds where `close` no longer ticks `Pass` over a carried note and a capped run with an open note no longer seals; `Corrected ·` rows were owed | `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:17` | open | read: 0.10.0 S10 and S13 against `close` and `seal` at the target |
| ⬜ 7 | `agents/warden.md` asks for an answer to every earlier finding and also says a carried ⬜ is not re-reported | `agents/warden.md:348` | open | read: lines 161 and 348 |
| ⬜ 8 | The owner file keeps *corrected in passing or not at all* one sentence before the rule that a ⬜ closes once at the run's end | `skills/code-review/orchestration.md:196` | open | read |
| 🟢 | The landing leaves only open notes out: an open 🔴 or 🟡 still holds `nobody`, and `Pass` is derived from every word | `skills/code-review/scripts/round_record.py:2595` | confirmed | read: `build` and `close` filter by `carried_ids`, which takes only `note_rows`' open notes |
| 🟢 | No shipped run turns red under the two arms | `skills/code-review/scripts/chain_check.py:4610` | confirmed | executed: 7 items, 0 errors, 24 notices |
| 🟢 | `runs_of` and `run_of_last` cut the run alike, and every reader of a note goes through `note_rows` | `skills/code-review/scripts/chain_check.py:3867` | confirmed | read |
| ❓ | The merge with #860 and #866, which edit `close` and `chain_check.py` beside these lines | `skills/code-review/scripts/round_record.py:4401` | ❓ out of verified scope | neither sibling's diff was reviewed here; the orchestrator answers it when it integrates them |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_rider_reaches_its_file.py -n 0` in the clone at `7795f390` | 2 failed (`test_every_rider_stamp_resolves_and_reproduces_its_hash`, `test_the_check_asks_git_for_nothing`), 47 passed |
| `python3 .github/scripts/rider_check.py` in the clone | exit 1; `DRIFTED agents/smith.md:87`; 19 ok, 1 drifted, 0 broken |
| probe P1: `carried_notes(strict=True)` over every work item with records in the clone | 7 items, 0 errors, 24 notices |
| probe P2: `carried_notes(strict=True)` over #858's branch at `4e4eeff`, cloned `--no-local` | 3 errors: ⬜ 6, ⬜ 7 and ⬜ 8 at round-1.md:33-35 *closes on `fixed`* |
| probe P3: a run stopped at round 3 with round 1's ⬜ 1 open, `notes` skipped, round 4 written by hand | `run_of_last` gives `[4]`; `open_notes` gives `[]`; `carried_notes` gives `([], [])`; `notes` exits 2 *outside the run that ends at round-4.md* |
| probe P4: `notes` given a round outside the run, an unknown id, a bad `Round` cell, an unresolvable `--at`, and a closed note | each exits 2 with the sentence the paste-ready case pins; records unchanged |
| `gh pr checks 879`, read and not run by this round | ubuntu: fail (2 rider cases, 12766 passed). Windows group 1: fail (same 2). Windows groups 2-4, lint, ledger, release, arm-check-grammar: pass. macOS: pending |
| the full suite, repository-wide lint and typecheck (the sealer's broad gate) | not yet — no run has happened at any SHA of this branch; the sealer answers it after the rounds settle |

## Paste-ready fixes

### 🔴 1

Read the rider at `agents/smith.md:87` first. Its instruction concerns the
waiver example, which the new paragraph does not touch. Then re-stamp it.

```
python3 .github/scripts/rider_check.py --reverify --only agents/smith.md
bin/test tests/test_a_rider_reaches_its_file.py
```

### 🟡 2

`skills/code-review/scripts/chain_check.py`, replacing the comment and the
constant at 852-856:

```python
# Where a note closed on a fix word becomes an error, as the unix second in a
# work item's directory name. NOT this item's own id, which is what the other
# cutoffs use: 0.21.0's items were framed in one sitting, 1791384154 through
# 1791384162, and every one after this one runs its rounds under the installed
# 0.20.0 `close`, which demands a fix-table row for a ⬜ and admits `fixed` --
# #858's round 1 closed three that way before this rule landed. One past the
# batch, so the first records held to it are written under it.
# Measured 2026-10-07: 35 ⬜ rows of 14 committed records closed `fixed`
# before it, and they print.
NOTES_FROM = 1791384163
```

`tests/test_a_note_closes_once_at_the_runs_end.py:47-48`:

```python
AT_THE_CUTOFF = "seal/specs/1791384163-an-item-under-the-rule"
BEFORE_THE_CUTOFF = "seal/specs/1791384162-an-item-before-the-rule"
```

The same value in prose moves in the same commit:
`skills/code-review/orchestration.md:237`,
`skills/implement/orchestration.md:650`, `changelog.md` and ledger N2.

### 🟡 3

`skills/code-review/scripts/round_record.py`, in `build`, directly after the
`reframed_after` refusal (after line 2619). This is unexecuted. It needs a
case seen red: a `second` with an open note, then `new` for the next round.

```python
    # #837. The redesign's first record is where the stopped run's notes stop
    # being read: `seal`, `notes` and `chain_check.carried_notes` read the run
    # the LAST record belongs to. Refused here, while `notes` can still close
    # them, rather than left open on a run nothing reads again.
    if stopped is not None and previous_pair == stopped:
        left = open_notes(reader, run_of_last(reader, earlier))
        if left:
            raise Refused(
                f"round-{stopped[0]}.md ended its run at a "
                f"`{chain.FOF_SECOND}` with {named_notes(left)} still open. A "
                "note closes once, at the run's end, and the "
                f"`{chain.FOF_SECOND}` is that end: run `{NOTES_COMMAND}` "
                "before the redesign's first record, which would leave them on "
                "a run nothing reads again. "
                f"{chain.NOTES_OWNER}; nothing was written"
            )
```

`overview.md` §*Not done*, first paragraph: replace it with one sentence saying
`new` refuses the redesign's first record while the stopped run carries an
open note.

### 🟡 4

`docs/review-chain-spec.md:246-248`, three lines for three:

```
At the run's end, in the notes table, such a row closes `answered` with
`corrected at <sha>` as its grounds, never `fixed`: `fixed` is a fix word, and
a fix word commissions the reader a correction does not owe.
```

`overview.md` §*Not done*, second paragraph: replace *It does not contradict
the new rule* with a sentence naming the line 246 rewording.

### 🟡 5

`tests/test_a_note_closes_once_at_the_runs_end.py`, after
`test_a_row_for_a_finding_that_is_not_a_note_is_refused`. Also drop *and so is
a row for a note already closed* from that case's docstring.

```python
def test_notes_names_each_row_it_cannot_apply_and_writes_nothing(repo):
    """The refusals `notes` raises before the write, each pinned (§14): a
    round outside the run, an id no record holds, a `Round` cell that names
    no round, an `--at` that does not resolve, and a row for a note the
    record already closed. Seen red by deleting each sentence in turn."""
    at = two_rounds_with_a_note_each(repo)
    before = record(repo, 1), record(repo, 2)
    for row, said in (
        (
            "| round-3 | 1 | answered | it stands |\n",
            "names round 3, outside the run that ends at round-2.md",
        ),
        (
            "| round-1 | 9 | answered | it stands |\n",
            "names round-1's 9, which no verdict table of the run holds",
        ),
        (
            "| round-x | 1 | answered | it stands |\n",
            "Write `round-K`, the record the note stands in",
        ),
    ):
        code, out = run_notes(repo, notes_table(*BOTH_ROWS, row), at=at)
        assert code == 2 and said in out, out
        assert (record(repo, 1), record(repo, 2)) == before
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at="deadbeefdeadbeef")
    assert code == 2 and "--at deadbeefdeadbeef does not resolve" in out, out
    assert (record(repo, 1), record(repo, 2)) == before
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at=at)
    assert code == 0, out
    commit(repo, "the notes closed")
    closed = record(repo, 1)
    code, out = run_notes(
        repo, notes_table("| round-1 | 1 | answered | again |\n"), at=at
    )
    assert code == 2, out
    assert f"round-1's {NOTE} 1, already closed in its verdict table" in out, out
    assert record(repo, 1) == closed
```

## Regression tests to plant

- `tests/test_a_note_closes_once_at_the_runs_end.py`: the 🟡 5 case above,
  and for 🟡 3 a case where `new` for the round after a `second` is refused
  while the stopped run carries an open note.
- `tests/test_a_note_closes_once_at_the_runs_end.py`: the cutoff pair moves
  with `NOTES_FROM` (🟡 2).

## Facts for the evidence ledger

- `Corrected · S13` and `Corrected · S10` (0.10.0), replacing the two re-read
  rows (⬜ 6).
- N2 restated at the new cutoff value (🟡 2), and N3 and N5 extended for the
  `new` refusal if 🟡 3 lands.

Needs a fix: yes — 🔴 1 (the rider re-stamp), 🟡 2 (the cutoff), 🟡 3 (a
stopped run's notes become unclosable), 🟡 4 (the policy sentence), 🟡 5 (the
unpinned refusals)
Loses a record or crashes: no

## Proof block

- Opened: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `routing.md`,
  `handoff.md`, `changelog.md`; the diff of `chain_check.py`,
  `round_record.py`, `agents/smith.md`, `agents/warden.md`,
  `skills/code-review/SKILL.md`, `skills/code-review/orchestration.md`,
  `skills/implement/SKILL.md`, `skills/implement/orchestration.md`,
  `templates/sdd-round.md` and the three pin modules; in `chain_check.py`,
  the vocabulary at 395-530, `verdict_table`, `verdict_of`, `checked_by`'s
  `no fixes to check` arm, `runs_of`, `check_round` and `main`'s per-item
  loop; in `round_record.py`, `landing_values`, `earlier_records`,
  `current_run`, `finding_number`, `verdict_rows`, `reach_forward`, `build`
  around 2570-2635, and `close`'s write pass and landing;
  `tests/test_a_note_closes_once_at_the_runs_end.py` in full;
  `docs/review-chain-spec.md:236-252`; `agents/smith.md:80-135`; the
  fragment's N rows and its re-read rows citing `close`, `seal`, `fix_table`,
  `reach_forward` and `build`; 0.10.0 S10 and S13, 0.11.4:64 and 0.8.1 R1-R2
  in `seal/releases/`; #858's round-1.md and round-2.md (read only).
- Executed: the rider module and `rider_check.py` in the clone; probes P1-P4
  in one file, run once and deleted with both clones and the venv `bin/test`
  built inside the clone.
- A slip: the probe's second half was appended through a `cat >>` heredoc
  after a `cd`, not through the `Edit` tool (contract §9). It touched only the
  probe file in the scratch clone.
- Not run: the full suite, lint and typecheck (the sealer's); the five modules
  the orchestrator ran (carried, read).
