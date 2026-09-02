# Questions — every branch appends to the same two files

Three decisions were settled by the repository owner in the routing batch and
are not re-opened here: the changelog is fragmented and gathered at release,
the ledger is fragmented and never gathered, and a ledger row stops carrying a
`Checked` SHA. What follows arrived during implementation.

## Q1 — a row stale on arrival — ANSWERED, by removing the cause

**Two branches, one cited file.** Branch A writes a row citing `code.py`;
branch B changes that code and squashes first; A squashes second. Every
time-window scheme misses it, because there is no interval in which the code
changed relative to A's row — A's row was born after B's change landed.

A content hash has no window to look at. It compares what the row recorded
against what is there, and the two differ on the first run. **Executed**: the
fixture builds exactly that merge order and the row reports `DRIFTED`, exit 1.

This was recorded as unreachable and marked for issue #31. It closes here as a
side effect of the coordinate naming content, which is the honest description —
nothing was built for it.

## Q2 — a SHA in a fragment's prose header — ANSWERED, by removing the cause

There is no header baseline for a prose SHA to be mistaken for. A ledger row
carries its own anchor and hash, so a fragment declares nothing at its head and
`find_baseline` no longer exists.

The narrower fixes that shipped for this in review round 2 — a two-pass header
scan, a bound on accidental prose — went with it.

## Decided and held during the redesign, recorded so no issue is needed

**An AST-based hash for `.py` — REJECTED by the repository owner.** It would
go quiet on comment-only changes, and comments carry load here: `# RIDER:`
comments are scheduled work living at the line they are about. A hash that
shrugs at comments un-schedules them silently.

**Test-anchoring — HELD as a future layer, not built.** A row citing its
proving test, with CI as continuous re-verification, would close the gap Q1
records (a claim whose code and test both moved past it). Held because it
layers ON TOP of content anchoring rather than replacing it, and the layer
underneath had to prove out first.

## Q3 — the generic declaration rule, at the structure signal — ANSWERED

Round 4's 🔴 1 closed a false ambiguity by naming the statement keywords that
may precede a call. Round 5 found that list wrong in both directions: it does
not reach `render(1);`, whose `pre` is empty, and it refuses C# `public new
void Render(int x)` and Swift `case loading(String)`, whose modifiers happen to
be statement keywords elsewhere. A new 🔴 at the site the last one was closing
is `docs/review-chain-spec.md:41`'s structure signal, so the third patch was
not written; the question went to the repository owner instead.

**Answered: the recorded hash breaks the tie, and the blocklist stops being
load-bearing.** `check_ledger` already holds `want` when it reaches the
ambiguity branch and throws it away. Where several places are found, the one
whose content reconstructs the row's own recorded hash is the row's unit; none
matching stays the honest DRIFTED, and two matching are identical spans, so the
choice between them is not a choice.

This reverses the decision written at the branch — *"with two places to look,
an OK would be a claim about whichever one the code happened to pick"*. The
reasoning holds for a checker picking arbitrarily and does not hold here: the
row's own recorded content is what picks, and it is the same evidence the
verdict would rest on either way. What it buys is the end of the loop the
signal was pointing at — a text rule for every brace language cannot be made
correct by enumerating keywords, and after this it does not have to be. A use
misread as a declaration no longer costs a BROKEN, because its span does not
reconstruct the hash.

Swift's `case` therefore needs no ruling. It stays in the list, where being
wrong is no longer expensive.

**One clause was implemented differently, and the grounds are in
`overview.md`.** Where NO place reconstructs the hash the answer here is
DRIFTED; the code reports BROKEN. `--reverify` refuses a row that resolves to
more than one place, so a DRIFTED it cannot heal is exit 1 for ever with no
remedy anybody can run, while BROKEN says *go look*, which is the act that
case needs. Overturn it by saying so — nothing else rests on it.

## Q4 — the same rule, a third time — ANSWERED at the level above, again

Q3 answered the second 🔴 at `generic_units` by letting the recorded hash break
a tie. The fix that carried it also added `return out or blocked`, which brings
keyword-blocked candidates back when none survives — and round 6 found that
those include pure call statements, not only the C# and Swift declarations the
resurrection was written for. A cited function moved to another file, with a
call left where it used to be, now reads DRIFTED instead of BROKEN-with-a-
destination, and `--reverify` anchors the claim onto the call permanently.

Three attempts at one rule is `CLAUDE.md`'s 3+ Fix Rule exactly, and the two
failure modes are one ambiguity: drop `or blocked` and Q3's finding returns,
keep it and this one stands. A vocabulary of keywords cannot separate them, so
no fourth patch was written there.

**Answered: carry the uncertainty out of `resolve` rather than trying to remove
it.** `resolve` knows which candidates were blocked and throws that away, which
is the reason neither consumer can act on it. Returned alongside the places,
the two consumers each answer correctly on their own terms — `check` reports
BROKEN with the repo-wide scan where the places are blocked-only and none
reconstructs the recorded hash, which is the answer round 4's 🔴 2 already
established for `.py` and this path never had; `--reverify` refuses to
re-anchor onto a blocked-only place and prints why, because it is the side that
makes the hash and so cannot use the hash to decide.

What that buys is the end of the separation problem. A blocked C# declaration
whose content still reconstructs resolves correctly, and a declaration that is
gone with only a call remaining fails to reconstruct and goes BROKEN with its
destination named. **The classifier is allowed to stay wrong, because being
wrong stops being expensive** — which is the same shape as Q3's answer, one
level further out.

The narrower option review round 6 also offered — dropping `not pre.strip()`
from the semicolon guard — was rejected. It closes the C family and leaves Go,
Ruby, Kotlin and Lua, and it would have been the fourth edit at the site the
rule says to stop editing.
