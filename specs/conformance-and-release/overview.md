# conformance and release — overview

📋 implement applied
· spec:     docs/worktree-guard-spec.md, docs/review-chain-spec.md (tests
            assert their decision tables); docs/review-handoff-protocol.md
            written here and now the convention's authority
· evidence: CI run green on first push (ubuntu + macos); GitHub-source
            install verified end to end
· verified: listed below, executed vs blocked separated

## What was done

The trust layer over the 0.2–0.3 features: a permanent test suite wired to
CI, a conformance eval suite, release plumbing (remote install path,
changelog, version tag), and the handoff convention extracted as a
tool-agnostic spec.

## What changed

```
tests/ (3 files, 44 cases)            hooks + evidence-check regression suite
.github/workflows/test.yml            ubuntu + macos matrix
evals/ (5 cases + README)             claims → reproducible checks
tag v0.3.2                            release record
docs/review-handoff-protocol.md       draft 0.1, READMEs link it
hooks/worktree-guard.py               fresh_leases() extracted (testability)
```

## Key judgments

| Judgment | Chosen | Grounds |
|---|---|---|
| Decision tests stub session detection | monkeypatched, not env flags in prod code | CI runners have no claude processes — every switch would hit conservative-deny and hide the logic under test |
| Hook-under-eval uncertainty | two eval cases marked experimental, framed as probes | reference docs leave hook firing in eval undefined; a probe's pass/fail IS the answer |
| Marketplace source | switched this machine from local path to GitHub | the README's install command was unverified until it was someone's real path |
| Protocol scope | review handoff only, memory explicitly a non-goal | the survey showed memory is a crowded field (claude-mem, beads); structured review handoff is the open one |

## What was verified (executed)

- 44/44 tests locally; CI green on first push, both OSes.
- `claude plugin marketplace add MichaelYcJo/claude_preset` +
  `install` from GitHub → 0.3.2 installed.

## Blocked / not verified (who must answer)

| Item | Who |
|---|---|
| Running the eval suite (`plugin eval` is early access) | Anthropic-side enablement; then `claude plugin eval . --allow-tools Bash Write Edit` |
| install.sh interactive branch | user, real terminal |
| Whether plugin hooks fire under eval | the two experimental probes, once evals run |
