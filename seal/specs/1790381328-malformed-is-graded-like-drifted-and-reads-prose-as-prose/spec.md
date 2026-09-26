# Feature Specification: MALFORMED is graded like DRIFTED, and rule (a) reads prose as prose

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Work item B of `release: 0.15.5` (milestone 47): #614, and the owner's answer
to #606's Q1. A patch release: fixes to instruments, no new gate. Every
refusal this work narrows or adds enforces a rule a document already states
(the milestone's own test). The one it adds, a dotless file name glued to a
locator, is what `malformed_rows`' docstring already says: "a `#` glued to a
path or a file name".

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `routing.md` §*Why this way*, and the orchestrator's spawn prompt: **#606's Q1 = (b), answered 2026-09-26 by the repository owner in the batch before the first edit** | `MALFORMED` is graded like `DRIFTED`: exit 1 on a lenient run, exit 2 under `--strict`. The owner was told the three side effects (below) before answering, so none of them is reopened here |
| `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/questions.md` Q1 — "(b) grade like `DRIFTED`: exit 1 with the lenient notice, 2 under `--strict` … The change from (a) to (b) is one branch in `exit_code` and its case" | The shape of the grading change: one branch of `evidence_check.py#exit_code`, which its own comment names as the one the owner may move. The row's Status is ticked by this branch with the owner's answer, because the owner answered and the row still reads ⬜ default (a) |
| `evidence_check.py#LENIENT_NOTICE` and its comment — "Printed on exit 1 and nowhere else. Exit 0 and exit 2 are states every reader grades alike" | Exit 1 now has a second cause. The notice still prints on exit 1 alone, and its sentence must be true for both causes (see *The notice* below) |
| `skills/evidence-check/SKILL.md` §*Which reader graded your tree* — "Three of them read its exit code and grade drift differently … the disagreement is the design", and the `DRIFTED` row: "This is the one verdict the readers grade differently" | After (b) there are two such verdicts. The reader table and the `DRIFTED` row are false as written and are corrected; the table gains `MALFORMED`'s grading beside drift's |
| `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py#test_no_document_describes_the_lenient_reader_alone` (#354) | A document that says what a lenient run exits names the strict reader in the same block. Every sentence this work writes about `MALFORMED`'s exit 1 sits beside `--strict` and `broad-gate` |
| `evidence_check.py#malformed_rows`' docstring — "a `#` glued to a path or a file name … An issue number `#299` or `org/repo#299`, a directive `#ifdef`, a decorator `@cache` and an address are prose, in a span or out of one" | The rule #614's four observations measure the code against. `Makefile#"all"` is a `#` glued to a file name and is missed; `org/repo#299's`, `chart.js@4` and `` `@lru_cache  # memoized` `` are prose and are refused |
| `evidence_check.py#ANCHOR_RE` (a hash of 6–12 lowercase hex) and `malformed_remedy` (the placeholder `@00000000`) | Nothing shorter than six hex characters is a hash anybody was told to write, which is the grounds for `PATH_HASH_RE`'s lower bound (#614 item 3) |
| `skills/agent-contract/SKILL.md` §12 — "A defect belongs to a class — enumerate the class" | Round 3's report names two shapes for the both-marks rule (`` `@lru_cache  # memoized` `` and `` `x = 1  # see @jane` ``). Both are fixed, not the one #614's text quotes |
| `skills/agent-contract/SKILL.md` §14 and §15 | Every changed message, verdict grading and rendered line is pinned in the commit that changes it, and every new case is shown red before it is committed |
| `CLAUDE.md` §*a change writes fragments, never the shared file* — "an edit drifts the row, which is re-read against that edit and re-stamped there with a dated note, its claim first corrected in place with a `Corrected <date>` note where the edit made it false" | Two release-file rows state the old grading or the old notice and are corrected in place; the rest of the rows this work drifts are re-read in place; new claims go in `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md` |
| `CLAUDE.md` §*a change writes fragments* — "an entry under `CHANGELOG.md`'s `## Unreleased`" becomes `seal/specs/<work-item-id>/changelog.md` | The release note for both halves goes in this directory's `changelog.md`. Released sections of `CHANGELOG.md` that describe 0.15.4's grading are history and are not edited |

`docs/` is silent on `MALFORMED` and on `OLD-FORMAT`'s grading
(`git grep -n -i "malformed\|old-format" -- docs` finds nothing about the
ledger checker, read 2026-09-26). No policy is contradicted, and this work
writes none.

## Scope

### In — part 1: `MALFORMED` is graded like `DRIFTED`

1. **`evidence_check.py#exit_code`**: the `MALFORMED` branch returns
   `2 if strict else 1`, and moves below the `BROKEN`/`refused` branch so a
   run holding a `BROKEN` row and a `MALFORMED` row still exits 2 leniently.
   Its comment says who decided it and when, and names the grading it departs
   from (`OLD-FORMAT`) and why the departure is accepted.
2. **The notice.** `LENIENT_NOTICE` becomes, verbatim and on one line:

   > exit 1 is the lenient reading. \`broad-gate\` runs this same check with \`--strict\`, where DRIFTED and MALFORMED are exit 2, and this tree would come back NOT SEALED.

   The verdict words are the ones the run prints on the rows above the
   notice, which is how a reader tells the two meanings of exit 1 apart. The
   notice still names one flag and still says `exit 2`, `broad-gate` and
   `NOT SEALED`, so the four structural cases in
   `test_the_lenient_run_says_what_the_broad_gate_will_say.py` keep holding.
3. **Every other statement of the grading in the checker**: the module
   docstring's `Exit codes:` line; `malformed_rows`' "It fails the run with or
   without `--strict`, like OLD-FORMAT"; `--strict`'s argparse help ("drift
   also fails").
4. **`skills/evidence-check/SKILL.md`**:
   - the `--strict` option row ("drift exits 2 … instead of 1");
   - §*Which reader graded your tree*: the lead sentence, and the table
     gains a `MALFORMED is` column. The advisor's cell in it is *printed as a
     block on the commit, never an exit code*, because
     `hooks/evidence-advisor.py#failing_rows` keeps `MALFORMED` and prints it
     while it drops drift;
   - the verdict table: `MALFORMED (exit 1; 2 under --strict, which is what
     broad-gate passes)`, its action cell saying that exit 1 here means *fix
     the coordinate*, not *re-read*, and that the verdict word says which;
     the `DRIFTED` row's "the one verdict the readers grade differently"
     becomes "one of the two".
5. **`skills/evidence-ci/SKILL.md`** step 4, *`--strict` or not*: a
   malformed coordinate follows the flag the way drift does, so the
   `|| [ $? -eq 1 ]` recipe lets it through with the rest of exit 1.
6. **`templates/evidence-check.yml`**, the comment inside the step: "--strict
   turns DRIFTED … into the same exit code as a BROKEN coordinate" names
   `MALFORMED` too, and "Dropping --strict softens drift and nothing else"
   becomes "softens drift and MALFORMED, and nothing else". The `# RIDER:`
   block at the top of the file and the line its stamp quotes are not
   touched.
7. **`.github/workflows/test.yml`**, the `ledger` job: its comment (drift is
   reported and does not fail; `--strict` where drift is exit 2) and the
   `::warning::` text, which today reads *evidence ledger reports drift —
   re-verify the rows above* and would be false on a malformed-only run. It
   becomes: `::warning::evidence ledger reports drift or a malformed
   coordinate — each row above names its verdict and what to do`.
8. **The tests that pin `MALFORMED` at exit 2 without `--strict`**,
   enumerated by construction (every test function in `tests/` whose body
   names `MALFORMED` or `malformed` and asserts an exit code, then read one by
   one — command in *Data & interfaces*):
   - `tests/test_a_row_points_by_content.py`:
     `test_a_coordinate_that_will_not_parse_is_malformed_under_both_readings`
     (asserts 2 for both readings: split to 1 lenient, 2 strict),
     `test_a_bare_quote_in_a_quoted_locator_is_malformed_and_the_escape_repairs_it`,
     `test_a_claim_whose_grounds_cite_nothing_is_malformed`, and the second
     half of `test_what_is_not_a_claim_is_not_refused` (each asserts 2
     leniently: becomes 1);
   - `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`:
     `test_a_malformed_row_is_silent`, renamed (see *Data & interfaces*). · NAME NOT IN TREE
     It inverts: lenient exit 1 carrying the notice as its last line,
     `--strict` exit 2 without it. Then the two `MALFORMED` lines of
     `test_the_grading_is_one_function_and_the_line_reads_its_answer`, and
     the `NOTICE` literal. The module docstring stays: every sentence in it
     is about drift and still holds.

   Test **names** stay where they remain true, so the ledger anchors that cite
   them drift rather than break. `..._under_both_readings` is still true (the
   row is named under both readings); only its exit assertion changes.
9. **Two new pins** (§14), each in the commit that changes the text:
   - the `MALFORMED` row of `SKILL.md`'s verdict table states the grading
     `exit_code` returns, and so does the reader table's `MALFORMED` column;
   - the `ledger` job's `::warning::` line in `.github/workflows/test.yml`
     names both causes of exit 1.

### In — part 2: rule (a) reads prose as prose (#614)

All in `evidence_check.py`, around `refused_coordinate`:

10. **Item 3, a version is not a hash.** `PATH_HASH_RE` takes six or more hex
    characters: `r"[0-9a-f]{6,}(?![\w.])"`. `chart.js@4`, `` `vue.js@3` ``
    and `jane.doe@beef` are prose. No upper bound, so a 40-character SHA
    pasted after a path is still named.
11. **Item 2, an issue number keeps its sentence.** A `#` followed by digits
    that no ASCII word character continues is an issue number, whatever the
    sentence glues after it: `ISSUE_TAIL_RE = re.compile(r"\d+(?![A-Za-z0-9_])")`
    replaces `tail.isdigit()`. `org/repo#299's`, `org/repo#299—see`,
    `“org/repo#299”`, `org/repo#299에서` and
    `[org/repo#299](https://example.com/org/repo/issues/299)` are prose.
12. **Item 1, a dotless file name takes any locator opener.** After a head
    ending in a letter or digit, a tail opening with a letter, `_`, `"` or
    `<` is a coordinate: `Makefile#"all: build"`, `Makefile#<module>` and
    `Makefile#_private` are named, as `Makefile#build` already is.
13. **Item 4, both marks count only where they are glued.** Today
    `"#" in s and "@" in s` refuses any code span holding both, so
    `` `@lru_cache  # memoized` `` and `` `x = 1  # see @jane` `` exit 2 (and
    exit 1 after part 1). Both marks count only where an `@` follows a `#`
    with no whitespace between them outside a quoted string, which holds
    whitespace only in a code span (outside one the cell is read word by
    word): `GLUED_MARKS_RE = re.compile(r'#(?:"(?:[^"\\\n]|\\.)*"|[^\s"#])*@')`,
    tested with `.search` so every `#` in the text is tried. The `#` in the
    unquoted class was added by round 1 of this work item, so each attempt
    stops at the next `#` and the search stays linear. Every
    malformed shape the suite names today keeps its name (see *Must still be
    named*).

    **In scope, not deferred.** Grounds: it is the same class as items 2
    and 3, prose refused (§12), in the same unit; it contradicts the stated
    rule that "a decorator `@cache` … is prose, in a span or out of one"; and
    the direction it errs in is the one the milestone ranks first, a
    consumer's build refusing prose. It reaches consumers at exit 2 still,
    because `templates/evidence-check.yml` passes `--strict`. Deferring it
    would ship a release note saying rule (a) reads prose as prose while one
    shape round 3 measured still does not.
14. **`malformed_rows`' and `refused_coordinate`'s docstrings** state the rule
    as built: the six-character hash, the issue-number tail, the dotless
    file name's openers, the glued marks, and each trade below.
15. **The cases.** #614's eleven parameters, as pasted (two functions after
    `test_a_directive_or_a_string_holding_a_hash_is_prose`), plus one
    function for item 4: `` `@lru_cache  # memoized` `` and
    `` `x = 1  # see @jane` `` beside a good anchor read `0 malformed` at
    exit 0.

### What each part gives up, stated so no reviewer finds it as a defect

Part 1, accepted by the owner before answering:

- A genuinely broken coordinate passes lenient CI with a warning. Only the
  broad gate, and any consumer running the vendored template, refuses it.
- Exit 1 carries two meanings, *re-read* and *fix the coordinate*. The verdict
  word in stdout and the notice's two words tell them apart.
- `MALFORMED`'s grading departs from `OLD-FORMAT`'s, the precedent 0.15.4
  followed. `OLD-FORMAT` stays exit 2 under both readings.

Part 2, measured by round 3 of work item 1790297087 or read here:

- `src/a.py@abc`, a path followed by fewer than six hex characters and no
  anchor, goes silent. `src/a.py#f@abc` is still named by the glued marks.
- A locator that opens with digits and goes on with anything but an ASCII
  letter, digit or `_`, with no hash, reads as an issue number:
  `docs/a.md#1장`, and (added by round 1 of this work item, which measured
  them) `docs/a.md#1-scope`, `docs/a.md#1.2` and `src/a.py#1>"x"`. With a
  hash (`docs/a.md#1장@abcdef12`) the glued marks name it.
- `Makefile#1x` stays silent, as it is today (read: at 47e32d57 its tail opens
  with a digit, which the dotless branch has never taken). The dotless
  branch's `"` and `<` openers name `C#"hello"` and `vector#<T>` (round 1).
- A path-less coordinate with unquoted whitespace, or a `"` no second `"`
  closes, between `#` and `@` (`#handler @abcdef12`, and from round 1
  `#handler>"a"b"@abcdef12`) goes silent. With a path, the per-word rule
  still names it (`src/a.py#handler` is a `#` glued to a path).
- `org/repo@abcdef12` and a schemeless `example.com/page#section` stay
  refused. Round 3 judged both genuinely ambiguous with a coordinate, and
  nothing here changes that.

### Must still be named

Each is a case in `tests/test_a_row_points_by_content.py` today, or is added:
every `MALFORMED_SHAPES` value; the bare-quote shape
`src/names.py#"LABEL = "ok""@<h>`; `src/service.py#Box@0` beside a good
anchor; the unticked one-mark coordinates of
`test_an_unticked_coordinate_with_one_mark_is_named`; every coordinate of
`test_a_coordinate_the_opener_list_misses_is_named`; and a quoted locator
holding a comment, `` `src/a.py#"x = 1  # c"@0` ``, which the glued marks
name through the quoted string.

### Out

- **`OLD-FORMAT`'s grading.** The owner answered for `MALFORMED` alone and
  was told the two would part.
- **`README.md`, `README.ko.md`, `CONTRIBUTING.md`, `docs/the-evidence-ledger.md`.**
  Each states drift's grading and none states `MALFORMED`'s; every sentence
  in them stays true after (b) (read 2026-09-26: `README.md` §*The ledger is
  checked*, `CONTRIBUTING.md` §*The two checks …* and §*Running the checks*,
  `docs/the-evidence-ledger.md` §*What the checker refuses*). Widening them to
  name a second verdict is a documentation change no reader is misled
  without.
- **`hooks/evidence-advisor.py`.** It imports the checker and reads no exit
  code, so the grading does not reach it, and it keeps printing `MALFORMED`
  on the commit. Its docstring says nothing about an exit code.
- **`skills/verify/scripts/broad_gate.py` and `seal_stamp.py`.** The gate
  passes `--strict`, so it reads `MALFORMED` as exit 2 before and after.
- **`CHANGELOG.md`'s released sections and the records of work item
  1790297087** other than its `questions.md` Q1 Status cell. They describe
  0.15.4 as it shipped.
- **The claim row with an empty `Code grounds` cell** (round 3's ❓, carried
  from rounds 1 and 2, answerer the repository owner). Not touched by #614,
  not in the milestone, and not asked in this run's batch; it stays where
  round 3 left it.
- **#585**, whether the cell-count refusal ships to every repository: 0.16.0,
  left out by the milestone.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 lenient malformed | Given a ledger whose only finding is a `MALFORMED` row, when `evidence_check.py .` runs, then it exits 1, names the row with its remedy, and prints the new notice as its last line | `test_a_malformed_row_is_told_what_the_gate_would_say` (renamed from `test_a_malformed_row_is_silent`), shown red against 47e32d57's `exit_code` · NAME NOT IN TREE |
| S2 strict malformed | The same ledger under `--strict` exits 2 and prints no notice | the same case's strict half |
| S3 grading table | `exit_code` returns 1 for `MALFORMED` alone leniently, 2 under `--strict`, 2 when a `BROKEN` row or a refused record sits beside it, and 2 for `OLD-FORMAT` under both readings | `test_the_grading_is_one_function_and_the_line_reads_its_answer`, with a new assertion for `MALFORMED` beside `BROKEN` |
| S4 notice | `LENIENT_NOTICE` equals the literal in *Scope* item 2, is one line, names `--strict` alone, and says `exit 2`, `broad-gate`, `NOT SEALED`, `DRIFTED` and `MALFORMED` | `test_the_checker_states_the_sentence_once`, `test_the_sentence_is_one_line`, `test_the_notice_borrows_the_word_the_failing_gate_prints` (gains the two verdict words) |
| S5 existing shapes | Every `MALFORMED` shape the suite names today is still named under both readings, at exit 1 leniently and exit 2 under `--strict` | the four `test_a_row_points_by_content.py` cases in *Scope* item 8 |
| S6 documents | `SKILL.md`'s `MALFORMED` verdict row and reader-table column state `exit_code`'s grading; the `DRIFTED` row no longer claims to be the only verdict graded differently | the new pin in *Scope* item 9, shown red with the old row restored |
| S7 CI warning | The `ledger` job's `::warning::` line names drift and a malformed coordinate | the new pin in *Scope* item 9, shown red against 47e32d57's `test.yml` |
| S8 dotless file name | `Makefile#"all: build"`, `Makefile#<module>` and `Makefile#_private` beside a good anchor are each named `MALFORMED` | #614's `test_a_file_name_with_no_dot_takes_any_locator`, red at 47e32d57 |
| S9 issue number glued | the five issue-number shapes of *Scope* item 11 beside a good anchor read `0 old-format · 0 malformed` at exit 0 | #614's `test_an_issue_number_or_a_version_glued_to_a_word_is_prose`, red at 47e32d57 |
| S10 version | `chart.js@4`, `` `vue.js@3` ``, `jane.doe@beef` beside a good anchor read `0 malformed` at exit 0 | the same function's last three parameters, red at 47e32d57 |
| S11 decorated line | `` `@lru_cache  # memoized` `` and `` `x = 1  # see @jane` `` beside a good anchor read `0 malformed` at exit 0 | a new case after #614's two, red at 47e32d57 |
| S12 still named | every shape in *Must still be named* is named | the existing cases plus the quoted-comment parameter, which must pass both before and after the glued-marks change (a guard, stated as one in its docstring) |
| S13 this tree | `evidence_check.py --strict .` over this repository reads `0 drifted · 0 broken · … · 0 malformed`, exit 0, after the ledger rows are re-read | executed at the phase that closes the records |

## Data & interfaces

**Exit codes after this work** (the module docstring's line, verbatim):

```
Exit codes: 0 clean · 1 drift or malformed only · 2 broken or old-format
coordinates (or drift or malformed with --strict).
```

**The enumeration command for *Scope* item 8**, read-only and re-runnable by
the builder after its edits to confirm nothing was missed:

```python
# for every tests/*.py: every FunctionDef whose source names MALFORMED or
# " malformed" and matches returncode|== 2|exit 2 — then read each one
```

Run 2026-09-26 by the framer over the tree at 47e32d57; it listed twelve
functions, of which the six in item 8 pin an exit code for `MALFORMED` and
the other six pin exit 0 for prose, exit 1 for `--reverify`, or nothing about
the ledger checker.

**Renamed test**: the case `test_a_malformed_row_is_silent` is renamed. · NAME NOT IN TREE
Its new name is `test_a_malformed_row_is_told_what_the_gate_would_say`,
because after the change it is the opposite of silent. No ledger row cites
it (`grep` over `seal/ledger.md` and `seal/releases/*.md`, 2026-09-26).

**Ledger rows this work makes false or drifts** (read 2026-09-26; the
builder's `evidence-check .` after the edits is the authority, and names any
row missed here):

| Row | What happens | Repair |
|---|---|---|
| `seal/releases/0.15.4.md`, *A `Code grounds` cell holding a coordinate neither …* | its claim says "exit 2 with or without `--strict`", false after part 1; it cites `malformed_rows`, `refused_coordinate`, `PATH_HASH_RE`, `exit_code` and four cases this work edits | claim corrected in place with a `Corrected <date>` note, then re-read and re-stamped with a dated note |
| `seal/releases/0.11.3.md`, *A run whose answer is exit 1 says that `broad-gate` …* | its claim quotes the notice ("where drift is exit 2"), false after part 1 | the same |
| `seal/releases/0.11.3.md`, *The condition for that line is the run's own answer …* (`exit_code`) and *No document that tells a reader what drift exits …* (`SKILL.md` §*Which reader graded your tree*) | drift only; both claims hold | re-read and re-stamped with a dated note |
| `seal/releases/0.15.4.md`, the bare-quote row and *Only the `Code grounds` cell is read …* | each cites a case whose exit assertion changes; both claims hold | the same |

New claims (the new grading, the notice, each rule (a) edge, the glued
marks, the two pins) go in
`seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`.

## Open questions → questions.md

No row needs a person: the owner's one decision was taken in the batch, and
every other judgment the ticket left open was answered from the tree
(`questions.md` lists them). The file holds one measurement row and two rows
for the work, each with the default the build proceeds on.

Framed 2026-09-26 by framer, before the build.
