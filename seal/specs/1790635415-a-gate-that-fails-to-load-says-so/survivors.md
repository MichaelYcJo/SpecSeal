# Survivors — a gate that fails to load says so

`survivor-check --range 2dc9a970..43e05300`, run by the builder at the end of
phase 3, reported one place. It is this work item's own frame, quoting the
sentence the work was asked to correct, so it is correct where it stands.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md` | would turn the notice off "and nobody would learn | §*Scope* item 6 names the `hooks/implementer.py` sentence this work makes false, quoting it so the builder can find it. It records what was corrected, and the correction is at `hooks/implementer.py`'s module docstring |
| `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/questions.md` | Each line names the gate file, the group, load or run, and the exception's class and first line. | Q3's options cell, reported by `survivor-check --range d89f8392..608e7eb5` in round 1's fix pass. It records what the question said when it was asked; the answer's cell points at the phase record, and `spec.md` §*Scope* item 4 carries the corrected rule |
| `tests/test_a_gate_that_fails_says_so.py` | Not JSON, not an object, or an empty `cwd`: nothing is recorded, nothing raises | `test_a_payload_the_report_cannot_read_records_nothing`'s docstring, reported by `survivor-check --range 93d67a5b..HEAD` in round 2's fix pass. It is about the hook's PAYLOAD, not a gate's output, and shares only the phrase "not an object" with the corrected G6 claim. Still true |
| `seal/releases/0.4.0.md` | Also measured with `cmdline.py` broken: the group prints nothing and the mark is still written | The `run_gate` row's execution note, reported by `survivor-check --range 551c7967..HEAD` after the sealer's run at `25582cd3`. It shares that wording with the `# RIDER:` phase 3 resolved out of `hooks/dispatch.py#run_gate`. Still true, measured 2026-09-29 at `c062880b` by a one-off probe deleted after it ran: with `cmdline.py` broken in a copy of `hooks/`, `pre-agent` for an `isolation: "worktree"` spawn printed `''` and the implementer mark was written. #28 records the failure for the `stop` group to say and prints nothing in `pre-agent`, so the group's own stdout is still empty |

The revert of #662 and #665 at the owner's decision after round 3 removed
1630 sentences: phase 5's cases, its record, G7 and G8, and the text the
release branch's files had before phase 5 edited them. `survivor-check`
reported 17 places over that range. Each is correct where it stands, and
none carries #662's or #665's rule. They are #28's and #661's own re-read
notes and case docstrings, the gate spec's pre-#662 text, and
`plan.md`'s phase rows, which the orchestrating session owns. They share
generic phrasing with what the revert took out.

| Range | Grounds |
|---|---|
| `3fb828fb..ab5219d6` | the revert of phase 5 (#662, #665); every reported place shares phrasing with removed text and is true where it stands, and the durable account is `phases/phase-5.md` and `overview.md` §*Not done* |
