# 1788789330-the-update-notice-names-the-expensive-move — review round 2

| Field | Value |
|---|---|
| Target SHA | 279628b |
| Ran by | warden on claude-opus-5 |
| PR | 233 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none. `notice(have, want)` is untouched by the fixes; what changed is three sentences of documentation and the assertion body of one existing case |
| New units | none. `db5b9cd` adds no function and no mechanism — it extends `test_the_warning_names_the_cheap_move_before_the_expensive_one`, corrects the docstring of the case beside it, and edits `README.md:182`, `README.md:325` and `README.ko.md:317` |
| Needs a fix | yes — findings 1 and 2 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of `1788789330-the-update-notice-names-the-expensive-move` (ticket #134, PR #233), at target `279628b`, base `86e140f`. The verifying round: round 1's seven findings were answered by a fix pass in three commits, and the diff `d36735e..279628b` is what this round was pointed at.

Round 1's verdicts were inherited rather than re-litigated. The fix pass's own re-enumeration claimed five more unscoped surfaces the report had not reached, four of them shapes round 1 had predicted — including a Korean paragraph carrying the scope in the NEXT sentence, which is the defect one clause over inside the fix for the first one. That record was to be treated as a claim to check, not as a result.

Three axes were named. Whether the re-enumeration actually closed its own class, re-derived by construction rather than read off the claim — grep the distinguishing terms of every changed sentence across the rest of the corpus and report the survivors. Every other translated or paired passage this work item touches, for the same one-sentence-late shape. And whether the notice now names the cheap move correctly, verified against what the repository actually measured at its coordinate rather than against the fix record's summary of it.

The standing reason for the axis: this repository has seven measured instances of a fix pass's own commit producing the next round's finding, and this work item had already produced one of them, so the shape was live here rather than hypothetical.

The report was to be written to a file under the work item, finding ids bare integers, and `Loses a record or crashes` to carry `no` or `yes — <what>` and nothing else.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The by-hand comment points below at an instruction that is above, in both editions | `README.md:325` | open | Read. The load paragraph is at `README.md:314-319` and `README.ko.md:305-311`, above the fenced block in both; `changelog.md:35` calls it *the paragraph above them*. Sibling: `README.ko.md:317` |
| 2 | The rewritten case pins each axis by word presence, so a positive claim about the third axis and a false clause in the reload's own sentence both stay green | `tests/test_version_check.py:117` | open | Executed. M6 and M7 survived the shipped assertion body; the scope-dropped and axis-deleted controls were killed. The proposed addition kills all four |
| 3 | `README.md:182` still describes the banner as one line; it is four. Round 1's finding 3 is recorded `fixed` on two of its three counts | `README.md:182` | open | Read. `notice((0,7,1),(0,8,0))` returns 4 lines; the same claim is absent from `README.ko.md:178`; pre-existing at `86e140f` |
| 4 | The notice's scope qualifier, in every user-facing surface | `hooks/version-check.py:154` | answered | Executed. Round 1's finding 1 is closed — the qualifier is inside the claim's sentence in all four surfaces, and the two that already had it are unchanged |
| 5 | `spec.md`'s enumeration arithmetic | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | answered | Executed. 37 lines re-derived at `86e140f`; 15 in class and 22 out reconcile row by row against the table as it now stands |
| 6 | The banner's length against `plan.md`'s short form | `hooks/version-check.py:148` | answered | Executed. 620 characters, lines `[53, 107, 197, 260]` — the fix record's figures are exact |

## Paste-ready fixes

```bash
claude plugin update specseal@specseal   # then load it — see above
```
```bash
claude plugin update specseal@specseal   # 그다음 적용 — 위 문단 참고
```
```python
    # A required phrase cannot see an ADDED clause. Round 2 ran the assertions
    # above against two mutations that carry every word they look for and still
    # tell a user the reload picks up the new install:
    #   the reload's claim + `and out of the one you just installed`
    #   the gap: `hooks or agent definitions is unmeasured, BUT the version you
    #            just installed is picked up`
    # Both were green. So pin the negative too: wherever a sentence puts the
    # reload beside the newly installed version, the negation has to govern the
    # whole sentence rather than the clause before the comma.
    for where, sentence in (("the reload's claim", reload_claim), ("the gap", gap)):
        if "install" not in sentence:
            continue
        assert any(
            negation in sentence
            for negation in ("nobody", "not measured", "unmeasured", "no one")
        ), (
            f"{where} names the newly installed version without saying that "
            "pairing is unmeasured, which is the claim run 6 does not support"
        )
        assert not any(
            adversative in sentence
            for adversative in (" but ", " however", " though ", " except ")
        ), (
            f"{where} carries an adversative after its negation, so the "
            "negation governs only part of the sentence and the clause after "
            "it hands an axis back as a positive claim"
        )
```
```
shows a short notice naming `/specseal:update` and the two moves that load a release
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_tmp_round2_gap_mutations.py -q` — the shipped case's assertion body verbatim against two new mutations and two controls | exit 1, `2 failed, 3 passed`. **M6 (third axis handed back after an adversative) and M7 (false clause added to the reload's own claim) SURVIVED.** Controls killed: scope qualifier dropped, third axis deleted. Sanity case on the real notice green. Probe deleted |
| `bin/test tests/test_tmp_round2_proposed_pin.py -q` — the same body plus the addition in the paste-ready fix below | exit 1, `4 failed, 1 passed`. All four mutations killed — M6 on the adversative assertion (`:48`), M7 on the unmeasured-pairing assertion (`:41`) — and the shipped notice still passes. Probe deleted |
| `bin/test tests/test_version_check.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py -q` | exit 0, `48 passed` |
| `python3 -c` calling `notice((0,7,1),(0,8,0))` on the module at `279628b` | 620 characters, 4 lines, `[53, 107, 197, 260]` |
| `git grep -ciI 'restart' 86e140f` · `git grep -nI '재시작' 86e140f` · `git grep -niI 'reload' 86e140f \| grep -vi preload`, deduplicated by `file:line` | 33 · 3 · 2 → **37 distinct**. All three 재시작 hits are in `README.ko.md`; the experiment's Korean edition is removed by `grep -vi preload`, which is what `spec.md` row 19 claims |
| `bin/evidence-check .` | exit 0. `seal/ledger/1788789330-….md` → `12 ok · 0 drifted · 0 broken`. The fix pass's recomputed anchors are current |
| `uvx ruff check` · `uvx ruff format --check` on `hooks/version-check.py` and `tests/test_version_check.py` | exit 0, `All checks passed!`, `2 files already formatted`. The two changed Python files only — not a repository-wide lint |
| `grep -c '하십시오' README.ko.md` · `git grep -nI 'see below' README.md` · `git grep -nI '아래 참고' README.ko.md` | 0 · `README.md:325` · `README.ko.md:317` |
| `git rev-parse HEAD` · `git status --porcelain` | `279628beaf6759a61320ea79148cfdabe5ac6f1f`, tree clean before and after the probes |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/version-check.py:154` | round 1's 1 — open |
| round-1 | `tests/test_version_check.py:96` | round 1's 2 — open |
| round-1 | `hooks/version-check.py:148` | round 1's 3 — open |
| round-1 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | round 1's 4 — open |
| round-1 | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/overview.md:21` | round 1's 5 — open |
| round-1 | `hooks/ledger-migrate.py:4` | round 1's 6 — open |
| round-1 | `README.ko.md:310` | round 1's 7 — open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `/reload-plugins` reaches hooks, agent definitions, or a newly installed version | `overview.md` §*Not verified*; the settling method is at `skills/update/SKILL.md` §5 | the repository owner |
| How the four-line `systemMessage` renders in a real session-start banner | `overview.md` §*Not verified* | the orchestrator, on the first session after this ships |
| The `141 cases` figure in `round-1-fixes.md` — an aggregate rather than a coordinate, so `agent-contract` §5 says it is a claim nobody has opened. The class boundary it rests on (evidential claim against diagnostic output) is a judgment, not a count | round 1's fix record | the orchestrator. Nothing in this round turns on it |
