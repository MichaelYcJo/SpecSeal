# the gate stops the session editing its own test fixtures — questions

<!-- specs/1788184145-the-gate-stops-the-session-editing-its-tests/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should the commit gate skip a heredoc body that is being written to a file rather than run? This is issue #34's second checkbox | **Skip it** — `cat > f <<EOF` and `python3 - <<EOF` that patches a file stop being read, so a person editing the gate's own tests by hand no longer meets the prompt. It costs the reader a judgment it makes nowhere else, deciding what a body is FOR, and it reopens what legacy #75 closed: a body that looks inert can run. **Leave it** — the gate keeps reading every body, and the path stays open for anyone editing by hand rather than through the `Edit` tool | Leave it. The gate is unchanged by this work | ⬜ |

| Q2 | `agents/smith.md` trips the commit gate at its own `[no-review]` waiver example (line 43), so a session patching its own contract by heredoc meets the prompt this work item exists to remove. How should that be resolved? | **Leave it, with the rider** — the example keeps working, and whoever opens the line is told why the file trips and that the trade was deliberate. The path stays open for anyone patching this file by heredoc. **Break the example** — split the token, or show it as an image or a non-copyable span, so the line stops being read as a command. The file stops tripping, and the example stops being copy-pasteable, which is the whole of its value: a waiver a reader retypes by hand is a waiver typed wrong. **Fix it at the gate** — Q1's change would cover this line too, since a heredoc patching a file would no longer be read | Leave it, with the rider. The rider is planted at `agents/smith.md:43` and stamped, so the fact reaches the next reader either way | ⬜ |

**Who answers Q1**: the repository owner. It is a deliberate trade against
legacy #75 rather than a change made to quiet a prompt, which is why option A
was taken first and this was not folded into it.

**Who answers Q2**: the repository owner. It is the same shape as Q1 — a
waiver example is only useful shown verbatim, so making the line stop tripping
may cost the example its job. Round 2 recorded the fact and planted the rider
rather than choosing, because choosing is not a fix a session should make on
its own.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
