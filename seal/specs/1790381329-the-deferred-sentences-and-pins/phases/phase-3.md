# 1790381329-the-deferred-sentences-and-pins — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | a80180e0 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#612. Every place in spec.md's #612 table, and any the repeated enumeration
adds, rewritten to carry the statement spec.md fixes: `git merge-base <ref>
HEAD` is the fork point on a branch checkout and the base's tip in CI, and
either way a row or file that arrived on the base after the branch was cut is
not this branch's removal. Both Korean editions written as Korean. The
documents case extended with one tip phrase per language, the finding's own
false sentence asserted absent where it stood, `unverified_check.py` joining
the list, and the case's docstring corrected.

## What this phase found

- **The frame holds; the enumeration found no twelfth place.** Searched at
  the build tip over `docs/ skills/ agents/ templates/ hooks/ .github/
  README.md README.ko.md CONTRIBUTING.md`: *fork point*, *forked from*,
  *where this branch forked*, *where you forked*, *after the fork*, *the
  fork*, *since the fork*, *after your branch was cut*, *branch point*,
  *branched off/from*, *moving tip*, *the base revision*, *merge base*,
  *merge-base*, *base's tip*, *base tip*, *merge ref*; Korean *갈라진 지점*,
  *갈라진 뒤*, *갈라*, *분기*, *현재 끝*, *병합 기준*, *베이스*, *base 끝*. 108
  lines on the first pass. Judgments of the ones that are not the eleven:
  - `docs/the-evidence-ledger.md` §*The unverified record, and the baseline
    it is read against* (*resolved once, to a merge base*): names the merge
    base without placing it. Not a twin.
  - `docs/commit-review-gate-spec.md` lines 420-427, `docs/review-chain-spec.md`
    line 692, `docs/one-root-by-lifetime{,.ko}.md`'s settle rows (*병합 기준
    커밋*), `chain_check.py`, `correction_check.py`, `survivor_check.py`: a
    merge base named without saying where it lands. Not twins.
  - `unverified_check.py#retired_by_rule` (*a CI reader's merge-base is by
    construction a commit the removal happened after*): true at the merge ref
    as at the fork. Not a twin. `base_label`'s docstring already states the
    tip in CI.
  - `settle.py`, `skills/settle/SKILL.md`, `docs/the-evidence-ledger.md`'s
    retirement paragraph, `.github/scripts/release_completeness_check.py` and
    the hygiene milestone-step comment: state both places correctly already
    (#605). Not twins.
  - `docs/release-checklist.md` step 0: true at both places, names neither.
    Kept in the case for the merge base, not held to the tip.
  - `skills/verify/scripts/broad_gate.py:536` (*the fork's stale*): a fork
    repository, not a fork point. Korean *갈라* hits in `writing-style` and
    `one-root-by-lifetime.ko.md` lines 58 and 80: unrelated senses.
- **One more false clause than the table listed.** `unverified_check.py`'s
  module docstring heading said *The base is the merge base, not the ref's
  tip*, which in CI is exactly what the merge base is. It now reads *not the
  ref*: what is refused is reading the ref itself.
- **The phrases.** English *the base's tip* and Korean *base 브랜치의 끝*, in
  every file that places the comparison. The case flattens the text (and
  drops the `#` of YAML comments) before it looks, so a phrase broken across
  a comment line still counts.
- **Seen red (§15).** The extended case against the unedited prose: 8
  failed, 1 passed (the checklist, which carries no tip phrase). After the
  prose: green. The false-sentence assertion, with the tip phrase present:
  red with *never the base branch's moving tip* put back into
  `docs/one-root-by-lifetime.md`, and red with *base 브랜치의 현재 끝이
  아니라* put back into the Korean edition; each file restored from bytes
  kept before the insertion.
- **Rows drifted and re-read.** `unverified_check.py#main` (four rows:
  0.4.0, 0.5.0 S7, 0.9.3 R1, 0.14.0 G5), `#merge_base` (0.9.3 R1),
  `#folded_items` (0.13.0 S1 and R13), and the two workflow anchors (0.4.0
  S12, 0.5.0 S5), each with a dated `Re-read` note. **0.13.0 S1's claim was
  made false by the edit** — it quoted *present at the fork point* — and is
  corrected in place with a `Corrected 2026-09-26` note. 0.13.1's row that
  hashes the whole `### 1788331011` section of `seal/releases/0.4.0.md`
  moved with those notes and was re-read and re-stamped too.
- **Verified by (executed, 2026-09-26):** `tests/test_unverified_rows_close.py`
  and `tests/test_docs_line_wrap.py`, 206 passed; then every module in
  `tests/` that reads a file this phase edited, 66 modules, 3258 passed, 7
  skipped, 2 failed — `test_every_spec_directory_that_reached_the_ladder_has_an_overview`
  (this work item had no `overview.md` yet; it has one now, green) and
  `test_this_repositorys_own_records_state_nothing_the_tree_lacks`, which
  reads `import_module` (now marked NAME NOT IN TREE) and
  `test_a_claim_split_into_two_rows_as_it_is_corrected_stays_measured`, the
  case phase 5 plants. `evidence-check .`: 0 drifted, 0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *never the base branch's moving tip* (`docs/one-root-by-lifetime.md`) and *base 브랜치의 현재 끝이 아니라* (its Korean edition) | nowhere: both were false; the sentences now name both places |
