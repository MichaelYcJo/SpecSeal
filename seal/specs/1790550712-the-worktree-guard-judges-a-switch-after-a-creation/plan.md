# Implementation Plan: the worktree guard judges a switch written after a creation (#620, #624, #243)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

`main`'s segment walk stops classifying once a verdict is set, unless the
segment creates a worktree. So a switch written after a creation is never
judged. The fix changes the walk: it takes the first switch-kind segment as
`reason` and the first creation as `creation_at`, in whichever order they are
written. A command carrying both then goes through the switch ladder with
the creation hooked in where the switch-then-create shape already has it, and
the verdict no longer depends on the order. `spec.md` decision 2 shows that
this ladder is never weaker than either direction alone.

Alongside that come three sentences and one reader condition from #624, and
the three counts #243 disputes. The counts are replaced by the class each
boundary really is, with a committed case beside each.

## Technical context

Code this builds on, by content anchor:

- `hooks/worktree-guard.py#main`. Three parts matter:
  - The walk is the loop over `walk_command(command, cwd)`. Its skip is
    `if reason is not None and not creates: continue`, and its early break is
    `if reason is not None and creation_at is not None: break`.
  - `if reason == "worktree-add":` is the branch that sends a create-first
    command to `judge_creation` and exits. It stays, and it is now reached only
    when no switch-kind segment exists.
  - The switch ladder: the ACTIVE row, `choose` rows 1-b and 2 with
    `before_ask=judge_the_creation`, the `if creation_at: judge_creation(...)`
    call, row 3 (tracked changes) and row 4 (silent).
- `hooks/worktree-guard.py#judgeable` and `#classify`. These are unchanged.
  `classify` runs `git rev-parse` for a `checkout`, so classifying segments
  after a creation costs one subprocess per `checkout` segment until a
  switch-kind verdict is found. The comment on the skip names this cost, and
  it is accepted.
- `hooks/worktree-guard.py#guard_worktree_creation`. The `if user_ok:` row's
  opening sentence (#624.3). Consent answers `silent` for any compound, so
  `allow` is unreachable once a switch segment exists.
- `hooks/worktree-guard.py#only_creates_a_worktree`. Read, not edited. It is
  the grounds for "a command carrying a switch never gets `allow`".
- `hooks/worktree_consent.py#automation_answered`. The
  `entry.get("isSidechain") is True` check (#624.1).
- `hooks/worktree_consent.py#creation_directory`. Its docstring describes the
  guard's walk (see §*Enumerated copies*). The writer still records the first
  creation only, so the guard's `creation_at` and the writer agree.
- Test helpers: `tests/test_the_guard_asks_once_per_session.py#decide`
  (`sessions=`, `session_id=`, `cwd=`), `#grant`, `#ask_entries`,
  `#write_transcript`, the `projects` fixture, and the `ACTIVE`/`IDLE`
  constants. `tests/test_worktree_guard.py#_reasons` drives the two reason
  tests. `tests/conftest.py` pins `SPECSEAL_LANG=en`.
- Paste-ready code for #624.1 and #624.3 is in
  `seal/specs/1790381327-an-automation-run-creates-its-worktrees-without-asking/rounds/round-2-report.md`
  §*Paste-ready fixes*. It is still in the tree, not retired. #624.2 has no
  paste-ready code. `spec.md` decision 6 gives its shape.
- The three #243 findings and round 3's own sweep are in the retired report,
  read through history:
  `git show f51e634^:seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/rounds/round-3-report.md`.
  Its paste-ready doc text is a starting point only. Decision 9 refuses its
  replacement figures.

The walk, as a shape and not as code:

```
switch_reason, creation_at, eff_cwd = None, None, cwd
for tokens, wheres in walk_command(command, cwd):
    creates = cmdline.adds_a_worktree(tokens)
    if creates and creation_at is not None:   continue   # first creation only, as the writer
    if not creates and switch_reason is not None: continue   # first switch only, as today
    ...classify over wheres; a creation fills creation_at, anything else fills switch_reason/eff_cwd...
    if switch_reason and creation_at: break
reason = switch_reason or ("worktree-add" if creation_at else None)
eff_cwd = the switch's target when there is one, else the creation's
```

Constraints the build must respect:

- `CONTRIBUTING.md` §*What a change to a gate must carry*. Every new case must
  be seen red. The PR body carries the two paragraphs below.
- `skills/agent-contract/SKILL.md`: §14, each changed reason is pinned in the
  same commit and in both languages. §15, each new case is shown red, and
  `phases/phase-N.md` says how. §7 and §8, probes are `test_tmp_*`, drive git
  from Python, and leave nothing behind.
- `CLAUDE.md` *a change writes fragments*. New rows go in
  `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md`
  (the `seal/ledger/` directory does not exist yet, and this work creates it).
  The changelog entry goes in this directory's `changelog.md`. Existing rows
  in `seal/releases/*.md` are corrected or re-read in place, which the same
  rule allows.
- `seal/config.md` sets `Document line ceiling` to 1000.
  `docs/worktree-guard-spec.md` is 527 lines, so there is room, but the
  corrected paragraphs should replace text rather than add to it.

**Failure direction, for the PR body.** Every change here blocks more or says
less.
- #620 turns silences and asks into asks and denies, only for commands that
  carry a switch after a creation. It never turns a deny into anything else.
- #624.1 refuses consent for shapes no measured transcript contains.
- #624.2, #624.3 and #243 change text only.
A wrong deny costs a prompt. A wrong allow here is a switch taken out from
under an ACTIVE session, which is the exact case S1 closes.

**Prompt budget, for the PR body.** New stops arrive only for a command that
creates a worktree and then switches, in a tree that is not clean and
single-stream.
- With consent: ACTIVE denies on every attempt. IDLE and detection-unusable
  get one choice deny per session in the switch direction, then an ask per
  attempt. Dirty gets an ask per attempt.
- Without consent: the counts equal today's switch-then-create counts.
A plain `git worktree add`, which is the form an automation run writes, is
unchanged (S4). How often the create-then-switch form occurs is measured by
Q4, and the PR body states that number instead of an estimate.

**What breaks in six months.** The walk now keeps one switch and one creation.
A command switching in two trees, or creating in two clones, is still judged
on the first of each (`questions.md` Q1). A later change that adds a third
kind of verdict to `classify` has to decide where it sits in this walk. The
order-independence case (S2) is what turns red if that is decided wrong.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Send any switch-plus-creation command to the switch ladder, whichever is written first** | The ladder's same-level text precedence (the creation's ask over the dirty-tree ask) carries over to create-first, so the dirty-tree fact is not shown when both ask. That loss already exists and is ratified for switch-first. A `cd` into the new worktree is judged against the session's tree (decision 5) | **chosen**: no new comparison, one precedence table, and order-independence can be pinned |
| In the create-first branch, run the switch ladder only when the creation's verdict is silent | With no consent and an ACTIVE tree, the creation's `ask` exits first. Approving it switches the branch under the ACTIVE session, the same outcome as the bug with one approval added. Not "stricter" | rejected |
| Collect both verdicts (`respond` raises a verdict object under a flag), compare ranks, emit the stricter | A second precedence table beside the ratified one. `choose` writes its budget marker when it denies, so a switch deny computed and then outranked spends a budget whose question nobody saw. Two text-picking rules for one decision would then have to be kept in step | rejected |
| Run the creation ladder, then the switch ladder, for create-first | This is the row above with a different entry order. The creation's `respond` exits the process, so the switch ladder is never reached whenever the creation says anything | rejected |
| Refactor the ladder into a per-tree function and judge every switch and every creation segment | Closes the residue in Q1 too, but it is a restructure of `main` in a patch release whose milestone says no new mechanism. It also moves every line of the ladder, which every existing `main` ledger row anchors on | rejected for this milestone. Q1 holds the default and the filing |
| #243: replace each wrong figure with the corrected one (17 spellings, 690 cells) | The new figures come from probes whose shapes are not in the tree either. Round 3 wrote that the fix *is not complete until the sweep that produced the three numbers is reproducible from the tree*. The same miscount one level down is what #243 already is | rejected |
| **#243: state each boundary as the class it is, and cite the committed case that enforces it** | A reader loses a headline number. The case name tells them where to get it | **chosen** |
| #624.2: delete the *Single-stream tree* lead outright | The person loses why the switch itself is not being questioned, which is the half of the sentence that is true in all three states | rejected. The lead is conditioned on what was measured (decision 6) |

## Enumerated copies

Every copy of each sentence this work corrects. A `git grep` for each old
phrase closes S12. The grep includes the outcome words (`allow`, `ask`,
`deny`, `silent`) next to the verb, and hits in round records, released
`CHANGELOG.md` sections, and `phases/`/`rounds/` of other work items are
records of the past and are left alone.

**The walk "stops at the first verdict" / "classifies the FIRST segment" (#620):**

1. `hooks/worktree-guard.py#main`: the comment above `creation_at = None`
   (*`reason` still takes the FIRST segment that classifies*), the comment on
   the skip (*this walk used to stop at the first verdict*), and the skip
   itself.
2. `hooks/worktree-guard.py#judge_creation` docstring: *`main` classifies the
   FIRST segment it can read*.
3. `hooks/worktree_consent.py#creation_directory` docstring: *The guard's own
   PreToolUse walk stops at the first verdict*.
4. `tests/test_the_guard_asks_once_per_session.py`: the section comment above
   `test_a_creation_behind_another_verdict_is_still_judged` (*`main` classifies
   the FIRST segment it can read*), and the docstring of
   `test_a_creation_anywhere_in_the_command_records` (*stops at the first
   verdict*).
5. `docs/worktree-guard-spec.md` §*Creation consent*: *A creation the guard
   never judged used to mint the record*. Its second sentence is present tense
   (*The guard's `PreToolUse` walk classifies the first segment*) and becomes
   past tense. *So the creation is judged between the ladder's two halves*
   gains *whichever of the two is written first*. §A gains one line under its
   table pointing a command that also creates to that section.
6. `seal/releases/0.15.5.md` row A4. Its notes column says *A switch written
   after a creation in one command is never judged when consent is present …
   is #620*. The claim stays true. The anchor `main` drifts, so the row is
   re-read with a dated note saying this work closed #620.

**`isSidechain` (#624.1):**

7. `hooks/worktree_consent.py#automation_answered`: the check and the comment
   above it, and condition 2 of the docstring, which gains the term so the
   docstring and the document state the same four conditions.
8. `docs/worktree-guard-spec.md` §*What exactly is read*, condition 2: *not
   marked `isSidechain: true`* becomes *carrying `isSidechain: false`*.
9. `seal/releases/0.15.5.md` row A1: *not marked `isSidechain: true`*. This is
   corrected in place with a `Corrected 2026-09-…` note.
10. `tests/test_the_guard_asks_once_per_session.py#test_a_sidechain_entry_is_not_consent`:
    docstring and body (the round 2 report's version).

**Row 3's *Single-stream tree* (#624.2):**

11. `hooks/worktree-guard.py#main`, row 3, the English and the Korean string.
12. `docs/worktree-guard-spec.md` §A, the *single stream, tracked changes
    present* row. It also covers only-IDLE and detection-unusable under
    `[shared-tree-ok]`, and the note under the table says so.

**The `[worktree-ok]` opening (#624.3):**

13. `hooks/worktree-guard.py#guard_worktree_creation`, the `if user_ok:` row,
    both languages.
14. `tests/test_worktree_guard.py#test_the_two_reworded_reasons_are_pinned_in_both_languages`
    and `#test_the_token_rows_count_sentence_is_said_only_where_a_count_was_taken`,
    both languages.

**The three counts (#243):**

15. `docs/worktree-guard-spec.md` §*Creation consent*, *The boundary the code
    implements* (*32 command-word shapes, exactly five*; *falls to `ask`*).
16. `docs/worktree-guard-spec.md` §*Creation consent*, *The property, measured
    rather than the shapes* (*1260 … 230 … 64*).
17. `seal/releases/0.9.1.md`, the row *The command word must be the WORD
    `git`* (*exactly five are vouched for*). Corrected in place: the class,
    not the count. Its *fall short of `allow`* is true and stays.
18. `seal/releases/0.9.1.md`, the row *Whatever the writer would record for …*
    (*1260 … 230 … 64*). Corrected in place, citing the committed case.
19. `tests/test_the_guard_asks_once_per_session.py#test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned`
    docstring: *"was true of two of them"* becomes *one*. This is the
    miscount round 3 of 1788817291 found in that item's `spec.md` (finding 4),
    and this test-docstring copy of it was never corrected.

Read and found true, no edit: `hooks/worktree-guard.py#only_creates_a_worktree`'s
docstring (it names spellings without a count, and *falling to `ask`* is said
of `/usr/bin/git`, a path, which does ask); `README.md` and `README.ko.md`
worktree-guard rows; `docs/worktree-guard-spec.md` §*Choice sites*.

## Ledger rows this work re-reads

Each anchor below is a unit this work edits, so the rows drift.
`evidence-check --reverify` on the touched release files names every row,
including any this list missed. Each row is re-read against the edit and
re-stamped with a dated note, or corrected in place where the edit made it
false.

| Anchor | Rows |
|---|---|
| `hooks/worktree-guard.py#main@cf55137d` | `seal/releases/0.15.5.md` A4, A5 · `seal/releases/0.9.1.md` *Whatever the writer would record for …* (also corrected, item 18) |
| `hooks/worktree-guard.py#guard_worktree_creation@26618e2e` | `seal/releases/0.15.5.md` A3 · `seal/releases/0.9.1.md` *A session that already created a worktree …*, *The first creation of a session is unchanged* · `seal/releases/0.9.4.md` S3, S4 |
| `hooks/worktree-guard.py#judge_creation@bc8a0654` | `seal/releases/0.9.1.md` *A creation anywhere in the command is judged before it runs* |
| `hooks/worktree_consent.py#automation_answered@415ab3a7` | `seal/releases/0.15.5.md` A1 (also corrected, item 9) |
| `tests/test_the_guard_asks_once_per_session.py#test_a_sidechain_entry_is_not_consent@d996dc32` | `seal/releases/0.15.5.md` A1 |
| `tests/test_worktree_guard.py#test_the_two_reworded_reasons_are_pinned_in_both_languages@44ff0fa3` | `seal/releases/0.15.5.md` A5 |

`hooks/worktree-guard.py#only_creates_a_worktree@279e226e` is not edited. The
row citing it is corrected for its claim (item 17), and its anchor does not
drift.

Builder's note, 2026-09-28, phase 4. Every stamp above was the base's
(`afcb3f7`) when this plan was approved, and each is re-stamped here to the
state its rows were re-read against, because `evidence-check --strict` grades a
drifted stamp in a live work item's record like a drifted ledger row. The
sentence above is no longer true: phase 3 corrected `only_creates_a_worktree`'s
docstring (*falling to `ask`*, which measured false), so its anchor drifted and
its three rows (`seal/releases/0.9.1.md` items 17 and the row above it,
`seal/releases/0.9.4.md` S3) were re-read with the others.

New rows, in the fragment:
- W1: order does not decide (`main`, the S2 case).
- W2: never weaker than either direction, and no `allow` for a command with
  a switch (S3).
- W3: sidechain (S7).
- W4: row 3 names what was measured (S8).
- W5: the `[worktree-ok]` opening (S9).
- W6: the command-word class, and the `ask`/silent split (S10).
- W7: a `cd` into the new worktree falls back to the session's tree (S6).

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #620. The walk change in `main`; copies 1–6; the §A pointer and the §*Creation consent* edits; decision 5's *Known limits* line; cases S1, S1b, S2, S3, S6 and the S5 extension of the writer-record sweep; S4 as a case or an executed table | each new case run against the base `hooks/` (copied to a scratch dir, per contract §7) and seen red, then green. `bin/test tests/test_the_guard_asks_once_per_session.py tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py -q` | e5af3c1 |
| 2 | #624. `is not False` with copies 7–10; row 3's conditioned lead with copies 11–12; the `[worktree-ok]` opening with copies 13–14; cases S7–S9 in both languages | S7 red with `is True` restored; S8 red at the base; S9 red with the old wording. The same narrow modules | d66b9f8 |
| 3 | #243. A `test_tmp_*` probe re-derives, by running, the verdict of each command-word shape (at least round 3's 55) and the heredoc known limit (Q2, Q3), then is deleted. A committed case pins one or more members of each verdict group (S10). Paragraphs 15–16 are rewritten as classes citing their cases (S11). Rows 17–18 and docstring 19 are corrected | S10 red with one shape moved to the wrong group. The probe's table goes in `phases/phase-3.md` as executed. The same narrow modules | 31fb7a3 |
| 4 | Records. The ledger fragment's W1–W7 rows; the drifted rows re-read and re-stamped; `changelog.md`; the S12 grep sweep with its output; Q4's count for the PR body | `bin/evidence-check --strict` on the fragment and on `seal/releases/0.9.1.md`, `0.9.4.md` and `0.15.5.md` exits 0. The S12 greps return only records of the past | d7a8f14 |

The broad gate (full suite, repository-wide lint, typecheck) belongs to none
of these phases. It is the sealer's, once, after the review rounds settle.

## Operational impact

None. There are no migrations, environment variables, dependencies or file
formats. The consent reader accepts one shape fewer, and no measured
transcript carries that shape.
