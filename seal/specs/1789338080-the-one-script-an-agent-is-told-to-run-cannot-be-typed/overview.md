# the one script an agent is told to run cannot be typed — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

## Why this work exists

The one script an orchestrator is told to run was the one script no shipped
document gave a way to reach, so four agent segments concluded it does not
ship and hand-wrote the record it generates; now the command resolves, every
document that names it says where it is, and a test enumerates the class
rather than this instance.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many `tests/test_docs_line_wrap.py`-covered files phase 3 edits | `plan.md` phase 3's `Verified by` cell said *the five covered files this phase edits* and then listed four | four, and the four it listed | **Executed** 2026-09-14: the nine documents intersected with that module's own `COVERED` list gives `agents/warden.md`, `agents/sealer.md`, `skills/code-review/SKILL.md` and `skills/code-review/orchestration.md`. The other five — `templates/sdd-round.md`, `agents/smith.md`, `skills/implement/SKILL.md`, `skills/verify/SKILL.md`, `templates/sdd-phase.md` — are in none of it; the module's own docstring records `agents/smith.md` at 148 columns as a reason it is not covered. The number was wrong and the list was right, so the cell now reads *four* and keeps its four names |
| The platform case's shape | `plan.md` names `tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_wrapper_pair_is_run_through_the_twin_the_platform_can_execute` as the form to follow, and that case opens with two `isfile` assertions | the same two assertions, kept | Written without them the case was green against a `bin/` holding neither file, because constructing an argv touches no filesystem. `skills/agent-contract/SKILL.md` §15 — *a new case is not planted until it has been seen red* — and it could not be. Recorded in `phases/phase-2.md` |
| Where the locator goes in two of the nine documents | `questions.md` Q4 assumes *one reachable form per document, attached to or beside its first mention* | at the first mention in seven documents, one sentence later in `skills/implement/SKILL.md` and `templates/sdd-phase.md` | `tests/test_the_rules_have_one_owner.py`'s `GENERATOR_NAMED` pins one exact phrase per carrier, and the first drafts inserted a parenthetical into the middle of three of them. Splitting a pinned phrase to satisfy a new pin is quieting one check with another, so the phrases were restored whole and the locators moved. No constant of that module was touched. **Round 1 🟡 4 cut this from three documents to two**: `agents/warden.md`'s pinned substring ends before the word *in*, so a clause appended after `round-N.md` leaves it whole, and the locator moved from line 186 to the first mention at 138 |
| `seal/ledger.md` is touched by a branch that removes nothing | `CLAUDE.md` §*a change writes fragments, never the shared file* — *appended is the word, and a removal is not one* | eleven hashes re-stamped in `seal/ledger.md`, no row appended and none removed | The rule forbids appending rows there, and its own next paragraph makes the shared file writable where leaving it true requires it. Seven anchors are whole sections, one of them `skills/code-review/orchestration.md#"# code-review — the orchestrator's half"` at lines 1–552, so no edit to that file could have avoided drifting them. The branch's own five rows went to `seal/ledger/1789338080-….md`, which is what the rule is about |

## What the mutation sweep found, after the phases closed

Every unit this work added was mutated one at a time before the hand-over, and
**two survived** — a unit that stays green while broken has nothing behind it,
whatever the suite total says.

- **`is_wrapped` read `all` and `any` alike**, because no half-shipped pair
  exists in the tree for the two spellings to disagree over. The answer decides
  which enumeration a script lands in, so a POSIX wrapper with no `.cmd` twin
  would have put its documents under the locator rule — pointing every reader
  at a command Windows cannot run — and taken the script out of the
  classification rule that would otherwise have caught the missing twin.
  `test_a_half_shipped_pair_is_not_a_wrapped_script` takes the twin away with
  `monkeypatch`, which is the only way to ask the question at all.
- **`unwrapped_pairs` returning nothing was a green suite.** An empty
  parametrisation runs no case and reports success, so the classification
  defence would have gone silent rather than red — the one failure mode that
  matters for a check whose whole job is to notice.
  `test_every_mention_lands_in_exactly_one_enumeration` asserts the two
  enumerations partition the mentions, which catches an empty one from either
  side.

Both were shown red by re-running the same mutation, and all twelve units die
under mutation now.

## What the pin's own message could not prevent

`plan.md` §*Failure scenario of the chosen approach* names it: a new document
names a script in passing, the pin goes red, and the cheapest green is to
delete the mention rather than add the locator. Nothing here closes that, and
the two things aimed at it shipped as planned — the failure names both accepted
forms and the document, and one mention per document satisfies the rule.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the sealer — `skills/agent-contract/SKILL.md` §2 puts the broad gate after the review rounds settle, and no phase here takes it |
| ✅ `Ran by` in all three phase records | the orchestrator, 2026-09-14 at `fef6aea` — no model override was passed at the spawn, `agents/smith.md` carries no model frontmatter and no default subagent model is configured, so the segment inherited this session's, and all three cells now read `specseal:smith on claude-opus-5[1m]` |

## Not done

**`evidence-check --reverify` moves a row's hash and leaves its `Checked` date
alone, and `CLAUDE.md` says re-verifying is re-reading followed by that
command.** So after this branch re-read eleven claims and re-stamped them, the
`Checked` column understates when each was last read by up to a year. Measured
**executed** 2026-09-14: the diff of `seal/ledger.md` is eleven rows, and
nothing outside the eight hex characters of each hash changed. Not taken here —
it is a change to `evidence_check.py`'s behaviour, which no part of #318 is
about, and hand-editing eleven dates in the shared file is the appending this
repository's fragment rule exists to stop. Filed by the orchestrator as #387, because this
repository has a tracker and `seal/follow-up.md` says a schedulable item
belongs there instead.

**`round-record` gets no README row.** Q2, answered **Out** by the repository
owner on 2026-09-14. Neither edition names `round_record.py` today, so the rule
that both READMEs move together is not reached, and adding the rows is additive
whenever the owner wants them.

**No `bin/chain-check`.** Argued in `spec.md` §Out and `plan.md`
§*Alternatives considered*, and now asserted rather than assumed: the pin
carries the classification and the property it rests on.

## Fed back into the spec

none — the pin states a convention the repository already kept everywhere it
could (`plan.md` §*The existing practice this makes checkable*), so nothing was
inferred during implementation that a planner should know they may overturn.
