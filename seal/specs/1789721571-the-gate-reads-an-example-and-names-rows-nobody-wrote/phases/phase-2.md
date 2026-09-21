# 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 354c09d |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#429, enumerated as three shapes in `spec.md` §*The two classes, enumerated* →
*#429 — a fenced line is table furniture to every walk*: one fence rule in
`hooks/config.py`, consumed by all three walks of the `| Item | Value |`
table — `config_rows`, `refusal`, and
`skills/implement/scripts/seal.py#table_span`, which is the writer. With it:
`broad-gate` naming a fenced `| Broad gate |` line where no live row was read,
because the fence rule is what makes that line invisible; `templates/config.md`
§*What is refused, and what stays allowed* stating the rule, including the
leftover phase 1 left there; cases for A1–A7 and A11, each seen red first; and
phase 1's cases re-run unchanged.

The spawn carried two constraints that decide the design. **One rule, one
place** — a fence rule in one walk and not another is the split
`hooks/config.py` exists to prevent. **The helper hands back positions, not
just lines** — `table_span` returns indices into its caller's own `lines` and
`with_row` overwrites one of them. And one bound: `config_rows`'s stop rule
does not move, because the fence rule filters lines in front of the walk
rather than reaching into the `if found: break` arms.

Q3 was named as this phase's to decide and record: the residue of CommonMark's
fence edge cases past what `spec.md` fixes, resolved toward *not a fence*. Q4
was named as this phase's to measure: whether any existing fixture in the three
modules carries a fenced table whose answer the rule moves.

## What this phase found

**All three shapes of #429 are reachable as framed, and the quiet one seals.**
Q2's other half is answered *all reachable*. The strongest reading is A5's,
measured rather than read: with the fence rule switched off, a repository whose
live table sits under an unclosed fence runs the fenced example's command and
`broad-gate` **exits 0 and prints the stamp** — the seal taken over a command
nobody chose, executed. `plan.md` had that as a consequence argued from the
code; it is now a failure a case reproduces.

**Q3, decided.** `spec.md` §*Data & interfaces* fixes the rule for the shapes
that matter. The residue below was decided against CommonMark and pinned in
`test_what_counts_as_a_fence_is_commonmarks_rule_as_far_as_it_goes`:

| The shape | Decided | Why |
|---|---|---|
| four or more spaces of indentation before the run | not a fence | that is an indented code block, and the bound is written into the pattern rather than checked after it |
| a BACKTICK fence whose info string holds a backtick | opens nothing | CommonMark 4.5. It lands on *not a fence*, which is also the direction the default resolves toward |
| a tilde fence whose info string holds tildes | opens | CommonMark leaves a tilde fence's info string unrestricted; narrowing it here would be this rule inventing an exception |
| a closing run LONGER than its opening | closes | CommonMark. Nothing rests on it, and the other reading would hide a live table |
| a closing run SHORTER than its opening | does not close | the shape the specification names: this repository's own records wrap a fenced example in four backticks, so a three-backtick rule would read the inner fence as the outer one's close |
| a run of the other character, or one carrying an info string | content | falls out of tracking the opening character and length rather than being a case |
| a fence opened BETWEEN two rows of a table | opens | this walk answers a question about the FILE and not about any one caller's state. The three walks hold different state at the same line, so a fence rule that consulted it would give them three answers — which is the split the rule exists to prevent |
| a fence that is never closed | runs to the end of the file | it lands on *nothing is declared*, which `hooks/config.py` already fails toward, and A5 is what makes it loud |

**The filter stands in front of the walk, and that has one consequence worth
writing down.** A fenced block between two rows of the live table is now
invisible rather than table-ending, so a table can span one where before the
fence's own delimiter line ended it. Nothing in the three walks changed to
allow that: it is what *the line is not shown to the walk at all* means. It is
the same direction as the rest of the rule — more of a person's live table is
read, not less.

**Q4, measured: no fixture in the three modules carries a fence at all, and a
fixture one module over did move.** `grep` over the three named modules finds
no fenced table, and all three run identically before and after — 266 passed,
3 skipped before, 275 passed, 3 skipped after, the nine new cases being the
whole difference. What moved is in a fourth module:
`test_the_broad_gate_row_is_asked_for_and_runs_as_written.py::test_the_module_header_names_every_refusal_and_none_names_a_command`
asserted `refused three ways` and the gate now refuses four. Its subject is
that the header names EVERY refusal and names no command to write, which is
unchanged, so the count was rewritten in place and the new refusal added to
its list — `skills/implement/SKILL.md` §5's first reading of a fixture whose
answer moves.

**One fact the handoff carried is false as written.** It said this
repository's own `seal/config.md` is *ten lines with no backticks*. It is ten
lines and it carries single backticks, in the header comment that points at
`templates/config.md`. Nothing follows for the rule — a fence is a run of
three — but A11's assertion was written as *no backtick* first and was red on
the real file, so the pin is now *no run of three backticks and no run of
three tildes*, which is the thing that would actually change the answers
above it.

**Both reads behind one refusal answer the same, measured.** Phase 1 left
`missing_row` calling the reader twice — `refusal(home)` always and
`rows_read(home)` in site 1's arm — and asked for the fence rule's reach over
both to be checked rather than assumed. The shape where they could disagree is
a fenced example below a line with nothing parsed above it; with the rule
switched off, the refusal says *The rows below it were read* out of the example
block. It is a case now.

**Failure direction: the gates block more, as `plan.md` predicted.** A
`Broad gate` row that exists only inside a fence stops being read, and
`broad-gate` exits 2 naming that line instead of running a command the
repository did not choose. A `Mode` row that exists only inside a fence reads
as undeclared, so `hooks/mode-gate.py` denies the first Bash call of a session
and asks on the second until `seal mode` writes a row. No new prompt for any
repository whose live table declares `Mode`, this one included: A11 is green
before and after, and its file has no fence.

**Five mutations, each seen red.** The four the fence rule can take — no fence
ever opens, any run closes whatever its character, a backtick fence's info
string may hold a backtick, a shorter run still closes — and `fenced_row`
returning None. The fourth of those survived the first case set and is what
the four-backtick case was added for; every mutation was restored from bytes
kept outside git.

**Platform.** Nothing here inspects a process or a path. The one console fact,
unchanged from phase 1: a script printing these messages on this machine
raises `UnicodeEncodeError: 'cp949' codec` on the em dash and needs
`PYTHONIOENCODING=utf-8`. It is a property of the console; the suite never
meets it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `missing_row`'s docstring sentence counting the gate's refusals — *there are two, because there are two causes* — and the module header's *A row is refused three ways* | The same two places, saying three and four. One place still carries wording this range removed: a closed work item's `questions.md` sentence about a duration, sharing the phrase `there are two causes and` and nothing else, excused in `survivors.md` with the standing text quoted |
| The assertion `refused three ways` in `test_the_module_header_names_every_refusal_and_none_names_a_command` | The same case, asserting `refused four ways` and the new refusal's own words. The case's subject did not move, which is why it was rewritten rather than reopened |
| Nothing else. The fence rule adds a filter and takes no branch out of any walk | — |
