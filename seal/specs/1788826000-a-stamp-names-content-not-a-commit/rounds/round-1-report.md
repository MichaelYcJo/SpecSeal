# 1788826000-a-stamp-names-content-not-a-commit — review round 1 report

| Field | Value |
|---|---|
| Target SHA | 404dd4d5fec6388d40e8691e5bf9e068719ac6bf |
| Base | origin/release/v0.9.1 |
| Branch | fix/239-a-stamp-names-content-not-a-commit |
| Ticket | #239 |
| PR | none open at the time of this round |
| Broad gate | not yet — contract §2 reserves it for the orchestrator |
| Parity mark | not applicable; `seal/parity.md` is absent |

## What this round was asked

Round 1 against `404dd4d`, the whole branch diff, with eight named attack
surfaces: the exclusion rule's losses, the self-reference fixed point, the
two-riders-in-one-unit case, the `Target SHA` exemption, the twelve preserved
migration dates, the mutations behind "a test seen red", the CI message the
change made false, and a mid-run `git checkout` the build reported.

**Inherited coordinates.** No `round-*.md` exists for this work item, so
nothing was carried from an earlier round. What was carried instead is the
phase records' coordinates — `phases/phase-4.md`'s list of which riders were
proved and which refused, and `seal/ledger/1788826000-….md` rows S1 to S5 —
used to locate the code, never as verdicts. Every claim below was re-derived.

## What the round found, in the order one thing causes the next

The branch's machinery does what it says. Every mutation the build reported
was reproduced red, the fixed point holds, the twentieth rider fires when you
do what it asks, and the check makes no git call. What is wrong sits on
either side of that machinery: the dates it wrote into the tree, and two holes
the corpus does not currently stand in but the next rider will.

### 1 · Every stamp says it was read on 2026-09-08, and twelve of them were not

`phases/phase-4.md` calls it the phase's main result — *"Twelve migrated with
their original dates intact"* — and `seal/ledger/1788826000-….md` row S4
records the same. **Not one original date is in the tree.** All twenty stamps
at `4bf8dcb` and at HEAD read `2026-09-08`.

Executed, in a fresh `git clone --no-local` at `cbdd66e` (the last commit
before the corpus moved), `python3 .github/scripts/rider_check.py --migrate`
wrote these dates:

| Rider | Date `--migrate` writes | Date in the tree |
|---|---|---|
| `hooks/cmdline.py:1775` | 2026-08-31 | 2026-09-08 |
| `hooks/cmdline.py:1814` | 2026-08-31 | 2026-09-08 |
| `hooks/dispatch.py:80` | 2026-09-02 | 2026-09-08 |
| `hooks/optin.py:51` | 2026-08-31 | 2026-09-08 |
| `hooks/review-history-guard.py:153` | 2026-08-31 | 2026-09-08 |
| `hooks/review-skill-gate.py:122` | 2026-08-31 | 2026-09-08 |
| `hooks/worktree-guard.py:165` | 2026-08-31 | 2026-09-08 |
| `hooks/worktree-guard.py:222` | 2026-08-31 | 2026-09-08 |
| `hooks/worktree-guard.py:1484` | 2026-08-31 | 2026-09-08 |
| `skills/code-review/scripts/round_record.py:1858` | 2026-09-06 | 2026-09-08 |
| `skills/evidence-check/scripts/evidence_check.py:1790` | 2026-09-07 | 2026-09-08 |
| `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:618` | 2026-09-06 | 2026-09-08 |

The twelfth was verified separately, because a `--no-local` clone does not
carry the `4581fe1` object: hashing that region at `4581fe1` and at HEAD both
give `8e0a246a`, so `--migrate` in this repository keeps `2026-09-06`.

**Why it matters.** `rider_check.py:399-402` states the rule the whole design
rests on — *a date says when a person read the claim and a hash says what they
read, so writing one without the other leaves a stamp asserting a reading that
never happened*. `phases/phase-2.md` repeats it as the reason `--migrate` may
call git at all. Twelve stamps now assert a reading on 2026-09-08 that nobody
performed, and the branch's own records say the opposite happened. The one
number that was right is 12; what did not survive is the dates.

The cause is finding 2, and the fix is both halves: the code, then the twelve
stamps.

### 2 · And `--reverify` is what erased them — it rewrites a stamp whose content never moved

`.github/scripts/rider_check.py:421`:

```python
if digest == rider.new.group("hash") and today == rider.new.group("date"):
    continue
```

The `and` is the defect. A rider whose region hashes to exactly what the stamp
records — nobody edited it, nobody re-read it — is rewritten with today's
date because the date differs.

Executed, in the clone where `--migrate` had just preserved the dates:

```
$ python3 .github/scripts/rider_check.py --reverify --only hooks/worktree-guard.py
restamped hooks/worktree-guard.py:165 -> 8801e5d6
restamped hooks/worktree-guard.py:222 -> 7e3ba403
restamped hooks/worktree-guard.py:1484 -> 7415c477
3 restamped · 0 refused
-    # Verified 2026-08-31 at 9829412.
+    # Verified 2026-09-08 against _tokenize_with_separators@8801e5d6.
```

Three hashes identical to what `--migrate` computed, three dates moved. Nothing
was re-read.

**`--only` takes a file, not a rider,** and that is the second half. The
DRIFTED message at `rider_check.py:344` hands the reader
`--reverify --only <path>`. Three files carry three riders each
(`hooks/worktree-guard.py`, `skills/code-review/scripts/round_record.py`) or
two (`hooks/cmdline.py`), so answering one drifted rider re-dates its
neighbours — which is exactly how the twelve dates went.

### 3 · And a date-only re-stamp drifts the evidence ledger row for a unit nobody touched

`phases/phase-4.md` says the ledger cost is one-time: *"In steady state it adds
no new drift event: a rider is re-stamped when its unit changes, and that same
change has already drifted the row."* Finding 2 breaks that, because a
re-stamp no longer implies the unit changed.

Executed in a clone at `404dd4d`, changing one rider's stamp date from
`2026-09-08` to `2026-09-09` and nothing else:

```
rider check : 20 ok · 0 drifted · 0 broken   exit 0
evidence    : DRIFTED  hooks/dispatch.py#run_gate  content changed at 54-98 — re-verify
              total: 814 ok · 1 drifted        exit 1
```

The two checks now disagree in a standing way, and the one that goes red is
the one nobody edited a claim in. Fixing finding 2 closes this as well; it is
listed apart because the record states the opposite as a settled property.

### 4 · Two riders written back-to-back merge into one block, and the second one's stamp is never read

`comment_blocks` opens a block at a `RIDER:` comment head and runs it forward
through every following comment line (`rider_check.py:197-206`), then advances
past it (`i = end + 1`). A second rider inside that run is not a second block.
`Rider.__init__` (`rider_check.py:218-219`) then reads the **first** stamp in
the merged body and no other.

Executed on a fixture with a correct first stamp and a deliberately wrong
second one:

```
blocks:        [(2, 5)]
riders found:  ['hooks/m.py:2']
stamps read:   ['ea8b798d']
verdict:       1 ok · 0 drifted · 0 broken
```

The rider stamped `deadbeef` is never resolved, never compared, and never
reported as unstamped.

**Why it matters.** This is the class §12 makes this change's, not a new one.
`phases/phase-3.md` found the same merging inside its own fixture — *"the two
merged into ONE comment run, so there was only ever one block"* — and hardened
the fixture. The production reader was left as it was, so the shape that made
the case verify nothing also makes a real second rider unverifiable. It is the
same failure as the three riders `RIDER_ROOTS` never scanned: a rider held by
nothing, and silent about it.

The corpus does not stand in it today — all twenty riders are separated by
code — so nothing is red. The next person who plants a rider under an existing
one gets a stamp that can say anything.

### 5 · Three anchors are the sentence anchors the ledger abandoned, and a reword makes them BROKEN

`evidence_check.resolve_unit`'s own docstring says why a markdown locator is a
heading path: *"A sentence anchor breaks on any rewording — eleven rows here
pointed at one — while a heading is the document's own structure and survives
its prose being rewritten."* Three of the four hand-written anchors are
sentence anchors:

- `agents/smith.md:60` → `"`git commit` a bare word is a pathspec and git rejects it."`
- `skills/implement/SKILL.md:379` → `"Two things the sentences kept dropping. A declaration reaches the review arm"`
- `templates/evidence-check.yml:5` → `"# spec-to-code coordinates stop resolving; warns (exit 1) on ranges touched"`

Executed — one word changed in each anchored line:

```
BROKEN   skills/implement/SKILL.md:379: the anchor resolves to nothing in this file
BROKEN   templates/evidence-check.yml:5: the anchor resolves to nothing in this file
BROKEN   agents/smith.md:60: the anchor resolves to nothing in this file
exit 2
```

**Why it matters, and it is sharpest at `skills/implement/SKILL.md`.** That
rider's instruction is *"Name the arm in the sentence when this section is next
opened."* The sentence it means is the anchored one. Doing what the rider asks
turns it BROKEN, and BROKEN's verdict text (`spec.md`, the degradation table)
reads *the rider's subject is gone — re-anchor it or delete the rider*. The
check would tell the person who just answered the rider that its subject no
longer exists.

`CLAUDE.md` states the rule this violates: *an anchor degrades to DRIFTED,
never to BROKEN*. All three files have headings available.

### 6 · The `881fb0f` refusal says git cannot resolve a commit git resolves fine

`content_at` (`rider_check.py:359-371`) returns `None` for **any** non-zero
exit, and `migrate` (`rider_check.py:504-511`) prints one sentence for it:
*"git cannot resolve 881fb0f any more, which is the defect this migration
removes."*

Executed in this repository:

```
$ git cat-file -t 881fb0f
commit
$ git merge-base --is-ancestor 881fb0f HEAD && echo ancestor
ancestor
$ git show 881fb0f:./.github/scripts/fold_ledger.py
fatal: path '.github/scripts/fold_ledger.py' exists on disk, but not in '881fb0f'
$ git ls-tree -r --name-only 881fb0f | grep fold_ledger
(nothing)
```

The commit resolves, is an ancestor of HEAD, and is dated 2026-09-02. What is
missing is the file: `fold_ledger.py` did not exist anywhere in the tree at
that commit, so the rider was stamped with a commit that predates its own
subject.

**Why it matters.** `phases/phase-4.md` and ledger row S4 promote this refusal
to the migration's headline evidence — *"one (`881fb0f`) that git can no longer
resolve at all, which is the ticket's own defect caught in the act"*. It is a
different defect, and it is the one thing in the branch that claims to have
observed the squash orphaning a stamp in the act. The refusal message needs to
say which of the three causes it hit, and the two records need the correction.

### 7 · The old string survives in two record files, and the disclosure names one

`questions.md` C1 and `overview.md` both say the quoted stamp in
`seal/specs/1788184145-…/rounds/round-2.md` is *"the one place the old string
survives a `grep`"*. Executed:

```
seal/specs/1788184145-the-gate-stops-the-session-editing-its-tests/rounds/round-2.md:25
seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96
```

Both are quotations inside records and both are correctly left alone. The
sentence should say two, so the next `grep` does not read the second as a
missed migration.

### 8 · Phase 3's removes table names two of the four units it removed

An AST comparison of `tests/test_a_rider_reaches_its_file.py` between
`origin/release/v0.9.1` and `404dd4d` gives four removals:
`test_every_rider_stamp_names_a_commit_this_branch_can_reach`, `is_shallow`,  <!-- NAME NOT IN TREE -->
`test_every_rider_carries_the_date_and_sha_it_was_verified_at`, and `STAMP`.  <!-- NAME NOT IN TREE -->
`phases/phase-3.md`'s *What this phase removes* names the first two. The other
two have live replacements — `test_every_rider_carries_a_verification_stamp`
and `NEW_STAMP` — so nothing is lost; the table is what is incomplete.

## What held, re-derived rather than accepted

- **The self-reference fixed point.** Editing a rider's own prose leaves the
  hash where it was; changing the code under it moves it. Both executed on
  fixtures, and both go red under the mutation that removes the exclusion.
- **The exclusion's losses look like the whole set for the `#` path.** Three
  constructed attacks all end loud rather than silent: commenting out a guard
  directly under a rider **drifts** (the region shrinks with the function), a
  rider whose `<!--` sits on its own line reports BROKEN *no verification
  stamp*, and a rider with no closing `-->` reports BROKEN *the anchor names a
  region that is entirely rider comment*. Only added or removed comment lines
  butted against a rider are swallowed, which is what `spec.md` states.
- **Two riders in one unit.** Re-run: narrowing the rule to `blocks[:1]` turns
  `test_a_second_rider_in_a_unit_does_not_drift_the_first` red. The hardened
  fixture pins what it claims to. (What it does not pin is finding 4.)
- **Every mutation the build reported.** Seven ran, each turning its named case
  red, each restored, 19 green after.
- **The twentieth rider fires when you do what it asks.** Adding
  `("exported_at", 12345)` to the parametrize list drifts it, exit 1.
- **The CI message names a live dependency.** `test_the_reopening_is_one.py`
  reports `s` with *"origin/release/v0.8.1 is not fetched here"*, so the
  skipping shape the rewritten message warns about is real and observed. The
  removed shallow-clone assertion's job is still done at the workflow level by
  `test_every_job_that_runs_pytest_has_the_whole_history` itself, which fails
  when a pytest job drops `fetch-depth: 0`.
- **135 is the right number.** `grep -c '^| Target SHA |'` over
  `seal/specs/**/round-*.md` gives 135 rows in 135 files.
- **The mid-run `git checkout 29e0460 -- .` left no trace in the committed
  tree.** `29e0460` is not an ancestor of `404dd4d`, and no file the branch
  touched is byte-identical to its `29e0460` version. The tree is
  self-consistent: 20 riders OK, `bin/evidence-check` 815 ok · 0 drifted · 0
  broken, and the module's 19 cases green. What cannot be checked is
  uncommitted work at that moment, because no record of the incident exists —
  see the Deferred table.

### 9 · Out of verified scope

The full suite, the repository-wide lint and the typecheck were not run.
Contract §2 reserves them for the orchestrator, after the rounds settle. What
ran here is narrow and listed under *Executed probes*.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 Twelve stamps assert a 2026-09-08 reading that did not happen; the records claim the twelve original dates were preserved | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` · `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S4 | open | **executed** — `--migrate` in a fresh clone at `cbdd66e` writes 2026-08-31 / 09-02 / 09-06 / 09-07 for eleven riders; the twelfth region hashes to `8e0a246a` at both `4581fe1` and HEAD, so it keeps 2026-09-06. Every stamp at `4bf8dcb` and at HEAD reads 2026-09-08 |
| 2 | 🔴 `reverify` rewrites a stamp whose region hash is unchanged, and `--only` takes a file so it re-dates every rider in it | `.github/scripts/rider_check.py:421` · message at `:344` | open | **executed** — `--reverify --only hooks/worktree-guard.py` restamped three riders with three unchanged hashes and moved three dates |
| 3 | 🟡 A date-only re-stamp drifts the evidence ledger row for a unit nobody edited, against `phase-4.md`'s steady-state claim | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` | open | **executed** — one date digit changed in `hooks/dispatch.py` gives `rider_check` 20 ok exit 0 and `evidence_check` `DRIFTED hooks/dispatch.py#run_gate` exit 1 |
| 4 | 🔴 Two riders written back-to-back merge into one block; the second one's stamp is never resolved, compared, or reported as missing | `.github/scripts/rider_check.py:197` and `:218` | open | **executed** — a fixture whose second rider carries `deadbeef` reports `1 ok · 0 drifted · 0 broken`; `all_riders` returns one rider and reads one stamp |
| 5 | 🟡 Three hand-written anchors are quoted sentences, so a reword reports BROKEN rather than DRIFTED — and `skills/implement/SKILL.md`'s rider asks for exactly that reword | `agents/smith.md:60` · `skills/implement/SKILL.md:379` · `templates/evidence-check.yml:5` | open | **executed** — one word changed in each anchored line gives `BROKEN … the anchor resolves to nothing in this file`, exit 2. `evidence_check.resolve_unit`'s docstring and `CLAUDE.md` both state the rule this breaks |
| 6 | 🟡 The migration's headline refusal says git cannot resolve `881fb0f`; git resolves it, and the file simply did not exist at that path | `.github/scripts/rider_check.py:359` and `:504` · `phases/phase-4.md` · ledger row S4 | open | **executed** — `git cat-file -t 881fb0f` → commit, ancestor of HEAD, 2026-09-02; `git show 881fb0f:./.github/scripts/fold_ledger.py` → *path exists on disk, but not in '881fb0f'* |
| 7 | ⬜ The disclosure says the old stamp string survives in one record; it survives in two | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md:28` · `overview.md:36` | open | **executed** — `grep -rn "Verified [0-9-]* at [0-9a-f]"` also hits `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96` |
| 8 | ⬜ Phase 3's removes table names two of the four units the phase removed | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-3.md` | open | **executed** — an AST comparison of the test file across the range also removes `test_every_rider_carries_the_date_and_sha_it_was_verified_at` and `STAMP`; both have live replacements |  <!-- NAME NOT IN TREE -->
| 9 | ❓ out of verified scope — the full suite, the repository-wide lint and the typecheck | whole tree | open | **unverified** — contract §2; the orchestrator answers |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_rider_reaches_its_file.py -q` in a clone at `404dd4d` | `19 passed in 0.35s` |
| `python3 .github/scripts/rider_check.py` in the working tree | `20 ok · 0 drifted · 0 broken`, exit 0 |
| Seven mutations, one at a time, each restored | each turns its named case red; `blocks[:1]` → the second-rider case · exclusion removed → the fixed-point and prose cases · comment-head dropped → the prose/string case · block stopped at `# ` → the blank-comment-line case · one `at <sha>` stamp restored → `test_no_rider_stamp_names_a_commit` · one hash digit changed → the resolve-and-reproduce case · `git status` added to the check path → `test_the_check_asks_git_for_nothing`. Restored: `19 passed` |
| `git clone --no-local` at `cbdd66e`, then `--migrate` | `11 migrated · 8 refused`, exit 1, dates 2026-08-31 / 09-02 / 09-06 / 09-07 preserved. The two extra refusals against this repository are objects a `--no-local` clone does not carry |
| Region hash of `test_the_refusal_above_can_actually_fail` at `4581fe1` and at HEAD | `8e0a246a` both — the twelfth date `--migrate` proves in this repository |
| `--reverify --only hooks/worktree-guard.py` on the migrated clone | `3 restamped · 0 refused`; three unchanged hashes, three dates moved to 2026-09-08 |
| One rider date changed to 2026-09-09, then both checkers | `rider_check` `20 ok`, exit 0 · `evidence_check` `DRIFTED hooks/dispatch.py#run_gate content changed at 54-98`, exit 1 |
| Fixture: two riders back to back, second stamped `deadbeef` | `blocks [(2,5)]` · one rider found · one stamp read · `1 ok · 0 drifted · 0 broken` |
| One word changed in each of the three quoted-line anchors | three `BROKEN … resolves to nothing`, exit 2 |
| Constructed exclusion attacks: guard commented out under a rider · `<!--` on its own line · missing `-->` | drifts · BROKEN *no verification stamp* · BROKEN *entirely rider comment*. None silent |
| `("exported_at", 12345)` added to the parametrize list the twentieth rider names | `DRIFTED tests/test_the_records_can_be_carried_out_and_in.py:1415`, exit 1 |
| `bin/test tests/test_the_reopening_is_one.py -q -rs` | `35 passed, 1 skipped` — `SKIPPED … origin/release/v0.8.1 is not fetched here` |
| `bin/test tests/test_ci_gives_the_checks_what_they_need.py -q` | `2 passed` |
| `bin/evidence-check` on the working tree | `total: 815 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `git for-each-ref 'refs/pull/*/head'` and `'refs/remotes/pull/*/head'` | `0` and `86` |
| `chain_check.reachable` over every round record's `Target SHA` | 120 SHAs parsed; 117 are not ancestors of HEAD, and 116 of those resolve through `refs/remotes/pull/<N>/head`. The one that does not (`bc94eb1`) is still carried by `origin/fix/111-a-git-call-that-fails-reads-as-no-remote`, which `reachable` is given as a declared ref |
| `grep -c '^| Target SHA |'` over `seal/specs/**/round-*.md` | 135 rows in 135 files |
| `git merge-base --is-ancestor 29e0460 404dd4d`, and every branch-touched file against `29e0460` | not an ancestor; no file identical to its `29e0460` version |

Every probe file was removed; nothing was written into the working tree. The
mutations ran in `git clone --no-local` copies under the session scratchpad.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `templates/sdd-round.md` and five other places name `refs/pull/<N>/head`, and `chain_check.py:617` scans `refs/remotes/pull/`. Executed: `git for-each-ref 'refs/pull/*/head'` returns 0 refs here and `refs/remotes/pull/*/head` returns 86. The exemption's first ground still holds — 117 of 120 squashed target SHAs resolve through the fallback — but a reader who runs the namespace the template names gets nothing and reads the ground as false. `tests/test_a_rider_reaches_its_file.py:116` pins the wrong string. The same six documents also carry it: `spec.md` §Question 2, `questions.md` A2, `phases/phase-1.md`, `changelog.md`, ledger row S5 | the pull request; it is one word in five documents and one assertion, and it is not a defect in the migration | the repository owner |
| Whether the mid-run `git checkout 29e0460 -- .` lost any uncommitted work. The committed tree carries no trace of it, but no record of the incident exists in `spec.md`, `plan.md`, `overview.md` or any phase record, so there is nothing to compare a claim against | `overview.md`'s *Where spec and implementation diverged*, which is where the other mid-run corrections are recorded | the implementing session |
| Whether a drifted rider is answered often enough to be worth its noise | `seal/follow-up.md`, which already states the trade as overturnable | the repository owner (carried from `overview.md`, unchanged) |
| `templates/evidence-check.yml`'s rider is half spent — the quoted phrase *"let drift warn without blocking"* no longer exists in the file | the repository owner, per `overview.md` | the repository owner (carried, unchanged) |

## Paste-ready fixes

Finding 2 — `.github/scripts/rider_check.py:421`. A rider whose content has
not moved was not re-read, so its date must not move either.

```python
        if digest == rider.new.group("hash"):
            # The content has not moved, so nobody re-read anything. Writing
            # today's date over the recorded one asserts a reading that did
            # not happen, which is the half of a stamp `--migrate` refuses to
            # manufacture and the half `--reverify` was silently rewriting.
            continue
```

Finding 2, the second half — `.github/scripts/rider_check.py:337-352`. Say
which rider to re-stamp, not which file, so answering one does not touch its
neighbours.

```python
                    "`{}` changed since this was verified on {} ({} -> {}). "
                    "Read the rider — that is what it is for — then either do "
                    "what it asks and delete it, or "
                    "`rider_check.py --reverify --only {}` — which re-stamps "
                    "every rider in that file, so read the others in it "
                    "first".format(
```

Finding 1 — the twelve stamps. With the fix above in place, restore each
recorded date; the hashes are already correct and must not change.

```
hooks/cmdline.py:1784                                            2026-09-08 -> 2026-08-31
hooks/cmdline.py:1827                                            2026-09-08 -> 2026-08-31
hooks/dispatch.py:94                                             2026-09-08 -> 2026-09-02
hooks/optin.py:57                                                2026-09-08 -> 2026-08-31
hooks/review-history-guard.py:161                                2026-09-08 -> 2026-08-31
hooks/review-skill-gate.py:128                                   2026-09-08 -> 2026-08-31
hooks/worktree-guard.py:173                                      2026-09-08 -> 2026-08-31
hooks/worktree-guard.py:230                                      2026-09-08 -> 2026-08-31
hooks/worktree-guard.py:1494                                     2026-09-08 -> 2026-08-31
skills/code-review/scripts/round_record.py:1870                  2026-09-08 -> 2026-09-06
skills/evidence-check/scripts/evidence_check.py:1802             2026-09-08 -> 2026-09-07
tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:629  2026-09-08 -> 2026-09-06
```

Verify the whole set the way this round did, rather than by hand:

```bash
git clone --no-local . /tmp/rider-dates && git -C /tmp/rider-dates checkout -q cbdd66e
python3 /tmp/rider-dates/.github/scripts/rider_check.py --root /tmp/rider-dates --migrate
# every `migrated` line's date is the date the corresponding stamp must carry
```

Finding 3 — `phases/phase-4.md`, the paragraph beginning *"The rider edits
drifted six ledger rows"*. Its last two sentences are false while finding 2
stands and become true once it is fixed.

```markdown
In steady state it adds no new drift event, but only once `--reverify` stops
rewriting a stamp whose region hash has not moved: until then a date-only
re-stamp drifts the ledger row for a unit nobody edited, and the two checks
disagree — measured, `rider_check` 20 ok and `evidence_check` DRIFTED on
`hooks/dispatch.py#run_gate` from one changed date digit.
```

Finding 4 — `.github/scripts/rider_check.py:197-206`. A second marker inside a
comment run opens a second block, so its stamp is read and checked.

```python
        elif stripped.startswith("#"):
            j = i
            # A second `RIDER:` inside the run is a second rider, not more of
            # this one. Without this, back-to-back riders merge into one block
            # and only the first stamp is ever resolved -- the same silence as
            # a rider outside `RIDER_ROOTS`, which is what #239 closed.
            while (
                j + 1 < n
                and lines[j + 1].lstrip().startswith("#")
                and MARKER not in lines[j + 1]
            ):
                j += 1
            end = j
```

and the case that must be seen red against the reader as it stands:

```python
def test_a_second_rider_directly_under_the_first_is_its_own_rider(tmp_path):
    """Back-to-back riders merged into one comment run, so `all_riders`
    returned one rider, `Rider.new` read the FIRST stamp, and the second
    rider's hash was never resolved. A rider held by nothing is the defect
    #239 closed for `RIDER_ROOTS`; this is the same one inside a block."""
    src = (
        "def unit():\n"
        f"    {MARK} first claim\n"
        "    # Verified 2026-01-01 against unit@00000000\n"
        f"    {MARK} second claim, written straight under the first\n"
        "    # Verified 2026-01-02 against unit@deadbeef\n"
        "    value = 1\n"
        "    return value\n"
    )
    blocks = riders.comment_blocks(src.splitlines())
    assert len(blocks) == 2, f"the two riders merged into one block: {blocks}"
    stamps = [r.new.group("hash") for r in riders.riders_in("m.py", src)]
    assert "deadbeef" in stamps, f"the second rider's stamp was never read: {stamps}"
```

Finding 5 — re-anchor the three riders to structure the document owns. For
`skills/implement/SKILL.md:379`, the enclosing heading, so answering the rider
by rewording the sentence reports DRIFTED:

```
     Verified 2026-09-08 against "## <the enclosing heading, verbatim>"@<hash from --reverify>.
```

For `templates/evidence-check.yml:5`, the anchor is a comment line the rider
itself asks somebody to correct, which has the same problem. Anchor it to the
`name:` line instead and let the hash carry the header:

```
# Verified 2026-09-08 against "name: evidence-check"@<hash from --reverify>.
```

For `agents/smith.md:60`, the rider is about the waiver example, and the
example is a code span inside a paragraph that will be reworded before the
example is. Anchor the enclosing heading rather than the line.

Recompute every hash after re-anchoring with the finding-2 fix in place:

```bash
python3 .github/scripts/rider_check.py --reverify --only skills/implement/SKILL.md
python3 .github/scripts/rider_check.py --reverify --only templates/evidence-check.yml
python3 .github/scripts/rider_check.py --reverify --only agents/smith.md
```

Finding 6 — `.github/scripts/rider_check.py:359-371` and `:504-511`. Name the
cause instead of asserting one.

```python
def content_at(root, sha, rel):
    """(the file as the stamped commit held it, why not) — one of them is None.

    Three different things fail here and they are three different repairs: the
    commit is gone, the commit is fine and the path was not in it, or git could
    not be run at all. The refusal used to say the first for all three, and the
    record built on it read a stamp naming a commit that predates its own file
    as the squash orphaning a stamp in the act.
    """
    try:
        run = subprocess.run(
            ["git", "-C", root, "show", f"{sha}:./{rel}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None, "git could not be run"
    if run.returncode == 0:
        return run.stdout, None
    known = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True,
    )
    if known.returncode != 0:
        return None, f"git cannot resolve {sha} any more"
    return None, f"{sha} resolves, but {rel} was not in it"
```

with the call site at `:501` reading:

```python
        was, why_not = content_at(root, rider.old.group("sha"), rider.rel)
        if was is None:
            refused.append(
                (
                    rider.where(),
                    "{}, so the date cannot be proved. Re-read the rider and "
                    "`--reverify`".format(why_not),
                )
            )
            continue
```

and the two records corrected — `phases/phase-4.md`'s third bullet and ledger
row S4's *Verified behavior* cell:

```markdown
- **One names a commit that predates its own file.**
  `.github/scripts/fold_ledger.py` was stamped `881fb0f`, which git resolves
  and which is an ancestor of HEAD — `fold_ledger.py` was simply not in that
  tree. Not the squash orphaning a stamp, which this migration never observed
  in the act; a stamp that was wrong when it was written.
```

Finding 7 — `questions.md:28` and `overview.md:36`, the same sentence in both:

```markdown
it is one of the two places the old string survives a `grep`, with
`seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96`
```

Finding 8 — `phases/phase-3.md`, two more rows in *What this phase removes*:

```markdown
| `test_every_rider_carries_the_date_and_sha_it_was_verified_at` — NAME NOT IN TREE | replaced by `test_every_rider_carries_a_verification_stamp`, in the same file |
| `STAMP` — NAME NOT IN TREE | replaced by `NEW_STAMP` in `.github/scripts/rider_check.py`, which the test file imports rather than restating |
```

Needs a fix: yes — findings 1, 2, 3 and 4; 5 and 6 are fix or justify
Loses a record or crashes: no

## For the record the orchestrator writes

| Row | Value |
|---|---|
| Contract changes | `RIDER_ROOTS` moved from `tests/test_a_rider_reaches_its_file.py` to `.github/scripts/rider_check.py`, and the test imports it → the test file · `test_every_rider_stamp_names_a_commit_this_branch_can_reach`, `test_every_rider_carries_the_date_and_sha_it_was_verified_at`, `is_shallow` and `STAMP` removed → pytest · `test_every_job_that_runs_pytest_has_the_whole_history`'s failure text rewritten → whoever reads a CI failure |  <!-- NAME NOT IN TREE -->
| New units | `HERE` (depth 1); `ROOT` (depth 1); `CHECKER` (depth 1); `RIDER_ROOTS` (depth 1); `SKIP_DIRS` (depth 1); `READABLE` (depth 1); `MARKER` (depth 1); `OLD_STAMP` (depth 1); `NEW_STAMP` (depth 1); `load_checker` (depth 1); `comment_blocks` (depth 1); `Rider` (depth 1); `Rider.__init__` (depth 2); `Rider.where` (depth 2); `riders_in` (depth 1); `tree_files` (depth 1); `all_riders` (depth 1); `region_lines` (depth 1); `region_hash` (depth 1); `check` (depth 1); `content_at` (depth 1); `restamp` (depth 1); `write_block` (depth 1); `reverify` (depth 1); `inferred_anchor` (depth 1); `migrate` (depth 1); `main` (depth 1) — all in `.github/scripts/rider_check.py`; `_load` (depth 1); `riders` (depth 1); `CHECKER` (depth 1); `OLD_STAMP` (depth 1); `MARK` (depth 1); `a_module` (depth 1); `hashed` (depth 1); `test_the_header_states_the_stamp_form_riders_actually_carry` (depth 1); `test_the_round_template_says_why_target_sha_is_exempt` (depth 1); `test_every_rider_carries_a_verification_stamp` (depth 1); `test_no_rider_stamp_names_a_commit` (depth 1); `test_every_rider_stamp_resolves_and_reproduces_its_hash` (depth 1); `test_the_check_asks_git_for_nothing` (depth 1); `test_the_hash_does_not_cover_the_rider_that_carries_it` (depth 1); `test_editing_a_riders_own_prose_does_not_drift_it` (depth 1); `test_a_second_rider_in_a_unit_does_not_drift_the_first` (depth 1); `test_a_changed_unit_drifts` (depth 1); `test_a_vanished_anchor_is_broken_not_drifted` (depth 1); `test_the_marker_in_prose_or_a_string_is_not_a_rider` (depth 1); `test_a_comment_block_runs_through_its_blank_comment_lines` (depth 1) — all in `tests/test_a_rider_reaches_its_file.py` |
| Broad gate | not yet — findings remain open, so it is not due |

## Proof

Files opened for this round:

```
.github/scripts/rider_check.py
.github/scripts/fold_ledger.py (diff)
agents/smith.md
CONTRIBUTING.md
docs/flow.md (diff)
hooks/cmdline.py · hooks/dispatch.py · hooks/optin.py · hooks/review-history-guard.py
hooks/review-skill-gate.py · hooks/root-migrate.py · hooks/worktree-guard.py (stamps)
seal/config.md
seal/follow-up.md (diff)
seal/ledger.md (diff and the run_gate row)
seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/spec.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/plan.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/routing.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/changelog.md
seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-1.md … phase-6.md
skills/code-review/scripts/chain_check.py (reachable, carried_by_a_pull_head, PULL_HEADS)
skills/code-review/scripts/round_record.py (diff)
skills/evidence-check/scripts/evidence_check.py (ANCHOR_RE … resolve_unit; diff)
skills/implement/SKILL.md (diff and the rider's context)
templates/evidence-check.yml
templates/sdd-round.md (diff)
tests/test_a_rider_reaches_its_file.py
tests/test_ci_gives_the_checks_what_they_need.py (diff)
tests/test_the_printed_ledger_name_is_the_file_that_was_read.py (diff)
tests/test_the_records_can_be_carried_out_and_in.py (diff)
~/.claude/skills/writing-style/SKILL.md
```
