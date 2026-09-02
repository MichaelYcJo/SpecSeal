# the release check never watched bin/ — questions

<!-- specs/1788302682-the-release-check-never-watched-bin/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

## Q0 — answered before the first edit

**The batch found nothing that changes what is built.** Routing was answered
by the repository owner on 2026-09-02 and committed before the first edit
(`routing.md`, 4d36435). Whether `bin/` ships is a fact, not a decision, and
it was settled by opening things (plan.md §Technical context).

**Plan approval is delegated.** The spawn instruction says no question is put
to the owner mid-run and a conservative default is taken instead; the
conservative default for a gate is the narrowest change that closes the
reported gap plus the pin that keeps it closed, which is what `plan.md`
chooses.

## The issue's second checkbox — each candidate outside the five roots

| Candidate | Ships through the plugin? | Reason | Decision |
|---|---|---|---|
| `bin/` | yes | the loader puts it on the Bash tool's PATH (plugin reference, *File locations*; executed here — `command -v evidence-check` resolves into the plugin cache) | **added** |
| `install.sh` / `uninstall.sh` | no | a person runs them from a clone (`bash install.sh`, README §Install); the loader reads neither, and a clone is always current — no version keys their delivery | not added |
| `docs/` | no | the loader documents no such component; skills and hooks name `docs/*.md` in prose and messages, none opens one at runtime (`grep -rn "open(.*docs/" hooks skills` — nothing) | not added |
| `evals/`, `tests/`, `specs/`, `.specseal/`, `.github/` | no | this repository's own work — none reaches a user through the plugin | not added |
| `assets/` | no | `demo.gif`, read by the README on GitHub only | not added |
| `README*.md`, `CHANGELOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `ruff.toml`, `.gitattributes`, `.gitignore` | no | read by people on GitHub or by tooling in a clone; `hooks/version-check.py` reads `plugin.json` only (its `open(` at line 71) | not added |
| `commands/`, `workflows/`, `output-styles/`, `themes/`, `monitors/`, `.mcp.json`, `.lsp.json`, `settings.json` | would, but none exists here | documented plugin components absent from this repository; the pattern is not widened to directories nobody can open. The classification test fails the moment one appears, which is where the decision is taken | not added — caught on arrival |

## Assumptions recorded rather than asked

| # | Assumption | Grounds | Status |
|---|---|---|---|
| A1 | The pattern is matched in the test with Python's `re`, not by spawning `grep -E` | CI runs the suite on windows-latest, where `grep` is not on every PATH; the pattern uses anchors, alternation and one escaped dot, which POSIX ERE and `re` read alike | ✅ recorded |
| A2 | `plugin.json` stays at 0.2.0 on this branch | the pull request targets `release/v0.3.0`; the version moves when that branch merges to `main` (`docs/branch-and-release.md`) | ✅ inherited |
| A3 | The release document's enumeration is kept in prose and pinned by the test rather than replaced by a pointer to the workflow | a reader of the release sequence should not have to open a workflow to learn which roots trigger the bump; the pin is what keeps the two from drifting | ✅ recorded |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
