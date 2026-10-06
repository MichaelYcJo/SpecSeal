# 1791327652-a-base-session-that-died-part-way-is-not-read-as-finished — overview

📋 implement applied
· spec:     this item's `routing.md`, `spec.md`, `plan.md`; work item 1791270161's `rounds/round-6-report.md` (verdicts, *Executed probes*, *Paste-ready fixes*), `overview.md`, `spec.md` Scope 1; `templates/config.md` §*Broad gate* rule 3; `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base*; `CONTRIBUTING.md` §*What a change to a gate must carry* (heading); `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*
· evidence: `seal/ledger/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished.md` U1–U3 added; work item 1791270161's fragment W5, W8 and `Corrected · D1` given the new word in place, and its 30 rows citing a drifted coordinate re-stamped by `evidence-check --reverify --checked 2026-10-07`
· verified: executed — the new cases red at 6de64c19's code and green after, the gate and recorder modules whole, eleven `bin/mutation-check` runs, `bin/evidence-check --strict .`, `survivor-check`; read — a worker replaced inside a live xdist run, and a recorder that stops writing for a reason other than a dead process

## Why this work exists

A base whose own pytest a test killed part-way gave `new` for the file it crashed in, so the gate told the branch it broke a file the base never finished measuring; now that file reads `new?` naming the sessions that stopped.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What rule 3 and the **New?** bullet carry | `spec.md` Data & interfaces: "`templates/config.md`: one sentence in rule 3" / rule 3 gains two sentences, the second saying that a red session's left-out count is named where both apply, and the **New?** bullet of `skills/verify/SKILL.md` gains one | both documents, pinned | Contract §14, and round 6's own words: "Rule 3, the **New?** bullet, the changelog and the module's pinned-sentence cases need the new reason under §14". The precedence is S4's, and a person reading `new?` with the unplaced count beside a crashed base would otherwise not know the second cause was also there |
| A `node` no dict can key | round 6's paste-ready fix for ⬜ 2: `self.last_sent[sender] = …` and `self.last_sent.get(sender, …)` with nothing before them / `path_of` first tries `hash(sender)` and reads an unhashable `node` as no sender | the guard | Keyed on `id()`, any object could be a key; keyed on the object, a plugin that set `report.node` to an unhashable value would raise `TypeError` out of a report hook, and the recorder never raises out of a hook (`spec.md` of 1791270161, Scope 1). xdist 3.8.0's `WorkerController` defines no `__eq__` and no `__hash__` · NAME NOT IN TREE, so no worker of xdist's meets the guard. Pinned in the S5 case, and red through `bin/mutation-check` |
| How S5 is shown | `spec.md` S5: "When a worker is replaced … a recorder case, or a stated read where it cannot be provoked" / a unit case frees a plain `object()` that sent a report and makes objects until one takes its address | the unit case, and the live replacement stated as read | At 6de64c19's recorder the first object made took the freed address and the crash report took `/r/a.py`, so the case is red there. An instance of a class the case defines was measured not to reuse the address within a thousand objects on CPython 3.13, so the case uses `object()`, as round 5's unit case already does. A replacement inside a live xdist run reuses no address in an ordinary run (round 6's ⬜ 2) |

## Not verified

| Item | Who must answer |
|---|---|
| The two gate cases (S1, S2) on Linux and Windows, where `os._exit` in a test also ends plain pytest without `pytest_sessionfinish` | CI's three-platform `pytest` job, at the pull request |
| A worker xdist starts in place of a crashed one, inside a live run: not provoked, read only (the terminal reporter keeps the crash report, which holds the old worker) | warden, in this work item's review round |
| A recorder that stops writing for a reason other than a dead process, such as a full disk: the record then holds no `end` line and reads as unended, by the same branch S1 drives; not provoked | warden, in this work item's review round |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

Nothing. `spec.md`'s Out list (any other demotion rule, the xdist path, and 1791270161's Q1 and Q2) was left as it says.

## Fed back into the spec

- Rule 3's sentence that a red session's left-out count is the one named where a session of the base also wrote no `end` line — *inferred during implementation* from S4, so a planner may overturn it.
