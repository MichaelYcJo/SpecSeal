# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — review round 1

| Field | Value |
|---|---|
| Target SHA | 596507a9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 412 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | candidates (depth 1); test_a_candidate_carrying_a_pipe_is_refused_where_candidates_are_derived (depth 1); table (depth 1); named (depth 1); GATE_SCRIPT (depth 1); module_header (depth 1); test_the_module_header_names_both_refusals_and_neither_names_a_command (depth 1); test_the_paragraph_above_the_lists_no_longer_says_it_names_what_to_write (depth 1); refusal_bullet (depth 1); test_an_ampersand_that_is_not_last_stays_allowed (depth 1) |
| Needs a fix | yes — findings 1 through 9; the ⬜ corrections are not counted. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the run, against the whole branch — there is nothing earlier to
inherit. Spec compliance first against `spec.md` and `plan.md`'s five phases,
then quality.

The round was pointed hardest at whether the new checks can fail, and whether
they fail for the reason they are named for: this work item exists because a
check that could not fail earned a stamp, and the builder had already found two
cases that stayed green while broken. It was also asked whether any path
reaches `/bin/sh` without passing the new refusal, whether the boundary the
criterion draws is the boundary the code draws, whether a row containing a pipe
behaves as the branch now claims, and whether the Bootstrap still reads as one
question.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A backgrounding `&` is refused only when it is last, so a value breaking the criterion's second half stays legal and untested | `skills/verify/scripts/broad_gate.py#not_as_written` | **fixed** `9a52268c` | fixed at 9a52268c — The mid-line `&` was in neither list. It is now in the allowed list with what it costs — backgrounded, status discarded, and unlike a `;` it may still be running when the gate stamps — and pinned by `test_an_ampersand_that_is_not_last_stays_allowed` over four values including `2>&1` and a quoted `&`. Whether to refuse it in code instead is `questions.md` Q6, answered by the orchestrator; Executed: `(failing) & echo second` exits 0 and `not_as_written` returns None. `agent-contract` §12; `spec.md` §*What is refused, and what stays allowed* |
| 2 | The pipe's stated cost omits that the row takes every row below it, and phase 4 derives candidates from `run:` steps where pipes are ordinary | `templates/config.md` §*What is refused, and what stays allowed*, the `a pipe` row | **fixed** `9a52268c` | fixed at 9a52268c — The pipe's cost cell now carries that the row takes every row below it, with the mechanism. The bootstrap refuses to propose a candidate carrying a `\|` and names the CI `run:` source as where one comes from. Also at bb5468be in the ledger fragment, the changelog and Q5's weight; the pull request body is the orchestrator's; Executed against `hooks/config.py#config_rows`: a pipe row above `Record language` leaves only `Mode`. The pull request body carries no correction at all |
| 3 | The criterion claims one home; the bootstrap restates rule 3, both carriers instruct copying the whole section downstream, and the cited test sees neither | `skills/implement/orchestration.md:145` | **fixed** `9a52268c` | fixed at 9a52268c — The bootstrap no longer restates rule 3, and a case asserts its absence. Both carriers now say to copy the row and the prose down to but not including the refused list, pointing at the plugin for the lists and the criterion. A checker for a fourth copy is mechanism a fix pass may not add; `templates/config.md:226`; `## Broad gate` now runs `:161`–`:238`. Executed: a reworded rule 3 in the config skill leaves 119 cases green |
| 4 | The removed design is still asserted in the module header and in the template paragraph above the new section | `skills/verify/scripts/broad_gate.py:13-17` | **fixed** `9a52268c` | fixed at 9a52268c — The module header says a row is refused two ways, names all three forms, and says neither refusal names a command to write. The template paragraph above the lists no longer argues from a refusal that names what to write. Both pinned by cases that read the header and the section rather than the file; Read: *the command names the row to write*, and `templates/config.md:173-177`. `agent-contract` §14; `phases/phase-5.md` says the sentence should survive nowhere |
| 5 | The `&` refusal's reason is `/bin/sh` semantics, asserted in `overview.md` as every platform's, and the pull request carries no platform sentence | `skills/verify/scripts/broad_gate.py#not_as_written` | **fixed** `9a52268c` | fixed at 9a52268c — The message says `/bin/sh` backgrounds, and that under `cmd.exe` the same character separates two commands. At bb5468be, `overview.md` records the platform claim as unmeasured with the `windows-latest` job named; Read: `quote()`'s docstring names `cmd.exe` and `windows-latest` in the same module. `CONTRIBUTING.md` §*What a change to a gate must carry* |
| 6 | `rows` merges the refused and allowed tables, and the refused loop discards the pairing it holds | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` | **fixed** `5d893171` | fixed at 5d893171 — `table(text, header)` returns one table's rows and the refused loop reads each form's reason from that form's own row. The first repair was not enough — renaming the pipe row's first cell still passed — so `named(rows, form)` matches the first cell, and the mutation is red; Read the helper and the loop; executed both mutations — moving the pipe row into the refused table, and swapping two reason cells — 15 cases green each time |
| 7 | Three Bootstrap cases slice to the end of the section, so deleting the sentence each names leaves it green | `tests/test_first_setup_asks_once.py:234` | **fixed** `9a52268c` | fixed at 9a52268c — All three Bootstrap cases bounded: the decline cases use the existing `paragraph()` helper, and the candidate case uses a new `candidates()` that ends at the pipe warning and separately asserts the table still sits inside the question; Read: `#151` occurs at `:170` and `:189` and the case asserts against the whole section; the `:163` slice has no lower bound. `overview.md` records the same shape repaired at one coordinate |
| 8 | A case's docstring claims it names the three refused forms; no assertion does | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:210` | **fixed** `9a52268c` | fixed at 9a52268c — `refusal_bullet()` slices the paragraph and the loop asserts all three forms are named, which is the check the docstring had been claiming; Executed: deleting the clause from `skills/config/SKILL.md` leaves 15 cases green |
| 9 | An ownerless `the seal` reached the refusal message, in the one file `SEAL_SWEPT` still omits | `skills/verify/scripts/broad_gate.py:248` | **fixed** `9a52268c` | fixed at 9a52268c — `the sealer's seal` in the message, and `skills/verify/scripts/broad_gate.py` added to `SEAL_SWEPT` — which immediately found a second ownerless instance at `:530` that nobody had reported; Read: `templates/config.md:183` writes *the sealer's seal*. `CLAUDE.md` §*a thing more than one party can have is named with whose*; the list's own comment records two prior misses |
| ⬜ | Ledger rows re-verified without their prose re-read; the S14 replacement is narrower than what it replaced | `seal/ledger.md:1942` | correction | `CLAUDE.md`: re-verifying is re-reading. `bin/evidence-check` reads anchors, not Notes, and came back 0 drifted |
| ⬜ | A fixture's planted value is never asserted to have reached the file | `tests/test_the_seal_is_taken_once_by_the_sealer.py:819` | correction | Not a false green today — the sibling pipe case proves the value lands |
| ⬜ | The allowed list does not say what a `;`-joined row costs the base comparison | `templates/config.md` §*Choosing a value — the criterion*, rule 3 | correction | Read: `first_command` splits on `&&` alone, so `bin/test -q; ruff check .` satisfies rule 3 and the mechanism cannot use it |
| 🟢 | The refusal precedes every shell run, and `first_command` closes by reachability as claimed | `skills/verify/scripts/broad_gate.py#gate` | confirmed | Read every caller of `broad_command`; both `shell=True` sites stand downstream |
| 🟢 | Every new gate case can fail | `tests/test_the_seal_is_taken_once_by_the_sealer.py` | confirmed | Executed: the call in `gate()` reverted, five cases red, exit 1 read directly |

## Paste-ready fixes

```markdown
| an `&` anywhere but at the end | the command before it is backgrounded and its status discarded, exactly as a `;` discards one — and unlike a `;`, it may still be running when the gate stamps. Telling it from a `2>&1` or a quoted `&` needs the shell parser this list exists to avoid, so it stays the row author's own composition. The trailing form IS refused, because nothing composes after it |
```
```markdown
naming a cause that is not the real one. **And it takes every row below it.** A cell of this table ends at the first `\|`, escaped or not, so the line stops being a row and `config_rows` stops reading there — a `Record language` or `Commit and pull request language` row written under it is invisible, with no message anywhere and each falling back to its default. Measured 2026-09-15; the row's own fragment carries it
```
```markdown
   **A candidate carrying a `\|` cannot be written into the row**, and a CI
   `run:` step is where one is likeliest to come from. Offer the command
   without the pipe, or offer the next candidate, and say why — a row with a
   pipe in it parses as no row and the gate then reports the row as absent.
   `templates/config.md` §*What is refused, and what stays allowed* carries
   the measurement.
```
```markdown
   Offer each candidate as **one shell command line** composed the way
   `templates/config.md` §*Choosing a value — the criterion* says to compose
   one, and name the file it came from — a candidate whose source is named is
   one the person can correct.
```
```markdown
take the row and the prose under `## Broad gate` **down to but not including**
`### What is refused, and what stays allowed`, and point at
`$CLAUDE_PLUGIN_ROOT/templates/config.md` for the two lists and the criterion
rather than copying them. A copied list is a list that goes stale the next time
the plugin changes one, which is what the criterion's one-home rule is for.
```
```python
#   1. the repository's own broad command — the `Broad gate` row of
#      `seal/config.md`, one shell command line the repository wrote for
#      itself. **A row is refused two ways, and both are exit 2 with nothing
#      run**: no row at all, because a seal taken over a command nobody chose
#      is the counterfeit `verify` names; or a row the gate would not run as
#      the command it reads as — wrapped in backticks or in `$(…)`, or ending
#      in a single `&`. Neither refusal names a command to write: the row is
#      a person's, and the message says where they answer it
```
```markdown
It is a refusal rather than a prompt because the command runs unattended — the
sealer asks nobody anything — and a refusal that names whose the row is and
where it is answered reaches that person through whoever read it, where a
question stops a session that may have nobody at the keyboard.
```
```python
        does = (
            "so `/bin/sh` backgrounds the whole line and answers 0 before any "
            "check has finished. A seal drawn from that 0 covers nothing "
            "that ran. Under `cmd.exe` the same character separates two "
            "commands instead, which is a different wrong answer and is "
            "refused for the same reason: the exit code read is not the "
            "checks'"
        )
```
```markdown
The refusal is a string test over the row's value and reaches no shell, so it
raises the same way on every platform. What it SAYS a shell does is `/bin/sh`
semantics: under `cmd.exe` a trailing `&` separates commands rather than
backgrounding, and backticks and `$(…)` are literal characters. Unmeasured on
this branch; the `windows-latest` job is where one run settles it.
```
```python
def table(text, header):
    """The rows of ONE table in a section — the one whose header cell is
    HEADER — so a form moved from the refused list to the allowed one stops
    satisfying the case named for the list it left."""
    after = text.split(header, 1)[1]
    out = []
    for line in after.splitlines():
        if line.startswith("| "):
            out.append(line)
        elif out:
            break
    return out


def test_each_refused_form_is_named_with_what_a_shell_does_with_it():
    """A list without the reason is an enumeration the next reader extends by
    analogy, which is how a narrow refusal becomes the general sanitiser #402
    steers away from. The reason is asserted IN the form's own row: the
    dictionary already holds the pairing, and a loop that only asks whether
    both strings are somewhere in the section throws it away."""
    body = section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3)
    refused = table(body, "| Refused |")
    for form, because in REFUSED.items():
        row = [line for line in refused if form in flat(line)]
        assert row, f"the refused list does not name {form}"
        assert because in flat(row[0]), f"{form} is listed with the wrong reason"
```
```python
def test_a_decline_leaves_no_trace_and_the_asymmetry_with_the_mode_is_stated():
    """The mode row records its answer because #151 measured what its absence
    costs: a never-asked repository got shared mode SILENTLY. Nothing about
    this row is silent — a repository that declined and one that was never
    asked meet the same refusal and are told the same correct thing — so a
    trace would separate two states nothing treats differently.

    Read from the decline paragraph alone. `#151` also stands in the mode
    paragraph of the same section, where it has been since before this row
    existed, so a case reading the whole section cannot fail by losing the
    argument it is named for.
    """
    decline = paragraph(bootstrap(), "**A decline writes nothing at all.**")
    assert "no sentinel" in decline
    assert "#151" in decline, "the asymmetry with the mode row is asserted, not argued"
```
```python
    for form in ("backticks", "`$(…)`", "trailing `&`"):
        assert form in bullet, (
            f"the config skill does not name {form}, so somebody reading it "
            "does not learn the refusal exists"
        )
```
```python
        "there is no command to seal over — and choosing one is not this "
        "session's to do. There is no default because a row is a thing a "
        "person wrote, and what the sealer's seal covers is exactly that "
```
```python
    # The message a session reads when the row is absent says what the
    # sealer's seal covers, and said it ownerless until #402's round 1. The
    # list was closed where somebody had looked, for the third time.
    ("skills", "verify", "scripts", "broad_gate.py"),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` over the three modules under review, at `596507a9` in a `git clone --no-local` | exit 0, 155 passed |
| The same three modules with `not_as_written`'s call in `gate()` reverted | exit 1, 5 failed / 102 passed — the backticks, red-suite, `$(…)`, trailing-`&` and nothing-ran cases |
| `bin/evidence-check --strict .` in the clone | exit 0 — 1272 ok, 0 drifted, 0 broken |
| A throwaway unit probe over `not_as_written` and `wholly_substituted`, 18 values | `(failing) & echo second` and `bin/test -q & ruff check .` come back allowed; every documented boundary behaves as its docstring says |
| The same probe against `/bin/sh`, exit codes read directly | bare 1 · backticked 0 · `$(…)` 0 · trailing `&` 0 · mid-line `&` 0 · `;` 0 · pipe 0 |
| The same probe over `hooks/config.py#config_rows`, four table shapes | a pipe row yields no `Broad gate` row, and above other rows takes all of them with it |
| Mutation probes behind findings 3, 6, 7 and 8, each reverted before the next | each named case stayed green |
| `bin/test -q tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_rules_have_one_owner.py` | exit 0 each — 2, 15 and 56 passed |
| The broad gate — full suite, repository-wide lint, typecheck | **not yet.** `agent-contract` §2 makes it the sealer's one act; no round has run it and this round did not |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `Broad gate` row can ever carry a pipe, and whether `config_rows` should learn to unescape one | `questions.md` Q5, already deferred by the work item, routed to an issue | the repository owner. Finding 2 adds two measurements that change how Q5's three options weigh |
| Whether the gate behaves on Windows as the refusal's message says | `overview.md` §*Not verified*, as an assertion rather than a deferral | named in finding 5. The `windows-latest` job is where one run settles it |
