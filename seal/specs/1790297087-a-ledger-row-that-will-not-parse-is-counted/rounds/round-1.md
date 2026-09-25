# 1790297087-a-ledger-row-that-will-not-parse-is-counted — review round 1

| Field | Value |
|---|---|
| Target SHA | 7b14b1fb8843bb1637ecf30a7104185b30900157 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 606 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 1 (rule (a) refuses prose in a code span and misses a coordinate outside one) and finding 2 (a quoted locator with no hash is told to escape a quote) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790297087 reviews the build at 7b14b1fb against spec.md and plan.md (frame 7c912915 and 5f3c5654, approved 0abfb371). It covers the MALFORMED verdict for a ledger coordinate that does not parse (#299), the claim that #322 was already fixed, the seven ledger rows corrected or removed, and the commit advisor's new block. The classes are every cell shape the MALFORMED rule refuses wrongly or lets through, every remedy it prints, and every exit path.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Rule (a) refuses a code span holding one mark (`` `#299` ``, `` `@cache` ``, `` `ops@example.com` `` beside a good anchor), which exits 2 on prose. It also lets through a coordinate outside backticks that has one mark (`src/service.py#Box`, `b.py#g>h`), which is #299's silence | `skills/evidence-check/scripts/evidence_check.py:1682-1685` | open | Executed probe in the clone. The fix below keeps 184 cases green, turns three probe cases from red to green, and the tree still reads 0 malformed |
| 🟡 2 | `BARE_QUOTE_RE`'s negative lookahead matches at end of text, so a quoted locator with no hash (`a.py#"line"`, `a.py#f>"g"`) is told to escape a bare quote | `skills/evidence-check/scripts/evidence_check.py:1603` | open | Executed: three shapes, each given the bare-quote remedy. §14: the remedy line is what a person acts on |
| ⬜ 3 | The advisor header says *rows whose coordinate does not parse*, but it counts texts, and a rule-(b) row has no coordinate. The closing line repeats the per-row remedy and prescribes `@00000000` for a bare-quote row whose hash is right | `hooks/evidence-advisor.py:184-194` | open | Read. The verdicts printed are right |
| ⬜ 4 | The repaired `SEPARATORS` quoted-line coordinate resolves to 347-807, so any module-level edit in `chain_check.py` drifts it. By name it resolves to 547 | `seal/ledger.md:76` | open | Executed: both resolutions. The claim holds either way |
| ❓ | Whether a claim row with an empty `Code grounds` cell should stay silent. Rule (b) requires a non-empty cell as `spec.md` §In 1 (b) says, and 0 such rows exist in this tree | `skills/evidence-check/scripts/evidence_check.py:1690` | ❓ out of verified scope | A product question behind the spec's wording, possibly there to spare group-label rows. Answerer: the repository owner |
| 🟢 | The five live rows and the two Notes coordinates parse and resolve, and each claim holds against its code | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.12.0.md` | confirmed | Executed: each reads `OK`. The code is read in the table above. `claude_block.py --check` exits 0 |
| 🟢 | The removed rider-stamp row's claim was false | `tests/test_a_rider_reaches_its_file.py:181`, `:204` | confirmed | A stamp names an anchor and a hash since #239. The SHA form survives only as `OLD_STAMP`, and a case refuses it |
| 🟢 | `ANCHOR_RE` and `resolve_unit` are unchanged, and work item B is unaffected | `skills/evidence-check/scripts/evidence_check.py:72-77` | confirmed | The diff touches only the comment above `ANCHOR_RE`. The `resolve_unit@c6839923` row reads `OK`, and B's branch cites and edits nothing in the file |
| 🟢 | Exit codes: `MALFORMED` is 2 with and without `--strict`, and `--reverify` returns 1 when it leaves one | `skills/evidence-check/scripts/evidence_check.py:2700-2701`, `:2050` | confirmed | Read. The cases in the lenient-run file and `test_reverify_names_a_malformed_row_and_leaves_it` passed in my run |
| 🟢 | #322 is already fixed | `tests/test_a_row_points_by_content.py:827` | confirmed | An `r"""` docstring since `97e29b7a`. 176 files compile under `-W error` with 0 errors on 3.13.5 |

## Paste-ready fixes

```python
# A quoted locator closed by its second `"` and then followed by something
# other than the `>` or `@` that must come next: the quote inside it was bare.
# At the end of the text the hash is what is missing, not a quote.
BARE_QUOTE_RE = re.compile(r'[#>]"[^"\n]*"(?=[^>@])')
# A leftover is a coordinate somebody wrote, not prose, when it holds both
# marks, or a `#` that opens a locator: a name, a quoted line, `<module>`.
# `#299` is an issue number and `@cache` a decorator, in a span or out of one.
LOCATOR_OPEN_RE = re.compile(r'#[A-Za-z_"<]')


def refused_coordinate(s):
    """True where S, left over after both patterns, is a coordinate."""
    if "://" in s:
        return False
    return ("#" in s and "@" in s) or bool(LOCATOR_OPEN_RE.search(s))
```
```python
        spans = [m.group(2).strip() for m in CODE_SPAN_RE.finditer(left)]
        words = CODE_SPAN_RE.sub(" ", left).split()
        refused = [s for s in spans + words if refused_coordinate(s)]
```
```python
    - a coordinate the patterns refused: what is left of the cell once every
      `ANCHOR_RE` and `OLD_COORD_RE` match is blanked still holds a span or a
      word that holds both marks or a `#` opening a locator. An issue number
      `#299` and a decorator `@cache` are prose, in a span or out of one;
```
```python
def test_prose_marks_beside_a_good_anchor_are_not_refused(repo):
    """An issue number, a decorator and an address in a code span are prose,
    exactly as `(#299)` outside one is; refusing them exits 2 on prose."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text()).group(0)
    ledger.write_text(
        f"| A | {good} (`#299`), the `@cache` decorator, owner `ops@example.com` |\n"
    )
    r = run(["."], str(repo))
    assert "0 old-format · 0 malformed" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout


def test_an_unticked_coordinate_with_no_hash_is_named(repo):
    """The same text row A of the span case names in backticks."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text()).group(0)
    ledger.write_text(f"| A | {good}, src/service.py#Box |\n")
    r = run(["."], str(repo))
    assert "MALFORMED src/service.py#Box  " in r.stdout, r.stdout


def test_a_quoted_locator_with_no_hash_is_not_told_about_a_bare_quote(repo):
    """The hash is what is missing; the line must say so."""
    (repo / "seal" / "ledger" / "f.md").write_text(
        '| A | `src/service.py#"def handler"` |\n'
    )
    r = run(["."], str(repo))
    assert "MALFORMED" in r.stdout and "bare" not in r.stdout, r.stdout
    assert "@00000000" in r.stdout, r.stdout
```

## Executed probes

| What was run | Result |
|---|---|
| `evidence_check.py --strict .` at `7b14b1fb` | `total: 2249 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0 |
| `malformed_rows` over `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` as at `ca2afdb9` | the five coordinates `spec.md` lists and no others |
| `check_text` on the seven repaired coordinates and the fragment's two rider rows | all `OK`, regions as in *The seven rows* |
| `claude_block.py --check` | exit 0 |
| every tracked `.py` compiled under `-W error`, Python 3.13.5 | 176 files, 0 errors |
| `malformed_rows` on 20 single-cell shapes beside or without a good anchor | `` `#299` ``, `` `@cache` ``, `` `ops@example.com` `` refused beside a good anchor. `b.py#g`, `b.py@abcdef12` and `b.py#g>h` outside backticks not refused. `(#299)` outside backticks not refused |
| `malformed_remedy` on quoted locators with no hash | `a.py#"line"`, `a.py#f>"g"`, `a.py#"line">"claim"` and `#"line"` all get the bare-quote remedy |
| Leftover marks in every Code grounds cell of this tree's ledgers | none in either shape |
| Claim rows with an empty Code grounds cell in this tree | 0 of 806 rows read |
| `chain_check.py` `SEPARATORS` by name and by quoted line | `547-547` and `347-807` |
| `bin/test` on `test_a_row_points_by_content.py`, `test_evidence_check.py`, `test_the_lenient_run_says_what_the_broad_gate_will_say.py` and `test_dispatch.py` | 181 passed, exit 0 |
| The same four modules plus three probe cases, with findings 1 and 2's fix applied | 184 passed, exit 0 |
| The three probe cases without the fix | 3 failed, exit 1 |
| `evidence_check.py --strict .` with the fix applied | 0 malformed. 1 drifted, the edited unit itself |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and it comes due when the rounds leave nothing open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
