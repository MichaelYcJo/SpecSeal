# 1789296200-the-record-before-the-fix-sequence-has-no-arm — review round 2

| Field | Value |
|---|---|
| Target SHA | 3db3a3a9084cf3cb60b31835a467412c48e5a235 |
| Written late | no |
| Ran by | warden on claude-opus-5 |
| PR | 381 |
| Broad gate | 3207f42 against origin/release/v0.11.3 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round: round 1's fixes were written by a fix pass and read by nobody, and this round fills round 1's `Fixes checked by` cell. Scope was `b88a0b2..80040fe`, nine commits, judged against round 1's findings. Round 1's verdicts are inherited.

The reviewer was warned about the three mechanical shapes that had each cost a retry in this release — the terminal-line form, unclosed HTML comments inside fenced blocks, and a verdict `#` column that is not a bare integer — and told that axes checked and found clean go under their own heading rather than into the verdict table.

**The round opened nothing needing a fix**, and it re-derived rather than accepted:

- **The corrected grounds are honest.** It re-ran all four ref commands itself: the starred form returns 0, `refs/remotes/pull` returns 138, and `a0f0e9a` is an ancestor of `refs/remotes/pull/364/head`. The records state only the narrower true sentence and do not repeat round 1's false one.
- **The rescued measurement is what it claims** — `cmp` exit 0 and an identical SHA-256 against the original, forty records named individually, header counts 310 / 158 / 152 / 112 / 40.
- **The case that was red really was red.** The document at `eb7a56a^` carries *spawned before* once, the reworded example teaches the same thing, and nothing else this branch added to that file is within reach of any of the check's eleven needles.
- **Both new messages were run and read.** The behind line names both commits, offers no false reading, and writes the record at exit 0. The refusal carries the row, the cell shape, the flag and the by-hand path.
- **The advertised by-hand repair was driven end to end**: exit 1, the row added by hand and committed, exit 0. The fourth exit actually opens, which is the claim finding 1 was about and the one a reading could not settle.
- **Three new units each die alone**, and the `if not late` → `if late` mutation kills 16.
- **The two `survivors.md` rows are justified** — reproduced over `b88a0b2..1468e48` and both messages read; each already names its own exit, so neither is the class round 1 reported.

**Three opened and none of them a fix.** `overview.md:6` still says `evidence-check` 1161 and four new units where the tree now reads 1164 and seven; the first `survivors.md` row's quotation stands in four places in the same file, so the judgment is right and the anchor is weak; and the by-hand path the refusal advertises has no case, though the path itself is executed and true — whether a message's promise owes a case is the repository owner's call.

The orchestrator answered all three rather than fixing them, on the arithmetic this release has already paid for once: on the sibling branch for #354, fixing a ⬜ that the verifying round had deliberately kept off its fix list is what made that round close on a fix and ended the run at round 3. None of the three changes what any check reads.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the refusal at the pull request never names the fourth exit | `skills/code-review/scripts/chain_check.py:2607` | answered | **closed.** executed — the shipped refusal captured from a scratch repository names `Written late`, `--written-late` and *added by hand*; the case dies alone when the appended text is removed; and the advertised hand-edit exit was driven end to end, exit 1 to exit 0 |
| 🟡 2 | `head_moved_line` prints *0 commits stand between them* with two readings that are both false when HEAD is behind the reviewed commit | `skills/code-review/scripts/round_record.py:1557` | answered | **closed.** executed — the state reproduced on a scratch repository now prints the BEHIND line, names both commits, offers neither false reading, exits 0 and writes the record. A sideways branch still gets the listing line, so the new branch did not swallow the case it must not |
| ⬜ 3 | *1 commit stand between them* — the singular arm is written for the noun and not the verb | `skills/code-review/scripts/round_record.py:1580` | answered | **closed.** executed — the line reads *1 commit stands between them*, and reverting the verb arm fails the case written for it |
| ⬜ 4 | the forty differing records are named in no committed file | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:29` | answered | **closed, and round 1's grounds corrected rather than repeated.** executed — the rescued file is byte-identical to the measurement's output, names 40 records, and carries the five header counts; `overview.md` and `phase-1.md` point at it; and the four ref commands re-run here show the number can be retaken in this clone |
| ⬜ 5 | `written_late_reason` is called on every record whether or not anything is late | `skills/code-review/scripts/chain_check.py:2531` | answered | **closed.** read — the guard skips nothing but the subprocess; executed — inverting it fails 16 cases. The twelve-line comment the paste-ready block would have deleted is intact |
| ⬜ 6 | `overview.md`'s verified line still says `evidence-check` at 1161 ok and four new units; the branch answers 1164 and seven | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:6` | answered | The line was true of the run that wrote it; `evidence-check` reached 1164 and the unit count reached seven in later commits of the same fix pass. Correcting it now would make round 2 close on a fix, spending the one reopening that remains and calling a third round for a count nothing reads. That is the arithmetic this release already paid for once, on the sibling branch for #354 |
| ⬜ 7 | `survivors.md`'s first quote stands in four places in the file it anchors into, one of them a different check | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/survivors.md:7` | answered | The judgment is right and only the anchor is weak: the quotation stands in four places in the file it anchors into, one of them a different check. Recorded so the next round does not dig it up again rather than re-cut now, which is a `survivors.md` edit and therefore a fix |
| ❓ 8 | the hand-edit exit the new refusal advertises is true and no case holds it | `skills/code-review/scripts/chain_check.py#written_late` | deferred seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md | seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md as **Q6**, written there with both options and a stated default. The path itself is executed and true — round 2 drove it end to end, exit 1 to exit 0 — so nothing ships unproven; what is undecided is whether a promise printed to a person is a contract a case must hold |

## Paste-ready fixes

```
`evidence-check` at 1164 ok · 0 drifted
```
```
the seven units this branch added each broken alone and each seen red
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_last_rounds_fixes_are_checked.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py -q` | 110 passed in 28.39s — the module that was red since `72c8eb5` is green, and the new prose and the new committed measurement file pass the wrap, identifier and one-word checks |
| `bin/test tests/test_new_says_when_head_is_not_the_target.py tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_a_record_says_why_it_was_written_late.py -q` | 70 passed in 49.51s — round 1 measured 67 here, and the three the fix pass added are the difference |
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_review_axes.py tests/test_a_fix_pass_may_add_a_unit.py tests/test_a_finding_id_is_a_bare_integer.py tests/test_broad_gate_rule.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py -q` | 122 passed in 41.82s — the further modules that read the two documents this range added prose to |
| `git show eb7a56a^:skills/code-review/orchestration.md`, flattened and searched | one occurrence of *spawned before* — the case was genuinely red before the rewording |
| the eleven backwards needles of the three phrase scans, over the flattened text of all four carriers at HEAD | no hits — nothing else this branch added to those documents is within reach |
| `cmp` and `shasum -a 256` between the rescued `phases/phase-1-measurement.txt` and the measurement's output in the session scratchpad | exit 0, digests equal — byte-identical |
| the rescued file's own counts | 40 record entries, 40 `Target SHA` lines, 40 *seen on* lines, header 310 / 158 / 152 / 112 / 40, the two hand-opened records at lines 121 and 115 |
| `git for-each-ref 'refs/remotes/pull/*'`, `git for-each-ref refs/remotes/pull`, `git for-each-ref 'refs/remotes/pull/*/head'` | 0, 138, 138 — the pattern in round 1's grounds is one path component short, exactly as the records now say |
| `git merge-base --is-ancestor a0f0e9a refs/remotes/pull/364/head` | exit 0 — the adding commit `phase-1.md` names first is reachable in this clone |
| the measurement's population re-enumerated by its own rule | 167 refs have a merge-base with `main`; 102 of them add a file under `seal/specs` — `phase-1.md`'s figure |
| probe: `new` with HEAD detached one commit behind the reviewed commit | the BEHIND line verbatim, both commits named, neither false reading, exit 0, record written |
| probe: `new` with HEAD on a branch that diverged sideways | *1 commit stands between them* with the listing and both readings — the new branch does not reach the state it must not |
| probe: `new` with HEAD one commit ahead | *1 commit stands between them* — the singular verb, in the commonest real case |
| probe: the late record refused, the `Written late` row then added by hand and committed, the check re-run | exit 1 then exit 0, the notice quoting the reason — the exit the new refusal advertises is real |
| mutation, copied tree at `80040fe`: `if not late` → `if late` in `written_late` | 16 failed, 46 passed — killed |
| mutation: the appended fourth-exit text removed from the refusal | 1 failed, 50 passed — `test_the_failure_names_the_fourth_exit` alone |
| mutation: the BEHIND branch removed from `head_moved_line` | 1 failed, 7 passed — `test_a_tree_behind_the_reviewed_commit_gets_neither_false_reading` alone |
| mutation: the verb arm reverted as well | 2 failed, 6 passed — the second is `test_one_commit_between_reads_as_one_commit` |
| `bin/survivor-check --range b88a0b2..80040fe`, with and without the exemption file | exit 0 both ways — 14 sentences removed, no removed wording still standing |
| `bin/survivor-check --range c7cc842...HEAD --exempt seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/survivors.md` | exit 0 — 36 sentences removed, none standing, which is what `overview.md` claims |
| `bin/survivor-check --range b88a0b2..1468e48` | exit 1, two places — `chain_check.py:2789` and `:2911`, the two rows `survivors.md` records |
| `bin/evidence-check .` | exit 0 — 1164 ok · 0 drifted · 0 broken · 0 external · 0 old-format, over `seal/ledger.md` at 1148 and the fragment at 16 |
| `bin/unverified-check seal/specs/` | exit 0 — this work item has 1 open row, the broad gate, with the orchestrator named as its answerer |
| `git status --porcelain`, `git worktree list` | tree clean at `3db3a3a`; no worktree or branch left by this round. Every probe file, the copied tree the mutations ran in, and the bytecode they cached are deleted |
| the full suite, the repository-wide lint, the typecheck | **not yet — not run, and not this round's** (`agent-contract` §2). It is the sealer's, and with nothing open it has now come due: what comes next is that agent's spawn, not a run assembled here |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/chain_check.py:2585` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1548` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1556` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:29` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/scripts/chain_check.py:2537` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/code-review/orchestration.md:415` | round 1's ❓ 6 — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `new --target <a revision that is not a full SHA>` writes the revision verbatim into `Target SHA` | already deferred by the branch: `overview.md` §Not done, the docstring of `test_a_target_given_as_a_revision_is_named_by_its_sha`, and an issue on the tracker. Round 1 recorded it too | the repository owner — carried forward so a later round does not re-open it as new |
| nothing counts how often `--written-late` is reached for | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md` Q5, added by the fix pass with both options and a stated answer | the repository owner — round 1's ❓ 6, and the row reached its durable home |
