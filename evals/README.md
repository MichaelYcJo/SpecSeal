# Conformance evals

Five cases proving the preset's claims with real agent runs, via
`claude plugin eval` (early access — runs once enabled on the account):

```bash
claude plugin eval . --allow-tools Bash Write Edit
```

| Case | Claim it proves | Graders |
|---|---|---|
| implement-proof | implement skill fires on build requests and ends with a proof block only fillable by reading the spec | Skill fired (with-only) · proof-block regex · file_exists |
| review-verdicts | code-review fires, catches a planted spec violation, reports with proof | Skill fired · violation quoted · proof-block regex |
| pr-body-style | PR bodies follow writing-style norms (no file-by-file listing, migration called out, plain Korean) | LLM judge · Skill fired |
| lint-hook *(experimental)* | plugin hooks fire inside eval runs — probe; reference docs leave this undefined | file-content regex |
| commit-gate *(experimental)* | the unreviewed-commit gate interrupts inside eval's dontAsk mode — probe | last-message regex |

The two experimental probes are diagnostics as much as tests: their pass/fail
answers whether hook enforcement is exercisable under eval at all.
