# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 58ea18bb |
| Ran by | unknown — the spawn prompt did not hand the value over, and the segment does not source it from its own idea of what it is |

## What this phase was asked

The documents and the record: `spec.md` Scope 5's eight files, a case pinning
the rule-3 sentence and the `new?` reason, the `changelog.md` fragment, and
ledger fragment rows for the new units with the re-read of
`seal/releases/0.10.0.md` S5 through `--reverify --into`, since the ledger is
frozen (A9). Rule 3 states both orders and recommends neither (Q2, the
owner's answer). `templates/config.md` already contradicted itself: its
example row runs lint first and rule 3 said runner first. Before the
hand-back, `bin/survivor-check` over the build range and `bin/evidence-check`
unscoped for drift.

## What this phase found

- **Two more files pinned the old rule 3**, and `spec.md` Scope 5 did not
  list them: `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`
  held the title `The suite runner comes first` and the reason `before the
  row's first \`&&\``. Both pins now hold the new title and reason, and one
  more asserts that rule 3 picks no order. With rule 3 rewritten,
  `templates/config.md`'s lint-first example row and the rule agree.
- **The eight files**: `templates/config.md` rule 3; `broad_gate.py`'s module
  docstring (the `gate` comment was rewritten in phase 3); `skills/verify/SKILL.md`,
  which gained a `New?` bullet under the two words; `agents/sealer.md` in two
  places; `agents/smith.md`; `README.md` and `README.ko.md`, each in the
  sealer row and the chain diagram; and the fixture comment in
  `tests/test_the_seal_is_taken_once_by_the_sealer.py#config`.
- **The pin, executed:** `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`
  holds both reasons whole and one phrase in each reader. Twelve pinned
  sentences were each deleted in turn with `mutation-check`, and each
  deletion went red.
- **`agents/smith.md`'s RIDER drifted** with the edit to `## Phases`, and
  `tests/test_a_rider_reaches_its_file.py` went red. The rider is about the
  waiver example. This phase added two sentences without the words of a
  commit, so the example and the rider's measurement both stand. It was
  read, then re-stamped with `rider_check.py --reverify --only agents/smith.md`.
  The stamp is a content hash (`46d4ea35`), so a squash leaves it standing.
- **The ledger, executed:** `evidence-check --reverify --into` wrote 44
  `Re-read ·` rows, and each row's Notes now say what changed under its
  coordinate. Every claim was read against this work's edits before the
  write, and only S5 had become false. It is corrected by a `Corrected ·`
  row carrying every coordinate the claim rests on now. `evidence-check
  --strict .` reads `4269 ok · 0 drifted · 0 broken` across the whole tree.
- **One of the 44 drifted before this work.** `seal/releases/0.15.1.md` L1
  cites a case that #752 (`f19e2762`) edited without a re-read, so the
  release branch at `e141980a` already reports it DRIFTED, and the sealer's
  strict ledger arm would refuse every branch for it. It was read here: the
  case now finds a folded section's heading as a whole line and still reads
  the release files. The claim holds, and the row's Notes name #752.
- **The records arm refused three names in this work item's own records:**
  `first_command` in `plan.md`, which this work removed; `PYTEST_ADDOPTS` in
  `plan.md`'s rejected alternative E; and pytest's
  `_report_keyboardinterrupt` in `phases/phase-3.md`. Each line now carries
  ` · NAME NOT IN TREE`.
- **`survivor-check --range 836fd7b2..HEAD` reported one place**, this
  work item's own `spec.md` quoting the fixture comment it asked to be
  corrected. It is exempted in `survivors.md` with that quote. With the
  exemption it exits 0.
- **The scratchpad is shared with sibling sessions**, and two message files
  written early in phase 1 under generic names were overwritten by
  another session after this session had committed with them. Every commit
  subject on this branch was checked and is this work item's. Message files
  are now named for the item.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| rule 3's title `The suite runner comes first` and its reason | `templates/config.md` §*Choosing a value — the criterion* rule 3, rewritten in place |
| `seal/releases/0.10.0.md` S5's sentence "What it re-runs is what stands before the row's first `&&`" | the `Corrected · S5` row in `seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md`; the released file is frozen and unedited |
