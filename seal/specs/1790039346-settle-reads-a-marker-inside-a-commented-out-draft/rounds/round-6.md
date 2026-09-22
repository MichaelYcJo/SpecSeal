# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 6

| Field | Value |
|---|---|
| Target SHA | 1eb0ef0767a49b8d7ca0942b6178226f0334788e |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | not yet |
| Fixes checked by | round-7 |
| Fix range | `16a56bc871edff394f430dc8caa37670e1639007..16a56bc871edff394f430dc8caa37670e1639007`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1 to 5, and all five were fixed on this branch rather than filed. The run is capped, so no round reads these fixes; what stands in place of a reader is the orchestrator's own re-derivation and the sealer's broad gate. **Corrected in place 2026-09-22**: this row first read that each was a `deferred #491` candidate, and #491 is narrowed to what is left. |
| Loses a record or crashes | yes — finding 1, a work item's whole SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway git repository at the target SHA. |

- [x] Pass

## What this round was asked

The verifying round, against the diff of round 5's fixes — `2aade426..16a56bc8`,
three commits — rather than the branch. Round 5's record read `Fixes checked by:
nobody`, which `chain_check` refuses at a ready pull request, and closing that is
the job. The round was told what it cost: a round that opens nothing needing a
fix does not consume the cap, and one that opens something ends the run capped.

What it reviewed is the fifth structure rather than a sixth patch. Rounds 1–4
failed because the span pass did not know the comment state; round 5 failed
because its lookahead did not know markdown's block structure. Round 5's own
paste-ready patch — a wider boundary list — was deliberately not applied,
because a boundary list is a guess at a block model and the guess is the class.
What landed computes both readings of a line and parks it where they disagree.

The round was asked to judge that rule as code on six shapes the five rounds
did not reach; to judge the boundary list in its narrower role, now that it
decides only how far the crossing reading looks; to read the rewritten oracle
as an independent implementation, because round 5 found the previous one
borrowing the scan's own constants; and to derive the mutation mapping for
eight new units itself.

Handed over: three rounds reporting different corpus figures for one file, with
the orchestrator's own re-derivation; the record bookkeeping a second time,
where removing units refused twenty-four lines and broke two ledger rows; four
`spec.md` lines the orchestrator settled; and the standing question of which of
the fix pass's claims rest on its own execution alone, this being the last
chance to check that the memo says so.

The broad gate was withheld — the sealer's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `FENCE_RE` accepts any indentation, so a four-space-indented delimiter opens a phantom fence, inverts the fence state for the rest of the file, and a marker quoted inside a real fenced example reads live — `settle --retire` removes the work item's directory at exit 0 | `skills/verify/scripts/unverified_check.py#FENCE_RE` | fixed | `44c4dded` — the fence bound and the oracle's bound move together; bounding the reader alone makes the shipped oracle call the corrected reader unsafe. Zero lines move across all 1,460 `.md` files, re-derived |
| 2 | 🟡 The oracle's block rule and fence rule are the reader's own, so the fuzz cannot report finding 1's class and goes red when the reader is corrected — round 5's finding 2, not closed | `tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules` | fixed | `44c4dded` — same commit. The false *richer on purpose* sentence and the unconditionally-true `#` guard went with it |
| 3 | 🟡 `_paragraph_ends_at`'s docstring states the justification the fix pass says its own fuzz disproved, without qualification, as the design's whole safety argument | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | fixed | `44c4dded` — the docstring says *cheap, not safe*, with the reason |
| 4 | 🟡 `_paragraph_ends_at` stops where markdown does not — an ordered marker not starting with 1, `#` with no space, seven hashes, more than nine digits — and an over-stop shortens the crossing reading's reach, which is the direction that goes live | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | fixed | `44c4dded` — judged before applying: liveness moves on six lines, all under `seal/specs/`, five toward parking. The `|` stop stays |` stop is left alone — it is a measured over-stop and removing it moves the corpus |
| 5 | 🟡 The corpus floor case keys a dictionary on the marker line, so 94 occurrences collapse to 83 and only the last state of each survives | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | fixed | `44c4dded` — counted by occurrence; a mutation parking a duplicated marker's first occurrence reddens it |
| ⬜ 6 | `spec.md` G3 grounds the gate change on the oracle being derived from the format rather than from the scan, which finding 2 disproves | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Goals* G3 | fixed | `c57e5b2a` — the orchestrator's |
| ⬜ 7 | `spec.md` A6's note says the replacement acceptance asserts agreement, and G3 four rows above says agreement would forbid the design | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | fixed | `c57e5b2a` — the orchestrator's |
| ⬜ 8 | `overview.md` §*Not verified* names the incomplete-block-list risk correctly and then names the safety fuzz as what watches it | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | fixed | `44c4dded` — the row names the mutations run before the watcher was trusted, and what is still unwatched |
| ⬜ 9 | `overview.md` §*Not verified* row 3 describes an exit 2 from the records arm that no longer happens, and names a `spec.md:30` that now holds a different row | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | fixed | `44c4dded` — closed with what closed it |
| ⬜ | The width rule in `_partner_ahead` has exactly one guard, and it is the fuzz case finding 2 is about | `skills/verify/scripts/unverified_check.py#_partner_ahead` | confirmed | Executed. Ignoring run width reddens `test_the_scan_never_reads_live_what_the_format_parks` and nothing else, 1 failed of 191. The guard does hold for that mutation; named so that fixing finding 2 does not lose it |
| 🟢 confirmation | Round 5's ⬜ 4 — the anchor list — is fixed and now matches the fragment | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Data & interfaces* | confirmed | Read against the fragment's anchor column: `_liveness`, `_paragraph_ends_at`, `_partner_ahead`, `live_lines`, `folded_items`, `coordinates`, `main` twice, `OPENER` and 15 cases |
| 🟢 confirmation | Round 5's ⬜ 5 — A6 — is fixed and the retirement renders | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | confirmed | Read. **RETIRED** is in the first cell, so a rendered view no longer shows a live acceptance criterion with its note invisible |
| 🟢 confirmation | The corpus figures are 761 / 94 / 83 for `seal/ledger.md`, the three named markers are live at 767, 992 and 1619, and 903 is the eleven-file total | `seal/ledger.md` | confirmed | Re-derived by execution at this SHA rather than carried. The eleven-file corpus gives 903 / 94 / 83; round 5's 102 / 85 reproduces on neither set |
| 🟢 confirmation | The marker audit holds: no compound name the tree lacks reaches an unmarked claim line, in either live work item | `seal/specs/` | confirmed | Re-derived over every `.md` file `record_files` reads, through `claim_lines` and `compound` rather than by eye. 17 names silenced here, 9 in the tree, 8 absent; `check_records` is silenced and read on no unmarked line in this work item, which is noise rather than a hole. `bin/evidence-check --strict .` at exit 0 agrees |
| 🟢 confirmation | Every one of the eight new units has a mutation that reddens it, and the two-reading AND is load-bearing on both sides | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed, six mutations against both modules in a clone at this SHA; baseline 191 passed exit 0, read with `echo $?` and not through a pipe. The mapping is in the table above |
| 🟢 confirmation | The AND cannot be broken from the span side on the shapes this round was asked to try | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Read and executed. A partner in the next paragraph, three runs on a line, a run reaching across a fence, a lone backtick line, a run on the last line, a marker beside an unclosed run — each answers the way the docstring's table says. The structural reason is that a marker line opens an HTML block in CommonMark 4.6 and so always ends the paragraph above it |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports five modules at 406 passed exit 0, `evidence_check.py --strict .` at exit 0 and `survivor-check` at exit 0, all at this SHA; I re-ran `bin/evidence-check --strict .` and the two affected modules and nothing else. The caller answers it |

## Paste-ready fixes

```python
# A run of backticks, and a fence opener. `live_lines` needs both as it
# scans; `blank_fences` keeps its own copy of the fence pattern because it
# serves the other gates and this scan may not move it.
#
# **Three spaces, not `\s*`.** CommonMark 4.5 bounds an opening fence to three
# spaces of indentation; four is an indented code block, or a lazy
# continuation line inside an open paragraph. Reading one as a delimiter does
# not merely park lines — it INVERTS the fence state for the rest of the file,
# so a real fenced block's content reads live and its delimiters read as
# content, and a fold marker quoted inside a fenced example becomes a fold
# record. The constant above names `skills/settle/SKILL.md` §2 as the document
# that shows the marker inside a fence with a real released id, which is the
# quotation this would read (round 6, finding 1; executed on a throwaway git
# repository, `settle --retire` at exit 0 with the directory removed).
# Measured 2026-09-22: bounding it moves 0 lines in every `.md` file in this
# repository and the eleven-file corpus stays at 903 not-live, 94 marker
# occurrences and 83 ids.
BACKTICKS = re.compile(r"`+")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
```
```python
    def block_ends_at(line):
        indent = len(line) - len(line.lstrip(" "))
        s = line.strip()
        if not s:
            return True
        if s.startswith("|") or s.startswith(">"):
            return True
        if indent <= 3 and s.startswith("#"):
            # CommonMark 4.2: one to six hashes, then a space, a tab or the
            # end of the line. The guard this replaces read
            # `s.lstrip("#").startswith((" ", ""))`, and `str.startswith("")`
            # is true of every string, so it asserted nothing.
            n = len(s) - len(s.lstrip("#"))
            if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
                return True
        if indent <= 3 and len(s) >= 3 and s[0] in "`~" and s[:3] == s[0] * 3:
            return True
        if len(s) >= 3 and s[0] in "*-_" and set(s.replace(" ", "")) == {s[0]}:
            return True
        if s[:2] in ("- ", "* ", "+ "):
            return True
        head = s.split(".", 1)[0]
        return head.isdigit() and s[len(head) : len(head) + 2] == ". "

    def fence_of(line):
        # CommonMark 4.5 bounds an opening fence to three spaces. Stripping
        # the line first was the one rule this reading still took from
        # `live_lines`, and while it did, this case agreed with the scan on
        # the shape that removed a directory (round 6, finding 2).
        if len(line) - len(line.lstrip(" ")) > 3:
            return None
        s = line.strip()
        if len(s) < 3 or s[0] not in "`~":
            return None
        n = runs(s, 0) if s[0] == "`" else len(s) - len(s.lstrip("~"))
        return s[0] * n if n >= 3 else None
```
```python
    - **Where a block ends** (CommonMark 4.1, 4.2, 4.3, 4.5, 4.8, 5.1, 5.2 and
      GFM 4.10): a blank line, a thematic break, an ATX heading, a fence
      delimiter, a block quote marker, a list item marker, or a table row.
      **A richer list is a WEAKER case, not a safer one**, and the sentence
      here used to claim the opposite. Every extra stop shortens
      `partner_in_this_block`, which makes this reading see fewer spans, which
      makes it call MORE lines live — and the only violation this case can
      report is the scan live where this reading parks. So each rule is the
      format's rule and no other, and the two indentation bounds above are
      where that stopped being true (round 6, finding 2).
```
```python
        # Round 6. A fence delimiter indented four spaces is an indented code
        # block, not a delimiter. One of them inverts the fence state for the
        # rest of the file, and the marker quoted inside the real fenced
        # example below becomes a fold record — `settle --retire` removing the
        # work item's directory at exit 0 with nothing having absorbed it.
        (
            "a marker in a fenced example under an indented delimiter",
            "A fence opens with\n\n    ```python\n\nand closes with a run at "
            "least as long.\n\n```markdown\n<!-- specs/s-8 -->\n```\n",
            set(),
        ),
```
```python
    **Being incomplete here is CHEAP, not safe, and the difference is a line
    the format parks.** This bounds one half of a disagreement rather than
    the answer, and a missing stop USUALLY only lets `_partner_ahead` reach
    further, which makes the crossing reading believe in a span the format
    would not, which parks a line — a fold reported as a deletion, at exit 1,
    which a person sees. Usually, not always: reaching further also changes
    which runs pair with which, and a run that consumes a partner early
    leaves a later run with none, so a later line goes live rather than
    parked. Measured 2026-09-22 with the setext underline (CommonMark 4.3)
    missing, which it still is: `["text `", "===", "text `", "plain prose",
    "text `"]` reads its last two lines live and the format parks them. The
    rule round 5 removed decided the answer by itself, so its missing stops
    removed a directory; this one only leans, but it leans in both
    directions. Add a stop when the format has one.
```
```python
    s = line.strip()
    if not s:
        return True
    # `|` is a deliberate over-stop — GFM parses a table row's cells
    # independently and the measurement above is what it buys. `>` is the
    # format's own rule (CommonMark 5.1).
    if s.startswith(("|", ">")):
        return True
    # CommonMark 4.2: one to six hashes, then a space, a tab or end of line.
    # `s.startswith("#")` alone stops on `#hello` and on `####### seven`,
    # which are paragraph text — and on the issue references this repository
    # writes constantly, 944 lines of them (round 6, finding 4).
    if s.startswith("#"):
        n = len(s) - len(s.lstrip("#"))
        if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
            return True
    if FENCE_RE.match(line):
        return True
    if s[0] in "*-_" and len(s) >= 3 and set(s.replace(" ", "")) == {s[0]}:
        return True
    if s[:2] in ("- ", "* ", "+ "):
        return True
    # CommonMark 5.3: an ordered list interrupts a paragraph only when it
    # starts with 1. `3. an item` inside a paragraph is paragraph text, and
    # stopping there shortens the crossing reading's reach, which is the
    # direction that goes live.
    return s[:2] in ("1.", "1)") and len(s) > 2 and s[2] in " \t"
```
```python
    ledger = os.path.join(ROOT, "seal", "ledger.md")
    with open(ledger, encoding="utf-8") as f:
        lines = f.read().split("\n")
    # Every OCCURRENCE, not a dictionary keyed on the line. This file carries
    # eleven marker lines twice, so keying on the text kept the last state of
    # each and a regression parking the first of a pair was invisible to the
    # floor below (round 6, finding 5).
    occurrences = [
        (n, line.strip(), state)
        for n, (line, state) in enumerate(uc.live_lines(lines), 1)
        if line.startswith(uc.OPENER + " specs/")
    ]
    parked = [(n, line) for n, line, state in occurrences if not state]
    assert not parked, parked
    for want in (
        "1788472135-the-run-outlives-its-last-finding",
        "1788613827-a-runs-report-carries-one-comparison-table",
        "1788844127-the-reviewers-report-reaches-the-record-retyped",
    ):
        assert any(f"specs/{want} " in line for _, line, _ in occurrences), want
    assert len(occurrences) >= 90, len(occurrences)
    assert len({line for _, line, _ in occurrences}) >= 80, len(occurrences)
```

## Executed probes

| What was run | Result |
|---|---|
| the two affected modules in a pristine clone at the target SHA | 191 passed, exit 0, read with `echo $?` and not through a pipe |
| the indented-delimiter document through `live_lines` and `comment_scan` | `live_lines` reads the marker live; `comment_scan` answers *began inside* |
| the same document through `folded_items` and `settle --retire` on a throwaway git repository | `{'1700000042-quoted'}`, exit 0, `removed seal/specs/1700000042-quoted/`, directory deleted |
| the real-fenced-example shape — one phantom opener above a genuine fenced block holding a marker | the marker reads live |
| `_paragraph_ends_at` against the oracle's `block_ends_at`, 40,000 generated lines and every `.md` file in the tree | 0 disagreements in both |
| both of finding 1's documents through the scan and the shipped oracle | the oracle returns the scan's verdicts line for line; 0 unsafe lines reported |
| `FENCE_RE` bounded to three spaces, shipped oracle, the same two documents | the oracle reports the corrected reader unsafe on 1 and 6 lines |
| a corrected oracle against the shipped reader, the same two documents | reports the marker line and its neighbours — 1 line and 2 lines |
| a corrected oracle against the bounded reader, the same two documents | 0 unsafe |
| the shipped fuzz generator with each pairing of reader and oracle, 2,000 documents | 0 unsafe in all four; the generator builds no indentation |
| `FENCE_RE` bounded to three spaces, over every `.md` file in the repository | 0 lines change; the eleven-file corpus stays at 903 / 94 / 83 |
| `FENCE_RE` bounded to three spaces, against both modules | 191 passed, exit 0 |
| the setext-underline document with and without the missing stop | shipped rule reads lines 3 and 4 live; with the stop, parked — incompleteness moved the answer toward live |
| the block rule corrected for the four over-stops, over every `.md` file in the repository | the rules disagree on 944 lines; liveness changes on 6 lines in 4 files, all under `seal/specs/` |
| six mutations of `_liveness`, `_paragraph_ends_at` and `_partner_ahead` against both modules | every one red; the mapping is in the confirmations above |
| `seal/ledger.md` through `live_lines` | 2,430 lines, 761 not-live, 94 live marker occurrences, 83 unique ids, the three named markers at 767, 992, 1619, and 11 marker lines appearing twice |
| the eleven-file corpus through `live_lines` | 903 not-live, 94 occurrences, 83 ids |
| the marker audit re-derived through `record_files`, `claim_lines` and `compound` over both live work items | 0 absent names on an unmarked claim line; 17 silenced here, 9 in the tree, 8 absent |
| `bin/evidence-check --strict .` at this SHA | exit 0 — `510 names read · 0 refused · 0 drifted · 0 external`; ledgers `1439 ok · 0 drifted · 0 broken` |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/unverified_check.py#live_lines` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | round 1's 2 — fixed |
| round-1 | `skills/settle/scripts/settle.py#coordinates` | round 1's 3 — answered |
| round-1 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/unverified_check.py` | round 1's 🟢 confirmation — confirmed |
| round-1 | `skills/settle/scripts/settle.py#main` | round 1's 🟢 confirmation — confirmed |
| round-1 | both test modules | round 1's 🟢 confirmation — confirmed |
| round-1 | `tests/test_a_row_points_by_content.py:763` | round 1's ⬜ — confirmed |
| round-2 | both test modules and `skills/verify/scripts/unverified_check.py` | round 2's 🟢 confirmation — confirmed |
| round-2 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/survivors.md` | round 2's ⬜ — confirmed |
| round-2 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-1-report.md:191` | round 2's ⬜ — confirmed |
| round-2 | the repository | round 2's ❓ out of verified scope — not run |
| round-3 | `skills/verify/scripts/unverified_check.py:107-110` | round 3's ⬜ 3 — fixed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | round 3's ⬜ — confirmed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:30` | round 3's 🟢 confirmation — confirmed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Operational impact* | round 3's 🟢 confirmation — confirmed |
| round-4 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | round 4's ⬜ 3 — fixed |
| round-4 | `skills/verify/scripts/unverified_check.py:107-118` | round 4's 🟢 confirmation — fixed |
| round-5 | `skills/verify/scripts/unverified_check.py#is_block_boundary` | round 5's 1 — fixed |
| round-5 | `tests/test_unverified_rows_close.py#a_character_level_reading` | round 5's 2 — fixed |
| round-5 | `skills/verify/scripts/unverified_check.py#comment_scan` | round 5's 3 — fixed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Data & interfaces* | round 5's ⬜ 4 — fixed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | round 5's ⬜ 5 — fixed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md` | round 5's ⬜ — confirmed |
| round-5 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/` | round 5's 🟢 confirmation — confirmed |
| round-5 | the two affected modules | round 5's 🟢 confirmation — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 1 — an indented fence delimiter flips the fence state | #491, `backlog: ledger & checker` | the repository owner |
| 2 — the oracle shares the same laxness, so its case cannot see the class | #491, one fix with 1 | the repository owner |
| 3 — a docstring states unconditionally what round 5's fuzz disproved | #491 | the repository owner |
| 4 — the paragraph reader stops where markdown does not | #491 | the repository owner |
| 5 — the three-marker case folds 94 occurrences into 83 keys | #491 | the repository owner |
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 and confirmed in rounds 4 and 5 | the orchestrator |
