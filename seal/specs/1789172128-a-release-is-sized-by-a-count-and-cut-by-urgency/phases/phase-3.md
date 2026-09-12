# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `e3047d4` |
| Ran by | specseal:smith on Opus 5 |

## What this phase was asked

Define the label and reconcile it with §*A label answers what it is about, and
survives the move*, naming `flow-measurement` as the standing precedent for a
label that is not a topic. The name follows Q2's answer — **(b), the prefix
form** — and the owner chose the form rather than a string, so this phase picks
one inside that constraint and states the grounds. Then apply the criterion to
**#362** and record the answer.

## What this phase found

**The name is `size: now`, and the prefix does more than avoid a collision — it
dissolves the contradiction the frame expected to have to excuse.**

`chain: capped` is the shape already on this tracker: a prefix naming what the
label is about, a value naming the state. Read that way, `size:` is a topic —
sizing, a concern every release has — and `now` is this schedule's verdict
inside it. §*A label answers what it is about* asks a label to name a concern
that outlives a schedule, and the **subject** does; only the **value** is spent
when the release ships. So the section states no second exception, and
`flow-measurement` above stays what it already was: the one label here that is
not a topic at all, a lookup key with an invariant.

That is a divergence from `spec.md`, which expected the label to be *the second
acknowledged non-topic label* with the section stating the exception. Under the
prefix form there is no exception to state, and writing one would have put a
carve-out in the document for a rule the label does not actually break. S6's
substance is met — the section does not leave two rules disagreeing, and
`flow-measurement` is named as the precedent — by resolving the tension rather
than by excusing it. The closing memo carries this as a divergence.

**Why not a bare `now`, recorded because a later reader will want to shorten
it.** Standing alone it is a schedule answer with no subject, which is the half
of a label the rule above requires; and it reads as the ordinary adverb, which
this document itself uses at two coordinates unrelated to labels (lines 193 and
258, checked after the edit). The document says both in one sentence rather
than carrying the argument.

**The label's definition ships before the label exists, and that is Q3's
accepted state.** Nothing in this phase touches the tracker: no label created,
none applied. The document says in so many words that nothing reads it, so the
interval in which it is described and absent costs nothing.

**Three things the definition had to say to be applicable without asking**, and
they are the reason it is four paragraphs rather than one: what carrying it
means and what not carrying it means (two states, no scale); that nothing reads
it and when it comes off, so a reader knows what a stale one costs; and that it
does not decide **which** release the ticket lands in, because a reader who
expected that would come away with a wrong answer from a correct label.

**S4's live test — the criterion applied to #362, and it answers.** Read:
#362 is `documentation`, `from-review`, `release`, unmilestoned, filed by
#359's round 3. Its two findings are a module docstring at
`.github/scripts/release_completeness_check.py:50-51` calling one input's
absence silent where two are, and the same line naming four inputs where the
case pinning them counts five. The ticket's own words are *neither costs
behaviour today; both are prose that a second caller of the script would be
entitled to trust.*

So nothing has to start with #362 in effect: no work item is blocked by the
docstring being wrong, and no gate's verdict moves when it is corrected. Under
the criterion **#362 takes no `size: now` label and rides the next release that
happens to carry it** — which is Q9's expected answer, reached from the ticket
rather than inherited from the question. The criterion decided it without
anybody being asked, and it stopped where the document says it stops: it says
nothing about which milestone #362 then lands in, and this work item assigns it
none.

**What was executed**, exit codes read directly:

| Ran | Exit | Reading |
|---|---|---|
| `bin/test -q` over `test_docs_line_wrap.py`, `test_release_hygiene.py`, `test_one_word_one_meaning.py`, `test_no_real_identifiers.py` | 0 | 70 passed — S9, S8, and the module whose section this phase edits |
| `grep -n "\bnow\b" docs/issues-and-milestones.md` minus the label's own lines | 0 | two ordinary-adverb uses at 193 and 258, which is the claim the new paragraph makes |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
