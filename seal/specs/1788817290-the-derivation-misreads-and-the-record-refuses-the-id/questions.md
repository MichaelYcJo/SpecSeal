# the derivation misreads and the record refuses the id — questions for the planner

<!-- seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. -->

Nothing here blocked the build. The routing was answered before the first
edit, and the design decision inside #194 — literal-set comparison plus a
stated hole — was answered in the same batch and is recorded in `routing.md`.
The two rows below are assumptions stated in writing because a different
answer would not have changed what was built, and one row is genuinely open.

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should the strict finding-id rule refuse the two committed records that pass today by miscounting? | **Refuse** — `r3 🟡 2` keys as finding 3 and `🟢 round 2's finding (🟡 4)` keys as 2; both silently attach a fix to the wrong verdict row, and refusing turns a wrong answer into a named one · **Grandfather** — key the rule to a work-item cutoff the way `SURFACE_FROM` does, so old records keep their miscount | **Refuse.** Neither record will be re-closed — `close` runs on the record `new` just wrote — so the grandfathering would guard nothing and would add a second cutoff constant to a file that already carries two | ✅ assumed, not asked; the measurement is in `plan.md` §Technical context |
| Q2 | Should a `pytest_*` hook in a `conftest.py` be a member of #211's class, given this tree holds none? | **Include** — it is a member by construction of pytest's plugin dispatch, and a case can be built in a synthetic repo · **Leave out** — no member exists here, so the rule would be unpinned mechanism | **Include.** §12 asks for the class rather than the instance, and the case is built against a repo the test creates, so the rule is pinned by something seen red rather than by the tree happening to hold an example | ✅ assumed, not asked |
| Q3 | Does `Contract changes` want a narrowing once the literal set makes it wider? | **Leave it wide** — every changed returnable literal enters the row · **Narrow to non-string literals** — a swapped message string stops pulling a reach walk | **Leave it wide** for this release. The row exists for #57's largest regression class, and a message a caller compares against is exactly the reach a person misses. Whether it becomes noisy is a fact only the next few records can supply | ⬜ **open** — the repository owner answers, after 0.9.1's records show how many entries the wider rule actually adds |

Q3 is the one row that outlives this branch. It carries no default that
changes code, so it is a question and not a blocker; `overview.md` §*Not
verified* names it with its answerer.
