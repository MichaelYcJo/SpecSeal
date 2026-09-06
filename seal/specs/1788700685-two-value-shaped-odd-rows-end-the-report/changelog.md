- **Two odd rows a transcript can carry still ended `session_cost`'s report,
  and both are values rather than types (issue #175).** `parse_time` states
  this file's rule — one odd row must not end the report — and `count` applied
  it to whether a value is a number at all. Neither reached a value of the
  type a field already carries. A transcript mixing a zone-aware stamp with a
  naive one exited 1 with stdout empty, on the report and on `--json` alike;
  a transcript whose only paired call begins and ends on one timestamp printed
  the span line and then lost the token block and the family table behind a
  `ZeroDivisionError`. Both are closed at a funnel rather than at the sites
  that consumed them: a stamp carrying no zone is read as UTC at `parse_time`,
  the assumption the same line already made when it rewrote a trailing `Z`,
  and a share of a span is taken through a new `share`, which prints a dash
  and one line saying why when the span is not positive. Neither number is
  invented — a share of a span of zero is not 0% and not 100%, and the times
  beside the dash are what was actually measured.

  **The issue named the wrong crash site, and three documents repeated it.**
  #175, `spec.md` and `plan.md` all put the naive-stamp failure in `analyse`'s
  subtractions. Measured: a two-call transcript dies in `load`'s `calls.sort`
  before `analyse` is entered at all — mixing a naive stamp with an aware one
  raises on an **ordering** as readily as on a subtraction — so a guard
  written where the issue pointed would have left the commoner shape standing.
  Normalising at `parse_time` closes eight sites rather than the four the plan
  counted: six subtractions and two orderings. The report's divisions were
  three and not four; the fourth site the plan listed is a multiplication and
  safe at zero.

  **The guard for the span stays in `report` on purpose.** The two shapes do
  not take the same path — a zero span dies inside `report`, which `--json`
  never calls, so `--json` exits 0 on that file already and exit 1 on the
  naive one. Moving the guard upstream into `analyse` would change a number
  `--json` emits correctly today, which is why both cases assert both arms.

  **What the branch is actually about is the ledger row this repairs.** #170
  closed the same rule one axis over and its row states the guarantee over the
  whole class: *no shape a harness can write ends the report*. That row's own
  grounds are a cross product of every field the readers read with the seven
  JSON types and with the field absent — so a value of the type a field
  already carries is outside it by construction. Measured on the module the
  row was stamped against: all eight variants of the `timestamp` field exit 0,
  while a naive stamp and an equal pair of stamps exit 1. The row is
  **under-specified rather than falsified** — every anchor still resolves and
  the four funnels still type-check — so it is corrected in place to name the
  axis its enumeration ran, and the second axis is this work item's own ledger
  fragment. Removing it would have taken the method with it, and the method is
  what found these two.

  **A third shape ends the report too, and it was nearly deferred on a
  measurement of the one field where it does not.** `json.loads` accepts the
  bare tokens `NaN`, `Infinity` and `-Infinity`, and all three are `float`,
  so a type check passes them. `token_thirds` rounds a mean and `round()`
  raises on a non-finite float, which ends the report with exit 1 and stdout
  empty on both arms — worse than either shape above, since the zero span at
  least printed its first line. Every usage field except `output_tokens`
  reaches that `round`, and `output_tokens` was the field the shape was first
  measured on, so it read as harmless. `count` now charges a non-finite value
  0, the direction every funnel in the file already takes.

  **A funnel answers for the values that enter it, and that turned out not to
  be the whole question.** Two counts accepted as finite add to one that is
  not, and the rounding of a mean then ended the report with nothing printed,
  on both arms — a shape that predates this work and was reached through a
  call the enumeration had listed all along, because the question was never
  which operations exist but which values reach them. The mean is now
  computed inside a guard and charged 0 when the file cannot compute it. The
  class behind it is recorded as a limit rather than claimed closed: what
  stays open is that direction, and the wrong-number one where a finite but
  nonsensical count passes every funnel there is.

  **Asking whether a number is finite can itself end the report, so the
  question is asked inside a guard.** `json.loads` builds an
  arbitrary-precision integer from any integer literal, and the finiteness
  test converts to a float before it answers — so a usage field carrying a
  401-digit integer raised `OverflowError` from inside the funnel written to
  keep such values out. That broke a shape which had worked: the same integer
  in `output_tokens` reported normally before the guard existed. It now
  scores 0 like every other value the funnel refuses, which also keeps it
  away from the division one frame later that raises on it for the same
  reason.

  **A negative span no longer prints an idle figure, and says what the
  arithmetic actually measured.** The idle line is shown when idle exceeds a
  tenth of the span, and a tenth of a negative span is negative, so the line
  printed sixty-five minutes of idle beside a span of minus thirty. The
  sentence under such a span said the last result predates the first call,
  which is false whenever the last call to begin is not the last to end —
  the span is taken from the last call to BEGIN, because the list is sorted
  by start. It now says that: the last call to begin ended before the first
  call began, which is what the subtraction computes and is true of every
  negative span. Both shapes are reachable through this work item's own
  normalisation, from a transcript mixing a naive local stamp with an aware
  one.

  **The enumeration that found the first two shapes is also what missed the
  third, and its record now says which node kinds it covers.** The walk
  listed arithmetic and ordering operators and five call names — 60 sites —
  and a builtin numeric consumer carries no operator at all, so the single
  `round` in the module sat outside it. A walk is complete over the node
  kinds it names; recorded as complete over *the operations*, it was a claim
  nobody could re-run. Both shapes were measured absent
  from 299 real transcripts — 0 calls with `start == end`, 94,514 of 94,514
  timestamps zone-aware — so this is a claim repaired, not a live crash, and
  the cases build both transcripts by hand. (#175)
