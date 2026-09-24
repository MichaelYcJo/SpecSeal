# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — round 3 report

Verifying round, and the last round of the run. Target SHA `0c335744`, base
`release/v0.15.1` (`9f846733`). The surface is round 2's fix range
`e6783db1..9a2e200b` (one commit) plus `f92e1595`, the orchestrator's
one-line marker in `rounds/round-2-report.md:393`. I worked in a
`git clone --no-local` at the target under the round's scratch directory.
Narrow runs only: the module, single cases with `1f8cdcda`'s script swapped
in, and one throwaway probe. The broad gate is the sealer's.

Round 1's and round 2's coordinates were carried from `round-1.md`,
`round-2.md` and `round-2-report.md` and opened, not re-found. Every verdict
the fix touched was re-derived at the target.

## Summary

Round 2's two fixes hold at their own coordinates. Both new cases are red
with `1f8cdcda`'s script and green at the target. `newly_released` holds what
the range moved and nothing an older release already carried. A renamed old
version heading now reports the reworded unreleased copy, where
`1f8cdcda` and the base were both silent.

One new 🟡 sits inside the unit round 2's fix created. The `lost` guard asks
whether `CHANGELOG.md` lost *any* sentence, and when it did, every newly
released sentence is written, a gathered fragment's text included. Two
ordinary release shapes trip it:

- **The release renames `## Unreleased`.** The heading line is a one-word
  sentence. It has no n-grams and can never be a source, but it counts as
  lost.
- **The release rewords an entry as it gathers.** That reword is exactly
  what round 2's 🟡 1 fix exists to write.

In either shape the gathered text subtracts the survivor that a correction
in the same commit left standing in another file, and the sweep exits 0.
`1f8cdcda` reported both. The release base `9f846733` was silent in both,
so against 0.15.0 this is the P6 silence left open in two shapes rather than
a new one. Against round 2's target it is a regression, and round 2's fix
made it.

The run ended at the reopening bound, which commissions nothing, so the
finding is deferred to a named home. A fix and a case are below, both
executed.

## Findings

### 🟡 1 — a release that renames `## Unreleased`, or rewords an entry, writes the gathered fragments' text and silences a survivor

`skills/code-review/scripts/survivor_check.py:1009` (`corrected`, the
`if len(gone) == lost:` guard), with `newly_released` at `:557` feeding it.

**What is wrong.** Round 2's fix writes the newly released sentences into
`written` whenever the file lost a sentence, so that a reworded entry splits
the removed sentence into its runs. The guard it added keeps a gathered
release's text out of `written` only when `CHANGELOG.md` lost nothing. But
`newly_released` returns everything that arrived under a version heading,
and that includes the text a gather wrote from `seal/specs/<id>/changelog.md`.
That text was written on the fragment's own branch, not by this range.

Two shapes make the file lose a sentence:

- **A release that renames `## Unreleased` to a version heading.** The
  `## Unreleased` line itself is counted as removed. Probe R2 shows this in
  isolation: a pure rename, nothing else changed, reads `against 1
  sentence(s)`.
- **A release that rewords any live entry**, which is the case round 2's
  🟡 1 was about.

In both, every gathered sentence reaches `written`. Where a fragment quotes
the wording that a correction in the same commit removed, the survivor's
n-grams are subtracted from `wanted` and nothing is reported.

**Executed** (probe, throwaway repositories; exit codes read directly):

| Shape | target `0c335744` | `1f8cdcda` | base `9f846733` | the fix below |
|---|---|---|---|---|
| P6: gather, no `## Unreleased`, `docs/a.md` corrected, `docs/b.md` quoting | 1, `docs/b.md:3` | 1 | 0 | 1 |
| H1: the same, and `## Unreleased` renamed to `## 1.0.0`, entry verbatim | **0**, `against 2` | 1 | 0 | 1 |
| H1k: H1 with the fragment left in place, as the gatherer leaves it | **0**, `against 2` | not run | not run | 1 |
| H1c: H1 with `## Unreleased` kept and the version inserted below | 1 | 1 | 0 | 1 |
| H2: `## Unreleased` kept, the entry reworded as it is released | **0**, `against 2` | 1 | 0 | 1 |
| H2k: H2 with the fragment left in place | **0**, `against 2` | not run | not run | 1 |

**Why it matters.** The sweep's job at a release commit is to report a
survivor of a correction made in that commit. H1 is the keep-a-changelog
release shape of a repository that lets entries accumulate under
`## Unreleased`, which is the shape the heading-based reading was chosen for.
The docstring at `:964` says a release that removes no live sentence writes
nothing, "which keeps a gathered release's text out of `written`". That is
true as worded, but a renamed heading is a removed live sentence, so a reader
takes the sentence as covering a case it does not cover. The gate row at
`plan.md:170` and ledger row F1 state the wrong allow as only "a live
`CHANGELOG.md` sentence that this range wrote, identical, under a version
heading". In H1 and H2 the gate also allows a survivor in another document.

**Would the release ship a defect if this stands?** Yes, a silencing one in
the two shapes above, so 🟡. It is not 🔴, because nothing is lost from a
record and nothing crashes. This repository has no `## Unreleased` section,
so its own releases do not reach H1.

**Ownership.** The guard and `newly_released` are round 2's `New units`
(`9a2e200b`), so by `docs/review-chain-spec.md` §*The cap bounds rounds, and
not the fixes of the round it stopped* the unit is the branch's. The run
ended at the reopening bound, and that bound's terminal record "commissions
nothing". So I record it as `deferred #557`, and the orchestrator
applies that test.

**The fix** (paste-ready, below) reads the gathered fragments at `a` by the
path the gatherer globs. It does not use the range's path list, because
`gather_changelog.py` does not delete a fragment (its docstring: `settle`
retires the work items later). It then drops their sentences from `moved`
before anything is written. They are still held, because `counted` is built
before the filter. Executed with the fix applied in the clone: the module
plus the new case gave `97 passed`, `ruff check` and `ruff format --check`
on both files passed, and every probe shape above reported.

**Its cost.** One more `read_blobs` batch per run, one path per marker in
`CHANGELOG.md`, most of them absent at `a`.

**Class (contract §12).** The class is text that arrives under a version
heading without this range having written it. A gather is the one mechanism
in this tree that writes such text: `gather_changelog.py` concatenates
fragments and writes the marker. A fragment that is copy-edited as it is
gathered no longer matches its fragment's keys. It is then written, as
wording the range did write. A fragment created and gathered inside the same
range is absent at `a`, so it is written too. Both results are deliberate.

## Round 2's findings, re-derived at the target

- **🟡 1 (reworded release): closed.** `tests/test_a_corrected_sentence_survives_elsewhere.py:2700`
  is red with `1f8cdcda`'s script swapped in (exit 0, `against 2
  sentence(s)`) and green at the target. It holds for the shape it pins. H2
  above is a sibling shape, a reword alongside a gather, which the same
  write-back silences. That is 🟡 1 of this round, not a reopening of round
  2's.
- **🟡 2 (older release held the unreleased copy): closed.** `:2730` is red
  with `1f8cdcda`'s script (exit 0, `against 0 sentence(s)`) and green at
  the target. Probe R1 renames the old heading (`## 0.9.0` to `## 0.9.1`,
  sentences unchanged) and rewords the unreleased copy. The target reports
  `docs/a.md:3`, while `1f8cdcda` and the base are silent. So a renamed
  section with unchanged sentences holds nothing, which is right.
- **`newly_released`, read.** It counts per sentence key, so a sentence
  repeated in an older release and moved in this range is held once. A
  renamed version heading contributes only its own heading line. A version
  renamed back to `## Unreleased` releases nothing, and its sentences become
  live and are written like any added text.
- **Round 1's pure-release case** (`:2658`) is green at the target and green
  with `1f8cdcda`'s script. **S17/S18** (`:2888`, `:2910`) are green at both.
- **Paperwork.** `only_released`'s docstring, the gate row at `plan.md:170`
  and ledger row F1 describe the code as written. The widened wrong allow is
  🟡 1's, and its fix makes the rows true as they stand. `f92e1595`'s marker
  sits on the prose line that names the probe file, outside any fence.

## #555 (already deferred), checked

At the target its claims hold. With the guard replaced by `if False:`, the
whole module stays green (`96 passed`, executed), and P6 goes from exit 1 on
`docs/b.md:3` to exit 0 (executed). One correction to its body: "the guard
keeps a gathered release's text out of `written`" holds only when
`CHANGELOG.md` loses nothing. H1 and H2 are the shapes where it does not,
which is this round's 🟡 1. If 🟡 1's fix lands, the fragment filter rather
than the guard is what keeps P6 reporting. A case planted for #555 would then
have to be seen red against the filter. That consequence is read from the
code, not executed.

## Regression tests to plant

- `tests/test_a_corrected_sentence_survives_elsewhere.py`, beside the two
  round-2 release cases: `test_a_release_that_renames_unreleased_and_gathers_still_reports` (NAME NOT IN TREE),
  the H1k shape. Seen red at `0c335744` (exit 0, `against 2 sentence(s)`)
  and green with the fix. It is in the paste-ready fixes.
- The H2 shape, the same fixture with `## Unreleased` kept and the entry
  reworded, is worth a second case, and #555's P6 case belongs next to both.

## Facts for the evidence ledger

- F1's claim would gain one clause once the fix lands: a gathered
  fragment's sentences are held and never written. Anchor it on
  `corrected` and the new case. Nothing to add at the target, because F1
  describes the code as it stands.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a release that renames `## Unreleased`, or rewords an entry, writes the gathered fragments' text and silences a survivor (this round's 🟡 1) | #557, filed by the orchestrator beside #555 in `backlog: gates & hooks`, carrying the fix and the case below | the repository owner, who schedules #555 |
| the `lost` guard is load-bearing and no case pins it | #555, already deferred in round 2's fix pass; its body needs the H1/H2 qualification | the owner of #555 |
| in local mode `OWNER_DIR` names an owner `changed` can never contain (round 1's ⬜ 5) | #554, already deferred in round 1 | the owner of #554 |

## Paste-ready fixes

### 🟡 1 — `skills/code-review/scripts/survivor_check.py`, `corrected`

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

### 🟡 1 — the case, `tests/test_a_corrected_sentence_survives_elsewhere.py`, after `test_a_sentence_in_an_older_release_does_not_hold_the_unreleased_one`

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

### 🟡 1 — the clause for `plan.md:170` and ledger row F1, once the fix lands

```text
... and where the file lost a sentence the released wording is written as
any file's is, except a gathered fragment's, which is held and never
written: the fragment's own branch wrote it, not this range.
```

Needs a fix: yes — 🟡 1, a release that renames `## Unreleased` or rewords an entry writes the gathered fragments' text in `corrected`; deferred to #557 because the run ended at the reopening bound
Loses a record or crashes: no

## Proof block

Opened at `0c335744` or the named revision:
`skills/code-review/scripts/survivor_check.py` (lines 494-578, 669-760,
799-830, 397-410, 904-1020), `tests/test_a_corrected_sentence_survives_elsewhere.py`
(lines 85-110, 444-470, 530-545, 2155-2170, 2570-2830 and the diff of
`9a2e200b`), `seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/rounds/round-1.md`,
`rounds/round-2.md`, `rounds/round-2-report.md` (head),
`seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/plan.md:170`,
the word diff of `seal/ledger.md` and the work item's ledger fragment over
`e6783db1..9a2e200b`, `docs/review-chain-spec.md` §*The cap bounds rounds,
and not the fixes of the round it stopped*, `.github/scripts/gather_changelog.py`
(docstring), `CHANGELOG.md` (head), issue #555's body.
The probe and every throwaway repository it built were deleted; the clone is
deleted after the evidence check.
