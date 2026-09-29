# Survivors — a gate that fails to load says so

`survivor-check --range 2dc9a970..43e05300`, run by the builder at the end of
phase 3, reported one place. It is this work item's own frame, quoting the
sentence the work was asked to correct, so it is correct where it stands.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md` | would turn the notice off "and nobody would learn | §*Scope* item 6 names the `hooks/implementer.py` sentence this work makes false, quoting it so the builder can find it. It records what was corrected, and the correction is at `hooks/implementer.py`'s module docstring |
| `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/questions.md` | Each line names the gate file, the group, load or run, and the exception's class and first line. | Q3's options cell, reported by `survivor-check --range d89f8392..608e7eb5` in round 1's fix pass. It records what the question said when it was asked; the answer's cell points at the phase record, and `spec.md` §*Scope* item 4 carries the corrected rule |
| `tests/test_gate_judges_the_repo_it_commits_to.py` | `;` runs what follows whether the `cd` succeeded or not, so a failed `cd` leaves the commit in the directory the shell was already in | `test_a_semicolon_carries_the_commit_to_both`'s docstring, reported by `survivor-check --range 908ac33d..HEAD` in phase 5 (#662). It is still true: that case's `cd` names a directory nobody created, so the `cd` fails and both are judged. The removed wording was the gate spec's table row, which now says X alone where X can be entered |
