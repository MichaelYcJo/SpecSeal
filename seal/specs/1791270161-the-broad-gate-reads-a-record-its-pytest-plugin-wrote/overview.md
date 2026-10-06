# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — overview

## Why this work exists

The broad gate stops guessing which pytest run printed a failing line and reads a record its own pytest recorder wrote inside that run.

## Where phase 1 stopped, and what is next

Phase 1 is closed at 27365f10: the recorder and S1–S5, green and each seen
red (`phases/phase-1.md`). Nothing of phase 2 is started. `broad_gate.py` is
untouched, and nothing loads the recorder yet.

Next, phase 2 (`plan.md`): `recording_env` and `read_record` in
`broad_gate.py`, the `HEAD` run recording, the fallback, `compare_at_base`
rewritten to one run and the five-row table, the retirements of Scope 7,
rule 3 and the **New?** bullet with their pins. Two facts from phase 1 that
phase 2 builds on: a failed collection repeats once per xdist worker, so the
reader reads a file's lines as a set; and pytest's `rootdir` comes back
resolved (`/private/var/…` on macOS), so `realpath` is needed on both sides.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The recorder's comment and the release-hygiene exemptions | `spec.md` R11 and `plan.md` Technical context: the `9.1.1`/`3.8.0` exemptions move "to the recorder's own comment where it names the builds it was measured on" / the recorder's docstring names builds by two components (`7.4, 8.0, 8.1 and 9.1`, xdist `3.8`) and the exact builds sit in `phases/phase-1.md` | two components in the shipped file | A three-part token in a `LOADED` file needs an exemption keyed on it, and the docstring's reader needs the minor version only. This changes Q-W2's default for phase 2: there is no token in the recorder for an exemption to move to |

## Not verified

| Item | Who must answer |
|---|---|
| The recorder on Linux and Windows (`PYTHONPATH` with `;`, a Windows temp path) | CI's three-platform test job, at the pull request |
| The recorder's fallbacks for pytest below 6.1 (`config.rootdir`, `os.getcwd()`) | nobody measured them; the next session decides whether a build that old is worth a probe |
| The full suite, lint and typecheck over the branch | the sealer, once, after the review rounds settle |

## What was fed back into the spec

none — phase 1 added no clause.
