# 1789956662-the-gate-and-ci-ask-about-different-ranges — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 6a78a2ee |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The drift pin: one case holding `broad_gate.py`'s base spelling against
`.github/workflows/hygiene.yml`'s. A11, red when either side is edited to
stop naming the remote-tracking ref. The shape is
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`'s
structural half.

## What this phase found

**Each place the workflow names a base is read on its own**, because one
substring search for `origin/${{ github.base_ref }}` would stay green while a
fourth base-taking step was added without it — the earlier three still carry
the string. What this phase built read the `--baseline` and `--range`
arguments and required each to start with the remote-tracking spelling.

**That reader was itself too narrow, and round 1's finding 4 measured it.**
It saw three of the four base-taking steps `plan.md` §*Technical context*
enumerates: it required the flag at the START of a line and a double-quoted
value, so the `BASE: origin/${{ github.base_ref }}` assignment on the
milestone step was invisible to it, as was the most ordinary YAML spelling,
the flag on the same line as its command. The reader now takes each
`--baseline` and `--range` argument wherever it sits on the line, quoted or
bare, plus each `BASE:` assignment, and `base_spellings` takes the file's
contents as an argument so the reader itself can be driven over shapes the
workflow does not happen to use today. A step naming its base some other way
is still unread, and that is written as the reach of the pin rather than as a
promise.

<!-- CORRECTED at round 1, finding 4, and again when the fix pass's own
survivor step reached this file. What this phase originally recorded, kept
verbatim because a record of a past state that quietly becomes true is a
record nobody can audit:

  **The workflow's side is read as arguments, not as text.** … so a new
  base-taking step is covered the day it is written rather than the day
  somebody remembers this case exists.

Two things were wrong with leaving that standing as the rendered claim. It
reads in the present tense while the correction sat in a comment, which
renders nowhere; and it used `text` in the sense of *one blob searched for a
substring* while the same work item's ledger row used it for *the argument
`base_spellings` takes*, which is one word carrying two meanings across two
records — `tests/test_one_word_one_meaning.py` is the rule that names that
shape. The quotation above is excused in this work item's `survivors.md`,
with the grounds that a phase record is a past state rather than a place that
still instructs anybody. -->

**Why the quotation stays**: the checker's pool already excludes a work
item's `rounds/` records, on the grounds that a record quoting a defective
sentence is not a place that still instructs anybody. A `phases/` record is
the same kind of thing and is not excluded, which is a follow-up rather than
something a fix pass may change.

**A format template is not the value it produces, and the first form of the
assertion was wrong about it.** `UPSTREAM_BASE` holds `{ref}@{{upstream}}` —
the braces are doubled to survive `str.format` — so `"@{upstream}" in
UPSTREAM_BASE` is false against correct code. It went red on the true tree,
which is the cheap direction for a wrong assertion to fail in. The case now
asserts the FILLED value, `base@{upstream}`, which is the revision git is
actually handed.

**The link between the two halves is asserted, not assumed.** The workflow
says `origin/<base>` and the gate reaches for `refs/remotes/origin/<base>`.
Those are the same ref under different spellings, and the case binds them:
`REMOTE_BASE` has to END with `REMOTE_LABEL`, and `REMOTE_LABEL` has to be
the prefix the workflow uses. Editing either constant alone parts them and
the case says so.

**A constant nobody reaches for is not a spelling.** The last limb counts the
calls to `resolve_base` in `gate()`, because everything above it could hold
while the gate had stopped resolving — which is the state this work item
started in, with the workflow already right.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds one case and changes no behaviour | none |
