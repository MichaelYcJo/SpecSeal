# a check reports clean while something is missing — questions for the planner

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Is guidance enough for #153, or does the tool have to announce its own narrowing? | **Guidance alone** — the handoff names the unscoped read and the scoped write. Cheapest, and it binds only a session that reads it. **Guidance and the tool** — the check also says which ledgers it did not read. Costs a line of output on every narrowed run | both | ✅ settled by evidence, not by preference — a session that narrows on its own initiative reads the guidance nowhere, and that is exactly how this trap was sprung: the narrowing was correct guidance for writing, carried into reading by the orchestrator without either instruction being wrong about its own subject |

Nothing else is open. The two tickets' routing was answered in one batch with
the rows in `routing.md`.
