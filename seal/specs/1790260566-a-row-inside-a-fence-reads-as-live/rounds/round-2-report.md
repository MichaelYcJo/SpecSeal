# 1790260566-a-row-inside-a-fence-reads-as-live — round 2 report

Target SHA `32fb90bd`. This is the verifying round. Its target is round 1's fix
diff, `70fe19ca..91fcb4e5` (`fd16c522` and `91fcb4e5`), and the merge of
`release/v0.15.3` at `32fb90bd`, which brought in #588 and #587. I worked in a
`git clone --no-local` of the worktree at the target SHA. I wrote nothing in
the worktree except this file.

## How the pieces relate

1. Round 1's three yellows are closed. Both code fixes do what the paste-ready
   fixes said. Both new cases fail against the code before the fix and pass
   after it. The narrowed sentences no longer claim that every reader asks the
   shared rule.
2. One half of the `fenced_after` fix has no case. If the backtick-info opener
   rule is removed, the whole module still passes (⬜ 2). The behaviour is
   correct, so nothing ships wrong. A case is proposed below.
3. The merge composes. The release side changed only `settle.py#first_cell`.
   This branch changed only docstrings in `settle.py`. The settle module
   passes on the merged tree. The `0.15.1.md` row hunk was resolved the way
   the commit message says, and both sides' notes are kept on D1 and E1. One
   sentence in that merge note describes the units wrongly (⬜ 3, paperwork).
4. `repoint` still has a comment that names the inner function the fix
   removed (⬜ 1).

## Round 1's verdicts, one by one

**🟡 1, `round_record.py#fenced_after`: closed.** At
`skills/code-review/scripts/round_record.py:1324` the opener pattern now
captures the info string. A backtick run whose info holds a backtick opens
nothing (`:1326`). A closer must be empty after its run (`:1335`). This is
round 1's paste-ready fix byte for byte. The opener still accepts any
indentation, and the docstring at `skills/verify/scripts/unverified_check.py:257`
states that on purpose. The new case
`test_a_fence_line_with_an_info_string_inside_a_fix_does_not_end_it` fails with
`fd16c522^`'s `round_record.py` restored: the record held
`` ```text\na\n```text\n``` `` and the prose. It passes at the target.
Executed.

**🟡 2, `root-migrate.py#repoint`: closed.** At `hooks/root-migrate.py:419-431`
anchors are found in `ec.unquoted(text)` and spliced from `text`. I read
`evidence_check.py#unquoted` (`:223`). It keeps every character offset, because
it blanks each character of a quoted line to one space and keeps `\r\n`. A
match cannot cross a blanked line, because no group of `ANCHOR_RE` matches a
newline. So `text[m.start() + len(path) : m.end()]` is the same span that the
old `m.group(0)[len(path):]` was. This is the same splice `reverify` makes at
`:1747-1750`. The new case `test_a_fenced_example_row_is_left_byte_for_byte`
fails with `fd16c522^`'s `root-migrate.py` restored, where the fenced
`.specseal/` path became `seal/`. It passes at the target. Executed.

**🟡 3, the completeness sentences: closed.** All six carriers are narrowed:
`unverified_check.py`'s `FENCE_RE` comment and `fence_opener` docstring,
`skills/evidence-check/SKILL.md` at `:295` and `:427`, `evidence_check.py`'s
section comment at `:142`, and `settle.py#coordinates`. The docstring now lists
`fenced_after` and `repoint`, and it names `payload_meter.py#FENCE`,
`fold_ledger.py#demote`, `close_issues_on_release.py` and
`correction_check.py#rows` as outside the rule. All four exist in the tree
(`:124`, `:245`, `:121` and `:356`). I searched the tree for the old
phrasings: *every fence walk*, *every reader … shares*, *one fence rule*. The
hits that remain are either scoped (ledger row P1-1 says *every fence walk in
`unverified_check.py`*) or about the config reader's own rule
(`docs/the-broad-gate.md:74`, `hooks/config.py:159`,
`skills/verify/scripts/broad_gate.py:772`). None claims the whole plugin. Read.

**⬜ 4 and ⬜ 5: deferred to #584 in round 1.** Nothing in the fix diff touches
`correction_check.py#rows` or `fold_ledger.py#demote`. The docstring now names
both as #584's.

**⬜ 6: still answered.** A search of `seal/specs/` for the empty-comment shape
`&lt;!-->` finds no instance. The fix diff changes one comment in
`evidence_check.py` and no code.

**⬜ 7: still answered.** `quoted_lines` and `unquoted` are unchanged by the fix
diff, and both still split the same way.

**⬜ 8: closed by the correction.** `phases/phase-1.md` now names both
directions. The sentence *an unclosed result is refused by `round_record.py`
with a named message* has its message at
`skills/code-review/scripts/round_record.py:457` (`NEVER_CLOSED`) and at `:465`
(`NEVER_CLOSED_VERBATIM`). Read.

## The two new cases, judged as code

Both cases are correct and each pins what its name says. I showed each one red
against the code before the fix. See the probes table.

The `fenced_after` case covers the closer half of the fix only. I removed each
half by mutation and ran the whole module. With the closer half removed, the
new case alone fails (1 failed, 128 passed). With the backtick-info opener
half removed, all 129 pass. Ledger row R1-1 in
`seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md` claims both
halves, and this case is the only one it cites. The code is correct, so this is
⬜ 2 and not a defect. The case under *Regression tests to plant* fails with
the opener half removed and passes at the target. I ran it from a probe and
then removed it.

## The merge at 32fb90bd

**Do A's `first_cell` and this branch's `settle.py` changes compose? Yes.**
Against the first parent, the merge changes only `CONTAINER_RE` and
`first_cell` (`skills/settle/scripts/settle.py:450-468`). Between the merge
base `c52e8350` and the first parent, this branch changed only docstrings in
`settle.py`: those of `open_rows`, `coordinates` and `anchored_rows`. The two
sides touch no common line. `anchored_rows` calls `first_cell` at `:531` for
every line, and that includes a fenced one. A container prefix in front of a
fenced example row is now stripped the same way as in front of a live row,
which is the behaviour #530 intended. `tests/test_settle_reads_before_it_removes.py`
passes on the merged tree. Executed.

**Is the notes union kept? Yes.** I compared every row in the eleven ledger
files the merge changed against the first parent, across the base, both
parents and the merge.

- **D1 and E1 in `seal/releases/0.15.1.md`.** Both sides edited these rows. The
  merge keeps every note from the release side (the #501 and #569 re-reads) and
  every note from this branch (the #487 phase 3 re-read). It adds one re-read
  note of its own for the merge. Each anchor's hash belongs to the side that
  edited that unit. This branch alone edited `CONTRIBUTING.md#"## House rules"`,
  and the merge carries `a0c75785` from this branch. The release side alone
  edited `docs/the-evidence-ledger.md#"## A row is a content anchor, and it names no commit"`
  (its hunk is at `:71`; this branch's hunk is at `:300`, in *The fold*). The
  merge carries `c69d1fb2` from the release side.
- **S1 in `0.15.1.md`.** This branch added a re-read note. The release side
  REMOVED the row because its anchors left `tests/`. The merge keeps it
  removed, which is what `CLAUDE.md` asks for a row whose anchor a change
  removes. The claim it held (no `docs/` file over the ceiling) is now F6 in
  #587's fragment, and `bin/fold-check` passes on the merged tree
  (`docs/the-evidence-ledger.md` is 365 lines).
- **S2, S3 and E2.** These are the same as the release side, as the commit
  message says. R4 in `0.15.1.md` and F2 in `0.8.2.md` carry this branch's
  re-stamps, and the release side did not touch those units.
- **G5 in `0.8.2.md` and S4 in `0.9.2.md`.** These differ between the base and
  the release side only. #588 changed them before the merge, and the merge did
  not.

`bin/correction-check --range c52e8350..32fb90bd` reports no correction marker
dropped at the one merge. `bin/evidence-check .` reports 2,157 ok, 0 drifted,
0 broken. Executed.

The merge's own note on D1 and E1 says *the unit carries both sides' edits,
each note above describes one, and they touch different sentences*. No single
unit carries both sides' edits. Each side edited a different anchored unit. It
is the row that carries both. The claim holds and the hashes are right, so
this is a paperwork correction (⬜ 3).

## New findings

**⬜ 1: `repoint`'s line-count comment names a function that no longer
exists.** `hooks/root-migrate.py:434-435` says *a mismatch here would be a
defect in `follow`*. `fd16c522` removed the inner function `follow` and put
the splice loop in its place. The next reader who looks for `follow` finds
nothing. Suggested wording: *a defect in the splice above*. Read.

**⬜ 2: the opener half of `fenced_after`'s fix has no case.** Described above.
The location is the new case at `tests/test_the_record_is_generated.py:1995`,
which is a unit round 1's fix created. Executed.

**⬜ 3: the merge note on D1 and E1 in `seal/releases/0.15.1.md` names the
wrong unit.** This is a correction to paperwork. Suggested wording: *the row
carries both sides' edits, one in each anchored unit*. Read.

## Regression tests to plant

Destination: `tests/test_the_record_is_generated.py`, next to
`test_a_fence_line_with_an_info_string_inside_a_fix_does_not_end_it`. This is
for ⬜ 2. It fails with the opener half removed and passes at `32fb90bd`
(executed from a probe that has since been removed).

```python
def test_a_backtick_line_whose_info_holds_a_backtick_opens_no_fix(repo):
    """Round 2's ⬜ 2 of work item 1790260566: the opener half of round 1's
    fix. CommonMark 4.5 says a backtick run whose info string holds a
    backtick opens no fence, so the prose after it is not a fix."""
    declared(repo)
    fixes = "```x`\nprose between\n\n```text\na\n```\n"
    code, out, text = generate(repo, report_text=report(fixes=fixes))
    assert code == 0, out
    section = paste_ready(text)
    assert "```text\na\n```" in section, text
    assert "prose between" not in section, text
```

## Facts for the evidence ledger

- If the case above is planted, R1-1 in
  `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md` can cite it
  beside the closer case. Its Executed cell would then cover the opener half
  it already claims.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — the record generator's fence walk takes the closer and backtick-info rules | `skills/code-review/scripts/round_record.py:1324` | confirmed | read; the new case red with `fd16c522^`'s file restored and green at the target, executed |
| 🟢 | round 1's finding 2 is closed — the re-point matches in `unquoted` and splices from the original | `hooks/root-migrate.py:419` | confirmed | read, and offsets hold (`unquoted` keeps each character's position); the new case red with `fd16c522^`'s file restored and green at the target, executed |
| 🟢 | round 1's finding 3 is closed — six carriers narrowed and the readers outside the rule named | `skills/verify/scripts/unverified_check.py:238` | confirmed | read; a tree search for the old phrasings finds only scoped or config-reader sentences; the named readers exist |
| carried | The correction check reads a fenced example row as a row | `skills/evidence-check/scripts/correction_check.py:356` | deferred #584 | already deferred in round 1; untouched by the fix diff, and now named in `fence_opener`'s docstring |
| carried | The release fold's demote walk keeps its own fence rule | `.github/scripts/fold_ledger.py:245` | deferred #584 | already deferred in round 1; untouched by the fix diff, and now named in `fence_opener`'s docstring |
| 🟢 | round 1's ⬜ 6 still holds — no empty comment of that shape in the tree | `skills/evidence-check/scripts/evidence_check.py:2242` | confirmed | executed: a search of `seal/specs/` finds no instance; the fix diff changes no code in that file |
| 🟢 | round 1's ⬜ 7 still holds — both ledger walks split the same way | `skills/evidence-check/scripts/evidence_check.py:223` | confirmed | read; `quoted_lines` and `unquoted` are unchanged by the fix diff |
| 🟢 | round 1's ⬜ 8 is closed — phase 1's failure direction names both directions | `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/phases/phase-1.md` | confirmed | read; the refusal it cites is `NEVER_CLOSED` at `round_record.py:457` |
| 🟢 | The merge composes `first_cell`'s container class with this branch's `settle.py` docstrings | `skills/settle/scripts/settle.py:450` | confirmed | read: no common line; executed: the settle module passes on the merged tree |
| 🟢 | The merge keeps both sides' notes on D1 and E1, and each anchor's hash is the editing side's | `seal/releases/0.15.1.md` | confirmed | executed: a row-by-row compare over base, both parents and merge; `correction-check` over the merge reports no dropped marker; `evidence-check` 0 drifted |
| ⬜ 1 | `repoint`'s line-count comment names `follow`, which the fix removed | `hooks/root-migrate.py:435` | open | read; a stale name in a comment and no behaviour change |
| ⬜ 2 | The opener half of `fenced_after`'s fix has no case; R1-1 claims it | `tests/test_the_record_is_generated.py:1995` | open | executed: with that half removed, 129 of 129 pass; the proposed case is red there and green at the target |
| ⬜ 3 | The merge note on D1 and E1 says one unit carries both sides' edits; each unit carries one side's edit | `seal/releases/0.15.1.md` | open | a correction to paperwork; read: this branch's hunk is in `CONTRIBUTING.md`, and the release side's is at `docs/the-evidence-ledger.md:71` |
| ❓ | Behaviour on Linux and Windows | the fix diff | ❓ out of verified scope | macOS only here; CI's matrix answers it at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `test_the_record_is_generated`, `test_the_root_migrates_itself`, `test_settle_reads_before_it_removes`, `test_a_merge_cannot_silently_drop_a_correction`, `test_unverified_rows_close` at `32fb90bd` | 504 passed, exit 0 |
| `bin/test tests/test_release_hygiene.py` at `32fb90bd` (the #588 fragment-row rules, over this branch's new R1-1 and R1-2) | 51 passed, exit 0 |
| The two new cases with `fd16c522^`'s `round_record.py` and `root-migrate.py` restored in the clone | both failed, exit 1: prose copied and a fix line lost; the fenced `.specseal/` path rewritten to `seal/`. The files were restored and the status is clean |
| `fenced_after` mutated in the clone, each half removed in turn, then the whole record-generator module run | closer half off: 1 failed (the new case), 128 passed; opener half off: 129 passed |
| The proposed opener-half case, appended to the module from a probe | green at the target, red with the opener half off; appended text and mutation removed, status clean |
| A row-by-row compare of the eleven ledger files the merge changed, over `c52e8350`, both parents and `32fb90bd` | no note lost at the merge; D1 and E1 hashes are each the editing side's; S1 removed on the release side and kept removed |
| `bin/correction-check --range c52e8350..32fb90bd` | exit 0; 1 merge examined, no correction marker dropped |
| `bin/evidence-check .` at `32fb90bd` | exit 0; 2,157 ok, 0 drifted, 0 broken; records arm 474 names, 0 refused |
| `bin/fold-check` at `32fb90bd` | exit 0; 14 documents held to 1,000 lines, 0 listed over it |
| The broad gate (full suite, lint, typecheck) | not yet: nobody has run it. It belongs to the sealer, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Nothing new is deferred. ⬜ 4 and ⬜ 5 were already deferred to #584 in round 1.

Needs a fix: no

Loses a record or crashes: no

This round leaves nothing that needs a fix. The sealer's broad run is now due.
The three ⬜ items are the smith's to take or to answer with grounds.

## Proof block

Files opened: `skills/code-review/scripts/round_record.py` (`fenced_after`,
`NEVER_CLOSED`), `hooks/root-migrate.py` (`repoint`),
`skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE`, `fence_rule`,
`quoted_lines`, `unquoted`, `reverify`), `skills/settle/scripts/settle.py`
(`first_cell`, `anchored_rows`), `skills/verify/scripts/unverified_check.py`
(the fix hunks), `skills/evidence-check/SKILL.md` (the fix hunks),
`tests/test_the_record_is_generated.py` and
`tests/test_the_root_migrates_itself.py` (the new cases),
`seal/releases/0.15.1.md` (D1, E1, S1),
`seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md`,
`seal/ledger/1790260563-the-fold-checks-run-only-as-this-repositorys-tests.md`
(F6), `docs/the-evidence-ledger.md` (each side's hunks),
`docs/the-broad-gate.md:72-78`, `skills/verify/scripts/broad_gate.py:768-776`,
`seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/phases/phase-1.md`
(the correction), `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/changelog.md`,
`rounds/round-1.md`, `rounds/round-1-report.md` (the opening), and the merge
commit message.
