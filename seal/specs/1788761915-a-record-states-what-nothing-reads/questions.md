# a record states what nothing reads — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | May the records arm ask git what the tree carries? Round 1's 🟡 3 is real — one untracked `scratch-notes.txt` holding `gone_helper` takes a live refusal from exit 2 to exit 0, and a `.gitignore`d bundle does the same — and the only repair is `git ls-files`. `README.md` §*A row carries no line number and no commit* says the check calls git for nothing outside `--migrate`, and `test_the_checker_asks_git_for_nothing` holds it with a run under an empty `PATH`, which a `subprocess` call would not survive | **Leave it** — the hole stays, and it stays in the safe direction: CI reads a clean checkout where the untracked file does not exist, so CI is the stricter reader and only the local run is lenient. **Widen the exception** — the records arm may call `git ls-files`, the no-git rule gains a second exception, and the runtime proof needs a records-arm carve-out; the reason behind the rule (nothing in a row for a squash to orphan) does not reach this call, which asks what the tree holds NOW rather than what a commit held | Left as it is. The fix was written, measured against six cases, and reverted when the policy was opened | ⬜ |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
