# Feature Specification: the fixes are what open the next round

<!-- specs/1788272986-the-fixes-are-what-open-the-next-round/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| Issue #57's measurement — ten regressions on `1788229400-…`, each traced to the fix that opened it; the largest class (4 of 10) is *a fix changed a unit's contract, and not every place that contract reaches was revisited* | The diff names the changed signature and `grep` names the reach; nothing here needs judgement, so it can be a gate rather than a question — and `CLAUDE.md`'s first goal ranks a gate above a question |
| `docs/review-chain-spec.md` §The last round verifies — the verifying round's job is *the answers rather than new findings* | Read literally, that sentence tells the verifying round to skip the units the fixes CREATED, which nobody has ever reviewed. Round 4's fix commit created eight new units; four carried defects |
| `docs/review-handoff-protocol.md` §round-N.md — the record's field table is what a conforming tool reads | The two new rows go in as protocol shape, not as this plugin's private convention, exactly as `Fixes checked by` did |
| `skills/code-review/SKILL.md` §Two stages — stage 2 names security; §Comparison axes — *the table is what makes an axis mandatory* | Security is named in prose and absent from the table, so it leaves no `❓` when nobody walks it. Three of round 5's four 🔴 had a stronger security frame than the one they were given — 🔴 B was a fail-open in a repository that maintains `tests/test_gates_do_not_fail_open.py` for that class alone |
| `chain_check.py` `STRICT_FROM` and its comment — grandfathering keyed to the unix second in the work item's directory name | The new rows reuse that shape: records of work items begun before this one print rather than fail, which is what keeps the eight merged `1788229400` records (and every other pre-rule record) green |
| `CLAUDE.md` — no real identifiers in examples or fixtures; fragments, never the shared files | New fixtures use neutral values; the changelog entry and ledger rows are fragments |

## Scope

**In — the five machine-checked items of issue #57.**

1. `round-N.md` carries a `| Contract changes |` row: every unit whose
   signature, return arity, return type, or set of returnable values changed
   in this round's fixes, each with the call sites it reaches.
   `chain_check.py` refuses a record without it and refuses a unit listed
   without its reach.
2. `round-N.md` carries a `| New units |` row: the top-level definitions and
   constants the round's fixes added. A verifying round treats what it names
   as a finding surface (*is this correct*) rather than a verification
   surface — written into `skills/code-review/SKILL.md` and
   `agents/warden.md`, because the warden's own scope rule (*answers rather
   than new findings*) would otherwise tell it to skip exactly these units.
3. Both rows accept an explicit `none` (with or without a reason after a
   separator), and records of work items begun before this one print rather
   than fail — the grandfathering shape `Fixes checked by` already uses,
   keyed to a new cutoff constant whose value is this work item's own id.
4. The comparison axes table in `skills/code-review/SKILL.md` gains a
   security row; `tests/test_review_axes.py` extends its pin to it.
5. The paste-ready-fix rule gains its second clause: a fix touching an OS
   boundary states its assumed precondition — path resolution, file modes,
   symlinks, subprocess working directory, encoding. The existing clause
   covers invented *names*; this covers unexamined *premises*.

**In — the three written rules**, placed in `skills/code-review/SKILL.md`
(the issue leaves placement to this work): a subsection under the findings
format carrying (6) an enumeration over an unbounded domain is a recorded
limit, not a closed finding; (7) what a mutation score licenses — the pins
discriminate, the fix is *tested*, and nothing about *safe* — stated where
the number is reported; (8) a document claim gets a pin.

**Out, per the issue.** The round cap's numbers, and any new question put to
a person — both new rows are written by the session that already has the fix
diff open, so the prompt budget of this change is zero.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A record without the rows is refused, for a new work item | Given a chain-declared item begun after the cutoff whose record carries no `Contract changes` (or no `New units`) row · When `chain_check.py` runs · Then it exits 1 naming the row and what it is for | Executed — `tests/test_the_fixes_name_their_surface.py` |
| A unit listed without its reach is refused | Given `Contract changes` reading `` `read()` gained a `None` return `` with no call sites · When the check runs · Then exit 1 naming the entry | Executed |
| `none` is an answer, reasons included | Given `none` or `none — the fixes changed no signature` in either row · When the check runs · Then exit 0 | Executed |
| Records predating the rule print rather than fail | Given the same missing rows on a work item begun before the cutoff · When the check runs · Then exit 0 with a notice per row | Executed, and read against `specs/1788229400-…/rounds/round-{1..8}.md` — all eight predate the cutoff |
| The verifying round knows the new-unit surface | Given a session reading `skills/code-review/SKILL.md` or `agents/warden.md` · When it reaches the verifying-round rules · Then it finds that `New units` is a finding surface, judged as code | Read, pinned by the new test file |
| The axes table asks the security questions | Given the table · When `test_review_axes.py` runs · Then the `| Security |` row and its probes hold | Executed |
| The three written rules survive a rewrite | Given the skill's new subsection · When any of the three sentences is dropped or rewritten · Then the new test file goes red | Executed — each pin seen red before the text landed |
| A session writing from the template writes a record the check accepts | Given `templates/sdd-round.md` · When its two new rows are copied · Then the placeholders name `none`, the arrow, and the reach | Read, counted outside comments by the new test file |

## Data & interfaces

Two new rows in `round-N.md`'s field table, read by `chain_check.py` on
**every** record of a chain-declared work item the pull request examines —
the same scope as `Fixes checked by`, because every round has its own fixes.

| The row says | `chain_check.py` |
|---|---|
| the row is absent, work item begun on or after `SURFACE_FROM` | **fails**, naming the row and what it is for |
| the row is absent, work item begun before (or with no timestamp prefix) | prints a notice — the grandfathering shape `STRICT_FROM` already uses |
| `none`, with or without a reason after a separator | passes |
| an empty cell | **fails** — a row that says nothing answers nothing |
| `Contract changes` entries (`;`-separated), each `unit → reach` (`→` or `->`) | passes |
| an entry with no arrow, or an empty unit or reach half | **fails**, naming the entry — a contract change without its reach is the unchecked half of the measured failure |

`SURFACE_FROM = 1788272986` — this work item's own id, so the first item held
to the rule is the one that wrote it, the same property `STRICT_FROM` has.
The draft-pull-request excuse does not reach these rows, exactly as it does
not reach `Fixes checked by`: the rows are filled when the fixes land, and a
record can honestly carry `none — <the fixes are not yet written>` while a
round is still running.

## Open questions → questions.md

Q1 — entry format for `Contract changes` (assumed: `;` between units, `→` or
`->` between a unit and its reach). Q2 — whether a malformed row on a
grandfathered record should fail (assumed: yes — formatting is always
repairable, unlike a review nobody ran). Both recorded with grounds in
`questions.md`; neither blocks, since either answer is a one-line change to
`fix_surface`.
