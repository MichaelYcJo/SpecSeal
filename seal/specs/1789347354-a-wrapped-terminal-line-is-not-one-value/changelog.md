- **A round record no longer loses the rest of a sentence that wraps onto an
  issue number (issues #309, #339).** The reviewer's two terminal lines are
  hand-wrapped prose, and the generator joins them back into one cell. The
  guard deciding where that join stops read a bare `#`, so a continuation
  beginning `#120` was taken for a heading and everything after it was
  dropped — with no refusal, in a repository whose reports open lines that way
  constantly. A truncated cell reads as a finished sentence, so nobody looks.

  **The same guard was wrong in the other direction too.** It asked for a
  space after `-`, `*` and `+`, which a horizontal rule does not have, so
  `---` under the terminal pair was joined INTO the cell instead of stopping
  it. `1) Proof.` passed for the same reason, because the pattern wanted a
  literal dot.

  **The repair is a narrowing, not a longer list of markers.** Every marker
  CommonMark requires a space after now asks for one, and the horizontal rule
  and the setext underline come back as patterns matching a whole line and
  nothing less. It is the same pattern `.github/scripts/issue_claims_check.py`
  has shipped and measured since 0.8.2, which is why the two are now kept
  spelled alike on purpose. Widening the list instead would have bought one
  more silently truncated shape for every marker added.

  **What it does not cover is now written down beside it.** A continuation
  opening with an HTML tag, with `**bold**`, or with an indented run of prose
  cannot be told from a block by its first characters, and the generator joins
  all three rather than guessing. Only a blank line under the terminal pair
  stops every shape, which is what `agents/warden.md` asks the reviewer to
  leave.

- **The rule reaches the document somebody would build a second tool from
  (issue #340).** `docs/review-handoff-protocol.md` defines what a conforming
  tool does with each field and had never been told that a terminal line
  wraps, so a tool built from it would truncate on purpose. It now states
  where the join stops and what the stop cannot reach.
  `templates/sdd-round.md` gained the same thing in the prose about those
  fields and links the protocol for the detail, and `agents/warden.md` keeps
  the half a reviewer acts on — leave the blank line — and names the protocol
  instead of repeating it. Four descriptions of the guard used to call it
  sound; none of them does now.

- **The same defect in the survivor checker is closed with it.**
  `survivor-check` reads a range of commits and reports wording a fix left
  standing elsewhere. It split a sentence at the same false boundary, so
  evidence straddling a wrap scored as two fragments and a survivor could go
  unreported. Nothing was truncated there, which is why it went unnoticed.
