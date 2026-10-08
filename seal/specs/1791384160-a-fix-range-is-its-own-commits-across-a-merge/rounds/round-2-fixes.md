# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — round 2 fixes

Fix range `24cfb66f..fb5ba994`, one commit. The two corrections to records
sit after it, at fadd8270, with `survivors.md` and this table in the commit
after that.

Following the orchestrator's direction, every carrier now states the rule by
what `own_commits` tests rather than by listing merge shapes. A commit is the
range's own when it is a non-merge commit that has `a` as an ancestor,
whatever branch it was made on. The shapes appear only as examples: a
sibling's squash on a base that never merged `a`, a sibling's commit made
after the base merged `a`, and an own fix on a topic forked before `a`,
before and after that topic merged `a`.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 🟡 1 | fixed | fb5ba994 — the home's ownership paragraph and limit paragraph, and the `own_commits` and `fragment_left_behind` docstrings, state the ancestry test with probes A, A2 and B2's shapes as examples |
| 🟡 2 | fixed | fb5ba994 — `skills/code-review/orchestration.md` §*And name the fix surface*, `docs/round-record-spec.md` §*A fix of a fix*, and the `fix_pass_units` and `touched` docstrings state the same test; `close`'s `fixed` refusal now names "a commit a merge brought in that was not made on top of" the start, and S6's case pins the words |
| ⬜ 3 | answered | corrected at fadd8270: `changelog.md` states the ancestry rule for `close` and the notice, and the `fixed` refusal as a commit not made on top of the start |
| ⬜ 4 | answered | corrected at fadd8270: the ledger rows S7–S9, S12 (both), `Corrected · S2, S3, S4, S6`, S1–S3, S4, S6 and `Corrected · A1` state the ancestry test, and `evidence-check --reverify` re-anchored S12's §*A fix of a fix* coordinate; `overview.md` and `phases/phase-1.md` carry the same correction |
