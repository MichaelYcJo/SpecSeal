# Round 2 report — #520, folded statements pile into one spec

Target: the fix range `edcd2e33..ca380837` (one commit) and the record commit
`b527bd86`, at Target SHA `b527bd86ca45775afcb71edb5e0b015deb858972`, branch
`docs/520-folded-statements-pile-into-one-spec`, PR #527, base
`release/v0.14.0`. This is a verifying round, so the branch was not re-read.
Probes ran in a `git clone --no-local` of the worktree in the session
scratchpad, and the clone is deleted.

## What this round was asked

A verifying round over round 1's fixes, not the branch. For findings 1 and 2,
which `rounds/round-1.md` records as `fixed` at `ca380837`, the question is
whether each is actually closed. Round 1's own probes from
`round-1-report.md` were re-run against the fix rather than rebuilt. The
units in round 1's `New units` row were reviewed by nobody, so they were
judged as code: `FROZEN_IDS_DIGEST`, `marker_digest`, `BOLD_OPENING` and the
five new cases. The same commit carried round 1's three ⬜ corrections (the
evidence-ledger exemption sentence, the settle §2 wording together with the
bare `**` bold, and headings indented up to three spaces), and they were
checked too. The smith dropped the reviewer's `full == base` clause from the
paste-ready fix for finding 2 as unsupported by any case, on the grounds that
the file check already refuses the root, and that choice was judged. What the
fix commit's message and the ledger rows say was read as the smith's account
and checked against the code and the probes.

Carried, not re-established: the digest `8f8c4d85f213` and the count 29 of
`docs/review-chain-spec.md` were re-computed here rather than carried, and
they match. The round 1 deferral to #526 was not re-found and is not
repeated.

## Findings 1 and 2 are closed (executed)

**Finding 1.** Round 1's probe was re-run through the new unit. A listed file
frozen at 2 that carries one old marker and one bound marker
`1790154762-a-later-fold` is now named: "carries 2 fold markers, but not the
ones frozen". A swap to a duplicate of an existing id is named too, because
the digest reads the sorted list with its duplicates. The `continue` the
smith added after the count branch makes the digest branch run only at equal
count, which is the `found == frozen` guard round 1's fix wrote out. The real
tree gives digest `8f8c4d85f213` over 29 markers, the value
`FROZEN_IDS_DIGEST` holds.

**Finding 2.** All four targets are now named. `.` and `tests` get "is not a
file in the repository", and `../outside.txt` and `tests/../..` get "is not a
path inside the repository". `./tests/test_x.py`, `tests//test_x.py` and
`/tests/test_x.py` still resolve, and all three name a file inside the root.

**The dropped `full == base` clause.** The smith was right. `.` normalises to
the base itself, and the base is always a directory, so the `isfile` check
refuses it with "is not a file in the repository". The probe confirmed this.
No input reaches the containment branch equal to the base and then passes.
The smith also added `os.path.abspath` around the root, which round 1's fix
lacked. Without it `os.path.commonpath` raises on a relative root mixed with
an absolute one. A relative root of `b0` was probed and resolves correctly.

**The new cases were seen red (executed).** This round did not take the
smith's red-first claims on trust. Each new case's input was run against the
pre-fix unit taken from `edcd2e33`:

- The old `target_problem` returned `[]` for `.`, `tests`, `../outside.txt`
  and `tests/../..`, so the new target case is red on it.
- With containment removed from the new unit, `../outside.txt` passes again.
  This matches the smith's mutation claim in ledger row S1.
- The old `startswith("**")` opening accepted a bare `**`.
- The old pairing `HEADING` accepted `   ## A` in one edition only.

The swap case is red on the old unit trivially, because the old
`ceiling_problems` takes no digest argument. It was not run with the digest
comparison mutated out here, so that part stays the smith's claim.

## Finding 3 🟡: a marker removed on purpose is reported as a swap (executed)

`tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems`, the
digest branch. Consider a fold that removes a statement from
`docs/review-chain-spec.md` and adds nothing, which settle does whenever a
statement stopped being true. The count branch fires first and says "a
removed marker lowers the frozen count". The maintainer lowers the count in
`OVER_CEILING`. The digest branch then fires with a message that is false for
this case. The probe froze at 1 with the digest of the old two ids, and the
check returned:

> docs/big.md carries 1 fold markers, but not the ones frozen until #1
> splits it. A fold that adds a statement here and removes another keeps the
> count; the new rule goes to the document for its own sub-subject

Nothing was added and the count did not stay the same. The one thing the
maintainer has to do is recompute `FROZEN_IDS_DIGEST` with `marker_digest`.
That instruction lives only in the comment above the constant. It is not in
either message, the evidence ledger's paragraph or settle §2. So the check is
right to refuse, and it then tells the person something untrue about what
happened and nothing about the fix. §14 of the agent contract applies,
because this is a message a person reads and acts on.

The message came from round 1's own paste-ready fix, so the defect entered
through the reviewer's text and not the smith's. The class is every message
this function prints on a legitimate removal (§12). There are two, the count
branch and the digest branch, and the fix below covers both. The planted case
fails on the current message, which does not contain `marker_digest`, so the
fix is seen red by construction.

## New units judged as code

- `marker_digest` reads markers with the fold's own `live_lines` and
  `FOLD_MARKER`, the same reader as `markers`, so the count and the digest
  cannot disagree about which lines are live. It is correct.
- `FROZEN_IDS_DIGEST` holds the value on disk. The case that checks it
  requires the same keys as `OVER_CEILING`, so an entry cannot be listed
  without a digest.
- **`BOLD_OPENING` refuses a bold-italic opening (⬜, executed).** The
  pattern `^\*\*[^*\s]` refuses `**`, `** Rule.**` and `****`, all
  correctly. It also refuses `***Rule.***`, which CommonMark renders as bold
  and italic, and the message then says "does not open with a bold rule
  sentence", which is false. No statement in the tree opens that way, and a
  writer can drop the italic. `` **`x` is the rule.** `` still passes.
- **The heading patterns still skip two CommonMark headings (⬜, executed).**
  Round 1's correction 5 closed the indentation member of this class. Two
  members are left. `##` followed by a tab, and a bare `##` with nothing
  after it, are both ATX headings that the pairing check does not read, so
  one edition carrying either passes. `docs/*.md` holds no line of either
  shape today. Both modules share the same pattern, so the same gap is in the
  shape reader's statement end. Accepting `[ \t]` or end of line after the
  hashes closes both.
- **`target_problem` follows a symlink out of the root (⬜, executed).** A
  target `docs/link.txt` that is a symlink to a file outside the root
  resolves, because `os.path.normpath` does not resolve links. Row S1 claims
  "a file inside the repository". Using `os.path.realpath` on both `base` and
  `full` closes it. Nobody writes a symlink as an enforcer today, so this is
  ⬜.
- The five new cases pass (37 in the three modules). Each one's input was
  seen red on the pre-fix unit, as above.

## Round 1's three corrections (read, with the neighbouring modules executed)

- **The evidence-ledger sentence** now names the exempt set by marker id: the
  101 folded before the cutoff, and the statements of earlier work items
  released with it or still waiting. This is closed.
  `test_the_evidence_ledger_states_the_values_these_constants_hold` is green,
  so the value pin still matches.
- **Settle §2** now says "carries exactly one line … and that line is written
  last". This matches the spec's "carries" and what `shape_problems` checks,
  and it is closed. The settle phrase pins in
  `test_settle_reads_before_it_removes` are green.
- **Bare `**`** is refused, and **headings indented up to three spaces** are
  read by both modules, while four spaces are not. Both are closed, with the
  remaining heading shapes noted above.

## A paperwork correction in the ledger fragment (read)

`seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`, rows E1 and
S1. E1 now claims that a heading indented one to three spaces is read, and S1
claims that a bare `**` is no longer bold. Neither row anchors the unit that
carries the claim: the pairing module's `HEADING` for E1, and the shape
module's `BOLD_OPENING` and `HEADING` for S1. `evidence-check` cannot see a
later edit to those constants. Adding the three anchors to the rows' `Code
grounds` fixes it. This is a correction to the run's paperwork and stays out
of `Needs a fix`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1 finding 1: a marker swap at equal count into the listed document is now refused | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | verified | Executed: round 1's probe (old id plus a bound id, frozen at 2) is named "but not the ones frozen"; a duplicate-id swap is named too; the real-tree digest is `8f8c4d85f213` over 29, matching the constant |
| 🟢 | Round 1 finding 2: `.`, a directory, `../outside.txt` and `tests/../..` are now refused as targets | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | verified | Executed: all four are named; the pre-fix unit passed all four; with containment removed, `../outside.txt` passes again |
| 🟢 | The smith dropped round 1's `full == base` clause | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | verified | Executed: `.` normalises to the base, which is a directory, so `isfile` refuses it; no input reaches that clause and passes. The added `abspath` fixes a relative-root `commonpath` error round 1's fix had |
| 3 | 🟡 After a marker is removed on purpose and the count is lowered, the digest branch says a fold "adds a statement here and removes another" and "keeps the count", both false, and neither message says to recompute `FROZEN_IDS_DIGEST` | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | open | Executed: frozen at 1 with the old two-id digest returned the swap message. The recompute instruction is only in a code comment. The text came from round 1's paste-ready fix |
| ⬜ | `BOLD_OPENING` refuses `***Rule.***`, which CommonMark renders bold, and says it is not bold | `tests/test_a_folded_statement_names_what_enforces_it.py#BOLD_OPENING` | correction | Executed. No instance in the tree; a writer can drop the italic |
| ⬜ | Both `HEADING` patterns skip `##` followed by a tab and a bare `##`, the rest of round 1's correction-5 class | `tests/test_both_editions_carry_the_same_folds.py#HEADING`; `tests/test_a_folded_statement_names_what_enforces_it.py#HEADING` | correction | Executed: one edition carrying either passes. No line of either shape under `docs/` |
| ⬜ | `target_problem` resolves a symlink inside the root that points at a file outside it | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | correction | Executed. `normpath` does not resolve links; `realpath` on both sides closes it. No such target is written anywhere |
| ⬜ | Ledger rows E1 and S1 claim the new heading and bold behaviour without anchoring `HEADING` or `BOLD_OPENING` | `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`, rows E1 and S1 | correction | Read. A paperwork correction: add the three constants to `Code grounds` |
| 🟢 | Round 1's three corrections (evidence-ledger exemption sentence, settle §2 "carries … written last" with bare `**` refused, headings indented up to three spaces) | `docs/the-evidence-ledger.md`; `skills/settle/SKILL.md`; the two `HEADING` patterns | verified | Read the wording; executed bare `**`, `   ## A`, ` ## A` and `    ## code` through the new units; the neighbouring pin modules are green |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three new modules at `b527bd86`, in the clone | 37 passed |
| `bin/test` over `test_settle_reads_before_it_removes`, `test_docs_line_wrap`, `test_the_rules_have_one_owner` at `b527bd86` | 154 passed |
| `bin/evidence-check --strict .` at `b527bd86` | exit 0 |
| `bin/unverified-check` at `b527bd86` | exit 0 |
| `uvx ruff check` and `uvx ruff format --check` on the three touched modules only | all checks passed; 3 files already formatted |
| One `test_tmp_` probe re-running round 1's planted inputs through the new units | swap named; duplicate swap named; `.`, `tests`, `../outside.txt`, `tests/../..` named; bare `**` named; `   ## A` named; real digest `8f8c4d85f213` over 29 |
| The same probe, new inputs | removal with count lowered and stale digest: swap message (finding 3); symlink escape `[]`; `***Rule.***` refused; `##` plus tab and bare `##` `[]`; indented heading ends a statement in the shape reader |
| The same probe, new case inputs against the pre-fix units from `edcd2e33` | old `target_problem`: all four `[]`; old bold opening: bare `**` `[]`; old pairing heading: `   ## A` `[]`; containment removed from the new unit: `../outside.txt` `[]`. Probe file, the extracted pre-fix modules and the clone are deleted |
| The swap case with the digest comparison mutated out | not run here: the smith's claim in ledger row P1, read and not re-executed |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet run, and not this round's; the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

Finding 3. Both messages say what to do on a removal, and a planted case pins
it. The existing swap case keeps passing, because the substring it asserts,
"but not the ones frozen", is kept.

```python
# tests/test_a_document_has_room_for_the_next_fold.py — ceiling_problems
        found = markers(text)
        if found != frozen:
            problems.append(
                f"{rel} carries {found} fold markers and is frozen at {frozen} "
                f"until {home} splits it. A new fold goes to the document for "
                "the rule's own sub-subject; a removed marker lowers the frozen "
                "count, so the room it made is not refilled, and recomputes "
                "FROZEN_IDS_DIGEST with marker_digest() in the same commit"
            )
            continue
        want = (digests or {}).get(rel)
        if want is not None and marker_digest(text) != want:
            problems.append(
                f"{rel} carries {frozen} fold markers, but not the ones frozen "
                f"until {home} splits it: their ids no longer match "
                "FROZEN_IDS_DIGEST. If a fold added a statement here and "
                "removed another, the new rule goes to the document for its own "
                "sub-subject. If a marker was removed on purpose, set the digest "
                "to marker_digest() of the file in the commit that lowered the "
                "count"
            )


# a planted case, red on the current message (it names no marker_digest)
def test_a_marker_removed_on_purpose_is_told_to_recompute_the_digest(tmp_path):
    frozen = body(12, 2)
    root = tree(tmp_path, {"big.md": body(12, 1)})
    found = ceiling_problems(
        root, 10, {"docs/big.md": (1, "#1")}, {"docs/big.md": marker_digest(frozen)}
    )
    assert len(found) == 1 and "marker_digest" in found[0], found
```

Needs a fix: yes — finding 3: after a marker is removed on purpose, the digest
branch reports a swap that did not happen and neither message says to
recompute `FROZEN_IDS_DIGEST`

Loses a record or crashes: no

## Regression tests to plant

- `tests/test_a_document_has_room_for_the_next_fold.py`: a removal with the
  count lowered and the digest stale, where the message names `marker_digest`
  (the fenced case under finding 3).

## Facts for the evidence ledger

- P1: once finding 3 is fixed, `Verified behavior` can say that a removal
  with a stale digest is told to recompute it.
- E1 and S1: anchor `HEADING` (both modules) and `BOLD_OPENING` (see the
  paperwork correction).

## Proof block

Opened: `rounds/round-1.md` and `rounds/round-1-report.md` in full; the full
diff of `ca380837` and of `b527bd86`; in
`tests/test_a_document_has_room_for_the_next_fold.py` the constants,
`markers`, `marker_digest`, `ceiling_problems`, `tree`, `body` and `OVER`; in
`tests/test_a_folded_statement_names_what_enforces_it.py` `statements`,
`bound`, `target_problem`, `shape_problems` and `planted`; the docstring of
`tests/test_both_editions_carry_the_same_folds.py`; the fold paragraph of
`docs/the-evidence-ledger.md` around "frozen at 29"; the placement rule of
`skills/settle/SKILL.md` §2; `FOLD_MARKER` in
`skills/verify/scripts/unverified_check.py`; `ruff.toml`; `bin/test`; and the
three modules as they stood at `edcd2e33`.
