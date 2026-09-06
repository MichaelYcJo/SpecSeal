# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `0128f78` |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Issue #98. Make the comment inside `shipped_templates`, the ledger row that
carries the same sentence, and round 5's summary say what each `git ls-files`
argument does. Correct the docstring that says two fixture documents carry the
only mention of one template. Re-verify the two ledger rows anchored on
`shipped_templates`, because the comment lives inside that unit's hashed
region.

The four quoting variants and the control-character fifth had to be
re-executed here rather than copied from the ticket.

## What this phase found

**The measurement holds on this machine, and it adds one reading the ticket's
block does not show.** git 2.50.1 (Apple Git-155), a scratch repository
holding `templates/spaced name.md`, `templates/한글.md` and a name carrying a
newline:

| Variant | What came back |
|---|---|
| no arguments | `"templates/new\nline.md"` and `"templates/\355\225\234\352\270\200.md"` — quoted and octal-escaped |
| `-z` alone | every name raw, NUL-separated |
| `core.quotePath=false` alone | the Korean name raw; the newline name **still** `"templates/new\nline.md"` |
| both | byte-identical to `-z` alone |

So #98 is right that `core.quotePath=false` alone turns the non-ASCII escaping
off, and right about what `-z` alone adds. The reading the ticket does not
show is the last row: the two listings are identical byte for byte, which is
what makes *"prune `core.quotePath=false` first"* the correct instruction
rather than merely the surviving one.

**Two of the three sites were already annotated and needed nothing.**
`round-5.md`'s finding cell and its summary row both carry round 6's
correction naming issue #98. The handoff said to check what was left rather
than re-correct, and what was left was the ledger row's own clause — which is
the third site, and the one that had travelled furthest. The Korean pull
request body at
`seal/specs/1788360817-…/pr.ko.md` already states the correction too.

**The sibling listing twenty lines below carries the same two arguments and no
comment claiming anything about them**, so it needed no edit. Worth recording
because that call is where round 5's finding 3 landed, and a session looking
for "the other place this sentence lives" will find the arguments there and
have to decide it is not one.

**Three anchors drifted, not two, and the third is phase 1's.**
`evidence-check` named `shipped_templates`, the descends case, and
`docs/issues-and-milestones.md`'s label section. Seven rows in all across the
three. Each row's claim was read against the cases it names — 175 of them,
all passing — before `--reverify` rewrote any hash;
`shipped_templates` moved `b1407676 -> 12c49cdb`. The blanket `--reverify`
rewrote only those seven, which matters because `seal/ledger.md`'s G5 row
carries a note warning that a blanket run can re-stamp S8, a row nobody in
this branch has read. S8 did not drift, so it was not touched.

**The row whose clause stated the false sentence is corrected in
`seal/ledger.md` itself.** That is `CLAUDE.md`'s one exception to the
fragment rule — a row an edit falsifies — and it is not a re-pointing: the
anchor still resolves, and only the content inside it moved. The new claim is
R2 in this work item's own fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *"`-z` alone turns the quoting off, and `core.quotePath=false` alone does not"* | the corrected comment inside `shipped_templates`, and R2 of `seal/ledger/1788735085-…md`; `seal/ledger.md`'s r5 1 / r5 2 row keeps the old wording quoted, marked as corrected, so a reader arriving from round 5 can see what changed |
| the docstring claim that two fixture documents name the same one template | the same docstring, now naming which document names which template |
