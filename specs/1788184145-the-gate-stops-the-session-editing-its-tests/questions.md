# the gate stops the session editing its own test fixtures — questions

<!-- specs/1788184145-the-gate-stops-the-session-editing-its-tests/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should the commit gate skip a heredoc body that is being written to a file rather than run? This is issue #34's second checkbox | **Skip it** — `cat > f <<EOF` and `python3 - <<EOF` that patches a file stop being read, so a person editing the gate's own tests by hand no longer meets the prompt. It costs the reader a judgment it makes nowhere else, deciding what a body is FOR, and it reopens what legacy #75 closed: a body that looks inert can run. **Leave it** — the gate keeps reading every body, and the path stays open for anyone editing by hand rather than through the `Edit` tool | Leave it. The gate is unchanged by this work | ⬜ |

**Who answers Q1**: the repository owner. It is a deliberate trade against
legacy #75 rather than a change made to quiet a prompt, which is why option A
was taken first and this was not folded into it.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
