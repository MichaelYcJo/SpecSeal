# Implementation Plan: the gate reads an example and names rows nobody wrote

<!-- seal/specs/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote/plan.md — HOW, in phases.
This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-18 by the repository owner's `automation` routing answer, when `smith` was spawned.

<!-- Left unfilled on purpose. The framer does not approve its own plan: the
line is filled by whoever reads this file and spawns the build, and that
reading IS the approval. -->

## Summary

Two repairs to how `seal/config.md` is read and how a failure to read it is
explained.

**#429** puts one fence rule in `hooks/config.py` and hands it to all three
walks of the `| Item | Value |` table, so a table inside a code fence stops
being the table the gates run. **#430** makes every cost sentence in
`skills/verify/scripts/broad_gate.py` ask what was actually written below the
line it is about, so a refusal stops naming rows nobody wrote.

They ship in one branch because they are one file's reader and that reader's
one refusal. #430 lands first and #429 second: the fence rule changes the input
every `broad-gate` refusal is built from, so it runs last, against the fuller
case set the first phase leaves behind.

## Technical context

**Three walks, not two.** The handoff named `config_rows` and `refusal`.
`skills/implement/scripts/seal.py#table_span` is a third copy of the same walk
and it is the **writer**: `with_row` overwrites the line whose index it
returns. Its own comment states what a partial repair costs — *a reader and a
writer that disagree about which row is the row leave a file two rows deep that
no command can bring into agreement.* Repair the reader alone and
`seal mode shared` rewrites the `Mode` row inside the fenced example while
every gate reads the live one.

**The walks differ in one way that constrains the design.** `config_rows` and
`refusal` consume `text.splitlines()` and care only about the text.
`table_span` consumes `text.splitlines(keepends=True)` and needs the **index**
of the line it found. So the shared unit yields each surviving line with its
original position; a helper that yields text alone would force a second fence
rule for the writer, which is the split `hooks/config.py` exists to prevent.

**The two review rounds of #82 are load-bearing and must not move.**
`config_rows`'s docstring quotes both: round 1 🟡 6, a row of a different shape
stepped past as though it were not there; round 2 🟡 5, a second header or a
stray separator stepped past wherever it appeared. The fence rule is a filter
in front of the walk, not an edit to the walk, so both rules go on operating
unchanged over what survives the filter. Any implementation that reaches into
the `if found: break` arms to special-case a fence is the regression the
docstring predicts.

**#430's four sites are one function and its neighbour.**
`skills/verify/scripts/broad_gate.py#missing_row` chooses between four arms on
`stopper` alone; three of them speak about what lies below a line and none asks
`below`, which `missing_row` already holds — it is the second element it
unpacked. The fourth site is the `hides_this_row(below)` refusal below it.

**The suite.** `bin/test tests/<file> -q` is the narrow form
(`CONTRIBUTING.md`). The broad gate is one act taken once, by the sealer, after
the rounds settle — not by the build.

## Alternatives considered

### #429 — which table is the live one

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The first table outside every code fence**, one rule shared by all three walks | A fence shape the rule reads differently from markdown — an unclosed fence, a tilde fence — hides a live table. Every such miss lands on *nothing is declared*: `broad-gate` exits 2 with a message, `seal mode` asks the mode question, the language rows fall back to English. Loud where it matters, and the direction this module already fails in | **chosen** |
| Skip a fenced `\| Item \| Value \|` **header** only, leaving fenced rows readable | Closes the ticket's shape and leaves two of the three. A fenced example below a table that never began still supplies the rows, and `refusal` still quotes a line out of a code fence back at a person as their malformed row | rejected |
| Read the **last** table in the file | Breaks the file this plugin's own procedure writes. `skills/config/SKILL.md` step 3 copies the `## Broad gate` prose out of `templates/config.md` into `seal/config.md`, and that prose carries a fenced example row — which, following the template's own layout, lands **below** the live table. The last table would then be the example. The rule would make the documented procedure produce a broken file | rejected |
| Require the live table under a **named heading** | Every `seal/config.md` in existence lacks one, including the stub `seal mode` writes. Every such repository would read as undeclared at once: mode questions everywhere and `broad-gate` refusing on files that are correct today. A format break paid by everyone to close a defect nobody has reported in the wild | rejected |
| **Refuse** a second table, or refuse a fence | `hooks/config.py` is imported by `hooks/mode-gate.py`, a `PreToolUse` hook. A wrong refusal there denies a Bash call with nobody at the keyboard to get past it. The module's docstring — *everything here fails toward "nothing is declared"* — and #415's `plan.md` §*Who reads this table* both forbid it | rejected |
| Leave the reader; write a rule in `templates/config.md` saying not to paste an example above the live table | A rule nothing enforces, in a document a person reads once, against a shape that same document's procedure produces. The sealer would go on sealing over a plausible example command, silently, which is the counterfeit `skills/verify/SKILL.md` §*The Seal Test* names | rejected |

### #430 — what the cost sentence says when nothing is below

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Each arm asks `below` as well as `stopper`**, and every sentence that speaks about what lies below a line has a subject | A fifth shape nobody enumerated keeps a flat sentence. The enumeration in `spec.md` §*The two classes* is what bounds that, and each site ships with a case that is red without its condition | **chosen** |
| Take `if not below` first, before asking `stopper` — the chooser round 2 of #415 rejected | Round 2's fix record is right and the reason still holds: *`below` being empty and the table not having begun are different facts.* Ordering on `below` reads a file whose table never began as a file that lost nothing, and loses the half of the message that explains why the rows survived | rejected |
| Repair site 2 alone, as #430 describes it | Three sentences of the same shape stay, one of them in the refusal directly below. `agent-contract` §12: the finding names an instance and the fix is owed to the class | rejected |
| Drop the cost clause from every arm and explain the stop rule in `templates/config.md` instead | The refusal is read by whoever is stopped by it, and what it cost is the thing they need before they open a document. The four-arm message exists because #415 round 1 measured a flat sentence sending a person to reformat rows that were read correctly | rejected |

### Whether one phase or two

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Two phases, #430 then #429** | Two commits where one would do, and the second phase re-runs the first's cases. That re-run is the point: the fence rule changes what `refusal` returns, which is `missing_row`'s input, so the sentences phase 1 pinned are the regression surface phase 2 needs | **chosen** |
| One phase | The reviewer reads one diff touching three modules, two defects and two classes, with no boundary saying which case belongs to which repair. A phase record is also where what building found gets written, and there would be one record for two findings | rejected |
| Two phases, #429 first | Phase 2 would edit message text whose fixtures had just been rewritten under it, and the shared reader — the riskier change, and the one every gate depends on — would land while the case set that catches it was still being written | rejected |
| Three phases, records last | A records-only phase is not a vertical slice. The implement skill puts the fragment rows on the commit that closes a phase, which is where they go here | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #430 — sites 1, 2, 3 of `missing_row` and site 4, the hidden-row refusal, each conditional on `below`; the docstring paragraph that enumerates the arms gains the condition; `skills/config/SKILL.md`'s sentence about what a bare pipe costs gains the last-row case; one case per site, each seen red against its own unfixed arm, plus A9 keeping the old sentence alive | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q`, and each new case run against the unfixed arm and shown red first | 59c750a |
| 2 | #429 — the fence rule in `hooks/config.py`, consumed by `config_rows`, `refusal` and `seal.py#table_span`; `broad-gate` naming a fenced `\| Broad gate \|` line where no live row was read; `templates/config.md` §*What is refused, and what stays allowed* stating the rule; cases for A1–A7 and A11 | `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_pull_request_language_is_the_repositorys.py -q`, plus phase 1's cases re-run unchanged | 354c09d |

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

Each phase closes with `seal/specs/1789721571-…/phases/phase-N.md` from
`templates/sdd-phase.md`, and carries its own rows into
`seal/ledger/1789721571-….md` and its own line into
`seal/specs/1789721571-…/changelog.md`.

## Operational impact

**No migration, no new dependency, no new environment variable.** Both changes
are to code already shipped.

**Failure direction, phase 2** (`CONTRIBUTING.md` §*What a change to a gate must
carry*): the reader reads fewer lines, so the gates **block more**. A
`Broad gate` row that exists only inside a fence stops being read, and
`broad-gate` exits 2 with a message naming that line instead of running a
command the repository did not choose. That is the cheaper mistake: a wrong
refusal costs one message to a person who can fix the file in a minute, and a
wrong allow is a seal over a narrower command than the repository chose, with
the seal saying it ran the repository's own broad gate.

**Failure direction, phase 1**: none. No verdict changes, only the sentence a
refusal already prints.

**Prompt budget.** Phase 1 adds none. Phase 2 adds **none for any repository
whose live table declares `Mode`** — this repository included, whose
`seal/config.md` carries no fence at all. For a repository whose only `Mode`
row sits inside a code fence, `hooks/mode-gate.py` denies the first Bash call
of a session and asks on the second, until `seal mode` writes a row: two
prompts, once, and then silence. That repository never declared a mode outside
an example, and #151 — a monorepo opted into shared mode with the question
never put to anyone — is the cost of assuming one. How many repositories are in
that state is unmeasured and unmeasurable from here; the pull request body says
so rather than implying a number.

**Platform honesty.** No process inspection, so nothing here varies by
operating system. The one axis that does is line endings, and A7 pins CRLF
against LF for every new answer.

**Behaviour a person could notice.** A repository that has been running a
fenced example's command will, after phase 2, either run its live row or be
refused. Nothing announces that at upgrade time beyond the changelog fragment,
which says it in the words of the defect rather than as a feature.
