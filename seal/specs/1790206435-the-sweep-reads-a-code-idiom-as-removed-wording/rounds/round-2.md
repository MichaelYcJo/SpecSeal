# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — review round 2

| Field | Value |
|---|---|
| Target SHA | 1f8cdcda56690b5be8ed0fdd28223da9e01f04ec |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 550 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `e6783db14ad7d4bec7ff3c580cabe367ce3948d5..9a2e200bcd5c98f8b4f79d3da91a7c9ff69981f7`, 1 commit |
| Contract changes | none |
| New units | newly_released (depth 1); two_sections (depth 1); test_a_release_that_rewords_an_entry_still_reports_its_verbatim_copy (depth 1); test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one (depth 1) |
| Needs a fix | yes — 🟡 1 and 🟡 2, one change to `corrected`'s held count in `skills/code-review/scripts/survivor_check.py`, with the gate row at `plan.md:170` and ledger row F1 rewritten to match |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round, reviewed at 1f8cdcda: round 1's fix range `dceb647b..c83e33fc` on `fix/543-the-sweep-reads-a-code-idiom-as-removed-wording`, and phase 5 (`6a424d81..64f42602`, #551's `--no-renames`), which was built after round 1's target on the owner's instruction and had not been reviewed. It asked whether round 1's 🟡 1 is closed — a release commit that only moves `## Unreleased` under a version heading removes nothing — and whether the held count writes nothing back; whether a release commit that ALSO rewords an entry while moving it still reports the reworded sentence's copy, the failure direction the gate row claims; whether the pure-move case is silent for the reason the docstring now gives; and whether leaving `whole_range`'s rename arm unpinned is right. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a release commit that rewords an entry while moving it under a version heading leaves a verbatim copy of the old wording unreported: the new wording never reaches `written`, so the removed sentence is one run at 1.00 against the base's two at 2.00 | `skills/code-review/scripts/survivor_check.py:981` | **fixed** `9a2e200b` | fixed at 9a2e200b — the report's paste-ready fix landed whole: `newly_released` after `only_released`, and `corrected` writes the released sentences' wording back when the file lost a sentence, so a reworded release splits the removed sentence into its runs again; `test_a_release_that_rewords_an_entry_still_reports_its_verbatim_copy` red at 1f8cdcda's script (exit 0, `against 2 sentence(s)`), green after; `only_released`'s docstring, a fifth carrier of *never written back*, corrected; executed: base exit 1 naming `docs/a.md:3`, tip exit 0, both `against 2 sentence(s)`; the docstring at `:939` names withholding `written` as safe, and in this scorer it merges runs; regression against the base in the silencing direction |
| 🟡 2 | the held count reads every version section at the tip rather than what the range moved, so a sentence that also stands in an older release holds its unreleased copy through any range, and the gate row and ledger row F1 state a narrower wrong allow than the code has | `skills/code-review/scripts/survivor_check.py:981` | **fixed** `9a2e200b` | fixed at 9a2e200b — `corrected` holds only `newly_released`, the released sentences at `b` beyond those at `a`; `test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one` red at 1f8cdcda's script (exit 0, `against 0 sentence(s)`), green after; the gate row in `plan.md` and fragment row F1 rewritten to the bound the code has, each with a `Corrected 2026-09-24` marker; the four real-range counts unchanged; executed: tip exit 0 `against 0 sentence(s)`, the fix exit 1 naming `docs/a.md:3`; the base was silent too, for another reason, so not a regression; the unit is round 1's and was reviewed by nobody until now |
| 🟢 | round 1's finding 1 is closed for the pure release — the unreleased section moved verbatim under a version heading removes nothing | `tests/test_a_corrected_sentence_survives_elsewhere.py:2658` | verified | executed: red with the `dceb647b` script (exit 1, `against 3 sentence(s)`), green at the tip; the reworded variant is 🟡 1 above |
| 🟢 | round 1's ⬜ 2 — `report`'s docstring says which unresolved declarations arrive | `skills/code-review/scripts/survivor_check.py:1404` | verified | read |
| 🟢 | round 1's ⬜ 3 — `phases/phase-3.md`'s removal row cites `whole_range`'s own docstring | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-3.md:92` | verified | read; the cited paragraph exists at `survivor_check.py:1301` |
| carried | round 1's ⬜ 4 — one blob read twice | `skills/code-review/scripts/survivor_check.py:781` | answered | already answered in round 1 (at `:764` of `6a424d81`); the grounds are unchanged at the tip |
| carried | round 1's ⬜ 5 — local-mode `OWNER_DIR` | `skills/code-review/scripts/survivor_check.py:1182` | deferred #554 | already deferred in round 1; `overview.md` names #554 under *Not done* |
| 🟢 | phase 5 — S17 and S18 are red against rename detection and green with `--no-renames` | `tests/test_a_corrected_sentence_survives_elsewhere.py:2822` | verified | executed: with the `6a424d81` script both fail at `against 0 sentence(s)`; each asserts `R…` |
| 🟢 | phase 5 — a pure move is silent because every removed sentence is written back, as the new docstring paragraph says | `skills/code-review/scripts/survivor_check.py:918` | verified | executed: `R099`, exit 0, `against 43 sentence(s)` |
| 🟢 | phase 5 — `whole_range`'s rename arm left unpinned is defensible: without the flag the declaration is refused as `not yours` and printed, never silenced | `skills/code-review/scripts/survivor_check.py:1343` | verified | executed: `R096` out of a work item directory; tip exit 0 with the declaration matched, flag removed exit 1 with `not yours`; disclosed in `phases/phase-5.md` and ledger row R1 |
| 🟢 | phase 5 — the class: both `git diff` calls of the sweep take the flag, and no other source list in the tree reads the range by name | `skills/code-review/scripts/survivor_check.py:943` | verified | read; `chain_check.py` and `round_record.py` use `-M` on purpose |
| ❓ | the full suite, `ruff check .`, `ruff format --check .`, and `evidence-check --strict .` after the fix pass | the tree at the reviewed HEAD | ❓ out of verified scope | `agent-contract` §2: the sealer's, after the rounds settle; answered by the sealer |

## Paste-ready fixes

```python
def newly_released(path, before, after):
    """`[Sentence]` standing under a version heading at `after` beyond what
    stood under one at `before` -- what the range itself moved or wrote into
    a released section, counted per sentence."""

    def released(text):
        return [
            Sentence(path, line, raw)
            for line, raw in segments(blank_struck(only_released(text)))
            if raw
        ]

    prior = Counter(s.key for s in released(before))
    out = []
    for sentence in released(after):
        if prior[sentence.key] > 0:
            prior[sentence.key] -= 1
        else:
            out.append(sentence)
    return out
```
```python
        moved = []
        if path == CHANGELOG and path in after:
            # A release moves `## Unreleased` under a version heading. What
            # THIS range put under one is held, never a heading the file
            # already had: a sentence standing in an older release is not
            # what a correction to the live section kept.
            moved = newly_released(path, before.get(path, ""), after[path])
        counted = Counter(s.key for s in now + moved)
        seen, lost = Counter(), len(gone)
        for sentence in was:
            seen[sentence.key] += 1
            if seen[sentence.key] > counted[sentence.key]:
                gone.append(sentence)
        if len(gone) == lost:
            # Nothing of this file was removed, so there is nothing the moved
            # section's wording could split; a gathered release writes none.
            moved = []
        old = Counter(s.key for s in was)
        fresh = Counter()
        for sentence in now + moved:
```
```text
    **The release commit is held, not removed** (round 1's 🟡 1, round 2's
    🟡 1 and 🟡 2). In a repository that lets the entry accumulate under
    `## Unreleased`, the release moves that section under a version heading.
    The section is live at `a` and blanked at `b`, so counted as any other
    file it reads as every sentence removed, and a document restating an
    entry is reported at the release with nothing anybody may correct. So
    for `CHANGELOG.md` the sentences this range put under a version heading
    -- the released sentences at `b` beyond those at `a` -- are added to the
    held count before the difference is taken; a sentence standing in an
    older release holds nothing. And where the file lost a sentence, their
    fresh wording is written, as any file's is: an entry reworded as it is
    released splits the removed sentence into the runs it no longer shares,
    and withholding it would merge them into one that never clears the
    floor. A release that removes no live sentence writes nothing, which
    keeps a gathered release's text out of `written`.
```
```python
def two_sections(unreleased, older):
    return (
        f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {unreleased}\n\n"
        f"## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- {older}\n"
    )


def test_a_release_that_rewords_an_entry_still_reports_its_verbatim_copy(tmp_path):
    """Round 2's 🟡 1. The release rewords the entry as it moves it under a
    version heading, and a document quotes the old wording verbatim. The new
    wording has to reach `written`, or the removed sentence is one run at
    1.00 and never clears the floor. Red at 1f8cdcda: exit 0, `against 2
    sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": changelog("## Unreleased", FOUND),
            **FILLER,
        },
        "the entry under Unreleased, and a document quoting it verbatim",
    )
    head = build(
        repo,
        {"CHANGELOG.md": changelog(RELEASED_HEADINGS[0], REPAIRED)},
        "release 1.0.0, rewording the entry as it is released",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the release reworded the entry and docs/a.md still quotes the old "
        f"wording verbatim; exit {code}\n{text}"
    )
    assert "docs/a.md" in text, text


def test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one(tmp_path):
    """Round 2's 🟡 2. Only what the range put under a version heading is
    held. A sentence that also stands in an older release must not keep its
    unreleased copy from counting as removed. Red at 1f8cdcda: exit 0,
    `against 0 sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "CHANGELOG.md": two_sections(FOUND, FOUND),
            **FILLER,
        },
        "an unreleased entry repeating an older release's sentence",
    )
    head = build(
        repo,
        {"CHANGELOG.md": two_sections(REPAIRED, FOUND)},
        "reword the unreleased entry; no release",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the unreleased entry was reworded and its copy in docs/a.md went "
        f"unreported because 0.9.0 carries the same sentence; exit {code}\n{text}"
    )
    assert "docs/a.md" in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `1f8cdcda` | 94 passed in 44.46 s, exit 0 |
| the three new cases with the `dceb647b` script swapped in, restored with `git checkout` | round 1's case red (exit 1, `against 3 sentence(s)`); S17 and S18 green |
| the three new cases with the `6a424d81` script swapped in, restored | 3 failed: round 1's case at `against 3`, S17 at exit 0 `against 0`, S18 at `against 0` |
| P1 — release renames `## Unreleased` to `## 1.0.0 — 2026-01-01` and rewords FOUND to REPAIRED; `docs/a.md` quotes FOUND verbatim | base exit 1 `docs/a.md:3`; tip exit 0; both `against 2 sentence(s)` |
| P1b — the same with `docs/a.md` restating FOUND in two runs | base, tip and the fix all exit 1 on `docs/a.md:3` |
| P2 — FOUND under `## Unreleased` and under `## 0.9.0`, a non-release commit rewords the Unreleased copy | base exit 0 (`against 1`); tip exit 0 (`against 0`); the fix exit 1 on `docs/a.md:3` |
| P2 control — the same without the older copy | base, tip and the fix all exit 1 on `docs/a.md:3` |
| P3 — round 1's case (pure release, two-run restatement) | base, tip and the fix all exit 0 |
| P4 — the S18 fixture at the tip | `R099 a.md b.md`; exit 0, `against 43 sentence(s)` |
| P5 — a file moved out of a work item directory (`R096`) with one sentence reworded; that work item's declaration for the exact range via `--exempt` | tip exit 0, matched; flag removed from `whole_range` only: exit 1, `not yours … touches nothing in it`, `elsewhere.md:3` reported |
| P6 — a gathered release and a correction to `docs/a.md` in one commit, `docs/b.md` quoting FOUND | base exit 0 (the gathered text reached `written` and subtracted FOUND); tip exit 1 on `docs/b.md:3`; the fix exit 1 on `docs/b.md:3` |
| the fix below applied in the clone: the module | 94 passed in 57.04 s, exit 0; the four real-range cases included |
| the fix applied: the two proposed cases | both green; restored to `1f8cdcda`, both red (exit 0 at `against 2` and at `against 0`) |
| the fix applied: `uvx ruff check` and `uvx ruff format --check` on `survivor_check.py` alone | all checks passed; already formatted |
| full suite, `ruff check .`, `ruff format --check .` (the broad gate) | not yet — no run has happened; the sealer's, once the rounds settle |
| `evidence-check --strict .`, `unverified-check` | not yet — not run by this round; the orchestrator re-runs after the fix pass and the sealer's `ledger` arm answers it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:930` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1345` | round 1's ⬜ 2 — fixed |
| round-1 | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-3.md:92` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:764` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py:1127` | round 1's ⬜ 5 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:591` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:523` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1293` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-1.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/plan.md` | round 1's 🟢 — confirmed |
| round-1 | the tree at the reviewed HEAD | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| in local mode `OWNER_DIR` names an owner `changed` can never contain (round 1's ⬜ 5) | #554 — already deferred in round 1 | the owner of #554 |
