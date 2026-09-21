# 1789996775-the-gate-states-what-its-own-fixes-disproved — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 4d8e6f74 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#461. Measure Q2 and Q3 first, then state the property `check-ref-format
--branch` actually has in `names_a_branch`'s docstring (A1), then guard
`moved_line`'s runner clause with the git answer Q3 returns (A2) and rewrite
its paragraph to say what the line now promises. The case asserts the printed
sentence, not the guard, and is seen red first.

## What this phase found

**Q2's answer is not *accepts `@{-1}`*, it is *expands `@{-N}` and then
checks*, and the stdout is what settles it.** The probe read exit codes
directly from `subprocess.run().returncode` in a scratch clone with two
branches and one switch back. `@{-1}` came back exit 0 **with `base` printed
on stdout**; `HEAD`, `HEAD~1`, `base@{u}` and `topic@{1}` each came back exit
128 with *is not a valid branch name*. A command that merely accepted `@{-1}`
would leave open why it is right to let it through; a command that prints the
branch it expanded to makes the property statable, and makes `@{-1}` reaching
the resolver correct rather than a leak. Round 2's finding 10 measured the
same five spellings and this phase re-ran them rather than restating the
table, which is what `questions.md` Q2 asks for in as many words.

**Q3's answer is yes, and the separation holds at both spellings of the
label.** `git check-ref-format refs/remotes/origin/<spelling>` exits 0 for
`base`, `release/v0.12.3` and a short SHA, and exits 1 for `@{-1}`, `HEAD~1`,
`base@{u}` and `topic@{1}`. The bare `origin/<spelling>` label the gate
actually builds separates them identically, so the guard asks git about the
string that is printed rather than about a constructed cousin of it. The
fallback `plan.md` held — dropping the runner clause wherever the given
spelling is not the one the workflow would spell — was not needed.

**`origin/HEAD` is the one spelling that passes Q3's call and never reaches
it**, which is why the two guards are not duplicates. `check-ref-format`
accepts `refs/remotes/origin/HEAD` — a clone really does create that ref — and
`names_a_branch` refuses `HEAD` a step earlier, so no `--base HEAD` ever
builds the label. Round 1's finding 6 is the record of what happens when only
one of the two guards is in place. Neither can be removed on the grounds that
the other covers it, and nothing in `spec.md` said so; it is fed back through
the ledger's W2 row and `overview.md`.

**The red reproduced round 2's finding 10 whole**, which is the strongest form
§15 asks for. Before the fix the case failed at

```
the line names a ref no runner's checkout can hold: broad-gate: --base @{-1}
is 4531912 in this checkout; this checkout says @{-1} tracks origin/base,
which is 99bc0d6 — not the origin/@{-1} a runner reads — origin/base is 1
ahead and 0 behind @{-1}.
```

The A1 case was red separately, at *the docstring does not name the spelling
it accepts*.

**The new unit was mutated alone.** `a_runner_could_hold` rewritten to
`return True` turns exactly one case red — the A2 case — and the other 32 stay
green. Restored from bytes kept outside git, hash checked, `tests/__pycache__`
cleared on both sides.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the docstring sentence *refuses `HEAD`, `HEAD~2` and anything carrying `@{…}`* | the measured property, in the same docstring, and the ledger's W1 row |
| the printed clause *not the `origin/@{-1}` a runner reads* | the third filling of `reads`, pinned by the A2 case, and R4's correction in `seal/ledger.md` |
