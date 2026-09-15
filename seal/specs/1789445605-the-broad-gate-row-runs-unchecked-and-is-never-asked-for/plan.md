# Implementation Plan: the broad gate row runs unchecked and is never asked for (#402, #401)

<!-- seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-15 by the repository owner, when `smith` was spawned.

## Summary

One function is added to `skills/verify/scripts/broad_gate.py` and called from
`gate()` before the first check runs: it looks at the `Broad gate` row's value
and refuses three forms — the value wrapped in backticks, the value wrapped in
`$(…)`, and a trailing `&` — because in each of them the exit code the gate
reads is not the checks'. Everything else a shell command line can contain
stays legal, listed with its reason, pipes included.

Around that, three documents stop leaving the row to whoever meets the refusal
last. `templates/config.md` §*Broad gate* becomes the one owner of a criterion
for choosing a value, which the row has never had. The Bootstrap asks for the
row in the same `AskUserQuestion` that already asks for the mode, as a proposal
built from the repository rather than a blank. And the refusal itself stops
telling the reader to write a command and starts saying whose the row is.

**#402 ships first**, in phases 1 and 2. It is the one where a stamp is
currently earnable over a red suite.

## Technical context

**What exists.**

- `skills/verify/scripts/broad_gate.py:218` `broad_command` — the one reader of
  the row. `:233` `missing_row` — the absent-row refusal, the shape the new one
  copies. `:516` `gate` — reads the row at `:532`, raises
  `Refused(missing_row(home))` at `:533`, and runs the row through `/bin/sh` at
  `:569`. The new call goes between `:532` and the first `run`.
- `skills/verify/scripts/broad_gate.py:346` `first_command` and `:389` — the
  second surface #402 names. Unreachable once the refusal stands, per
  `spec.md` §*The class, enumerated by construction*.
- `hooks/config.py:58` `config_rows` — `.strip()` at `:83` and nothing else.
  Not touched: it reads a generic `| Item | Value |` table for three callers,
  and one row's shell semantics are not its business.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` — 56 cases, real git
  fixture repositories, `run_gate` helper, and
  `test_without_the_row_the_gate_names_it_and_runs_nothing` at `:640`, which is
  the sibling every refusal case sits beside.
- `tests/test_first_setup_asks_once.py:60` — `ORCH` and a `bootstrap()` reader
  that returns the Bootstrap section. Its cases are the shape the new
  Bootstrap pins take, and its docstring records that every one of them was
  seen red against the documents before they were edited.
- `skills/implement/orchestration.md` §*Orchestrator: Bootstrap* step 1 (the
  mode question, then `seal mode`) and step 3 (the parity question). The parity
  setup below it is the proposal shape this work copies: *three of the four
  fields come from the machine; only one needs the user. Never guess.*
- `skills/config/SKILL.md` step 3 already tells a session how to add a row that
  is not there — *take the row and its section from
  `$CLAUDE_PLUGIN_ROOT/templates/config.md`* — so the bootstrap needs no new
  writer.

**Constraints.**

- `agent-contract` §15 — every case seen red before it is planted. Each phase
  below names the mechanism that makes it red.
- `agent-contract` §14 — the refusal is text a person reads, so the document
  and the pin ride the same commit as the behaviour.
- `agent-contract` §8 — the gate's fixtures commit, so git is driven from
  Python. The existing module already does this; follow it.
- `CLAUDE.md` — the changelog entry goes to this directory's `changelog.md`,
  the rows to `seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md`.
  `seal/ledger.md` is touched only to remove a row whose claim went with the
  code.
- `tests/test_no_real_identifiers.py` — fixtures use `example.com` and
  `/Users/x/`.
- `tests/test_the_rules_have_one_owner.py` — the criterion is written once and
  pointed at from everywhere else.

**The failure scenario of the chosen approach, in six months.** The refused
list grows. Somebody meets a fourth form that decouples the exit code — a `;`
between two checks, a pipe into `tee` — reads the list as a promise that the
gate catches such things, and adds a case. Two or three of those and the
narrow refusal has become the general sanitiser #402 refuses, with a shell
parser inside it and legitimate rows unwritable. The defence is that the
**criterion is written down beside the list**, not just the list: a form
belongs in it only when the value does not run as the command it reads as, or
when the exit code read is not that command's. A pipe fails neither test — its
status rule is the row author's own composition — and the allowed list says so
in the same breath, so the next reader meets the argument rather than an
enumeration they can extend by analogy.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Strip the backticks and run the value** | The row in the file is still wrong, the next person still believes backticks are fine, and the fix has taught a formatting habit instead of ending it. It also has no answer for `&`: stripping it would change what the command means | **rejected.** #402 §*Not this* names it, and it is the direction that makes a wrong value silently work |
| **Refuse every shell metacharacter** | `pytest -n $(nproc)` and `bin/test \| tee out.txt` become unwritable, and the row stops being an arbitrary shell command line — which is the one thing #402 says is unchanged. Telling a quoted `;` from a status-discarding one needs a shell parser, whose own failure modes nobody has budgeted | **rejected.** This is the over-reach the ticket steers away from |
| **Refuse backticks alone** | Closes the instance and leaves the cause. `$(…)` is the same semantics in the spelling a person who knows shell would reach for, and `agent-contract` §12 asks the fix to be owed to every instance the same cause produces. Measured on this repository's own history: a class closed at the coordinate three times, one name apart each time | **rejected.** The class is the two wrapping forms plus the trailing `&` |
| **Refuse the wrapping forms and leave a trailing `&`** | `bin/test -q &` returns 0 before anything has finished — the same green over the same nothing, reached by a different keystroke. It is enumerated rather than reported, and it costs nothing: no broad command anybody would write wants to be backgrounded by the gate | **rejected**, and this is the judgment most open to being overturned. It is listed in `spec.md` with its reason so a reviewer can argue with it directly |
| **Put the check in `hooks/config.py#config_rows`** | It is the shared reader for three callers and one of them is a `PreToolUse` hook. A refusal there would be a refusal about every row, and the `Broad gate` row's shell semantics would live in the module whose docstring says it reads a generic table | **rejected.** The check goes where the value is executed |
| **Harden `first_command` as well** | Two guards in two places is two answers to keep in step, and the second is unreachable — `compare_at_base` runs only after the suite has already run. A guard that cannot fire is the counterfeit one file over | **rejected**, and `spec.md` says why the second surface closes by reachability |
| **#401: ask at the first commit on the first work item** | It puts a person-question at a commit, which is the mid-run interruption `skills/implement/SKILL.md` §1 exists to remove, and it needs a new gate arm — a prompt `CONTRIBUTING.md` requires an argument for. It also arrives after the first edit, so it is not in the batch at all | **rejected** |
| **#401: offer a proposal the person confirms, at the moment the gate first refuses** | Same objection one step later: the refusal fires after the rounds have settled, which is the timing that IS the defect. A proposal there is a better-worded version of what already happens | **rejected as a timing**, and adopted as the **form** the bootstrap question takes |
| **#401: ask at bootstrap, as a bare question** | A repository being opted in may not yet know its broad command, and a question with nothing in it to accept is answered badly to get past it — which is how a row nobody believes in gets written | **rejected on its own**, and this is the objection the proposal form answers |
| **#401: a `mode-gate`-style hook arm that stops a Bash call until the row exists** | It fires in every repository that legitimately has no row yet, and it owes `CONTRIBUTING.md`'s prompt budget an argument that nothing cheaper reaches the same guarantee. Something cheaper does: the refusal already arrives at the one moment the row decides anything | **rejected** |
| **#401: give the row a default, or a sentinel meaning "declined"** | Both are values the gate would run or read, and `templates/config.md`'s Seal Test argument is the reason the row exists. A sentinel is also a second vocabulary for a row that has none | **rejected.** Out of scope by the ticket and by the template |
| **Generalise `seal.py`'s `with_row` to write any row** | `skills/config/SKILL.md` §*What this does not do* refuses a schema, on the grounds that a generic setter is a parser for a file people edit by hand. And that skill already tells a session how to add the row and its section | **rejected.** No new writer |
| **Do nothing about the timing; fix only #402** | The refusal stays the only arrival, and the next repository to opt in meets it after its rounds have settled, with every reason to answer it itself. That is the measured status quo and it is what #401 reported | **rejected** |

## Phases

Vertical slices — each phase ends with something runnable and verified. **#402
ships in phases 1 and 2.**

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The gate refuses a value it would not run as written.** One function in `skills/verify/scripts/broad_gate.py` returning a reason or `None`, called in `gate()` between the row being read (`:532`) and the first `run` (`:569`), raising `Refused` — exit 2, nothing run. The message names the form, quotes the value, and shows the row rewritten without the wrapping. Three forms refused, per `spec.md`; nothing stripped | `bin/test -q tests/test_the_seal_is_taken_once_by_the_sealer.py` — A1–A6 and A11 as executed cases beside `test_without_the_row_the_gate_names_it_and_runs_nothing:640`, exit codes read directly. **Red first** by reverting the call in `gate()`: A1–A4 and A6 go red, and A2 comes back green the way #402 measured it — exit 0 with the failure printed | |
| 2 | **What is refused and what stays allowed, where the person writing the row reads it.** `templates/config.md` §*Broad gate* gains both lists with a reason each, and the sentence that a refused value is refused rather than repaired. `skills/config/SKILL.md` step 3 gains the same pointer for the door a person reaches later. §14 is satisfied by this phase riding phase 1's commit | `bin/test -q tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` — A7, the new module. **Red first** by deleting the sentence each case pins | |
| 3 | **The criterion the row has never had.** The three rules into `templates/config.md` §*Broad gate*, which becomes their one owner; `skills/config/SKILL.md` and `skills/implement/orchestration.md` point at it and restate nothing. Rule 3 exists in two places today and is folded into the one home rather than copied a third time | `bin/test -q tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py tests/test_the_rules_have_one_owner.py` — A8. **Red first** by deleting each rule, and by leaving rule 3's second copy in place | |
| 4 | **The bootstrap asks for the row in the same question as the mode.** `skills/implement/orchestration.md` §*Orchestrator: Bootstrap* step 1 carries a second question in the one `AskUserQuestion`: candidates read off the repository and offered, never guessed (the parity-setup shape), a decline that says what it costs, and the criterion named by pointer. The row is written after `seal mode`, the way `/specseal:config` step 3 already writes one — the row **and its section** from `templates/config.md` | `bin/test -q tests/test_first_setup_asks_once.py` — A9, in the module that already pins the mode question. **Red first** by reverting the Bootstrap edit | |
| 5 | **A session that meets the refusal brings it to a person.** `broad_gate.missing_row`'s sentence stops telling the reader to write a command and says whose the row is, naming `/specseal:config`; `agents/sealer.md`'s exit-2 bullet and `skills/code-review/orchestration.md` where the sealer is spawned say the refusal goes back to a person. Plus the records: `changelog.md` and `seal/ledger/<id>.md` in this directory, and `overview.md` | `bin/test -q tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` — A10, the refusal text executed and the two documents pinned. **Red first** by restoring the old sentence. Then `bin/evidence-check --strict .` for the fifteen drifted rows | |

This table is also where the work records how far it got. There is no separate
task list.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

**Where the phases may be re-cut, and where they may not.** Phases 2 and 3 both
edit `templates/config.md` §*Broad gate* and may land in one commit; phases 1
and 2 must, because §14 puts the document and the behaviour in the same commit.
What must not move is phase 1's position: #402's refusal is the one thing here
that is currently earnable over a red suite, and every later phase is about who
is asked and when.

**The fifteen drifted ledger rows are phase 5's, and they are re-read rather
than re-pointed.** `spec.md` §*Data & interfaces* counts them by anchor. Where
the claim still holds, `bin/evidence-check --reverify .`; where the claim went
with the code, the row is removed from `seal/ledger.md` and the new claim is
written into this work item's fragment, which does not exist yet — this work
item opens `seal/ledger/`.

## Operational impact

- **The gate blocks more, and the direction is the cheap one.** A row taking
  one of the three refused forms stops being sealed. A wrong deny costs one
  prompt; the wrong allow it replaces is a stamp over a red suite.
- **No prompt is added.** The bootstrap's third question rides an
  `AskUserQuestion` that already stops the session, once per repository. No
  gate gains an arm. `CONTRIBUTING.md` §*What a change to a gate must carry*
  asks for this as a number in the pull request body, and the number is zero
  new interruptions.
- **New repositories see one more question at opt-in**, answerable from the
  proposal or declined in the same breath.
- **This repository's own row is unaffected**, and no migration is needed for
  any existing row: `seal/config.md:10` is unwrapped and has no trailing `&`.
- **No new dependency, no new environment variable, no compatibility break.**
  The refusal is exit 2, which `agents/sealer.md` and the round record already
  treat as *refused, nothing ran*.
