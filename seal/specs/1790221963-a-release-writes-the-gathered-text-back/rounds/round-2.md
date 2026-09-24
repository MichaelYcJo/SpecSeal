# 1790221963-a-release-writes-the-gathered-text-back — review round 2

| Field | Value |
|---|---|
| Target SHA | e6c85df63ece3b680b6d923fb97fb3ba540f94d6 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 560 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `ab9b026b16ff41b4f4b11a2ff680ba50206620ea..e5dc540d4d730da0331977dd64f6b046c93e5ab0`, 2 commits |
| Contract changes | corrected → round-1-report.md, round-1.md, spec.md, round-3-report.md, round-3.md, round-2-report.md, round-2.md, examine; score → round-2-report.md, round-2.md, examine |
| New units | test_a_gathered_fragment_cannot_subtract_a_survivor_through_a_lost_entry (depth 1) |
| Needs a fix | yes — 🟡 1, the round-1 split writes gathered n-grams for every file, so a gathered fragment again subtracts another file's survivor (Z1, Z2 silent at the tip) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round at round 1's fixes (`0b094396..1e2905cc`), reviewed at e6c85df6. It asked whether X5 is red with the split removed and green at the target, whether P6, P6d, H1k, H1, H1c, H2k, H2 and X1–X6 give what round 1's table gives, whether the new docstring bound matches the code, and whether the one shape the fix pass measured as still reporting less than the base — a sentence removed from another file whose new wording lives only in a gathered fragment — is the rule working or a defect. It was told that a 🟡 here spends the run's one reopening.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the round-1 split writes a gathered sentence's n-grams into `written`, which every file's removed sentences are scored against, so where the lost changelog entry shares a claim's wording, a gathered fragment quoting it subtracts the survivor that a correction in another file left, which is #557's defect back through the fix, and the code comment, module docstring and ledger H1 each say it cannot happen | `skills/code-review/scripts/survivor_check.py:1062` | **fixed** `d66b9632` | fixed at d66b9632 — and e5dc540d — the reviewer's paste-ready fix, whole: the split is `corrected`'s third return value and `score` subtracts it from a `CHANGELOG.md` source alone, `examine` passing it; the reviewer's case red at e6c85df6 (exit 0, `against 3 sentence(s)`), green after; six mutations isolate it — removing the subtraction fails X5 alone, writing the split back or scoring every source with it fails the new case alone; the comment, both docstrings and ledger H1 and F1 state the source-scoped bound; executed: Z1 and Z2 exit 1 at `bf7ba905`, exit 0 at `e6c85df6`; Z1n (no fragment) exit 1 at all four states; the per-source fix below trialled: module 104 passed, the new case red at the tip, X5 alone red with the split removed, X5W kept at 1 where the set-level patch loses it |
| 🟢 | round 1's finding 1 is closed: a gathered rewording of a lost live entry splits it again | `skills/code-review/scripts/survivor_check.py:1062` | confirmed | executed: X5 failed (1 failed, 102 deselected) with `bf7ba905`'s script swapped in, restored with `git checkout`; module 103 passed at the tip; X5 exit 1 naming `docs/b.md` at the tip, 0 at `bf7ba905`, 1 at the base |
| 🟢 | round 1's shapes answer as recorded at the tip: P6, P6d, H1k, H1, H1c, H2k, H2 exit 1 naming `docs/b.md`; X1–X4 exit 0; X6 exit 1 | `skills/code-review/scripts/survivor_check.py:1047` | confirmed | executed at four script states; H1k, H1, H2k, H2 exit 0 at `61f0d0d8`; unchanged from round 1's table |
| 🟢 | round 1's finding 2 is closed: the records state the failure direction after the fix, and the one report-less shape they name is the rule working | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | confirmed | read at `plan.md:144`, `spec.md` §Out, ledger H1; executed: W exit 1 at the base, 0 at `bf7ba905` and the tip; controls Wc exit 0 and Ww exit 1 at every state, so the tip treats gathered wording as wording that predates the range |
| 🟢 | round 1's finding 3 is closed: the records say step A's gate row was left as written, and that step A is squashed, not released | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | confirmed | read at `questions.md:23`, `spec.md` judgment 7, `plan.md:103`, the overview's divergence row; executed: the sweep over `0b094396..1e2905cc` with `survivors.md` exit 0, one exempt row |
| carried | round 1's finding 4, a file moved whole writes the corrected wording it quotes | `skills/code-review/scripts/survivor_check.py:1054` | deferred #563 | already deferred in round 1; X1 exit 0 at all four states, unchanged by the fix range |
| carried | round 1's findings 5–7: the fragment path spelled two ways, a fragment's own `## ` heading, a CRLF changelog | `skills/code-review/scripts/survivor_check.py:1016` | deferred #564 | already deferred in round 1; X2, X3, X4 exit 0 at all four states, unchanged by the fix range |
| ❓ | the other modules that load the sweep and the hygiene modules were not re-run this round | `tests/` | ❓ out of verified scope | the orchestrator reports `149 passed` at `1e2905cc`; this round ran the one module. Who answers it: the sealer, whose full suite covers them |

## Paste-ready fixes

```python
    gone, written, split = [], set(), set()
```
```python
        # ...except against what THIS file lost: a live entry the release
        # replaced with a gathered fragment rewording it is still split by
        # that rewording, as a reworded release is (step A's round 2 🟡 1).
        # Those n-grams are kept apart from `written`, which every file's
        # removed sentences are scored against, and `score` subtracts them
        # from this file's alone: written for every file, a fragment quoting
        # wording the same commit corrected elsewhere would subtract that
        # survivor again (round 2's 🟡 1).
        lost_here = {gram for sentence in gone[lost:] for gram in sentence.grams()}
        for sentence in held:
            split.update(gram for gram in sentence.grams() if gram in lost_here)
```
```python
    return gone, written, split
```
```python
    """`[Sentence]` -- what the range removed -- the n-grams it wrote, and
    the gathered n-grams that split `CHANGELOG.md`'s removed sentences alone.
```
```python
    🟡 1, #557). Of a gathered sentence, only the n-grams that also occur in a
    sentence THIS file lost count, and they are the third return rather than
    part of `written`: `score` subtracts them from `CHANGELOG.md`'s removed
    sentences alone, so a live entry the release replaced with a gathered
    fragment rewording it is still split into the runs it no longer shares,
    as a reworded release is, while no gathered text subtracts another
    file's sentence. A release that removes no live sentence writes nothing
    at all."""
```
```python
def score(gone, keep, where, weight_of, floor, split=frozenset()):
```
```python
        mine = set(sequence) & keep
        if source.path == CHANGELOG:
            # What a gathered rewording shares with the entry it replaced
            # splits that entry, and no other file's sentence (`corrected`).
            mine -= split
```
```python
    gone, written, split = corrected(root, a, b)
```
```python
        score(gone, keep, where, weights(len(pool), files), floor, split),
```
```python
at the release and not written as the range's own (#557): the fragment's
own branch wrote it, so it may not subtract a survivor the same commit's
correction left. Only its n-grams that also occur in a sentence
`CHANGELOG.md` itself lost count, and against that file's sentences alone,
so a gathered rewording of a lost entry still splits that entry into runs.
```
```python
def test_a_gathered_fragment_cannot_subtract_a_survivor_through_a_lost_entry(
    tmp_path,
):
    """Round 2's 🟡 1. The release rewords a live entry that quotes the claim,
    gathers a fragment quoting it verbatim, and corrects `docs/a.md`. What the
    fragment shares with the lost entry splits that entry and nothing else:
    written for every file, it subtracts the claim from `docs/a.md`'s
    corrected sentence too, and the survivor in `docs/b.md` goes silent. The
    same release without the fragment reports. Red at e6c85df6: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    quoting = f"The docs no longer say that {FOUND[0].lower()}{FOUND[1:]}"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {quoting}\n\n{older}"
            ),
            **FILLER,
        },
        "a live entry quoting the claim, a fragment quoting it, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0],
                f"{FOUND}\n\n- The docs now name the generator as its writer.",
                marker=True,
            )
            + f"\n{older}",
        },
        "release 1.0.0: reword the entry, gather the fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered text shared with the lost entry was written for every "
        f"file and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -p no:xdist` in the clone at `e6c85df6` | 103 passed, exit 0 |
| The same module, `-k` X5, with `bf7ba905`'s `survivor_check.py` swapped in, then `git checkout` | exit 1, 1 failed (X5), 102 deselected; `git status` clean after |
| Twenty shapes at the base, `bf7ba905`, the tip, the per-source fix and the set-level patch (a Python probe driving git per contract §8, deleted) | see the table below |
| The proposed case appended to the module, at the tip | exit 1, 1 failed: `exit 0` in the assertion message |
| The per-source fix plus the proposed case, whole module | 104 passed, exit 0 |
| The per-source fix with `mine -= split` removed, over the 19 release, gather and rewording cases | exit 1, 1 failed (X5), 18 passed |
| `uvx ruff check` and `uvx ruff format --check` over the fixed `survivor_check.py` and the module with the case | exit 0 and exit 0 |
| `bin/survivor-check --range 0b094396..1e2905cc` with this work item's `survivors.md` | exit 0; 31 sentences; one exempt row, `spec.md:44` |
| `bin/evidence-check --strict .` over this report's copy in the clone | exit 0; see the proof block |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch, and it is the sealer's |

```
shape   base   bf7   tip  set-level  per-source
P6        1b    1b    1b    1b    1b
P6d       1b    1b    1b    1b    1b
H1k        0    1b    1b    1b    1b
H1         0    1b    1b    1b    1b
H1c       1b    1b    1b    1b    1b
H2k        0    1b    1b    1b    1b
H2         0    1b    1b    1b    1b
X1         0     0     0     0     0
X2         0     0     0     0     0
X3         0     0     0     0     0
X4         0     0     0     0     0
X5        1b     0    1b    1b    1b
X6         1     1     1     1     1
W         1b     0     0     0     0
Wc         0     0     0     0     0
Ww        1b    1b    1b    1b    1b
Z1         0    1b     0    1b    1b
Z2         0    1b     0    1b    1b
Z1n       1b    1b    1b    1b    1b
X5W       1b     0    1b     0    1b
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:1047` | round 1's 🟡 1 — fixed |
| round-1 | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | round 1's ⬜ 2 — answered |
| round-1 | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | round 1's ⬜ 3 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py:1054` | round 1's ⬜ 4 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:1016` | round 1's ⬜ 5 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:554` | round 1's ⬜ 6 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:810` | round 1's ⬜ 7 — deferred |
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py` | round 1's 🟢 — confirmed |
| round-1 | `tests/` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
