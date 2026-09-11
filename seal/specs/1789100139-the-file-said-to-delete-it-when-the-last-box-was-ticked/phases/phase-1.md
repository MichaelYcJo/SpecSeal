# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — phase 1

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `6dfc40f` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

Move `docs/flow.md` §*Order inside a ticket* — its three numbered steps —
into `skills/implement/orchestration.md` as an `Orchestrator:`-prefixed
section, and move `tests/test_the_rules_have_one_owner.py`'s `FLOW` constant
and the two cases that read it rather than deleting them. The two cases pin
that the draft pull request opens between the smith and the warden rounds,
and that step 2 no longer defers the framer to a ticket. Verified by seeing
both cases red against the pre-move tree and green after.

## What this phase found

**The frame undercounted the constant's usages, and the count came from a
grep for the wrong thing.** `plan.md` §Technical context reads
`tests/test_the_rules_have_one_owner.py:61,500` — 2 hits — because
`grep -n "flow\.md"` finds only the lines carrying the literal string. `FLOW`
is used a third time at line 141, as the link carrier for rule 6 in the
`RULES` table, and that line spells the constant rather than the path. The
module would not even collect after the constant was renamed:
`NameError: name 'FLOW' is not defined` at collection, not a test failure.

The class this belongs to is worth naming for the phases after it. A live
reference to a file can be a **path** or a **name bound to that path**, and
the enumeration this work item is built on saw only the first kind. The other
eight files in the table were re-checked for the same shape and none has one:
`tests/test_release_hygiene.py` writes `"docs/flow.md"` as a literal in all
three places, and the two scripts and the four documents carry prose.

**Rule 6's link carrier moved with the section, which is the reason the
constant moved rather than being deleted.** `RULES["6 the draft pull request
opens before round 1"]` lists the owner as `skills/code-review/
orchestration.md` and the carriers as the handoff protocol and — until this
phase — `docs/flow.md`. Deleting the entry would have dropped a carrier the
rule still has: the sentence *the draft pull request opens (… owns when)* is
in step 2, and step 2 is now in `skills/implement/orchestration.md`. So the
carrier is the same sentence at a new address, and the table says so.

**The two cases were renamed, because their names were about the file.**
`test_the_flow_*` named `docs/flow.md`; after the deletion "the flow" names
nothing in the tree. They are `test_the_order_*` now, after the section that
holds the steps. What they assert is untouched.

**Placement is the top of the file rather than the end, and the intro says
why.** `skills/implement/orchestration.md`'s three existing sections are
steps *inside* the sequence this one states — step 1 is "write `routing.md`
before the first edit", which the routing section then details over forty
lines. A reader starting a work item needs the order before any step of it,
so the section is first and the intro's *the three sections* became *the
sections* with a paragraph naming where the fourth came from.

**Nothing forced the heading prefix and the wrap; both were checked rather
than assumed.** `tests/test_a_section_marked_for_one_role_reaches_only_that_
role.py` refuses an `orchestration.md` listed under any agent's `skills:`,
which is what makes an `Orchestrator:`-marked heading safe here — no agent
receives this file. `skills/implement/orchestration.md` is in
`tests/test_docs_line_wrap.py`'s `COVERED` list at 88 columns, and
`docs/flow.md` was not, so step 2 arrived as a single 232-column line and had
to be re-wrapped. `flat()` collapses whitespace before matching, so the
re-wrap does not move what the cases pin.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `FLOW = ("docs", "flow.md")` in `tests/test_the_rules_have_one_owner.py` | `ORCH_IMPL = ("skills", "implement", "orchestration.md")`, in the same file. All three usages moved to it |
| `docs/flow.md` §*Order inside a ticket* — still standing at the end of phase 1 | `skills/implement/orchestration.md` §*Orchestrator: the order inside a ticket* holds it now. The copy in `docs/flow.md` goes with the file in phase 4, which is why two files state the sequence between this commit and that one |
