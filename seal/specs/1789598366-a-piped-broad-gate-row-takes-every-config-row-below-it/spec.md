# Feature Specification: a piped broad gate row takes every config row below it (#415)

<!-- seal/specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## What is wrong, in the order the causes run

One regex decides what a row of `seal/config.md` is, and it disagrees with the
format the file is written in.

```
| Broad gate | bin/test -q | tee out.txt |      a person writes this
        ↓
hooks/config.py#CONFIG_ROW matches a cell as [^|]*?
        ↓ the cell ends at the first `|`, so the line is not a row
config_rows stops reading — "any other line ends the table"
        ↓
every row BELOW it is gone, with no message anywhere
        ↓ and two things then act on a file they cannot see
broad-gate says the `Broad gate` row is ABSENT       ← a true message, wrong cause
seal mode finds no `Mode` row and inserts a second one ← read, measured in phase 1
```

The stop rule is not the defect. `config_rows`'s docstring and the two review
rounds behind it (round 1 🟡 6 and round 2 🟡 5, recorded in
`tests/test_the_pull_request_language_is_the_repositorys.py#items`) put it
there so that prose and a second table below this one are not read as more of
it. What is wrong is that a line a person wrote *as a row* is classified as
*the end of the table*, and the two are indistinguishable to the caller.

**The escape is markdown's, not this row's.** `seal/config.md` is a markdown
document, `\|` is how a markdown table cell carries a literal pipe, and
`templates/config.md` already writes its own cells that way — the pipe row of
its allowed list is spelled `bin/test -q \| tee out.txt` and relies on the
renderer to show one pipe. So a reader that honours `\|` is the generic table
reader agreeing with the format it claims to read. #415 prices this option as
*one row's shell semantics entering a generic table reader*, and that pricing
is wrong: no shell semantics are involved, and any cell of any row can need a
literal pipe.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §*The opt-in signal is the root itself* | The `Mode` row records an answer and decides nothing about opting in. Nothing added here may make the reader's answer feed back into whether a repository is opted in |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The two ledger claims this change falsifies are REMOVED where they stand and rewritten into this work item's own fragment |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | Three parties read this table. Every sentence this work writes says which one it is about |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class — *readers of the `\| Item \| Value \|` table that cannot carry a literal pipe* — and the class is enumerated below, not fixed at the coordinate #415 points at |
| `skills/agent-contract/SKILL.md` §14 | `missing_row`'s sentence is what a person meets. A change to it ships with the case that pins the new text |
| `skills/agent-contract/SKILL.md` §15 | Every case here is seen red before it is committed, against the mutation its phase names |
| `skills/verify/SKILL.md` §*The Seal Test* | A case whose fixture is well-formed cannot see a reader that mis-reads a malformed one. Each case's own assertion must be able to fire before its fixture's guard does |
| `templates/config.md` §*Choosing a value — the criterion* | A pipe satisfies the criterion. Nothing here restricts what a broad command may be |

## Scope

### In

1. **`hooks/config.py#CONFIG_ROW` learns markdown's escape.** A cell may
   carry `\|`, and `config_rows` puts one literal pipe into the value. The
   row's item cell learns it on the same terms, because the regex describes a
   cell and not a column.
2. **The writer keeps step with the reader.**
   `skills/implement/scripts/seal.py#table_span` reads the same constant, so
   the change reaches it; what this work owes is the case that pins the two
   still agreeing about which line is the `Mode` row. Their disagreement is
   what `with_row` turns into a second `Mode` row in a person's file.
3. **A line that will not parse is named rather than treated as the end of
   the table.** `hooks/config.py` gains a pure reader that reports the first
   line refused *after the table had begun*, and
   `skills/verify/scripts/broad_gate.py#missing_row` uses it: where the
   refused line's first cell is `Broad gate`, the refusal says the line will
   not parse and quotes it as written, in place of *has no `Broad gate` row*.
   Same exit 2, same moment, a different sentence.
4. **The fourth copy of the loop is closed.**
   `tests/test_the_pull_request_language_is_the_repositorys.py#items` calls
   the one reader instead of reimplementing it.
5. **The documents that promise the old behaviour change with it** —
   `templates/config.md` §*What is refused, and what stays allowed*,
   `skills/config/SKILL.md`, the changelog fragment, and this work item's
   ledger fragment.

### Out, and why each

| Out | Why |
|---|---|
| `hooks/mode-gate.py` gains no message and no refusal | It is a `PreToolUse` hook, so a wrong refusal there stops a session with nobody able to get past it. Its own docstring says everything in it fails toward silence, the way `hooks/optin.py` does. This is the caller a wrong refusal costs most, and it is the one caller this work leaves exactly as it is |
| An **unescaped** pipe is not made to work | Accepting it means a greedy last cell, whose failure scenario is in `plan.md`: a three-column table written under this one would be absorbed as rows of it, and `templates/config.md` ships three-column tables |
| Skipping an unparseable line and reading on | It re-opens the two findings the stop rule was written for, in both copies of the loop. The defect being repaired here is a silence, so a repair that adds a second silence is the wrong direction |
| Refusing a pipe, or restricting what a broad command may be | The row is an arbitrary shell command line by design, and `templates/config.md` §*Choosing a value — the criterion* already settled that a pipe stays legal. `broad_gate.py#not_as_written` returns None for a piped value and keeps doing so |
| A schema for `seal/config.md`, or a general markdown-table parser | `skills/config/SKILL.md` §*What this does not do* refuses a schema by name: a generic setter invites a short document to drift into key-value settings |
| `hooks/routing.py`'s table and `templates/parity.md` | Different tables with different readers. Nothing here reaches either, and `evidence_check.py` only asks whether `parity.md` exists |
| The language rows gaining a code reader | `Record language` and `Commit and pull request language` have none today — read, and stated as a claim rather than a measurement in `questions.md` M2. Giving them one is a different work item with its own frame |
| Markdown's other in-cell escapes | Only `\|` is what makes a line stop being a row. The rest render as themselves and cost nothing |
| A sweep of every `seal/ledger.md` anchor this branch drifts | Only the rows whose **claims** this change makes false are touched. Drift alone is the mechanism firing correctly |
| A pull-request arm that reports a malformed `seal/config.md` | The message arrives at whoever runs `broad-gate` or opens the front door, and nowhere else. Adding a CI arm is a change to a gate, which `CONTRIBUTING.md` asks its own argument for |

## The class, enumerated by construction

Every reader of the `| Item | Value |` table in this tree, found by grepping
for `config_rows`, `CONFIG_ROW` and the header regex rather than by recalling
them:

| Reader | Asks for | What this work does to it |
|---|---|---|
| `hooks/config.py#config_rows` | every row | **repaired** — the one production reader |
| `hooks/config.py#declared_mode` | `Mode` | inherits the repair; unchanged in itself |
| `skills/implement/scripts/seal.py#table_span` | the `Mode` row's index | inherits the repair through the shared constant, and gains the case that pins the agreement |
| `skills/verify/scripts/broad_gate.py#broad_command` | `Broad gate` | inherits the repair; its refusal's **sentence** changes |
| `hooks/mode-gate.py#undeclared` | `Mode`, through `declared_mode` | inherits the repair and nothing else, deliberately |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` | every row | **closed** — it calls the one reader |

The sixth is why this cannot be left as it was. It agrees with `config_rows`
today; after the repair it would disagree about a real input, which is the
exact state `hooks/config.py`'s own docstring says the module exists to
prevent — *a file that one of them parses and the other does not*. Closing it
also settles a deferral standing since work item
`1788817289-local-mode-from-first-setup-to-the-gate`, whose `overview.md`
named it with the repository owner as answerer.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given a four-row table whose second row is a `Broad gate` row written with `\|`, and `Mode`, `Record language` and `Commit and pull request language` beneath it, when `config_rows` reads it, then **four rows come back** and the `Broad gate` value holds one literal pipe | a case over `hooks/config.py#config_rows`, red when `CONFIG_ROW`'s cell is reverted to `[^\|]*?` — red on the **count**, not only on the value |
| A2 | Given that same file, when `broad_gate.py#broad_command` reads it, then it returns the command with its pipe, and `not_as_written` still returns None for it | a case over both units together, so the pipe is shown to survive the whole path a value takes before a shell sees it |
| A3 | Given a config whose `Mode` row sits **below** a `Broad gate` row written with `\|`, when `seal mode shared` runs, then the file holds exactly one `Mode` row afterwards | a case that counts `Mode` rows in the written file; red against the reverted regex, where the row below is invisible to `table_span` |
| A4 | Given a config carrying a line that begins with `\|`, sits under the header, and still will not parse — an **unescaped** pipe is the shape to use — when `broad-gate` runs, then it exits 2 and says **that line will not parse as a row**, quoting it, and does **not** say the row is absent | a case asserting both halves of the sentence, red when the new branch in `missing_row` is deleted (§14) |
| A5 | Given a config with no `Broad gate` row and no unparseable line at all, when `broad-gate` runs, then the message is the absent-row refusal exactly as it reads today | the existing refusal cases stay green; this pins that the new branch did not swallow the old message |
| A6 | Given any config file already in this tree or in the test corpus, when read before and after the change, then `config_rows` returns the same rows | phase 1's measurement, recorded with its population — this is the *nothing else moved* half |
| A7 | Given `hooks/mode-gate.py`, when a config carries an unparseable line, then the hook writes no new message and denies nothing it did not deny before | a case over `undeclared`, asserting the hook's answer is still `""` or the home and never a refusal string |
| A8 | Given the test module's own reader, when the suite runs, then exactly one implementation of the loop is loaded | the `__code__.co_filename` assertion `tests/test_the_mode_question_is_asked_once.py#test_the_command_and_the_gate_read_one_parser` already uses for `seal.py`, extended to the test copy |
| A9 | Given `templates/config.md` §*What is refused, and what stays allowed*, when a reader opens the pipe row, then it states how a pipe **is** written and no longer says a pipe cannot reach the row | the two cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py` that assert the old sentences change with it, in the same commit |

**A6 is the one that can come back inconvenient.** It asks for *no other
change*, and a regex that widens what parses can only ever make more lines
into rows. If the measurement finds a file whose reading moves, that is a
divergence row in `overview.md` with the file named — not a reason to weaken
A6 into something that passes.

## Data & interfaces

| Coordinate | What changes |
|---|---|
| `hooks/config.py#CONFIG_ROW` | the cell pattern, both cells, escape-aware |
| `hooks/config.py#config_rows` | unescapes `\|` into the value it returns; its stop rule, its signature and its return shape are unchanged |
| `hooks/config.py` | gains one pure reader that reports the first refused line. It denies nothing and raises nothing, so no caller becomes able to refuse by importing it |
| `hooks/config.py#declared_mode` | unchanged |
| `skills/implement/scripts/seal.py#table_span`, `#with_row` | unchanged in source; both read `CONFIG_ROW` through the alias, so the repair reaches them |
| `skills/verify/scripts/broad_gate.py#missing_row` | gains a branch and a second sentence |
| `skills/verify/scripts/broad_gate.py#broad_command`, `#not_as_written` | unchanged |
| `hooks/mode-gate.py#undeclared` | unchanged |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` | removed, and its callers point at `hooks/config.py#config_rows` |
| `templates/config.md#"## Broad gate"` | the allowed list's pipe row |

**Two ledger claims go false and are handled as removals.** Both are in this
release's own fragments rather than in the shared file:

- `seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md`
  carries a row whose claim is *a pipe … cannot reach the row at all … and it
  takes every row below it*. After this work the escaped spelling reaches the
  row, so the claim is false.
- The same fragment cites two test units whose **names** state the old
  behaviour. A record naming a unit the tree lacks is refused by
  `evidence-check`'s records arm, and a refused record takes even the
  non-strict run to exit 2, so a rename and the fragment edit are one commit.

`CLAUDE.md` is the rule for both: the row is removed where it stands and the
new claim is written into this work item's own fragment. Nothing is
re-pointed.

## What this repair cannot see

Stated here so nobody reads the change as wider than it is.

- **A pipe written without the escape still is not a row.** What changes for
  that person is the message, not the outcome. The naive spelling — the one
  somebody typing *one shell command line* reaches for first — still fails,
  and now says so.
- **`hooks/mode-gate.py` still says nothing.** A config whose `Mode` row is
  hidden below an unparseable line still reads as undeclared, and the gate
  still simply asks the mode question again. That is deliberate and it is the
  cost of keeping a `PreToolUse` hook silent.
- **Every other way a row goes missing is unchanged.** A row above the
  header, a row after a blank line, a row in a second table — all still
  invisible and still silent. The stop rule stays; only its
  misclassification of an escaped pipe goes.
- **Nothing checks a repository's `seal/config.md` at a pull request.** The
  new sentence reaches whoever runs `broad-gate` or opens `/specseal:config`,
  and reaches nobody else.

## Open questions → questions.md

One row needs a person: whether the `Broad gate` cell is a markdown cell that
takes markdown's escape, or a shell line that simply may not hold a pipe. The
two answers build different code, so it blocks. Two rows are measurements and
one belongs to the work; none of the three waits on anybody.

Framed 2026-09-17 by framer, before the build.
