# 1788272986-the-fixes-are-what-open-the-next-round

Rows for the work item that closed #57.

## The fix surface is a row the pull-request check refuses to lose

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A record of a work item begun on or after the cutoff needs `Contract changes` and `New units`, and a changed unit is listed with its reach | `skills/code-review/scripts/chain_check.py#fix_surface@de2adbfb` | **Executed** — `tests/test_the_fixes_name_their_surface.py`: a missing row fails naming what it buys, a `;`-separated entry with no `→`/`->` (or an empty half) fails naming the entry, an empty cell fails on any record, and a commented row is not the row | 2026-09-01 | Read on every record, like `Fixes checked by`, because every round has its own fixes. Only the ABSENT row is grandfathered — a malformed one is always the author's to fix |
| `none` is an answer in both rows, with or without a reason after a separator | `skills/code-review/scripts/chain_check.py#says_none@101cad37` | **Executed**: `none`, `` `none` — the fixes changed no signature `` and `none, nothing added` pass; `nonempty` would not — the boundary is a separator, matched as a prefix the way `verdict_of` matches its vocabulary | 2026-09-01 | `none — the fixes are not yet written` is the honest mid-run value, which is why the draft excuse is not needed here |
| Records of work items begun before `SURFACE_FROM` print rather than fail | `skills/code-review/scripts/chain_check.py#SURFACE_FROM@e8df3db3` | **Executed**: the same missing rows on a `1787700000` item exit 0 with a notice per row, a no-timestamp item is excused too, and the item at the cutoff second is held to the rule (`>=`, read from the module so a moved cutoff moves the case) | 2026-09-01 | The value is this work item's own id, so the first item held to the rule is the one that wrote it — the property `STRICT_FROM` already has. Every existing record in this repository predates it; none was edited |

## What round 1 settled

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| An unreadable round record cannot read as "no rows required" | `skills/code-review/scripts/chain_check.py#fix_surface@de2adbfb`, `skills/code-review/scripts/chain_check.py#main@fd1525ae` | **Executed** (round 1's probe): a garbage record exits 1 — `fix_surface` returns nothing for it, and `checked_by` errors on the same record in the same loop, so the silence is never the whole answer | 2026-09-02 | Merged from round 1's evidence-todo |
| The decode-failure fail-open class cannot reach `chain_check.py` | `skills/code-review/scripts/chain_check.py#git@0d87d1f9` | Read: `git()` pins `encoding="utf-8", errors="replace"`, so the locale-decode → `None` → silent-allow path `tests/test_gates_do_not_fail_open.py` covers in hooks is unconstructible here | 2026-09-02 | Round 1's 🟡 2, answered — the state that file pins cannot be built against this reader |
| A cell of only separators is refused in both fix-surface rows | `skills/code-review/scripts/chain_check.py#fix_surface@de2adbfb` | **Executed**: `\| ; \|` and `\| — \|` on a post-cutoff item exit 1 naming both rows — `tests/test_the_fixes_name_their_surface.py::test_a_cell_of_only_separators_is_not_an_answer`, seen red against the unguarded loop first | 2026-09-02 | Round 1's 🟡 1. Re-anchored from the pre-fix claim ("passes") to the refusal that closed it |

## The review-skill rules the same measurement bought

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The verifying round treats what `New units` names as a finding surface, not a verification surface | `skills/code-review/SKILL.md#"## Orchestrator: the run ends with a verifying round"@e62eadae`, `agents/warden.md#"## Role">"judge them as code — *is this correct* — never as fixes. A finding there is"@98a430c2` | Read, pinned by `test_the_fixes_name_their_surface.py` with the inverted spellings refused beside the sentences | 2026-09-01 | Without the exemption, *answers rather than new findings* tells the reviewer to skip the one set of units nobody has reviewed — round 4's fix commit created eight, four defective |
| The axes table carries a security row, and a paste-ready fix at an OS boundary states its assumed precondition | `skills/code-review/SKILL.md#"## Comparison axes"@1c5f6051`, `skills/code-review/SKILL.md#"## Findings format"@6d56ea73` | Read, pinned by `test_review_axes.py` (the row and its probes) and the new test file (the sentence and the five boundary premises) | 2026-09-01 | Security was named in stage 2 and absent from the table, and the table is what makes an axis mandatory |
