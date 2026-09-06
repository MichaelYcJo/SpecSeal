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

  **One member of the second axis is left open and recorded rather than
  fixed.** `json.loads` accepts the bare tokens `NaN`, `Infinity` and
  `-Infinity`, all three are `float`, so all three pass `count`'s type check
  and print `nan` in a token column at exit 0 — the wrong number `bool` is
  excluded to prevent, one level down. It does not end the report, which is
  what this work item is scoped to, so it rides as a stamped `# RIDER:` at
  `count` naming its one-line close, and the corrected #170 row names it as
  open rather than closing it by wording. Both shapes were measured absent
  from 299 real transcripts — 0 calls with `start == end`, 94,514 of 94,514
  timestamps zone-aware — so this is a claim repaired, not a live crash, and
  the cases build both transcripts by hand. (#175)
