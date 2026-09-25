# Round 3 report — 1790297087-a-ledger-row-that-will-not-parse-is-counted

Target SHA `b43d65cb0f1856ae58888aad7c10030f29ba7ac7`, PR #606, branch
`fix/299-a-ledger-row-that-will-not-parse-is-counted`. This is the verifying
round after the run's one reopening, so the run is capped and this record ends
it. Its surface is round 2's fix range, `eeadbfeb..c8218c81` (2 commits), and
the units round 2's `New units` row names: `URL_RE`, `PATH_HASH_RE`, the two
new cases, and the rewritten `refused_coordinate`.

Probes ran in a `git clone --no-local` of the branch at the target SHA, in
the round's scratch directory. Nothing was written in the orchestrator's tree
except this file.

## Summary

Round 2's 🟡 1 is closed for every shape it named. Each is named beside a
good anchor, `#ifdef` and `org/repo#299` read as prose, and seven of the ten
new or changed cases were red against the checker at `eeadbfeb`. The fix
pass's one divergence from the paste-ready fix, stripping a word's trailing
sentence punctuation, is sound. It never silences a shape the unstripped
rule named except a digits-only locator, which is prose by design, and a
mutation that removes it turns the directive case red.

The class is still open at both edges of the new boundary, which is what
§12 predicts for a rule written as a list of shapes. Three findings follow,
all in `refused_coordinate` and `PATH_HASH_RE`. Both units are the run's
own, since round 1's fixes created the first and round 2's the second.
Ownership would ordinarily make these the branch's to fix. But the
reopening bound ended this run, not the round cap, and a record at that
bound commissions nothing (`docs/review-chain-spec.md` §*The cap bounds
rounds, and not the fixes of the round it stopped*). So each is reported
with a deferral candidate and not as a fix to commission.

1. **A coordinate goes silent (🟡 1).** A file name with no dot takes only a
   letter after its `#`. A path takes anything but digits.
2. **Prose is refused (🟡 2).** An issue number glued to a character the
   strip list does not hold exits 2: `'s`, an em dash, a curly quote, a
   Korean particle, and the `](` of a markdown link whose URL was blanked.
3. **Prose is refused (🟡 3).** `PATH_HASH_RE` takes a hex run of any length.
   A dotted package name at a one-digit version, or an address whose host
   is hex letters, reads as a path followed by a hash.

No finding loses a record or crashes. Each fails in one of two ways. A
coordinate the rule should name reads as covered, which is the silence #299
exists to end, but only in a shape narrower than any of round 2's. Or a
prose cell turns the run red with a named text and a remedy, so a person
sees it and can reword it.

## 🟡 1 — a file name with no dot takes only a letter after its `#`

`skills/evidence-check/scripts/evidence_check.py:1627`. The branch that
judges a dotless file name, `head[-1:].isalnum() and tail[:1].isalpha()`,
names `Makefile#build` and nothing else a locator can open with. The path
branch above it takes any locator that is not digits only, and the
path-less branch below it takes `"` and `<`. So a file name with no dot,
glued to a quoted line, to `<module>` or to a name opening with `_`, is
silent beside a good anchor and alone. · NAME NOT IN TREE

**What is wrong (executed).** At `b43d65cb`, `malformed_rows` on
`` `Makefile#"all: build"` ``, `` `Makefile#<module>` `` and
`` `Makefile#_private` `` returns nothing, beside a good anchor and alone. · NAME NOT IN TREE

**Why it matters.** It is the class round 2's 🟡 1 named: a coordinate
somebody wrote that the patterns refused, silent beside a good anchor, so the
row reads as covered. `overview.md`'s *Rule (a)'s reach* row states the rule
as *a path or a file name with a `#` attached … and a locator that is not
digits only*. For a file name that sentence is not what the code does. The
new case's docstring says *a file name with no dot glued to a name*, which is
accurate and is exactly where the code stops.

**What the fix leaves out.** A dotless file name glued to a digit
(`Makefile#1x`) stays prose. Admitting a digit would refuse `F#4.7`, and a
language name with a version is the likelier text.

## 🟡 2 — an issue number glued to anything but ASCII closing punctuation is refused

`skills/evidence-check/scripts/evidence_check.py:1622-1624`. The fix pass
strips `.,;:!?)]` from the end of each word and then asks whether the
locator is digits only. Only the ASCII closers on that list reach the digits
test. Everything else a sentence can glue after an issue number makes the
locator not-digits, and the path branch then refuses it.

**What is wrong (executed).** At `b43d65cb`, beside a good anchor and alone,
each of these is named `MALFORMED` and the run exits 2:

| Text | Why it is prose |
|---|---|
| `org/repo#299's` | a possessive |
| `org/repo#299—see` | an em dash, the dash this repository's prose uses |
| `“org/repo#299”` | curly quotes |
| `org/repo#299에서` | a Korean particle, glued as Korean always glues it; `seal/config.md` has a `Record language` row for exactly this |
| `[org/repo#299](https://example.com/org/repo/issues/299)` | a markdown link; `URL_RE` blanks the URL and leaves `[org/repo#299](` |

`[#299](…)`, `(#299)` and `` `org/repo#299`의 `` are prose already, because
no path precedes the `#` or the span ends before the particle.

**Why it matters.** The divergence the fix pass made is the right idea, but
it is a list. A cell that cites a good anchor and names its issue in any of
these forms turns an installing repository's run red on prose. Round 2
counted `#ifdef` in that category.

**The fix.** Judge the issue number by its own shape, not by what follows it:
a digit run that no ASCII word character continues. That subsumes the strip
list for the `#` half and admits the five shapes above. It keeps
`src/service.py#1x` a coordinate, because `x` continues the digit run.

**What the fix leaves out.** `docs/a.md#1장`, a digit-opening locator
continued by a non-ASCII letter, becomes prose. It is the same trade the
strip already makes for `src/a.py#12`, and a Korean particle after an issue
number is the likelier text. The strip stays, because the `@` half still
needs it (`src/a.py@abcdef12.`).

## 🟡 3 — `PATH_HASH_RE` takes a hex run of any length

`skills/evidence-check/scripts/evidence_check.py:1610`. `[0-9a-f]+(?![\w.])`
matches one hex digit. Any dotted word followed by `@` and a short hex run
reads as a path followed by a hash.

**What is wrong (executed).** At `b43d65cb`, beside a good anchor and alone,
`chart.js@4`, `` `vue.js@3` `` and `jane.doe@beef` are each named
`MALFORMED` and the run exits 2. The first two are package pins, `@` read as
a version separator the way npm writes one. The third is an address whose
host happens to be hex letters.

**Why it matters.** It is the `@` twin of 🟡 2. `ANCHOR_RE` accepts a hash of
6 to 12 hex characters, and the remedy tells a writer to put `@00000000`, so
nothing shorter than six is a hash anybody was told to write.

**The fix.** Require at least six hex characters, the minimum `ANCHOR_RE`
takes. No upper bound, so a full 40-character commit SHA pasted after a path
is still named.

**What the fix leaves out.** `src/a.py@abc`, a path followed by a
three-character hex run and no anchor, goes silent. `src/a.py#f@abc` is still
named by the both-marks rule. Two shapes stay refused under the fix and are
not claimed as prose here, because they are genuinely ambiguous with a
coordinate: `org/repo@abcdef12` (GitHub's commit autolink, and also
`path@hash`) and a schemeless `example.com/page#section`.

## Also read, not counted in Needs a fix

- **The both-marks rule reads a whole span.** A code span quoting a decorated
  line with a comment, such as `@lru_cache  # memoized`, or `x = 1  # see
  @jane`, holds both marks and is named. This predates round 2's fix: the
  line `if "#" in s and "@" in s` is unchanged from `eeadbfeb`, and the
  build's rule refused any span holding one mark. It fails loudly and its
  reach is narrow. Recorded as an observation rather than a numbered
  finding. The orchestrator may fold it into the issue that 🟡 1–3 go to. · NAME NOT IN TREE
- **The fix range's own survivor sweep names one place, and it is not a
  survivor.** `survivor-check --range eeadbfeb..c8218c81` with the work
  item's exemptions exits 1 on `seal/releases/0.13.0.md:10`. That row shares
  only the phrase *a span holding* with the removed `overview.md` bullet: it
  is 0.13.0's S3 row about `settle`'s segment rule, and the shared phrase
  comes from its note about a lone closing delimiter. The branch sweep, the
  one the orchestrator ran, exits 0 with every survivor excused.

## Regression tests to plant

Destination: `tests/test_a_row_points_by_content.py`, after
`test_a_directive_or_a_string_holding_a_hash_is_prose`. Both are fenced
under `## Paste-ready fixes`. They were planted in the clone and run. At
`b43d65cb` all 11 parameters failed. With the three fixes applied, all 11
passed.

## Facts for the evidence ledger

None new. The rows this work item's fragment already carries for
`refused_coordinate` will drift when the deferred fix edits it, and are
re-read there.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a file name with no dot, glued to a quoted line, `<module>` or a `_` name, is silent beside a good anchor; the dotless branch takes only a letter | `skills/evidence-check/scripts/evidence_check.py:1627` | deferred new issue | Executed: three shapes return nothing at b43d65cb; three planted cases red there and green with the fix below. Inside `refused_coordinate`, which round 2's fixes rewrote. The run is capped, so it goes to a new issue the orchestrator files · NAME NOT IN TREE |
| 🟡 2 | an issue number glued to a possessive, an em dash, a curly quote, a Korean particle or a link's `](` exits 2; the punctuation strip is ASCII closers only | `skills/evidence-check/scripts/evidence_check.py:1622-1624` | deferred new issue | Executed: five prose shapes named MALFORMED at b43d65cb, beside a good anchor and alone; five planted cases red there and green with the fix below |
| 🟡 3 | `PATH_HASH_RE` takes one hex digit, so `chart.js@4`, `vue.js@3` and an address with a hex host exit 2 | `skills/evidence-check/scripts/evidence_check.py:1610` | deferred new issue | Executed: three prose shapes named MALFORMED at b43d65cb; three planted cases red there and green with the fix below. A unit round 2's fixes created |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1, 🟡 2, 🟡 3 — rule (a)'s boundary in `refused_coordinate` and `PATH_HASH_RE`: a dotless file name's locator, an issue number glued to non-ASCII-punctuation text, a one-digit hex run after a dotted word. One unit, one issue, the paste-ready fixes below | a new issue the orchestrator files, labelled `evidence-check` and `from-review` | the orchestrator files it; the repository owner schedules it |

## Paste-ready fixes

### 🟡 1, 🟡 2, 🟡 3

Replaces `PATH_HASH_RE` and the `#` half of the loop in `refused_coordinate`, `skills/evidence-check/scripts/evidence_check.py:1608-1630`:

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

### The cases for 🟡 1–3

Destination `tests/test_a_row_points_by_content.py`, after `test_a_directive_or_a_string_holding_a_hash_is_prose`. In the clone they were run with a dotted package name ending in `.io` where `chart.js@4` stands below. That is the same shape, a dotted name and a one-digit version, and the identifiers test refuses a `.io` host in a tracked file. `chart.js@4` was probed separately with `malformed_rows` at b43d65cb and is named.

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

Needs a fix: yes — findings 1, 2 and 3 (rule (a)'s boundary: a dotless file name's quoted, `<module>` or `_` locator is silent, and an issue number glued to non-ASCII punctuation or a one-digit version after a dotted word exits 2), each deferred to a new issue because the run is capped
Loses a record or crashes: no

## Proof block

Files opened this round:

- `skills/evidence-check/scripts/evidence_check.py` (lines 60–90, 1590–1760; `ANCHOR_RE` and `resolve_unit` compared across three commits)
- `tests/test_a_row_points_by_content.py` (the `run` helper, the fix range's hunks, and the non-ASCII parameters)
- `tests/test_a_rider_reaches_its_file.py:181`
- `tests/test_no_real_identifiers.py` (its host pattern)
- `seal/releases/0.13.0.md:10`
- `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/rounds/round-2.md`, `rounds/round-2-report.md`, `overview.md` (lines 55–72, and the fix range's hunks), `survivors.md` (the fix range's hunk)
- `bin/test`
- PR #606's check list and the `release` job's failed log
