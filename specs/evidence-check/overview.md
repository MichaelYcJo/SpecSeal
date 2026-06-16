# evidence-check — overview

📋 implement applied
· spec:     docs/worktree-guard-spec.md, docs/review-chain-spec.md read for
            layout conventions; no prior spec existed for this feature —
            the SKILL.md written here is now its authority
· evidence: verified behaviors recorded below and in the commit message
· verified: fixture + real-world runs, listed under "What was verified"

## What was done

A drift detector for evidence ledgers: every `file:line` coordinate in
`_evidence.md` files is classified BROKEN / DRIFTED / EXTERNAL / OK, with
drift derived from `git diff <baseline SHA>..HEAD` overlapped against the
cited range. Shipped as a skill with a vendorable script plus a CI workflow
template. This is the competitive-landscape doc's opportunity #1 —
spec-to-code traceability had no equivalent in any surveyed framework.

## What changed

```
skills/evidence-check/SKILL.md               (new) verdicts, flags, limits
skills/evidence-check/scripts/evidence_check.py (new) the checker
templates/evidence-check.yml                 (new) CI workflow template
README.md / README.ko.md                     evidence-rot section added
```

## Key judgments

| Judgment | Chosen | Grounds |
|---|---|---|
| Drift semantics | "touched since baseline" = re-verify, not "wrong" | correctness of a claim is unknowable mechanically; staleness of its coordinate is not |
| Bare filenames | stay EXTERNAL, never fuzzy-matched | resolving to the wrong file would validate wrong evidence — worse than no check |
| Unprefixed migration coordinates | `--default-repo` resolution chain | discovered against a real ledger: migration ledgers cite the original repo with no prefix |
| CI delivery | vendor the script, don't fetch at run | deterministic, offline-safe builds |

## What was verified (executed)

- Fixture repo: all four verdicts, exit codes 0/1/2, `--strict`, `--map`.
- Real-world ledger: 424 coordinates parsed without error; 121 resolved via
  the root → default-repo chain; 9 broken found; 1 drifted.

## Not verified (who must answer)

| Item | Who |
|---|---|
| The CI template on an actual GitHub Actions run | first adopting repo |
| Recall on ledgers with loose citation styles (bare filenames dominate the real-world EXTERNAL count) | future work — needs a stricter citation convention, not a looser matcher |
