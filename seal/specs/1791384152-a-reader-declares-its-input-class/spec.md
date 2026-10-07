# Feature Specification: a reader declares its input class (#835)

<!-- seal/specs/1791384152-a-reader-declares-its-input-class/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | both checks run with nobody asked; a check that reads a person's sentence is the guess class the inventory counts as the shape that reopens, so neither check reads one |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | where #835 says the two rules are stated; each gets a bullet there that links to its home |
| `CONTRIBUTING.md` §*House rules* › *A change writes a fragment, never a shared registry* | why the registry is not a table every change edits; three branches once conflicted on one shared file, and eleven are open this release |
| `docs/the-record-layout.md` §*docs/*, §*The size a reader takes whole*, §*A change writes fragments, never a shared file* | what a `docs/` document is (standing policy), the 1,000-line ceiling, and the fragment rule the registry's shape has to satisfy |
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | the coordinate grammar a `## Removes` row writes, and the rule that the checker calls git for nothing, which bounds what the Removes judgment can read |
| `skills/settle/SKILL.md` §*2. Write one standing statement per segment* | a new `docs/` document is created only for an area that has none; the statement shape with `Enforced by:`; `Enforced by: nothing — <why>` as the shape a rule nothing reads takes |
| `templates/config.md` §*The fold's values*, §*The ledger freeze* | the cutoff-row pattern `Removes from` copies: a work-item id, absent means not checked, an unparsable value is refused naming the row |
| `seal/follow-up.md`, the preamble | a thing tied to a coordinate lives at the coordinate and `grep` is the list that needs no file kept in sync; this is why the registry is the code's own docstrings |
| `skills/implement/SKILL.md` §*5. Incorporate review* | what a mechanism is, for rule 2: a rule, a checker, a template section, a walk |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | enumerate the class; a change to what a person sees is documented and pinned in the same commit; a case is seen red before it is planted |
| #834 `spec.md` §*What the table says* and `inventory/6-tests.md`, `7-records.md`, `8-evidence.md` (branch `chore/834-every-reader-and-record-is-inventoried`) | the counts both rules rest on; part 7 rows 8, 9, 16, 28 and 29 are the precedents the two mechanisms copy |

Two tests are the precedents the registry check copies, and both are cited by
path so the build opens them: `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`
(an AST walk over every tracked `.py`, a list K1 of calls found by
construction, an `ALLOWED` table whose every entry carries its grounds, and a
failure that names the site and the repair) and
`tests/test_every_reader_ends_a_line_where_gfm_does.py` §*S19* (every
`.splitlines(` call in shipped code held to a frozen list keyed `(path, unit)`,
red for a call the list does not name and for a named unit that no longer
makes one).

## Scope

**In.** Two rules, each with the one check that holds it, and the document
that states them.

1. **A reader declares its input class, in its own docstring.** The registry
   is the code: every unit the population rule below names carries one line
   `Reads: <class> — <what it reads>; unknown <direction>`. A test walks the
   AST, finds the population by construction, and refuses a unit with no
   declaration, a declaration outside the vocabulary, and a census line (the
   transition, below) whose unit has changed or gone.
2. **A mechanism names one it removes, in `spec.md`.** A `## Removes` section
   in the frame's own file holds coordinates in the ledger's grammar, or the
   one line `nothing — <why>`. The records arm of `evidence-check`, which
   already reads every live work item's `spec.md` on every ledger run, reads
   a row's coordinate as a claim of absence: one that still resolves at HEAD
   is a finding. Where `seal/config.md` declares `Removes from`, a live
   `spec.md` of a work item at or above it must carry the section.

The population, the vocabulary, the census, the section's shape and what
neither check can read are each decided below, and `docs/the-reader-registry.md`
is their permanent home.

**Out, and why.**

- **A table under `docs/`, which the ticket's wording asked for.** Four
  grounds, each in the tree. The ceiling holds every top-level `docs/*.md` to
  1,000 lines and the inventory is 2,287 lines across eight parts, part 6
  alone 986; a subdirectory dodges the ceiling's letter (`fold-check` reads
  the top level only) and not its reason. A table every reader change edits
  is the shared file the house rule refuses, and eleven branches are open on
  this release. A table beside the code is a second copy of a judgment the
  docstring can carry once, which is the shape #834 found disagreeing with
  itself. And the table is itself a guess-class reader: its own parse of the
  `Class` column read 1,381 of 1,467 rows, the rest wrapped or quoted a pipe.
  The `docs/` home is therefore the rule, not the rows.
- **Test functions.** A test pin's class is its assertion's shape, by the
  inventory's own rule in `inventory/6-tests.md`: a presence pin is `guess`,
  `refused`; an absence pin is `guess`, `passed`. A declaration on a pin adds
  nothing a reader of the assertion does not already have. The four helper
  modules the inventory counts as code (`tests/conftest.py`,
  `tests/block_shapes.py`, `tests/commonmark_oracle.py`,
  `tests/gfm_table_oracle.py`) are in the population. The pins' growth is
  real — 3,817 `assert "<text>" in …` and `not in` assertions in 151 test
  files at this frame's tree, executed by the framer's probe on 2026-10-08
  — and it is held by rule 2 where a frame names a pin it removes, and by
  nothing else here. `§12 enumerate the class` is why the number is stated
  rather than guessed.
- **`bin/` and the shell steps of `.github/workflows/*.yml`.** No AST; the
  inventory's rows for them (part 5) stay what they are, a reading.
- **A ratchet on the `guess` count.** It cannot be set before the count is
  known, and the count is known only once the census below is empty, which
  is #834's build. Whether a `Reads: guess` then costs a removal is the
  repository owner's decision, taken with the count; this item prints no
  number and pins none, because a count pinned in prose is the shape
  `inventory/6-tests.md` §*Observations* names as a reader of a sentence.
- **Re-reading whether a declaration is still true.** Nothing re-reads a
  class once written, the way nothing re-reads whether an `Enforced by:`
  target still enforces its sentence (part 7 row 8). The warden reads the
  diff's `Reads:` lines at review; that is where a `guess` is argued.
- **Siblings' units.** The build changes no reader's body. Which units each
  sibling changes is its own `plan.md`; the seams are in this item's.

## The decisions

### The registry is the code, and `docs/` holds the rule

A declaration lives where a `# RIDER:` lives: at the coordinate, so that
opening the unit is what finds it and `grep -rn "Reads: guess"` is the list.
`docs/the-reader-registry.md` is the one document for the area, created
because none owns it (`skills/settle/SKILL.md` §2): it states the vocabulary,
the grammar, the population, the census and the `## Removes` section, each
as a standing statement with its `Enforced by:` line, and it records the
counts at landing as the reading of a moment, not as a pin.
`docs/the-record-layout.md`'s *docs/* table gains its row, and
`CONTRIBUTING.md` §*What a change to a gate must carry* gains two bullets that
state each rule in one sentence and link here.

### The vocabulary, and the grammar the check reads

The classes are the inventory's three with one more for a matched unit that
reads nothing it decides from:

| Class | Means |
|---|---|
| `owned` | a format this repository's own writer produces, or a vocabulary its own checker defines |
| `observed` | a fact asked of the system — an exit code, an AST, `git ls-files`, a JSON a program wrote, an attempted call |
| `guess` | a person's text, or a shape predicted from text the reader does not control |
| `nothing` | the unit calls a primitive and decides nothing from what it reads — a writer, a formatter of its own output |

The direction is the inventory's: `refused`, `passed`, `mixed`.

```
Reads: <owned|observed|guess> — <what it reads, for a person>; unknown <refused|passed|mixed>
Reads: nothing — <why the primitive is not a reading>
```

One line per unit, anywhere in the unit's docstring, the class word first
after `Reads:` and the direction word last after `; unknown`. The check reads
the two words and nothing between them; the prose is the reviewer's. A unit
that reads several inputs declares the weakest class it reads, `guess` being
weakest. ` — ` and ` -- ` are both the separator, because the words are read
by position and the dash is not read.

### The population, by construction

Every top-level `def` and `class` in `hooks/*.py`, `hooks/git/*.py`,
`skills/*/scripts/**/*.py`, `.github/scripts/*.py` and the four helper
modules under `tests/`, whose body — methods and nested functions included —
calls a primitive from the test's own list K1, or reads `os.environ`,
`sys.stdin` or `sys.argv`. K1 is two families, each closed by construction:

- **the process boundary** — `open`, `read_text`, `read_bytes`, `read`,
  `readline`, `readlines`; `subprocess.run`, `check_output`, `check_call`,
  `call`, `Popen`, `getoutput`, `getstatusoutput`, `os.popen`; `os.getenv`;
  `listdir`, `scandir`, `walk`, `glob`, `iglob`, `rglob`, `iterdir`;
  `exists`, `isfile`, `isdir`, `lexists`, `stat`;
- **a standard-library parser handed text** — `match`, `search`,
  `fullmatch`, `findall`, `finditer`, `sub`, `subn`; `shlex.split`;
  `json.load`, `loads`; `ast.parse`; `tomllib.load`, `loads`;
  `xml.etree` `parse`, `fromstring`; `csv.reader`, `DictReader`;
  `splitlines`.

Methods are matched by attribute name whatever the receiver, because a
compiled pattern is called on a name; `split` is matched only on `shlex`,
because `str.split` is everywhere. Measured by the framer's probe on
2026-10-08 over this frame's tree: 1,521 top-level units, **654 in the
population** (hooks 168, skills 359, `.github/scripts` 105, test helpers 22),
102 of them with no docstring at all; the inventory rowed 680 code readers at
a finer altitude, so the two numbers are the same class seen from two
heights. A call K1 does not know is a row to add to K1, never an exemption
(the encoding test's rule). What no row can hold, stated rather than left to
be found: a unit that decides from text another unit read, with `==`, `in` or
`startswith` and no primitive (the inventory's `understood`-shaped rows). Such
a unit declares voluntarily — the check accepts a `Reads:` line on any unit —
and is otherwise read through the unit that read the text for it.

### The census is the transition, and it only shrinks

`tests/undeclared_readers.txt` holds one line `path#unit@hash` for every
population unit undeclared when the check lands, the hash computed by
`evidence_check.content_hash` over the span `evidence_check.py_spans` gives,
imported and not copied. A unit on the census with its hash unchanged is not
required to declare; one whose hash moved was changed, and the check says
*declare it and remove its line*; a line naming no undeclared population unit
— gone, renamed, declared since, or no longer calling a primitive — is
refused naming the line. A malformed line is refused by the grammar. When the
file is empty the check says to delete it, and with no file it reads no
census. #834's build empties it (below); until then the rule binds every new
unit and every changed one, which is the half of the inventory's finding that
costs: the families that reopened were readers being changed.

### `## Removes`, read by the records arm

`templates/sdd-spec.md` gains the section above the framer's mark:

```markdown
## Removes

| Removes | Coordinate | Where it lands, or why it can go |
|---|---|---|
| <a copy, a reader, a rule sentence, a test pin> | <path#unit, or path#"heading"[>"line"]> | <the file or record that now owns it, or why nothing needs to> |
```

or the one line `nothing — <why>`, with the reason not empty (the
`Enforced by: nothing — <why>` rule). The coordinate is the ledger's
grammar without a hash: a function or class for code, a heading path for a
document, an optional `>"quoted line"` narrowing to one sentence. The
records arm (`evidence_check.py#file_claims`, through `claim_lines`) reads the
rows under this heading as claims of absence and under no other rule: a
coordinate that resolves at HEAD by `resolve_unit` is a finding, `STANDING`,
graded as a stated name the tree does not carry is graded today; the names
on those lines are not read by the name half. A row whose coordinate cell is
not a coordinate is refused naming the row, so the template's placeholder
fails until it is filled, the way `## Not verified`'s does. The section is
read wherever it is present; where `seal/config.md` declares
`Removes from | <work-item id>`, a live `spec.md` at or above it with no
section, or an empty one, is a finding. The row is documented in
`templates/config.md` beside `Ledger frozen from`, whose reader it copies:
absent means not checked, a value that is not a work-item id is refused
naming the row. This repository sets the value at the build, to the epoch
second the row is written, so every 0.21.0 work item framed before it stays
unbound and every later frame is bound.

Why the records arm and not a new script or `unverified-check`: the arm
already opens every live `spec.md` on every ledger run — the advisor after
each commit, CI's evidence job, the broad gate under `--strict` — and it is
the reader that would otherwise refuse a correct removal as a stale name
(`coordinate_misses` reads a `path#name` by token of the file, so a removed
unit is a miss). One reader of the section, no git, no new hygiene step. What
it cannot read: that the coordinate ever existed, so a misspelled one passes
as gone — the warden opens the row at the base at review; and the `<why>` of
a `nothing` row, which the warden reads too.

### What this item removes

The per-phase table `templates/sdd-phase.md` §*What this phase removes*
(`| Removed item | Where it must land |`) and its pins in
`tests/test_a_phase_hands_the_next_one_a_record.py`. It recorded one fact —
what a work item takes out of the tree and where it lands — per phase, filled
by the builder, held to its shape by a template pin, its content read by the
next phase at most and drifted by nothing any check tracks (part 7 row 16:
*none tracked*). The
`## Removes` section records the same fact once, at the frame, with a check
that reads it; a removal a phase makes that the frame did not name is a
divergence and goes where divergences go, `overview.md`'s table. Two records
of one fact is the shape #834 found disagreeing with itself. Phase records
already written keep their tables; they are records of a moment.

### What #834's build does with this frame

The home the table moves into is the code: for every inventory row whose
unit is in the population, #834's build writes the row's `Class` and
`Unknown` into the unit's docstring as its `Reads:` line and removes the
unit's census line; for a rowed unit outside the population it writes the
line too, voluntarily. The inventory's other columns — `Decides`,
`Duplicates`, `Note` — are the reading of a moment and stay under
`inventory/` in #834's directory, read at the release tag after the
directory retires. `skills/settle/scripts/settle.py#PROCESS_DIRS` does not
list `inventory`, so whether it leaves with the process record or with the
fold is #834's spec to say. The build lands after every other 0.21.0 chain
and after this item, because it touches most reader files and the census has
to exist first.

## User scenarios & acceptance *(mandatory)*

Rule 1, the registry check (`tests/test_a_reader_declares_its_input_class.py`):

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| R1 a new reader is undeclared | Given a planted root with a top-level unit that calls a K1 primitive and carries no `Reads:` line, when the check runs, then it fails naming `path#unit`, the grammar, and that a pre-existing unit's repair is its census line | the planted case; seen red first against this tree with one census line removed |
| R2 a declaration outside the vocabulary | Given `Reads: maybe — …` or a class line with no `; unknown <word>`, then it fails naming the unit and the two words it reads | planted cases, one per defect |
| R3 a census unit changed | Given a census line whose hash is not the unit's, then it fails: *declare it and remove its census line* | planted root with a census file |
| R4 a census line names nothing | Given a line for a unit that is gone, renamed, declared since, or no longer in the population, then it fails naming the line | planted cases, one per cause |
| R5 a voluntary declaration | Given a unit outside the population with a well-formed `Reads:` line, then it passes and is counted | planted case |
| R6 the census grammar | Given a line that is not `path#unit@hash`, then it is refused naming the line; given an empty file, the check says to delete it; given no file, no census is read | planted cases |
| R7 the primitives | Given one planted unit per K1 family (boundary call, `os.environ`, `sys.stdin`, a parser call, `shlex.split`, and `str.split` which must NOT match), then each is in or out of the population as the rule says | parametrised planted cases |
| R8 this tree passes | Given this repository at landing, then every population unit is declared or on the census, and the census hashes are the tree's | the real-tree case |
| R9 the failure is the instruction | Given each failure, then its text is pinned whole, names the site and the repair, and the test's docstring states what the walk cannot see (§14, the encoding test's shape) | the pins |

Rule 2, the `## Removes` section (`evidence-check`'s records arm):

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a named removal still stands | Given a live `spec.md` with a row whose coordinate resolves at HEAD, when `evidence-check` runs, then it reports `STANDING` with the coordinate, graded like a stated name the tree lacks | planted root with a ledger fragment; `bin/evidence-check` exit |
| S2 a removal that happened | Given a row whose coordinate names no unit at HEAD, then no finding, and no name on that line is read by the name half | planted root; the unit's name absent from the tree |
| S3 the `nothing` line | Given `nothing — <why>`, then no finding; given bare `nothing`, then refused naming the line | planted cases |
| S4 presence under the cutoff | Given `Removes from | N`, a live item at or above N with no section or an empty one fails naming the file; one below N is read where present and not required; with no row, presence is not checked | planted roots, one per branch |
| S5 the row's grammar | Given a coordinate cell that is not a coordinate (the template's placeholder), then refused naming the row | planted case |
| S6 the row refuses an unreadable value | Given `Removes from | 17x`, then exit 2 naming the row, in the `Ledger frozen from` shape | planted case |
| S7 quoted rows are not read | Given a row inside a fence or an HTML comment, then not read (`claim_lines`) | planted case |
| S8 the templates | Given `templates/sdd-spec.md`, then it carries the section above the mark and the mark is still last; given `templates/sdd-phase.md`, then it carries no *What this phase removes* section and no test pins one; `agents/framer.md`'s writes table and report list name the section | the pins moved in the same commit |
| S9 this item's own row | Given this `spec.md`, then its `## Removes` row names the phase template's section; the arm as it stands reads no quoted locator (`RECORD_COORD_RE`), so the row is silent until phase 2 teaches the arm, reports `STANDING` while the template still carries the section, and is clean once phase 2 removes it | `bin/evidence-check .` at a probe commit inside phase 2, before and after the template edit |

The document and the rules' statement:

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| D1 the home | Given `docs/the-reader-registry.md`, then every statement is a bold rule with grounds and one `Enforced by:` line, under the ceiling, and `fold-check` passes | `bin/fold-check`; `tests/test_a_folded_statement_names_what_enforces_it.py` |
| D2 the rules are stated once | Given `CONTRIBUTING.md` §*What a change to a gate must carry*, then two bullets name the rules and link to the home; `docs/the-record-layout.md` §*docs/* has the row; `templates/config.md` documents `Removes from`; `seal/config.md` carries it | the text hygiene tests the brief names, and `tests/test_no_passage_is_pasted_into_a_second_file.py`'s ratchet unchanged |

## Data & interfaces

- `tests/undeclared_readers.txt` — one `path#unit@hash` per line, sorted by
  path then unit, LF-ended; the hash is `evidence_check.content_hash` over
  the `py_spans` span, eight hex characters. Read by the registry check only.
- `seal/config.md` row `Removes from | <work-item id>` — read by
  `evidence_check.py`'s records arm through the one config reader the tree
  has when the build lands (sibling #867 is making it one).
- `spec.md` `## Removes` — the table above or `nothing — <why>`; read by the
  records arm.
- The docstring line `Reads: …` — read by the registry check; written by
  whoever writes or changes a population unit, and by #834's backfill.

## Removes

| Removes | Coordinate | Where it lands, or why it can go |
|---|---|---|
| the per-phase removal table, a second record of what a work item takes out of the tree | `templates/sdd-phase.md#"## What this phase removes"` | this section, at the frame; a removal the frame did not name is a divergence row in `overview.md` |

## Open questions → questions.md

Framed 2026-10-08 by framer, before the build.
