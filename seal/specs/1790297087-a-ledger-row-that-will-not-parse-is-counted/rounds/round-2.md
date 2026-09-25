# 1790297087-a-ledger-row-that-will-not-parse-is-counted — review round 2

| Field | Value |
|---|---|
| Target SHA | aca4f283c51f308a75eb1f4cd8fb2cc2c4fd86f5 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 606 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `eeadbfeb30e3e286bdfaff73a26e28b942ab074f..c8218c815deecdefbc3702099201fba5b05a186d`, 2 commits |
| Contract changes | refused_coordinate → round-1-report.md, round-1.md, round-2-report.md, round-2.md, malformed_rows |
| New units | URL_RE (depth 1); PATH_HASH_RE (depth 1); test_a_coordinate_the_opener_list_misses_is_named (depth 1); test_a_directive_or_a_string_holding_a_hash_is_prose (depth 1) |
| Needs a fix | yes — finding 1 (rule (a)'s new boundary misses #299's bare-quote shape when the quoted line holds a URL, as well as `path@hash` and non-ASCII or digit-opening locators beside a good anchor, and it refuses `#ifdef` in prose) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790297087 is the verifying round over round 1's fixes (db92ea3b..7281cc4b) at aca4f283. For each round-1 verdict closed as fixed or answered, it asks whether it is actually closed. It reads the units the fixes created, refused_coordinate and LOCATOR_OPEN_RE, as a finding surface, probing rule (a)'s new boundary in both directions. It also reads the Windows fixture-encoding change and the three new survivors.md rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `refused_coordinate` looks at the character after a `#`, not at the path before the mark. Beside a good anchor it misses a bare-quote coordinate whose quoted line holds a URL, a `path@hash` with no anchor, and a locator opening with a digit, a non-ASCII letter or nothing. Outside backticks, `#ifdef` exits 2 | `skills/evidence-check/scripts/evidence_check.py:1605-1615` | **fixed** `c003fee90d51cf62d1da6187521474017f58091a` | fixed at c003fee90d51cf62d1da6187521474017f58091a; Executed: five probe cases red at aca4f283 and green with the fix below. The checker at db92ea3b named each missed shape. The unit was created by round 1's fixes |
| ⬜ 2 | The *Rule (a)'s reach* row still states the build's rule, which round 1's fix replaced | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/overview.md:19` | answered | corrected at c003fee90d51cf62d1da6187521474017f58091a: `overview.md`'s *Rule (a)'s reach* row and the first *Fed back into the spec* bullet state the rule as it now is; Read. A correction to the run's paperwork, not counted in Needs a fix |
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

## Paste-ready fixes

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
```python
    - a coordinate the patterns refused: what is left of the cell once every
      `ANCHOR_RE` and `OLD_COORD_RE` match is blanked, and every URL in it,
      still holds both marks, a `#` glued to a path or a file name, or a path
      followed by `@` and a hash. An issue number `#299` or `org/repo#299`, a
      directive `#ifdef`, a decorator `@cache` and an address are prose, in a
      span or out of one;
```
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
```python
    live `EXPANDS` row, and one whose locator opens with a digit, which is
    named whether it holds one mark or both. Each is named whole, as
    written."""
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1682-1685` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1603` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/evidence-advisor.py:184-194` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/ledger.md:76` | round 1's ⬜ 4 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1690` | round 1's ❓ — out of verified scope |
| round-1 | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.12.0.md` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_rider_reaches_its_file.py:181`, `:204` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:72-77` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2700-2701`, `:2050` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_row_points_by_content.py:827` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
