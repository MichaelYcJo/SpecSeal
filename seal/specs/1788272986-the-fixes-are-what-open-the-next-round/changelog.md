- **A round record names its fix surface, and the check refuses to lose it.**
  Ten regressions on one work item each traced to the fix that opened it, and
  the largest class — four of ten — was a fix that changed a unit's contract
  while not every place that contract reaches was revisited. The diff names
  the changed signature; only a search names the reach; a person reading the
  diff missed all four. So `round-N.md` carries two new rows, filled in when
  the fixes land by the session that already has the fix diff open:
  **`Contract changes`** — every unit whose signature, return arity, return
  type, or set of returnable values the round's fixes changed, each with the
  call sites it reaches (`unit → site, site`, units separated by `;`) — and
  **`New units`**, the top-level definitions and constants the fixes added.
  `chain_check.py` refuses a record without them and refuses a unit listed
  without its reach; `none` is an answer, with or without a reason. Records
  of work items begun before the rule landed print instead of failing — the
  same grandfathering `Fixes checked by` carries, keyed to a new
  `SURFACE_FROM` cutoff — so no merged record goes red. The verifying round
  treats what `New units` names as a finding surface (*is this correct*)
  rather than a verification surface, because a unit the fixes created has
  been reviewed by nobody: the one measured fix commit that created eight
  new units carried defects in four. The handoff protocol moves to draft
  0.7 with the two rows. (#57)

- **Four review-skill rules from the same measurement.** The comparison axes
  table gains a **security row** — who can reach the path and as whom, the
  trust of inputs at OS and process boundaries, whether each failure fails
  open or closed, what a crafted name, path, or payload reaches — because
  security was named in stage 2 and absent from the table, and the table is
  what makes an axis mandatory. The paste-ready-fix rule gains its second
  clause: **a fix touching an OS boundary states its assumed precondition**
  (path resolution, file modes, symlinks, subprocess working directory,
  encoding) — the first clause covers invented names, this covers unexamined
  premises. And two closings are refused in writing: **an enumeration over
  an unbounded domain is a recorded limit, not a closed finding**, and **a
  mutation score licenses *tested*, never *safe*** — stated where the number
  is reported, since three consecutive rounds each reported a perfect score
  and all three were rounds whose fixes opened findings. A third written
  rule, **a document claim gets a pin**, is what the new tests themselves
  practice: every new sentence above is pinned by
  `tests/test_the_fixes_name_their_surface.py` or
  `tests/test_review_axes.py`. (#57)
