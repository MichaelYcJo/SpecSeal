# Changelog

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
