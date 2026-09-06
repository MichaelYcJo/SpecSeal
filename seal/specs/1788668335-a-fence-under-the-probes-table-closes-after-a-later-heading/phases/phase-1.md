# 1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading — phase 1

<!-- seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 2b6e8f1 |
| Ran by | <left for the orchestrator — the spawn prompt named no model, and the template's own rule is that a segment transcribes this value or leaves it, never sources it from its own idea of what it is> |

## What this phase was asked

Reproduce #169's reported shape at this branch's HEAD before applying the
fix the issue wrote, because that fix is stamped at `da047ab` and the module
has moved. In order: open `section_body` and say what it returns at the
boundary; build the exact input #169 describes and run `new` on it at HEAD,
recording the exit and what the record carried; only then decide what is
owed. If it does not reproduce, close the issue on that evidence and plant
the second case anyway. If it does, fix it — and judge the issue's
`SECTIONS` membership test against the alternative `plan.md` names, because
a refusal keyed to a list of section constants goes stale the day a section
is added.

Then §12: #169 calls the late-closed shape *the one member of the class left
open*. Check that claim by decomposing where a fence can close relative to
the section it opened in, not by listing shapes somebody thought of, and say
how the enumeration is known to be complete.

Plant `test_a_fence_closed_after_the_deferred_table_is_refused` and
`test_prose_under_the_probes_table_stays_in_the_report`, both owed whatever
the reproduction shows. This branch changes the record generator, so it
validates its own records in CI: a refusal added here has to accept every
record this work item will itself produce.

## What this phase found

**The shape reproduces.** `section_body` walks `readable` lines, and
`readable` is `blank_fences(strip_comments(...))` — so a heading inside a
fence is blanked, `section_body` does not stop at it, and the walk runs past
`## Deferred` into the fence's closer. Executed at `c4d7077`: exit 0, the
record carrying `## Deferred` and its row inside the fence while its own
Deferred section read `nothing to drain`, and `chain_check` exiting 0. The
`spec.md` alternative — that the body stops at the next `##` and the shape is
already refused as unclosed — is false, and the reason it is false is the
fence blanking rather than anything about `section_body` itself.

**#169's claim about the class is false, and its proposed fix reaches neither
group it misses.** Decomposing on one boolean over one span — a fence has a
closer or it has not, and where it has one the span either crosses a line the
generator reads the report by or it does not — gives seven members. Measured
at `c4d7077`:

| Member | At `c4d7077` |
|---|---|
| no closer | exit 2, but `never closed` only under the probes table; elsewhere `0 Needs a fix: lines` |
| closer, crosses nothing read | copied whole, correct |
| closer, crosses `## Verdicts` | exit 2, `the report has no ## Verdicts section` |
| closer, crosses `## Executed probes` | **exit 0 — the table silently gone** |
| closer, crosses `## Deferred` | **exit 0 — the section silently gone** (#169) |
| closer, crosses a terminal line | exit 2, `0 Needs a fix: lines` |
| closer, crosses a prose heading | exit 0, and left that way (`spec.md` §Out) |

So **two** members lost a whole table with nothing said, not one; and three
more were caught only by a message that blames the reviewer for a section
they did in fact write. The issue's `SECTIONS` membership test inside
`fenced_after` reaches neither group: a fence that takes `## Executed probes`
means `build` never calls `fenced_after` at all, so no guard living in that
function can see the shape.

**How the enumeration is known to be complete.** It is a partition on a
single boolean over a single span, computed on the report the generator
actually reads — not a catalogue of shapes. Every fence has exactly one
closer state, and where the closer exists the span either contains a read
line or it does not; a boolean has no third value. The seven rows are that
partition crossed with *which* read line, and the fix keys on the span rather
than on the row, so the fix is complete even where the row list is not. That
is the difference from #169's method, which asked *where else have I seen
this* and returned what somebody remembered.

**Where the guard lives, and why the never-closed refusal moved.** One
sentence read over the whole report: *a fence must close, and its span must
not cross a line the generator reads the report by.* Both halves are
report-wide because a fence can open in one section and destroy another —
the unclosed refusal in `fenced_after` had exactly that blind spot. Its
raise is now unreachable and was removed rather than left as dead code.

**The list is not typed a second time.** The guard reads `REPORT_TABLES`'
headings and `TERMINAL_LINES`, which were the module's own statement of what
it reads from the report and had **no reader at all** before this phase — both
constants were defined and never used. A section added later is guarded, and
gets a case, by being added there. The parametrized case asserts the
parametrization equals `REPORT_TABLES`, so the two cannot drift.

**What is refused is a report LOSING a section, never a fence mentioning
one** — and that is what answers the CI constraint. A reviewer of this very
generator pastes record-shaped blocks, headings and all, and a rule reading
the mention would stop the tool on its own review rounds. The guard asks
whether the heading still stands outside the fence.
`test_a_fence_quoting_a_heading_is_kept_while_the_real_one_stands` pins it,
and that case runs `chain_check` over the produced record and reads exit 0.

**A `#` at column 0 is a Markdown heading and a Python comment both**, and
only the fence tells them apart — which is why nothing in the guard reads the
`#` character. Mutating it to a `startswith("#")` test turns both acceptance
cases red, which is the case for the constant-keyed shape rather than an
argument for it.

**#169's second case is real and it was load-bearing to add.** Widening
`fenced_after`'s copy to the whole section body leaves both pre-existing
fence cases green, exactly as the issue recorded, and turns only
`test_prose_under_the_probes_table_stays_in_the_report` red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `fenced_after`'s `never closed` refusal — it read one section, and a fence can open in one and destroy another | `swallowed`, which reads the whole report and raises `NEVER_CLOSED`. The message keeps the words `never closed`, so `test_an_unclosed_fence_under_the_probes_table_is_refused` still pins it; the comment left at the old site says why the raise cannot stand there |
