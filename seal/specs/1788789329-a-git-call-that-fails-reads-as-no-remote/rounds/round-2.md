# 1788789329-a-git-call-that-fails-reads-as-no-remote — review round 2

| Field | Value |
|---|---|
| Target SHA | bc94eb1 |
| Ran by | warden on claude-opus-5 |
| PR | 234 |
| Broad gate | passed at e13b75b — 2559 passed, 2 skipped; ruff check and ruff format clean |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of `1788789329-a-git-call-that-fails-reads-as-no-remote` (ticket #111, PR #234), at target `bc94eb1`, base `86e140f`. The verifying round: round 1's five findings were answered in `60d5354` and `4729bbe`, and the diff of those fixes is what this round was pointed at.

Round 1's verdicts were inherited rather than re-litigated. The fix pass's own re-enumeration was the named target, because two of the three things it reports are defects its own first fix commit introduced. E1 — the advice branched on `mine is None`, so when BOTH sides are silent it sent the person back to *"Run this again if the failure here was transient"*, which is finding 2's own defect re-entered at a narrower coordinate by the fix for finding 2, and the case written in the same commit asserted that output as correct. E2 — `manifest_of` returned a flat list, so an export that read the remote and only missed the HEAD SHA promised a fix for a refusal that was never coming. Both were to be checked for completeness of their combinations rather than read.

E3 was to be re-derived rather than read, because it is a case armed or disarmed by the hour it runs at: four escape cases name the `<stem>.zip.partial` they plant a link at from the LOCAL date while `seal.py:542` names it from UTC, so east of UTC they assert a refusal against nothing for nine hours a day. The round was also to ask whether any other case in the tree takes its date from a different clock than the code it pins.

Three further axes. M6 survives by construction and was called behaviour-identical — a truthiness read and an identity read differ on `""` and on `0`, and finding 5 existed because two spellings of one question sat five lines apart. One existing case was moved rather than broken, `test_a_manifest_field_of_the_wrong_type_does_not_raise`'s two `remote` rows now running behind `--allow-unreadable-remote`, and the move was to be judged for whether it preserved what the case was for. And `seal/ledger.md` was edited — six anchors re-stamped after the claims were re-read — which the repository rule allows only where a branch changes cited code and the claim still holds.

The design decision was settled and not the round's to reopen: an unreadable remote refuses, and the escape is `--allow-unreadable-remote`, a flag of its own, never `--allow-other-repo`.

The bound was stated: round 1 met the reopening floor, a round that opens nothing needing a fix does not consume the cap, and an unfounded finding costs the run its last round. The report was to be written to a file, finding ids bare integers, and every verdict row to carry one — round 1's record had five rows written with `—` and `round_record.py close` refused the whole file until they were numbered.

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

## Paste-ready fixes

no paste-ready fix in the report

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

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/implement/scripts/seal.py:1048` | round 1's 1 — fixed |
| round-1 | `skills/implement/scripts/seal.py:1067`, `README.md:526` | round 1's 2 — fixed |
| round-1 | `skills/implement/scripts/seal.py:406-411` | round 1's 3 — fixed |
| round-1 | `skills/implement/scripts/seal.py:194-213` | round 1's 4 — fixed |
| round-1 | `skills/implement/scripts/seal.py:407-411` | round 1's 5 — fixed |
| round-1 | `skills/implement/scripts/seal.py` | round 1's 6 — answered |
| round-1 | `seal/ledger.md` | round 1's 7 — answered |
| round-1 | `seal/ledger.md`, `seal/ledger/1788789329-…md` | round 1's 8 — answered |
| round-1 | `README.md`, `README.ko.md`, the work item's records | round 1's 10 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a re-stamped row's `Checked` date should move | `overview.md` §*Not verified* | the repository owner |
| Whether E3's residual window — the UTC midnight instant between the helper's call and the export's own — is worth closing | `overview.md` §*Not verified* | the repository owner |
| Whether `git config --get` exits 1 for an unset key on builds other than 2.50.1 | `overview.md` §*Not verified* | the repository owner |
| Windows | `overview.md` §*Not verified* | CI's Windows leg |
| `porcelain`, `indexed`, `tracked` and `gitlinks_under_root` moved onto `git_asked` | `overview.md` §*Not done* | whoever next edits one of them for a reason of its own |
