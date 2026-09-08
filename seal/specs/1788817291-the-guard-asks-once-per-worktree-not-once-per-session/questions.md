# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — questions for the planner

<!-- seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

The ticket names three open questions and says they are the implementer's to
decide and argue rather than to bring back. They are recorded here with what
was chosen and why, so a later reader can overturn a decision rather than
rediscover that one was made.

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Does the consent record expire? | **No bound** — the session id already scopes it; a session that ends stops using its id. **A time bound** — a session outliving it is asked a second time, which is the failure this work removes, and the bound is a second thing to get wrong | No bound, and no pruning either — the choice markers beside it are not pruned | ✅ decided |
| Q2 | Does a failed `git worktree add` (non-zero exit) record consent? | **Yes** — the record is about the approval, which happened; the retry after a failure is the worst moment to put the question again. **No** — reading the outcome means reading `tool_response`, whose shape varies and which a compound command makes ambiguous | Yes, and the exit status is never read | ✅ decided |
| Q3 | What happens when `PostToolUse` cannot write the record? | **Silent, no record** — the next creation asks, which is one extra prompt. **Raise** — the module's own `_idle_minutes` note says a crash reads as a silent allow | Silent, no record. The guard fails toward the prompt | ✅ decided |
| Q4 | Is the record a third directory or a value in the existing choice marker? | **Third directory** — the choice marker is written before the answer and means *the question was put*, and the two fail in opposite directions. **A value in the existing one** — one place, one resolution | Third directory, `specseal-worktree-consent/`. `spec.md` §Data & interfaces holds the argument | ✅ decided |

Q4 is not one of the ticket's three. The ticket asks the implementer to *say*
whether this is a third directory or a value in the existing one, which makes
it the same kind of row: a decision recorded rather than a decision deferred.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges. Q1–Q4 land in
`docs/worktree-guard-spec.md` §*Creation consent*.
