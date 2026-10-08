# Round 1 report — 1791384159 a unit the extractor cannot bound is refused (#870, #848)

Target SHA: 8ca2b57ad154dc15fc9e67177fbd247b6ee306a2, diffed against fb86a834
(the merge of `origin/release/v0.21.0`). Reviewed in a `git clone --no-local`
at that SHA under the session scratchpad; nothing was written in the worktree
except this file. No earlier rounds exist, so nothing was carried.

## What the account claimed, and what the code does

- **One table, four dispatches.** Claimed: `bounding_rule` is the one place a
  suffix decides the rule. Read: `evidence_check.py:709`, and the four former
  dispatches now read it. The suffix tests left in the file (`:2824`, `:5496`,
  `:5603`, `:5960`) sit outside unit resolution. Holds.
- **Four callers read the refusal.** Claimed. Read: `judge` at
  `evidence_check.py:2329`, `read_citation` at `:2914`, `region_lines` at
  `.github/scripts/rider_check.py:499`, and the survivor sweep reads the
  empty places at `skills/code-review/scripts/survivor_check.py:1268`. Holds.
- **The lexer per family.** Claimed: raw strings, holes, chars against
  lifetimes and nested comments are read per family. Executed: every form the
  spawn named resolves the same span as a hand count (Rust `r#"…"#`, byte
  chars and lifetimes; C++ `R"x(…)x"` single- and multi-line; Go backticks;
  Swift `#"…"#` and `"""` with a `\(…)` hole holding `"}"`; Kotlin `"""` with a
  `${…}` hole; JS templates with a nested template in a hole; C# `$@"…"` with
  `""` and `{{`; C digit separators; nested comments in Rust, Swift and
  Kotlin). Holds for every form it names. Finding 1 is about what the walk
  does with the lexer's answer, not about any form.
- **An unbalanced or unlexable unit reads `BROKEN`.** Claimed. Executed: true
  where the misread leaves a bracket open or a single-line string unclosed.
  It is not true where the misread opens a multi-line form that a later line
  closes, which is finding 1.
- **Q2, 0 new `BROKEN` and 0 new `DRIFTED` here.** Not re-run by me. The CI
  `ledger` job at this SHA reads `pass`. Who answers the repository-wide
  reading: the sealer, through `broad-gate`.
- **The eight `agents/warden.md#"## Report"` rows.** Not re-run; carried as
  the account states them, and outside this diff.
- **#888 holds the opener shapes.** Opened: #888 is open and titled for the Go
  receiver, the generic function and the typed constant. Holds.

## Findings from execution

### 🟡 1 · The walk ignores the lexer's own string and comment state, so #848 comes back through a misread

`brace_span` (`skills/evidence-check/scripts/evidence_check.py:1137`) decides
where a unit starts and ends from brackets alone. `brace_lexed` (`:1016`)
already knows whether each line starts inside a string or a comment, and the
walk never asks. Two instances follow from that one cause.

**A declaration the lexer reads inside a comment is bounded by indentation.**
A JS regex holding `/*` (`/^\/*/`, a common "leading slashes" pattern) opens
a block comment for the lexer, which runs to the next `*/`, usually the next
JSDoc. Every line in between is blanked, so a declaration there has no
brackets, the stack is empty on its first line, and the deeper-line clause
alone ends it. That is the indentation rule this work removed. Executed:
#848's own function placed after `const SLASHES = /^\/*/;` and before a
`/** next */` resolves to lines 3–4 of 3–7 under both the base checker and
this branch's, so a body edit reads `ok`. A regex holding a backtick does the
same through a phantom template literal (3–4 again). The Known-limits bullet
says a misread either refuses or "re-balances by accident"; this one does
neither and is silent.

**A multi-line string the unit opens ends the unit on its first line.** A
constant whose value is a multi-line string with its content at column 0 is
common in Go (SQL in a raw string), in JS templates and in Java text blocks.
The stack is empty after the declaration line and the next line is not
deeper, so the walk stops while the lexer still has the string open.
Executed: Go `const query = `…`` resolves 1–1 of 1–4, the JS template 1–1 of
1–3, the Java text block 2–2 of 2–4. The value is the unit's content and sits
outside the hash. This is not a regression (the base checker answers the
same), but it is the defect class this work exists to close, and `SKILL.md`
now promises "a constant whose value continues" is bounded.

The fix reads the state the lexer already computes. Applied to the clone and
executed: the phantom-comment and phantom-template cases are refused with a
line naming why, the three string constants bound to 1–4, 1–3 and 2–4, and
`tests/test_a_unit_the_extractor_cannot_bound_is_refused.py` with
`tests/test_a_row_points_by_content.py` stay green (262 passed). One side
effect, also executed: a JSDoc line ` * render(x) …` that the opener takes as a
candidate used to make the reading ambiguous, and now refuses it with the
comment named. Both are `BROKEN`.

### 🟡 2 · A comment between a YAML key's compact items ends the key

`block_span` (`evidence_check.py:1194`) takes the `- ` items at the key's own
indent, and stops at the first other line no deeper than the key. A comment
line is such a line. Executed: `on:` / `- push` / `# both` / `- pull_request`
resolves `on` to 1–2, so `pull_request` is outside the hash. Commented-out
steps at a key's indent are common in workflow files. The same stop already
cut a key's deeper value at a column-0 comment under the old rule, and the
fix covers both. Executed in the clone: 1–4, and
`test_this_repositorys_bare_yaml_rows_keep_their_spans` stays green. Only a
comment no deeper than the key is skipped, so a deeper trailing comment keeps
its place in the span and no existing row's hash moves.

### 🟡 3 · The installer paragraph promises that every other row keeps its verdict, and four kinds do not

`changelog.md:36` ends "every other row keeps its hash and its verdict", and
`tests/test_a_unit_the_extractor_cannot_bound_is_refused.py` pins that
sentence. `docs/the-evidence-ledger.md:288` says "the only `DRIFTED` an
installer meets on upgrade is a body the old span left out". Executed, each
against the base checker and this branch's:

- **Rows that were right now read `BROKEN`.** A TSX component returning
  `<p>Don't panic</p>`, a function calling `s.replace(/'/g, …)`, one calling
  `s.split(/\{/)`, and Swift `s.contains(/"/)` each resolved to 1–2 before and
  are refused now. JSX text with an apostrophe is in most React components.
- **A bounded declaration is refused because of a call.** `function render`
  bounded at 1–2, plus a later `render(<p>Don't</p>)` line, is refused as a
  whole. The call is a candidate the walk cannot bound, and one such
  candidate refuses the reading. Before, it was set aside as a one-line call.
  This answers the spawn's question: yes, "any candidate unbounded refuses
  all" refuses a unit with one bounded definition.
- **`.pyi` moved from the text rule to `ast`, and no sentence says so.** A
  decorated stub resolved to 4–4 and now to 3–4, so it reads `DRIFTED`.
- **A YAML key with a compact sequence reads `DRIFTED`.** `on` went from 1–1
  to 1–3 and `steps` from 3–3 to 3–5. The `### Changed` bullet says the items
  now belong to the key, and the installer paragraph then says every other
  row keeps its hash.

Each of these is loud or a single re-read. The defect is the release note: an
installer who meets them has been told they will not.

## Findings from reading

### ⬜ 4 · The refusal says "declared on line N" about a line that is a call

`evidence_check.py:1348` writes every refused candidate as "declared on line
N". For the call in finding 3 the line reads "declared on line 5", and line 5
is `render(<p>Don't</p>)`. "a candidate on line N" says what is known. The
sentence is pinned in six cases, so changing it moves them together.

### ⬜ 5 · `--migrate` leaves a refused suffix's row with a reason that names no remedy

At `evidence_check.py:3476`, an old `path:line` row in a `.rb` file is left
with "no single unit contains s-e", because `file_units` lists nothing for a
suffix no rule bounds. Before this branch it migrated to a bare symbol. The
line would better name the quoted-line anchor, as every other refusal does.

### ⬜ 6 · The day-one list leaves out TypeScript's own module suffixes and matches case

`BRACE_FAMILY` (`evidence_check.py:686`) has `.mjs` and `.cjs` and not `.mts`
and `.cts`. The changelog says "TypeScript", so an installer with `.mts`
files reads it as covered. `.cxx`, `.hh`, `.hxx` and the upper-case `.C` and
`.H` C++ suffixes are refused too, because `bounding_rule` compares the
suffix as written. All are refused loudly, and `spec.md` fixed the list "and
no more", so this is the owner's call and not a defect.

## Checked and found holding

- **C preprocessor branches.** Both branches are read, and a branch pair that
  closes one brace each re-balances: executed, a function with
  `#ifdef`/`#else` branches resolves 1–7 of 1–11, with `return 0;` outside.
  The base checker answered 1–2, so this improves on it, and `SKILL.md`
  §*Known limits* names the class. No finding.
- **The `Corrected ·` row for 0.4.0.** Read against `seal/releases/0.4.0.md:17`:
  the released claim named the fall-through for a file that will not parse,
  which this branch removed. The corrected claim lists the five rules and the
  refusal. The case it cites exists at `tests/test_a_row_points_by_content.py:2258`.
  Holds. No other released row claims the indentation rule (grep over
  `seal/releases/`, `docs/`, `skills/`), and the one released row citing
  `generic_units` is re-read in the fragment.
- **A `/}/` regex inside a body** closes the body's `{` early, and the
  deeper-line clause carries the walk to the right end (1–3, as before).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The walk ends or starts a unit from brackets alone and ignores the lexer's string and comment state: a declaration inside a phantom comment (a regex holding `/*` or a backtick) is bounded by indentation, which reproduces #848, and a multi-line string with column-0 content ends its constant on the first line | `skills/evidence-check/scripts/evidence_check.py:1137` | open | executed: #848's function after `/^\/*/` resolves 3–4 of 3–7; Go, JS and Java string constants resolve to their first line; the fix in the clone refuses the first and bounds the second, 262 passed |
| 🟡 2 | A comment at a YAML key's indent ends the key, so compact items after it are outside the hash | `skills/evidence-check/scripts/evidence_check.py:1194` | open | executed: `on` with a comment between items resolves 1–2 of 1–4; the fix gives 1–4 and keeps this repository's bare YAML spans |
| 🟡 3 | The installer paragraph and the policy sentence promise every other row keeps its verdict, while unlexed forms (JSX apostrophe, regex quote or bracket), a call-shaped candidate, `.pyi` decorators and YAML compact items change it | `seal/specs/1791384159-a-unit-the-extractor-cannot-bound-is-refused/changelog.md:36` | open | executed old against new for each instance; the false sentence is pinned in the changelog case |
| ⬜ 4 | A refused call-shaped candidate is described as "declared on line N" | `skills/evidence-check/scripts/evidence_check.py:1348` | open | read; the refusal of a bounded `render` names the call's line as a declaration |
| ⬜ 5 | `--migrate` leaves a row in a suffix no rule bounds with "no single unit contains", naming no remedy | `skills/evidence-check/scripts/evidence_check.py:3476` | open | read |
| ⬜ 6 | `.mts`, `.cts`, `.cxx`, `.hh`, `.hxx` and upper-case suffixes are refused although the changelog names their languages | `skills/evidence-check/scripts/evidence_check.py:686` | open | read; `spec.md` fixed the list, so the owner answers |
| ❓ | Old and new checker `--strict` over this tree byte-identical (Q2) | `seal/specs/1791384159-a-unit-the-extractor-cannot-bound-is-refused/questions.md` | ❓ out of verified scope | not re-run in this round; the CI `ledger` job reads `pass`; the sealer answers it through `broad-gate` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the spawn named plus `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py`, in the clone at the target SHA | exit 0, 481 passed |
| Two probe modules loading the base checker (fb86a834) and this branch's, resolving 42 shapes across the nine families, YAML and `.pyi`; each run once and deleted | phantom comment and phantom template 3–4 under both; Go, JS and Java column-0 strings 1–1, 1–1, 2–2; YAML with a comment 1–2; JSX apostrophe, regex quote, regex bracket, Swift regex quote refused where the base gave 1–2; bounded `render` refused through its call; `.pyi` 4–4 to 3–4; every raw, hole, char and nested-comment form bounded as counted by hand |
| The fixes for 🟡 1 and 🟡 2 applied to the clone, the probe re-run, then `bin/test` over `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py` and `tests/test_a_row_points_by_content.py` | exit 0, 262 passed; phantom cases refused with the new line; strings 1–4, 1–3, 2–4; YAML 1–4. The clone was restored afterwards |
| `gh pr checks 889` | exit 8 (pending): lint, ledger, release, both arm-check-grammar, ubuntu and macOS groups 1–2 pass; macOS group 3 and Windows groups 1–4 pending |
| `gh issue view 888` | open, titled for the receiver, generic and typed-constant shapes |
| The full suite, repository-wide lint and typecheck | not yet, and not this round's; the sealer runs them once after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Declaration shapes the opener never matched (Go receivers, generics, typed constants) | #888, already deferred by `spec.md` §*Out* | the repository owner, who files and schedules #888 |

## Regression tests to plant

- `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py`: the two cases
  in fix 1 and the case in fix 2. Each was seen red against the target SHA by
  the probe (3–4 instead of a refusal; 1–1, 1–1, 2–2; 1–2) before the fix was
  applied in the clone.
- The same module's changelog case gains two phrases (fix 3).

## Facts for the evidence ledger

- U4's claim gains: a declaration line the lexer reads inside a comment or
  string is refused, and a unit does not end while a string or comment its
  lines opened is open (`brace_span`, `brace_lexed`, with fix 1's cases).
- U7's claim gains: a comment no deeper than the key does not end its value
  (`block_span`, with fix 2's case).

## Paste-ready fixes

### 🟡 1

`skills/evidence-check/scripts/evidence_check.py`, in `brace_lexed`:

```python
    for n, line in enumerate(lines):
        if unreadable is not None:
            errors[n] = f"line {unreadable + 1} holds a raw string the walk cannot read"
            out.append(["", False, False])
            continue
        inside = len(stack) > 1  # the line starts inside a string or comment
        brackets, residue = [], []
```

```python
        out.append(["".join(brackets), closers, inside])

    if len(stack) > 1 and unreadable is None:
        opened = stack[1][-1]
        for n in range(opened, len(lines)):
            errors.setdefault(
                n, f"a string or comment opened at line {opened + 1} never ends"
            )
    return tuple((b, c, errors.get(n), s) for n, (b, c, s) in enumerate(out))
```

and its docstring's first sentence names the fourth field: "`(brackets,
closers_only, error, inside)` … and whether the line starts inside a string
or comment form". In `brace_span`:

```python
    stack = []
    if lexed[i][3] and not lexed[i][2]:
        # The walk would read nothing but blanked text from here, which is
        # the indentation rule again (#848): a declaration the lexer reads
        # inside a comment or string is a misread or no declaration at all.
        return None, f"line {i + 1} sits inside a comment or string as the walk reads it"
    j = i
    while j < len(lines):
        brackets, _closers, error, _inside = lexed[j]
        if error:
            return None, error
```

```python
        if not stack and j + 1 < len(lines) and lexed[j + 1][3]:
            # A string or comment this line left open is still open: the
            # unit has not ended, whatever the next line's indentation.
            j += 1
            continue
        if not stack:
            k = j + 1
```

The cases, in `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py`:

```python
@pytest.mark.parametrize(
    "rel, text, name, span",
    [
        ("q.go", "const query = `\nSELECT a\nFROM t\n`\n\nfunc g() {}\n", "query", (1, 4)),
        (
            "q.ts",
            "export const QUERY = `\nSELECT a\nFROM t\n`;\n\nexport const x = 1;\n",
            "QUERY",
            (1, 3),
        ),
        (
            "Q.java",
            'class Q {\n  static String Q1 = """\nSELECT a\nFROM t\n""";\n}\n',
            "Q1",
            (2, 4),
        ),
    ],
)
def test_a_string_the_unit_opened_keeps_the_unit_open(rel, text, name, span):
    """A constant whose value is a multi-line string with its content at
    column 0 ends where the string ends, not on its first line."""
    assert ec.resolve_unit(rel, name, text) == ([span], False)


def test_a_declaration_the_walk_reads_inside_a_comment_is_refused():
    """A regex holding `/*` opens a comment for the lexer; a declaration
    under it would be bounded by indentation alone, which is #848."""
    text = (
        "const SLASHES = /^\\/*/;\n\nexport function multiLine(\n"
        "  opts: { a: number },\n): number {\n  return opts.a + 1;\n}\n\n"
        "/** next */\nexport function g() {}\n"
    )
    unit = ec.resolve_unit("a.ts", "multiLine", text)
    assert unit.places == [], unit
    assert unit.refused == (
        "the bracket walk cannot bound `multiLine` (declared on line 3: line 3 "
        "sits inside a comment or string as the walk reads it); anchor a quoted "
        "line instead"
    )
```

`skills/evidence-check/SKILL.md` §*Known limits*, after "which refuses it
too.":

```markdown
  A form a misread opens across lines — a regex holding `/*` or a backtick —
  refuses every declaration inside it, because a declaration the lexer reads
  inside a comment or string is never bounded by indentation.
```

### 🟡 2

`skills/evidence-check/scripts/evidence_check.py`, the body of `block_span`
after its docstring:

```python
    indent = len(lines[i]) - len(lines[i].lstrip())

    def quiet(line):
        # A blank line, or a comment no deeper than the key: YAML reads
        # neither as structure, so neither ends the key's value.
        rest = line.lstrip()
        return not rest or (rest.startswith("#") and len(line) - len(rest) <= indent)

    j = i + 1
    while j < len(lines):
        nxt = lines[j]
        if not quiet(nxt) and (len(nxt) - len(nxt.lstrip())) <= indent:
            item = nxt.lstrip()
            at_own_indent = len(nxt) - len(item) == indent
            if not (at_own_indent and (item.rstrip() == "-" or item.startswith("- "))):
                break
        j += 1
    while j > i + 1 and quiet(lines[j - 1]):
        j -= 1
    return i + 1, j
```

```python
def test_a_comment_between_compact_items_does_not_end_the_key():
    text = "on:\n- push\n# both\n- pull_request\njobs:\n  a: 1\n"
    assert ec.resolve_unit("w.yml", "on", text) == ([(1, 4)], False)
```

### 🟡 3

`seal/specs/1791384159-a-unit-the-extractor-cannot-bound-is-refused/changelog.md`,
the end of the installer paragraph, from "names;":

```markdown
  names. Three more kinds change, and each line says why: a brace-language
  unit whose lines hold a form the walk does not lex — an apostrophe in JSX
  text, a JS regex holding a quote or an unbalanced bracket — reads `BROKEN`
  with the remedy, and so does a name whose call elsewhere in the file the
  walk cannot bound; a `.pyi` symbol is now read by `ast`, so a decorated
  stub takes its decorators into the span and reads `DRIFTED` once; a YAML
  key with `- ` items at its own indent reads `DRIFTED` once. Re-read each,
  then `--reverify`; every other row keeps its hash and its verdict.
```

`docs/the-evidence-ledger.md`, the paragraph's last sentence:

```markdown
The walk leaves a last line of nothing but closers out of the span, so a row
the old rule bounded right keeps its hash. The `DRIFTED` rows an installer
meets on upgrade are a body the old span left out, a `.pyi` unit `ast` now
bounds with its decorators, and a YAML key's items at its own indent.
```

In `test_the_changelog_fragment_tells_an_installer_what_to_run`, the tuple
gains two entries:

```python
        "an apostrophe in JSX text",
        "a `.pyi` symbol is now read by `ast`",
```

Needs a fix: yes — 🟡 1 (the walk ignores the lexer's string and comment
state, reproducing #848 through a regex), 🟡 2 (a comment ends a YAML key's
compact items), 🟡 3 (the installer paragraph and policy sentence promise
unchanged verdicts that change)
Loses a record or crashes: no

The broad gate has not run. Once these three are fixed and a verifying round
leaves nothing open, the sealer's spawn comes due.

## Proof block

Files opened in this round:

- `skills/evidence-check/scripts/evidence_check.py` (the diff; lines 385–410,
  1008–1214, 1485, 1590–1640, 2270–2420, 3450–3530, 5945–5968)
- `.github/scripts/rider_check.py` (the diff; the loader lines)
- `skills/code-review/scripts/survivor_check.py` (lines 443–473, 990–1068,
  1250–1276)
- `skills/evidence-check/SKILL.md`, `docs/the-evidence-ledger.md` (the diff)
- `seal/ledger/1791384159-a-unit-the-extractor-cannot-bound-is-refused.md`,
  `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md`
  (the diff)
- `seal/releases/0.4.0.md` (lines 15–20)
- `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py` (the test list;
  lines 440–700)
- this work item's `spec.md`, `questions.md`, `overview.md`, `survivors.md`,
  `changelog.md`, `routing.md`
- `bin/test`
