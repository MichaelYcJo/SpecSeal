# 1791076831-a-here-document-body-is-data-to-the-commit-gate — overview

📋 implement applied
· spec:     this directory's spec.md (R1–R3, S1–S12), plan.md, questions.md Q1–Q5; docs/commit-review-gate-spec.md (the four paragraphs spec.md §Grounding names); CONTRIBUTING.md §What a change to a gate must carry; skills/agent-contract/SKILL.md §9
· evidence: seal/ledger/1791076831-a-here-document-body-is-data-to-the-commit-gate.md — H1–H4 added; 15 `Re-read ·` and 3 `Corrected ·` rows (0.16.0's E3, E7, E9) for released rows this range moved
· verified: executed — the three refusals at 101f9bd0; the new module at 101f9bd0 (every silent case red, every stop case green) and at the head; the plan's ten gate and reader modules at the head (1437 passed, 77 skipped); the document and ledger modules; one mutation per added unit, each red; the by-construction enumeration in bash 3.2.57 and zsh 5.9 (35,616 runs, 0 holes). Read — gh's help text for Q4

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
| That the two `gh` subcommands in `GH_NOTHING_LOCAL` (`pr ready`, and `pr edit` given a flag) run nothing local at runtime — no hook-running git, pager, browser or editor; the set was read from `gh … --help` at 2.100.0 (Q4, narrowed by #763), and the enumeration ran `gh` as a stub | the reviewer (warden), or a person with a scratch repository and network access |
| Windows and Linux shells — the enumeration ran macOS bash 3.2 and zsh 5.9 only | CI's `windows-latest` and `ubuntu-latest` jobs, for the cases; nobody for the enumeration |
| The full suite, lint and typecheck | the sealer, after the review rounds settle |
| ✅ `seal/releases/0.15.1.md`'s L1 reads DRIFTED on this branch and on its base, because `f19e2762` (#752) changed a test it cites; the strict ledger check in the broad gate refuses it, and this work item did not re-read a row it never moved | re-read into this work item's fragment by the orchestrator at `f75ef84b`; `evidence-check --strict` read 0 drifted there |
| Whether the generated corpus 0.16.0's I10 names held a shape #739 now makes data; that probe was deleted and was not run again | nobody can rerun it; the reviewer judges whether the I10 re-read's wording is enough |

## Not done

Unquoted delimiters and nested bodies keep today's reading, as `spec.md` §Scope puts them out; so the `git commit -m "$(cat <<'EOF' … EOF)"` false stop is not fixed here. Interpreters other than Python (`node -`, `perl -`) are not data. `git commit -F - <<'EOF'` is not a consumer, although its body is a message: the frame's consumer list is closed and nothing measured that shape.

## Fed back into the spec

none
