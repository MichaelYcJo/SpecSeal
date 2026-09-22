# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — review round 3

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Target SHA | 02b2038d3a73c3306a255c856110dea4df1f8999 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 486 |
| Broad gate | fb628ba6 against ad420686 |
| Fixes checked by | no fixes to check |
| Fix range | `02b2038d3a73c3306a255c856110dea4df1f8999..02b2038d3a73c3306a255c856110dea4df1f8999`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1 through 4. None of them is a fix to commission, because the cap is spent: each is a candidate for its own issue, and finding 2 is the one that should carry the measurement about code spans with it. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last round, against the diff of round 2's fixes — `cd4ed9de..80075126`,
two commits. Round 2 was the one reopening the chain allows, so this round
ends the run whatever it finds; what it opens becomes an issue rather than a
fourth fix pass.

Its job was round 2's eight verdicts: for each one recorded as closed, is it
actually closed. Two surfaces were named as where the round earns its keep — a
refactor that landed inside the fix pass, `strip_comments` extracted into
`comment_scan` with two views over one scan, whose untouched callers this round
alone reviews; and a sub-point of finding 6 the pass refused rather than took.
The class to enumerate was every one of the thirteen units round 2's record
names, against the mutation that should turn it red, with the pass's own count
of ten mutations for thirteen units re-derived rather than carried.

Corrections handed over: the four ledger rows re-read in `80075126`, one of
them at a coordinate whose walk moved; two reporting claims the previous pass
withdrew itself; and a near miss it disclosed — a `zip` strictness keyword
that arrived in 3.10 inside a module with no interpreter guard — handed over as
a class to enumerate rather than an instance to confirm.

The broad gate was withheld; it comes due at this round's end.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The opt-out refusal reads the scratch marker with `os.path.exists`, the accessor `hooks/optin.py` documents as measured-wrong, so `settle` and the opt-in module disagree about what a marker is | `skills/settle/scripts/settle.py:614` · `hooks/optin.py:200` | deferred #489 | #489 — The run is capped: round 2 spent the one reopening, and a third fix-closing record is what `chain_check` refuses. Filed into the `release: 0.13.0` milestone so it closes on this release branch before the version ships, not in the backlog. One-word fix, `os.path.exists` → `os.path.isfile`, reintroducing the directory-as-marker defect `hooks/optin.py` names; executed — against a repository with no root and a DIRECTORY of that name, `home_at` answers `""` while `settle` answers *has opted out … Delete that file to turn them back on*, and every clause after the dash is false |
| 🟡 2 | `coordinates` got the fence half of round 2's finding 5 and not the comment half: a marker inside a commented-out draft in `seal/ledger.md` still opens a section | `skills/settle/scripts/settle.py:320` | deferred #489 | #489 — Same ticket and same reason. The comment half of the rule `coordinates` did not get; the ticket carries the measurement that the obvious closure loses three real markers and the one that does not; executed — a scratch ledger with a parked marker attributes `hooks/quoted.py` to the id in the parked block. The naive closure is wrong: applying `opens_outside_a_comment` to today's `seal/ledger.md` loses three real markers at lines 767, 992 and 1619, because a row's anchor quotes an unclosed opener inside a code span |
| 🟡 3 | The fragment half of finding 5's fix is pinned by nothing — reverting it turns no case red | `skills/settle/scripts/settle.py:333` · `tests/test_settle_reads_before_it_removes.py:678` | deferred #489 | #489 — Same ticket. The fragments loop is pinned by nothing — the one of eleven mutations that reddened nothing; executed — mutation M7, the fragment loop back to a whole-file `finditer`: both modules exit 0 with nothing red, where all ten other mutations reddened at least one case |
| 🟡 4 | `test_one_comment_scanner_serves_both_readers` says it pins that the two views come out of one scan; its assertions only ask that they agree, which a duplicated walk also satisfies | `tests/test_unverified_rows_close.py:1482` | deferred #489 | #489 — Same ticket. The single-scan pin asks only that the two views agree, which a duplicated walk satisfies; executed — stubbing `comment_scan` at module level makes both readers answer from the stub, so the single scan is pinnable and is not pinned (NAME NOT IN TREE) |
| 🟢 confirmation | Round 2 finding 1: a marker inside a commented-out draft is no longer a fold record | `skills/verify/scripts/unverified_check.py:697` | confirmed closed | executed — M1 and M2 each redden `test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record` and the comment-shape family |
| 🟢 confirmation | The refactor is behaviour-preserving: `strip_comments` returns what it returned | `skills/verify/scripts/unverified_check.py:182` | confirmed | executed — 1,435 tracked markdown files and 584 token arrangements, zero differing; the eight caller modules 336 passed at exit 0 |
| 🟢 confirmation | Round 2 finding 2: *The fold is complete.* no longer prints over a marked item still on disk, and still prints when it is | `skills/settle/scripts/settle.py:518` | confirmed closed | executed — M4 reddens the first case, M5 reddens the second |
| 🟢 confirmation | Round 2 finding 3: the exit-code list names five states and the skill names the refusal | `skills/settle/scripts/settle.py:60` · `skills/settle/SKILL.md:39` | confirmed closed | executed — M10 reddens `test_the_module_and_the_skill_both_say_local_mode_is_refused` |
| 🟢 confirmation | Round 2 finding 4: the `--released-at` refusal is about the ref and nothing else | `skills/settle/scripts/settle.py:667` | confirmed closed | executed — M9 reddens the case |
| 🟢 confirmation | Round 2 finding 5, for the half it named: a fenced marker in `seal/ledger.md` opens no section | `skills/settle/scripts/settle.py:320` | confirmed closed | executed — M6 reddens `test_a_fenced_marker_in_the_ledger_opens_no_section`. What the fix did not reach is findings 2 and 3 above |
| 🟢 confirmation | Round 2 finding 6, and the sub-point the pass refused rather than took | `skills/settle/scripts/settle.py:497` · `:518` | confirmed closed | executed for the docstring (M11 reddens the pin); read for the refusal — `survey["released"]` is built from `present`, so the term is inert in `candidates`, and `stranded = sorted(marked & present)` is the second reader the pass claimed |
| 🟢 confirmation | Round 2 finding 7: an opted-out repository is told which state it is in | `skills/settle/scripts/settle.py:608` | confirmed closed | executed — M8 reddens the case. The accessor it uses is finding 1 above |
| 🟢 confirmation | Round 2 finding 8: the S1 row says seven | `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3` | confirmed closed | read — the sentence reads *seven fence shapes* and names the six comment shapes beside them |
| 🟢 confirmation | Every one of the thirteen new units reddens under a named mutation, and the row names exactly the thirteen the fix range adds | `tests/test_settle_reads_before_it_removes.py` · `tests/test_unverified_rows_close.py` · `skills/verify/scripts/unverified_check.py` | confirmed | executed — eleven mutations, each applied alone and restored, every substitution asserted to have matched; the mapping is in the probes table |
| 🟢 confirmation | No construct this branch added to the unguarded reader needs a floor the module does not declare | `skills/verify/scripts/unverified_check.py` | confirmed | executed on 3.9.6 — compile, import, the three changed functions, the command over this work item, and `--baseline` over 90 overviews, all exit 0; the other two unguarded scripts the branch changed compile there too |
| 🟢 confirmation | The four ledger rows re-read in `80075126` are true at their new coordinates | `seal/ledger.md:80` · `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md` | confirmed | executed — `evidence-check` 13 ok and 1,402 ok, 0 drifted, 0 broken, exit 0; the `strip_comments` row's claim is what the equivalence measurement establishes |
| ⬜ 5 | The refusal path asks git for the common directory twice: `home_at` resolves it internally and the new arm resolves it again, although `home_at(root, common)` exists for exactly this and says so | `skills/settle/scripts/settle.py:606` · `hooks/optin.py:178` | deferred #489 | #489 — Same ticket, as its ⬜ item: one extra `rev-parse` on an error path where `home_at(root, common)` already takes the value; read — one extra `rev-parse` on an error path only; the parameter is documented with the measurement that created it |
| ⬜ | Round 1 finding 6, deferred to #487 — still the right call, and findings 2 and 4 above both point at it | `skills/settle/scripts/settle.py:218` | deferred #487 | already deferred in round 1 |
| ⬜ | Round 1 finding 9, deferred to #488 | `CLAUDE.md` §*a change writes fragments, never the shared file* | deferred #488 | already deferred in round 1 |
| ❓ scope | The broad gate — the full suite, the repository-wide lint and the typecheck | whole tree | ❓ out of verified scope | §2 gives it to the sealer and the prompt withholds it; the orchestrating session answers. Nothing in this report leaves a fix outstanding that would spend it, so it has come due |

## Paste-ready fixes

```python
        if common and os.path.isfile(os.path.join(common, optin.SCRATCH)):
```
```python
CODE_SPAN = re.compile(r"`+[^`]*`+")


def blank_code_spans(lines):
    """The same lines with inline code spans blanked out, indices intact.

    A ledger row's anchor quotes the text it is anchored to, and that text is
    often a comment -- `seal/ledger.md` carries an anchor holding an opener
    with no closer, and the comment state it opens runs for hundreds of lines.
    Measured 2026-09-22: asking `opens_outside_a_comment` of that file without
    this loses three real section markers, at lines 767, 992 and 1619, and
    calls 787 of its lines not live.
    """
    return [CODE_SPAN.sub(lambda m: " " * len(m.group(0)), line) for line in lines]
```
```python
    out = collections.defaultdict(list)
    reader = load(READER, "specseal_unverified_reader")
    ledger = under(root, LEDGER)
    if os.path.isfile(ledger):
        with open(ledger, encoding="utf-8") as f:
            lines = reader.blank_fences(f.read().split("\n"))
            # A line stops being live two ways, which is what `folded_items`
            # already asks: a fence is a quotation and an enclosing comment is
            # a parked draft. Code spans are blanked first because a row's
            # anchor quotes comment text, and an unclosed opener inside one
            # would park every section below it.
            live = reader.opens_outside_a_comment(reader.blank_code_spans(lines))
            current = None
            for n, line in enumerate(lines):
                if not live[n]:
                    continue
                marker = MARKER_LINE_RE.match(line)
```
```python
def test_a_fenced_coordinate_in_a_fragment_is_not_the_fragments_own(tree):
    """The other half of round 2's finding 5. `coordinates` reads two places
    and the fix changed both; only the ledger half had a case, so reverting
    the fragment loop to a whole-file `finditer` turned nothing red."""
    fragment = tree / "seal" / "ledger" / "1700000001-alpha.md"
    fragment.write_text(
        fragment.read_text(encoding="utf-8")
        + "\nAn example of the convention:\n\n```markdown\n"
        + "| q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n"
        + "```\n",
        encoding="utf-8",
    )
    assert "hooks/quoted.py" not in settle.coordinates(str(tree))["1700000001-alpha"]
```
```python
    # One scan, asked of the code rather than of the two answers agreeing:
    # a second private copy of the walk answers identically and would pass
    # every assertion above. Both readers reach `comment_scan` through the
    # module global, so replacing it is what tells them apart.
    real = uc.comment_scan
    uc.comment_scan = lambda lines: iter([(True, "SENTINEL")])
    try:
        assert uc.strip_comments(lines) == ["SENTINEL"]
        assert uc.opens_outside_a_comment(lines) == [True]
    finally:
        uc.comment_scan = real
```

## Executed probes

| What was run | Result |
|---|---|
| `tests/test_settle_reads_before_it_removes.py` and `tests/test_unverified_rows_close.py` in a `--no-local` clone at the target SHA | `161 passed`, exit 0 read directly — the baseline every mutation below runs against |
| M1 — `folded_items` stops asking whether the line is live | red: `test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record`, `test_every_comment_shape_a_policy_document_can_carry` |
| M2 — `comment_scan` reports the state the line ENDED in | red: 18 cases including `test_one_comment_scanner_serves_both_readers`, `test_readable_would_erase_every_fold_record`, both comment-shape and fence-shape families (NAME NOT IN TREE) |
| M3 — `comment_scan` keeps the text a comment opener swallows | red: `test_one_comment_scanner_serves_both_readers`, `test_readable_would_erase_every_fold_record`, three older comment cases (NAME NOT IN TREE) |
| M4 — the fold-is-complete arm fires on `if marked:` again | red: `test_a_marked_item_still_on_disk_is_not_the_fold_being_complete`, alone |
| M5 — the fold-is-complete arm never fires | red: `test_the_fold_is_complete_still_prints_when_it_is` and two older cases |
| M6 — `coordinates` reads the ledger without fence tracking | red: `test_a_fenced_marker_in_the_ledger_opens_no_section`, alone |
| M7 — `coordinates` reads the FRAGMENTS without fence tracking | **exit 0, nothing red** — finding 3 |
| M8 — the opt-out is not told apart from no root | red: `test_an_opted_out_repository_is_told_which_state_it_is_in`, alone |
| M9 — the ref refusal talks about local mode again | red: `test_the_released_at_refusal_is_about_the_ref_and_nothing_else`, alone |
| M10 — the skill stops saying the command refuses local mode | red: `test_the_module_and_the_skill_both_say_local_mode_is_refused`, alone |
| M11 — `survey`'s docstring says the retirement is derived from it | red: `test_surveys_docstring_does_not_invite_the_mutation_that_reopens_finding_4`, alone |
| the pre-refactor `strip_comments` body against the shipped one, over `git ls-files "*.md"` and 584 comment-token arrangements | 1,435 files, 0 differing; 584 arrangements, 0 differing |
| `comment_scan` replaced at module level by a stub returning one sentinel pair | `strip_comments` → `['SENTINEL']`, `opens_outside_a_comment` → `[True]` — the single scan is pinnable, finding 4 |
| the eight modules that exercise `strip_comments`, `readable` and their callers | `336 passed`, exit 0 |
| `coordinates` over a scratch ledger holding a real section and a parked section marker below it | the parked marker opened a section and took `hooks/quoted.py` with it — finding 2 |
| `opens_outside_a_comment` over today's `seal/ledger.md`, and over it again with inline code spans blanked | 3 real markers lost, 787 lines not live; with code spans blanked, 0 lost and the parked marker still reads not live |
| `opens_outside_a_comment` over every top-level `docs/` document in this repository | 0 non-live lines — the shipped `folded_items` fix costs nothing on the real corpus |
| `settle` against a repository with no `seal/` and a DIRECTORY named `specseal-scratch` under its git directory | `home_at` → `""`; `settle` → exit 2, *has opted out … Delete that file to turn them back on* — finding 1 |
| `/usr/bin/python3` (3.9.6): compile, import and exercise of `skills/verify/scripts/unverified_check.py`; the command over this work item; `--baseline origin/release/v0.13.0 seal/specs` | all exit 0; 90 overviews · 303 open · 65 closed · 0 unreadable |
| `/usr/bin/python3 -m py_compile` over `.github/scripts/gather_changelog.py`, `.github/scripts/fold_ledger.py` and `hooks/optin.py` | exit 0 each |
| `evidence-check` over the work item's ledger fragment, and over `seal/ledger.md` | 13 ok and 1,402 ok · 0 drifted · 0 broken, exit 0 each |
| `folded_items` over this repository at the target SHA | empty set — `settle --retire` here removes nothing, so no destructive arm was reachable from this review |
| the broad gate — the full suite, repository-wide lint, typecheck | not yet. §2 assigns it to the sealer, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/unverified_check.py:85` · `:636` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py:604` | round 1's 2 — fixed |
| round-1 | `skills/settle/scripts/settle.py:497` · `:508` | round 1's 3 — fixed |
| round-1 | `skills/settle/scripts/settle.py:377` · `:426` | round 1's 4 — fixed |
| round-1 | `skills/settle/scripts/settle.py:450` | round 1's 5 — fixed |
| round-1 | `skills/settle/scripts/settle.py:218` · `.github/scripts/fold_ledger.py:210` | round 1's 6 — deferred |
| round-1 | `skills/verify/scripts/unverified_check.py:862` | round 1's 7 — fixed |
| round-1 | `overview.md:81` | round 1's 8 — fixed |
| round-1 | `CLAUDE.md` §*a change writes fragments, never the shared file* | round 1's 9 — deferred |
| round-1 | `spec.md` §*The ticket's headline claim is false* | round 1's 🟢 confirmation — confirmed |
| round-1 | `seal/ledger.md` | round 1's 🟢 confirmation — confirmed |
| round-1 | `overview.md` §*The dry run over this repository's own 97* | round 1's 🟢 confirmation — confirmed |
| round-1 | `overview.md` §*Where spec and implementation diverged* | round 1's 🟢 confirmation — confirmed |
| round-1 | `README*.md` · `docs/one-root-by-lifetime*.md` | round 1's 🟢 confirmation — confirmed |
| round-1 | `skills/settle/scripts/settle.py:95` | round 1's 🟢 confirmation — confirmed |
| round-1 | whole tree | round 1's ❓ scope — out of verified scope |
| round-2 | `skills/verify/scripts/unverified_check.py:668` · `skills/settle/scripts/settle.py:497` | round 2's 🔴 1 — fixed |
| round-2 | `skills/settle/scripts/settle.py:482` | round 2's 🟡 2 — fixed |
| round-2 | `skills/settle/scripts/settle.py:52` · `skills/settle/SKILL.md` | round 2's 🟡 3 — fixed |
| round-2 | `skills/settle/scripts/settle.py:559` · `:585` | round 2's 🟡 4 — fixed |
| round-2 | `skills/settle/scripts/settle.py:299` | round 2's 🟡 5 — fixed |
| round-2 | `skills/settle/scripts/settle.py:354` | round 2's 🟡 6 — fixed |
| round-2 | `skills/settle/scripts/settle.py:545` · `hooks/optin.py:200` | round 2's 🟡 7 — fixed |
| round-2 | `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3` | round 2's ⬜ 8 — fixed |
| round-2 | `skills/verify/scripts/unverified_check.py:668` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `skills/verify/scripts/unverified_check.py:97` | round 2's 🟢 confirmation — confirmed |
| round-2 | `skills/verify/scripts/unverified_check.py:658` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:545` · `:563` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:376` · `:472` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:482` · `tests/test_settle_reads_before_it_removes.py:244` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `skills/verify/scripts/unverified_check.py:894` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `overview.md:83` | round 2's 🟢 confirmation — confirmed closed |
| round-2 | `tests/test_settle_reads_before_it_removes.py` · `tests/test_unverified_rows_close.py` · `tests/test_a_script_says_which_interpreter_it_needs.py` | round 2's 🟢 confirmation — confirmed |
| round-2 | `seal/ledger.md` · `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md` | round 2's 🟢 confirmation — confirmed |
| round-2 | `overview.md:82` | round 2's 🟢 confirmation — confirmed |
| round-2 | the eleven places the fix-range run names | round 2's 🟢 confirmation — confirmed |
| round-2 | `skills/settle/scripts/settle.py:218` | round 2's ⬜ — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 1 — the opt-out arm reads the marker with `os.path.exists` | #489, milestone `release: 0.13.0` | the sibling work item that closes #489 on this release branch |
| 2 — `coordinates` got the fence half of the rule and not the comment half | #489 | the same work item; the ticket carries the code-span measurement |
| 3 — the fragments loop is pinned by nothing | #489 | the same work item |
| 4 — the single-scan pin does not pin a single scan | #489 | the same work item |
| 5 — ⬜ the refusal path resolves the git directory twice | #489 | the same work item |
| round 1's 6 and 9 | #487 and #488, carried from round 1 | the repository owner |

Every open row has a home and an answerer, so nothing is left in this
directory to drain. The run ended `capped` at this record: round 2 spent the
one reopening, and the five findings above are what a fourth fix pass would
have closed. They went into this release's milestone rather than the backlog
on purpose — the owner's standing answer to a branch-caused defect is to fix
it before it ships, and the chain gate is what keeps that fix out of THIS
pull request.
