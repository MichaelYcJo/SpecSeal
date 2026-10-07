# 1791270164-the-release-seal-is-drawn-in-curves — review round 2

| Field | Value |
|---|---|
| Target SHA | bf1a944776e4de1ecf2ab238e4e4b04d9d7baaa4 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #859 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (`test_only_neutral_domains` red on three legs), 🟡 2 (`apt-get update;` under `bash -e`) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of #832 is the verifying round for round 1's fixes at `99bcad40..092004bb`, which include the merge f6d39425 of `origin/release/v0.20.0`. It reviewed at bf1a9447, the push that gave PR #859 its first CI.

The reviewer was asked to open each fix and to treat round 1's `New units` as a finding surface. In particular it judged:
- the merge's resolution of the 1791270161 and 1791270165 fragments;
- whether the green-cell guard closes its class;
- whether the grown pair case holds under any mark chart;
- `utf-8-sig`;
- `apt-get update;`.

It also read every workflow of `gh pr checks 859` once each had finished. It did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `test_only_neutral_domains` is red on the ubuntu, macOS and Windows group 2 legs: the release SVG and its case carry the SVG namespace host, which `ALLOWED_DOMAINS` does not hold | `.github/scripts/release-seal.svg:1` | open | executed: the three legs' logs, 1 failed each, the same two lines; reproduced in the clone, exit 1; with the namespace's domain allowlisted, 5 passed. Phase 8's line, not a fix of a fix |
| 🟡 2 | Round 1's ⬜ 8 is not closed: the step runs under `bash -e`, so `apt-get update;` still ends it at a failed refresh, and the comment, the case, ledger W3 and an overview row say it does not | `.github/workflows/publish-release.yml:114` | open | executed: `bash -e` stops at `false;`, and `\|\| true` runs the next command; the proposed assertion is red against today's step and green with the fix. read: the PR's own job logs `-e` as its shell |
| ⬜ 3 | `spec.md` ends with a `Reframed` line that names no round, so `chain_check` refuses the foot and the `release` job is red | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:419` | open | a correction: executed, the job's log; the fence committed in the clone clears that refusal |
| ⬜ 4 | `round-1.md`'s `New units` row lists 109 units the merge brought, and `Contract changes` the merge's contracts | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | open | a correction: executed, 109 of 111 are defined at `559977a3`; the two others are the fix pass's cases |
| 🟢 | round 1's blocking finding is closed — the merge made the pull request mergeable, CI ran, and every row the release branch changed survived | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:1` | confirmed | executed: the four-point row probe; the six rows both sides changed differ from the release branch's only in the re-stamped SKILL.md anchor; `correction-check` exit 0 over two ranges; `evidence-check --strict` 0 drifted |
| 🟢 | round 1's 🟡 2 is closed, and so is its class: every styled cell beside the disc | `skills/verify/scripts/seal_stamp.py:492` | confirmed | executed: the case red with the guard reverted; a probe over 246 row sets at 0.90 and with no disc, every text cell shown as drawn |
| 🟢 | round 1's 🟡 3 is closed under any chart `read_chart` accepts | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:321` | confirmed | executed: green under seven charts, among them a checkerboard whose small stamp is 7,728 units |
| 🟢 | round 1's 🟡 4 is closed | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:553` | confirmed | executed: red with `RESET` padded by 300 spaces; green at the target and under seven charts |
| 🟢 | round 1's 🟡 5 is closed | `skills/verify/scripts/seal_stamp.py:514` | confirmed | executed: three parameters red with the fix reverted; read: `TITLE_RED` is no `KEY` colour |
| 🟢 | round 1's ⬜ 6 is closed | `hooks/sealer-stamp.py:41` | confirmed | read: *never smaller*; *the sheet* only where a case says it was retired |
| 🟢 | round 1's ⬜ 7 is closed | `skills/verify/scripts/seal_stamp.py:332` | confirmed | executed: the BOM copy red with the reader reverted; the encoding and line-reader modules, 305 passed |
| ❓ | The 109 units the merge brought, as code | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | ❓ out of verified scope | not reviewed here: they are #849's, #851's and #855's, reviewed at their own pull requests; the orchestrator decides whether that stands (⬜ 4) |
| ❓ | The full suite, lint and typecheck after the rounds settle | the tree at the last round's target | ❓ out of verified scope | not run (contract §2); the sealer answers, once, after 🔴 1 and 🟡 2 land |

## Paste-ready fixes

```python
ALLOWED_DOMAINS = (
    "example.com",  # the designated fixture domain — use this in examples
    "github.com",
    "arxiv.org",
    "claude.com",  # official docs this plugin is built against
    # The SVG namespace URI, which every SVG file carries for a renderer to
    # read it as SVG: an identifier, not an address (#832).
    "w3" ".org",
)
```
```yaml
      # dropped. `|| true` rather than `&&`: `apt-get update` exits non-zero
      # when any one list fails, a third-party list `librsvg2-bin` does not
      # come from included, and the install is still worth trying then. A
      # bare `;` is not enough: a step with no `shell:` runs under `bash -e`,
      # which ends the step at the failed refresh as `&&` did. Before the
      # suite, so the suite at the tag runs the one case that draws with the
      # real binary; an install that fails costs the image, and the draw's
      # `::warning::` says so.
      - name: install rsvg-convert
        continue-on-error: true
        run: sudo apt-get update || true; sudo apt-get install -y --no-install-recommends librsvg2-bin
```
```python
    The package lists are refreshed first, and the refresh does not gate
    the install: `apt-get update` exits non-zero when any one list fails,
    a third-party list the package does not come from included, so `&&`
    after it skipped an install that would have worked (round 1's ⬜ 8). A
    bare `;` skipped it too, because the step runs under `bash -e`, so the
    refresh is followed by `|| true` (round 2's 🟡 2)."""
```
```python
    run = next(line for line in held[at] if "librsvg2-bin" in line)
    assert "sudo apt-get update || true;" in run, run
    assert "apt-get update &&" not in run, run
```
```text
Both rows below sit in markdown tables, so each `|` of `||` is written `\|`.

ledger, Corrected · W3 — replace
  `sudo apt-get update; sudo apt-get install -y --no-install-recommends librsvg2-bin` (#832), the refresh not gating the install,
with
  `sudo apt-get update \|\| true; sudo apt-get install -y --no-install-recommends librsvg2-bin` (#832), the refresh not gating the install under the step's `bash -e`,
then: bin/evidence-check --reverify --into seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md --checked <today> .

overview.md, the phase 8 divergence row — its middle and right cells:
| The step runs `sudo apt-get update \|\| true; ` first — `&&` until round 1's ⬜ 8, `;` until round 2's 🟡 2 | A runner image's package lists can name a version the mirror has dropped, and that costs the image at the first tag. `\|\| true` because `apt-get update` exits non-zero when any one list fails, a third-party list included, and the step runs under `bash -e`, which ends it there after `&&` or `;` alike; the case holds the `\|\| true`. Q10 measures the step at the first tag (phase 8, rounds 1 and 2) |
```
```markdown
The frame was redrawn on 2026-10-07 by framer, after the owner's look at
phase 2's stamp.

Framed 2026-10-06 by framer, before the build.
```
```text
round-1.md, New units:
test_a_mark_leading_a_continuation_row_beside_the_disc_is_drawn_in_its_style (depth 1); test_a_half_block_in_a_value_is_text_in_the_twin (depth 1)

round-1.md, Contract changes:
none — the fix pass changed no unit's contract; the rows the generator wrote are the merge's
```

## Executed probes

| What was run | Result |
|---|---|
| `gh pr checks 859 --watch` to the end, `gh pr view 859`, at `bf1a9447` | exit 1. Pass: `lint`, `ledger`, `arm-check-grammar` 3.13 and 3.14, Windows groups 1, 3 and 4. Fail: `release`, at *a declared review chain has the round record it claimed*; pytest ubuntu, macOS and Windows group 2. None pending. `MERGEABLE`, `UNSTABLE` |
| the ubuntu, macOS and Windows group 2 job logs | `test_only_neutral_domains` the one failure on each: 12,738, 12,730 and 6,706 passed |
| `tests/test_no_real_identifiers.py` in the clone, then with the namespace's domain in `ALLOWED_DOMAINS` | exit 1, 1 failed; exit 0, 5 passed |
| a test_tmp probe: each table row of the 1791270161 and 1791270165 fragments at `6de64c19`, `96127593`, `559977a3` and `f6d39425` | no release-branch row lost; six rows both sides changed, each equal to the release branch's but for the SKILL.md anchor |
| `bin/correction-check --range 559977a3...bf1a9447` and `--range 99bcad40..bf1a9447` | exit 0 each, no correction dropped, no released ledger file changed |
| `bin/evidence-check --strict .` at the target | exit 0, 6,835 ok · 0 drifted · 0 broken |
| the hook module whole; the sealer module's stamp slice (`-k` over disc, twin, letter, text lines, SGR, title, reference, chart, ladder, budget, mark, half-block, layout); the install case | exit 0: 35 passed; 281 passed; 1 passed |
| `856aeeec`'s change to `seal_stamp.py` reverted, the three new or changed cases | exit 1: the `✓` case, three half-block cases and the chart case failed, the `·` case passed |
| `bab19faa`'s workflow change reverted, the install case | exit 1, 1 failed |
| a test_tmp probe: 246 row sets at 0.90 and with no disc, every non-blank text cell against `what_a_terminal_shows` | exit 0, 2 passed |
| the pair case and the one-file case under the S, the key, and the empty, full, checkerboard, row-stripe and column-stripe charts | 2 passed under each of the seven; the archived § refused by `read_chart` |
| a test_tmp probe: a small stamp and a real run's stamp under those charts | small: S 4,662, key 4,135, empty 3,278, checkerboard 7,728; real: S 5,254, key 4,727, empty 3,870, checkerboard 8,320 |
| `RESET` padded by 300 spaces, the one-file budget case | exit 1, on *a real run's stamp no longer fits the budget with its disc* |
| `bash -e -c 'false; echo …'` and `bash -e -c 'false \|\| true; echo …'` | exit 1 with nothing printed; exit 0 and printed |
| 🟡 2's fence in the clone, the install case; the same case against today's step | exit 0, 1 passed; exit 1, 1 failed |
| ⬜ 3's fence committed in the clone, then `chain_check.py --baseline` against `559977a3` | the `spec.md` refusal gone; the round-1 record's `nobody` and `not yet` remain |
| the survivor, correction, mode and CLAUDE.md-block steps of the `release` job, in the clone | exit 0 each |
| the encoding and line-reader hygiene modules | exit 0, 305 passed |
| the full suite, lint and typecheck | not yet — the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | PR #859 against `release/v0.20.0` at `559977a3`; `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:486` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:343` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:551` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:506` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/sealer-stamp.py:40` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:330` | round 1's ⬜ 7 — fixed |
| round-1 | `.github/workflows/publish-release.yml:111` | round 1's ⬜ 8 — fixed |
| round-1 | `.github/scripts/release-seal.svg:21` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:323` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:462` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2976` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/publish_release_note.py:393` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md:1` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:1` | round 1's ❓ — out of verified scope |
| round-1 | the tree at the last round's target | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/code-review/scripts/round_record.py`'s `touched` diffs a fix range by path and excludes no merge, so a fix range holding a merge of the base lists the merge's units as the fixes' `New units` (⬜ 4) | a new issue against the round-record generator | the plugin's owner, through an issue the orchestrator opens |
