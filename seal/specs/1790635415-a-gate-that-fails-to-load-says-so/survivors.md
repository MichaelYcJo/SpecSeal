# Survivors — a gate that fails to load says so

`survivor-check --range 2dc9a970..43e05300`, run by the builder at the end of
phase 3, reported one place. It is this work item's own frame, quoting the
sentence the work was asked to correct, so it is correct where it stands.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md` | would turn the notice off "and nobody would learn | §*Scope* item 6 names the `hooks/implementer.py` sentence this work makes false, quoting it so the builder can find it. It records what was corrected, and the correction is at `hooks/implementer.py`'s module docstring |
| `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/questions.md` | Each line names the gate file, the group, load or run, and the exception's class and first line. | Q3's options cell, reported by `survivor-check --range d89f8392..608e7eb5` in round 1's fix pass. It records what the question said when it was asked; the answer's cell points at the phase record, and `spec.md` §*Scope* item 4 carries the corrected rule |
| `tests/test_gate_judges_the_repo_it_commits_to.py` | `;` runs what follows whether the `cd` succeeded or not, so a failed `cd` leaves the commit in the directory the shell was already in | `test_a_semicolon_carries_the_commit_to_both`'s docstring, reported by `survivor-check --range 908ac33d..HEAD` in phase 5 (#662). It is still true: that case's `cd` names a directory nobody created, so the `cd` fails and both are judged. The removed wording was the gate spec's table row, which now says X alone where X can be entered |
| `tests/test_a_gate_that_fails_says_so.py` | Not JSON, not an object, or an empty `cwd`: nothing is recorded, nothing raises | `test_a_payload_the_report_cannot_read_records_nothing`'s docstring, reported by `survivor-check --range 93d67a5b..HEAD` in round 2's fix pass. It is about the hook's PAYLOAD, not a gate's output, and shares only the phrase "not an object" with the corrected G6 claim. Still true |
| `tests/test_gate_judges_the_repo_it_commits_to.py` | A shell, `ssh`, `xargs`, an interpreter given `-c` or a script (stdin is then input to a program that may hand it to a shell), and a name nobody listed all keep the body read as shell | `test_a_body_a_shell_may_run_is_still_read_as_shell`'s docstring, reported by the same run. Every shape it lists still reads as shell; the list is not the whole rule, and `test_the_program_a_heredoc_feeds_is_named_by_its_consumer` states the rule. Still true |
