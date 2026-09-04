# a check reports clean while something is missing — questions for the planner

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Is guidance enough for #153, or does the tool have to announce its own narrowing? | **Guidance alone** — the handoff names the unscoped read and the scoped write. Cheapest, and it binds only a session that reads it. **Guidance and the tool** — the check also says which ledgers it did not read. Costs a line of output on every narrowed run | both | ✅ settled by evidence, not by preference — a session that narrows on its own initiative reads the guidance nowhere, and that is exactly how this trap was sprung: the narrowing was correct guidance for writing, carried into reading by the orchestrator without either instruction being wrong about its own subject |

| Q2 | Phase 1 tells every round to run the **unscoped** read, so from now on every branch will SEE the rows it drifted in `seal/ledger.md` — and the only tool for re-stamping them, `evidence-check --reverify`, has no row selector. It narrows by FILE, so a branch whose own drift is in the shared file must re-stamp `seal/ledger.md` whole, which takes S8's false claim with it and has to be undone by hand afterwards. This branch did exactly that (see `overview.md`). Should it become an issue, and in which release? | **An issue for a row selector** — `--reverify --only <anchor>`, or a refusal to re-stamp a row a config names. It is the general fix and it is not this work item's. **An issue for S8 alone** — correct the claim, and the recurring cost goes with it, since S8 is the only false row in the file today. **Neither** — the hand-restore is two commands and a sentence in the memo, and it recurs only while S8 stands | none — the session did not open one. Opening an issue is an outward-facing act, and `agents/smith.md` gives this session the pull request and nothing beyond it | ⬜ the repository owner |

Nothing else is open. The two tickets' routing was answered in one batch with
the rows in `routing.md`, and Q2 arrived from the work rather than before it —
it is written here rather than raised, which is what `skills/implement/SKILL.md`
§1 asks of anything that surfaces after the batch.
