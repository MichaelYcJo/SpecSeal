# 1788686494-the-printed-ledger-name-collapses-through-relpath — phase 1

<!-- seal/specs/1788686494-the-printed-ledger-name-collapses-through-relpath/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | fa53e67 — the unit and its cases. `762f1b2` carries this record, the ledger fragment, and the one assertion the mutation battery added after the first commit |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Build the display helper and nothing else; phase 2 belongs to a different
segment and must not be started here. One new top-level unit in
`skills/evidence-check/scripts/evidence_check.py` that renders a path as a
name for a person without a lexical `..` collapse, with `plan.md`'s accepted
rule: strip the root's own segments when the path literally starts with them,
otherwise return the spelling verbatim, never fold a `..`. Its docstring says
why `os.path.relpath` cannot be used for a name a person reads, naming #163
and round 13 of work item `1788501054` as the grounds. Unit cases pinning it,
in the test module judged to be the right home, with that judgement written
down here. Every case seen RED first against `os.path.relpath` in the same
position, both runs reported. The cases enumerated by decomposing the input
rather than by listing what comes to mind, with the method stated — and at
minimum `./seal/ledger.md` under `.`, a `..` after a symlinked segment, a path
not under the root, a root with a trailing separator, `.` versus an absolute
root, and Windows separators. Verification narrowed to the touched test module
plus `ruff`; the full suite is the orchestrator's.

Two facts the handoff asked to be settled by reading rather than assumed:
whether any caller passes an absolute root with a relative path or the
reverse, and what the helper does where `seal_home` answers a path outside the
tree.

## What this phase found

**The unit is `display_name(path, root, flavour=os.path)`**, placed directly
after `resolve_patterns`, whose docstring it is the display-side half of. The
two are meant to be read together and now sit together.

**Both handoff facts, settled by reading the call sites.**

- *Absolute or relative.* `main` does `root = os.path.abspath(args.root)`
  before anything else, and both ledger sources are joined under that: the
  `--ledger` arm through `os.path.join(root, pat)`, the default arm through
  `default_patterns(root)` → `seal_home(root)`. So **in every shipped run both
  sides are absolute**, and the handoff's `./seal/ledger.md` spelling is
  reachable only from a direct in-process caller passing `root="."`, which
  `default_patterns(".")` is. Both are pinned anyway; the `.`-root case is
  cheap and the fact that it is not the shipped shape is the sort of thing
  that changes.
- *Outside the tree.* `seal_home` can answer `optin.home_at(root)`, whose
  local-mode arm is `os.path.normpath(os.path.join(root, <git-common-dir>))` —
  absolute when the root is, and **from a linked worktree it sits outside the
  worktree root**. The decision, which is `plan.md`'s accepted alternative
  applied: the header prints that path absolute and verbatim. Longer than
  `relpath`'s `../main/.git/seal/ledger.md`, and it names the file that was
  read from whatever directory the reader is standing in. Pinned by
  `test_a_local_mode_home_outside_the_tree_prints_absolute`.

**The unit slices, it never rejoins.** Rejoining the surviving segments with
`flavour.sep` would respell the separators — and on Windows a `--ledger`
pattern typed with `/` arrives as `C:\proj\seal/ledger.md`, so a rejoin
changes the name the operator typed. Slicing the original substring from the
offset where the root's segments end is what keeps every separator, every `.`
and every `..` exactly as spelled. A mutation confirms it: rejoining turns
`test_a_windows_pattern_typed_with_forward_slashes_keeps_them` red.

**`flavour` exists so a Windows case runs on a POSIX machine.** It is the path
module whose separators and drive rule to apply, `ntpath` for the five Windows
cases. `agent-contract` §13 is the reason rather than convenience: round 14 of
`1788501054` was a red Windows CI leg at a reviewed head, on a case that
asserted the POSIX answer unconditionally, and a case that skips off Windows
is the same defence resting on a guarantee nobody removed. Callers still pass
two arguments, so phase 2 is unaffected.

**Test home: a new module,
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`.** Three
candidates were opened before choosing. `tests/test_evidence_check.py` scopes
itself in its own docstring to "ledger discovery, the CLI surface, and the
exit codes", and the display helper is none of the three.
`tests/test_a_row_points_by_content.py` is the verdict machinery — anchors,
hashes, regions. `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`
is work item `1788501054`'s module, and `spec.md` already assigns the phase-2
**integration** case there because that is where the symlink fixture lives;
putting the unit cases there as well would spread one symptom across a module
named for a different one. This repository names one module per symptom
sentence, and this symptom had no module. Phase 2's source-reading case, which
refuses a future `relpath` on a ledger path, wants the same home.

**How the cases were enumerated.** By decomposing the unit's input — two path
strings and a path flavour — into four axes, then taking the cross product and
pruning to what this program can reach. The axes are written into the module
docstring so the next editor extends the decomposition rather than the list:

- **A, the lexical relation** between `path` and `root`, which is what the
  rule branches on: all of root's segments match with something left · all
  match with nothing left · a segment differs partway · a segment differs at
  the first position · root has no segments at all · root matches as a
  *character* prefix but not a *segment* one · the anchors differ though the
  segments agree · the drives differ.
- **B, what the surviving tail holds**, by segment kind: ordinary · `.` ·
  `..` · `..` reached through a symlink that exists on disk.
- **C, how `root` is spelled**: absolute · `.` · with a trailing separator ·
  one separator alone.
- **D, the separator style**, by flavour: POSIX `/` · Windows `\` · Windows
  mixed, which is what `os.path.join(root, "seal/ledger.md")` produces there.

Eighteen cases. The handoff's six minimum cases all fall out of it, and three
that would not have been reached by listing did too: the character-prefix
sibling (A), the second Windows drive where `ntpath.relpath` raises rather
than answering (A), and the anchors-differ case whose `relpath` answer depends
on the process's current directory (A).

**The decomposition had one hole, and the mutation battery is what found it.**
Six mutations were put in the unit's position one at a time; five turned a
case red and `m4`, the separator set taken from a literal `("/", "\\")`
instead of from the flavour, survived every case. It survives in the *tail*
because the unit slices rather than rejoins — splitting `a\b.md` into two
segments and then slicing from the first returns the same characters either
way. Where it does not survive is at the boundary the root ends on:
`/tmp/proj\seal/ledger.md` is one segment on POSIX, a file named `proj\seal`
under `/tmp`, and it is **not** under `/tmp/proj` — the hardcoded set reads
three segments there, matches the root, and answers `seal/ledger.md`, a name
under a root the file is not under. That is issue #163's own failure shape one
character over. The hole was at the A×D crossing, which the pruning had
dropped as uninteresting. A second assertion now pins it, and the case's
docstring said it was red against that mutation before it actually was — the
claim was corrected in the same edit.

**The red runs.** Two stand-ins, both from `plan.md`'s Alternatives table,
each put in `display_name`'s position by a `test_tmp_*` probe that re-ran every
case (agent-contract §7; both probes deleted before hand-over):

| Stand-in | Result |
|---|---|
| `flavour.relpath(path, root)` — the defect | 11 of 18 red |
| return `path` always — the rejected alternative | 9 of 18 red |
| either | **18 of 18 red** |

The headline reds, read from the output: `assert 'x/ledger.md' ==
'x/lnk/../ledger.md'`, and on the live symlink fixture `assert
'…_test_th0/x/ledger.md' == '…_test_th0/ledger.md'` — the rendered name
reopening a different file from the one the pattern opened, which is the whole
of #163 stated as an assertion.

Nine cases are green against `relpath` by design, and that is the acceptance
row *an ordinary name is unchanged*: where no `..` and no boundary oddity is
involved, the unit agrees with `relpath` exactly, so nothing an ordinary run
prints today moves in phase 2. Those nine are the ones red against
verbatim-always instead.

**What phase 2 needs from here.** `display_name(ledger, root)` is the call.
The five sites `plan.md` names are unchanged and still call `relpath`; nothing
in this phase routes anything, so the printed output of every existing case is
byte-identical and no existing assertion was touched. The scan-suggestion site
at line 627 renders a scanned source path under `repo` and is out of scope per
`spec.md` — note that it also appends `.replace(os.sep, "/")`, which
`display_name` deliberately does not do, so a phase-2 session must not route
it through the helper on the assumption that the two are interchangeable.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds a unit, a test module and a ledger fragment | none |
