# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — review round 1

| Field | Value |
|---|---|
| Target SHA | 6a424d812541cb73b63f8972d76c9e556b65990b |
| Written late | no |
| Ran by | warden on Fable 5.1 |
| PR | 550 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `dceb647bd921c5a2d72eb34283c1b97ab3f48acb..c83e33fcc69d32aa842882167864f490b484780d`, 1 commit |
| Contract changes | none |
| New units | only_released (depth 1); test_a_release_that_moves_the_unreleased_section_under_a_version_removes_nothing (depth 1) |
| Needs a fix | yes — 🟡 1, the release commit that moves `## Unreleased` under a version heading |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 was asked to review the whole branch at 6a424d81 against `release/v0.15.1` (9f846733): spec compliance first against `spec.md` §The measured state and §Data & interfaces and `plan.md`'s gate table — this sweep runs in CI's hygiene job and at every seal, so a wrong failure direction silences a real survivor — then quality, in a clone under the round's own directory, narrow runs only, with the smith's handoff before round 1 as the account to audit: the tokenizer reader, the released-section blank and the gathered set, the ownership question before `unresolved`, the four real-range counts and their two divergences, and the rename gap the branch found and left filed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a release commit that moves `## Unreleased` under a version heading counts every sentence of the section as removed; a document restating an entry is reported at the release with nothing correctable — a regression against the base in the repository shape the heading-based reading was chosen for | `skills/code-review/scripts/survivor_check.py:930` | **fixed** `c83e33fc` | fixed at c83e33fc — `only_released` beside `blank_released`; `corrected` adds the sentences standing under a version heading at the tip to `CHANGELOG.md`'s held count before the difference is taken, counted and never written back; `test_a_release_that_moves_the_unreleased_section_under_a_version_removes_nothing` red at 64f42602 (`against 3 sentence(s)`, `docs/a.md:3` at 2.00), green after; gate-table row under `plan.md` §Operational impact; the four real-range counts unchanged (4/60, 0/61, 8/35, 1/156); executed: base `9f846733` exit 0 against 1 sentence, tip `6a424d81` exit 1 naming `docs/a.md:3` at 2.00; the gathered-fragment shape of the same event is silent |
| ⬜ 2 | `report`'s docstring says every unresolved declaration is printed; since phase 3 a foreign one is dropped before it arrives | `skills/code-review/scripts/survivor_check.py:1345` | **fixed** `c83e33fc` | fixed at c83e33fc — `report`'s docstring says `unresolved` is the declarations this run could have used, decided by `whole_range`'s second anchor, so a foreign one never arrives; read; behaviour right, sentence overstates |
| ⬜ 3 | `phases/phase-3.md` cites `docs/review-chain-spec.md` §The survivor sweep for a sentence that section does not carry | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-3.md:92` | **fixed** `c83e33fc` | fixed at c83e33fc — `phases/phase-3.md`'s removal row cites `whole_range`'s own docstring instead of `docs/review-chain-spec.md` §The survivor sweep, with a dated note that the citation was corrected by this pass; read; paperwork under `seal/specs/`, a correction and not a fix |
| ⬜ 4 | the tip's `CHANGELOG.md` is read twice per run, once from `corpus` and once from `corrected` | `skills/code-review/scripts/survivor_check.py:764` | answered | `gathered_fragments` reads one blob once from `corpus` and once from `corrected`, one process spawn per run; threading the set down would widen `corpus`'s and `corrected`'s signatures, which S6, E1, C2 and F1 anchor and three ledger rows cite; no change; read; one process spawn, answerable with grounds |
| ⬜ 5 | in local mode `OWNER_DIR` names an owner `changed` can never contain, so a declaration is `not yours` for its own run (base) and an unresolved one is now silent (tip) | `skills/code-review/scripts/survivor_check.py:1127` | deferred new issue | executed; pre-existing in its cause, wrong allow empty |
| 🟢 | #543 · `python_prose` keeps COMMENT, STRING and FSTRING_MIDDLE, blanks the rest with a `\|`, falls back whole on a tokenizer error, and holds line numbers over CRLF | `skills/code-review/scripts/survivor_check.py:591` | confirmed | read against `spec.md` §Data & interfaces; the module's 91 cases and the CRLF probe executed |
| 🟢 | #307 · the released region is read off the heading in the three spellings, `## Unreleased` stays live, the gathered set is read off the marker with no path list | `skills/code-review/scripts/survivor_check.py:523` | confirmed | read; S7–S11 executed in the module run |
| 🟢 | #439 · an unresolved declaration takes the ownership question from the same lazy `changed` list; ownerless and owned-and-touched still print | `skills/code-review/scripts/survivor_check.py:1293` | confirmed | read; S13, S14 and G6 executed in the module run |
| 🟢 | the B-range divergence (9 → 8 at phase 1) is the reader applied on the range side, and the row it drops was already excused by the previous frame | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-1.md` | confirmed | executed: base and tip scripts over `3dd24073^..3dd24073` |
| 🟢 | the gate table's four rows are carried per phase — red-first, direction, zero prompts, platform | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/plan.md` | confirmed | read; the smith's red-first runs are its claim, the mutations likewise |
| ❓ | the full suite, `ruff check .` and `ruff format --check .`; S15 and S16 at the seal | the tree at the reviewed HEAD | ❓ out of verified scope | `agent-contract` §2 — the sealer's, after the rounds settle |

## Paste-ready fixes

```python
def only_released(text):
    """The complement of `blank_released`: every line of a released section
    kept, line numbers intact, every other line blanked.

    Read by `corrected` for the tip's changelog, so a sentence a release
    moved from `## Unreleased` under a version heading is counted as still
    held rather than as removed. Counted, never written back: a released
    section subtracts nothing from what the range is looking for."""
    out, released = [], False
    for line in text.split("\n"):
        if SECTION_HEADING.match(line):
            released = VERSION_HEADING.match(line) is not None
        out.append(line if released else "")
    return "\n".join(out)
```
```python
        counted = Counter(s.key for s in now)
        if path == CHANGELOG and path in after:
            # A release moves `## Unreleased` under a version heading. The
            # section is blanked at `b`, so without this every sentence of
            # it would count as removed and the documents restating an entry
            # would be reported at the release with nothing to correct -- the
            # gathered-fragment shape, one heading over. Held, not written:
            # nothing here reaches `written`.
            counted.update(
                sentence.key
                for line, raw in segments(blank_struck(only_released(after[path])))
                if raw
                for sentence in (Sentence(path, line, raw),)
            )
```
```python
def test_a_release_that_moves_the_unreleased_section_under_a_version_removes_nothing(
    tmp_path,
):
    """The release commit of a repository that lets the entry accumulate
    unreleased: `## Unreleased` takes a version heading and nothing else
    changes. The section is live at `a` and blanked at `b`, so without the
    held-count every sentence of it reads as removed and the document
    restating an entry is reported at the release with nothing anybody may
    correct. Two disjoint runs in the restatement, because one run scores
    1.00 and never clears the floor."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    restated = FOUND.replace("itself and the", "itself and, from then on, the")
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{restated}\n",
            "CHANGELOG.md": changelog("## Unreleased", FOUND),
            **FILLER,
        },
        "the entry under Unreleased, and a document restating it",
    )
    head = build(
        repo,
        {"CHANGELOG.md": changelog(RELEASED_HEADINGS[0], FOUND)},
        "release 1.0.0: the unreleased section takes a version heading",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 0, (
        "a release that only moved the unreleased section under a version "
        f"heading was read as a correction to chase into docs/a.md; exit {code}\n{text}"
    )
    assert "docs/a.md" not in text.split("examined", 1)[-1], text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `6a424d81` | 91 passed in 44.17 s, exit 0; the four real-range commits resolve in the clone, none skipped |
| release commit renaming `## Unreleased` to `## 1.0.0 — 2026-01-01`, `docs/a.md` restating the entry with two disjoint runs, base script `9f846733` | exit 0, `against 1 sentence(s)`, no removed wording standing |
| the same fixture, tip script `6a424d81` | exit 1, `against 3 sentence(s)`, `docs/a.md:3` at 2.00 against `CHANGELOG.md:7` |
| the same event as a gathered fragment — fragment deleted, its text written under `## 1.0.0` with its marker — tip script | exit 0, `against 0 sentence(s)` |
| the release commit with `docs/a.md` carrying the entry verbatim (one run), tip script | exit 0 — one run scores 1.00, under the floor by the module's own design; the two-run fixture above is the calibrated shape |
| `python_prose` over `x = 1\r\n"""doc one\r\nline two"""\r\ny = "lit"\r\n` | 4 lines in, 4 out; widths `[6, 11, 12, 10, 0]` both ways; sentence keys `doc one line two`, `lit` |
| `--exempt <repo>/.git/seal/specs/<id>/survivors.md` holding `origin/gone..HEAD`, tip script | exit 1, the survivor named, no `unresolved` line |
| the same file holding this run's own resolved range, tip script | exit 1, `not yours … written by seal/specs/<id> and this range touches nothing in it` |
| base script over `3dd24073^..3dd24073` | exit 1, 9 places including `seal/ledger.md:2053` at 2.47 (*no longer the first*, *the paragraph does*, *applies to the*) and `CHANGELOG.md:2090` |
| tip script over the same range | exit 1, 8 places: the two above gone, `skills/code-review/scripts/survivor_check.py:142` joined |
| full suite, `ruff check .`, `ruff format --check .` (the broad gate) | not yet |
| `evidence-check --strict .`, `unverified-check` | not run by this round; the handoff reports 0 and 0 as the orchestrator's re-run, read here and the sealer's `ledger` arm answers it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a whole file moved as a rename (`R096`) with one sentence reworded is silent, because `git diff --name-only` runs with rename detection and lists the new path alone; repair `--no-renames` on both calls with a red-first case | already deferred in `overview.md` §*Not done* and ledger row U2; a new issue | the orchestrator, who files it with the repair in `phases/phase-3.md` |
| in local mode `OWNER_DIR` names an owner that `changed` can never contain, so the ownership question refuses every local-mode declaration (⬜ 5) | a new issue, beside the rename one — both are `whole_range`/`corrected` gate changes outside the three tickets | the orchestrator, who files it |
