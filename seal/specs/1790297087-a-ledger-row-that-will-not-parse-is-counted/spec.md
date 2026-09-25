# Feature Specification: a ledger row that will not parse is counted

<!-- seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Work item E of `release: 0.15.4` (milestone 46): #299 and #322, the ledger
checker's silences. A patch release: fixes to instruments, no new gate, and
every refusal added enforces a rule a document already states.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* — "Only the major level can be broken" and "`BROKEN` means *go edit the ledger*" | `BROKEN` is reserved for a unit that is not there. A coordinate the checker cannot even read names no unit, so it is not a `BROKEN` row. Grounds for a verdict of its own |
| `skills/evidence-check/SKILL.md` §*Verdicts and what to do*, the `OLD-FORMAT` row, and `evidence_check.py#old_format_rows`'s docstring — "Its own verdict, not folded into BROKEN, because the remedy differs — and it fails the run with or without `--strict`: a red build saying 'run the migrator' beats a green build checking nothing" | The precedent this work follows shape for shape: the other coordinate the anchor pattern refuses already has its own verdict, its own count printed at zero, and exit 2 under either reading. A malformed coordinate is the same silence with a different remedy |
| `evidence_check.py`, the comment above `OLD_COORD_RE` — "the one unacceptable outcome is silence" | The rule #299 measures being broken, stated in the file being fixed |
| `skills/evidence-check/SKILL.md` §*Verdicts and what to do*, the `UNREADABLE` row | `UNREADABLE` is already a verdict (records arm, a record or directory that could not be opened). #299's suggested name would give one word two meanings, so the new verdict is `MALFORMED` |
| `skills/evidence-check/SKILL.md` §*Known limits*, "Every row the check calls `BROKEN` or `DRIFTED` gets a line back from `--reverify`, whether or not it could heal it. Silence there reads as a heal that happened" | `--reverify` names every `MALFORMED` row it leaves. Today it reports `0 rows re-verified` over them (#299, instance 1) |
| `skills/evidence-check/SKILL.md` §*A row inside a fence is an example, not a claim* (#444, shipped in 0.15.3) | The new arm reads through `unquoted(text)` like every other ledger walk: a closed fence is skipped; an unclosed fence, an HTML comment and an indented block are read. **This rule is not re-opened** |
| `templates/ledger.md` §*Coordinates* — "The hash is eight hex characters", "Escape a pipe inside a quoted anchor as `\|`" | What a well-formed coordinate is, and where the missing quote-escape sentence goes (see *The live instances* below) |
| `templates/ledger.md`, the `\| Clause \| Code grounds \| Verified behavior \| Checked \| Notes \|` header, and `docs/the-evidence-ledger.md`'s paragraph on #501 — "A row under no header is counted against the five columns `templates/ledger.md` declares" | Where a row's coordinate lives: the `Code grounds` cell, which is the second cell of a fragment row that has no header |
| `CLAUDE.md` §*a change writes fragments, never the shared file* — "Appended is the word, and a removal is not one — nor is an edit" | Repairing a row in `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` is done in that file with a dated note; new rows go in `seal/ledger/1790297087-a-ledger-row-that-will-not-parse-is-counted.md` |
| `skills/implement/SKILL.md` §1, `seal/follow-up.md` — "this work may be that prerequisite. If so, include the item in this change and delete its row" | `seal/follow-up.md`'s row for #299's first instance is removed by this branch. #299's own *Housekeeping* paragraph said not to, because two work items in flight on 2026-09-09 touched that file; policy outranks the ticket, and that reason belongs to a moment that has passed |

## Scope

### What the defect is, located

Read, `skills/evidence-check/scripts/evidence_check.py` at `ca2afdb9`:

- `check_text` reads a ledger with `ANCHOR_RE.finditer`, and `old_format_rows`
  with `OLD_COORD_RE`. **A coordinate that matches neither is in no finding
  list at all**, so it enters no count. It is dropped in the parse; the walk and
  the count are innocent. This answers #299's first *Not verified* row.
- `ANCHOR_RE` wants a path holding `/` or `.`, a locator that is a dotted name
  or a quoted line with no unescaped `"`, and a hash of 6–12 lowercase hex.
  Any miss of any part drops the coordinate whole.
- `reverify` walks the same `ANCHOR_RE`, so it is silent over the same rows.
- `hooks/evidence-advisor.py#failing_rows` gets `check_ledger`'s findings and
  filters to `BROKEN` and `OLD-FORMAT`, so a new verdict would reach it and be
  dropped there, one reader further on.

### The live instances — this is an active trap, not a latent one

Executed by the framer on 2026-09-25, a scratch probe over every ledger the
checker reads (`seal/ledger.md`, 31 `seal/releases/*.md`, no fragments exist),
through the module's own `unquoted`: 1,112 table rows, 2,521 anchor matches.
In the `Code grounds` cells, after blanking `ANCHOR_RE` and `OLD_COORD_RE`
matches, **five coordinates are left over, and all five are real claims no
reader has ever checked**:

| File | Row's coordinate, as written | Why the pattern refuses it |
|---|---|---|
| `seal/ledger.md` | `tests/test_a_rider_reaches_its_file.py#"STAMP = re.compile(r"Verified …")"@05033bb1` | unescaped `"` inside a quoted locator |
| `seal/ledger.md` | `` hooks/cmdline.py#"EXPANDS = "$`*?[]{}""@6d56a043 `` (the cell's other anchors parse) | unescaped `"` inside a quoted locator |
| `seal/ledger.md` | `skills/code-review/scripts/chain_check.py#"SEPARATORS = " " + chr(0x2014) + …"@9750da73` (the cell's other anchors parse) | unescaped `"` inside a quoted locator |
| `seal/releases/0.4.0.md` | `.github/workflows/hygiene.yml#"echo "base is ${{ github.base_ref }} — …"; exit 0"@0cb0ca06` | unescaped `"` inside a quoted locator |
| `seal/releases/0.12.0.md` | `.github/scripts/claude_block.py#<module>@00000000` | `<module>` is neither a name nor a quoted line, and `00000000` is a placeholder. The same release file's row that recorded *Round 1's 🟡 4* repaired this exact coordinate in its own row; this sibling row was missed |

That answers #299's second *Not verified* row: five rows are being skipped
right now. The same probe also names what the arm must **not** refuse (see
*Must not be refused*).

`unescape` already turns `\"` back into `"`, so escaping is the repair for
the four quoted ones. Nothing documents that escape: `templates/ledger.md`
and `skills/evidence-check/SKILL.md` each name only `\|`.

### In

1. **A `MALFORMED` verdict** in `evidence_check.py`, produced by a function
   beside `old_format_rows` and called from `check_ledger` the same way.
   It reads **table rows only**, through `unquoted(text)`, and **only the
   `Code grounds` cell**: the column whose header cell is `Code grounds`, or
   the second cell of a row under no header. A row is `MALFORMED` where that
   cell:
   - (a) still holds a `#` or `@` after every `ANCHOR_RE` and
     `OLD_COORD_RE` match in it is blanked — a coordinate somebody wrote that
     the pattern refused, whatever part of it was wrong; or
   - (b) is not empty, holds no `ANCHOR_RE` match and no `OLD_COORD_RE`
     match, and sits in a row with some other non-empty cell. That is a row
     that claims something and cites nothing a reader can check.

   A row with every cell empty (the template ships one) is not a claim.
   The finding names the text as written, says it is not checked, and names
   the remedy. For a hash the remedy is the workflow the suite already pins
   (`test_an_ordinary_new_row_is_still_anchored_by_reverify`): write eight hex
   characters, `@00000000` will do, and run `--reverify`. For a quoted locator
   holding a `"`, the remedy is `\"`.
2. **The count a reader looks at moves.** `MALFORMED` joins `totals`; the
   per-ledger line and the `total:` line gain `· N malformed` after
   `old-format`, **printed at zero** like `old-format` is. The existing text
   up to `old-format` is unchanged, so `broad_gate.py#LEDGER_RE` and the
   cases asserting on substrings still read it.
3. **Exit 2 with or without `--strict`**, in `exit_code`, the `OLD-FORMAT`
   grading. Questions.md Q1 holds the one part of this the tree could not
   settle.
4. **`--reverify` names each `MALFORMED` row it leaves**, as a `LEFT` line
   with the reason, and returns 1 when it left one, the way it already
   returns 1 for an unreadable ledger. It does not heal one: see plan.md
   *Alternatives*.
5. **The commit advisor prints them.** `hooks/evidence-advisor.py#failing_rows`
   takes `MALFORMED` into its filter and `main` prints its own block, with its
   docstring saying so. It is the same filter `OLD-FORMAT` joined late
   (round 4, 🟡 6) and the suite pins that docstring.
6. **The five live rows are repaired** where they sit. Each is re-read
   against its code first. A claim that still holds gets its coordinate
   corrected, with `\"` or a real unit in place of `<module>`, then
   `--reverify` fills the hash and the row takes a dated note. A claim that
   no longer holds is corrected or taken out under `CLAUDE.md`'s rules, with
   the new claim going in this work item's fragment.
7. **Documents, in the commit that changes what they describe** (contract
   §14):
   - `skills/evidence-check/SKILL.md`: a `MALFORMED` row in *Verdicts and
     what to do*, the `--reverify` bullet names `MALFORMED` beside `BROKEN`
     and `DRIFTED`, and the escape sentence adds `\"`.
   - `templates/ledger.md`: the same escape sentence adds `\"`.
   - The comment above `ANCHOR_RE` says `\"` as well as `\|`.
8. `seal/follow-up.md`'s #299 row is removed.
9. **#322 is closed as already fixed**, and nothing is built for it. Read:
   `tests/test_a_row_points_by_content.py#test_an_old_format_ledger_is_loud_never_invisible`'s
   docstring became `r"""` in `97e29b7a` (#531, 2026-09-23), and the line
   the issue cites has moved from 763 to 823. Executed on 2026-09-25: every
   `git ls-files '*.py'` compiled under `python3 -W error` (3.12.11) gives
   **zero** errors, so the class the issue asked about is empty today. The
   pull request says `Closes #322` and gives these grounds.

### Must not be refused

Each of these is in this repository's ledgers today (the probe's other seven
leftovers, all outside a `Code grounds` cell) or in the template every
repository starts from:

- the notation row `| Coordinate notation | \`path#anchor@hash\` from the repo root |`
  in `seal/ledger.md` and `templates/ledger.md`, which sits under an
  `Item | Value` header;
- the template's empty `| | | | | |` row;
- a path-less shorthand such as `` `#analyse@e52dee1b` `` in a Notes or
  Verified-behavior cell (`seal/releases/0.9.5.md`, two rows), and a quoted
  malformed example in a Notes cell (`seal/releases/0.12.0.md`, one row);
- `path#unit@hash` written as notation in a Clause cell
  (`seal/releases/0.9.0.md`);
- the `Decision | Content | Grounds` scope-decisions table, which is not
  under a `Code grounds` header;
- anything inside a fenced block that closes.

### Out

- **#585**, whether `evidence-check` ships the cell-count refusal to every
  repository. The owner's product decision for 0.16.0, and the milestone
  leaves it out on purpose. This work edits the same file first; it counts no
  cells beyond locating `Code grounds`.
- **The records arm.** `check_records` reads stamps in `spec.md`, `plan.md`
  and the rest with the same `ANCHOR_RE`, so a malformed stamp in a record is
  also silently unread (`stamps_read` counts only matches). It is the same
  class in a different reader over prose, where there is no `Code grounds`
  cell to confine a rule to, and a rule over prose needs its own
  false-positive measurement. Answerer: the repository owner, as a new issue
  the orchestrator files if wanted.
- **`.github/scripts/rider_check.py`**, which reads `# RIDER:` stamps with
  its own copy of the hash width. Riders are not ledger rows. Not measured
  here; answerer: the repository owner, with the records arm.
- **`hooks/root-migrate.py`, `settle.py`, `fold_ledger.py`**, which read
  `ANCHOR_RE` to move or label rows rather than to judge them. A malformed row
  is left where it is by each of them, and the check now names it. Nothing to
  change.
- **`--migrate`**, which rewrites `path:line` rows and has nothing to say
  about a new-format row that does not parse.
- **Widening `ANCHOR_RE`.** #299's first comment already argues against it: a
  wider range moves the boundary and leaves the silence on the other side.
- **`broad_gate.py`.** Its seal panel is drawn on success only, where
  `MALFORMED` is zero by construction, and `LEDGER_RE` still matches the
  total line's unchanged prefix. Item D of this milestone edits that file.
- **README.md and README.ko.md.** Both were read for a list of verdicts and
  hold none, so nothing there goes stale.
- **`docs/the-evidence-ledger.md`.** Its statements arrive through `settle`'s
  fold at a release, the way #444's did. The rule below is written to be
  folded.
- **A lint guard for #322's class** (for example ruff's `W605`). A new gate,
  in a patch release. Questions.md Q2.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 placeholder hash | Given a fragment row `\| A \| \`src/service.py#handler@0\` \|`, when `evidence_check.py .` runs, then the output names that coordinate under `MALFORMED`, the totals read `1 malformed`, and it exits 2 | a case in `tests/test_a_row_points_by_content.py`, seen red against `ca2afdb9`'s checker |
| S2 short hash | Same with `@abcde` (five hex) | same file, same way |
| S3 no path | Same with `` `#handler@abcdef12` `` in the `Code grounds` cell | same |
| S4 unescaped quote | A quoted locator containing `"`: `MALFORMED`, and the detail says to write `\"`. The same row written with `\"` resolves `OK` | same; the second half pins that the documented repair works |
| S5 a cell with one good and one bad | `` `a.py#f@<good>`, `b.py#g@0` `` reads `1 ok` and `1 malformed` | same |
| S6 prose grounds | A row with a claim and `Code grounds` = `none — policy only` is `MALFORMED` | same |
| S7 not refused | Every shape in *Must not be refused* reads no `MALFORMED`, and a malformed row inside a closed fence is not reported while one inside an unclosed fence is | same; one case per shape, or one case over a ledger holding all of them |
| S8 both readers | `MALFORMED` exits 2 with and without `--strict`, and `exit_code` says so directly | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, whose `zero` dict gains the key |
| S9 printed at zero | A clean ledger's per-ledger and `total:` lines end `· 0 old-format · 0 malformed` | the existing substring cases stay green and one asserts the new tail |
| S10 reverify speaks | `--reverify` over S1's ledger prints a `LEFT` line naming the coordinate, writes nothing, and exits 1 | a case beside `test_an_ordinary_new_row_is_still_anchored_by_reverify` |
| S11 the advisor | A commit in a repository whose ledger holds S1's row prints a `MALFORMED` block from `hooks/evidence-advisor.py` | `tests/test_dispatch.py`, beside `test_a_commit_with_a_pre_anchor_ledger_is_pointed_at_the_migrator`, and the docstring pin in `tests/test_a_row_points_by_content.py` |
| S12 this repository | After the repair, `evidence_check.py --strict .` over this tree reads `0 malformed`, `0 drifted`, `0 broken`, and its `ok` total is higher than at `ca2afdb9` by the anchors the repair made readable | executed at phase 2's close, and the before-and-after totals written in `phases/phase-2.md` |
| S13 the documents | `SKILL.md` has a `MALFORMED` verdict row and names `\"`; `templates/ledger.md` names `\"` | read by the reviewer. No case pins `OLD-FORMAT`'s row in `SKILL.md` today (searched), so none is owed for this one |

## Data & interfaces

- Verdict word: `MALFORMED`. It stays English in every record language,
  because a checker matches it (`skills/implement/SKILL.md` §*The language
  the records are written in*).
- Totals line, whole: `total: N ok · D drifted · B broken · E external · O old-format · M malformed`.
- `exit_code(totals, refused, drifted, strict)`: returns 2 when
  `totals["MALFORMED"]` is non-zero, whatever `strict` is.
- **`ANCHOR_RE` and `resolve_unit` do not change** — neither name, nor
  `ANCHOR_RE`'s pattern, nor `resolve_unit`'s signature and return shape.
  Work item B of this milestone (#603, `survivor_check.py`) loads
  `evidence_check.py` by path and calls both (constraint from the
  orchestrator, 2026-09-25). Nothing in this frame needs either to change: the
  arm reads what `ANCHOR_RE` refuses without altering what it accepts. If the
  build finds it must, it adds a new unit beside the old one and leaves the
  old one in place, and says so in `plan.md` *Operational impact*.
- The column name `Code grounds` becomes vocabulary the checker reads.
- `evidence_check.py` stays loadable alone. `evidence-ci` vendors it into a
  user repository's `tools/` with no sibling beside it, which is why its
  fence rule has a vendored copy (the comment above `VENDORED_FENCE_RE`). A
  cell splitter it needs lives in the file, or loads from the shared reader
  with the same kind of fallback.
- A table cell splits on an unescaped `|` (`\|` is an escaped pipe; the
  ledger rule in `docs/the-evidence-ledger.md` says a pipe in a cell is
  escaped).

## Open questions → questions.md

Two person rows (Q1 the exit grading for other repositories, Q2 a lint guard
for #322's class), each with the default the build proceeds on, and the work's
rows for the five live claims.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-09-25 by framer, before the build.
