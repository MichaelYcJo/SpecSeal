# 1790297087-a-ledger-row-that-will-not-parse-is-counted — review round 3

| Field | Value |
|---|---|
| Target SHA | b43d65cb0f1856ae58888aad7c10030f29ba7ac7 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 606 |
| Broad gate | 7db394a3 against 7b557144 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1, 2 and 3 (rule (a)'s boundary: a dotless file name's quoted, `<module>` or `_` locator is silent, and an issue number glued to non-ASCII punctuation or a one-digit version after a dotted word exits 2), each deferred to a new issue because the run is capped |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790297087 is the verifying round after the run's one reopening. It reads round 2's fixes (eeadbfeb..c8218c81) at b43d65cb and ends the run whatever it finds. It asks whether round 2's finding is closed, whether rule (a), rebuilt on the coordinate's own shape, holds in both directions, whether the report stayed unchanged beyond two markers, and whether PR #606's CI is green at that tip.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a file name with no dot, glued to a quoted line, `<module>` or a `_` name, is silent beside a good anchor; the dotless branch takes only a letter | `skills/evidence-check/scripts/evidence_check.py:1627` | deferred #614 | Executed: three shapes return nothing at b43d65cb; three planted cases red there and green with the fix below. Inside `refused_coordinate`, which round 2's fixes rewrote. The run is capped, so it goes to a new issue the orchestrator files · NAME NOT IN TREE |
| 🟡 2 | an issue number glued to a possessive, an em dash, a curly quote, a Korean particle or a link's `](` exits 2; the punctuation strip is ASCII closers only | `skills/evidence-check/scripts/evidence_check.py:1622-1624` | deferred #614 | Executed: five prose shapes named MALFORMED at b43d65cb, beside a good anchor and alone; five planted cases red there and green with the fix below |
| 🟡 3 | `PATH_HASH_RE` takes one hex digit, so `chart.js@4`, `vue.js@3` and an address with a hex host exit 2 | `skills/evidence-check/scripts/evidence_check.py:1610` | deferred #614 | Executed: three prose shapes named MALFORMED at b43d65cb; three planted cases red there and green with the fix below. A unit round 2's fixes created |
| 🟢 | round 2's blocking finding is closed for every shape it named — the #299 bare quote holding a URL, `path@hash`, locators opening with a digit, a non-ASCII letter or nothing, and `#ifdef` as prose | `skills/evidence-check/scripts/evidence_check.py:1613` | verified | Executed: 7 of the 10 new or changed cases fail against the checker at eeadbfeb and all pass at b43d65cb; the other 3 (`Makefile#build`, a path-less quoted line, a path-less coordinate with both marks) were already named at eeadbfeb and are guards. The class stays open at the edges, which are findings 1–3 |
| 🟢 | the fix pass's divergence, stripping a word's trailing `.,;:!?)]` before judging, is sound | `skills/evidence-check/scripts/evidence_check.py:1622` | verified | Read: stripping from the right never changes the head and only helps the `@` match, so the only shape it silences is a digits-only locator, which is prose by design. Executed: removing the strip turns the directive case red (1 failed, 133 passed) |
| 🟢 | round 2's ⬜ 2 is answered: the *Rule (a)'s reach* row and the *Fed back* bullet state the rule round 2's fix built | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/overview.md:19`, `:62` | verified | Read. One clause overstates the code for a dotless file name, which is 🟡 1's shape and closes with its fix |
| 🟢 | `round-2-report.md` changed only by two ` · NAME NOT IN TREE` markers | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/rounds/round-2-report.md:22`, `:106` | verified | Read: eeadbfeb..c8218c81 has two hunks in the file, each appending the marker to a line that names the retired constant; no other byte changed |
| 🟢 | `ANCHOR_RE` and `resolve_unit` are unchanged | `skills/evidence-check/scripts/evidence_check.py:72`, `:469` | verified | Executed: each unit's text is byte-identical at the base 7b557144, at eeadbfeb and at b43d65cb; the fix range's hunks lie between 1602 and 1700 |
| 🟢 | the new `survivors.md` row quotes real text and its grounds hold | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/survivors.md:36` | verified | Executed: the quote is `tests/test_a_rider_reaches_its_file.py:181`; the branch sweep from 7b557144 exits 0 with 4 survivors, all exempt |
| 🟢 | round 1's findings 1–4 stay closed after round 2's rewrite of the unit | `skills/evidence-check/scripts/evidence_check.py:1613`, `hooks/evidence-advisor.py:190`, `seal/ledger.md:76` | verified | Executed: the four reader modules round 2 ran, 196 passed at b43d65cb, including the cases each was pinned by; `--strict .` 0 broken |
| 🟢 | the tree reads clean at the target | `seal/ledger.md`, `seal/releases/*.md`, `seal/ledger/*.md` | verified | Executed: `--strict .` gives 2258 ok, 0 drifted, 0 broken, 0 malformed, exit 0 |
| ❓ | whether a claim row with an empty `Code grounds` cell should stay silent | `skills/evidence-check/SKILL.md:497-499` | ❓ out of verified scope | Carried from rounds 1 and 2, and not touched by the fix range. Answerer: the repository owner |
| 🟢 | the `windows-latest` leg passes at b43d65cb, the new non-ASCII parameters included | PR #606's checks, `pytest (windows-latest, 3.12)` | verified | Executed (read from CI): pass in 13m13s, and so did `ubuntu-latest`, `macos-latest`, `lint` and `ledger`. Read: the harness decodes the checker's output as UTF-8, and the checker reconfigures its streams to UTF-8 |
| ❓ | whether the `release` leg turns green once this round's record exists | PR #606's checks, `release` job | ❓ out of verified scope | Executed: it fails at b43d65cb because `chain_check.py` refuses `Pass` beside round-2.md's `Fixes checked by: nobody`, which is the state this round exists to clear. Answerer: the orchestrator, after round-3.md is written and round-2.md's cell names it |

## Paste-ready fixes

```python
# A hash after a path with no anchor between them: `src/a.py@abcdef12`. An
# address ends in a domain, so a hex run followed by `.` is not one, and a
# run shorter than the six characters `ANCHOR_RE` takes is a version.
PATH_HASH_RE = re.compile(r"[0-9a-f]{6,}(?![\w.])")
# An issue number: a run of digits that no ASCII word character continues.
# What follows it is the sentence's -- a closing mark, a possessive, a dash,
# a particle a language glues on, the `](` of a link whose URL was blanked.
ISSUE_TAIL_RE = re.compile(r"\d+(?![A-Za-z0-9_])")


def refused_coordinate(s):
    """True where S, left over after both patterns, is a coordinate: both
    marks, or a `#` glued to a path or a file name, or a hash after a path.
    `#299`, `org/repo#299's`, `#ifdef`, `C#` and `@cache` are prose."""
    s = URL_RE.sub(" ", s)
    if "#" in s and "@" in s:
        return True
    # A word's closing punctuation is the sentence's, not the word's, so
    # `src/a.py@abcdef12.` is a path followed by a hash.
    for token in (word.rstrip(".,;:!?)]") for word in s.split()):
        head, mark, tail = token.partition("#")
        if mark and not ISSUE_TAIL_RE.match(tail):
            if "/" in head or "." in head:
                return True
            if head[-1:].isalnum() and (
                tail[:1].isalpha() or tail[:1] in ("_", '"', "<")
            ):
                return True
            if not head and tail[:1] in ('"', "<"):
                return True
        head, mark, tail = token.partition("@")
        if mark and ("/" in head or "." in head) and PATH_HASH_RE.match(tail):
            return True
    return False
```
```python
@pytest.mark.parametrize(
    "coord", ['Makefile#"all: build"', "Makefile#<module>", "Makefile#_private"]
)
def test_a_file_name_with_no_dot_takes_any_locator(repo, coord):
    """Round 3's finding 1. A file name with no dot glued to a quoted line,
    `<module>` or `_name` is a coordinate as `Makefile#build` is."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text(encoding="utf-8")).group(0)
    ledger.write_text(f"| A | {good}, `{coord}` |\n", encoding="utf-8")
    r = run(["."], str(repo))
    assert f"MALFORMED {coord}  " in r.stdout, r.stdout


@pytest.mark.parametrize(
    "prose",
    [
        "org/repo#299's",
        "org/repo#299—see",
        "“org/repo#299”",
        "org/repo#299에서",
        "[org/repo#299](https://example.com/org/repo/issues/299)",
        "chart.js@4",
        "`vue.js@3`",
        "jane.doe@beef",
    ],
)
def test_an_issue_number_or_a_version_glued_to_a_word_is_prose(repo, prose):
    """Round 3's findings 2 and 3. Digits that no ASCII word character
    continues are an issue number whatever the sentence glues after them,
    and a path followed by `@` takes a hash only as long as a hash is."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text(encoding="utf-8")).group(0)
    ledger.write_text(f"| A | {good}, {prose} |\n", encoding="utf-8")
    r = run(["."], str(repo))
    assert "0 old-format · 0 malformed" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout
```

## Executed probes

| What was run | Result |
|---|---|
| `malformed_rows` on 56 cell shapes, each beside a good anchor and alone, at b43d65cb | every shape round 2's 🟡 1 named is right; misses and refusals as listed in 🟡 1–3 |
| The 10 new-case parameters with the checker from eeadbfeb swapped in | 7 failed, 3 passed |
| Round 2's fix with the trailing-punctuation strip removed, then `test_a_row_points_by_content.py` | 1 failed (the directive case), 133 passed |
| `bin/test` on `test_a_row_points_by_content.py`, `test_evidence_check.py`, `test_dispatch.py` and `test_the_lenient_run_says_what_the_broad_gate_will_say.py` at b43d65cb | 196 passed, exit 0 |
| `evidence_check.py --strict .` at b43d65cb | `total: 2258 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0 |
| `ANCHOR_RE` and `resolve_unit` text at 7b557144, eeadbfeb and b43d65cb | identical |
| `survivor-check --range 7b557144..b43d65cb --exempt survivors.md` | 4 survivors, all exempt, exit 0 |
| `survivor-check --range eeadbfeb..c8218c81 --exempt survivors.md` | exit 1, one place: `seal/releases/0.13.0.md:10`, sharing *a span holding* only |
| The 11 planted parameters below, at b43d65cb | 11 failed |
| The three fixes below applied, then the 11 planted parameters and the four modules | 207 passed, exit 0; ruff check and format clean on the checker |
| The three fixes applied, then `malformed_rows` on the 56 shapes | 🟡 1–3's shapes right; `Makefile#1x` and `src/a.py@abc` silent, as the trade states |
| `gh pr checks 606` at b43d65cb | lint, ledger, `ubuntu-latest`, `macos-latest` and `windows-latest` (13m13s) pass; `release` fails on round-2's `Fixes checked by` |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it at b43d65cb. It is the sealer's, and it comes due now: this round is the capped run's last and leaves nothing open on this branch, since findings 1–3 are deferred |

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
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1605-1615` | round 2's 🟡 1 — fixed |
| round-2 | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/overview.md:19` | round 2's ⬜ 2 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1696` | round 2's 🟢 — verified |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1604` | round 2's 🟢 — verified |
| round-2 | `hooks/evidence-advisor.py:190` | round 2's 🟢 — verified |
| round-2 | `skills/evidence-check/SKILL.md:497-499` | round 2's ❓ — out of verified scope |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:72`, `:469` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.14.0.md`, the work item's fragment | round 2's 🟢 — verified |
| round-2 | `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/survivors.md:25-27` | round 2's 🟢 — verified |
| round-2 | `tests/test_a_row_points_by_content.py`, `tests/test_dispatch.py` | round 2's 🟢 — verified |
| round-2 | PR #606's checks | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1, 🟡 2, 🟡 3 — rule (a)'s boundary in `refused_coordinate` and `PATH_HASH_RE`: a dotless file name's locator, an issue number glued to non-ASCII-punctuation text, a one-digit hex run after a dotted word. One unit, one issue, the paste-ready fixes below | a new issue the orchestrator files, labelled `evidence-check` and `from-review` | the orchestrator files it; the repository owner schedules it |
