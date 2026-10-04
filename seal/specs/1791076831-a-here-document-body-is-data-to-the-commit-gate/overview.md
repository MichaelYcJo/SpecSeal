# 1791076831-a-here-document-body-is-data-to-the-commit-gate — overview

📋 implement applied
· spec:     this directory's spec.md (R1–R3, S1–S12), plan.md, questions.md Q1–Q5; docs/commit-review-gate-spec.md (the four paragraphs spec.md §Grounding names); CONTRIBUTING.md §What a change to a gate must carry; skills/agent-contract/SKILL.md §9
· evidence: seal/ledger/1791076831-a-here-document-body-is-data-to-the-commit-gate.md
· verified: executed — the three refusals at 101f9bd0; the new module at 101f9bd0 (every silent case red, every stop case green) and at the head; the corpus module; the plan's narrow modules; mutation-check per added unit; the by-construction enumeration run in real shells. Read — gh's help text for Q4

## Why this work exists

The commit gate refused whole Bash calls whose only commit was text in a here-document body that nothing runs, which stopped unattended runs (#739); such a body is now data, and every body something can run is read as before.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The per-body record's fields | spec §Data: "returning per body `(text, quoted, terminated)`" / code returns `Heredoc(text, quoted, terminated, delimiter, dashed)` | code | R2d asks that "the k-th opener owns the k-th body". A count alone can match while two openers are misread in opposite directions, so each opener's word on the line is compared with its body's delimiter |
| R2f's runners | spec R2f: "no `python3`/`python` consumer and no `git … commit` segment" / code: any `python3`/`python`, any `git`, and a `gh` subcommand outside the measured remote-only set | code, the stricter side | `git add` runs the `post-index-change` hook, so "a commit runs hooks" holds for more than `commit`; and Q4's measurement found `gh pr create`, `pr checkout`, `pr merge`, `pr close`, `issue develop` and `release create` running local git. Every narrowing here keeps a body read, never the reverse |
| R2f's reach | spec R2f: "A sink writes a file when it has an output redirection … or when it is `tee` with an operand" / code: a sink's body reaches a file when ANY stage of its pipeline writes one | code, the stricter side | `cat <<'EOF' \| tee f.sh` writes the body to `f.sh` through a stage that owns no body. Read as the spec words it, the body would be data beside a `git commit` that runs `f.sh` as a hook |
| Where the new cases live | plan phase 2: "S1–S8 planted in the gate's test module" / code: `tests/test_a_heredoc_body_nothing_runs_is_data.py` | code | One module holds the rule's cases in both directions beside the reader's, and the gate's module is 1,667 lines of other subjects |

## Not verified

| Item | Who must answer |
|---|---|
| That each `gh` subcommand in `GH_REMOTE` runs no local git at runtime — Q4 was answered from `gh … --help` at 2.100.0, and the enumeration ran `gh` as a stub | the reviewer (warden), or a person with a scratch repository and network access |
| Windows and Linux shells — the enumeration ran macOS bash 3.2 and zsh 5.9 only | CI's `windows-latest` and `ubuntu-latest` jobs, for the cases; nobody for the enumeration |
| The full suite, lint and typecheck | the sealer, after the review rounds settle |

## Not done

Unquoted delimiters and nested bodies keep today's reading, as `spec.md` §Scope puts them out; so the `git commit -m "$(cat <<'EOF' … EOF)"` false stop is not fixed here. Interpreters other than Python (`node -`, `perl -`) are not data. `git commit -F - <<'EOF'` is not a consumer, although its body is a message: the frame's consumer list is closed and nothing measured that shape.

## Fed back into the spec

none
