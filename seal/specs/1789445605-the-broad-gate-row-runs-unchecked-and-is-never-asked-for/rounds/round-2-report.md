# Round 2 — the verifying round, over round 1's fixes (#402, #401)

Target: the diff `96c88c9f..HEAD`, three commits. HEAD is `6fc9bb71` on
`fix/401-402-the-broad-gate-row-runs-unchecked-and-is-never-asked-for`,
confirmed at the start of the round and unmoved at the end; the working tree
was clean. Round 1's record and report are both in `rounds/`, and this round
answers the nine verdicts they closed.

## What this round found, in causal order

**All nine of round 1's findings are closed, and I watched each repair fail
before I called it one.** Thirteen mutations, one at a time, each restored
before the next: every case round 1 named as unfalsifiable is now red when the
sentence it pins is changed. That is the substance of the round and it is
below under *What I confirmed rather than doubted*.

Two things opened, and they are one cause between them. The fix pass repaired
round 1's 🟡 4 — the removed design still asserted in the template paragraph —
and pinned the repair with a case that reads the whole `## Broad gate` section
rather than the paragraph. That is round 1's 🟡 7 shape, which the same fix
pass repaired correctly one module over.

1. **The case planted for 🟡 4 cannot lose the sentence it is named for.**
   Deleting the entire clause the fix added leaves all 17 cases in the module
   green.
2. **The `&`'s platform hedge reached three places and not the fourth**, which
   is the document that owns the list — and one of the two sentences that
   still state `/bin/sh` semantics as universal is a sentence this fix pass
   wrote.

The corrections are under ⬜ at the bottom and `Needs a fix` does not count
them.

---

## 🟡 1 · The case planted for round 1's 🟡 4 passes with the clause deleted

`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:275`
(`test_the_paragraph_above_the_lists_no_longer_says_it_names_what_to_write`) ·
`templates/config.md:173-180`

The case takes `flat(broad_gate_section())` — the whole `## Broad gate`
section, `templates/config.md:161` to the end of the file — and makes three
assertions against it. Two are sound. The third is this one:

```python
    assert "#401" in section_text, (
        "the paragraph asserts the change without the report behind it"
    )
```

`#401` stands twice inside that section. Once in the rewritten paragraph at
`:177`, and once at `:241` in the criterion's closing prose, where it has
stood since before this branch: *were written nowhere until #401*. So the
needle cannot go missing by anything happening to the paragraph.

Executed, two mutations, each restored before the next:

| Mutation | Result |
|---|---|
| `#401` replaced with `the report` in the rewritten paragraph alone | 17 passed |
| The whole new clause deleted — *It does **not** name a command to write: doing that asked the one party that may not choose one, which is what #401 reported.* | 17 passed |

The second is the one that matters. The sentence this fix pass added to close
round 1's 🟡 4 can be taken back out in full and the case named for it stays
green, because the surviving assertion `"names whose the row is and where it
is answered" in section_text` matches the sentence *before* it, which the
deletion leaves standing.

**Why this one rather than a style note.** The release's whole subject is a
check that could not fail, and round 1 opened four cases of this exact shape.
The fix pass repaired three of them in `tests/test_first_setup_asks_once.py`
with the `paragraph()` helper that module already ships, and then wrote a
fourth into the sibling module. `agent-contract` §12 is the grounds: the
finding named an instance and the fix is owed to the class. The fix pass's own
record describes these cases as reading *the header and the section rather
than the file* — the section is the half that is not a bound.

The sibling module already has the pattern to copy: `refusal_bullet()` at
`:349` slices one paragraph out of `skills/config/SKILL.md` and stops at the
blank line. The paste-ready fix below does the same against the template.

## 🟡 2 · The `&`'s platform hedge reached the message, the overview and the pull request, and not the list that owns it

`templates/config.md:206` (the refused table) · `templates/config.md:225` (the
allowed table, added by this fix pass)

Round 1's 🟡 5 was that the `&` refusal states `/bin/sh` semantics as every
platform's. The fix closed it in three places, and I read all three:
`broad_gate.py#not_as_written` now names `cmd.exe` beside `/bin/sh`,
`overview.md`'s *Not verified* row records the claim as unmeasured with the
`windows-latest` job named, and pull request #412 gained a *Platform* section
that says the same thing.

`templates/config.md` §*What is refused, and what stays allowed* is the one
home for both lists, and it is the document the message sends a reader to. It
still says, at `:206`:

```
| a trailing `&` that is not part of `&&` | `bin/test -q &` | backgrounds the
whole line, so the shell answers 0 before any check has finished |
```

*the shell* is `/bin/sh`. Under `cmd.exe` the same value does not background;
it separates two commands, so the exit code read is the second one's. The
refusal is still right there, for a different reason, which is exactly what
the message now says and this cell does not.

The second instance is new in this diff. The allowed row the fix pass added at
`:225` reads *the command before it is backgrounded and its status
discarded … it may still be running when the gate stamps*. On Windows nothing
is backgrounded and nothing is still running, so the cost a reader is being
asked to accept is not the cost they would pay. A sentence written into a
shipped document in the same commit that hedged the same claim elsewhere is
the class left half-enumerated.

**What separates this from 🟡 1.** This one can be answered with grounds — the
whole section is written in `/bin/sh` terms and the hedge could reasonably be
said to live in the message and in `overview.md`. If that is the answer, it
belongs in the template beside the rows rather than in a transcript.

---

## ⬜ Corrections — records, not the tool

`docs/review-chain-spec.md` §*The last round verifies* puts these outside
`Needs a fix`. They owe no fix pass.

**Nine verdict rows in `round-1.md` read `fixed at <sha> — at  —` with
nothing between the second `at` and the dash.** The fix pass's own table wrote
its third cell as ``at `9a52268c` — …``, and
`skills/code-review/scripts/round_record.py:3697` composes
`fixed at <sha> — <note>` after cutting the commit's code span out of that
cell. The two prepositions meet and the gap is where the commit used to be.
The tool did what it is written to do; the cell it was handed opened with a
preposition the tool supplies itself. All nine `fixed` rows carry it.

**There is no `rounds/round-1-fixes.md`.** Twenty-nine of them stand elsewhere
in this tree and `skills/code-review/SKILL.md:198` names the file as the older
half of the convention `round-N-report.md` completes. The fix pass's table
exists, in a session scratch directory that nothing promises to keep, so every
claim about what the fix pass did reached this round as prose in a spawn
prompt — which `agent-contract` §5 says is not evidence. I opened each of them
instead, and they all held; the point is that nothing but the prompt would
have carried them to the next round.

**`spec.md` still lists three allowed forms and not the mid-line `&`.**
`seal/specs/1789445605-…/spec.md:124-129` is the allowed table the compliance
stage reads, and round 1's 🟡 1 cited it by name. The form is now in
`templates/config.md`'s allowed list with its cost, in the test module's
`ALLOWED` mapping, and in the changelog — and in neither of the spec's two
lists, which is the state round 1 called not defensible, at the one coordinate
it was not repaired.

**`questions.md` orders its rows Q1, Q2, Q3, Q4, Q6, Q5.** Q6 was inserted
above Q5 rather than after it.

**Three of round 1's own ⬜ corrections stand unrepaired**, which is the
correct outcome for two of them and worth saying for the third.

- `seal/ledger.md:1885`, `:1942`, `:1943` — the prose was re-read and
  corrected in `bb5468be`. I read all three cells against the code they
  describe and they now agree. Closed.
- `seal/ledger.md` S14's replacement still covers one of the four claims S14
  bound. Nothing in the diff addresses it.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py:819` — the fixture's
  planted value is still never asserted to have landed. Round 1 called it a
  fixture that can rot rather than a defect, and that reading still holds.
- `templates/config.md` §*Choosing a value — the criterion*, rule 3 — the
  allowed list still does not say what a `;`-joined row costs the base
  comparison. Unchanged.

---

## What I confirmed rather than doubted

Listed because the job of a verifying round is the answers, and an answer with
no grounds behind it is the reviewer trusting the fix pass's account.

**Every repair is red under mutation.** Thirteen mutations in a
`git clone --no-local` at `6fc9bb71`, one at a time, each restored from the
original bytes before the next. The baseline over the four modules is 177
passed.

| Round 1's finding | Mutation | Cases red |
|---|---|---|
| 🟡 1 | `not_as_written` widened to refuse any `&` outside `&&` | `test_an_ampersand_that_is_not_last_stays_allowed`, 3 of its 4 values |
| 🟡 2 | the *takes every row below it* measurement deleted from the pipe cell | `test_the_allowed_list_says_a_pipe_cannot_reach_the_row_at_all` |
| 🟡 2 | each of the pipe warning's three needles in the bootstrap, separately | `test_a_candidate_carrying_a_pipe_is_refused_where_candidates_are_derived`, three times |
| 🟡 3 | the `Makefile` candidate source moved out of the bounded slice | `test_the_question_proposes_candidates_read_off_the_repository` |
| 🟡 4 | the module header reverted to *the command names the row to write* | `test_the_module_header_names_both_refusals_and_neither_names_a_command` <!-- NAME NOT IN TREE: work item 1789598366 (#415) renamed it to `test_the_module_header_names_every_refusal_and_none_names_a_command` when a third refusal joined the header. The name is kept as round 2 read it. --> |
| 🟡 5 | the `cmd.exe` clause dropped from the refusal message | `test_a_row_ending_in_a_single_ampersand_is_refused` |
| 🟡 6 | the pipe row moved into the refused table | two allowed-list cases |
| 🟡 6 | the backticks and `$(…)` reason cells swapped | `test_each_refused_form_is_named_with_what_a_shell_does_with_it` |
| 🟡 6 | the pipe row's **name cell alone** renamed | two allowed-list cases |
| 🟡 6 | the `&` row's name cell alone renamed | `test_each_allowed_form_is_listed_with_what_it_costs` |
| 🟡 7 | `#151` removed from the decline paragraph, leaving the mode paragraph's | `test_a_decline_leaves_no_trace_and_the_asymmetry_with_the_mode_is_stated` |
| 🟡 8 | the three forms deleted from the config skill's bullet | `test_the_config_skill_points_at_the_section_and_restates_no_form` |
| 🟡 9 | `the sealer's seal` reverted to `the seal` in `missing_row`, then in `suite_counts` | `test_no_instructing_document_leaves_an_instance_anonymous`, both times |

Row 9 of that table is the one the fix pass said it caught itself, and it is
where the first repair was not enough. With `named()` matching only the first
cell, renaming the pipe row's name is red; the cost cell's own *and a pipe
cannot reach this row at all* no longer finds the row for it. The second
repair holds where the first did not.

**The removed partition case left no hole, and the comment standing in its
place is true.** `templates/config.md` names *the whole command wrapped in
`$(…)`* in the refused table and *`$(…)` **inside** a longer line* in the
allowed one, so a case asserting no form appears in both would assert a
falsehood — and that distinction is the one the section exists to draw. What
the case would have caught is caught better by `table()` and `named()`
together: the pipe row moved between tables is red, which is the mutation that
motivated it.

**`rows()` is gone and nothing calls it.** The only `rows(` in the tree is
`tests/test_a_rider_reaches_its_file.py:51`, that module's own helper with a
different signature.

**Both ownerless instances are repaired and the sweep sees them.** `grep` for
the bare phrase in `skills/verify/scripts/broad_gate.py` returns nothing, and
reverting either one — `missing_row` at `:251` or `suite_counts` at `:530` —
turns `test_one_word_one_meaning.py` red.

**The three corrected ledger cells say what the code says.** I read
`seal/ledger.md:1885`, `:1942` and `:1943` against the sections and functions
they anchor rather than trusting the green check. S4's Notes no longer argue
from *a refusal naming what to write*; S4/S12's claim now says two options of
the mode question rather than of the call; S5's Notes no longer name the
config skill as a second carrier of rule 3. `evidence-check --strict` comes
back 1273 ok, 0 drifted, 0 broken.

**Q6's answer and the code draw the same boundary.** The criterion has two
halves, and a mid-line `&` fails neither in the sense a `;` does not: the
value runs as it reads, and the exit code the gate reads is the composition's.
The trailing form breaks the second half because nothing composes after it, so
there is no composition whose status could be the one read.
`templates/config.md`'s allowed list now carries the form with its cost, the
test module's `ALLOWED` mapping pins the cost to the row, and
`test_an_ampersand_that_is_not_last_stays_allowed` pins the code's boundary
over four values including `2>&1` and a quoted `&`. Document and code agree.
What round 1 called not defensible — the form in neither list — is gone from
every carrier except `spec.md`, which is the ⬜ above.

**Pull request #412 now says what the tree says.** The *Platform* section
states the refusal reaches no shell, names both `/bin/sh` and `cmd.exe`, says
Windows is unmeasured and names the `windows-latest` job. The last section
carries the pipe's file-wide cost with the four-row measurement and the
bootstrap's refusal to propose one. The *What stays legal* paragraph now lists
*an `&` that is not last*. I read the body against the tree line by line and
found no claim the tree contradicts.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The case planted for round 1's 🟡 4 reads the whole section, so the clause it pins can be deleted with every case green | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:275` | open | Executed: `#401` deleted from the paragraph — 17 passed; the whole new clause deleted — 17 passed. `#401` stands twice in `## Broad gate`. `agent-contract` §12; round 1's 🟡 7 is the same class, repaired in the sibling module by the same fix pass |
| 🟡 2 | The `&`'s platform hedge reached the message, `overview.md` and the pull request, and not the two cells of the list that owns the form | `templates/config.md:206` and `:225` | open | Read: `:206` says *the shell answers 0*, and `:225` — added by this fix pass — says the command before the `&` is backgrounded and may still be running. Under `cmd.exe` neither is what happens. `CONTRIBUTING.md` §*What a change to a gate must carry*; `agent-contract` §12 |
| 🟢 | Round 1's 🟡 1 — the mid-line `&` is in the allowed list with its cost, and the boundary is pinned | `templates/config.md:225`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:801` | **fixed** `9a52268c` | Executed: widening `not_as_written` to refuse any `&` outside `&&` reddens three of the four parametrised values. Q6 answers the code route and the criterion and the code draw one boundary |
| 🟢 | Round 1's 🟡 2 — the pipe's file-wide cost, and the bootstrap's refusal to propose one | `templates/config.md:224`, `skills/implement/orchestration.md:152` | **fixed** `9a52268c` | Executed: deleting the measurement reddens the pipe case; each of the warning's three needles reddens the new bootstrap case separately |
| 🟢 | Round 1's 🟡 3 — rule 3 is no longer restated and neither carrier copies the lists down | `skills/implement/orchestration.md:144`, `skills/config/SKILL.md:63` | **fixed** `9a52268c` | Read both carriers; the negatives are section-wide, which is the strong direction, and the two positive needles occur once each. A checker for a fourth copy is mechanism a fix pass may not add |
| 🟢 | Round 1's 🟡 4 — the module header names both refusals and the template paragraph no longer argues from the removed sentence | `skills/verify/scripts/broad_gate.py:12-20`, `templates/config.md:173` | **fixed** `9a52268c` | Executed: the header reverted is red. The template half is repaired in the document and its case is 🟡 1 above — the prose is right, the pin is not |
| 🟢 | Round 1's 🟡 5 — the refusal message names `/bin/sh` and `cmd.exe`, and `overview.md` records the claim as unmeasured | `skills/verify/scripts/broad_gate.py:333-341`, `overview.md` §*Not verified* | **fixed** `9a52268c` | Executed: dropping the `cmd.exe` clause reddens the ampersand case. The two cells the fix did not reach are 🟡 2 above |
| 🟢 | Round 1's 🟡 6 — one table's rows, and a row found by its name cell | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` and `:89` | **fixed** `5d893171` | Executed: the pipe row moved into the refused table, the two reason cells swapped, and each name cell renamed alone — red every time. The second repair holds where the first did not |
| 🟢 | Round 1's 🟡 7 — all three Bootstrap cases bounded | `tests/test_first_setup_asks_once.py:163`, `:230`, `:287` | **fixed** `9a52268c` | Executed: `#151` removed from the decline paragraph alone is red; a candidate source moved out of the bounded slice is red. `paragraph()` raises when its opening is gone, so the decline case cannot pass on a missing heading |
| 🟢 | Round 1's 🟡 8 — the config skill's bullet is bounded and the three forms are asserted | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:349` | **fixed** `9a52268c` | Executed: the clause deleted from `skills/config/SKILL.md` is red |
| 🟢 | Round 1's 🟡 9 — both ownerless instances repaired, and the sweep reaches the file | `skills/verify/scripts/broad_gate.py:251` and `:530`, `tests/test_one_word_one_meaning.py:184` | **fixed** `9a52268c` | Executed: reverting either instance reddens the sweep. No bare instance is left in the file |
| 🟢 | The partition case was removed rather than weakened, and the comment left in its place is true | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:196` | confirmed | Read: `$(…)` is named in both tables and must be. What the case would have caught is caught by the per-table pairing, which is red under the mutation that motivated it |
| 🟢 | `rows()` is removed and nothing calls it | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` | confirmed | Read: the only `rows(` left in the tree is another module's own helper |
| 🟢 | The pull request body now says what the tree says, for findings 2 and 5 | pull request #412 | confirmed | Read the body against the tree: the *Platform* section, the pipe's file-wide cost with its measurement, and *an `&` that is not last* in the legal list |
| ⬜ | Nine `fixed` rows read `fixed at <sha> — at  —`, a doubled preposition and an empty gap | `rounds/round-1.md` | correction | The fix table's third cell opened with ``at `<sha>` —`` and `skills/code-review/scripts/round_record.py:3697` prepends `fixed at <sha> — ` after cutting the commit's code span |
| ⬜ | No `rounds/round-1-fixes.md`; the fix pass's table lives only in a session scratch directory | `rounds/` | correction | 29 such files stand elsewhere in the tree; `skills/code-review/SKILL.md:198` names the convention. Every claim about the fix pass reached this round as prose (`agent-contract` §5) |
| ⬜ | `spec.md`'s allowed list still omits the mid-line `&`, which is round 1's 🟡 1 at the coordinate its grounds cited | `spec.md` §*What is refused, and what stays allowed* | correction | Read: three allowed forms, and the form is in neither of the spec's two lists |
| ⬜ | `questions.md` orders its rows Q1, Q2, Q3, Q4, Q6, Q5 | `questions.md:21` | correction | Q6 was inserted above Q5 rather than after it |
| ⬜ | Round 1's three ledger-prose corrections are done; its S14, fixture and `;`-cost corrections stand | `seal/ledger.md:1885`, `:1942`, `:1943` | correction | Read all three corrected cells against the code they describe. S14's replacement still covers one of four claims, and the other two were correct to leave |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` over the four modules the fix diff touches, at `6fc9bb71` in a `git clone --no-local` | exit 0, 177 passed |
| Thirteen mutations behind round 1's nine findings, each restored from the original bytes before the next | every named case red; the table above lists which |
| The clause added for round 1's 🟡 4 deleted in full from `templates/config.md` | exit 0, 17 passed — the finding above |
| `#401` replaced in the rewritten paragraph alone, leaving the section's second occurrence | exit 0, 17 passed |
| Each of the bootstrap pipe warning's three needles, separately | exit 1 each — the new case reddens on all three |
| `evidence-check --strict .` in the clone | exit 0 — 1273 ok, 0 drifted, 0 broken |
| `survivor-check --range 96c88c9..6fc9bb7` against this work item's `survivors.md` | exit 0 — 47 sentences removed, 2 survivors, both excused |
| `deferral-check` in the clone | exit 0 — resolves |
| `grep` for the bare ownerless phrase across `skills/verify/scripts/broad_gate.py` | no match |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** `agent-contract` §2 makes it the sealer's one act; no round has run it and this round did not. It comes due when nothing is left open |

Every probe ran in a `git clone --no-local` of this repository at `6fc9bb71`,
under the session scratchpad. The clone, its virtualenv and the two driver
scripts were deleted before this report was written; the user's own checkout
was read and never written.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `Broad gate` row can ever carry a pipe, and whether `config_rows` should learn to unescape one | `questions.md` Q5, already deferred by the work item, routed to an issue. Round 1's measurement about the rows below is now recorded in Q5's own cell | the repository owner |
| Whether the gate behaves on Windows as the refusal's message says | `overview.md` §*Not verified*, already deferred and rewritten by the fix pass. 🟡 2 above is about two document cells, not about this measurement | the repository owner, at the next `windows-latest` run |

## Paste-ready fixes

Finding 1 — `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
replacing the case at `:275` and adding the bounded helper above it. The shape
is `refusal_bullet()`'s at `:349`, which this module already ships:

```python
def refusal_paragraph():
    """The paragraph that argues a refusal over a prompt, bounded at the blank
    line — not the section.

    Round 2's 🟡 1. `#401` stands twice under `## Broad gate` — once here and
    once in the criterion's closing prose, where it has been since before this
    branch — so a section-wide slice cannot fail by losing it from the
    paragraph the case is named for. Deleting the whole clause left 17 cases
    green."""
    body = broad_gate_section()
    opening = "**An absent row is a refusal, not a default.**"
    assert opening in body, "the refusal paragraph is gone from the template"
    return flat(body[body.index(opening) :].split("\n\n", 1)[0])


def test_the_paragraph_above_the_lists_no_longer_says_it_names_what_to_write():
    """*A refusal that names what to write is answered by the next person to
    read it* was half the stated reason for preferring a refusal to a prompt,
    and the refusal no longer does that. The paragraph sits inside the very
    section this branch rewrote."""
    assert "names what to write is answered" not in flat(broad_gate_section()), (
        "the template still argues from the sentence the message dropped"
    )
    paragraph = refusal_paragraph()
    assert "names whose the row is and where it is answered" in paragraph
    assert "does **not** name a command to write" in paragraph, (
        "the paragraph no longer says what the message stopped doing"
    )
    assert "#401" in paragraph, (
        "the paragraph asserts the change without the report behind it"
    )
```

Finding 2, first cell — `templates/config.md:206`, the refused table's third
row. `before any check has finished` is the needle the case reads, and it
stays:

```markdown
| a trailing `&` that is not part of `&&` | `bin/test -q &` | `/bin/sh` backgrounds the whole line and answers 0 before any check has finished. `cmd.exe` separates two commands instead, so what the gate reads is the second one's status. Two different wrong answers, refused for the same half of the criterion |
```

Finding 2, second cell — `templates/config.md:225`, the allowed table's `&`
row. `may still be running when the gate stamps` is the needle the case reads,
and it stays:

```markdown
| an `&` anywhere but at the end | the command before it is backgrounded and its status discarded, exactly as a `;` discards one — and unlike a `;`, it may still be running when the gate stamps, writing into the tree the stamp is about. That is `/bin/sh`; `cmd.exe` sequences the two commands instead, so nothing is left running and the status read is the second command's. Telling an operator `&` from a `2>&1` or a quoted `&` needs the shell parser this list exists to avoid, so it stays the row author's own composition. The **trailing** form is refused, because nothing composes after it and the whole line goes to the background |
```

Needs a fix: yes — finding 1; finding 2 is fix-or-justify and justifying it means writing the grounds into the two cells.
Loses a record or crashes: no

Whether to spend the run's one reopening on this: I would. Both repairs are
single edits in files this branch already owns, neither touches the shipped
gate, and finding 1 is a case that cannot fail inside the release whose
subject is a check that could not fail. An issue would carry finding 2 well
enough and would carry finding 1 badly, because the case ships green and reads
as coverage.

## Proof

Files opened for this round:

- The fix diff in full — `skills/verify/scripts/broad_gate.py`,
  `templates/config.md`, `skills/config/SKILL.md`,
  `skills/implement/orchestration.md`,
  `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
  `tests/test_first_setup_asks_once.py`,
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `tests/test_one_word_one_meaning.py`, `seal/ledger.md`, this work item's
  ledger fragment, `changelog.md`, `overview.md`, `questions.md`,
  `survivors.md`, `rounds/round-1.md`
- `rounds/round-1.md` and `rounds/round-1-report.md` in full
- `spec.md` §*What the shell actually does* and §*What is refused, and what
  stays allowed*
- `skills/code-review/scripts/round_record.py` — `close`'s grounds
  composition; `skills/code-review/scripts/chain_check.py` — `CLOSED_WORDS`
  and `verdict_of`
- `skills/code-review/SKILL.md` §*What lives in the work item's `rounds/`*,
  `CONTRIBUTING.md` §*Running the checks*, `CLAUDE.md`, `seal/config.md`
- Pull request #412's body, in full

Not opened: the rest of `tests/`, `plan.md` and the phase records beyond what
round 1 quoted, and `docs/` beyond the sections cited.
