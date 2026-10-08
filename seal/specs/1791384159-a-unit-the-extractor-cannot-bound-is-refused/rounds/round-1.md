# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — review round 1

| Field | Value |
|---|---|
| Target SHA | 8ca2b57ad154dc15fc9e67177fbd247b6ee306a2 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 889 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1 (the walk ignores the lexer's string and comment state, reproducing #848 through a regex), 🟡 2 (a comment ends a YAML key's compact items), 🟡 3 (the installer paragraph and policy sentence promise unchanged verdicts that change) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the build at 8ca2b57a, against fb86a834, the release branch the build merged. The spawn named six things to attack. First, the per-family lexer: raw strings, template literals, JS regex literals, char literals against lifetimes, nested block comments and preprocessor lines. Second, whether a refusal can fire on a row that resolved correctly before. Third, whether 'any candidate unbounded refuses all' can refuse a unit with one bounded definition. Fourth, the YAML block rule. Fifth, the Corrected row for 0.4.0. Sixth, the reviewer's own axes. It also ran the eight guard modules once. Facts arrived labelled. Read from the smith: the one bounding table, the refusals, Resolution, the byte-identical --strict, and the release branch's eight warden.md drifts. Read: #888 holds the opener shapes. The round was stopped once by the orchestrator in error and resumed.

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

## Paste-ready fixes

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
```markdown
  A form a misread opens across lines — a regex holding `/*` or a backtick —
  refuses every declaration inside it, because a declaration the lexer reads
  inside a comment or string is never bounded by indentation.
```
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
```markdown
The walk leaves a last line of nothing but closers out of the span, so a row
the old rule bounded right keeps its hash. The `DRIFTED` rows an installer
meets on upgrade are a body the old span left out, a `.pyi` unit `ast` now
bounds with its decorators, and a YAML key's items at its own indent.
```
```python
        "an apostrophe in JSX text",
        "a `.pyi` symbol is now read by `ast`",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the spawn named plus `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py`, in the clone at the target SHA | exit 0, 481 passed |
| Two probe modules loading the base checker (fb86a834) and this branch's, resolving 42 shapes across the nine families, YAML and `.pyi`; each run once and deleted | phantom comment and phantom template 3–4 under both; Go, JS and Java column-0 strings 1–1, 1–1, 2–2; YAML with a comment 1–2; JSX apostrophe, regex quote, regex bracket, Swift regex quote refused where the base gave 1–2; bounded `render` refused through its call; `.pyi` 4–4 to 3–4; every raw, hole, char and nested-comment form bounded as counted by hand |
| The fixes for 🟡 1 and 🟡 2 applied to the clone, the probe re-run, then `bin/test` over `tests/test_a_unit_the_extractor_cannot_bound_is_refused.py` and `tests/test_a_row_points_by_content.py` | exit 0, 262 passed; phantom cases refused with the new line; strings 1–4, 1–3, 2–4; YAML 1–4. The clone was restored afterwards |
| `gh pr checks 889` | exit 8 (pending): lint, ledger, release, both arm-check-grammar, ubuntu and macOS groups 1–2 pass; macOS group 3 and Windows groups 1–4 pending |
| `gh issue view 888` | open, titled for the receiver, generic and typed-constant shapes |
| The full suite, repository-wide lint and typecheck | not yet, and not this round's; the sealer runs them once after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Declaration shapes the opener never matched (Go receivers, generics, typed constants) | #888, already deferred by `spec.md` §*Out* | the repository owner, who files and schedules #888 |
