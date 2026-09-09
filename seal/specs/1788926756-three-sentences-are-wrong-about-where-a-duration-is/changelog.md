<!-- specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is -->

### Fixed

- **A run's span could be shorter than one of its own calls.** `session_cost.py`
  took a window's span as the last element's end minus the first element's
  start, over a list sorted by START — so the span ended at the last call to
  *begin*, and a call that outlived every later one ended after the window
  counting it. A background command running 0–1000s beside calls at 10–12s
  and 990–995s gave a span of **995 seconds** for a window holding a single
  1000-second call. The span now ends at the last call to **end**.

  **Nothing this repository has published moves, and elsewhere on the machine
  three printed figures do.** Both rules were computed over every transcript
  under `~/.claude/projects`, on every printed surface the span feeds rather
  than on two of them. Run level: 169 transcripts with calls, one span moves,
  by six thousandths of a second, with its printed span 10.3m either way.
  Row level — which a run-level sweep does not cover, and which is what the
  per-cycle readings publish — 599 spawn-cycle rows, 8 move at all and 2 move
  far enough to change a printed figure. The between-the-rows figure, which is
  what the refusal below is about, moves on 3 transcripts. `idle`, the `model`
  share and the whole-run `command` share move nowhere, and no run switches
  between printing the figure and refusing it. Every move on every axis is in
  another project's transcript; this repository's own directory has 16
  transcripts and not one moving figure. So what makes the published readings
  safe is that per-project measurement and not the rule being harmless, and
  `skills/verify/SKILL.md` now says what a span ends at where a person taking
  a reading meets it.

  **What it does not close, said plainly rather than left to be found:**
  `command` can still print above 100% of the span. `command_s` sums call
  durations and calls can run at once — on that same shape, 1007 seconds of
  command time inside 1000 seconds of wall clock — and one real transcript on
  this machine prints **115.7%** from 5,761 seconds of genuine overlap. The
  old span rule was the smaller of two causes. The larger one is a decision
  about what the number should mean and is with the owner.

- **A negative span claimed less than the arithmetic knew, and claimed it
  about runs that were not negative.** The line under a negative span said
  *the last call to begin ended before the first call began*. That was exactly
  what the old arithmetic computed; under the new rule a negative span means
  **no call** ended after the first call began, and the line says that. The
  narrowing also removes a false reading: a transcript holding one call that
  ran from 10:00 to 12:00, beside a result written before its own call, used
  to report minus sixty minutes for a run that plainly lasted two hours. It
  now reports 120.0m.

- **The between-the-rows refusal named a cause the head row need not carry.**
  Where the rows' spans sum past the run's own, the report withholds the
  figure and says why — and it said *a call outlived a spawn's result*. The
  head row's cut is not a spawn's result: the cut list opens at the first
  spawn's **start**, so a head call can outlive its own row's cut and still
  end before that spawn's result arrives, and the sentence then named
  something the transcript does not carry. It now names *the cut its row ends
  at*.

- **The same refusal printed `by 0.0m` as its grounds for withholding a
  figure.** The magnitude went through a one-decimal formatter, so any overlap
  under three seconds read as the spans having summed past the run by nothing,
  beside a span column whose own figures did not add up to it. The line now
  prints **both sums** — *the rows' spans sum to 33.1m
  against the run's own 16.7m* — and leaves the subtraction to the reader,
  which carries the same fact and never rounds one of the two away.

  Neither printed figure is the rows' overlap, and the reason changed with the
  span rule. Every row's interval now sits inside the run's, so the difference
  is the gaps between the rows *minus* their overlap; where the head row
  covers the whole run there are no gaps and the two coincide, which is
  precisely why naming it the overlap would be a claim that holds on one shape
  and fails in general.

### Added

- **A case for the exact-cover boundary, which nothing pinned.** Where the
  rows' spans sum to exactly the run's own, the report prints the
  between-the-rows figure rather than the refusal — the partition agreeing,
  and the one shape where a reader can watch the arithmetic work. The `>= 0`
  guard that decides it had been probed and never planted; tightening it to
  `> 0` now turns a case red.
