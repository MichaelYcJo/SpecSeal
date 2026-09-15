# Feature Specification: the broad gate row runs unchecked and is never asked for (#402, #401)

<!-- seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## The two tickets are one row, in causal order

One row of `seal/config.md` carries four properties, and two tickets are about
the last three of them.

1. **It is an arbitrary shell command line a person writes by hand.** That is
   the design, and it is not in question here.
2. **Nothing checks what was written.** `hooks/config.py#config_rows` strips
   whitespace and hands the rest to `/bin/sh`, so a value wrapped in backticks
   — the way every command in every document in this project is written — stops
   being the command and becomes a program that prints one. **#402.**
3. **Nothing ever asks for it.** The question reaches a person only as the
   gate's refusal, after the review rounds have settled, which is the last
   moment available and the one where whoever is there has every reason to
   answer it themselves. **#401.**
4. **Nobody has written down how to choose a value.** The session that met the
   refusal derived three rules under pressure; two of them are written nowhere.
   **#401, second half.**

②③④ all follow from ①, and ③ is why ② was reached at all: the first repository
to fill the row in by hand is the first repository where nobody was asked.

## Two corrections this spec starts from

`agent-contract` §5 — nothing that arrives in prose is a fact until the
coordinate is opened. Both tickets carry one claim each that does not resolve
as written, and the first of the two changes the shape of the work.

**`hooks/routing.py#parse` carries no backtick rule.** #402 says the defence
already exists one file over — *"`hooks/routing.py#parse` refuses a backticked
answer in the routing rows, loudly for the two strict axes"* — and reads as
though there were a check to copy. Opened at `hooks/routing.py:101`: `parse`
compares each value against a fixed vocabulary (`REVIEW_ANSWERS`,
`DESTINATION_ANSWERS` at `hooks/routing.py:51` and `:55`) and returns `None`
for anything outside it. A backticked answer is rejected the way `yes` or
`Through the review chain` is rejected — by not being a member — and no code
in that module mentions a backtick at all. The sentence in
`templates/sdd-routing.md` is what names the mistake; the refusal is vocabulary
matching.

**So the defence cannot be copied, and the reason it cannot is the reason #402
exists.** A closed vocabulary refuses every wrong value for free. The `Broad
gate` row has no vocabulary — it is any shell command line — so the same
guarantee has to be bought by naming the forms that are refused, which is what
this work builds and what §*What is refused, and what stays allowed* below
decides.

**#402's second-surface coordinate is one function earlier than the ticket
says.** The ticket names `broad_gate.py:349`; the `command.split("&&", 1)[0]`
is `first_command` at `skills/verify/scripts/broad_gate.py:346`, and its one
caller is `compare_at_base` at `:389`. Both stand downstream of `gate()`
(`:516`), which is where the row is read (`:532`) and where the shell runs it
(`:569`). A refusal raised in `gate()` before the first check runs closes the
second surface without a second repair, and this spec's scope says so rather
than leaving the reader to assume it.

## What the shell actually does — executed

Executed by the framing session on 2026-09-15, macOS, `/bin/sh`, reading each
exit code directly (`agent-contract` §1). This is the measurement the whole
refusal is drawn against, so it is here rather than cited.

| Value as written | Printed | Exit |
|---|---|---|
| `echo "true"; echo "a check failed" >&2; false` | `true` and the failure | **1** |
| `` `echo "true"; echo "a check failed" >&2; false` `` | the failure alone | **0** |
| `$(echo "true"; echo "a check failed" >&2; false)` | the failure alone | **0** |
| `false &` | nothing | **0** |
| `false \| cat` | nothing | **0** |

Rows 2 and 3 are the same content as row 1 and come back green with the
failure still on the screen. Row 4 is the same green over a check that had not
finished. Row 5 is in the table because it is the form that stays **allowed**,
and the reason is in the allowed list below rather than left to be noticed.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `templates/config.md` §*Broad gate* | The clause both tickets defeat: no default, because the sealer judges nothing and *a row is a thing a person wrote, and what the sealer's seal covers is exactly that*. It is also the file this work adds to, twice |
| `skills/verify/SKILL.md` §*The Seal Test* | A check that cannot fail is the counterfeit. A wrapped row is that counterfeit reached by a formatting habit rather than by a default |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | This changes a gate's verdict and touches the question budget. The pull request owes a test seen red, a stated failure direction, a prompt budget and platform honesty |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides #401's timing between three candidates: the design that stops to ask a person is the more expensive, and the difference has to be argued |
| `skills/implement/SKILL.md` §1 | Every question a person genuinely has to answer goes in one batch before the first edit. The `Broad gate` row is the one person-question in the flow that is structurally exempt |
| `skills/implement/orchestration.md` §*Orchestrator: Bootstrap — create what's missing* | The batch that already exists, once per repository. It asks two things today and gains a third |
| `skills/implement/orchestration.md` §*Orchestrator: Parity setup — deriving what can be derived* | The shape the third question takes: what the machine can derive is proposed, the person confirms, and nothing is guessed |
| #88, via `skills/implement/orchestration.md` §*how the work is routed* | Questions that belong together are asked together. One ask, not a second wait |
| `skills/config/SKILL.md` §*What this does not do* | Refuses a generic row setter and a schema. This is why the bootstrap writes the row the way that skill already writes one, and why `seal.py`'s writer stays the `Mode` row's |
| `tests/test_the_rules_have_one_owner.py` | The criterion gets ONE home and every other document points at it |
| `agent-contract` §12 | The defect is a class. It is enumerated by construction below, and it is finite |
| `agent-contract` §14 | The refusal is text a person reads and acts on, so it is documented and pinned in the same commit |
| `agent-contract` §15 | Every case this commissions is seen red before it is planted |
| #180 | The repair is the check. A sentence in `templates/config.md` may come along; it cannot be the fix |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry goes to this directory's `changelog.md`, the new evidence rows to `seal/ledger/1789445605-…md`. `seal/ledger.md` is touched only for rows this work removes |

## What is refused, and what stays allowed

Both tickets leave this judgment open and it is decided here. The criterion is
one sentence with two halves:

> **The value must run as the command it reads as, and the exit code the gate
> reads must be that command's.**

Everything refused breaks one of the two halves. Everything else is the
repository's own composition and stays legal, because the row is an arbitrary
shell command line by design (#402 §*Not this*).

**Refused — three forms.**

| Form | Written as | What the shell does | Which half it breaks |
|---|---|---|---|
| The whole value wrapped in a matched pair of backticks | `` `bin/test -q && ruff check .` `` | runs the content, **discards its exit status**, then executes its **output** as a command | the value is not the command that runs |
| The whole value wrapped in `$(…)` | `$(bin/test -q && ruff check .)` | identical semantics in the other spelling | the same half. Enumerated from the class rather than reported (§12): refusing one spelling and not the other closes the instance and leaves the cause |
| A trailing `&` that is not part of `&&` | `bin/test -q &` | backgrounds the whole line; the shell returns 0 before any check has finished | the exit code read is not the command's |

**Allowed, deliberately — and the cost of each is named rather than hidden.**

| Form | Why it stays legal |
|---|---|
| A pipe, `\|` | #402 settles it: a pipe is a normal thing in a broad command. Its cost is real and belongs in the open — `bin/test -q \| tee out.txt` exits with `tee`'s status, so a row written that way is a claim the repository made about itself, which is exactly what `templates/config.md` already says the row is. `agent-contract` §1 is the reader's rule for it, not the gate's |
| `$(…)` **inside** a longer command line | `pytest -n $(nproc)` is a sane broad command and the line still runs as what it reads as. Refusing every substitution would make legitimate rows unwritable, which is the over-reach #402 warns against |
| `;`, `\|\|`, quotes, redirection, variables, globs | Telling a status-discarding `;` from one inside a quoted argument needs a shell parser, and a parser here is the general sanitiser #402 refuses. The row stays the repository's to compose |

**What the refusal is not.** It does not strip, rewrite, or normalise the
value — stripping makes a wrong value silently work and leaves the file still
wrong and the next person still believing backticks are fine. It names the
form, shows the row rewritten, and runs nothing.

## The class, enumerated by construction

The class is *a value the gate executes that the gate never looked at*, and it
is bounded by the readers.

**There is exactly one reader of the row's value.** `broad_command`
(`skills/verify/scripts/broad_gate.py:218`) is the only caller of
`hooks/config.py#config_rows` that asks for `Broad gate`; grepped across
`*.md`, `*.py` and `*.yml`, every other mention of the row is documentation
(`templates/config.md`, `skills/config/SKILL.md`, the two READMEs) or is about
the round record's `Broad gate` **cell**, which is a different thing with the
same name.

**So the value reaches a shell in exactly two places**, and both are inside
`gate()`'s reach:

| Where | What it does with the value | Closed by |
|---|---|---|
| `broad_gate.py:569` | the whole row, `shell=True` — the run that earns the stamp | the refusal at `gate()`, raised before this line |
| `broad_gate.py:389` (`compare_at_base` → `first_command`) | the row's first `&&`-joined command, `shell=True`, at the base | the same refusal — this line is only reached after `:569` has run |

Nothing else executes the value, so one refusal in one place closes both.

## Scope

**In.**

1. `broad-gate` refuses a value that breaks either half of the criterion,
   before any check runs, exit 2, nothing run — the shape the absent row
   already takes. The message names the form, quotes the value, and shows the
   row rewritten without the wrapping.
2. `templates/config.md` §*Broad gate* gains the two lists above, each entry
   with its reason.
3. `templates/config.md` §*Broad gate* gains **the criterion for choosing a
   value**, three rules, and becomes its one owner.
4. `skills/implement/orchestration.md`'s Bootstrap asks for the row in the
   **same `AskUserQuestion`** as the mode, as a proposal built from the
   repository, with a decline that is knowing.
5. The refusal and the two documents that meet it send the question to a
   person instead of leaving a session to choose: `broad_gate.missing_row`,
   `agents/sealer.md`'s exit-2 bullet, and
   `skills/code-review/orchestration.md` where the sealer is spawned.
6. The records — `changelog.md` and `seal/ledger/<id>.md` in this directory's
   own files, `overview.md`, and the re-verification of every ledger row this
   work drifts.

**Out, each with the reason it is out.**

| Not in scope | Why |
|---|---|
| A default value for the row | The Seal Test argument in `templates/config.md` is the whole reason the row exists. Not reopened |
| Removing or softening the refusal on an absent row | Correct behaviour for a run with nobody at the keyboard. The timing is the defect, not the refusal |
| Letting the sealer pick a command | `agents/sealer.md` is a runner and a reporter and judges nothing |
| A general sanitiser, or any restriction on what a broad command may be | #402 §*Not this*. The allowed list above is the commitment |
| Stripping the backticks | #402 §*Not this*. A wrong value that silently works teaches the next person that it was right |
| A rule in `templates/config.md` **as the repair** | #180. The template gains sentences; the refusal and the ask are what make them true |
| A new hook arm or prompt for a repository that is already opted in and has no row | A new prompt owes `CONTRIBUTING.md`'s budget, and nothing cheaper than the existing refusal is being skipped: the refusal already arrives at the one moment the row decides anything. Their door is the refusal's new sentence and `/specseal:config` |
| A generic `| Item | Value |` row writer in `skills/implement/scripts/seal.py` | `skills/config/SKILL.md` §*What this does not do* refuses a schema, and `seal.py`'s `with_row`/`write_row` are documented as the `Mode` row's. The bootstrap writes the row the way `/specseal:config` step 3 already instructs — the row **and its section**, taken from `templates/config.md` |
| Any durable trace of a knowing decline | See below. It would distinguish two states that are treated identically |
| Hardening `first_command` separately | It is unreachable with a refused value, and a second guard in a second place is a second answer to maintain |
| The pipe's status rule | Allowed, with its cost stated in the allowed list. Changing it would restrict what a broad command may be |

**Why a decline leaves no trace, since the mode row's own history argues the
other way.** Bootstrap records the mode answer because #151 measured what its
absence costs: a root somebody chose and a root that appeared because a session
followed a routing rule are byte-identical, and the never-asked repository got
shared mode **silently**. Nothing about the `Broad gate` row is silent. A
repository that declined and a repository that was never asked both meet the
same refusal at the same moment, and the refusal says the same correct thing to
both. A trace would separate two states nothing treats differently, and would
add a writer and a way for that writer to go stale.

## The criterion for choosing a value

Three rules. The third exists in the tree already, in two places; the first two
were derived under pressure by the session that met the refusal and are written
nowhere. `templates/config.md` §*Broad gate* becomes the one owner of all
three, and `skills/config/SKILL.md` and the Bootstrap point at it rather than
restating it (`tests/test_the_rules_have_one_owner.py` is the rule being
followed here).

| # | Rule | Why |
|---|---|---|
| 1 | A check that is red repository-wide for reasons unrelated to any branch does not belong in the row | It would block every future work item for something none of them caused, and a gate that always fails is read as noise and then ignored |
| 2 | A command that **fixes** the tree (`--fix`, `--write`, a formatter in write mode) is not a gate command | A gate asks what is wrong; one that changes the answer while reading it can only come back green, which is the counterfeit `verify` names |
| 3 | The suite runner comes first | `broad_gate.first_command` re-runs what stands before the first `&&` on the failing files at the base, and that comparison is what earns each failure its `new` or `failing on base too` |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The reported mistake is refused | Given a repository whose `Broad gate` row is the whole command wrapped in backticks · When `broad-gate` runs · Then it exits **2**, nothing ran, and the message names backticks and shows the row rewritten without them | executed case in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, a fixture repository, exit code read directly |
| A2 | The quiet direction is the case | Given the row's content is a check that fails but whose output is runnable · When the value is bare · Then the gate is not sealed; when the same content is wrapped · Then the gate **refuses** rather than sealing | executed case carrying #402's measured pair — bare exits 1, wrapped exited 0 before this work |
| A3 | The other spelling is refused too | Given the value wrapped in `$(…)` · When `broad-gate` runs · Then the same refusal, naming that form | executed case |
| A4 | A backgrounded row is refused | Given a value ending in a single `&` · When `broad-gate` runs · Then refused, naming what the shell returns | executed case |
| A5 | What stays allowed still runs | Given rows containing a pipe, a `;`, a `$(…)` inside a longer line, and a `&&` chain · When `broad-gate` runs against a green tree · Then every one of them is sealed exactly as today | executed cases, one per allowed form |
| A6 | Nothing runs before the refusal | Given a refused value · When `broad-gate` runs · Then no check output file was written and no worktree was added | executed case asserting the kept-output directory holds nothing |
| A7 | The template says what is refused and what is not | `templates/config.md` §*Broad gate* carries both lists, each entry with a reason | document case in the new module, red by deleting the sentence it pins |
| A8 | The criterion has one home and is reachable from the others | `templates/config.md` §*Broad gate* carries the three rules; `skills/config/SKILL.md` and `skills/implement/orchestration.md` point at it and do not restate it | document cases + `bin/test -q tests/test_the_rules_have_one_owner.py` |
| A9 | The bootstrap asks | The Bootstrap section asks for the row in the same `AskUserQuestion` as the mode, proposes candidates read off the repository, never guesses, offers a decline, and says what the decline costs | document cases in `tests/test_first_setup_asks_once.py`, the shape that already pins the mode question |
| A10 | A session that meets the refusal brings it to a person | `broad_gate.missing_row`'s text says the row is a person's, names `/specseal:config`, and does not tell the reader to write one; `agents/sealer.md` and `skills/code-review/orchestration.md` say the refusal goes back to a person | executed case on the refusal text + document cases |
| A11 | Nothing else about the gate moved | The absent-row refusal still exits 2 with nothing run; a green tree still seals; a failing test is still labelled `new` or `failing on base too` | the existing cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, run whole |

## Data & interfaces

**Coordinates this work reads or changes.**

| Coordinate | What it is |
|---|---|
| `hooks/config.py:58` `config_rows` | strips whitespace at `:83` and nothing else. **Unchanged** — it is the shared reader of a generic table and the `Broad gate` row's semantics are not its business |
| `skills/verify/scripts/broad_gate.py:218` `broad_command` | the one reader of the row's value |
| `skills/verify/scripts/broad_gate.py:233` `missing_row` | the absent-row refusal. Its sentence changes (A10); its behaviour does not |
| `skills/verify/scripts/broad_gate.py:516` `gate`, reading the row at `:532` | where the new refusal is raised, beside `Refused(missing_row(home))` |
| `skills/verify/scripts/broad_gate.py:569` | the shell run the refusal must precede |
| `skills/verify/scripts/broad_gate.py:346` `first_command`, `:389` | the second surface, closed by reachability |
| `templates/config.md` §*Broad gate* | gains the two lists and the criterion |
| `skills/config/SKILL.md` step 3 | points at the criterion; says the row is a person's |
| `skills/implement/orchestration.md` §*Orchestrator: Bootstrap* step 1 | gains the second question |
| `agents/sealer.md` §*The command*, the exit-2 bullet | gains the refusal's two kinds and what to do with them |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py:640` | `test_without_the_row_the_gate_names_it_and_runs_nothing`, the sibling every new gate case sits beside |
| `tests/test_first_setup_asks_once.py:60` | `ORCH` and the Bootstrap section reader the new document cases use |

**The ledger rows this work will drift.** Counted in `seal/ledger.md` on
2026-09-15 by anchor, so the builder meets a number rather than a surprise:

| Anchor | Rows |
|---|---|
| `skills/verify/scripts/broad_gate.py#gate` | 3 |
| `skills/verify/scripts/broad_gate.py#broad_command` | 1 |
| `skills/verify/scripts/broad_gate.py#missing_row` | 1 |
| `skills/verify/scripts/broad_gate.py#first_command` | 1 |
| `templates/config.md#"## Broad gate"` | 1 |
| `skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create what's missing"` | 8 |

Fifteen rows, and `seal/ledger/` does not exist yet, so this work item opens
it. `CONTRIBUTING.md` §*House rules* governs each: where the claim still holds
after re-reading, `bin/evidence-check --reverify .`; where the claim went with
the code, the row is **removed** from `seal/ledger.md` and the new claim is
written into this work item's own fragment. A removal is the one case that
touches the shared file, and `CLAUDE.md` says so.

## Operational impact

- **The gate blocks more.** A `Broad gate` row that ran before and earned a
  stamp will now be refused if it takes one of the three forms. That is the
  point, and the direction is the cheap one: a wrong deny costs one prompt,
  where the wrong allow this replaces is a green stamp over a red suite.
- **This repository's own row is unaffected.** `seal/config.md:10` reads
  `bin/test -q && uvx ruff check . && uvx ruff format --check .` — not
  wrapped, no trailing `&`.
- **The prompt budget is unchanged**, and the pull request has to say so:
  the third bootstrap question rides an `AskUserQuestion` that already stops
  the session, once per repository, and no gate gains an arm.
- **New repositories see one more question at opt-in.** Answerable with a
  proposal or declined in the same breath.

## Open questions → questions.md

Both judgments the tickets left open are answered above from the tree and
neither is deferred. What is in `questions.md` is one row a measurement
settles and two the work settles; nothing there blocks the build.
