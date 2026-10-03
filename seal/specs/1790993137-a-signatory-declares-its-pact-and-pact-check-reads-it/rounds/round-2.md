# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — review round 2

| Field | Value |
|---|---|
| Target SHA | 2a0243b2cbf6e6a3ceae715facf1a4252a9bcad0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 735 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `652275a07ae4f0b8123ec9787c525278ffdf821f..d9602677221dea95e01197e1b895fb7d4076a657`, 5 commits |
| Contract changes | none |
| New units | SIGNATORY_DELIMITER (depth 1); TABLE_BREAK (depth 1); HEADING_LINE (depth 1); _stops_at (depth 1); WEB (depth 1); MOBILE (depth 1); HEAD (depth 1); CLAUSE (depth 1); ENDS_ABOVE (depth 1); stops_at (depth 1); TABLE_ENDS (depth 1); test_every_way_the_table_ends_is_read_or_refused (depth 1); ENTRY (depth 1); test_every_entry_refusal_reads_after_the_pact (depth 1); test_a_signatory_row_below_a_blank_line_is_refused (depth 1); test_prose_naming_the_pact_is_not_a_citation (depth 1); test_a_pact_name_inside_a_graded_anchors_heading_is_not_a_near_miss (depth 1); test_an_entry_refusal_is_printed_after_the_pact (depth 1) |
| Needs a fix | yes — 🟡 12 (a blank line inside the `Signatory` table drops the signatories below it, exit 0), 🟡 13 (`pact-check` refuses prose naming the pact at exit 2) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round. It targets `2a0243b2` over round 1's fix range `0487fb5b..62726cb9`. It was asked:
- whether each of round 1's fixes holds;
- whether the units the fix pass created are correct: `PACT_MENTION_RE` and its `REFUSED`, the refused Signatory row, `--full-history`, `declared_pacts` as a production reader, the self-listed signatory, the four branch cases and the widened word case;
- whether 🟡 3's reader list holds when checked by property;
- whether `PACT_MENTION_RE` now refuses text it should not;
- whether the ledger corrections and re-reads hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 12 | A blank line inside the pact's `Signatory` table ends the walk, and a signatory written below it is never read: `pact-check` prints `1 of 1 signatory read`, exit 0 | `hooks/config.py:851` | **fixed** `5b45e4c4` | fixed at 5b45e4c4; executed: a row below a blank line was unread at exit 0; above it, the same row read `NOT FOUND`, exit 1; the stray-line fix covers only a line that starts with `\|` |
| 🟡 13 | `PACT_MENTION_RE` takes `pact:<name>` followed by anything, so prose naming the pact, a code span holding it, and the placeholder form are each refused at exit 2 as a pact anchor that does not parse | `skills/evidence-check/scripts/pact_check.py:104` | **fixed** `7090a9f4` | fixed at 7090a9f4; executed: three prose shapes beside a valid citation each exit 2; `pact:orders-api.` ending a sentence exits 0; the three malformed shapes stay refused under the fix |
| ⬜ 14 | Three refusals from `remote_entries` print after *the pact* as *the pact the `Signatory` table holds an empty row*, *the pact `<url>` holds a space*, *the pact `<a>` and `<b>` are one repository*, in `pact-check` and `chain-check` | `hooks/config.py:856` | **fixed** `64c5704c` | fixed at 64c5704c; executed: each printed as quoted; the fix commit says both of the table's refusals read after *the pact*, and it changed two of five |
| ⬜ 15 | The word case's printed texts leave out the refusal sentences `pact-check` and `chain-check` print from `hooks/config.py` | `tests/test_one_word_one_meaning.py:588` | **fixed** `8705cdd4` | fixed at 8705cdd4; read: `PACT_PRINTED` names `pact_check.py` and two `chain_check.py` units; the three config units are clean today |
| ⬜ 16 | P9's Code grounds cite one of three `UNREADABLE` cases and not the pact-level stray case, while its note says each branch has a case | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:9` | answered | corrected at `d9602677`; read: a correction to the run's paperwork, not a fix |
| ⬜ 17 | `round-1.md`'s 🟡 3 and ⬜ 5 Grounds read *fixed at bf035a2f — ;* and *fixed at 1e1bb977 — `62726cb9`*, the close's splice of the fixes table | `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-1.md:36` | answered | corrected at `652275a0`; read: a correction to the run's paperwork; the generator's join, not this branch's code; the orchestrator answers it |
| 🟢 | round 1's finding 1, re-read: HEAD's history is read with `--full-history`, so a clause a merge did not keep is `SUPERSEDED` | `skills/evidence-check/scripts/pact_check.py:254` | verified | executed: flag dropped, the merge case red; read: `other()` unchanged in shape, a merge listed carries one parent's text |
| 🟢 | round 1's finding 2, re-read: a `Signatory` line with no closing pipe or a second cell is refused | `hooks/config.py:849` | verified | executed: recording dropped, three ids red; the class has one more line, 🟡 12 |
| 🟢 | round 1's finding 3, re-read: `stated_names` and `stated_coordinates` blank pact anchors first | `skills/evidence-check/scripts/evidence_check.py:2940` | verified | executed: each blanking dropped alone, a case red each time; read: every regex read in the file sorted by what it reads, none missed beyond the limit `PACT_ANCHOR_RE`'s comment names |
| 🟢 | round 1's finding 4, re-read: a malformed anchor naming this pact is refused at exit 2 | `skills/evidence-check/scripts/pact_check.py:476` | verified | executed: the loop disabled, three ids red; the net is wider than an attempt, 🟡 13 |
| 🟢 | round 1's finding 5, re-read: `declared_pacts` is `pact-check`'s reader and answers an unreadable config as None | `hooks/config.py:799` | verified | executed: the old answer restored, two cases red; read: no file still reaches `ONE-SIDED` as before |
| 🟢 | round 1's finding 6, re-read: 0.15.4's MALFORMED claim names three patterns | `seal/releases/0.15.4.md:54` | verified | read: claim corrected in place under a dated note |
| 🟢 | round 1's finding 7, re-read: the re-pointed coordinates | `seal/releases/0.5.0.md:212` | answered | carried the orchestrator's answer; read: round 1's identity probe makes the alias the same unit, so the claim names what it is about |
| 🟢 | round 1's finding 8, re-read: the four branches each have a case pinning the sentence | `tests/test_pact_check.py:446` | verified | read: four cases, sentences pinned; executed: the config case red when broken; the other three reds are the smith's account |
| 🟢 | round 1's finding 9, re-read: a pact listing its own repository is refused in the table's words | `skills/evidence-check/scripts/pact_check.py:402` | verified | executed: the check disabled, the case red |
| 🟢 | round 1's finding 10, re-read: the repeated git calls | `skills/evidence-check/scripts/pact_check.py:195` | answered | carried the orchestrator's answer; read: the cost is local and small |
| 🟢 | round 1's finding 11, re-read: the word case reads five more texts | `tests/test_one_word_one_meaning.py:581` | verified | executed: the module green; read: the five texts are read; `hooks/config.py`'s sentences are not, ⬜ 15 |
| 🟢 | the ledger corrections round 1's fixes owed | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:5` | verified | read: 0.15.4 corrected; 0.9.0 R1 and 0.16.0 P1 re-read and re-hashed; fragment P1, P5, P8 and P9 carry dated notes; executed: `evidence-check --strict` exit 0 |

## Paste-ready fixes

```python
    values, seen_header, stray, ended = [], False, None, False
    for _index, line in unfenced(text.splitlines(), text):
        if not seen_header:
            seen_header = bool(SIGNATORY_HEADER.match(line))
            continue
        if ended:
            # Past the line that ended the table -- a blank one, say -- and
            # before the first clause: a row written here is a signatory the
            # walk never reaches, the same silence as the stray row below
            # (round 2 of #647).
            if line.lstrip().startswith("#"):
                break
            if line.lstrip().startswith("|"):
                stray = (
                    f"has a `Signatory` table that ends above `{line.strip()}`, "
                    "a row the walk never reaches — it and every signatory "
                    "below it would go unread"
                )
                break
            continue
        if CONFIG_SEPARATOR.match(line.strip()) and not values:
            continue
        match = SIGNATORY_ROW.match(line)
        if not match:
            # A table line the walk cannot read -- no closing pipe, or a
            # second cell -- ends the walk, and every signatory written below
            # it would go unread in silence. So it is refused (round 1 of
            # #647, yellow 2).
            if line.lstrip().startswith("|"):
                stray = (
                    f"has a `Signatory` table that stops at `{line.strip()}`, "
                    "which is not a one-cell row closed by `|` — every "
                    "signatory below it would go unread"
                )
                break
            ended = True
            continue
        values.append(unescaped(match.group("value").strip()))
    if not seen_header:
        return [], ["holds no `| Signatory |` table, so it names no signatory"]
    # Each sentence is printed after "the pact " by both callers, so an
    # entry's refusal gets a lead-in that reads after those words.
    signatories, entry_refusals = remote_entries(values, "an empty row", named=False)
    refusals = [
        f"has a `Signatory` entry that will not read: {r}" for r in entry_refusals
    ]
    if stray is not None:
        refusals.append(stray)
    if not values:
        refusals.append("has a `Signatory` table that lists nobody")
    return signatories, refusals
```
```python
#
# **An attempt, not a mention**: the name must be followed by what opens a
# locator or a hash -- `/`, `#`, a quote or `@` -- so prose naming the pact
# (`pact:orders-api,`, a code span holding `pact:orders-api`) is not refused,
# and neither is the form written with its placeholders, `/"<heading path>"`.
# The name is read whole, so `pact:orders-api.` ending a sentence is prose
# and not a near miss.
PACT_MENTION_RE = re.compile(
    r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]*[A-Za-z0-9_-])"
    r"(?![A-Za-z0-9_.-]*[A-Za-z0-9_-])(?!/\"<)(?=[/#\"'@])[^\s`|]*"
)
```
```python
            graded = [m.span() for m in checker.PACT_ANCHOR_RE.finditer(view)]
            for near in PACT_MENTION_RE.finditer(view):
                inside = any(s <= near.start() < e for s, e in graded)
                if near.group("name").lower() != name or inside:
                    continue
```
```python
    # Each sentence is printed after "the pact " by both callers, so an
    # entry's refusal gets a lead-in that reads after those words.
    signatories, entry_refusals = remote_entries(values, "an empty row", named=False)
    refusals = [
        f"has a `Signatory` entry that will not read: {r}" for r in entry_refusals
    ]
```
```python
    (("hooks", "config.py"), "pact_declaration"),
    (("hooks", "config.py"), "remote_entries"),
    (("hooks", "config.py"), "pact_signatories"),
```
```markdown
`tests/test_pact_check.py#test_a_signatory_config_that_will_not_read_is_unreadable@00000000`, `tests/test_pact_check.py#test_an_anchor_file_that_will_not_read_is_unreadable@00000000`, `tests/test_pact_check.py#test_a_signatory_row_the_table_walk_cannot_read_is_exit_2@00000000`
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on six modules: `test_pact_check`, `test_a_signatory_declares_its_pact`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory`, `test_one_word_one_meaning`, `test_a_signatorys_ci_prints_its_pact`, `test_a_record_states_what_the_tree_has` | 179 passed, exit 0 |
| `bin/evidence-check --strict .` at the target | exit 0; 3678 ok; records arm 0 refused |
| `bin/fold-check` at the target | exit 0, 158 statements in 15 documents |
| Seven breaks of round 1's fixes, one at a time, each case run (the table above) | every one red; tree restored after each |
| `pact-check` over a signatory `spec.md` holding each prose shape of 🟡 13 | three exit 2, `See pact:orders-api.` exit 0, other pact and fenced exit 0 |
| `pact-check` over a pact with a blank line inside the `Signatory` table (🟡 12) | `1 of 1 signatory read`, exit 0 |
| `pact-check` over an empty row, a row with a space, and a duplicate row (⬜ 14) | each `REFUSED`, exit 2, with the sentences quoted in ⬜ 14 |
| The paste-ready fixes for 🟡 12, 🟡 13 and ⬜ 14 applied in the clone, with the proposed cases | 6 proposed cases red before the fixes and green after; with the five pact modules, 72 passed, exit 0; clone restored |
| The full suite, the repository-wide lint and the typecheck | not yet — not run in this round; the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/pact_check.py:240` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/config.py:820` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2930` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:437` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/config.py:799` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/releases/0.15.4.md:54` | round 1's ⬜ 6 — answered |
| round-1 | `seal/releases/0.5.0.md:212` | round 1's ⬜ 7 — answered |
| round-1 | `skills/evidence-check/scripts/pact_check.py:393` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:387` | round 1's ⬜ 9 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:195` | round 1's ⬜ 10 — answered |
| round-1 | `tests/test_one_word_one_meaning.py:565` | round 1's ⬜ 11 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1658` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:295` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py:4514` | round 1's 🟢 — confirmed |
| round-1 | `skills/implement/scripts/seal.py:284` | round 1's 🟢 — confirmed |
| round-1 | `skills/config/SKILL.md:31` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-pact.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.13.1.md:65` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
