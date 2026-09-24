# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — round 2 report

Verifying round. Target SHA `1f8cdcda`, base `release/v0.15.1` (`9f846733`).
Two surfaces: round 1's fix range `dceb647b..c83e33fc` (one commit), and
phase 5 (#551, `6a424d81..64f42602`, commits `943651b8` and `64f42602`),
which was built after round 1's target and had been reviewed by nobody.
Worked in a `git clone --no-local` at the target SHA under the round's
scratch directory. Narrow runs only: the module, the three new cases, and
probes. The broad gate is the sealer's.

Round 1's coordinates were carried from `round-1.md` and `round-1-report.md`
and opened, not re-found. Its verdicts were re-derived for every row the
fixes touched.

## Summary

The three new cases are sound. Each is red with its fix reverted and green
at the tip. Phase 5's `--no-renames` is right, and a pure move is silent for
the reason the docstring now gives. Leaving `whole_range`'s rename arm
unpinned is defensible, because removing the flag there denies wrongly and
prints the denial; it never silences anything.

Round 1's fix does not hold in the direction the prompt asked about. Both
defects sit in one block of `corrected`, `skills/code-review/scripts/survivor_check.py:973-985`:

- **🟡 1.** A release commit can reword an entry as it moves it under a
  version heading. When it does, a verbatim copy of the old wording
  elsewhere goes unreported. The base reports it. The tip does not, because
  the new wording never reaches `written`.
- **🟡 2.** The held count reads every version heading at the tip, not only
  what the range moved there. A sentence that also stands in an older
  release keeps its `## Unreleased` copy counted as held through any range,
  release or not.

One change to that block closes both, and it is fenced below. It was
executed against the module (94 passed) and against both proposed cases,
which are red at the tip and green with the change.

## 🟡 1 — a release that rewords an entry silences the old wording's verbatim copy

**Where.** `skills/code-review/scripts/survivor_check.py:981` (the held
count) and `:993` (the loop that fills `written`). The docstring paragraph
at `:930-942` states the reasoning.

**What happens (executed).** At `a`, `CHANGELOG.md` has the entry FOUND
under `## Unreleased`, and `docs/a.md` quotes FOUND verbatim. The release
commit renames the section to `## 1.0.0 — 2026-01-01` and rewords the entry
to REPAIRED as it does so.

| Script | Exit | Removed | Reported |
|---|---|---|---|
| base `9f846733` | 1 | 2 sentences | `docs/a.md:3` |
| tip `1f8cdcda` | **0** | 2 sentences | nothing |

**Why.** FOUND is correctly counted as removed. But REPAIRED stands under a
version heading at `b`. `now` is built through `blank_released`, so
REPAIRED is not in it, and the held count adds keys to `counted` only.
Nothing puts REPAIRED's n-grams into `written`. So `wanted` keeps every
n-gram of FOUND, including the stretch REPAIRED wrote back. The verbatim
copy then shares one contiguous run with the source. `runs` counts that as
one piece of evidence, and it scores 1.00, under `FLOOR` (1.6).

At the base the reworded entry was in `written`. That split FOUND into the
two runs REPAIRED does not share, which scores 2.00 and is reported.

**Why it matters.** The paragraph at `:939` reads *Counted and never
written: nothing from a released section reaches `written`, so it
subtracts nothing from what the range is looking for*. That treats "subtract
nothing" as the safe direction, and in this scorer it is not. What `written`
subtracts is what splits a removed sentence into independent runs, and runs
are what the score counts. Withholding it merges the runs and lowers the
score.

So a correction made while releasing, with its old wording quoted verbatim
elsewhere, goes silent. That is the direction this check exists to stop, and
it regresses against the base. A restatement that breaks the copy into two
runs is still reported: probe P1b at base, tip and with the fix. That is why
round 1's case, which uses a two-run restatement, could not see this.

**Attribution.** The block that silences the copy is `blank_released` on the
range side, from phase 2 (#307). Round 1's fix did not create it. It is in
the event the fix and its gate row address, and the fix's docstring states
the reasoning that produces it. The prompt named this probe.

## 🟡 2 — a sentence standing in an older release holds its unreleased copy

**Where.** `skills/code-review/scripts/survivor_check.py:981`. The block
reads `only_released(after[path])`, which is every version section at `b`.
It does not read what this range moved.

**What happens (executed).** `CHANGELOG.md` carries FOUND both under
`## Unreleased` and under an older `## 0.9.0 — 2025-01-01`. A commit that is
not a release rewords the Unreleased entry to REPAIRED. `docs/a.md` quotes
FOUND.

| Script | Exit | Removed | Reported |
|---|---|---|---|
| base `9f846733` | 0 | 1 sentence | nothing (the 0.9.0 copy is a second carrier, which lowers the weight) |
| tip `1f8cdcda` | **0** | **0 sentences** | nothing |
| the fix below | 1 | 1 sentence | `docs/a.md:3` |
| control, no older copy: base, tip, fix | 1 | 1 sentence | `docs/a.md:3` |

**Why it matters.** The base was silent here too, so this is not a
regression. The branch's new unit is what silences it, though. And the gate
row states a bound the code does not have: `plan.md:170` and ledger fragment
row F1 say *the wrong allow is a sentence a release both moved under a
heading and removed from a live document in one commit — which no release
commit does*. The executed wrong allow is any range, not only a release,
where the removed sentence also stands under any version heading.

The fix is to hold only what this range put under a version heading. That is
the multiset difference between the released sentences at `b` and those at
`a`. Round 1's pure-release case still passes with it.

## Round 1's rows, re-derived

- **🟡 1, the pure release.** Verified. The round 1 case is red with the
  `dceb647b` script swapped in (exit 1, `against 3 sentence(s)`) and green
  at the tip. The same event with the release's entry quoted verbatim is
  silent at base, tip and fix (probe P3). What does not hold is the
  reworded variant, which is 🟡 1 of this round.
- **⬜ 2.** Verified by reading. `report`'s docstring at `:1403-1407` now
  says `whole_range` decides by the second anchor which unresolved
  declarations arrive.
- **⬜ 3.** Verified by reading. `phases/phase-3.md:92` cites `whole_range`'s
  own docstring, carries a dated correction note, and the paragraph it
  cites exists.
- **⬜ 4.** Answered, carried. One blob is read twice, and the grounds stand.
- **⬜ 5.** Deferred to #554, carried. `overview.md` now names it under
  *Not done*.

## Phase 5 (#551), verified

- **S17 and S18 are red with the fix reverted.** With the `6a424d81` script
  swapped in, S17 exits 0 at `against 0 sentence(s)` and S18 fails its
  count assertion at `against 0 sentence(s)`. Both are green at the tip.
  Each asserts git reports `R…`, so neither can quietly turn into the
  delete-plus-add shape.
- **A pure move is silent for the reason the docstring gives.** Probe P4 is
  the S18 fixture (`R099 a.md b.md`). It exits 0 with `against 43
  sentence(s)`, so the old path is read and every removed sentence is
  written back. Under rename detection the count was 0.
- **`whole_range`'s unpinned arm.** Probe P5 moves
  `seal/specs/<id>/notes.md` to `docs/notes.md` as `R096`, with one sentence
  reworded, and passes a declaration of that work item for the exact range.
  At the tip the declaration matches and the run exits 0. With the flag
  removed from `whole_range` only, it prints `not yours … this range
  touches nothing in it` and exits 1 on `elsewhere.md:3`. That is the
  direction `phases/phase-5.md` states: a wrong deny that prints, never a
  silence. Leaving the arm unpinned is honest, and it is disclosed in two
  records. A case is optional, and it is listed below.
- **The class, enumerated.** `git diff` runs in two places in
  `survivor_check.py`, and both take the flag. The other `--name-only`
  callers in the tree answer a different question. `chain_check.py:878`
  and `:884` and `round_record.py:2965` read renames on purpose with `-M`.
  The rest are `ls-tree` calls or the commit gate's file list. None is a
  sweep source list.
- **`retired_directories` with the flag.** Read. A fold that git used to
  see as a rename out of `seal/specs/<id>/` now lists the old path. That
  path lands in a retired directory and leaves the range, and the new
  `docs/` path is written only. The outcome is unchanged.

## Regression tests to plant

Destination: `tests/test_a_corrected_sentence_survives_elsewhere.py`, beside
the round 1 case at `:2658`. Both were executed as probes: red at
`1f8cdcda`, green with the fix below. The first exits 0 at `against 2
sentence(s)` and the second at `against 0 sentence(s)`. The fenced
paste-ready block carries them.

Optional, not a finding: a case for `whole_range`'s rename arm in probe P5's
shape, beside S13 and S14. It uses `ITEM_A`, `LONG_SECTION` and `GROUNDS`,
and asserts exit 0 with the grounds printed.

## Facts for the evidence ledger

- **F1 (fragment) has to be rewritten with the fix.** Its claim *counted
  and never written back* stops being true, and its stated wrong allow is
  the bound 🟡 2 shows false.
- **`plan.md:170`.** The gate-table row for round 1's fix carries the same
  sentence and needs the same rewrite.
- **The `corrected` docstring paragraph** at `:930-942`. The replacement is
  fenced below.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a release commit that rewords an entry while moving it under a version heading leaves a verbatim copy of the old wording unreported: the new wording never reaches `written`, so the removed sentence is one run at 1.00 against the base's two at 2.00 | `skills/code-review/scripts/survivor_check.py:981` | open | executed: base exit 1 naming `docs/a.md:3`, tip exit 0, both `against 2 sentence(s)`; the docstring at `:939` names withholding `written` as safe, and in this scorer it merges runs; regression against the base in the silencing direction |
| 🟡 2 | the held count reads every version section at the tip rather than what the range moved, so a sentence that also stands in an older release holds its unreleased copy through any range, and the gate row and ledger row F1 state a narrower wrong allow than the code has | `skills/code-review/scripts/survivor_check.py:981` | open | executed: tip exit 0 `against 0 sentence(s)`, the fix exit 1 naming `docs/a.md:3`; the base was silent too, for another reason, so not a regression; the unit is round 1's and was reviewed by nobody until now |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| in local mode `OWNER_DIR` names an owner `changed` can never contain (round 1's ⬜ 5) | #554 — already deferred in round 1 | the owner of #554 |

## Paste-ready fixes

### 🟡 1 and 🟡 2 — one change to `corrected`, and the helper it calls

Place the helper after `only_released`:

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

In `corrected`'s loop, replace everything from `counted = Counter(s.key for s in now)`
through `for sentence in now:` with:

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

The `lost` guard is why P6 stays reported. This repository's release
inserts a version section and removes no live sentence, so the gathered
text never reaches `written`. At the base it did, and that silenced P6.

Replace the docstring paragraph at `:930-942`:

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

### The two regression cases

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

Needs a fix: yes — 🟡 1 and 🟡 2, one change to `corrected`'s held count in `skills/code-review/scripts/survivor_check.py`, with the gate row at `plan.md:170` and ledger row F1 rewritten to match

Loses a record or crashes: no

## Proof block

Files opened this round, in the clone at `1f8cdcda` unless noted:

- `skills/code-review/scripts/survivor_check.py` — `:480-560`, `:643-760`, `:778-1010`, `:1023-1140`, `:1267-1360`, and the two diffs
- `tests/test_a_corrected_sentence_survives_elsewhere.py` — `:85-110`, `:440-470`, `:530-545`, `:640-690`, `:1609-1700`, `:2155-2165`, `:2570-2600`, `:2720-2735`, and the two diffs
- `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/rounds/round-1.md` and `round-1-report.md` (main checkout)
- `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-5.md`; the `plan.md`, `spec.md`, `overview.md` and `phases/phase-3.md` diffs over the two ranges
- `seal/ledger/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording.md` — rows F1, R1, U1, U2, C2
- `skills/code-review/scripts/chain_check.py:395-440` (the closing vocabulary, main checkout); `bin/test`; `CHANGELOG.md:1-20`
- the `--name-only` / `--name-status` callers under `skills/`, `.github/` and `hooks/` (grep)

The probe file (one `test_tmp` file under the clone's `tests/`) and the three temporary script NAME NOT IN TREE
copies it wrote were deleted. The clone's tree was restored with
`git checkout` after each swap, and `git status --short` was empty at the
end. The clone and its runner venv are removed at hand-over.
