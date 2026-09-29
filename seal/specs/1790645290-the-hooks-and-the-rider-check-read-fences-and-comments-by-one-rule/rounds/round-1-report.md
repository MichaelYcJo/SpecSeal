# Round 1 report: 1790645290, the hooks and the rider check read fences and comments by one rule

- **Target:** `fix/658-667-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule` at `9b52cf25`, the work item's own diff `66b34a4e...9b52cf25`. No earlier rounds.
- **Where I worked:** a `git clone --no-local` of that SHA. Every probe ran there or beside it, and all of them are deleted.
- **What I held the code to:** `spec.md` §*The acceptance property*. For every line, `new(L)` must be `base(L)` or `renderer(L)`, and the walk must be exact wherever it claims a line.

## How the findings relate

Two of the three findings needing a fix break the invariant, and each has its own cause. The third is the dependency the invariant's check brought in.

```
the walk trusts a line boundary Python drew      -> 🟡 1  all three readers lose a live row or rider
the walk misses `>` written without a space      -> 🟡 2  exact where it claims, false on those lines
bin/test's failure path promises a partial run   -> 🟡 3  pytest runs no case at all
the oracle reads `--->` differently from spec    -> ⬜ 4  test-only; why a wider fuzz is noisy
```

What held, before the findings:

- **Executed:** the property module passes at `9b52cf25`.
- **Executed:** a wider fuzz of 200,000 generated documents found no document where the routing reader or the rider check leaves both readings. Every config-reader violation it found reduces to 🟡 2 or ⬜ 4.
- **Read:** at the top level, the walk's two constructs, its unclosed rule and its mid-line opener rule match CommonMark §4.5, §4.6 type 2 and §6.6. That covers the no-break-space closer and a closer indented one to three spaces. Every container, indented and other-HTML context falls back to the base reading.

I considered one more thing and it is not a finding. The invariant is per line, so hiding a comment inside the config table joins the rows around it. In C5, `Mode shared` after a mid-table comment is read, while a GFM renderer shows it as paragraph text rather than as a table row. The frame accepts this: C5's *Expected* column, and its scope row that excludes each reader's table grammar.

## Findings

### 🟡 1 A line break CommonMark does not honour lets the walk hide a live declaration, a live `Mode` row and a live rider

**Where:** `hooks/blocks.py:208`, which walks lines that have already been split. It reaches the readers at `hooks/routing.py:168`, `hooks/config.py:327` and `:425`, and `.github/scripts/rider_check.py:340` and `:403`. The same happens through the config reader's other callers: `skills/implement/scripts/seal.py:1481` and `:1591`, and `skills/verify/scripts/broad_gate.py:759` and `:828`.

**What is wrong.** Every reader splits its text with `str.splitlines()`. That method also ends a line at U+2028, U+2029, U+0085, a form feed, a vertical tab and `\x1c` to `\x1e`. CommonMark ends a line at `\n`, `\r` or `\r\n` only. So a `&lt;!--` or a fence run that follows one of those characters starts a line for the walk but not for a renderer. The walk then claims the lines below it with certainty.

**Executed.** I built a `routing.md` whose first line is `A note`, U+2028, `&lt;!--`. A blank line, the two-axis table and a `-->` line follow it.

- `routing.parse` returns `None`. The base reader read the declaration.
- markdown-it-py, given the real text, hides no line of it.
- A form feed or a U+0085 in place of U+2028 gives the same three answers.
- The same shape in `config.md` gives `config_rows` → `[]`, where the base read `Mode shared`.
- For the rider check, I used `A note`, U+2028 and a fence run on one line, a real rider below it, and a closing fence. `comment_blocks` returns `[]`. The same text with the break replaced by a space, which is what a renderer sees, returns the rider. The base rider check had no fence state and read it.

**Why it matters.** This is #667's first direction, in all three readers. The routing and config losses are loud but give the wrong cause. The gate asks for a declaration that is in the file, and `broad-gate` calls a visible row absent. The rider loss is silent: the check passes a rider it never checked. The characters are rare. U+2028 arrives with text pasted from web or JavaScript sources, and a form feed still turns up in old text files. That rarity is why this is 🟡 and not 🔴.

**Why the property did not see it.** `tests/commonmark_oracle.py:101` joins the lines it is given with `\n`. So the oracle is handed the reader's split and agrees with the walk. The corpus is built as lists of lines, so no document in it can hold such a break.

**The class (§12).** Every walk caller that got its lines from `str.splitlines()`. I listed them with `git grep` for the four entry points outside `tests/`, and the list under *Where* is all of them. The paste-ready fix threads the text to each of them.

### 🟡 2 A block quote written without a space after `>` is claimed as exact, and it is not

**Where:** `hooks/blocks.py:89`, `CONTAINER`. The docstring's claim is at `hooks/blocks.py:58`.

**What is wrong.** `CONTAINER` requires a space, a tab or the end of the line after every marker. CommonMark requires that after a list marker only. A lone `>` is already a block-quote marker, because the space after it may be omitted (§5.1). So the walk gives `` >``` `` the prefix `""` and calls it certain and live, while a renderer opens a fence inside the quote and hides the line.

**Executed.**

- **Half 2 fails.** The fuzz used the module's `ALPHABET` plus 37 lines, over 200,000 documents. It found 1,888 half-2 disagreements, which reduce to 116 shapes. 1,599 of the 1,888 reduce to the one-line document `[">```"]`.
- **Half 1 fails for the config reader.** Take `["&lt;!--", "```   ", "b ---> c", ">```"]`. The base hides line 3, because the fence-only reading opens a fence on line 1. The renderer hides line 3 too, yet the reader shows it. Three of the eleven reduced config shapes are this one.

**Read.** No reader's answer changes today. `CONFIG_HEADER` and `CONFIG_ROW` need a pipe in column 0 (`hooks/config.py:72`, `:97`). `table_rows` needs a stripped line that starts with a pipe. `comment_blocks` needs a line whose left-stripped form starts with the opener. So a `>`-led line is never a row or a rider.

It is 🟡 all the same. The module's contract is false on these lines, and so is the acceptance property the work is judged by. The next reader built on the walk inherits that. The corpus missed it because `ALPHABET` holds `"> ```"` and `"> quote"` but never `>` without a space.

**Executed with the fix below:**

- The `[">```"]` class is gone.
- The module's own corpus still shows 0 disagreements.
- `test_the_walk_is_exact_somewhere` still passes.
- The three config shapes no longer leave both readings.

### 🟡 3 When the parser cannot be installed, bin/test says the other cases still run, and pytest runs none

**Where:** the comment at `.github/scripts/run_tests.py:491`, the docstring at `:203`, the sentence at `:228`, and the case at `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:799`.

**Executed.** I built a virtualenv holding pytest and no markdown-it-py, then ran `python -m pytest -q -p no:cacheprovider` over two modules: the property module and `tests/test_unverified_rows_close.py`.

- It exited 2 with `Interrupted: 1 error during collection`.
- No case from `tests/test_unverified_rows_close.py` ran.
- The error is a bare `ModuleNotFoundError`, not the "sentence of their own" the docstring promises.

**Why it matters.** The main comment says "every other case still runs", and the printed sentence names only the oracle's cases. What a contributor gets offline, in a `.venv` adopted from before #667, is no run at all, where before this change they got the whole suite. The case at `:799` pins "the suite still runs" with `subprocess.run` mocked to exit 0. So it asserts a claim that the real pytest contradicts.

**Not executed.** I did not run the `-n auto` form. I expect the same result, because every xdist worker collects the same modules, but that is unverified.

**Read.** CI and the platforms hold. `.github/workflows/test.yml:67` installs the pin on all three legs. `has_markdown_it` looks for the same `.dist-info` name that pip and uv write, under `Lib/site-packages` on Windows. An adopted `.venv` holding another version gets the pin installed over it. That is deliberate and pinned at `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:774`.

### ⬜ 4 The oracle reads an inline comment past its first `-->` when a `-` comes before that closer

**Where:** `tests/commonmark_oracle.py:48`. The cause is markdown-it-py 4.2.0's comment pattern in its common/html\_re module, `(?:[^-]|-[^-]|--[^>])*-->` after the opener. That pattern lets the text of a comment contain `--->`. CommonMark 0.31.2 §6.6 says a comment's text does not include `-->`.

**Executed.**

- Parsing `x &lt;!-- a ---> c d --> e` inline gives one `html_inline` token that runs to the second `-->`.
- On the document `["x &lt;!-- a", "b ---> c", "d --> e", "f"]`, the oracle hides lines 1 and 2. The walk claims line 2 is live, which is correct by the specification.
- After the 🟡 2 fix, all 61 remaining reduced half-2 shapes hold a `--->` line. So do 8 of the 11 reduced config shapes.

**Why ⬜.** Nothing ships wrong. No reader hides a line because of an inline comment, and the oracle errs toward hiding more. Two risks remain. Its error could mask a future reader that newly hides such a line. And whoever widens `ALPHABET` will meet a red on correct code and may "fix" the walk toward the parser. Pinning the divergence as a named case in the oracle's own table closes both risks.

## Regression tests to plant

| Destination | Case | Seen red |
|---|---|---|
| `tests/test_routing_is_recorded.py` | the U+2028, form-feed and U+0085 shapes of 🟡 1 read the declaration | at `9b52cf25` (executed, probe) |
| `tests/test_the_mode_question_is_asked_once.py` | the `config.md` shape of 🟡 1 reads `Mode shared` | at `9b52cf25` (executed, probe) |
| `tests/test_a_rider_reaches_its_file.py` | the rider shape of 🟡 1 is read as one rider | at `9b52cf25` (executed, probe) |
| `tests/test_the_hooks_hide_what_a_renderer_hides.py` | `ALPHABET` gains `` >``` `` and two more; `FOUND` gains `[">```"]` | at `9b52cf25`: half 2 fails on `[">```"]` alone (executed) |
| `tests/test_the_hooks_hide_what_a_renderer_hides.py` | the oracle's `--->` divergence as a named case | not a defect case; it pins the parser |
| `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:799` | the sentence says pytest stops at collection | red once the sentence changes; the new case runs in the smith's slice |

## Facts for the evidence ledger

- `hooks/config.py#CONFIG_ROW` and `#CONFIG_HEADER` match only a line whose first character is a pipe. This is the ground for 🟡 2 changing no row today.
- `tests/commonmark_oracle.py#hidden` joins the lines it is given with `\n`. So the oracle sees the reader's split and never the file's own line breaks. A claim about 🟡 1's fix should be written against the post-fix code, not recorded from this round.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A line break that `str.splitlines` makes and CommonMark does not lets the walk hide a live routing declaration, a live `Mode` row and a live rider | `hooks/blocks.py:208` | open | executed: `routing.parse` gives None, `config_rows` gives nothing, the rider is gone, and the base read all three; the oracle cannot see it because it is handed the reader's split |
| 🟡 2 | `CONTAINER` needs a space after `>`, so `` >``` `` is claimed live and exact while a renderer hides it | `hooks/blocks.py:89` | open | executed: 1,599 of 1,888 half-2 disagreements reduce to that one line; half 1 fails for the config reader on 3 reduced shapes; the fix clears both and keeps the module green |
| 🟡 3 | With the parser missing, bin/test says the other cases still run, and pytest interrupts collection and runs none | `.github/scripts/run_tests.py:491` | open | executed: exit 2, `Interrupted: 1 error during collection`, zero cases run from the second module; the case at `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:799` pins the claim under a mock |
| ⬜ 4 | The oracle runs an inline comment past a `-->` that a `-` precedes, which CommonMark 0.31.2 excludes | `tests/commonmark_oracle.py:48` | open | executed: one `html_inline` token past the first closer; every remaining fuzz disagreement holds a `--->` line; no reader affected |
| ❓ | bin/test's parser-failure path under `-n auto` | `.github/scripts/run_tests.py:505` | ❓ out of verified scope | not run; the smith answers it in the slice that fixes 🟡 3 |
| ❓ | The per-reader case tables S5 to S8, S10, S12 and S15 were read in part and not run by this round | `tests/test_routing_is_recorded.py:717` | ❓ out of verified scope | only the property module was run here; the sealer's broad run answers the rest |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` in the clone at `9b52cf25` | exit 0, 49 passed |
| Probe: the 🟡 1 shapes (U+2028, form feed, U+0085) through `routing.parse`, `config_rows` and `comment_blocks`, and the oracle on the real text | routing None, config `[]`, rider `[]`; the oracle on the real text hides nothing |
| Probe: 40 seeds × 5,000 documents, `ALPHABET` plus 37 lines, halves 1 and 2 for all three readers | 1,888 half-2 disagreements in 116 reduced shapes; config leaves both in 12 documents; routing 0; rider check 0 |
| Probe: the same fuzz with `CONTAINER` fixed | 61 reduced half-2 shapes, every one holding `--->`; module corpus 0; `test_the_walk_is_exact_somewhere` passes |
| Probe: pytest in a virtualenv without markdown-it-py, over two modules | exit 2, interrupted at collection, zero cases |
| `python3 skills/evidence-check/scripts/evidence_check.py .` in the clone, one run, read-only | exit 0; 0 drifted and 0 broken in every file. A probe, not a seal |
| The broad gate: the full suite, lint and typecheck | not yet |

### 🟡 1

```python
import importlib.util, os
root = "."  # the clone at 9b52cf25
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(root, path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
routing = load("hooks/routing.py", "r")
OPEN = "<" + "!--"
text = ("A note " + OPEN + "\n\n| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n| Branch | feature/x |\n-->\n")
print(routing.parse(text))  # None at 9b52cf25
```

## Paste-ready fixes

### 🟡 1

`hooks/blocks.py`, below `CLOSER`:

```python
# The line breaks `str.splitlines` makes and CommonMark does not: CommonMark
# ends a line at "\n", "\r" or "\r\n" alone. Where a file holds one, a
# reader's line is not a renderer's line, and a fence or a comment opener the
# split put at a line's start is one no renderer sees there. So the walk
# claims nothing in such a file, and every reader keeps its base reading.
FOREIGN_BREAKS = frozenset("\x0b\x0c\x1c\x1d\x1e\x85  ")


def walk_text(text, lines):
    """`walk(lines)` for LINES split from TEXT, or a walk that claims no
    line where TEXT holds a break CommonMark does not honour."""
    if FOREIGN_BREAKS.isdisjoint(text):
        return walk(lines)
    count = len(lines)
    return Walk([LIVE] * count, [True] * count, [])
```

`hooks/routing.py`:

```python
def shown(lines, text=None):
    """[(index, line)] for each of LINES `table_rows` reads, ending removed.
    TEXT, where the caller has it, is what LINES were split from."""
    walked = blocks.walk(lines) if text is None else blocks.walk_text(text, lines)
    hidden = walked.hidden()
    return [
        (index, raw.rstrip("\r\n"))
        for index, raw in enumerate(lines)
        if index not in hidden
    ]

# in table_rows:
    for _index, line in shown(text.splitlines(), text):
```

`hooks/config.py`. The parameter goes through all three names, and every caller passes the text it split:

```python
def fence_map(lines, text=None):
    hidden, opened_at = hidden_lines(lines, text)
    ...

def hidden_lines(lines, text=None):
    walked = blocks.walk(lines) if text is None else blocks.walk_text(text, lines)
    base, base_opened = blocks.fence_only(lines)
    ...

def unfenced(lines, text=None):
    ...
    yield from fence_map(lines, text)[0]

# config_rows and refusal:
    for _index, line in unfenced(text.splitlines(), text):
```

The config reader's other callers:

```python
# skills/implement/scripts/seal.py, table_span (its lines keep their endings):
    for i, line in unfenced(lines, "".join(lines)):
# skills/implement/scripts/seal.py, the write guard:
        if fence_map(new.splitlines(), new)[1] is not None:
# skills/verify/scripts/broad_gate.py, hidden_row_at:
    hidden, _opened_at = config.hidden_lines(lines, text)
# skills/verify/scripts/broad_gate.py, fence_left_open:
    opened_at = config.fence_map(text.splitlines(), text)[1]
```

`.github/scripts/rider_check.py`:

```python
def quoted_lines(lines, text=None):
    ...
    walked = _blocks.walk(lines) if text is None else _blocks.walk_text(text, lines)
    ...

def comment_blocks(lines, rel=None, text=None):
    ...
    quoted = (
        quoted_lines(lines, text)
        if (rel or "").endswith(".md") and any(MARKER in line for line in lines)
        else set()
    )

# both callers, which split `text` themselves:
    comment_blocks(text.splitlines(), rel, text)
```

The cases:

```python
# tests/test_routing_is_recorded.py
@pytest.mark.parametrize("brk", [" ", "\x0c", "\x85"], ids=["ls", "ff", "nel"])
def test_a_break_commonmark_does_not_honour_hides_no_declaration(brk):
    """A line break `str.splitlines` makes and a renderer does not put the
    comment opener at no line's start, so the table under it is live and the
    base read it (#667, round 1 🟡 1)."""
    from block_shapes import OPEN, TABLE

    text = "\n".join([f"A note{brk}{OPEN}", "", *TABLE, "-->"]) + "\n"
    parsed = routing.parse(text)
    assert parsed is not None and parsed["review"] == CHAIN, parsed
```

```python
# tests/test_the_mode_question_is_asked_once.py
def test_a_break_commonmark_does_not_honour_hides_no_config_row():
    """#667, round 1 🟡 1: the same shape in config.md."""
    open_ = "<" + "!--"
    text = f"A note {open_}\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n-->\n"
    assert config.config_rows(text) == [("Mode", "shared")]
```

```python
# tests/test_a_rider_reaches_its_file.py
def test_a_break_commonmark_does_not_honour_quotes_no_rider():
    """#667, round 1 🟡 1: a fence run after U+2028 opens no fence for a
    renderer, so the rider below it is live and is read."""
    open_ = "<" + "!--"
    lines = (
        "# doc\n\nA note ```\n\n"
        f"{open_} RIDER: real\nVerified 2026-01-01 against r@abcdef12. -->\n\n```\n"
    )
    assert len(rc.comment_blocks(lines.splitlines(), "doc.md", lines)) == 1
```

The last case names the module under the local name that the case file already uses for `rider_check.py`.

### 🟡 2

`hooks/blocks.py:89`:

```python
# A container's marker run in front of a line: indentation, a block quote's
# `>`, a list item's bullet or number. What follows it is what the line is.
# A list marker needs a space, a tab or the line's end after it; a block
# quote's `>` needs nothing (CommonMark 5.1, the space after it may be
# omitted), so `>` followed by a fence run is a fence inside a quote.
CONTAINER = re.compile(r"^(?:[ \t]*(?:>|(?:[-+*]|\d{1,9}[.)])(?=[ \t]|$)))*[ \t]*")
```

`tests/test_the_hooks_hide_what_a_renderer_hides.py`:

```python
# ALPHABET, beside "> ```":
    ">```",
    ">" + OPEN,
    ">| a |",

# FOUND:
    # a block quote needs no space after its marker
    [">```"],
```

### 🟡 3

`.github/scripts/run_tests.py`, the returned sentence in `add_markdown_it`:

```python
    if subprocess.run(step).returncode != 0:
        return (
            f"bin/test: could not install {MARKDOWN_IT} into {venv} (the "
            "command above exited non-zero). The suite's CommonMark oracle "
            "imports it, so pytest stops at collection and runs no case. "
            "Remove that directory and run bin/test again to build it afresh "
            "with the parser in it."
        )
```

The comment in `main`, and the docstring's last sentence:

```python
    # The parser the oracle reads (#667). Its failure is a sentence and a
    # pytest run that stops at collection: the oracle's module cannot import,
    # and pytest runs no case while any module fails to collect. It decides
    # nothing about `-n auto`.
```

```python
    What a failed install costs is different, and the sentence says so: the
    run is not serial, it stops at collection, because the oracle's module
    cannot import and pytest runs nothing while one module fails to collect.
```

`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:799`: rename the case so its name ends "and pytest is still called" rather than "and the suite still runs", and replace the import assertion:

```python
    assert "stops at collection and runs no case" in err, err
```

### ⬜ 4

`tests/test_the_hooks_hide_what_a_renderer_hides.py`, `test_the_oracle_names_each_kind_it_hides`, one more row and the id `"past the first closer"`:

```python
        # markdown-it-py 4.2.0 runs a comment past a closer a `-` precedes,
        # which CommonMark 0.31.2 §6.6 does not; pinned so a wider corpus
        # meets the divergence by name. The walk follows the specification.
        (
            ["x " + OPEN + " a", "b ---> c", "d " + CLOSE + " e", "f"],
            {1: "comment", 2: "comment"},
        ),
```

Needs a fix: yes — 🟡 1, 🟡 2 and 🟡 3

Loses a record or crashes: no

## Proof

Files opened this round, all at `9b52cf25` in the clone:

- `hooks/blocks.py`
- the diff of `hooks/config.py`, and `hooks/config.py` lines 1–40 and 230–520
- the diffs of `hooks/routing.py`, `.github/scripts/rider_check.py`, `.github/scripts/run_tests.py`, `.github/workflows/test.yml`, `CONTRIBUTING.md`, `templates/config.md`, `skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/unverified_check.py`, `skills/implement/scripts/seal.py` and `skills/evidence-check/scripts/evidence_check.py`
- `.github/scripts/rider_check.py` lines 120–330 and 396–406
- `.github/scripts/run_tests.py` lines 95–190 and 440–520
- `.github/workflows/test.yml` lines 1–80
- `skills/verify/scripts/broad_gate.py` lines 640–835 and 1060–1110
- `skills/implement/scripts/seal.py` lines 1470–1500 and 1570–1610
- `tests/commonmark_oracle.py`, `tests/block_shapes.py` and `tests/test_the_hooks_hide_what_a_renderer_hides.py`
- the diffs of `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`, `tests/test_unverified_rows_close.py`, `tests/test_release_hygiene.py`, `tests/test_a_script_copied_alone_exits_2.py` and `tests/test_routing_is_recorded.py`
- `seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/` `spec.md`, `overview.md`, `survivors.md` and `changelog.md`
- markdown-it-py 4.2.0's common/html\_re module, its inline HTML rule and its table rule, in the clone's `.venv`
