# Feature Specification: the gate reads an example and names rows nobody wrote

<!-- seal/specs/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

Two findings of round 3 of #415, filed as #429 and #430 because that run was
capped. They are one file's reader and that reader's one refusal.

- **#429** — `hooks/config.py` reads a `| Item | Value |` table inside a code
  fence as if it were the live table, so an example written above the live one
  is the table every gate gets: the broad command, the mode, every row.
- **#430** — `skills/verify/scripts/broad_gate.py` tells a person that every
  row below an unparseable line was lost, without asking whether anything is
  below it. This repository's own `seal/config.md` is the shape it is wrong
  about.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Neither defect may be closed by refusing. `hooks/config.py` is loaded by a `PreToolUse` hook, and a hook that denies wrongly stops a session with nobody at the keyboard. The reader keeps failing toward *nothing is declared*; only `broad-gate`, which already talks to a person and already exits 2, gains a sentence |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Each phase carries a case seen red, a stated failure direction, a prompt budget, and a platform statement. The prompt budget is the one a passing suite cannot report, so it is answered in the pull request body |
| `agent-contract` §12 *a defect belongs to a class* | Neither ticket's coordinate is the whole defect. #429 has three walks of the same table, not one; #430 has four sentences of the same shape, not one. §*The two classes, enumerated* below is the enumeration both phases build against |
| `agent-contract` §14 *a fix that changes what a person sees documents it and pins it* | Every sentence this work changes ships in the same commit as the case that pins its new text and the document that states the rule |
| `agent-contract` §15 *a new case is not planted until it has been seen red* | Every case here is shown failing against the unfixed arm before it is committed, and the handover says how |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry is `seal/specs/1789721571-…/changelog.md` and the evidence rows are `seal/ledger/1789721571-….md`. Nothing is appended to `CHANGELOG.md` or `seal/ledger.md` |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Every new fixture uses the neutral values the existing config fixtures already use — `bin/test -q`, `tee out.txt`, `C:\Users\x\tools\`. No real domain, path or org name enters a fixture |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | Three parties walk this table and two build refusals from it. Every sentence in the new code and its documents says whose walk and whose refusal it means — `config_rows`'s stop rule, `seal mode`'s writer, `broad-gate`'s refusal — and never *the reader* or *the refusal* bare |
| `hooks/config.py` module docstring, §*Two callers need the row and they need the SAME answer* | The fence rule is one rule in one place, consumed by every walk. A rule that lands in one walk and not another is the split that module exists to prevent, and it is the constraint that decides #429's design |
| `templates/config.md` §*What is refused, and what stays allowed* | The one home of what this table's format allows. The fence rule is written there, where `skills/config/SKILL.md` **points** rather than copies, so no repository's `seal/config.md` freezes a copy that the next release makes false |
| `skills/verify/SKILL.md` §*The Seal Test* | What the sealer's seal covers is the command a person wrote. #429 is a seal taken over a command nobody chose — the quiet direction, and why it outranks #430 in severity while landing second |

## Scope

### In

1. **One fence rule in `hooks/config.py`**, consumed by all three walks of the
   `| Item | Value |` table — `config_rows`, `refusal`, and
   `skills/implement/scripts/seal.py#table_span`.
2. **`seal mode`'s writer walks by the same rule.** `table_span` is a third
   copy of the walk and it locates the line `with_row` overwrites. Its own
   comment states the cost of leaving it behind: *a reader and a writer that
   disagree about which row is the row leave a file two rows deep that no
   command can bring into agreement.* A repair that lands in the reader alone
   creates exactly that file.
3. **Every cost sentence in `skills/verify/scripts/broad_gate.py` asks
   `below`** — the three arms of `missing_row` that speak about what lies
   below a line, and the hidden-row refusal below them.
4. **`broad-gate` names a fenced `| Broad gate |` line** where no live row was
   read. Item 1 creates this shape: a `Broad gate` line that used to be read
   becomes invisible, and the absent-row refusal would then be a true sentence
   about a cause that is not the real one — the failure #415 was opened about.
5. **The documents that state the format**: `templates/config.md`
   §*What is refused, and what stays allowed*, the docstrings of the changed
   units, and the sentence in `skills/config/SKILL.md` that says what a bare
   pipe costs.
6. **Cases for every changed sentence**, each seen red first, and the two
   fragments.

### Out, each with why

| Out of scope | Why |
|---|---|
| Refusing a second table, or refusing a fence | `hooks/config.py` is imported by `hooks/mode-gate.py`, a `PreToolUse` hook. Its own docstring: *everything here fails toward "nothing is declared"*. #415's `plan.md` §*Who reads this table* is where that was ratified |
| Changing `config_rows`'s stop rule | Both halves of it — a differently shaped row ends the table, a second header or separator ends it once a row is found — were arrived at over two review rounds of #82 and are quoted in the docstring. The fence rule removes lines **before** the walk sees them and leaves both halves operating unchanged on what survives. A repair that reopens either is a regression the docstring already predicted |
| Four-space indented code blocks | A four-space-indented line is already no row to `config_rows`, which anchors on `^\|`. `refusal` counts it as a line somebody wrote as a row, deliberately — *an indented row is still a row somebody wrote* — and that is a decision in force, not an oversight |
| A `Broad gate` row below a blank line or prose under the stopping line | #415's `spec.md` §*What this repair cannot see* names it, round 3 measured it over four shapes, and the verdict is that `below` is exactly what the stopping line cost. Not this work item's |
| The `else` arm of `missing_row` — *every row from there down is lost — this one included* | Read: the clause `this one included` gives the sentence a subject in every reachable state, so it is not a member of #430's class. Examined and left, rather than unexamined |
| The two ⬜ corrections round 3 left open — the four-record limitation case at `tests/test_the_mode_question_is_asked_once.py:358`, and two byte-identical refused lines quoted twice | #415's paperwork, not either ticket. Pulling them in widens the diff a reviewer reads for no gain, and the second is cosmetic by its own verdict |
| `seal/parity.md`'s table | It has the same shape and nothing parses it — `hooks/optin.py#parity_config` tests for the file's existence only. No walk to fix |
| The other markdown-table readers in this repository — `evidence_check.py`, `round_record.py`, `chain_check.py` | They read generated records, not a file whose own header comment invites a person to paste an example into it. Whether they share the blindness is Q1 of `questions.md`, a measurement whose answer opens a follow-up issue and does not grow this work item |
| A notice from `hooks/config.py` or `hooks/mode-gate.py` when a fenced table is present | A `PreToolUse` hook that prints is noise on every Bash call. The sentence belongs to `broad-gate`, which speaks once and only when it refuses |

## The two classes, enumerated

`agent-contract` §12: the ticket names an instance and the fix is owed to the
class. Both enumerations below are **read**, not executed — this frame ran
nothing. Q2 of `questions.md` is the measurement that confirms them, and the
red-first case each phase owes is the instrument.

### #429 — a fenced line is table furniture to every walk

The fence is invisible in both directions and to every walk, so one rule
closes three shapes:

1. **A fenced table above the live one.** `config_rows` starts at the first
   `| Item | Value |` header and never looks for another, so the fenced rows
   are the rows. Executed by the handoff at `0404df2`: `[('Broad gate',
   'EXAMPLE')]`, and the live table below is never reached.
2. **A fenced table below a live table that never began.** Where nothing has
   parsed yet, both walks step past prose and read on — so with no parseable
   row above it, a fenced example's rows become the live rows. Read, from the
   `if found: … continue` arms of both walks.
3. **`refusal` counts a fenced pipe-line as a line somebody wrote as a row.**
   Its walk reads on past the stopping line and treats any line beginning with
   a pipe as a refused row, so `broad-gate` can quote a line out of a code
   fence back at a person as their malformed row. Read.

**The shape is invited, not contrived, and two coordinates invite it.**
`seal/config.md:3-5` is a header comment pointing the reader at
`templates/config.md`, a document of example `| Item | Value |` tables. And
`skills/config/SKILL.md` §*Procedure* step 3 tells a session to take the
`Broad gate` row **and the prose under `## Broad gate` down to but not
including `### What is refused, and what stays allowed`** out of that template
and put it in `seal/config.md`. That block contains a fenced example row:

```markdown
| Broad gate | bin/test -q && uvx ruff check . && uvx ruff format --check . |
```

The instruction names no position for the copied block. Where it lands above
the live table — or where the live table has no row above it — the sealer runs
that example, and the example is a plausible command by construction. So the
quiet direction is reachable by following this plugin's own documented
procedure, which is what settles the *contrived or invited* question the
handoff asked for.

**What a repository that has one gets today, unmeasured.** Nobody has opened a
live `seal/config.md` outside this clone, so the population of files carrying a
fenced table is unknown and this specification claims nothing about it. This
repository's own `seal/config.md` carries no fence — read, ten lines, no
backticks — so nothing here changes for it.

### #430 — a sentence about what lies below a line, computed without asking

Four sites, of which the ticket names one:

| # | Site | The sentence today | Wrong when |
|---|---|---|---|
| 1 | `missing_row`, the `stopper is None` arm | *The rows below it were read* | nothing is below it. Reachable: a `Broad gate` line that will not parse, written as the table's only row |
| 2 | `missing_row`, the `mine is stopper` arm | *every row written BELOW that line is lost with it* | nothing is below it. #430's own instance, and the shape `seal/config.md` and `templates/config.md`'s shipped table both have — the `Broad gate` row is the last row of each |
| 3 | `missing_row`, the `reached` arm | *so every row under that line is lost* | nothing is under the stopping line. Reachable: a refused line above the table's first row, a parsed row, then a refused line last |
| 4 | the hidden-row refusal, gated on `hides_this_row(below)` | *Every other row under that line is gone the same way* | `below` holds this gate's row and no other. `hides_this_row` is true only when `below` holds it, so an empty `below` never reaches this branch — but a one-element `below` does, and then there is no *other* row. Read |

Site 4 is the answer to the handoff's question about that branch: it is
**unreachable with `below` empty and reachable with `below` holding one row**,
and in that state it makes the same claim about rows nobody wrote.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 The live table is the first one outside every fence | Given a `config.md` with a fenced `\| Item \| Value \|` table above a live one · When any of the three walks reads it · Then only the live table's rows arrive | `config_rows` returns the live rows; the fenced values appear nowhere in the result |
| A2 A fenced table below a table that never began is still not the table | Given a `config.md` whose live table has no parseable row, with a fenced example below it · When `config_rows` reads it · Then it returns no rows | an empty list, and `broad-gate` refuses with the absent-row message |
| A3 A fenced pipe-line is not a line somebody wrote as a row | Given a fenced line beginning with a pipe that will not parse · When `refusal` reads it · Then it is in neither `refused` nor `below`, and it is not `stopper` | `refusal` returns it nowhere, and no `broad-gate` message quotes it |
| A4 The writer and the reader agree | Given a `config.md` with a fenced `\| Mode \| … \|` row above a live table · When `seal mode shared` writes the row · Then the live table's row is what changed and the fenced line is byte-identical | `table_span` returns the live row's index; the file after the write differs on one line, inside the live table |
| A5 A fence that never closes hides what follows it, and says so loudly where it matters | Given a `config.md` with an unclosed fence above its live table · When `broad-gate` runs · Then it exits 2 with nothing run, and the refusal names the fenced `\| Broad gate \|` line rather than reporting the row absent | exit code read directly; the message contains the fenced line and does not contain `has no \`Broad gate\` row` alone |
| A6 The `Broad gate` refusal names a fenced line when no live row was read | Given a `config.md` whose only `\| Broad gate \|` line is inside a fence · When `broad-gate` runs · Then the refusal quotes that line, says a table inside a code fence is not read, and names `/specseal:config` as the door | a pinned case on the new sentence |
| A7 CRLF changes nothing | Given any of A1–A6's files written with CRLF endings · When each walk reads it · Then every answer is byte-identical to the LF file's | the same assertions over a CRLF fixture, as round 3 measured for the existing walks |
| A8 A `Broad gate` line last in its table is told what it actually cost | Given `\| Mode \| shared \|` then an unparseable `\| Broad gate \| … \|` as the last row · When `broad-gate` refuses · Then the message says nothing was written below it, and does not say rows were lost or that the table had not begun | `ALONE` in the message; `LOST` and `KEPT` both absent |
| A9 The same file with a row below it keeps the old sentence | Given the A8 file with `\| Record language \| Korean \|` under the refused line · When `broad-gate` refuses · Then the message says every row below that line is lost, and does not say nothing was written below it | `LOST` present, `ALONE` absent — this is the case that keeps A8's repair from being a flat swap |
| A10 The other three sites of #430's class are conditional too | Given each of sites 1, 3 and 4 reached with nothing below · When `broad-gate` refuses · Then no sentence names a row that was not written, and each keeps the half that explains the cause | one case per site, each seen red against its unfixed arm |
| A11 Nothing in this repository's own answers moves | Given `seal/config.md` as it stands · When every walk and `broad-gate` read it · Then the mode is `shared`, the broad command is the row's own text, and no refusal is built | run before and after each phase; the values are identical |

## Data & interfaces

**The fence rule, stated once.** A line inside a fenced code block is not part
of any `| Item | Value |` table: not a header, not a separator, not a row, and
not a line somebody wrote as a row. A fence opens at a line indented at most
three spaces whose first run is three or more backticks or three or more
tildes, and closes at the next line of at least as many of the same character
with nothing after it but spaces. A fence that is never closed runs to the end
of the file.

**Three or more, and tildes as well as backticks, is a decision with grounds.**
This repository's own records wrap a fenced example in four backticks — #429's
body and `rounds/round-3-report.md` both do — and that is exactly the text a
person would paste into `seal/config.md` to document the format. A rule that
recognised three backticks only would read the inner fence as the outer one's
close and leave the live table inside a fence.

**The helper hands back positions, not just lines.** `seal.py#table_span`
returns indices into the caller's own `lines`, so a helper that yields only
surviving text cannot serve it, and a second fence rule written to serve it is
the split `hooks/config.py` exists to prevent. The shared unit therefore
carries each surviving line's original index.

**Line endings.** `config_rows` and `refusal` walk `text.splitlines()`;
`table_span` walks `lines` with `keepends=True` and rstrips each one. The
shared unit must answer the same for both, which is what A7 pins.

**What the changed sentences say.** The wording below is the contract. Round
3's report drafted site 2's and measured it against the shape it is for; the
other three are written here in the same shape. A builder who diverges records
the divergence in `overview.md` with both sides quoted.

- Site 2, nothing below: *— and nothing was written below it, so nothing else
  was lost with it: this one line is the whole of what changes*
- Site 1, nothing below: keep *the stop rule needs a row before it can stop*,
  and drop the clause that says rows below were read.
- Site 3, nothing under the stopping line: keep the quoted stopping line, and
  say nothing was written under it rather than that every row under it is lost.
- Site 4, `below` holding this row alone: drop *Every other row under that line
  is gone the same way*, and say nothing else was written under it.

**The evidence rows** go in `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`,
anchored `path#unit@hash` on the units this work changes. The fragment needs no
header.

## Open questions → questions.md

Four rows, none of them a person's. `questions.md` names which judgments the
tickets left open were answered here instead, so nobody reopens them.

<!-- The line below is the framer's mark. -->

Framed 2026-09-18 by framer, before the build.
