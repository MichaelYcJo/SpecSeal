- **A funnel answered for each value that entered, and nothing answered for
  what two of them made (issue #192).** `session_cost`'s `count` checks that
  every token figure a transcript carries is a finite number. `load` then adds
  a turn's `input_tokens` to its `cache_read_input_tokens`, and `token_thirds`
  sums those and divides — so two figures that each passed could add up to one
  that would not, and the report ended with nothing printed at all. That one
  site was fixed in 0.9.2. What was left is every *other* place a computed
  number could reach the same edge, and it is now checked rather than watched
  for: a new site that turns a computed number into a whole number without a
  guard fails the test suite instead of turning up in the next review round.

  **The check finds those places by running the code, not by keeping a list of
  function names.** It reads `session_cost.py`'s own syntax tree, and for each
  call it hands the function a stand-in value that reports back whether it was
  asked to become a whole number, and then asks the same function what it
  answers for an ordinary one. A site counts when both are true. So `round`,
  `int`, `math.floor`, a renamed import, and a helper somebody wrote in the
  file this morning are all found the same way, and none of their names
  appears in the check. That closes the two gaps the previous review round had
  written down as a name list's blind spots — a `from math import …` and an
  `import … as …` — with no name list and no table of aliases to keep in step.

  **What each conversion can fail on is measured, not assumed.** The check
  hands each one the values `count` lets through — an infinity, a
  not-a-number, and an integer too large to have a decimal form — and collects
  what it complains about. A `try` around a conversion has to cover what was
  actually seen, so a guard against one of the two failures is refused; and a
  conversion that cannot fail at all is left alone rather than asked for a
  guard it does not need. The first draft had the two failure names written
  into it, which would have refused the correct guard already in `count`.

  **Three shapes it does not reach, written into the code where somebody will
  meet them.** A list index or slice bound is a whole-number conversion too,
  but telling a computed bound from `len(inputs) // 3` needs to know where the
  value came from, which the check cannot see. A plain division fails on two
  large computed integers without converting anything, and the wider rule that
  would catch it also flags a percentage calculation whose inputs are
  durations — a behaviour change this issue did not ask for. And
  `math.isfinite` converts its argument in order to answer a yes or no, which
  is why it can fail on a very large integer; it is excluded because it does
  not answer with a whole number, and both halves of that exclusion are
  pinned by a test. The first two are written up as questions for the
  repository owner.

  **Verified by breaking it forty-four times.** Every unit the change adds was
  mutated one at a time, and 43 of the 44 mutations turn a test red — including
  the real module with its guard removed, and the real module with one new
  unguarded conversion added in a function nobody would have thought to look
  at. The first pass left five survivors, each a unit no test actually
  exercised, and each now has one; two more survivors were the code being
  wrong rather than untested. The single remaining survivor is recorded in the
  file rather than papered over: one class the check raises internally could
  derive from either of two base classes and no test can tell, because the
  recording happens before the raise.
