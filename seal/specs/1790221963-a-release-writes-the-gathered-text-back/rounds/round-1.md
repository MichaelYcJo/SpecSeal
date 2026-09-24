# 1790221963-a-release-writes-the-gathered-text-back — review round 1

| Field | Value |
|---|---|
| Target SHA | bf7ba90528c4864b0b2e94f8d01c76e457e1fc47 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 560 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `0b094396a13ebb66087534fad42a794ca33b7205..1e2905cc72ef617a93ded9678e58dab11107b04a`, 4 commits |
| Contract changes | none |
| New units | test_a_release_that_replaces_an_entry_with_a_gathered_rewording_reports (depth 1) |
| Needs a fix | yes — 🟡 1, the gathered-text filter withholds a gathered rewording of a sentence `CHANGELOG.md` itself lost, a new silence against the base |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 was asked to review the whole branch at bf7ba905 against `release/v0.15.1` (61f0d0d8): spec compliance first against `spec.md`, `plan.md` and the gate table — this sweep runs in CI's hygiene job and at every seal, so a silence is the failure direction to hunt — then quality, in a clone under the round's own directory, narrow runs only, with the smith's handoff as the account to audit: the gathered-text filter after the `lost` guard, the marker blank in `newly_released`, the six new cases and the eight mutations that isolate them, and step A's three corrected ledger rows; and to probe the six shapes step A's round 3 listed plus P6d itself.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the gathered-text filter also withholds a gathered rewording of a sentence `CHANGELOG.md` itself lost, merging its runs; a verbatim copy that reported at the base is silent at the target | `skills/code-review/scripts/survivor_check.py:1047` | **fixed** `79c791fe` | fixed at 79c791fe — and 7c419218 — of a gathered sentence's n-grams only those in a sentence this file lost are written, so a gathered rewording of a lost entry splits the removed sentence again; X5 red at bf7ba905 (exit 0, `against 2 sentence(s)`), green after; five mutations isolate X5 from G1–G6; the new bound in the module docstring, `corrected`'s docstring and the `shipped` comment, ledger H1 and F1, the changelog fragment; X5 probe: exit 1 at `61f0d0d8`, exit 0 at `bf7ba905`; the fix below trialled green (module 102 passed, X5 exit 1, the seven shapes still exit 1) |
| ⬜ 2 | the failure direction is stated as *reports more, and only there*, and over-holding as noise; finding 1 is a report less | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/plan.md:144` | answered | corrected at 7c419218 and 813a55f4 — ledger H1's note (dated `Corrected 2026-09-24`), `plan.md` and `spec.md` state the failure direction after the fix, including the one shape that still reports less than the base: a sentence removed from another file whose new wording lives only in a gathered fragment, held because the fragment's branch wrote it; paperwork correction; the same claim at `plan.md:88`, `spec.md:66` and ledger row H1's note |
| ⬜ 3 | the work item's spec, questions and plan say step A's gate row was corrected, and the overview says it was left; the row itself carries a now-false clause with no pointer | `seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md:23` | answered | corrected at 813a55f4 and 1e2905cc — `spec.md`, `questions.md` and `plan.md` say step A's gate row was left as written and this item's plan carries the row; `overview.md` says step A is squashed into `release/v0.15.1` (#550) and not yet released; one fix-range survivor excused in `survivors.md`; paperwork correction; also `spec.md:181`, `plan.md:103`; step A has no marker in `CHANGELOG.md`, so *shipped* in the overview's grounds is not true of the release |
| ⬜ 4 | a file moved whole in the range writes the corrected wording it quotes, and the survivor goes silent | `skills/code-review/scripts/survivor_check.py:1054` | deferred new issue | X1 probe: exit 0 at both ends; pre-existing; same class as this work item's ground; not #551 |
| ⬜ 5 | `a_gathered_fragment` and the held set spell the fragment's path two ways | `skills/code-review/scripts/survivor_check.py:1016` | deferred #564 | #564 — predates the branch and is unreachable here; the gathered-text class, filed by the orchestrator; X2 probe: exit 0 at both ends; unreachable here, because the gatherer globs `seal/specs/` |
| ⬜ 6 | a fragment's own `## ` heading ends the released section, and its text after it is written | `skills/code-review/scripts/survivor_check.py:554` | deferred #564 | #564 — the same issue; X3 probe: exit 0 at both ends; no fragment in the tree has one |
| ⬜ 7 | a CRLF `CHANGELOG.md` yields no gathered ids, so neither the held set nor the marker blank applies | `skills/code-review/scripts/survivor_check.py:810` | deferred #564 | #564 — the same issue; X4 probe: exit 0 at both ends; pre-existing; unreachable here (`eol=lf`) |
| 🟢 | #557's shapes report at the target: P6, P6d, H1k, H1, H1c, H2k, H2 | `skills/code-review/scripts/survivor_check.py:1047` | confirmed | executed at `bf7ba905`, each exit 1 naming `docs/b.md`; H1k, H1, H2k and H2 exit 0 at `61f0d0d8` |
| 🟢 | the guard and the filter are pinned apart, as the handoff says | `tests/test_a_corrected_sentence_survives_elsewhere.py` | confirmed | executed: guard off → G5 alone red; filter off → G1–G4 red; both off → G1–G6 red; marker blank off → G4 alone red; held set read at `b` → G2 alone red; the file restored byte-identical |
| ❓ | the six other modules that load the sweep, the four neighbouring modules, and the branch's own sweep were not re-run this round | `tests/` | ❓ out of verified scope | the handoff and the orchestrator report them green at `bf7ba905`; this round ran the module alone. Who answers it: the sealer, whose full suite covers them |

## Paste-ready fixes

```python
        held = [sentence for sentence in moved if sentence.key in shipped]
        moved = [sentence for sentence in moved if sentence.key not in shipped]
        # ...except against what THIS file lost: a live entry the release
        # replaced with a gathered fragment rewording it is still split by
        # that rewording, as a reworded release is (step A's round 2 🟡 1).
        # Only the grams the lost sentences carry are written, so gathered
        # text still cannot subtract another file's corrected wording.
        lost_here = {gram for sentence in gone[lost:] for gram in sentence.grams()}
        for sentence in held:
            written.update(gram for gram in sentence.grams() if gram in lost_here)
```
```python
def test_a_release_that_replaces_an_entry_with_a_gathered_rewording_reports(
    tmp_path,
):
    """The gathered-text filter's other side. The release replaces the live
    entry `FOUND` with a gathered fragment whose text rewords it, and
    `docs/b.md` quotes `FOUND`. The fragment's rewording is withheld from
    `written`, but it must still split the sentence `CHANGELOG.md` itself
    lost into the runs it no longer shares, as a reworded release does;
    withheld whole, `FOUND` is one run under the floor and its copy goes
    silent. Red at bf7ba905: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": "# a\n\nUnrelated.\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {REPAIRED}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {FOUND}\n\n{older}"
            ),
            **FILLER,
        },
        "a live entry, a fragment rewording it, a document quoting the entry",
    )
    head = build(
        repo,
        {
            "CHANGELOG.md": changelog(RELEASED_HEADINGS[0], REPAIRED, marker=True)
            + f"\n{older}",
        },
        "release: the live entry replaced by the gathered rewording",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered rewording was withheld whole, so the lost entry never "
        f"split and its copy in docs/b.md went silent; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `bf7ba905` | 102 passed, exit 0 |
| `uvx ruff check` and `uvx ruff format --check` over `survivor_check.py` and the test module | exit 0 and exit 0 |
| Eleven shapes at `bf7ba905` (a Python probe driving git per contract §8, deleted) | P6, P6d, H1k, H1, H1c, H2k, H2 exit 1 naming `docs/b.md`; X1 move, X2 `specs/` root, X3 `## ` fragment, X4 CRLF exit 0 |
| The same shapes at `61f0d0d8` (the base's script copied beside the target's, deleted) | P6, P6d, H1c exit 1; H1k, H1, H2k, H2 exit 0 `against 2 sentence(s)`; X1–X4 exit 0 |
| X5 (gathered rewording of a lost live entry) and X6 (the range's own rewording) at both ends | X5: base exit 1, target exit 0. X6: exit 1 at both |
| Five mutations of `survivor_check.py` over the module, restored byte-identical and asserted | guard off: 1 failed (G5). Filter off: 4 failed (G1–G4). Both off: 6 failed (G1–G6). Marker blank off: 1 failed (G4). Held set at `b`: 1 failed (G2) |
| The 🟡 1 fix applied in the clone, restored byte-identical | module 102 passed; X5 exit 1; P6, P6d, H1k, H1, H1c, H2k, H2 exit 1 |
| `bin/evidence-check --strict .` over this report's copy in the clone | exit 0; total 1777 ok, 0 drifted, 0 broken; no NOT-IN-TREE line |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it on this branch; it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 4, a file moved whole in a range writes the corrected wording it quotes (pre-existing, not introduced here) | a new issue, candidate | the repository owner, who decides whether a moved text counts as written by the range |
