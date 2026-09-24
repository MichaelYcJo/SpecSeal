# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — review round 3

| Field | Value |
|---|---|
| Target SHA | 0c335744f939f4526a0de0f5a17fbb1bcd2921a7 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 550 |
| Broad gate | 34d15ce3 against 9f846733 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, a release that renames `## Unreleased` or rewords an entry writes the gathered fragments' text in `corrected`; deferred to #557 because the run ended at the reopening bound |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the last round of the run — round 2 opened two 🟡 and spent the one reopening — reviewed at 0c335744: round 2's fix range `e6783db1..9a2e200b`, the paste-ready fix to the release held count landed whole, plus f92e1595, the orchestrator's one-line mark on round 2's report. It asked whether both round-2 cases are red with 1f8cdcda's script and green at the target, what `newly_released` holds when a section is renamed with its sentences unchanged and when a release both gathers and rewords, whether round 1's pure-release case and S17/S18 still hold, and whether #555's claims about the unpinned `lost` guard are right. Anything it opened needing a fix goes to a named home rather than onto this branch.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a release that renames `## Unreleased`, or rewords an entry, loses a sentence, so every newly released sentence is written, the gathered fragments' text included, and a survivor of a correction in the same commit goes unreported | `skills/code-review/scripts/survivor_check.py:1009` | deferred #557 | executed: H1, H1k, H2 and H2k exit 0 at the target, exit 1 at `1f8cdcda` for H1 and H2, exit 1 with the fix; the base is silent too, so not a regression against 0.15.0; the unit is round 2's `New units`, and the run ended at the reopening bound, which commissions nothing |
| 🟢 | round 2's finding 1 is closed — a reworded release reports the verbatim copy | `tests/test_a_corrected_sentence_survives_elsewhere.py:2700` | verified | executed: red with the `1f8cdcda` script, exit 0 `against 2 sentence(s)`; green at the target |
| 🟢 | round 2's finding 2 is closed — a sentence in an older release no longer holds the unreleased copy | `tests/test_a_corrected_sentence_survives_elsewhere.py:2730` | verified | executed: red with the `1f8cdcda` script, exit 0 `against 0 sentence(s)`; green at the target; probe R1 (old heading renamed) reports at the target only |
| 🟢 | `newly_released` holds what the range moved; a renamed section with unchanged sentences holds nothing | `skills/code-review/scripts/survivor_check.py:557` | verified | read; executed R1 and R2 |
| 🟢 | round 1's pure-release case is still silent | `tests/test_a_corrected_sentence_survives_elsewhere.py:2658` | verified | executed at the target and with the `1f8cdcda` script |
| 🟢 | phase 5's S17 and S18 at the target | `tests/test_a_corrected_sentence_survives_elsewhere.py:2888` | verified | executed; `9a2e200b` does not touch `whole_range` |
| 🟢 | the gate row, ledger row F1 and `only_released`'s docstring match the code as written | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/plan.md:170` | verified | read; the wrong allow they understate is 🟡 1's, and its fix makes them true |
| 🟢 | `f92e1595`'s marker is on the prose line that names the probe file | `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/rounds/round-2-report.md:393` | verified | read; `evidence-check --strict .` run in the clone with this report copied in |
| carried | the `lost` guard is load-bearing and no case pins it | `skills/code-review/scripts/survivor_check.py:1009` | deferred #555 | already deferred in round 2's fix pass; executed: guard removed, the module `96 passed` and P6 exit 0; the body's "keeps a gathered release's text out" needs the H1/H2 qualification |
| carried | round 1's ⬜ 5 — local-mode `OWNER_DIR` | `skills/code-review/scripts/survivor_check.py:1182` | deferred #554 | already deferred in round 1; untouched by `9a2e200b` |
| carried | round 1's ⬜ 4 — one blob read twice | `skills/code-review/scripts/survivor_check.py:781` | answered | answered in round 1; untouched by `9a2e200b` |
| ❓ | the full suite, `ruff check .`, `ruff format --check .` | the tree at the reviewed HEAD | ❓ out of verified scope | `agent-contract` §2: the sealer's, after the rounds settle; answered by the sealer |

## Paste-ready fixes

```diff
@@ def corrected(root, a, b):
     released splits the removed sentence into the runs it no longer shares,
     and withholding it would merge them into one that never clears the
-    floor. A release that removes no live sentence writes nothing, which
-    keeps a gathered release's text out of `written`."""
+    floor. A gathered fragment's text is held and never written, because
+    the fragment's own branch wrote it, not this range: a release that
+    renames `## Unreleased` or rewords an entry loses a sentence, and
+    the gathered wording would then subtract the survivor a correction
+    in the same commit left standing in another file (round 3's 🟡 1).
+    A release that removes no live sentence writes nothing at all."""
     names = git(root, "diff", "--name-only", "--no-renames", "-z", a, b)
     if names is None:
@@ def corrected(root, a, b):
     before = read_blobs(root, a, paths)
     after = read_blobs(root, b, paths)
+    # A gathered fragment's text stands under a version heading at `b`, and
+    # this range did not write it -- the fragment's own branch did. Read at
+    # `a` by the path the gatherer globs, which the release does not delete,
+    # so `moved` below can hold that text without writing it.
+    fragments = [f"seal/specs/{item}/changelog.md" for item in sorted(gathered)]
+    shipped = {
+        sentence.key
+        for path, text in read_blobs(root, a, fragments).items()
+        for sentence in sentences(path, text)
+    }
     gone, written = [], set()
     for path in paths:
@@ def corrected(root, a, b):
             # section's wording could split; a gathered release writes none.
             moved = []
+        # Held above like any released sentence, never written: a release
+        # that renames `## Unreleased` or rewords an entry loses a sentence,
+        # and the gathered text would then subtract the survivor a
+        # correction in the same commit left standing in another file.
+        moved = [sentence for sentence in moved if sentence.key not in shipped]
         old = Counter(s.key for s in was)
         fresh = Counter()
```
```python
def test_a_release_that_renames_unreleased_and_gathers_still_reports(tmp_path):
    """Round 3's 🟡 1. The release renames `## Unreleased` to a version and
    gathers a fragment into the same section, and the same commit corrects
    `docs/a.md`. The renamed heading is a lost sentence, so the moved
    section's fresh wording is written -- and the gathered fragment's text,
    which quotes the old wording, must not be written with it, or it
    subtracts the survivor standing in `docs/b.md`. The fragment stays, as
    the gatherer leaves it. Red at 0c335744: exit 0, `against 2
    sentence(s)`."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    entry = "The frobnicator now rejects a negative width with a plain message."
    older = "## 0.9.0 — 2025-01-01\n\n### Fixed\n\n- An older entry.\n"
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{FOUND}\n",
            "docs/b.md": f"# b\n\nQuoted here: {FOUND}\n",
            FRAGMENT: f"### Fixed\n\n- {FOUND}\n",
            "CHANGELOG.md": (
                f"# Changelog\n\n## Unreleased\n\n### Fixed\n\n- {entry}\n\n{older}"
            ),
            **FILLER,
        },
        "an unreleased entry, a fragment quoting the claim, two documents",
    )
    head = build(
        repo,
        {
            "docs/a.md": f"# a\n\n{REPAIRED}\n",
            "CHANGELOG.md": changelog(
                RELEASED_HEADINGS[0], f"{FOUND}\n\n- {entry}", marker=True
            )
            + f"\n{older}",
        },
        "release 1.0.0: rename Unreleased, gather the fragment, correct docs/a.md",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, (
        "the gathered fragment's text was written back with the renamed "
        f"section and subtracted the survivor in docs/b.md; exit {code}\n{text}"
    )
    assert "docs/b.md" in text, text
```
```text
... and where the file lost a sentence the released wording is written as
any file's is, except a gathered fragment's, which is held and never
written: the fragment's own branch wrote it, not this range.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `0c335744` | 96 passed in 44.27 s, exit 0; the four real-range cases included |
| the two round-2 cases, round 1's pure-release case, S17, S18, with `1f8cdcda`'s script swapped in (restored with `git checkout`, `git status` clean) | 2 failed (exit 0 at `against 2`, exit 0 at `against 0`), 3 passed |
| the same five at the target | 5 passed |
| probe `test_tmp_round3_probe.py` (NAME NOT IN TREE), deleted after: shapes P6, H1, H1k, H1c, H2, H2k, R1, R2 against the scripts at `0c335744`, `1f8cdcda`, `9f846733`, the target with the guard removed, and the target with the fix | the table under 🟡 1; R1: target exit 1 `docs/a.md:3`, `1f8cdcda` and base exit 0; R2: exit 0 everywhere, `against 1 sentence(s)` (the renamed heading line) |
| the module with `if len(gone) == lost:` replaced by `if False:` | 96 passed, exit 0 |
| the new case at `0c335744` | 1 failed: exit 0, `against 2 sentence(s)` |
| the fix below applied: the module plus the new case | 97 passed in 49.10 s, exit 0 |
| the fix applied: `uvx ruff check` and `uvx ruff format --check` on `survivor_check.py` and the test module | all checks passed; 2 files already formatted |
| `bin/evidence-check --strict .` in the clone with this report copied in | exit 0; records arm: 1 work item read, 171 names read, 0 refused |
| `bin/test tests/test_no_real_identifiers.py -q` in the clone with this report staged | 5 passed, exit 0 |
| full suite, `ruff check .`, `ruff format --check .` (the broad gate) | not yet: no run has happened; the sealer's, once the rounds settle |

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
| round-2 | `skills/code-review/scripts/survivor_check.py:981` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_a_corrected_sentence_survives_elsewhere.py:2658` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/survivor_check.py:1404` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/survivor_check.py:781` | round 2's carried — answered |
| round-2 | `skills/code-review/scripts/survivor_check.py:1182` | round 2's carried — deferred |
| round-2 | `tests/test_a_corrected_sentence_survives_elsewhere.py:2822` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/survivor_check.py:918` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/survivor_check.py:1343` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/survivor_check.py:943` | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a release that renames `## Unreleased`, or rewords an entry, writes the gathered fragments' text and silences a survivor (this round's 🟡 1) | #557, filed by the orchestrator beside #555 in `backlog: gates & hooks`, carrying the fix and the case below | the repository owner, who schedules #555 |
| the `lost` guard is load-bearing and no case pins it | #555, already deferred in round 2's fix pass; its body needs the H1/H2 qualification | the owner of #555 |
| in local mode `OWNER_DIR` names an owner `changed` can never contain (round 1's ⬜ 5) | #554, already deferred in round 1 | the owner of #554 |
