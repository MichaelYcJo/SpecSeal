# the release check never watched bin/ — overview

📋 implement applied
· spec:     CLAUDE.md (goal clause, fragment convention, gate rules),
            CONTRIBUTING.md §What a change to a gate must carry,
            docs/branch-and-release.md §Cutting a release, .specseal/follow-up.md
            (empty tables — nothing waiting on this work), the Claude Code plugin
            reference §File locations (the `bin/` row), specs/1788302682-…/{routing,
            spec,plan,questions}.md
· evidence: 2 rows in .specseal/map/1788302682-the-release-check-never-watched-bin.md
· verified: executed — the new test red against the unfixed workflow (3 failed),
            green after (29 passed), three mutations each red on the test that
            guards it; `grep -E` with the step's pattern on a sample file list;
            `command -v evidence-check` resolving into the plugin cache's `bin/`;
            neighbouring files (release_hygiene, changelog-gathered, docs_line_wrap,
            no_real_identifiers) 76 passed; ruff check/format on the test file;
            evidence_check --strict 71 ok. Read — the plugin reference, README §CLI,
            install.sh's header, the hooks' and skills' `docs/` citations.
            Unverified — the broad gate (below)

## Why this work exists

A wrapper fix could reach the marketplace without a version bump and so reach
nobody; now the release check watches `bin/`, and a test holds the list of
watched roots to the repository so the next shipping root cannot go unwatched
the way `bin/` did.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| none | | | |

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate — full suite, lint, typecheck | the orchestrator, once after the review rounds settle (`CLAUDE.md` §Verification Scope) |
| the hygiene step on a real pull request into `main` whose diff touches only `bin/` — the workflow was exercised only through its pattern, never by GitHub Actions | the repository owner, at the next release pull request that carries a `bin/` change |

## Not done

The pattern was not widened to plugin components this repository does not
have (`commands/`, `workflows/`, `output-styles/`, `themes/`, `monitors/`):
a pattern naming directories nobody can open reads no better than one missing
a real root, and the classification test is what catches their arrival
(`questions.md`, the second-checkbox table). `install.sh` and `uninstall.sh`
stay out on purpose — a person runs them from a clone, which is always
current, and the loader never reads them.

## Fed back into the spec

none
