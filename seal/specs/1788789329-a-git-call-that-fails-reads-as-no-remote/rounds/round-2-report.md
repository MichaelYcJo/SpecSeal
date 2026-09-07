# Round 2 — the verifying round (#111, PR #234)

Target SHA `bc94eb136a11e8604dce7d313e0f5964c4856bb9`. The worktree did not move
under me: `git status --short` is empty at the start and at the end, apart from
this file. Every command ran in a `git clone --no-local` of the worktree at the
target; the worktree itself was read and never written.

## What this round was asked

The verifying round of `1788789329-a-git-call-that-fails-reads-as-no-remote`
(ticket #111, PR #234), at target `bc94eb1`, base `86e140f`, over the fix diff
`5cf81b3..bc94eb1` whose substance is `60d5354` and `4729bbe`. Round 1's five
verdicts are inherited, and the question is whether each is actually closed.

Three things the fix pass reported about its own diff were named as the place
attention belongs, and two of them are defects its own first fix commit
introduced: E1, the advice branching on `mine is None` so that a both-silent
import went back to the re-run line, with the case written alongside asserting
that output as correct; E2, `manifest_of` returning a flat list so that an
export missing only the HEAD SHA promised a refusal that was never coming; and
E3, four escape cases naming the `<stem>.zip.partial` they plant a link at from
the local date where the export names it from UTC, which arms or disarms them
by the hour they run at and therefore had to be re-derived rather than read.

Also named: whether `if head is not None` surviving mutation at 96 passed is
really behaviour-identical; whether moving
`test_a_manifest_field_of_the_wrong_type_does_not_raise`'s two `remote` rows
behind `--allow-unreadable-remote` preserved what that case was for; and
whether each of the `seal/ledger.md` rows the fix pass re-stamped still carries
a claim the branch leaves true. The design decision — an unreadable remote
refuses, and the escape is a flag of its own — is settled and was not reopened.

## The short of it

Every one of round 1's five findings is closed, and all three of E1, E2 and E3
hold up under execution. Nothing in the code needs a fix.

What this round opens is three ⬜ items. Two are the run's own paperwork and one
is a message that is true but tells a person half of what they need:

- The fix record says it re-stamped **six rows** in `seal/ledger.md`. Six
  *anchors* moved; they sit in **eleven** rows, and the two the record
  describes as "two rows anchored at `import_`" are one `import_` anchor
  reaching eight rows plus one test anchor reaching one.
- `round-1.md`'s `Needs a fix` cell stops mid-sentence, because the report
  wrote that value across three lines and the generator reads one.
- When the zip and this clone are silent at once, the closing advice names only
  the export. Following it alone leaves the import still refusing.

## Findings

### 1 ⬜ The fix record's count of what it re-stamped does not match the file

`seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md:46`

The comment reads *"Round 1's fix pass re-stamped six more rows there … four
cases pinning the export's `.partial` escapes … and two rows anchored at
`import_`"*. Measured over `5cf81b3..bc94eb1`:

- **Rows whose line changed** — eleven, not six.
- **Anchors whose hash moved** — six, which is where the number comes from.
- **The two beyond the four `.partial` cases** — `import_`, which appears in
  eight of the eleven rows, and
  `test_a_manifest_field_of_the_wrong_type_does_not_raise`, which is a test
  anchor and appears in one.

Why it matters: the disclosure exists so a reader can audit which claims were
re-read before their stamps moved. A reader told *two rows anchored at
`import_`* opens two of eight and stops.

The claims themselves are sound, and I opened all eleven. The eight
`import_` rows are about the member count, the declared total, the manifest's
own size, `testzip`, `read_manifest` and `unsafe` — every one of which runs
before the remote guard the fix range touched, confirmed by reading the order
inside `import_`. The four `.partial` rows are about `write_zip`, `unused` and
`O_EXCL`; only the clock the cases name the path by changed, so those claims
now hold around the clock instead of fifteen hours a day. The
wrong-type row is strengthened rather than weakened, for the reason finding 5
below gives.

The correction is to the sentence: *six anchors, across eleven rows — the four
`.partial` cases, `import_` in eight rows, and
`test_a_manifest_field_of_the_wrong_type_does_not_raise` in one.*

### 2 ⬜ `round-1.md`'s `Needs a fix` cell stops mid-sentence

`seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/rounds/round-1.md:12`

The cell reads `yes — findings 1, 2 and 3. A guard whose only signal is key`.
The report's own line runs on for three more clauses, and the row keeps the
first line alone: `round_record.py`'s cell writer refuses a newline outright,
so a multi-line value arrives as its first line.

This is not a defect in the generator — a row is one line and its cells are
what stands between the pipes. It is a defect in the record it produced, and
the record is what a later reader has. Whoever writes a `Needs a fix:` line
owes it in one line; this report does so.

### 3 ⬜ Both sides silent: the advice names one of the two steps

`skills/implement/scripts/seal.py:1135`

E1's fix is correct and I confirm it below. What it leaves is a smaller thing.
With the zip silent and this clone's git silent at once, executed:

```
whether this zip came from this repository cannot be answered:
  this clone's remote could not be read: git config could not be run (…timed out after 15 seconds)
  the zip records no remote this command can read, so the machine that exported it could not read one either

Nothing was written. Records are keyed by work-item id, …
Re-running this cannot change what the zip records — export again on the machine that wrote it, or pass --allow-unreadable-remote to import without the check.
```

Exporting again clears the zip side and nothing else. `mine is None` still
holds, so the next import refuses again, this time with the other advice line.

Not a fix request, for two reasons. The bullet above names the other half, so
nothing is hidden; and `--allow-unreadable-remote` is offered in the same
sentence and clears both sides in one step, so nobody is stuck. The precedence
the fix chose is right — the zip side is the one no re-run here can clear, and
naming the other first is what round 1's 🟡 2 was.

## What each inherited verdict rests on now

**Round 1's 🟡 1 — the guard reads the field's type.** `the_zip_is_silent = not
isinstance(theirs, str)` at `seal.py:1094`. Executed: reverting the signal to
key presence reddens five cases. The parametrised values are `None`, `42`,
`[]`, `{}` and `True`, and `json.dumps` writes each as the shape the guard has
to see.

**Round 1's 🟡 2 and E1 — three combinations reach the refusal, and there is no
fourth.** `unreadable` is non-empty when `mine is None` or when the zip is
silent, and `the_zip_is_silent` alone chooses the advice. That partitions four
states, of which the fourth — both sides answered — never reaches the block:

| this clone | the zip | what happens |
|---|---|---|
| silent | silent | refuses; the zip's advice |
| silent | answered | refuses; the re-run advice |
| answered | silent | refuses; the zip's advice |
| answered | answered | no refusal |

`test_the_advice_names_the_machine_that_can_fix_it` runs the first three, with
the `config --get` injection still in force for the both-silent leg. Executed:
restoring the `mine is None` branch reddens it.

**E2 — the note is keyed on `remote` and nothing else.** `manifest_of` returns
`unread` as a dict at `seal.py:425-440`, and `export` prints one line per key
and the flag sentence only under `if "remote" in unread` at `:596`. Executed:
widening that to `if unread` reddens
`test_the_export_omits_a_head_it_could_not_read`. I also ran the combination no
case covers — both fields unread — and the output is correct: two lines, one
flag sentence.

**E3 — re-derived, not read, and the class is empty.** The measurement is
armed by the hour, so I checked the hour first. At the moment this round ran,
`datetime.datetime.now(datetime.UTC)` gave `2026-09-07` and
`datetime.date.today()` gave `2026-09-08`, so the two clocks disagreed. With
the helper reverted to the local date, all four cases went red, and the failure
names both dates: a link planted at `seal-repo-2026-09-08.zip.partial` against
a zip the export wrote as `seal-repo-2026-09-07.zip`. With the helper as
committed, the module is 96 passed.

For the class rather than the coordinate: `grep` over `tests/`,
`.github/scripts/`, `skills/`, `bin/`, `hooks/` and `templates/` for
`date.today`, `localtime`, `astimezone` and `%Y-%m-%d` returns no local-clock
date anywhere. The three remaining date reads —
`the_stem_the_export_will_use`, `gather_changelog.py:151` and
`fold_ledger.py:358` — are all UTC, and both release scripts take `--date`
explicitly in every case that asserts on one. Every other clock read in the
tree is `time.time()`, which carries no timezone. No second instance exists.

**Round 1's ⬜ 4 — the docstring.** `remote_url`'s docstring at
`seal.py:194-215` now names all three states that exit 1 with empty streams and
says exit 1 is an answer only for a caller whose `root` git has already
resolved. Read, not executed; the finding was never reachable.

**Round 1's ⬜ 5 and M6 — the surviving mutation is correct.** `manifest_of`
admits `head` on `is not None` at `seal.py:436`. Reverting it to `if head`
survives at 96 passed, which I reproduced. *Behaviour-identical* is the right
word for it: `head_sha` returns `git_asked(...)`, whose value is `None` or a
`str` and never `0`, so the two spellings differ on exactly one value, `""`,
which `git rev-parse HEAD` does not produce at exit 0. The change is in the
safe direction and no case can catch it. Recording it alive rather than hiding
it is the right call.

**The moved case preserves what it was for.** `remote` is read out of the
manifest at exactly one place, `seal.py:1090`, and the only path on which a
non-string reaches `normalise_remote` from there is behind
`--allow-unreadable-remote`. That is the path the two `remote` rows now take at
`tests/…:1450`, so `normalise_remote`'s own `isinstance` guard — what those
rows have always been about — is still exercised. What the rows used to also
cover, a non-string arriving on the default path, is now a refusal and is
covered by `test_a_manifest_remote_of_the_wrong_type_refuses`. Both halves are
pinned. Moved, not narrowed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The fix record says six rows were re-stamped in `seal/ledger.md`; six anchors moved across eleven rows, and the two beyond the `.partial` cases are `import_` in eight rows and one test anchor in one | `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md:46` | open | Executed: the anchor sets of `seal/ledger.md` at `5cf81b3` and `bc94eb1` differ by six anchors; `git diff` shows eleven changed rows. All eleven claims opened and none is falsified. A record correction — no fix pass is owed |
| 2 | `round-1.md`'s `Needs a fix` cell stops mid-sentence, because the report wrote the value across three lines and the generator keeps one | `seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/rounds/round-1.md:12` | open | Read: `round_record.py`'s cell writer refuses a newline, so the row carries the first line alone. A record correction |
| 3 | With the zip and this clone silent at once, the closing advice names only the export; following it alone leaves the import still refusing | `skills/implement/scripts/seal.py:1135` | open | Executed: both reasons print above, then one advice line. Not a fix request — the bullet names the other half and `--allow-unreadable-remote` clears both in one step |
| 4 | Round 1's 🟡 1 — a non-string `remote` walks past the refusal | `skills/implement/scripts/seal.py:1094` | answered | Executed at `bc94eb1`: reverting the signal to key presence reddens five cases. `null`, `42`, `[]`, `{}` and `True` all refuse at exit 1 with the root unchanged |
| 5 | Round 1's 🟡 2, and E1 — the advice sends the person into a re-run that can never end | `skills/implement/scripts/seal.py:1135`, `tests/test_the_records_can_be_carried_out_and_in.py:669` | answered | Executed: restoring the `mine is None` branch reddens the case. Three combinations reach the refusal and the case runs all three; the fourth never reaches the block |
| 6 | Round 1's 🟡 3, and E2 — the export says nothing about the field it left out, and the flag note fired for a missing HEAD SHA | `skills/implement/scripts/seal.py:425-440`, `:594-608` | answered | Executed: widening `if "remote" in unread` to `if unread` reddens `test_the_export_omits_a_head_it_could_not_read`. The both-unread combination, which no case covers, prints correctly |
| 7 | Round 1's ⬜ 4 — `remote_url`'s docstring missed exit 1's third meaning | `skills/implement/scripts/seal.py:194-215` | answered | Read. The docstring now names all three and states the condition a caller reaching for `answered=(0, 1)` has to be able to say |
| 8 | Round 1's ⬜ 5, and M6 — two spellings of one question five lines apart | `skills/implement/scripts/seal.py:436` | answered | Executed: reverting to `if head` survives at 96 passed, reproduced. `head_sha`'s value is `None` or a `str`, so the two differ on `""` alone, which git does not produce at exit 0. Correctly recorded alive |
| 9 | E3 — four escape cases named the export's zip stem from the local clock | `tests/test_the_records_can_be_carried_out_and_in.py:108`, `:1138`, `:1162`, `:1192`, `:1219` | answered | Executed, re-derived rather than read: at the hour this round ran the two clocks read `2026-09-07` and `2026-09-08`, and reverting the helper reddened all four with both dates named in the failure |
| 10 | E3's class — whether any other case takes a date from a different clock than the code it pins | `tests/`, `.github/scripts/`, `skills/`, `bin/`, `hooks/`, `templates/` | answered | Executed `grep` for `date.today`, `localtime`, `astimezone` and `%Y-%m-%d`: no local-clock date anywhere. The three remaining reads are UTC, and every other clock read is `time.time()`, which has no timezone. No second instance |
| 11 | `test_a_manifest_field_of_the_wrong_type_does_not_raise` moved behind `--allow-unreadable-remote` | `tests/test_the_records_can_be_carried_out_and_in.py:1427`, `:1450` | answered | Read, with the reach measured: `remote` is read out of the manifest at `seal.py:1090` alone, and the flag is the only path from there to `normalise_remote` for a non-string. The default path is now a refusal and is pinned separately. Moved, not narrowed |
| 12 | The six re-stamped `seal/ledger.md` anchors each still carry a true claim | `seal/ledger.md` | answered | Executed `evidence-check .` at the target: `784 ok · 0 drifted · 0 broken`, exit 0. The eight `import_` rows are about checks that run before the guard this range touched, confirmed by reading the order inside `import_`; the four `.partial` rows are about `write_zip` and `unused`, untouched |
| 13 | `New units` and `Contract changes` on `round-1.md` | `seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/rounds/round-1.md:10-11` | answered | Re-derived by construction: diffing the top-level `def`/`class`/constant list across `5cf81b3..bc94eb1` returns exactly the five names the row carries, and no unit was added to `seal.py`. `manifest_of` is the only changed contract, and `export` its only code call site |
| 14 | The `Checked` date on every re-stamped row still reads `2026-09-03` | `seal/ledger.md` | answered | Already disclosed and routed to the repository owner in `overview.md` §*Not verified*, and round 1 recorded the same. Not re-raised |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_records_can_be_carried_out_and_in.py -q` at `bc94eb1` in a `git clone --no-local` | `96 passed`, exit 0 |
| `bin/test` over fifteen modules that pin the changed READMEs, ledger, ledger fragment, changelog fragment and work-item records (`test_docs_line_wrap`, `test_no_real_identifiers`, `test_lint_python`, `test_one_word_one_meaning`, `test_the_pull_request_language_is_the_repositorys`, `test_a_probe_does_not_outlive_its_round`, `test_a_row_points_by_content`, `test_the_ledger_fragments_fold_at_release`, `test_the_changelog_is_gathered_at_release`, `test_the_set_a_work_item_always_has`, `test_routing_is_recorded`, `test_absence_claims`, `test_release_hygiene`, `test_a_rider_reaches_its_file`, `test_chain_hooks`) | `432 passed`, exit 0 |
| The clock, before anything rested on it: `datetime.datetime.now(datetime.UTC)` against `datetime.date.today()` in the clone's interpreter | `2026-09-07` and `2026-09-08` — the two disagreed, so E3's window was open at the hour this round ran |
| E3 re-derived: the helper reverted to `datetime.date.today().isoformat()`, the four link cases run | `4 failed, 92 deselected`. `seal-repo-2026-09-08-2.zip` asserted against a zip the export wrote as `seal-repo-2026-09-07.zip` |
| Four mutations of the fixed units, each pattern asserted to match exactly once, applied, run, reverted | MA the advice back to `mine is None` → 1 red; MB the flag note keyed on either field → 1 red; MC the guard back to key presence → 5 red; MD `manifest_of` back to `if head` → **survives, 96 passed**, which is finding 5's own shape and is expected |
| E3's class: `grep` over `tests/`, `.github/scripts/`, `skills/`, `bin/`, `hooks/`, `templates/` for `date.today`, `localtime`, `astimezone`, `%Y-%m-%d`, `datetime.now`, `utcnow`, `time.time()` | No local-clock date anywhere. Three UTC date reads, and every other clock read is `time.time()` |
| The ledger's anchor sets at `5cf81b3` and `bc94eb1`, compared | Six anchors moved; `git diff` shows eleven changed rows |
| `bin/evidence-check .` at `bc94eb1` in the clone | `784 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0 |
| Probe (`tests/test_tmp_probe_r2.py` in the clone, run once, deleted): the both-silent refusal, an export with both fields unread, and `--allow-unreadable-remote` with a list-valued `remote` | Both-silent prints both reasons and the zip's advice alone; the export prints two omission lines and one flag sentence; the flag path imports at exit 0 with no traceback |

The mutation harness, run from the clone root:

```python
MUTATIONS = {
  "MA the advice branches on this clone again (E1's own defect)": (
     "            if the_zip_is_silent:",
     "            if mine is None:"),
  "MB the flag note keyed on either field again (E2's own defect)": (
     '    if "remote" in unread:',
     "    if unread:"),
  "MC the guard's signal back to key presence (finding 1)": (
     "        the_zip_is_silent = not isinstance(theirs, str)",
     '        the_zip_is_silent = "remote" not in manifest'),
  "MD manifest_of admits head on truthiness again (finding 5)": (
     "    head, head_why = head_sha(repo)\n    if head is not None:",
     "    head, head_why = head_sha(repo)\n    if head:"),
}
# each pattern asserted to match exactly once, applied, the module run, reverted
```

E3's re-derivation, which is the one measurement that is armed or disarmed by
the hour it runs at:

```python
# In the clone, before the mutation:
#   UTC date   2026-09-07
#   local date 2026-09-08
# so the window was open. The helper reverted to the local clock:
def the_stem_the_export_will_use(seal, repo):
    return seal.zip_stem(str(repo), datetime.date.today().isoformat())
# bin/test tests/test_the_records_can_be_carried_out_and_in.py \
#   -k "partial_name or o_excl or zips_own_name"
#   -> 4 failed, 92 deselected
```

## Inherited coordinates

| From | Coordinate | Why it was still worth opening |
|---|---|---|
| Round 1, finding 6 | `skills/implement/scripts/seal.py`, the `git()` call sites | Carried, not re-derived: the fix diff adds no `git()` call, which `git diff` shows by construction |
| Round 1, finding 7 | `seal/ledger.md`, the nine rows re-stamped before `5cf81b3` | Carried. This round re-derived only the six anchors the fix range moved |
| Round 1, finding 9 | `seal/ledger.md`, the `Checked` column | Carried as deferred. Not re-raised |
| Round 1's probes table | git's own exit codes, nine shapes against git 2.50.1 | Carried. Nothing in the fix range changes what git answers |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a re-stamped row's `Checked` date should move | `overview.md` §*Not verified* | the repository owner |
| Whether E3's residual window — the UTC midnight instant between the helper's call and the export's own — is worth closing | `overview.md` §*Not verified* | the repository owner |
| Whether `git config --get` exits 1 for an unset key on builds other than 2.50.1 | `overview.md` §*Not verified* | the repository owner |
| Windows | `overview.md` §*Not verified* | CI's Windows leg |
| `porcelain`, `indexed`, `tracked` and `gitlinks_under_root` moved onto `git_asked` | `overview.md` §*Not done* | whoever next edits one of them for a reason of its own |

Needs a fix: no
Loses a record or crashes: no

Nothing this round opened touches the root or raises. Findings 1 and 2 are
prose in records; finding 3 is a message that is true, printed on a path that
returns 1 at `seal.py:1148` before `destination_root` and `write_members`, so
nothing is written on it.

The broad gate has come due. `round-1.md` still reads `Broad gate | not yet`,
and this round opened nothing in the code, so the full suite, the
repository-wide lint and the typecheck are the next step and are the
orchestrator's.

For the record the orchestrator will write:

- **Contract changes** — `none`. This round opened no fixes. For the fix diff
  the round-1 record already carries, `manifest_of` is the only changed
  contract and I confirm it: `export` at `seal.py:577` is its only code call
  site, and the other two entries in that cell are markdown basenames, which
  `round_record.py`'s `call_sites` vocabulary writes for a call outside Python.
- **New units** — `none`, for the same reason. The five names on `round-1.md`
  are right by construction: diffing the top-level `def`, `class` and constant
  list across `5cf81b3..bc94eb1` returns exactly those five, all in
  `tests/test_the_records_can_be_carried_out_and_in.py`, and `seal.py` gained
  none.

## Proof

Files opened:

- `skills/implement/scripts/seal.py` (at `5cf81b3` and `bc94eb1`)
- `tests/test_the_records_can_be_carried_out_and_in.py` (at both)
- `tests/conftest.py`
- `seal/ledger.md` (at both, and the eleven changed rows)
- `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md`
- `seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/`:
  `overview.md`, `changelog.md`, `rounds/round-1.md`, `rounds/round-1-report.md`,
  `rounds/round-1-fixes.md`
- `README.md`, `README.ko.md` (the diff)
- `docs/review-chain-spec.md`, `templates/sdd-round.md`,
  `skills/code-review/scripts/round_record.py`
- `bin/test`, `bin/evidence-check`, `.github/scripts/run_tests.py` (head)
- `seal/config.md`, `CLAUDE.md` (repository and user)

Commands run are the Executed probes table above. Exit codes were read from the
runner's own status or as `cmd >/dev/null 2>&1; echo $?`, never through a pipe.

Not run, and who answers: the full suite, the repository-wide lint and the
typecheck — `agent-contract` §2 reserves them for the orchestrator, and they
are now due. The Windows leg — CI. `ruff check` and `ruff format --check` on
the changed files are inherited as executed from the fix pass and were not
re-run here; `tests/test_lint_python.py` passed at the target, which is the
closest check this round has on them.
