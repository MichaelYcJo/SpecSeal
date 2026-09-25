# 1790297086-the-broad-gate-says-what-ci-says — overview

📋 implement applied
· spec:     <filled when the work item closes>
· evidence: <filled when the work item closes>
· verified: <filled when the work item closes>

## Why this work exists

The broad gate and the cases that read the workflow it mirrors said things CI
does not say. `cmd.exe` got `xcopy\e`, a release pull request met two arms CI
skips, and the workflow's readers counted comments. After this work each of
them reads the way CI does.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The order of the three removals that make a name's part | `spec.md` S1: "with `"` and `^` removed and one leading `@` dropped", with no order | the leading `@` is dropped first, then `"` and `^` are removed | `cmd.exe` reads only an unescaped, unquoted `@` as the echo-off prefix. The built-in check already strips `@` from the raw name (`lstrip("@")`) |
| The empty part | `spec.md` S1: "An empty part … counts as a directory" | answered inside the scan, and the predicate is never asked | The drive's root always exists, so there is nothing to ask. A4's recording case pins that `/abs/x` asks nothing |
| The existing `WORKFLOW_SHAPES` row for `BASE:` | a bare `BASE: origin/…` line was read as a base on its own | the row now carries the `env:` line it stands under | `spec.md` S2 #462: a `BASE:` counts only as a key of `env:`. A line with no mapping above it is not one |
| When `overview.md` opens | `plan.md` phase 4: "`overview.md` written" | opened in phase 2 | The implement skill opens it at the first unverified item, and M1 is one from phase 1. `tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview` refuses a phase record without it |

## Not verified

| Item | Who must answer |
|---|---|
| `cmd.exe` runs `where/q cmd` as `where` plus its switch and exits 0 (A6, `questions.md` M1) | CI's `windows-latest` leg at the pull request |
| The full suite, lint and typecheck over the finished branch | the sealer's one broad run, after the review rounds settle |

## Not done

nothing

## Fed back into the spec

none
