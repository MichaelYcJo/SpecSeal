# Feature Specification: a base session that died part-way is not read as finished (#849)

<!-- seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `templates/config.md` §*Broad gate*, rule 3 | the words `new` and `new?` a failing file reads at the base, and that every failure of the mechanism is strict |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | the direction: a measurement the gate cannot vouch for reads `new?`, never `new` |

The frame is round 6 of work item 1791270161 (#825): `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/rounds/round-6-report.md`, its verdict table, its probes and its *Paste-ready fixes*. That run ended capped, and the owner chose to fix its three findings here.

## Scope

In:

1. **🟡 1.** A base session whose record has no `end` line stopped part-way. Its process died, or its recorder stopped writing. `read_record` counts such sessions as `unended`. Where a file would read `new`, `base_word` returns `new?` with a new reason naming the count. It checks `unplaced_red` first. Rule 3 of `templates/config.md` §*Broad gate* gets the sentence.
2. **⬜ 2.** The recorder's `last_sent` is keyed on the worker object itself, not on `id()` of a worker it does not hold.
3. **⬜ 3.** Work item 1791270161's `overview.md` divergence table gains the row for the strict `new`: since round 4, the comparison depends on the `end` line, which `spec.md` Scope 1 of that item did not describe.

Out:

- Any other demotion rule, and the xdist path. Round 6 confirmed that `path_of` closes its class.
- The owner's Q1 and Q2 of 1791270161. Both stay as built, (a).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given a row run without xdist, and a base where a test in `tests/test_two.py` calls `os._exit` in its body. When the branch fails a test in that file. Then the file reads `new?`, naming one session that wrote no end, and not `new`. | a gate case on `CRASHES_ITS_WORKER`, red at 6de64c19 |
| S2 | As S1, with the crash in a fixture's setup. | a gate case on `CRASHES_ITS_WORKER_IN_SETUP`, red at 6de64c19 |
| S3 | Given a base whose every session ended. When a file the base never collected fails on the branch. Then it reads `new`, as before. | the existing `new` cases stay green |
| S4 | Given a base with both an unplaced red session and an unended one. Then the reason is `unplaced_red`'s, which is checked first. | a gate case |
| S5 | Given the recorder under xdist. When a worker is replaced. Then the replacement inherits no entry of the freed worker. | a recorder case, or a stated read where it cannot be provoked |
| S6 | Rule 3 names the unended reason, and a pin holds the sentence. | the policy pin case |

## Data & interfaces

- `skills/verify/scripts/broad_gate.py`: `RunRecord` gains `unended`. `read_record` counts a keyed session with no `end` line. There is a new constant `UNENDED_AT_BASE`, and `base_word` returns it after the `unplaced_red` check.
- `skills/verify/scripts/pytest_record/specseal_pytest_record.py#Recorder`: `last_sent` is keyed on the sender.
- `templates/config.md`: one sentence in rule 3.

## Open questions → questions.md

None. The fixes are the reviewer's, executed in a clone in round 6 (the gate module passed 431).

Framed 2026-10-07 by the session, before the build.
