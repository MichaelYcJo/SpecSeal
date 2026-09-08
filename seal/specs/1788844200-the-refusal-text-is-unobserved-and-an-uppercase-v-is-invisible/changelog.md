<!-- specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible -->

### Fixed

- **This plugin's own version written with an uppercase `V` was invisible to
  the release check.** The token pattern read a lowercase `v` only, so a
  loaded file naming `V0.9.0` passed a check whose whole job is to refuse
  exactly that number. The prefix now reads either case, and neither guard
  around it moved: a version preceded by a word character is still not one of
  ours — `py3.13.9` names CPython — and a version preceded by a dot is still
  the tail of a longer number. Both of those guards now carry the argument for
  why they exist, written beside the pattern, which is what a reader needed
  before deciding the uppercase case either way.
- **Nothing observed most of what the check prints when it refuses a file.**
  The refusal names the running version, says why such a line is a timer,
  lists the refused lines and offers the routes out — and only the routes were
  read by any assertion. Deleting the refused lines, the running version or
  the whole explanation each left the module green, so a refusal could lose
  the half a person acts on first and no test would say so. All seven of its
  elements — four pieces and the three separators that join them — are now
  pinned one at a time, and every one was seen red on its own deletion before
  the case was committed.
- **Two records described an order bug that never happened.** The exemption
  list of files whose whole job is to name a moment stopped depending on the
  order it is written in, and both the case that pins it and the ledger row
  that records it said the bug had also broken a narrower prefix written after
  a wider one. It never did, in either implementation: every prefix entry
  takes the same date check, so only an exact path can change answers. The
  reason is corrected in both places, and no assertion was added — asserting
  an arrangement that changes no answer is the failure being corrected.
- **The tracker document said the check refuses a real version "whether it has
  shipped or is still ahead".** It refuses versions at or above the running
  one and keeps everything below as history, which is what lets that same
  document say which release an issue shipped in. A reader learning the rule
  from the wider sentence would go looking for history to rewrite. The three
  documents naming the check now agree.
