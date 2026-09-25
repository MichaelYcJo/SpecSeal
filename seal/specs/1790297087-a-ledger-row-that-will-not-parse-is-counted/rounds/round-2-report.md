# Round 2 report — a ledger row that will not parse is counted

Verifying round of work item 1790297087 (#299, #322), PR #606. Target
`aca4f283`, fix range `db92ea3b..7281cc4b` (3 commits) and the record-closing
commit after it. Read against `rounds/round-1.md`'s verdicts and its
`New units` row. Probes ran in a `git clone --no-local` at the target, under
this round's scratch directory, and nothing was written in the worktree
except this file.

## What the fix pass claimed, and what I found

| Claimed | Found |
|---|---|
| 7 new or changed cases red before the fix, green after | **Executed.** With `evidence_check.py` and `hooks/evidence-advisor.py` put back to `db92ea3b`, the 8 selected cases gave 7 failed and 1 passed. The one that passed is row D of `test_what_is_left_of_a_cell_is_read_span_by_span`, a guard that the fix keeps naming a digit-opening locator with both marks. It passes against both checkers, as a guard should. At `aca4f283` the four reader modules give 186 passed |
| `evidence_check --strict .` at 0 malformed | **Executed**: `total: 2254 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0 |
| `survivor-check` over the branch: every survivor excused | **Executed** over `db92ea3b..aca4f283` with the exemption file: the three rows round 1's fix pass added are the three exempted places, exit 0 |
| `ANCHOR_RE` and `resolve_unit` unchanged | **Executed**: `git diff 7b14b1fb..aca4f283` of the checker touches neither. The fix range has 3 hunks, all between lines 1598 and 1700 |
| 39 reader modules, 1964 passed | **Not re-run.** I ran the four modules that hold every case the fix range touched. The wider count is the fix pass's claim |

## 🟡 1 — `refused_coordinate` looks at the character after a `#`, not at the path before it

`skills/evidence-check/scripts/evidence_check.py:1605-1615`. This is `LOCATOR_OPEN_RE` and `refused_coordinate`, both units that round 1's fixes created. The code is round 1's own paste-ready fix, copied exactly.

**What is wrong (executed).** Rule (a) now names a leftover only when it holds both marks, or when a `#` in it is followed by an ASCII letter, `_`, `"` or `<`. It also skips the whole leftover when `://` appears anywhere in it. I probed that boundary in both directions, with each shape beside a good anchor.

- **Coordinates it misses.** Each of these was named by the checker at `db92ea3b`, before round 1's fix:
  - `` `src/service.py#"X = "https://example.com""@abcdef12` `` is #299's own shape: a bare `"` inside a quoted locator. It goes silent when the quoted line holds a URL, because `"://" in s` returns before the both-marks test. A quoted locator is a line of text, and a line can hold a URL.
  - `` `src/service.py@abcdef12` `` has a path and a hash but no anchor. It holds one mark, `@`, and the rule never names a lone `@`.
  - `` `src/service.py#1x` ``, `` `docs/a.ko.md#개요` `` and `` `docs/a.md#Überblick` `` each open the locator with a character outside the ASCII opener list. This repository writes Korean headings itself.
  - `` `src/a.py#` `` has an empty locator.

  When one of these is alone in its cell, rule (b) names it, but with the "cites no coordinate" remedy and not the parse remedy. Beside a good anchor, nothing names it.
- **Prose it refuses.** This is new since the fix, and it affects bare words: `#ifdef DEBUG` and `#define MAX` outside backticks now exit 2. Before the fix, a bare word had to hold both marks. Inside code spans, `` `#include <x.h>` ``, `` `#fff` ``, `` `#noqa` `` and `` `"#"` `` are refused as they were at `db92ea3b`. That makes them the same class but not a regression.

**Why it matters.** The first missed shape is the silence #299 was opened to end. It returned through the unit that closed round 1's finding 1. The directive shape is the first half of that same finding (exit 2 on prose) in another spelling. A repository with C sources writes `#ifdef` in prose. None of these shapes is in this tree today. An executed scan of every `Code grounds` cell found no leftover that is URL-exempt, carries a lone `@`, or holds an unnamed `#`. So the cost falls on repositories that install the plugin.

**The fix (executed).** Decide a `#` by what comes before it: a path, or a file name joined to a letter. An all-digit locator is an issue number. Name a path that `@` and a hex run follow. Blank a URL instead of excusing the whole text. With the fix applied in the clone:
- the four modules gave 186 passed;
- the five probe cases in *Regression tests to plant* were red at `aca4f283` and green with the fix;
- `--strict .` read 0 malformed and 1 drifted, and the drifted row is the fragment row citing the edited unit.

Round 1's probe covered 20 shapes. None of these was among them.

## ⬜ 2 — `overview.md` still describes the rule as it was before round 1's fix

`seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/overview.md:19`, the *Rule (a)'s reach* row. It reads *Leftover code spans holding a `#` or `@`, and words outside a span holding both*, which is the build's rule. Round 1's fix replaced that rule, and 🟡 1's fix would replace it again. The row is paperwork for this run, so this is a correction and not counted in `Needs a fix`. The fix pass should update it in the same commit as 🟡 1.

## Round 1's verdicts, answered

- **Finding 1**: the shapes it named are closed. Executed: `` `#299` ``, `` `@cache` ``, `` `ops@example.com` `` and a URL beside a good anchor all read 0 malformed. Bare `src/service.py#Box` and `b.py#g>h` are named. Both cases were red at `db92ea3b`. The class is still open, and that is this round's 🟡 1, inside the new unit.
- **Finding 2**: closed. `BARE_QUOTE_RE` at `:1604` uses a positive lookahead. Executed: `a.py#"line"`, `a.py#f>"g"`, `a.py#"line">"claim"` and `#"line"` now get the missing-hash remedy. `a.py#"X = "ok""@abcdef12` and `a.py#"a" b"@abc` still get the bare-quote remedy.
- **Finding 3**: closed. Executed red first: the S11 case and the docstring pin were red against the advisor at `db92ea3b`. Read: the header at `hooks/evidence-advisor.py:190` counts texts, and each row line carries its own remedy.
- **Finding 4**: closed. Executed: `resolve_unit` resolves `SEPARATORS` to lines 547–547, and the three anchors of the row at `seal/ledger.md:76` read `OK`.
- **The empty-cell question**: still the owner's to answer. The fix pass wrote the behaviour into `skills/evidence-check/SKILL.md` §*Known limits*, lines 497–499. That records the choice and does not settle it.
- **`survivors.md`'s three new rows**: read, and each is sound. The quotes stand at `skills/evidence-check/SKILL.md:257`, `evidence_check.py:1655` and `:1707`. Each is a remedy the removed closing line restated: the verdict row's action cell, `malformed_remedy`'s text and `malformed_rows`' text. The advisor now prints the last two on each row. The first cell's wording is general, and it still tells a bare-quote row whose hash is right to write `@00000000`. That costs one `--reverify` and misleads nobody.
- **The Windows fixture change**: read. The 23 `encoding="utf-8"` additions change no assertion. An executed static scan of both test files, using the AST, found no `read_text` or `write_text` call without `encoding` whose literal or module-constant content is non-ASCII. The test helper `run` already decodes as UTF-8. I could not read the `windows-latest` leg, because `gh` has no host configured in this checkout.

## Regression tests to plant

Destination: `tests/test_a_row_points_by_content.py`, after `test_an_unticked_coordinate_with_one_mark_is_named`. They are in the fenced block under 🟡 1 below. The five cases, run as probes, were red at `aca4f283` and green with the fix.

## Facts for the evidence ledger

- The fragment row for rule (a) (`seal/ledger/1790297087-a-ledger-row-that-will-not-parse-is-counted.md`, row 2) cites `refused_coordinate`. 🟡 1's fix drifts that anchor. The row's Re-read note should then state the new boundary, and should cite the new case as well as `test_prose_marks_beside_a_good_anchor_are_not_refused`.
- Executed on this tree: every `Code grounds` leftover once `ANCHOR_RE` and `OLD_COORD_RE` are blanked is empty. None is URL-exempt, none carries a lone `@`, and none holds an unnamed `#`. No parsed quoted locator holds `://`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `refused_coordinate` looks at the character after a `#`, not at the path before the mark. Beside a good anchor it misses a bare-quote coordinate whose quoted line holds a URL, a `path@hash` with no anchor, and a locator opening with a digit, a non-ASCII letter or nothing. Outside backticks, `#ifdef` exits 2 | `skills/evidence-check/scripts/evidence_check.py:1605-1615` | open | Executed: five probe cases red at aca4f283 and green with the fix below. The checker at db92ea3b named each missed shape. The unit was created by round 1's fixes |
| ⬜ 2 | The *Rule (a)'s reach* row still states the build's rule, which round 1's fix replaced | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/overview.md:19` | open | Read. A correction to the run's paperwork, not counted in Needs a fix |
| 🟢 | round 1's finding 1 is closed for the shapes it named: issue number, decorator, address and URL beside a good anchor are prose, and a bare `src/service.py#Box` and `b.py#g>h` are named | `skills/evidence-check/scripts/evidence_check.py:1696` | verified | Executed: both new cases red at db92ea3b and green at aca4f283. The class is still open, which is this round's finding 1 |
| 🟢 | round 1's finding 2 is closed: a quoted locator with no hash gets the missing-hash remedy | `skills/evidence-check/scripts/evidence_check.py:1604` | verified | Executed: four shapes get the missing-hash remedy, two bare-quote shapes keep theirs, and both parametrized cases were red at db92ea3b |
| 🟢 | round 1's finding 3 is closed: the advisor header counts texts and the closing line is gone | `hooks/evidence-advisor.py:190` | verified | Executed: the S11 case and the docstring pin were red against the advisor at db92ea3b and are green at aca4f283 |
| 🟢 | round 1's finding 4 is closed: `SEPARATORS` is cited by name | `seal/ledger.md:76` | verified | Executed: resolves to 547-547, and all three anchors in the row read OK |
| ❓ | Whether a claim row with an empty `Code grounds` cell should stay silent. The fix pass documented the silence in Known limits | `skills/evidence-check/SKILL.md:497-499` | ❓ out of verified scope | Carried from round 1, and documenting it does not settle it. Answerer: the repository owner |
| 🟢 | `ANCHOR_RE` and `resolve_unit` are unchanged | `skills/evidence-check/scripts/evidence_check.py:72`, `:469` | verified | Executed: neither is touched by the diff from 7b14b1fb to aca4f283, and every fix-range hunk lies between lines 1598 and 1700 |
| 🟢 | The tree reads clean, and the repaired rows the fix range re-read resolve | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.14.0.md`, the work item's fragment | verified | Executed: `--strict .` gives 2254 ok and 0 malformed, exit 0 |
| 🟢 | The three new rows in `survivors.md` quote real text, and their grounds hold | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/survivors.md:25-27` | verified | Executed: survivor-check exits 0 with all three exempt. Read: each quote is a per-shape remedy the removed line restated |
| 🟢 | The 23 fixture encodings change no assertion and leave no non-ASCII fixture unencoded | `tests/test_a_row_points_by_content.py`, `tests/test_dispatch.py` | verified | Read, plus an executed AST scan that found 0 such calls. The four touched modules compile under -W error on 3.13.5 |
| ❓ | Whether the `windows-latest` leg passes at aca4f283 | PR #606's checks | ❓ out of verified scope | `gh` has no host configured in this checkout. Answerer: the orchestrator, from the PR's checks |

## Executed probes

| What was run | Result |
|---|---|
| `evidence_check.py --strict .` at aca4f283 | `total: 2254 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0 |
| `survivor_check.py --range db92ea3b..aca4f283 --exempt` with the work item's `survivors.md` | 23 removed sentences, 3 survivors, all exempt, exit 0 |
| `bin/test` on `test_a_row_points_by_content.py`, `test_dispatch.py`, `test_evidence_check.py` and `test_the_lenient_run_says_what_the_broad_gate_will_say.py` at aca4f283 | 186 passed, exit 0 |
| The 8 new or changed cases against the checker and advisor at db92ea3b | 7 failed, 1 passed (row D's guard), exit 1 |
| `malformed_rows` on 35 cell shapes, each beside a good anchor and alone, at aca4f283 and at the checker from 7b14b1fb | the misses and refusals listed under 🟡 1. At 7b14b1fb every missed span shape was named |
| `resolve_unit` for `SEPARATORS`, and `check_text` on its row | `547-547`, and three `OK` |
| Leftover scan over every `Code grounds` cell of `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` | 0 URL-exempt, 0 lone `@`, 0 unnamed `#` |
| AST scan of both test files for `read_text` or `write_text` without `encoding` whose content is non-ASCII | 0 |
| Four touched `.py` files compiled under `-W error`, Python 3.13.5 | exit 0 each |
| 🟡 1's fix applied, then the same four modules | 186 passed, exit 0 |
| 🟡 1's fix applied, then five probe cases (the four missed shapes, and one directive-and-string prose case) | 5 passed. At aca4f283 without the fix: 5 failed |
| 🟡 1's fix applied, then `--strict .` | 0 malformed. 1 drifted: the fragment row citing the edited unit |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it. It belongs to the sealer, and it comes due once a round leaves nothing open. This round leaves 🟡 1 open |

## Paste-ready fixes

### 🟡 1

Replaces lines 1605–1615 of `skills/evidence-check/scripts/evidence_check.py` (`LOCATOR_OPEN_RE` and `refused_coordinate`):

```python
# A URL is prose, `#fragment` and all, but only the URL: a quoted locator is a
# line of text and may quote one, so the URL is blanked and the rest is read.
URL_RE = re.compile(r'[A-Za-z][A-Za-z0-9+.-]*://[^\s"`]*')
# A hash after a path with no anchor between them: `src/a.py@abcdef12`. An
# address ends in a domain, so a hex run followed by `.` is not one.
PATH_HASH_RE = re.compile(r"[0-9a-f]+(?![\w.])")


def refused_coordinate(s):
    """True where S, left over after both patterns, is a coordinate: both
    marks, or a `#` glued to a path or a file name, or a hash after a path.
    `#299`, `org/repo#299`, `#ifdef`, `C#` and `@cache` are prose."""
    s = URL_RE.sub(" ", s)
    if "#" in s and "@" in s:
        return True
    for token in s.split():
        head, mark, tail = token.partition("#")
        if mark and not tail.isdigit():
            if "/" in head or "." in head:
                return True
            if head[-1:].isalnum() and tail[:1].isalpha():
                return True
            if not head and tail[:1] in ('"', "<"):
                return True
        head, mark, tail = token.partition("@")
        if mark and ("/" in head or "." in head) and PATH_HASH_RE.match(tail):
            return True
    return False
```

The first bullet of `malformed_rows`' docstring (`:1672-1676`):

```python
    - a coordinate the patterns refused: what is left of the cell once every
      `ANCHOR_RE` and `OLD_COORD_RE` match is blanked, and every URL in it,
      still holds both marks, a `#` glued to a path or a file name, or a path
      followed by `@` and a hash. An issue number `#299` or `org/repo#299`, a
      directive `#ifdef`, a decorator `@cache` and an address are prose, in a
      span or out of one;
```

The docstring of `test_prose_marks_beside_a_good_anchor_are_not_refused`, and the cases to plant after `test_an_unticked_coordinate_with_one_mark_is_named`:

```python
def test_prose_marks_beside_a_good_anchor_are_not_refused(repo):
    """Round 1's finding 1. An issue number, a decorator, an annotation, an
    address and a URL fragment in a code span are prose, exactly as `(#299)`
    outside one is; refusing them exits 2 on prose. A leftover is a
    coordinate when it holds both marks, a `#` glued to a path or a file
    name, or a path followed by `@` and a hash, and a URL is blanked first."""


@pytest.mark.parametrize(
    "coord",
    [
        'src/service.py#"X = "https://example.com""@abcdef12',
        "src/service.py@abcdef12",
        "src/service.py#1x",
        "docs/a.ko.md#개요",
    ],
)
def test_a_coordinate_the_opener_list_misses_is_named(repo, coord):
    """Round 2's finding 1. A `#` is a coordinate's when a path precedes it,
    not when an ASCII letter follows it, and a URL inside a quoted line is
    blanked rather than excusing the whole text: the first shape is #299's
    own, and it had gone silent beside a good anchor."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text(encoding="utf-8")).group(0)
    ledger.write_text(f"| A | {good}, `{coord}` |\n", encoding="utf-8")
    r = run(["."], str(repo))
    assert f"MALFORMED {coord}  " in r.stdout, r.stdout


def test_a_directive_or_a_string_holding_a_hash_is_prose(repo):
    """Round 2's finding 1, the other half: a `#` that opens a word is not a
    locator, outside backticks or in a span."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text(encoding="utf-8")).group(0)
    ledger.write_text(
        f"| A | {good}, guarded by #ifdef DEBUG, `#include <x.h>`, `\"#\"`, "
        "org/repo#299 |\n",
        encoding="utf-8",
    )
    r = run(["."], str(repo))
    assert "0 old-format · 0 malformed" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout
```

Row D's sentence in `test_what_is_left_of_a_cell_is_read_span_by_span`'s docstring (`:1008-1010`) names the unit this fix removes. Reworded:

```python
    live `EXPANDS` row, and one whose locator opens with a digit, which is
    named whether it holds one mark or both. Each is named whole, as
    written."""
```

Needs a fix: yes — finding 1 (rule (a)'s new boundary misses #299's bare-quote shape when the quoted line holds a URL, as well as `path@hash` and non-ASCII or digit-opening locators beside a good anchor, and it refuses `#ifdef` in prose)
Loses a record or crashes: no

## Proof

Files opened this round:
- `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/`: `rounds/round-1.md`, `spec.md` (lines 1–200), `overview.md` (lines 15–25), `survivors.md` and `changelog.md`.
- `skills/evidence-check/scripts/evidence_check.py`: lines 40–120 and 1560–1760.
- `skills/evidence-check/SKILL.md`: lines 257 and 486–500.
- `hooks/evidence-advisor.py`: the fix diff.
- The two test files, through the fix diff, and the `run` helper at lines 50–57.
- `bin/test` and `bin/survivor-check`.
- The full fix diff `db92ea3b..7281cc4b`, and the record diff `7281cc4b..aca4f283`.

The probe clone and its probe files were deleted before handing over.
