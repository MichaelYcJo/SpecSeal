# Feature Specification: the gate stops the session editing its own test fixtures

<!-- specs/1788184145-the-gate-stops-the-session-editing-its-tests/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/implement/SKILL.md:393` — *"An edit must be able to fail. Prefer the `Edit` tool"* | The instruction already exists at the skill level. This work carries it into the two agent files, which is where a spawned session reads its own contract, and adds the reason the skill does not carry |
| `docs/review-chain-spec.md` — the commit gate is fail-closed and asks rather than guesses | The gate is not the defect. Nothing here changes what it reads or how it answers |
| `CLAUDE.md` — no real identifiers in examples or fixtures | New prose uses no domain, user path or org name |

## Scope

**In.** `agents/smith.md` and `agents/warden.md` state that file edits go
through the `Edit` tool, and name both reasons: an edit must be able to fail,
and no Bash command line exists for the commit gate to read.

**Out, and deliberately.** Option B of issue #34 — teaching the gate to skip a
heredoc body that is being written to a file rather than run. It reopens what
legacy #75 closed, so it is a decision for the repository owner and sits in
`questions.md` as Q1 rather than in this diff.

**Also out.** `hooks/commit-review-gate.py` is not touched, no test fixture is
rewritten, and no waiver mechanism is added or widened.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The smith reads its own contract before editing | Given a spawned `smith` about to patch a test fixture · When it reads phase 3 · Then it finds the `Edit` tool named with both reasons, not only the silent-no-op one | `agents/smith.md` phase 3 carries both reasons; read |
| The warden reads the same thing | Given a spawned `warden` about to write a probe or reproduce a finding · When it reads its Role section · Then it finds the same instruction, placed beside the probe rules it already has for keeping off the commit gate | `agents/warden.md` Role carries it; read. `grep -i 'Edit. tool' agents/warden.md` returned nothing before this work |
| The wording survives the suite's own prose rules | Given the new paragraphs · When `test_docs_line_wrap` and `test_the_set_a_work_item_always_has` run · Then both pass | Executed |
| The wording cannot be deleted without a check going red | Given either agent file · When a rewrite drops the pairing, the second reason, the command-word rule or the `eval` branch · Then `tests/test_edits_go_through_the_edit_tool.py` fails | Executed — planted during round 1, extended in round 2, and each case shown red under a mutation before being called passing |
| The warden's own file does not trip the gate it warns about | Given `agents/warden.md` · When `_hides_a_commit` reads it whole · Then False, and prose added above the waiver row does not flip it | Executed — the same test file pins it. `agents/smith.md` trips at its own waiver example and carries a rider saying so; the trade is Q2 |
| A reader can find why option B was not taken | Given someone asking why the gate still reads heredoc bodies · When they open the work item · Then `questions.md` Q1 names the trade and the answerer | Read |

## Data & interfaces

None. Two markdown files change; no hook, no schema, no command-line surface.

## Open questions → questions.md

Q1 — whether a heredoc body being written to a file is a shell the gate should
read. It is issue #34's second checkbox and is not decided here.
