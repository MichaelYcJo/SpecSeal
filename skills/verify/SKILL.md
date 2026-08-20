---
name: verify
description: |
  Seal Test — evidence protocol for completion claims. Auto-triggers on
  done/complete/fixed/passes/PR keywords, before commits, and before
  handing work to the review chain.
---

# The Seal Test

A completion claim is a mark, and a mark must be *earned*. The community
baseline ("no completion claims without fresh verification evidence") stops
at freshness — it accepts any green command as proof. This protocol demands
more: **a check that cannot fail proves nothing, and evidence that outlives
its tree state proves less than nothing.**

A claim is sealed only when all four conditions hold:

## The four conditions

### 1. Named before run

State the proving command **before** executing it, next to the claim it
proves. Choosing the command after seeing what passes is how a test suite's
green becomes "feature works" — the claim-to-command mapping is the
verification, the run is just its execution.

### 2. Able to fail

Show the check CAN go red. For a bug fix: the reproduction failed before the
change (or fails when the change is reverted). For a new test: it was
observed failing against the pre-change code. A check that has never been
seen red is a counterfeit seal — this is the condition the generic gates
skip, and the one that catches assertion-free tests, mocked-away behavior,
and wrong-file test runs.

### 3. Bound to the tree

Evidence attaches to a tree state, not to a session. Note the state the
proof ran against (commit + dirty files); **any edit after the run breaks
the seal** — re-run, don't re-tell. Same drift logic the evidence ledger
applies to spec coordinates, applied to your own claims.

### 4. Executed, read, or unverified — labeled

Every claim carries one label. `executed` (ran it, read full output, exit
code checked) · `read` (inferred from reading code — a judgment, not proof)
· `unverified` (say who or what can answer). Reporting a `read` as passing
is the lie this whole skill exists to prevent.

## Procedure

1. List the claims this response is about to make.
2. For each, name the proving command (condition 1). No command exists →
   label `read` or `unverified`, never "should work".
3. Run fresh; read the FULL output; record exit code and the line that
   proves or refutes (conditions 2–3).
4. Any claim red or unproven → report the actual state. The seal is
   withheld, not negotiated.

## Seal block

End with this block. Values that cannot be filled honestly stay `none —
<reason>` (an unfillable row is a finding, not an embarrassment):

```
🔏 verify sealed @ <commit-ish>[+dirty: <files>]
· <claim> — <command> → <key output line> (exit <n>)  [executed]
· <claim> — <where read, file:line>                   [read]
· <claim> — unverified; <who/what answers>            [unverified]
· red proven: <how the check was seen failing, or none — <reason>>
```

The block feeds forward: the smith ends reports with it, the warden audits
the seal instead of re-deriving it, and `_ai/` handoffs carry it across
sessions. A seal the warden cannot audit from the block alone was not a
seal.

## Counterfeits (stop on sight)

- Output quoted from an earlier run — freshness is per tree state, not per
  conversation.
- "Tests pass" for a claim no test covers — green suite, unproven claim.
- Satisfaction vocabulary before the run: should, probably, seems, likely.
- A new test that passed on first run and was never seen red (condition 2).
- Partial evidence generalized — one endpoint checked, "API works" claimed.
