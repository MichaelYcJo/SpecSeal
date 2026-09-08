# 1788817289-local-mode-from-first-setup-to-the-gate — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `50e3e0b` |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Decide where the untracked declaration lands and argue it in `spec.md` rather
than picking, then make `chain_check.py` say which root it searched, so a
local-mode repository stops reading a false *no declaration*.

## What this phase found

**The tempting alternative is not unsafe in the way the codebase's own
docstring warns about, and it is still wrong.** Teaching `--worktree` to read
declarations from the working tree would make the local run STRICTER, not more
permissive: finding a declaration is what makes the check demand round
records, and finding none is the arm that passes with a notice. So
`read_record`'s *more permissive locally than in the place it actually runs*
does not by itself decide it. What decides it is that the local run would then
assert a chain verdict CI can never reproduce — a second guarantee the tree
has to keep true — and that a declaration is committed before the first edit
by rule, so an uncommitted one is not the transient state the flag was built
for. Recorded as Q3 rather than dropped.

**The residual friction is correct and has to be said out loud.** A
local-mode round still prints *examined nothing*. That is local mode's
documented trade — `templates/hygiene.yml`'s header and `implement`
§Bootstrap both say it installs no pull-request checks — and the notice is
that trade surfacing rather than a defect hiding. Anyone reading this later
will want to "finish" the fix; the argument against is in `spec.md`.

**`routing.optin` rather than a second load of the module.**
`hooks/routing.py` imports it by plain name, so it is already in
`sys.modules`; loading it again under a name of this file's own would leave
two module objects answering the one question that module is named for having
one answer to.

**A message change needs its own case even when a behaviour case covers the
same line.** The shared sentence's new half — the prefix and the branch that
were searched — survived every mutation until a case was written for it. *Add
this file* on its own does not say a search happened, and the whole complaint
in #225 is that a reader cannot tell a search that found nothing from one that
looked in the wrong place.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the unconditional *Add seal/specs/<work-item>/routing.md to declare* | `chain_check.py#nothing_declared`, which keeps it for the shared and no-root states and replaces it in local mode; both sentences are pinned in `tests/test_local_mode_reaches_the_review_chain.py` |
