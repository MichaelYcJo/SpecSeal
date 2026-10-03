# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d364dc6c |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Re-point each K5 row whose subject moved: the agent contract's §9 and §17,
both READMEs (the citation and the documents list), the `docs/round-record-spec.md`
and `docs/review-chain-spec.md` preambles, `docs/the-evidence-ledger.md` 477,
the hook and checker comments, and the four test comments. Then make
`docs/the-record-layout.md` match D9. Every K5 edit to `hooks/cmdline.py` and
`hooks/worktree-guard.py` goes in a commit of its own, last in the phase, so a
merge with #737 resolves in one place; `docs/worktree-guard-spec.md` is edited
only where the frame names a reference there.

## What this phase found

**No K5 row names `hooks/cmdline.py`, `hooks/worktree-guard.py` or
`docs/worktree-guard-spec.md` as a site to change.** K5 lists `hooks/cmdline.py`
2234 and 2384 among the references whose subject stays in the parent (an
unresolvable target, `Unresolved`), and they were left. Neither of the two
#737 files and not the guard's policy changed in this phase. The four hooks
that did change, `hooks/commit-review-gate.py`, `hooks/gate.py`,
`hooks/mode-gate.py` and `hooks/routing.py`, are in the phase's last commit,
d364dc6c, alone, which is the separation the spawn asked for applied to every
hook.

**The K5 sites changed**, by commit:

- 8e4db2f7: `skills/agent-contract/SKILL.md` §9 and §17; `README.md` and
  `README.ko.md`, the documents list and the git hooks row's citation, and the
  Korean count *세 문서* that became *다섯 문서*; the `docs/round-record-spec.md`
  and `docs/review-chain-spec.md` preambles; `docs/the-evidence-ledger.md`'s
  fold-marker statement; `skills/code-review/scripts/chain_check.py#restored_from`;
  the comments in `tests/test_chain_hooks_hardening.py`,
  `tests/test_release_hygiene.py` and twice in
  `tests/test_the_commit_gate_decides_at_the_commit.py`; and
  `docs/the-record-layout.md` per D9.
- d364dc6c: `hooks/commit-review-gate.py` three times (the comment above
  `DOC_ROOTS`, the `touches_code` docstring, the comment in `main`),
  `hooks/gate.py` twice (the module docstring, the comment above `DOC_ROOTS`),
  `hooks/mode-gate.py` and `hooks/routing.py` once each.

**D9 as built.** F1's heading and table stay, and F1 says it was built by
#727 and that the table records the decision at 233f0455. The section's
opening says four parts were decided, F1 built and three not yet. *each is
under 500 lines* became the measured 586, 254 and 250 lines. The over-target
list lost its third bullet and says two kinds. The `docs/` table narrows the
parent's question and adds the two new files in alphabetical place.

**Verified, executed.**

- The S5 probe, `test_tmp_s5_every_citation_resolves.py`, run from the
  scratchpad and deleted. It collapses each live file's whitespace (every
  tracked file except `seal/specs/`, `seal/releases/`, `seal/ledger*` and
  `CHANGELOG.md`), finds each `` `docs/<one of the three>.md` `` followed by
  `§*…*` or `under *…*`, and asks whether the cited file holds a heading that
  begins with it. Before the hook commit it named exactly the three hook
  citations of §*Review arm* by the parent's path; after it, **13 citations,
  all resolving, none naming a moved heading by the parent's path**.
- `bin/test` over 22 modules that read the documents this phase touched or
  the moved text (the agent contract, every agent, ledger rules, changelog,
  one word one meaning, line wrap, the reopening, old roots, a moved rule,
  one owner, a document naming a script, the settings' front door, both
  editions, release hygiene, hooks hardening, the fold room, enforced-by
  shape, riders, the frozen reading, the pull-request check, the direct
  answer, the waiver): 965 passed, 8 skipped. Then, with the hook edits, the
  rider, frozen-reading, hardening, routing, mode, fail-open and one-word
  modules: 270 passed.
- `python3 .github/scripts/rider_check.py --root .`: 20 ok, 0 drifted, 0
  broken.
- `uvx ruff check` and `uvx ruff format --check` over every Python file the
  phase touched: clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/the-record-layout.md`'s bullet naming the gate's policy over target | none: after the cut it is not |
| the record layout's *each is under 500 lines* | the measured counts in the same paragraph |
