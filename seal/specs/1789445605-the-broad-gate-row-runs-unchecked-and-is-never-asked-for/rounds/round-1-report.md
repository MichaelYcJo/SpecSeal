# Round 1 — the broad gate row runs unchecked and is never asked for (#402, #401)

Target SHA `596507a9`, confirmed as the branch head when this round started
and still the head; the working tree was clean. Base `release/v0.12.0`, pull
request #412 (draft). Round 1, no earlier round to inherit from.

## What this round found, in causal order

**The headline behaviour holds, and I saw it hold.** The refusal sits in
`gate()` between the row being read and the first `run`, and both places the
value reaches a shell stand downstream of it — I read every caller and then
reverted the call and watched five cases go red. The class-by-reachability
argument for `first_command` is true as written.

Everything below is what stands around that centre.

1. **The boundary the code draws is narrower than the criterion on one
   axis.** A backgrounding `&` is refused only when it is the last character.
2. **The one form the allowed list singles out cannot be written**, and phase
   4's new proposal machinery now reads candidates from the place that
   produces it.
3. **The criterion claims one home in three places that restate or copy it**,
   and the test cited as the enforcement sees none of them.
4. **The old design is still asserted in the two places a reader opens
   first** — the module header and the template paragraph above the new one.
5. **The refusal's reason for `&` is `/bin/sh` semantics stated as every
   platform's**, and the pull request carries no platform sentence at all.
6. **The cases that hold all of this in place can be mutated green.** Four
   distinct shapes, each verified. This matters more here than it would
   elsewhere: the release's whole subject is a check that could not fail.
7. **An ownerless `the seal` reached a message a session reads**, in the one
   file the sweep list still does not carry.

The ledger corrections are at the bottom, under ⬜, and `Needs a fix` does not
count them — `docs/review-chain-spec.md` §*A finding located in a record is a
correction, not a round* owns that rule.

---

## 🟡 1 · A backgrounding `&` is refused only when it is last

`skills/verify/scripts/broad_gate.py#not_as_written`

The check is `value.endswith("&") and not value.endswith("&&")`. Executed
under `/bin/sh`, with a check that genuinely fails inside:

| Value | Refused by `not_as_written` | Shell exit |
|---|---|---|
| `(a failing check) &` | REFUSED | 0 |
| `(a failing check) & echo second` | **allowed** | **0** |
| `(a failing check); echo second` | allowed | 0 |

The middle row breaks the criterion's second half — *the exit code the gate
reads must be that command's* — exactly as the refused row does, and it is in
neither list. `templates/config.md` §*What is refused, and what stays allowed*
lists `;`, `||`, quotes, redirection, variables and globs as legal; it does
not mention an `&` anywhere but at the end. A reader of the refused table
comes away believing the gate catches a backgrounded check.

Two things separate this from `;`, which is deliberately legal. `plan.md`'s
own argument for refusing the trailing form — *no broad command anybody would
write wants to be backgrounded by the gate* — is equally true one word
earlier. And backgrounding does something `;` does not: the suite may still be
running, writing into the tree, when the gate draws the stamp.

`agent-contract` §12 is the grounds. `$(…)` was enumerated beside backticks
for precisely this reason; the same enumeration stopped one step short here.

**The boundary case is also untested.** The parametrised list at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:858` that pins what stays
allowed carries eight values and none of them contains an `&` except the
trailing-`&&` guard.

Refusing a mid-line `&` without a shell parser is not free — `2>&1` and a
quoted `&` are both legitimate — so the honest repair may be to move it into
the allowed list with its cost named rather than into the refused list. What
is not defensible is its absence from both. The fenced fix below takes the
documentation route; the code route is named beside it.

## 🟡 2 · The one allowed form the list singles out cannot be written, and the bootstrap now proposes it

`templates/config.md` §*What is refused, and what stays allowed*, the `a pipe`
row · `skills/implement/orchestration.md` §*Orchestrator: Bootstrap*, the
candidate table

The branch knows a pipe cannot reach the row and says so in the same cell,
which is honest, and `questions.md` Q5 carries it as an open question for the
repository owner. Two measured facts are missing from all four places the
branch records it, and both change how that open question weighs.

**The cost is not confined to the row.** `hooks/config.py#config_rows` stops
reading the table at the first line that does not parse, so a `Broad gate` row
containing a pipe takes every row *below* it with it. Executed against
`config_rows` on a four-row table:

```
| Mode | shared |
| Broad gate | bin/test -q \| tee out.txt |
| Record language | Korean |
| Commit and pull request language | Korean |
                                     →  [('Mode', 'shared')]
```

`Record language` and `Commit and pull request language` are gone, silently,
and each falls back to its default. Nothing anywhere reports it. The template's
cost cell says only that `broad-gate` names a cause that is not the real one.

**And phase 4 now reads candidates from where pipes live.** The new proposal
table's first source is *the `run:` steps of whatever job gates a pull
request*, and a `run:` step piping into `tee` is ordinary. So the bootstrap
can derive a candidate, the person can accept it, the session writes it, and
the row parses as no row — the failure mode this work item exists to end,
reached through the machinery this work item adds.

The pull request body is the third place: it says *Pipes, `;`, `||`, quotes,
redirection, and `$(…)` inside a longer line are all still legal* and carries
none of the correction the template carries.

`config_rows` staying unchanged is not in question — `spec.md` §*Data &
interfaces* lists it Unchanged with its reason, and Q5 is where the repair is
decided. What is owed is the measurement, in the three places that state the
cost.

## 🟡 3 · The criterion claims one home in three places that restate or copy it

`templates/config.md:223` §*Choosing a value — the criterion* ·
`skills/implement/orchestration.md:145` · `skills/config/SKILL.md` step 3

The section says: *this section is their one home. Every other document that
mentions the row points here instead of restating them, because a rule written
in three places is three places for it to disagree with itself.* Three things
in this diff contradict it.

**The bootstrap restates rule 3's normative half.** At
`skills/implement/orchestration.md:145`: *Offer each candidate as one shell
command line, joined with `&&`, the suite runner first.* That is rule 3 minus
its reason, in a third place. The ledger fragment states the opposite as fact
— *`skills/config/SKILL.md` and `skills/implement/orchestration.md` name that
section and restate nothing*.

**Both carriers instruct a session to copy the whole section downstream.**
`skills/config/SKILL.md` step 3 and the bootstrap both say to take the row
*and its section* from `templates/config.md`. `## Broad gate` begins at
`templates/config.md:161` and now runs to the end of the file at `:238` —
78 lines, including the refused list and the criterion table. Every repository
bootstrapped after this release gets a frozen copy of both in its own
`seal/config.md`, and the next change to either list leaves that copy saying
something false about the tool. The instruction predates this branch; what
this branch changed is what *its section* now contains.

**And nothing catches a fourth copy.** `tests/test_the_rules_have_one_owner.py`
rule 12 checks that the owner states the rule and that each link names the
owner. It does not check that a link restates nothing. Verified by mutation:
adding *put the suite runner at the front, because the base comparison re-runs
whatever stands before the row's first `&&`* to `skills/config/SKILL.md` leaves
119 cases green, because the two assertions guarding it are literal negatives
(`"put the suite runner first" not in skill`) that a reworded copy walks past.

A string test for *was this restated* is weak by nature, which is a fair
answer to the third point. It is not an answer to the first two.

## 🟡 4 · The old design is still asserted where a reader opens first

`skills/verify/scripts/broad_gate.py:13-17` · `templates/config.md:173-177`

Phase 5 changed `missing_row` so it no longer tells the reader what to write,
and `phases/phase-5.md` records that the old sentence should survive *nowhere
in the message*. It survives outside the message, in the two places somebody
meets before the message.

The module header, which is the first thing anyone opening the file reads:

```
**No row is a refusal, not a default**: the command names the
row to write and exits 2 with nothing run
```

That names the removed behaviour. The same numbered list is where the command
says what it does in order, and it does not mention the second refusal — the
branch's headline change — at all.

The template paragraph directly above the new section:

```
It is a refusal rather than a prompt because
the command runs unattended — the sealer asks nobody anything — and a
refusal that names what to write is answered by the next person to read it,
where a question stops a session that may have nobody at the keyboard.
```

*a refusal that names what to write* is half the stated reason for preferring
a refusal to a prompt, and the refusal no longer does that. The paragraph sits
inside the very section this branch rewrote.

`agent-contract` §14 is the grounds: a change to what a person reads is
documented in the same commit, and these are the two documents that explain
the thing that changed.

## 🟡 5 · The `&` refusal states `/bin/sh` semantics as every platform's

`skills/verify/scripts/broad_gate.py#not_as_written` · `overview.md` §*Not
verified* · the pull request body

The message for a trailing `&` reads *so a shell backgrounds the whole line
and answers 0 before any check has finished*. Under `cmd.exe` a trailing `&`
is a command separator, not a background operator, and backticks and `$(…)`
are literal characters rather than syntax. `quote()`'s own docstring one
function over says so, and says CI runs `windows-latest` on every push.

`overview.md` does not record this as unmeasured. It asserts the opposite:
*the forms it names are POSIX shell semantics, which is what `run(...,
shell=True)` uses on every platform this plugin supports.* That sentence is
contradicted inside the same module.

The refusal itself stays defensible — refusing more, on a platform where the
form would have failed loudly anyway, costs one prompt. What is wrong is the
stated reason and the unhedged claim. `CONTRIBUTING.md` §*What a change to a
gate must carry* asks for platform honesty **in the pull request**, and PR
#412 has no sentence about a platform anywhere in it.

## 🟡 6 · The two lists can be swapped and every case stays green

`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66`
(`rows`), `:89`, `:123`, `:133`

`rows(text)` returns every line in the section beginning `| `. The refused
table and the allowed table live under one heading, so the helper merges them
and nothing distinguishes a form that is refused from one that is legal. Two
consequences, both confirmed.

**The pipe row can be moved into the refused table and both allowed-list cases
stay green** — so the two cases named for the allowed list assert only that
certain characters appear somewhere under the heading.

**A refused form can be paired with the wrong reason.** At `:94-96` the loop
reads:

```python
for form, because in REFUSED.items():
    assert form in body
    assert because in body
```

The dictionary already holds the pairing and the assertions throw it away.
Swapping the *what a shell does with it* cells of the backticks row and the
`$(…)` row leaves 15 cases green, with the backticks row now explaining itself
as *the same semantics in the spelling somebody who knows shell reaches for
first*. The docstring says the case exists to stop *a list without the reason*.

Both were reproduced by mutation in a throwaway clone; I confirmed the cause
by reading the helper and the loop.

## 🟡 7 · The Bootstrap cases read to the end of the section, so the sentence they name is not what holds them up

`tests/test_first_setup_asks_once.py:163`, `:190`, `:234`

Every case in this group slices from a marker to the end of the whole
`## Orchestrator: Bootstrap` section and never bounds the other end. At `:163`,
`test_the_question_proposes_candidates_read_off_the_repository` takes
`boot[boot.index(BROAD_ROW):]`. At `:190`,
`test_the_decline_is_offered_and_says_what_it_costs` takes everything after
`The second question`. At `:234`,
`test_a_decline_leaves_no_trace_and_the_asymmetry_with_the_mode_is_stated`
asserts against the entire flattened section.

Two verified consequences.

**Deleting the argument the case is named for leaves it green.** `#151`
occurs twice in that section — at `:170` in the mode paragraph, where it has
been since before this branch, and at `:189` in the new decline paragraph.
`assert "#151" in boot` cannot fail by deleting `:189`, and the message beside
it reads *the asymmetry with the mode row is asserted, not argued*.

**Moving the candidate table out of the question leaves it green.** The
`:163` slice has no lower bound, so the four-row table can be moved anywhere
below — past the decline paragraph, out of the question entirely — and all
four needles still match. The case name says *the question proposes*.

`overview.md` §*Fed back into the spec* records this exact shape, found and
repaired in `agents/sealer.md` during phase 5: *a case can pin a whole file
while claiming to pin one bullet*. The repair was applied at the coordinate
rather than to the class. `tests/test_first_setup_asks_once.py` already ships
a `paragraph()` helper that bounds a slice at the blank line, and these three
cases do not use it.

## 🟡 8 · A case's docstring claims a check the case does not make

`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:210`

`test_the_config_skill_points_at_the_section_and_restates_no_form`'s docstring
says *it names the three forms so somebody reading it knows the refusal
exists*. Deleting the clause that names them from `skills/config/SKILL.md` —
*the whole command wrapped in backticks or in `$(…)`, or a trailing `&`* —
leaves 15 cases green, because the four assertions all match sentences on
either side of it. Nothing checks that the three forms are named.

## 🟡 9 · An ownerless `the seal` reached a message a session reads

`skills/verify/scripts/broad_gate.py:248` ·
`tests/test_one_word_one_meaning.py` (`SEAL_SWEPT`)

The new `missing_row` text says *a row is a thing a person wrote, and what
the seal covers is exactly that*. `templates/config.md:183` writes the same
sentence as *what the **sealer's** seal covers*.

`CLAUDE.md` §*a thing more than one party can have is named with whose* is the
rule, and it names `seal` as the word that bought it: the warden's review
mark, the sealer's stamp and the smith's proof block are three different
things with that name.

`tests/test_one_word_one_meaning.py` is green because `SEAL_SWEPT` does not
list `skills/verify/scripts/broad_gate.py`. That list carries
`seal_stamp.py` and `round_record.py` and a comment on each saying why it was
extended — *the list was closed where somebody had already looked*, written
after this happened twice before. This is the third time, and adding the file
is what stops a fourth.

---

## ⬜ Corrections — records, not the tool

These are located in records. `docs/review-chain-spec.md` §*A finding located
in a record is a correction, not a round* puts them outside `Needs a fix`;
they owe no fix pass and no reader.

**Two ledger rows were `--reverify`'d without their prose being re-read.**
`CLAUDE.md` says re-verifying is re-reading and then running the command; the
hash moved and the sentence did not.

- `seal/ledger.md:1942` (S4) — its Evidence cell says *the message names the
  row to write and the file to write it in*. The branch removed exactly that,
  and two new cases assert it is gone. Its Notes cell also rejects *asking a
  person for the command* on the grounds that *a refusal naming what to write
  is answered by the next reader*, which the message no longer does.
- `seal/ledger.md:1885` (S4 / S12) — the claim reads *one `AskUserQuestion`
  with two options* and the Notes read *prompt budget: one question*. The
  section it anchors now says *one `AskUserQuestion` carrying two questions*.
  The call count is unchanged and the row's wording is not. This row appended
  a *Re-read* paragraph on each of its two previous re-verifications and
  appended none this time.
- `seal/ledger.md:1943` (S5) — its Notes say *`templates/config.md` and the
  config skill both say to put the runner first*. The branch removed that
  sentence from the config skill, correctly. The row was not touched.

Neither of these is visible to `bin/evidence-check`, which reads anchors and
not Notes prose; I ran it and it came back 0 drifted and 0 broken.

**The S14 removal is correct and one claim went unreplaced.** Removing it
rather than re-pointing it follows `CLAUDE.md`, the reason is recorded, and
the replacement is in the work item's own fragment. S14 bound four claims and
the replacement covers one: no row anywhere now claims the bootstrap *says in
three lines what it created*. The behaviour is still tested; what was lost is
the record that somebody read it.

**A fixture's value is never asserted to have landed.**
`tests/test_the_seal_is_taken_once_by_the_sealer.py:819`
(`test_the_forms_that_stay_allowed_are_sealed_exactly_as_today`) reads exit 0
and `SEALED` only. Breaking `config()` so the parametrised value never reaches
the file leaves all three cases green. It is not a false green today — the
sibling pipe case proves the value does land — so this is a fixture that can
rot unobserved rather than a defect.

**The allowed list does not say what a non-`&&` composition costs the base
comparison.** `first_command` splits on `&&` alone, so a `;`-joined row makes
`compare_at_base` re-run the whole suite at the base and append the failing
files to the second command. Rule 3 as written — *the suite runner comes
first* — is satisfied by `bin/test -q; ruff check .`, which the mechanism the
rule protects cannot use. The cost is time, not a wrong label, which is why
this sits here rather than above.

---

## What I confirmed rather than doubted

Listed because a review that reports only findings does not tell the reader
which claims were checked.

- **The refusal precedes every shell run.** `gate()` calls `not_as_written`
  immediately after `broad_command` and before `git rev-parse`, the kept-output
  directory, and both `shell=True` sites (`:686` and `:498`). `broad_command`
  has one caller, and `compare_at_base` runs only after the suite has run, so
  the reachability argument for `first_command` holds as written.
- **#402's measured pair reproduces.** Same content: exit 1 bare, exit 0
  backticked, exit 0 in the `$(…)` spelling, with the failure printed.
- **The cases can fail.** With the call in `gate()` reverted, five cases go
  red — the backticks case, the red-suite case, the `$(…)` case, the trailing
  `&` case, and the nothing-ran case — exit 1, read directly.
- **`wholly_substituted`'s boundary is the one its docstring claims.** Eight
  values read off the unit behave as documented, including `$(a) && $(b)` and
  `pytest -n $(nproc)` returning None.
- **#401's measured cause is repaired at the cause.** The old message
  instructed the one party that may not choose; the new one removes the
  instruction rather than adding a sentence beside it.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A backgrounding `&` is refused only when it is last, so a value breaking the criterion's second half stays legal and untested | `skills/verify/scripts/broad_gate.py#not_as_written` | open | Executed: `(failing) & echo second` exits 0 and `not_as_written` returns None. `agent-contract` §12; `spec.md` §*What is refused, and what stays allowed* |
| 2 | The pipe's stated cost omits that the row takes every row below it, and phase 4 derives candidates from `run:` steps where pipes are ordinary | `templates/config.md` §*What is refused, and what stays allowed*, the `a pipe` row | open | Executed against `hooks/config.py#config_rows`: a pipe row above `Record language` leaves only `Mode`. The pull request body carries no correction at all |
| 3 | The criterion claims one home; the bootstrap restates rule 3, both carriers instruct copying the whole section downstream, and the cited test sees neither | `skills/implement/orchestration.md:145` | open | `templates/config.md:226`; `## Broad gate` now runs `:161`–`:238`. Executed: a reworded rule 3 in the config skill leaves 119 cases green |
| 4 | The removed design is still asserted in the module header and in the template paragraph above the new section | `skills/verify/scripts/broad_gate.py:13-17` | open | Read: *the command names the row to write*, and `templates/config.md:173-177`. `agent-contract` §14; `phases/phase-5.md` says the sentence should survive nowhere |
| 5 | The `&` refusal's reason is `/bin/sh` semantics, asserted in `overview.md` as every platform's, and the pull request carries no platform sentence | `skills/verify/scripts/broad_gate.py#not_as_written` | open | Read: `quote()`'s docstring names `cmd.exe` and `windows-latest` in the same module. `CONTRIBUTING.md` §*What a change to a gate must carry* |
| 6 | `rows` merges the refused and allowed tables, and the refused loop discards the pairing it holds | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` | open | Read the helper and the loop; executed both mutations — moving the pipe row into the refused table, and swapping two reason cells — 15 cases green each time |
| 7 | Three Bootstrap cases slice to the end of the section, so deleting the sentence each names leaves it green | `tests/test_first_setup_asks_once.py:234` | open | Read: `#151` occurs at `:170` and `:189` and the case asserts against the whole section; the `:163` slice has no lower bound. `overview.md` records the same shape repaired at one coordinate |
| 8 | A case's docstring claims it names the three refused forms; no assertion does | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:210` | open | Executed: deleting the clause from `skills/config/SKILL.md` leaves 15 cases green |
| 9 | An ownerless `the seal` reached the refusal message, in the one file `SEAL_SWEPT` still omits | `skills/verify/scripts/broad_gate.py:248` | open | Read: `templates/config.md:183` writes *the sealer's seal*. `CLAUDE.md` §*a thing more than one party can have is named with whose*; the list's own comment records two prior misses |
| ⬜ | Ledger rows re-verified without their prose re-read; the S14 replacement is narrower than what it replaced | `seal/ledger.md:1942` | correction | `CLAUDE.md`: re-verifying is re-reading. `bin/evidence-check` reads anchors, not Notes, and came back 0 drifted |
| ⬜ | A fixture's planted value is never asserted to have reached the file | `tests/test_the_seal_is_taken_once_by_the_sealer.py:819` | correction | Not a false green today — the sibling pipe case proves the value lands |
| ⬜ | The allowed list does not say what a `;`-joined row costs the base comparison | `templates/config.md` §*Choosing a value — the criterion*, rule 3 | correction | Read: `first_command` splits on `&&` alone, so `bin/test -q; ruff check .` satisfies rule 3 and the mechanism cannot use it |
| 🟢 | The refusal precedes every shell run, and `first_command` closes by reachability as claimed | `skills/verify/scripts/broad_gate.py#gate` | confirmed | Read every caller of `broad_command`; both `shell=True` sites stand downstream |
| 🟢 | Every new gate case can fail | `tests/test_the_seal_is_taken_once_by_the_sealer.py` | confirmed | Executed: the call in `gate()` reverted, five cases red, exit 1 read directly |

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

The probe file was deleted and the clone restored to `596507a9` before this
report was written.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `Broad gate` row can ever carry a pipe, and whether `config_rows` should learn to unescape one | `questions.md` Q5, already deferred by the work item, routed to an issue | the repository owner. Finding 2 adds two measurements that change how Q5's three options weigh |
| Whether the gate behaves on Windows as the refusal's message says | `overview.md` §*Not verified*, as an assertion rather than a deferral | named in finding 5. The `windows-latest` job is where one run settles it |

## Paste-ready fixes

Finding 1 — the documentation route. The code route, if it is preferred, is a
second clause in `not_as_written` refusing an `&` that is neither part of
`&&` nor preceded by `>` or `<` and is followed by whitespace; it is narrower
than a parser but it does false-positive on a quoted `&`, which is why the
list entry is offered first. Into the *Stays legal* table of
`templates/config.md`:

```markdown
| an `&` anywhere but at the end | the command before it is backgrounded and its status discarded, exactly as a `;` discards one — and unlike a `;`, it may still be running when the gate stamps. Telling it from a `2>&1` or a quoted `&` needs the shell parser this list exists to avoid, so it stays the row author's own composition. The trailing form IS refused, because nothing composes after it |
```

Finding 2 — into the `a pipe` cost cell of the same table, replacing the
sentence that ends *naming a cause that is not the real one*:

```markdown
naming a cause that is not the real one. **And it takes every row below it.** A cell of this table ends at the first `\|`, escaped or not, so the line stops being a row and `config_rows` stops reading there — a `Record language` or `Commit and pull request language` row written under it is invisible, with no message anywhere and each falling back to its default. Measured 2026-09-15; the row's own fragment carries it
```

Finding 2, second half — into `skills/implement/orchestration.md`, after
*Offer each candidate as one shell command line*:

```markdown
   **A candidate carrying a `\|` cannot be written into the row**, and a CI
   `run:` step is where one is likeliest to come from. Offer the command
   without the pipe, or offer the next candidate, and say why — a row with a
   pipe in it parses as no row and the gate then reports the row as absent.
   `templates/config.md` §*What is refused, and what stays allowed* carries
   the measurement.
```

Finding 3 — at `skills/implement/orchestration.md:145`, replacing *joined with
`&&`, the suite runner first*:

```markdown
   Offer each candidate as **one shell command line** composed the way
   `templates/config.md` §*Choosing a value — the criterion* says to compose
   one, and name the file it came from — a candidate whose source is named is
   one the person can correct.
```

Finding 3, second half — in both `skills/config/SKILL.md` step 3 and the
bootstrap, wherever *the row **and its section*** appears:

```markdown
take the row and the prose under `## Broad gate` **down to but not including**
`### What is refused, and what stays allowed`, and point at
`$CLAUDE_PLUGIN_ROOT/templates/config.md` for the two lists and the criterion
rather than copying them. A copied list is a list that goes stale the next time
the plugin changes one, which is what the criterion's one-home rule is for.
```

Finding 4 — `skills/verify/scripts/broad_gate.py`, the header's first numbered
item:

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

Finding 4, second half — `templates/config.md:173-177`, replacing the clause
*and a refusal that names what to write is answered by the next person to read
it*:

```markdown
It is a refusal rather than a prompt because the command runs unattended — the
sealer asks nobody anything — and a refusal that names whose the row is and
where it is answered reaches that person through whoever read it, where a
question stops a session that may have nobody at the keyboard.
```

Finding 5 — `skills/verify/scripts/broad_gate.py#not_as_written`, the trailing
`&` branch:

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

Finding 5, second half — `overview.md` §*Not verified*, replacing the
sentence asserting POSIX semantics everywhere:

```markdown
The refusal is a string test over the row's value and reaches no shell, so it
raises the same way on every platform. What it SAYS a shell does is `/bin/sh`
semantics: under `cmd.exe` a trailing `&` separates commands rather than
backgrounding, and backticks and `$(…)` are literal characters. Unmeasured on
this branch; the `windows-latest` job is where one run settles it.
```

Finding 6 — `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
the helper and the refused loop:

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

Finding 7 — `tests/test_first_setup_asks_once.py`, using the `paragraph()`
helper the module already ships. The same change applies at `:163` and `:190`:

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

Finding 8 — the assertion the docstring already promises, added at
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:210`:

```python
    for form in ("backticks", "`$(…)`", "trailing `&`"):
        assert form in bullet, (
            f"the config skill does not name {form}, so somebody reading it "
            "does not learn the refusal exists"
        )
```

Finding 9 — two edits. `skills/verify/scripts/broad_gate.py#missing_row`:

```python
        "there is no command to seal over — and choosing one is not this "
        "session's to do. There is no default because a row is a thing a "
        "person wrote, and what the sealer's seal covers is exactly that "
```

And `tests/test_one_word_one_meaning.py`, into `SEAL_SWEPT`:

```python
    # The message a session reads when the row is absent says what the
    # sealer's seal covers, and said it ownerless until #402's round 1. The
    # list was closed where somebody had looked, for the third time.
    ("skills", "verify", "scripts", "broad_gate.py"),
```

Needs a fix: yes — findings 1 through 9; the ⬜ corrections are not counted.
Loses a record or crashes: no

## Proof

Files opened for this round:

- `skills/verify/scripts/broad_gate.py` — `missing_row`, `wholly_substituted`,
  `not_as_written`, `broad_command`, `first_command`, `compare_at_base`,
  `quote`, `gate`, `main`, and the module header
- `hooks/config.py` — `config_rows`, `CONFIG_ROW`, `seal_home`
- `templates/config.md`, `skills/config/SKILL.md`,
  `skills/implement/orchestration.md`, `skills/code-review/orchestration.md`,
  `agents/sealer.md`
- `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `tests/test_first_setup_asks_once.py`,
  `tests/test_the_rules_have_one_owner.py`,
  `tests/test_one_word_one_meaning.py`
- The work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `changelog.md`, `survivors.md`, `routing.md`, `phases/phase-1.md` and
  `phases/phase-5.md`
- `seal/ledger.md` (the rows this branch moved), `seal/ledger/` this work
  item's fragment, `seal/config.md`
- `CLAUDE.md`, `docs/review-chain-spec.md`,
  `skills/code-review/scripts/round_record.py`
- #402, #401 and pull request #412, in full

Not opened: the rest of `tests/`, `docs/` beyond the section cited, and the
release history.
