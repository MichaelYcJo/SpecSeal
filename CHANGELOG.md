# Changelog

## 0.4.0 — 2026-09-02

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered -->
- **The ledger fragments fold into `map.md` at the release, and an open
  evidence-todo row refuses it.** A work item writes its evidence rows to
  `.specseal/map/<work-item-id>.md` so two branches never queue at one file,
  and nothing ever folded them back: the directory gained one file per work
  item forever and almost every pull request touched it. Release preparation
  now runs `.github/scripts/fold_ledger.py --version X.Y.Z` beside the
  changelog gather, in the same commit. It moves every fragment into
  `.specseal/map.md` under a `## X.Y.Z — <date>` heading, one `###` section
  per work item marked with `<!-- specs/<work-item-id> -->`, copies every row
  byte for byte, and removes the fragment. A row is a content anchor, so
  `evidence-check` reports the same thing before and after; measured on this
  repository's own ledger, 55 rows across six fragments all arrived. The same
  step refuses to run, naming the file, while any `specs/<id>/evidence-todo.md`
  in the tree has an open row: a row in a file with no `drained` line whose
  first cell does not begin with ✅. `--dry-run` prints and writes nothing;
  `--check` reports a fragment left behind or an open row, and the hygiene
  workflow runs it on every pull request into `main`. Both halves work on
  today's paths, so the root merge only re-points them. `CLAUDE.md`,
  `CONTRIBUTING.md`, both READMEs, `docs/branch-and-release.md`, the
  `implement` and `evidence-check` skills and the two templates no longer say
  a ledger fragment is never gathered.

<!-- specs/1788331011-two-roots-hold-three-lifetimes -->
- **Two roots become one, laid out by lifetime, and the opt-in is the
  folder.** `specs/<id>/` held a work item's documents and its review
  records, which die at different times, and `.specseal/` held the ledger,
  whose rows outlive the work item. Both now live under `seal/`:
  `seal/specs/<id>/` for the whole work item, `seal/ledger.md` and
  `seal/ledger/<id>.md` for the rows, `seal/follow-up.md` and
  `seal/parity.md` as they were, `seal/README.md` for the export rules. A
  repository is opted in when `seal/` exists at the root (or under `.git/`,
  the place local mode will use); `.specseal/` opts nothing in any more, and
  the throwaway opt-out is the file `.git/specseal-scratch`, which cannot be
  committed. **Behavior that writes to your tree without being asked,
  disclosed on its own line: at the first session start after updating, a
  repository with the old layout is moved once.** Every move is a staged
  `git mv`, `seal/README.md` is rewritten from the template, the ledger rows
  that cite a moved file are re-pointed with their hashes untouched, one
  line says what moved, and the person reviews `git diff --cached` and
  commits. That commit belongs to no work item, so inside a session the
  commit gate asks; `: '[no-review]'; git commit …` waives it for the one
  command, with `[no-parity]` beside it where `seal/parity.md` exists.
  Until that session start every gate is silent in that
  repository, because the signal it reads has moved. A tree with
  uncommitted changes under `.specseal/` or `specs/` is refused with a line
  saying to commit first and retried at the next clean start; a move that
  stopped resumes; a repository carrying `.specseal/scratch` is left alone;
  the once-per-repository marker is `~/.claude/specseal/root-migrated`. To
  move by hand instead — the README's *Coming up from 0.3.x* carries the
  same sequence: `mkdir -p seal/specs`, `git mv .specseal/map.md
  seal/ledger.md`, `git mv .specseal/map seal/ledger`, the rest of
  `.specseal/` into `seal/`, each `specs/<id>` into `seal/specs/<id>`,
  `rmdir .specseal specs`, then `evidence-check --reverify .`, which
  re-points each row citing a moved file. Every gate, checker and release
  script reads the new paths; the `<!-- specs/<id> -->` markers in
  `CHANGELOG.md` and the ledger are unchanged; the chain check no longer
  judges a declaration that a pull request only renamed; `templates/map.md`
  and `templates/specseal-README.md` are `templates/ledger.md` and
  `templates/seal-README.md`. Nothing is deleted: a work item's directory
  lives until a later `settle` folds it.

## 0.3.0 — 2026-09-02

<!-- specs/1788272986-the-fixes-are-what-open-the-next-round -->
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

<!-- specs/1788276387-the-windows-step-never-reaches-its-guard -->
### Fixed

- The evidence-ci guard test resolves the interpreter on Windows: the bash
  step quoted `sys.executable` with backslashes, so the step failed before
  its guard ran and the Windows CI leg has been red since the test landed.
  (`1788276387-the-windows-step-never-reaches-its-guard`)

<!-- specs/1788277657-one-bar-misreads-two-of-the-three-segment-kinds -->
- **The per-segment acceptance bars are written rules, and one bar no longer
  misreads two of the three segment kinds.** The meter the handoff protocol
  points at (`session_cost.py`) had numbers and no rule about what they mean;
  the one figure that existed anywhere was a single acceptance bar on an
  issue, right for a reviewing segment and wrong for the other two. The
  protocol (draft 0.8, §After the run) now says it: a reviewing segment is
  judged on tools per turn **≥ 1.8** (measured range 1.29–1.89, the batched
  round at 1.89 the fastest); an implementing segment on **`repeats = 0`**
  and calls per deliverable, never on tools per turn — an edit-test loop is
  inherently serial (1.08–1.17 measured); a verifying segment is exempt. At
  very small rounds the ratio has few independent batches to rise on (a
  23-call round read 1.64 doing everything right), so the bar is a lens for
  rounds of ordinary size, never a refusal threshold — no gate fails a round
  on it. (#51)

- **A fix pass resumes the implementer instead of respawning it.** The
  code-review skill's orchestrator sections said when the verifying round
  runs and nothing about how the fixing session is obtained. Now they do:
  resume the session that built the branch — its context already holds the
  files, the tests, and the grounds — and spawn fresh only when that session
  no longer exists, with the handoff before round 1 as the price. Measured
  three times with no counterexample: fresh spawn 282 calls / 45 minutes
  (#33); resume 30 calls / 3.9 minutes (#29) and 26 calls / 5.2 minutes
  (the #57 chain). (#51)

- **Q1 of the meter work item is answered: the advisory stays at 1.2.** The
  script cannot tell a reviewer's transcript from an edit-test loop, so its
  threshold sits where it does not nag the serial case; the bars above are
  the orchestrator's instrument, applied knowing the segment kind.
  `session_cost.py` itself is unchanged. (#51)

<!-- specs/1788302682-the-release-check-never-watched-bin -->
- **The release check watches `bin/` now, and a test says which roots it
  watches.** The hygiene step that asks a pull request into `main` for a
  version bump filtered the diff through five roots — `skills/`, `agents/`,
  `hooks/`, `templates/`, `.claude-plugin/` — and `bin/` was not one of them,
  although the plugin loader puts `bin/` on the Bash tool's PATH while the
  plugin is enabled. A pull request fixing only a wrapper would have shipped
  without moving the version, which is the one way an update reaches nobody.
  `bin/` is in the pattern; `docs/branch-and-release.md` names it with the
  others; and `tests/test_the_release_check_watches_what_ships.py` classifies
  every tracked top-level entry as shipping or staying home, so the next
  `commands/` or `output-styles/` fails the suite until somebody decides,
  instead of falling out of the pattern the way `bin/` did. Nothing else that
  a user runs directly lives outside those roots: `install.sh` is run from a
  clone, never through the plugin. (#10)

<!-- specs/1788305134-the-reader-stops-where-it-need-not -->
- **The command reader stopped commits it did not need to stop, and once
  it stopped asking it answered where it should have refused.** A path the
  command wrote out for itself one segment earlier is a path the gate can
  read: `SB=/abs; git -C "$SB" commit` names `/abs`, and the gate's answer
  is byte-identical to the written-out form. Nothing this process cannot
  see is guessed at — `git -C "$WT"` from the environment, `$SB/r$n` in a
  loop, `$(pwd)` and `$1` all still reach the ask — because the substitution
  runs in FRONT of the test that refuses them rather than replacing it. A
  `((` inside a `${…}` word is a word to both paren models, so the heredoc
  below it opens and `echo ${x:-((} <<EOF / cd /target / EOF / git commit`
  is judged where the shell is rather than where the body says. A refused
  segment that carries no name — `fi`, `then echo hi`, a subshell — keeps
  the names the command has written, where every refusal used to empty
  them and `if …; then … fi` prompted for that alone. That aim was proven
  against bash rather than assumed, and the proof found 82 shapes it had
  opened: a body's SECOND statement arrived as a top-level assignment and
  bound, so `if false; then echo hi; SB=/three; fi; git -C "$SB"` answered
  `/three` where bash has `/one`; and `! for SB in …` passed as a simple
  command because only the first word met the reserved-word test. A stack
  of open bodies runs beside the name environment now, and a statement
  inside a body is forgotten rather than bound — a stack, because a
  multi-line `case` puts its arm pattern `a )` where a subshell's closer
  stands and an integer count took it for one. A call to a function the
  string itself defined empties the names it holds, an array assignment
  `SB=(x)` empties the name rather than binding `(x)`, and `((SB=…))`,
  `let` and `${SB:=…}` forget it. The differential that found all of this
  is in the tree as `tests/test_the_reader_agrees_with_bash.py`: whatever
  the reader answers, bash must answer the same, and a prompt is exempt.
  `agents/warden.md` and `agents/scribe.md` say how to write a scratch-repo
  probe that commits without raising the prompt.

<!-- specs/1788310269-the-implementer-leaves-a-mark -->
- **The routing declaration's third axis has a reader now.** `Implementation`
  said whether `smith` or the session builds a work item, and nothing looked at
  the answer again — a session could declare `smith`, build the whole item
  itself, and leave a record saying otherwise. Two hooks close that. When
  `smith` is spawned, a gate in the `pre-agent` group writes the checked-out
  branch name to `.git/specseal-implementer` and prints nothing, so it can
  neither deny nor ask. After a command that actually runs `git commit`, a
  reminder in the `post-bash` group prints one line naming the declaration
  where it answers `smith` and no mark stands for this branch — once per
  session per repository, never a decision, and silent when the mark stands,
  when the row is absent or unreadable, or when it answers `the session`. The
  commit gate's verdict is byte-identical with the row and without it. Both
  fail toward "no mark", which is toward a reminder: a mark gate that quietly
  stops running turns the notice on rather than off. A mark gate broken on
  disk leaves the worktree guard's verdict in the same group untouched, which
  is the objection issue #26 recorded against putting a second gate there,
  measured. `hooks/routing.py`, `templates/sdd-routing.md`, the README's gate
  table and `docs/review-chain-spec.md` no longer say the axis is read by
  nothing.

## 0.2.0 — 2026-09-01

<!-- specs/1788229400-every-branch-appends-to-the-same-two-files -->
- **Every branch appended to the same two files, and one of them broke at the
  merge.** Three branches ran in parallel on 2026-09-01, touched 34 files, and
  shared exactly one — `CHANGELOG.md`, in all three pairs. Nothing else
  overlapped at all, so parallel work was never what conflicted: appending to
  one three-line region was. The cost is when the conflict arrives, after the
  broad gate has run and before the pull request opens, where nothing may be
  edited — so resolving it buys a second run of the whole broad gate. Both
  registries are now written one fragment per work item, and no two work items
  share an id. **A changelog entry goes in `specs/<work-item-id>/changelog.md`**
  and `.github/scripts/gather_changelog.py --version X.Y.Z` concatenates the
  ungathered ones into a dated section at the release; `--check` reports any
  that never arrived, and the hygiene workflow runs it on every pull request
  into `main`, so a release cannot ship a change with no entry. Each gathered
  entry sits under an HTML comment naming its work item — invisible to a
  reader, and the only link from a released entry back to the work that
  produced it. Matching the text instead would have worked once: any later
  copy-edit to a released entry would make its fragment read as ungathered
  forever. `## Unreleased` is gone with the region it named. (#46)

- **A ledger coordinate names content, not a position.** A row cited
  `path/file.py:120-134`, and a line number moves for edits that have nothing
  to do with the claim — so inserting a line above a cited function left the
  row pointing at the wrong lines while still reporting OK. Everything built to
  manage that was compensation: the coordinate rotted, so the row was
  re-anchored, so whatever it was measured from reset, so a stamp was needed,
  so a squash orphaned the stamp.

  **A row now cites `path#unit@hash`**, and `path#unit>place@hash` where a
  claim rests on one statement inside a large unit. The unit is a function or
  class for code and a heading path for a document. `.py` is read with the
  stdlib `ast`; every other language falls to a rule that needs no parser and
  no dependency — the name followed by `(`, `{`, `=` or `:`, then the block to
  the next line at the same or lower indentation, which lands on a closing
  brace because that brace sits at the declaration's own indent.

  **An anchor degrades to DRIFTED, never to BROKEN.** The two cost different
  things: BROKEN says *go edit the ledger*, which is the bookkeeping this
  removes, and DRIFTED says *go re-read the claim*, which is the work the
  ledger is for. So only the unit can be BROKEN. A narrowing anchor whose
  place has changed widens back to its unit and reports DRIFTED — precision
  buys a smaller hash, never a new way to fail. Narrowing is an escape hatch
  rather than a habit: cite the unit, and reach past it only where whole-unit
  hashing has been measured to drift rows on unrelated edits.

  A document anchor is a heading rather than a sentence, because a sentence
  breaks on any rewording while a heading survives the prose beneath it being
  rewritten.

  **Behavior that writes to your tree without being asked, disclosed here on
  its own line: an existing 0.1.0 ledger migrates itself.** At the first
  session start after updating, in an opted-in repository, every `path:line`
  row is rewritten to the new form — stamps dropped, dates kept, and where
  git can produce the file at a row's old stamp, a cited range whose content
  changed since that commit is left loud rather than rewritten onto whatever
  sits at those lines now — and one line tells you what happened:
  *ledger migrated to anchor format (12 rows; 2 left…) — review the diff and
  commit*. `claude plugin update` is the whole of what you do. The write is
  deterministic, idempotent and all-or-nothing per row; the old text stays in
  git history; rows it cannot prove are left, named, and keep failing the
  ordinary check loudly (`OLD-FORMAT`, exit 2) rather than being guessed at.
  It runs once per repository, never over an uncommitted ledger file — the
  dirty check covers exactly the files it would rewrite, and a dirty one is
  skipped with one line and retried at the next clean session start. Fallback for CI or by hand: `bin/evidence-check --migrate .`, which
  the `OLD-FORMAT` line also names.

  **Two behaviours arrive without being asked for.** After a `git commit` in
  an opted-in repository, a broken anchor prints one advisory line in the
  terminal — the row, where its content went if that is provable, and the
  `--reverify` remedy. It never blocks, and it is silent when the ledger is
  clean or absent. And where a BROKEN row's content provably moved — renamed
  in place, or moved to another file, judged by content identity across a
  bounded repo-wide scan — the check names the destination, and
  `bin/evidence-check --reverify .` re-anchors it mechanically; a whole-file
  rename heals the same way. The hash covers the region under the
  anchor with trailing whitespace and blank lines removed, so a reformat is not
  a change; indentation is kept, because in Python a dedent moves a statement
  out of the block it belonged to.

  The verdicts follow from that. **BROKEN** where the anchor is gone, or where
  it resolves to several places and none of them holds the content the row
  recorded — where one of them does, that is the row's place and the run is
  clean. **DRIFTED** where the content under it changed. **OK** prints the
  region's current line numbers, for a reader to open. There is no baseline,
  no stamp and no commit SHA in any row, and the check calls git for nothing
  — the one exception is `--migrate`, which consults the old stamp's commit
  before it trusts a line number it is rewriting.

  **Re-verifying a row is recomputing its hash**, so it has a flag:
  `evidence-check --reverify` rewrites every resolvable row and names what it
  changed. It is deliberately separate from the check — one that refreshed what
  it was checking would report OK for ever — and it leaves a row whose anchor
  is gone alone, because that is the one row somebody has to look at.

  What this closes rather than manages: a stamp a squash can orphan, a row
  whose coordinate resolves while pointing at the wrong lines, a coordinate
  into a file newer than the baseline that could never drift, and a row that
  was stale the moment it landed because another branch changed the cited code
  and merged first. That last one had been recorded as unreachable; a content
  hash sees it on the first run, because there is no time window to look at.
  (#12, #14, #23, #31, #52, #56)

- **The evidence checker stops answering for files it never read.** Nine fixes
  from the fifth review round, each with a case that was seen failing against
  the unfixed code first.

  **A ledger nobody can read now fails the build.** A permissions failure, a
  directory named `.md`, an I/O error — all three used to be indistinguishable
  from an empty ledger, and the run printed all zeros and exited 0. The check
  reports the file as broken, `--migrate` counts it among the rows it left,
  and `--reverify` exits non-zero. Nothing about this is new behaviour anyone
  relied on: a green build over a ledger nothing checked is the state the
  `OLD-FORMAT` verdict exists to prevent.

  **A coordinate is now confined to the repository it is placed in.** A row
  spelling a path that climbs out of the tree — `../elsewhere/file.py#name` —
  was read from wherever it landed, and `--reverify` wrote back a hash of what
  it found there. It is refused in all three commands: broken in the check,
  left by `--migrate`, and untouched by `--reverify`. Whoever writes a ledger
  already has write access to the repository, so this crosses no boundary in
  an ordinary project; it matters where a repository is checked out but not
  trusted, because the plain check and the session-start migration both read
  what the ledger tells them to. Present since 0.1.0 in the `path:line` form,
  so this is a new guard rather than a repair. The containment test is against
  the checkout the row was placed in, not always the root, so a `--map` prefix
  still reaches its own checkout.

  **The ledger writer now follows a symlink and writes the file behind it.**
  A symlinked ledger used to be replaced by a regular file: the real ledger
  never updated, stayed stale, and the command reported success. The rename is
  still atomic, and the mode is carried over — every ledger was being demoted
  from 0644 to 0600, which git does not track outside the exec bit and which
  therefore never appeared in a diff.

  Following the link is a deliberate reversal, and it is the part of this
  entry worth arguing with. A writer that replaces the name it was given never
  writes outside the directory it was pointed at, and that is usually the
  behaviour preferred at a write boundary. It is traded here for the silent
  data loss above, on the grounds that the ledger path is the repository
  owner's own: `.specseal/map.md` and `.specseal/map/*.md`, in a tree whoever
  points them elsewhere can already write to. What would change the answer is
  a ledger path that is not owner-controlled — one taken from an environment
  variable, a command-line argument in a shared runner, or a checkout a
  session does not trust — and at that point the link should be replaced
  rather than followed.

  **The rule that decides what a declaration is now reports how sure it is,
  instead of being asked to be right.** For files this skill reads without a
  parser — everything that is not Python — a list of keywords used to settle
  whether a line declares a name or merely uses it, and that list was wrong in
  both directions at once. It refused two real declarations whose modifiers
  are statement keywords in another language, C#'s `public new void
  Render(int x)` and Swift's `case loading(String)`, reporting live code as
  broken. Letting them back in when nothing else survived then resurrected
  plain call statements, so a function moved to another file with
  `return render(y);` left behind read as though it were still there — and
  `--reverify` made that call site the row's permanent anchor.

  No list of keywords separates those two cases, so the answer stops being a
  list. The rule marks a candidate that survived only by being put back, and
  the two commands act on the mark rather than trying to tell declarations
  from calls themselves.

  - The check accepts such a place only where its content reconstructs the
    row's own recorded hash. Otherwise the unit is gone, and the answer is
    broken-with-the-destination-named — the same answer Python already got
    from its parser, and the one this path was missing.
  - `--reverify` refuses to write onto such a place at all, and prints why. It
    is the command that produces the hash, so it has no hash to compare
    against.
  - What that costs, stated: a declaration whose modifiers look like statement
    keywords and whose content changed in place is re-verified by hand. The
    command names the row rather than skipping it silently.

  A bare `render(1);` is refused on structure rather than vocabulary — nothing
  before the name, and the statement ends — which is kept alongside all of the
  above because it needs no evidence at all. Swift, Kotlin, Go, Ruby and Lua
  end no statement with a semicolon, so the same shape is treated as uncertain
  wherever it spans a single line, and the span is what keeps a real
  declaration out of it: `render() {` opens a block, `render(y)` does not.

  **A row citing a unit the rule is unsure of is written by hand, and the
  check now says how.** It names the place and the hash it holds, so recording
  it is a copy rather than a computation. `--migrate` refuses such a place the
  same way `--reverify` does, with one exception it can prove: where the old
  stamp's commit holds the cited lines unchanged, the person's own line
  numbers vouch for that place and the row migrates.

  **Every row the check calls broken or drifted gets a line back from
  `--reverify`.** Two paths used to answer with nothing at all — a Python unit
  that is gone with no provable destination, and a row whose narrowed claim
  went stale, which is the row the check literally ends with *re-verify*.
  Silence from a heal command reads as a heal that happened.

  **`--migrate` reads the file under the root it was given.** Run from a
  subdirectory, the proof that a cited line range had not moved since its
  stamp was read against a same-named file elsewhere in the repository: an
  untouched row was refused forever, and a row whose look-alike happened to
  match was rewritten and reported as proved.

  **A `--map` declaration no longer turns the rename scan off for local
  rows.** One declared prefix used to switch the scan off for every row the
  run could not place, so a purely local file rename lost both its
  `(moved?)` hint and its `--reverify` heal. A row whose prefix is not among
  the declared maps is a local row and keeps its scan. An unprefixed row in a
  repository declaring `.specseal/parity.md` or `--default-repo` stays
  undecidable — it may be citing the original repository, and nothing in the
  coordinate says which — so those rows keep the scan off, and the skill's
  Known limits now says that the loss is any move rather than a renamed
  directory, and that it costs the `--reverify` heal as well as the hint.

  **The migration that runs itself now prints the warning the typed command
  prints.** `--migrate` reports how many rows were rewritten without the
  since-the-stamp proof; the session-start hook dropped that count, so the
  path a person asked for warned and the path nobody asked for was silent —
  and it never asks twice.

  Known limits also gains two entries it was missing: a one-line constant is
  the most collidable of the boilerplate twins, since substituting the name
  leaves nothing but the value, and a nested `def` is anchored by its
  qualified name — `outer.inner` — with the short name alone resolving to
  nothing until `--reverify` re-anchors it.

- **Three more things the checker used to answer for without having read
  them.** Found reviewing the fixes above.

  **A row read through `--default-repo` is confined to that checkout.** Two of
  the three ways a coordinate is placed already refused a path that climbs out
  of the tree it names; the third did not, so a source file symlinked out of
  the checkout was read and reported clean.

  **`--reverify` stops answering a broken row with silence.** Where the check
  says a row is ambiguous and tells the reader to look, running the heal
  command printed nothing at all, which reads as a heal that happened. Every
  row it leaves alone now gets a line saying which row and why.

  **A declared `--map` prefix no longer affects rows that do not carry it.**
  The per-row test that replaced the per-run one was written with a term that
  could never fire, because a row carrying a declared prefix is resolved into
  the mapped checkout before the question is asked. The term is removed; the
  behaviour it was meant to produce was already there.

## 0.1.0 — 2026-09-01

- **The cost meter could not count above 1.00 tools per turn, and a day's
  conclusions were drawn from that floor.** `session_cost.py` counted a turn
  per `tool_use` block, so a message carrying three calls was three turns
  and the batching ratio was structurally pinned at ~1.00 — five runs of two
  agent types measured exactly 1.00, including a session that demonstrably
  batched. A turn is now one assistant **message** that carries at least one
  tool call, keyed by the message id (a message split across transcript rows
  is one turn; a transcript with no ids degrades to one turn per row — the
  old floor, never an inflated ratio). A message's tokens count once however
  many calls it carries, and model time runs from a turn's last result to
  the next turn's first call, so the wait between two calls issued together
  is no longer booked as thinking. The `batching` advisory stops claiming
  calls go out "one at a time" when the ratio is above 1. Readings taken
  with the old meter are not comparable to new ones: the same six
  transcripts that all read 1.00 read 1.08–1.89 recounted per message. (#29)

  Around the meter, three smaller things move what that measurement run
  established into the documents that outlive it. `docs/review-handoff-protocol.md`
  (now draft 0.6) gains **the handoff before round 1**: the coordinates-carry
  rule applied to the orchestrator→implementer handoff, each handed fact
  labelled executed / read / unverified — an unlabelled fact is an assertion
  nobody has opened, and one such fact (a count standing in for a claim)
  reached five documents before a review round found it false. The same
  section names `plan.md`'s Status column as the progress channel an
  orchestrator reads while an implementer runs — time since it last advanced
  is the stall signal — and finally points at the meter itself, which had
  sat unreferenced through a full day of measurements nobody took. And both
  agent contracts state the batching expectation the meter can now observe:
  independent reads and probes go out together, with the honest caveat that
  an edit-test loop is inherently serial and is not forced to fake a batch.

- **A review run ends with a round that reads the last set of fixes, and the
  record says who did.** A round's findings are closed after it ends, by
  whoever writes the fixes, and the round that follows is what opens them.
  Every round had one except the last, whose fixes were written by the
  session that then ticked `- [x] Pass` on its own record. Measured across
  two consecutive work items: the one round that ever looked at another
  round's fixes found **seven** defects inside them, and its own fixes then
  went in unread. (#33)

  Two changes, and they meet at one cell.

  A run now ends with a **verifying round** — spawned after the previous
  round's fixes are committed, targeted at the diff of those fixes rather
  than at the branch, and asking whether each closed finding is actually
  closed. **A round that opens nothing needing a fix does not consume the
  cap**, because the cap counts rounds that found something and a round that
  finds nothing is the loop having converged. The three-round and five-round
  numbers are unchanged. This is not the rule that a round has to find
  nothing: a 🟡 the smith answers with grounds has opened nothing needing a
  fix, and the run ends there.

  And `round-N.md` carries `| Fixes checked by |` beside `Pass`. `Pass` says
  the findings are closed; this says who opened the work that closed them.
  Three values and no others — `round-N` naming a LATER round, `no fixes to
  check`, or `nobody — <why>`. `chain_check.py` reads it on every record and
  refuses what the repository can contradict: a round naming itself, a
  checker git does not carry, a checker whose own `Target SHA` is the same
  commit as this record's or an ancestor of it — the number is later and the
  review is not — and `no fixes to check` beside a verdict that closed with a
  fix. Where either record's `Target SHA` names two commits — the row allows
  both when HEAD moved mid-review — the newest on each side is compared.

  A verdict cell is read by stripping markdown emphasis and matching the
  vocabulary against the START of the cell, so `**fixed** \`sha\`` counts as
  the fix it is whatever follows the word, while a long `answered` cell that
  mentions a fix made elsewhere still does not. The first version instead
  looked for where the commit began and cut there, which meant it had to
  recognise a commit: a seven-character abbreviation with no digit in it —
  about one in 959 — was not recognised, nothing was cut, and a blocking
  finding that had been properly closed read as still open.

  And `round-N.md` carries `| Needs a fix |`: whether this round opened
  anything that does. It is the reviewer's own answer, copied rather than
  re-derived from the verdict table, because a finding the implementer answers
  with grounds needs no fix and still ends the run. No check reads the row —
  it is there because the answer a run ends on had nowhere to live but a
  transcript. **Existing records are not migrated for this one**, unlike
  `Fixes checked by`: a reviewer who was never asked left no answer, and
  filling the cell in from the verdict table is the derivation the field
  exists to refuse.

  **`nobody — <why>` prints on every run, and fails in one place**: on the
  run's last record, beside a checked `Pass`. That pair is the review claiming
  to have passed while the fixes that closed its findings went unread.
  Anywhere else the cell only prints, because failing for an honest disclosure
  is what teaches people to write none.

  **Work items begun before this release are excused that refusal** and only
  print. The cutoff is the unix second already in a work item's directory
  name, compared against one constant, so nothing needs configuring: a fresh
  install is held to the rule everywhere, and a repository updating the plugin
  has exactly its existing items excused. A check whose first act is red on
  merged history nobody can honestly repair is a check people learn to skip.
  The way out for everything after the cutoff costs no round — one verifying
  round at the diff of those fixes.

  **Every existing round record needs the new row**, not only the newest.
  There is no fallback, for the reason `docs/review-handoff-protocol.md`
  gives for the `rounds/` move: the failure names the row and the three
  values it takes. Write `| Fixes checked by | round-N |` on each record
  whose fixes a later round opened, and `| Fixes checked by | nobody — <why> |`
  on the last one if nothing did.

- **The agent files say that file edits go through the `Edit` tool**, and
  they name both reasons rather than only the familiar one. An edit must be
  able to fail, which is why a shell substitution that misses its pattern is
  an unverified edit. And no Bash command line exists, so the commit gate has
  nothing to read.

  The second reason is what a session hit. The gate reads a heredoc body as
  shell, because a commit hidden in one used to walk straight past it, and
  two kinds of segment count. One has a commit in it: a command word of
  `git` with the `commit` subcommand, which a partial patch to a file
  carrying shell commands as test data can leave in command position, and
  which a document showing a waiver example carries on purpose. The other
  has no commit at all: a segment the reader cannot expand, so an `eval`
  argument holding a variable, a command substitution or a glob stops the
  session with no `git` in the body. Neither command commits anything, and
  the prompt reaches whoever is at the keyboard — in an unattended run,
  nobody. (#34)

  The gate is unchanged. Whether it should skip a heredoc body that is being
  written to a file rather than run is a separate decision, and it is
  recorded as an open question on the work item instead of being made here.

- **A change to a gate now answers for what it costs in interruptions.**
  `CONTRIBUTING.md` asked three things of one — a test seen red, a stated
  failure direction, platform honesty — and none of them was the price the
  change puts on whoever is at the keyboard. A fourth is added: say how many
  times the change stops to ask a person, and if it adds one, say why nothing
  cheaper reaches the same guarantee. It is the item a passing suite cannot
  report on, because nothing counts interruptions. (#43)

  The goal that budget is drawn against is now stated where a design is
  chosen rather than only where a procedure is followed. `implement` already
  carried the reasoning to every session that loads it, but a person deciding
  between two mechanisms reads the ticket and `CONTRIBUTING.md`, and neither
  said a prompt was a cost.

  Nothing changes for anyone installing the plugin. Both files are
  contributor-facing, and `install.sh` distributes only the marker block in
  `CLAUDE.md`, which keeps its size.

- **`writing-style` produced text that satisfied it and could not be read,
  and three things about the file explain why.** (#9)

  **The per-document sections looked complete.** Someone opening the file to
  write a PR body starts at that section, reads its table, and applies it.
  The line saying the sentence rules for their language apply too sits two
  hundred lines above, where they never went. Each of those sections now says
  it at the top: what follows adds to the sentence rules and never replaces
  them.

  **There was no way to notice the jargon was yours.** Every example was a
  word from somebody else's domain, so it read as somebody else's vocabulary
  — while the word learned from this codebase an hour ago already feels like
  ordinary language. A mechanical test replaces the judgment: if you first
  met the word here, in the code or in a policy document, it is jargon. The
  word class that actually leaks is named too, because a list never
  enumerates it.

  **Conversation with the user was not one of the kinds of writing.** It is
  the one written most, and the density that makes a PR body precise makes it
  unreadable. It now has a row in the opening table and a section of its own.

## 0.0.1 — 2026-08-31

- **Initial release.** An implement/review agent chain with hook enforcement,
  an evidence ledger with drift detection, and a tool-agnostic review handoff
  protocol.

  The gates ship opt-in: a repository is judged only once it says so, and
  every gate that cannot read its input fails toward asking rather than
  toward silence. `specs/` holds a work item's documents and
  `.specseal/` holds the ledger that points into the code.
