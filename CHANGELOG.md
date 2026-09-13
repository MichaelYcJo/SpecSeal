# Changelog

## 0.11.2 — 2026-09-13

<!-- specs/1789211172-a-round-record-disarms-survivor-check -->
<!-- seal/specs/1789211172-a-round-record-disarms-survivor-check/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`survivor-check` no longer lets a branch's own review paperwork subtract
  the survivor it quotes.** A reviewer's report quotes the defective wording
  verbatim, because that is what a report is for. The check read every path in
  the range as prose, so the quotation counted as wording the fix wrote, and
  the survivor it was about was subtracted before anything was looked for.
  Measured at three tips of one branch: the commit that added only round 1's
  record and report turned a range that had reported its survivor green.

  - **What changes for you.** The gate gets **stricter**, and the first
    branches to meet it are the ones that went through review — which are the
    branches where a survivor is most likely, since a fix pass correcting one
    coordinate is how survivors are made. A pull request into a release branch
    that reported nothing may now report something. The answer is a correction
    or a `seal/specs/<work-item-id>/survivors.md` row with the standing text
    quoted and the grounds written. There is no value meaning *check nothing*.
  - **What does not change.** `bin/survivor-check`'s command line, both
    exemption row shapes, the floor, the scoring, and the report's text. The
    number of sentences a range is measured against does not move either: a
    round record the range only adds removes nothing, and the real range this
    was measured on reported the same 894 files and 16 removed sentences
    before and after.
  - **The exemption path is still open.** Writing a
    `seal/specs/<id>/survivors.md` row silences its survivor a second way —
    the row quotes the standing text, so the commit adding it puts that quote
    inside the range. That is a different mechanism, it was deliberately left
    standing here, and it is tracked as issue **#371**. A `survivors.md`
    written before this release is not armed by this change.

- **The module now says which side each exclusion holds on.** Its docstring
  read *Everything under a work item's `rounds/` is out* and named neither of
  the two functions it had to be true of — the pool that is searched and the
  range that is measured are computed separately, and the exclusion had held
  on one of them since the module shipped. A case pins the new sentence, and a
  second case walks the module for every path list it derives from git and is
  red until each one is filtered or named with grounds. The reason the defect
  existed is that a docstring asserted the class and nothing measured it.

## 0.11.1 — 2026-09-12

<!-- specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked -->
<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`docs/flow.md` is deleted, and this entry is the record of what it
  carried.** It was the third file every branch appended to, after
  `CHANGELOG.md` and `seal/ledger.md`. Those two were cured with per-work-item
  fragments because checkers read them; nothing read this one, so it is cured
  by deletion. No marker is left behind in any file it was removed from — the
  removal is recorded here, in one place, rather than as a trail of notes
  saying a file used to exist. Its 120 lines went four ways:

  - **The order a ticket runs in is now `skills/implement/orchestration.md`
    §*Orchestrator: the order inside a ticket*.** This is the one a person
    has to know: whoever opened `docs/flow.md` each morning for the three
    numbered steps reads them there. It is the first section of that file,
    ahead of the three it already had, because those three are steps inside
    the sequence — step 1 is *write `routing.md` before the first edit*,
    which the routing section then details. Nothing about the sequence
    changed: the draft pull request still opens between the smith and the
    warden rounds, and step 2 still names the framer. The two cases that
    pinned those claims moved with the section rather than being deleted.
  - **The sizing rule is now `docs/issues-and-milestones.md`** — *a release
    is sized in work items rather than in ticket numbers, and three or four
    is the size*, in the paragraph that already says what a `release:`
    milestone holds, with the measurement behind it. It is the only standing
    rule the file carried, and exactly one document states it now. **That
    wording is what this work moved and not what the document says today**:
    the entry below replaces it in this same release with a criterion, and
    names the count as a ceiling.
  - **The 18 checkbox rows and the grounds for their order are on the
    tracker.** Each scheduled release milestone's description states the
    release's purpose and why its issues sit in that order, and a ticket
    whose position had grounds that were in no ticket body gained a comment
    carrying them. Scheduling an issue is one act again — the milestone —
    where it used to be the milestone *and* a line in this file.
  - **The clause naming the file is gone from the 0.4.0 design record**,
    `docs/one-root-by-lifetime.md` §*Order* and its Korean edition. The rest
    of the sentence stands and no version number was added to either, which
    is what marking the path as removed would have cost: both editions are
    in `RECORDS_OF_A_MOMENT` precisely to exempt version tokens.

  Two rules end with the file rather than moving: *a branch writes this file
  for the rows its own work created*, and *a shipped version's section is
  deleted, not kept*. Both were about maintaining it.

  `docs/release-checklist.md` loses four steps, including the one explaining
  how to resolve the conflict this file caused on adjacent lines. The
  quadratic cost that conflict was measured at is still recorded, one bullet
  up, without naming the file. Six live citations were repaired: two in
  `skills/code-review/scripts/survivor_check.py`, one in
  `skills/verify/scripts/broad_gate.py`, one in
  `tests/test_a_corrected_sentence_survives_elsewhere.py`, and in
  `tests/test_release_hygiene.py` the `RECORDS_OF_A_MOMENT` entry with its
  docstring argument and one fixture path. Dropping that entry was measured
  first: seven offending lines remained and all seven were in the file being
  deleted. (#351)

<!-- specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships -->
<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A ticket already merged into the release branch now says so on the
  tracker, and a release can no longer ship a milestone that is not true.**
  An issue's state does not move until `main` moves, and `main` moves once per
  release — so for the length of a release a finished work item and one nobody
  has started looked identical. The line that used to tell them apart was a
  bullet in a checklist every branch edited, and it was deleted with that file
  in the release before this one. Two pieces answer two different questions:

  - **A signal, so a person can tell them apart.** A push to `release/*` runs
    `.github/scripts/label_merged_on_release_branch.py`, which reads the pull
    request numbers out of the commit subjects that arrived, fetches those
    bodies, and puts `merged: X.Y.Z` on every issue their closing keywords
    name. One query answers *what is already in*. It closes nothing: an issue
    closed at the release-branch merge is closed for something nobody has
    received, and the close stays where it was, on `main`. It removes nothing
    either — the labels accumulate, one per release, because deleting a label
    deletes it from every issue that ever carried it.
  - **A gate, so a release cannot ship a milestone that claims work it has not
    got.** A pull request from `release/vX.Y.Z` into `main` runs
    `.github/scripts/release_completeness_check.py`, which refuses while the
    milestone holds an open issue the release branch does not carry, and names
    each one. This is the completeness check the deleted checklist asked as
    *is everything in*, now asked by the machine at the moment the release is
    being cut.

  **The commits are the truth and the label is a cache of them.** The gate
  recomputes what the release carries from the release branch's own range and
  never asks the labels, so a label write that failed cannot block a release —
  the remedy for that would be a person adding a label by hand, which is the
  act the signal exists to remove. The gate does compare the two and says
  which way they disagree: a label naming a release the issue is not in fails,
  because that is always a hand-edit or a squash subject that lost its `(#N)`
  and one command repairs it, while a missing label only reports.

  Neither piece parses anything new. Both read through
  `close_issues_on_release.py`'s existing readers rather than a second copy of
  its treatment of a keyword quoted inside a code fence.

  **A shape the gate cannot judge passes and says why.** A hotfix branch is
  the other thing that reaches `main` and it carries no release milestone. So
  does a milestone that does not exist, and that one says loudly that it
  verified nothing: `gh issue list --milestone` answers a title nothing has
  with an empty list and exit 0, so without a separate existence read a typo
  would have passed the check by measuring an empty set.

  **What a release has to do differently.** `docs/release-checklist.md` step 0
  gains the first box on the list: before anything else, every open issue in
  the milestone that is not shipping moves to another milestone. Leave it and
  the release pull request goes red at step 5 — which is the check working,
  at the worst moment to be doing release planning.

  Two sentences that were false are gone with it. The checklist said the
  close-issues workflow "runs on the tag and closes every issue the changelog
  section names"; it runs when `main` moves and it reads pull request bodies.
  And `docs/issues-and-milestones.md` said *nothing automated reads a
  milestone*, which this change is what makes untrue — that section now says
  what reads one, and that a wrong one costs a blocked release rather than a
  person's wrong answer. (#359)

<!-- specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency -->
<!-- seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A release's size is decided by what has to be in effect before the next
  work item starts, and three or four is now named as the ceiling it always
  was.** The rule used to read *a release is sized in work items rather than in
  ticket numbers, and three or four is the size*, which reads as a target. A
  session holding it read it as one twice in a single day: it proposed moving
  eighteen issues out of the release milestones to bring them "down to size",
  and read a two-item release as under the rule with room for a third. Neither
  of the last two releases was cut at three or four, and neither was a failure
  to reach it — one shipped the agent that writes a frame, because nothing
  could be framed until it existed, and the next replaced a deleted checklist
  with a gate, because the work item after it had to start with the
  replacement already in effect.

  - **The criterion, in `docs/issues-and-milestones.md`.** One change that
    decides how the next ticket runs is a release on its own. The count
    survives as a ceiling — as much as one section can describe while a reader
    still comes away knowing what the release is about — in the wording
    `docs/review-chain-spec.md` already uses for the review cap, so one idea is
    not spelled two ways.
  - **The evidence is cited as prose, not as version numbers, and the document
    says why.** Both releases sit at or above the running version, and
    `test_no_loaded_file_names_a_version_at_or_above_the_running_one` refuses a
    loaded file that names one. Without the note, a later author for whom both
    numbers have become history would replace the descriptions with numbers and
    be right to.
  - **A label, `size: now`, so the judgement is written down once per ticket
    instead of re-answered from thirty-five issue bodies at every cut.** Two
    states: a ticket carries it or it does not, and not carrying it means the
    ticket rides the next release that happens to carry it. No tier list and no
    scale. The prefix is what keeps it inside the rule the same section opens
    with — a label answers *what it is about*, and this one is about sizing,
    which every release has, while only the value is spent when the release
    ships. It is the shape `chain: capped` already has on this tracker.
  - **What does not change is stated, so it is not re-argued.** A `release:`
    milestone is still the pool a release is cut from rather than the release
    itself, `backlog:` is still the unscheduled pool, and nothing schedules
    from either. Nothing reads the new label at all, so a stale one costs a
    reader a wrong answer and costs no automation anything.

  `tests/test_a_release_is_sized_by_a_criterion.py` holds the new wording
  present and the replaced sentence absent, and sweeps the loaded tree for a
  second statement of a release's size. Creating the label and applying it are
  the repository owner's, after this merges.

## 0.11.0 — 2026-09-11

<!-- specs/1789081272-the-writer-of-the-contract-is-not-its-executor -->
<!-- seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The agent that writes a work item's spec is no longer the agent that
  builds against it.** `framer` is a fifth agent definition. Spawn it where
  the SDD ladder already calls for a `spec.md`, and it reads the repository
  widely, collects everything a person has to answer into one batch, and
  writes `spec.md`, `plan.md` and `questions.md`. It writes no code and
  builds nothing. Until now one `smith` did both halves, which left the
  reviewer's *spec compliance first* comparing the work against its own
  description of itself — a contract and an account of what got built are
  not the same document, and nothing in the chain could tell them apart.
  The three writes are named in `agents/framer.md` itself, which is the
  whole of the permission under the §6 that shipped in 0.10.0; no exception
  is carved anywhere, and the definition assigns no broad gate, so §2 still
  names exactly one that does. Nothing existing is renamed and nothing is
  withdrawn: a session that never spawns it works as it did. (#84)
- **The two skills a design gate reaches for move with it, and the smith
  now says whether the drawing holds before building to it.**
  `feature-planner` and `confidence-check` were callable from `smith`'s
  design gate, which is the one moment a build is deciding rather than
  applying — and that moment is the framer's now. Each skill is named as
  callable in exactly one `agents/*.md`, counted from the glob rather than
  from a list, so the next move takes the clauses with it. The other half is
  what the smith gains: **its first act on a frame is to say whether the
  frame holds**, at the head of its requirements phase, with the phase
  record named as where a *no* goes. It happened twice unprompted during an
  earlier build and lived in no document. It sits before the design gate
  rather than after, because a frame judged after that gate is judged after
  its questions have already been put to a person. (#84)
- **A plan now records who approved it and when, and a question records who
  can answer it.** `templates/sdd-plan.md` gains an `Approved <date> by
  <who>` line, written when the builder is spawned, in the spelling
  `templates/sdd-routing.md`'s `Answered` line already has — until now
  nothing told a later session or CI that a person had seen the plan at all.
  `templates/sdd-questions.md` gains a column for **who can answer this
  row** — *a person* · *a measurement* · *the work* — and says outright that
  the framer opens rows without owning their answers. That file held three
  kinds of question and could not tell them apart, so a row a measurement
  settles and a row only the repository owner can settle looked identical,
  and the batch put to a person carried both. (#84)
- **The routing declaration gains a fourth axis, `Planning`, and a session
  that declares an agent it never spawned is told so once.**
  `templates/sdd-routing.md` gains a `Planning` row answering `framer` or
  `the session`, on exactly the terms the `Implementation` row already has:
  optional, absent reads as not answered, and an answer outside the
  vocabulary reads as unanswered rather than as *this file is not a
  declaration* — nothing decides a commit on it, so a typo there must not
  re-ask the review question on a branch whose answer is committed. Every
  declaration already written parses unchanged and reads `planning: None`;
  no migration, and no file has to be rewritten. **It is a record and not a
  fourth checkbox**: the ladder decides when the framer runs, so nobody is
  asked. The mark is a second constant inside `hooks/implementer.py` rather
  than a second module beside it — the file is named for the axis and not
  for the agent, and a mark written by one hook and read by another in two
  spellings is a mark that is written and never found. Spawning `framer`
  writes `<git-dir>/specseal-planner` the way spawning `smith` writes
  `specseal-implementer`, and after a commit where either declared agent
  left no mark, one line names the declaration — **one line for both axes,
  never one each**, once per repository per session, and it never blocks.
  (#84)

## 0.10.0 — 2026-09-10

<!-- specs/1788993115-a-payload-is-written-again-on-every-spawn -->
<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A meter says what each agent's startup payload is made of, and what it
  costs.** `payload-meter`, on PATH beside `session-cost`, reads every
  `agents/*.md`, resolves its `skills:` list to files, and reports the
  definition, each injected `SKILL.md` and the two `CLAUDE.md` files the
  harness adds, in bytes, characters and tokens, per file and in total;
  `--sections` splits each file at its headings, `--json` writes the same as
  data, `--baseline <run.json>` prints the delta against an earlier run, and
  `--calibrate <main transcript>` reads the measured prefix of every agent
  that transcript spawned. **Every token figure carries a basis** —
  `measured (<transcript>)` where it came from a spawn's first `usage`
  block, `estimated (<ratio> B/token, from <agent>)` otherwise — because
  bytes do not track tokens at one ratio: the three agents measured at 2.87,
  3.41 and 3.44 B/token over the bytes their spawns read. Two things the
  measuring found that the issue had not. A payload IS cached across spawns
  of one agent for five minutes, and is re-written on every spawn further
  apart than that — which in a review chain is every one, so the cost stands
  and the sentence is narrower than it was. And a skill name resolves to
  `~/.claude/skills/<name>/SKILL.md` when the user has one, shadowing the
  plugin's; the meter reports the tree's file and says on the row what the
  spawn read instead. A spawn read the tree as it stood when it was made, so
  calibrating against a transcript after the tree changed keeps the earlier
  run's ratio, labels the agent estimated and says to take a spawn after the
  change. (#292)
- **A section written for the orchestrator no longer rides every `smith`
  spawn, and a test keeps it out.** A heading prefixed `Orchestrator:` marks
  a section addressed to the session that spawns agents, and
  `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` fails
  when such a heading sits in any file an agent's `skills:` list injects, or
  when an `orchestration.md` is itself listed. The `implement` skill splits
  the way `code-review` already had: its Bootstrap, its parity setup and the
  whole routing question — three axes, one `multiSelect` question, one
  `routing.md` — move to `skills/implement/orchestration.md`, headings and
  text unchanged, and `skills/implement/SKILL.md` opens with the pointer
  that sends an orchestrator there. What stays in the implementer's half is
  the per-command waiver, because the implementer is who types the
  command. Measured on this tree with no new spawn: 13,727 bytes left the
  smith's payload, an estimated 4,783 tokens at the 2.87 B/token its spawn
  paid; the `CLAUDE.md` pair grew 265 bytes (an estimated 92) for the
  Bootstrap pointer and a comment, so the smith's payload is 13,462 bytes
  and an estimated 4,691 tokens smaller, summed over its files. The rider
  that asked for an arm to be named in one sentence is answered — the
  sentence names the PARITY arm and a migration repository — and deleted.
  (#292)
- **The `CLAUDE.md` block has one source, and what `/specseal:update`
  shows you is a diff against it.** `templates/claude-md-block.md` is the
  block; `install.sh` reads it from there, `.github/scripts/claude_block.py
  --write` regenerates the copy inside this repository's `CLAUDE.md` and
  `--check` fails a pull request where the two differ, so the copy the
  installer used to read and the copy a contributor sees cannot drift again
  (they had, by one sentence). One sentence of the block changed with it —
  a fresh repository is sent to *the Bootstrap section of
  `skills/implement/orchestration.md`* — so every installed block shows
  that one-line diff at the next `/specseal:update`, against the template
  rather than against a `CLAUDE.md`. (#292)

<!-- specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it -->
<!-- seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A fourth agent, `sealer`, takes the one broad run that two agents were
  forbidden and nobody was assigned.** The rule that the full suite runs once,
  after the review rounds settle, has been in this plugin since the beginning,
  and it named who must not run it without ever naming who must: `smith` and
  `warden` are both refused it by the contract's §2, and the act fell to
  whoever happened to be orchestrating. The sealer's whole procedure is one
  command. It reads nothing of the work item — not the specification, not the
  code — runs the checks in order, reads the full output, reports it under the
  three labels, and writes one cell. It judges nothing: a failing check comes
  back with its own lines and no cause and no suggested fix. Its only
  preloaded skill is `agent-contract`, which makes it the smallest payload of
  the four agents at 20 KB, against `smith`'s 99 KB. (#30)
- **A green run prints a seal, and the numbers you need are printed beside
  it.** On success `broad-gate` draws a wax seal — a lily on a disc inside a
  twisted rope — with a panel of readings next to it: the tree and the base the
  run was taken against, the suite's own counts, the exit code your `Broad
  gate` row came back with, the evidence ledger as `N ok · 0 broken`, the
  chain check, and how many review rounds the work item ran. **It never says
  a linter was clean**, because the row is one shell line and nothing in it
  says which part is a linter — a seal that asserted one over a row with none
  in it would be the counterfeit the `verify` skill exists to refuse. The disc is computed from a counted-stitch chart rather than
  drawn as text, so it cannot come out lopsided, and it is emitted with colour
  only where a colour changes. **Where the terminal cannot draw half-blocks —
  a Windows console on a legacy codepage, or any pipe, which is what an agent
  reads through — the same disc prints as letters** at the same width and
  height, so nothing is lost and nothing arrives as question marks. `--shape`
  asks for the letters anywhere, and `bin/seal-stamp` draws one so you can see
  it. **A failing run prints no picture at all** — the words `NOT SEALED`, the
  tree and base, and each failing check with its first lines. (#30)
- **`broad-gate` is a command, where the broad run used to be a command
  assembled from memory each time.** It runs your repository's own broad
  command first, then the four checks every opted-in repository carries —
  the evidence ledger, the unverified-row tally, the review-chain check and
  the survivor check — reading each exit code directly and keeping each
  output in a file. **When a test fails it re-runs only the failing files at
  the base commit**, in a scratch worktree it removes afterwards, and labels
  each failure `new` or `failing on base too`, so a failure that predates the
  work is named as one rather than chased. **Your broad command comes from a
  new `Broad gate` row in `seal/config.md`**, one shell command line, and its
  absence is a refusal rather than a default: `broad-gate` names the row to
  write and exits without running anything. A default would seal a repository
  that runs something else, which is exactly the counterfeit the `verify`
  skill exists to refuse. Put your suite runner first in the row — that is
  what the base comparison re-runs. (#30)
- **`round_record.py seal` writes the broad gate's cell, and it exists because
  `close` could not write it twice.** The cell recording the run has always
  been set by `close --broad-gate`, which also applies a round's fix table —
  and once that table has been applied, `close` correctly refuses to take it
  again, because a second pass would overwrite verdicts the reviewer had
  closed. That left one real situation with no route through it: CI found
  three failures after the gate had already run, the gate had to be re-taken
  at a later commit, and the only way to write the new value was to hand
  `close` a fix table with a header and no rows — which nobody would think to
  do. `seal` is that path with a name. It takes no fix table, reads no verdict
  row, changes the last record's `Broad gate` cell and nothing else, and
  refuses before writing anything when a finding is still open in the last
  record's verdict table, or when the run was taken before the round it would
  seal. `close --broad-gate` still works for the one pass where fixes and the
  gate land together. (#30)
- **A review run that ends at its cap can now be sealed, and could not
  before.** The review chain is bounded — three rounds, five while a red
  finding is open — and a run that reaches the bound closes what is left by
  deferring it, to an issue or to the follow-up list. That produced a state
  with no way out: the record's `Pass` box came out checked, because deferring
  a finding closes it, while the reviewer's own `Needs a fix` line still read
  `yes` from when the round was running, and nothing rewrites what the
  reviewer wrote. The seal refused on that line, so the cell recording the
  broad run could not be written, and the pull-request check then failed the
  branch for a missing cell nothing was able to write. Two rules of the
  workflow contradicted each other, over exactly the case the cap exists for.
  **The seal now asks the verdict table instead of the reviewer's line**: a
  record with nothing still open has ended its run, however the round felt
  while it was running. The other two refusals are unchanged, and the message
  a person sees when a finding really is open now says which of the two rows
  was read. (#30)
- **"After the rounds settle" now names the row a machine already reads.** A
  work item has build phases with a progression of their own and a review
  chain with its own rounds, so the phrase named neither and every reader had
  to guess which. The condition is the last round record's `Pass` box, checked
  — nothing in its verdict table still open — and the `verify` skill states it
  with the reason the box is the row rather than `Needs a fix`. The two agent
  definitions that act on it, the sealer's own definition and the review
  orchestration skill each name the row and point at that section. The proof
  block's `broad gate` line asks for the same thing. (#30)
- **One word named three different things, and now every reference says
  whose.** `seal` meant the mark recording that a review happened, the stamp
  the broad gate prints, and a smith's own proof block — the first two in the
  two agent definitions a reader opens side by side. The rule that resolves it
  is not fewer seals: **every agent seals what it verified, and the one seal
  over the whole project is the sealer's.** The `verify` skill states that and
  names the two things that already tell the final one apart — it covers a
  tree nobody is still editing, and it is the only seal that is drawn, which
  is why the picture prints on success alone. The warden's definition now
  names what it actually keeps, the review mark, and the rule that a document
  naming a thing more than one party can have says whose is written down in
  the `writing-style` skill, so the next such word does not need its own
  conversation. (#30)
- **The rule now names its owner everywhere it is stated.** It stood in nine
  places saying the run was the orchestrator's, or saying only who was
  forbidden it: two agent definitions, `CONTRIBUTING.md`, the review-chain
  specification, the handoff protocol, the review orchestration skill, the
  `verify` skill, the round-record template, and the suite runner —
  both the `bin/test` wrapper and the module it runs, which are one command
  and were two owners until round 1 found the second. All of them now say
  the sealer's and name the definition that assigns it.
  Two more places were not documents at all but the failure messages the
  chain check prints at a refused pull request — the one place a person
  actually reads the instruction — and both now say to spawn the sealer
  instead of telling the reader to take the run by hand. Both agent
  definitions also gained the distinction the rule needed: **asking whether
  anything already covers a case is a coverage probe, not a seal.** Run it,
  and report it as a probe. (#30)

<!-- specs/1789034970-the-contract-is-settled-against-the-agents-that-exist -->
<!-- seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The agent contract no longer contradicts the agent it ships beside.** §2
  forbade the full suite, the repository-wide lint and the typecheck to every
  agent and handed them to the orchestrator, which is not an agent at all —
  and `sealer`, whose entire procedure is that run, received that sentence
  before its first tool call. It shipped with a paragraph in its own
  definition saying so, and that paragraph carried its own expiry. §2 now says
  the broad gate is a single act taken once after the rounds settle, that
  whether it is yours is what your own definition says, and that one
  definition in this plugin hands it over. Nothing about narrow-and-often
  changed, and the three agents whose files stay silent still run none of the
  three checks. (#120)
- **§6 stopped carving exceptions and started naming writes.** It used to say
  an agent writes no durable record, with each real write excepted in the
  definition that held it — two of four agents already had one, and the same
  shape gives five agents four exceptions. It now says *what you write is
  named in your own definition and nothing else*. A definition that names no
  write names none, which is where every agent starts and what the next one
  inherits. The four acts withheld from every agent whatever its file says are
  unchanged: post nothing, push nothing, open no pull request, spawn no agent.
  `warden`'s report and parity mark are the same two writes under a different
  rule, and its definition says so with a bound the old word carried
  implicitly — there is no third. (#120)
- **A probe leaves nothing behind, whatever kind of thing it made.** §7
  defined a probe as one file named `test_tmp_*`, run once, deleted — and a
  probe that creates a git worktree satisfies every word of that while leaving
  something behind. One did, during a review round: its probe files were
  deleted, its report said so, and the worktree surfaced two work items later
  when `git switch` refused a branch a worktree already held. The file rule
  stays, because it is right for the common case and it is what that reviewer
  correctly followed. What is added is that the rule is about leavings — a
  worktree, a branch, a checkout, a scratch clone, a virtual environment — and
  that those are examples rather than a list, because the next leaving is a
  kind nobody has met and an enumeration that predates it reads as permission.
  The rule says whose leaving it is, too: what the probe made for itself is
  what goes, and a thing the repository's own tooling builds to be reused is
  not your probe's leaving even when your probe's run created it. And the
  procedure a reviewer actually follows says the same — `code-review`'s
  Probes row used to state deleting one named file as the whole obligation,
  which is the row the reviewer in the story above was following. (#120)
- **The routing declaration's `Implementation` row now says how to answer
  it.** The row has asked `smith` · `the session` since it was added and has
  never carried a criterion, so it is answered by habit — and the other two
  axes need none, because a wrong answer in either is contradicted at the next
  commit when the gate stops recognising the file. The criterion: is this work
  finding out or writing down? Finding out goes to `scribe`, because a large
  input and a small output is what a subagent boundary is for; writing down
  stays with the session, which already holds the context a delegate would
  re-buy. The one case `smith` answers is a diff large enough to threaten what
  the orchestrator still has to hold — and the threshold there is a number
  nobody has, which the template says rather than inventing one. What it does
  name is the axis: replaceability, not cost. (#120)
- **No section was added, retired or renumbered.** The contract stays one
  file, sixteen sections, so every `§N` in every round record this repository
  has written still means what it meant. Splitting it was weighed and refused:
  the defect was contradiction rather than irrelevance, and a line drawn at
  four agents would be redrawn when the fifth arrives. (#120)
- **A round record's terminal lines may wrap, and the generator no longer
  drops what comes after the wrap.** `Needs a fix:` and `Loses a record or
  crashes:` are the two lines that say whether a review run continues, and the
  generator matched one physical line — so a reviewer whose sentence reached
  the margin had the rest of it silently cut, and the cell still read as a
  finished sentence. It happened to this work item's own round 1, which
  shipped ending mid-clause at *the one that reopens the*. The value is now
  joined across the wrap and stops at a blank line, at the other terminal
  label, or at a line opening a new markdown block, and `agents/warden.md`
  says so where it shows the two lines: **leave a blank line under the pair**,
  which markdown wants anyway. **That last stop is known to be incomplete in
  both directions** — it passes plain prose and stops a continuation beginning
  with an issue number — which #339 carries with the verified fix; the blank
  line is the stop that covers every shape. (#120)

## 0.9.5 — 2026-09-09

<!-- specs/1788908215-the-orchestrator-is-measured-by-the-whole-session -->
<!-- specs/1788908215-the-orchestrator-is-measured-by-the-whole-session -->

### Added

- **The orchestrator was the one segment nobody could measure, because the
  only row it had was the whole session.** Every other segment of a chain —
  a smith, a warden, a scribe — is a transcript of its own, so measuring it
  is measuring one file. An orchestrator's segments are spawn cycles inside
  one file, and there was no way to ask for one of them. So three segment
  kinds accumulated bands a later run can be read against and the most
  expensive one accumulated a single cumulative number that answered nothing.

  `session_cost.py --spawns` slices a transcript at its spawn cycles and runs
  the same analysis over each slice, so a cycle carries the numbers a smith
  row carries — span, command time, model time, calls, tools per turn, mean
  turn gap — and the two can sit side by side. A cycle ends when a spawn
  call's result arrives and begins where the row before it ended: the
  **head** is the framing before the first spawn, **cycle N** runs from spawn
  N-1's result to spawn N's, and the **tail** is the closing work after the
  last one. Every paired call in the transcript lands in exactly one of those
  rows, and the printed table says so by putting its own total beside the
  transcript's.

  **The interval the spawn call itself spans leaves the orchestrator's
  numbers**, because whatever ran in it ran in another transcript and is
  already counted there. It is reported beside the row as `delegated`
  instead. The call stays in the count and in the walk that bounds the model
  gaps, because the orchestrator did make it: on a twenty-minute spawn
  between two checks the row reads four seconds of command time, sixteen
  seconds of model time and twenty minutes delegated, where charging the
  interval reads twenty-one minutes of command time and dropping the call
  outright swallows one of the two gaps.

  **How much of an agent's run that interval covers is the harness's answer,
  and the report now says which answer it is looking at.** Measured on this
  one across 67 spawns of three runs: an `Agent` call pairs in 1.5 to 3.7
  seconds, and each subagent's transcript opens at its spawn's result stamp —
  61 of the 67 within a second, the six misses being subagents of subagents,
  which have no call in the main transcript at all. So the result is written
  when the spawn is **accepted**, the agent then runs for a median of about
  1,000 seconds, and that wall clock is in none of the columns of any row: it
  falls between two rows, because a row's span starts at its own first call
  and its model time never counts the gap before it. So the rows partition
  the run's calls and not its wall clock, and the table now prints how much
  time sits between them — 12 to 31 per cent of the three runs measured, of
  which the wait after a spawn's result is 98 per cent. A `delegated` column
  of seconds is the tell, and the report prints the sentence saying so rather
  than leaving a reader to take zeroes for *nothing was delegated*.

  **A row whose span exceeds its own parts by an hour is a different thing,
  and it is not the agent.** That hour is one gap INSIDE the row, above the
  fifteen minutes model time stops counting at — the orchestrator issuing
  nothing between two of its own calls. Every row over 5,000 seconds in the
  three runs measured decomposes that way, with opening gaps of 6 to 580
  seconds beside internal gaps of 1,038 to 6,285. The `delegated` column
  reads 0 to 3 seconds on those same four rows, which is the point: the
  agent's wall clock is the opening gap and never the column named for it.

  **And where a call outlives the cut its row ends at, the between-the-rows
  figure is refused rather than printed.** Assigning a call by its start is
  what makes the calls partition, and it leaves a long-running one — a
  background command, a suite spanning a cut — in the row it began in while
  the next row has already started, so two rows' spans cover the same
  seconds and sum past the run. The subtraction is then a negative, and a
  negative printed as *the wait* is the one thing this change exists to
  stop; the report prints the two sums and refuses the figure instead. No
  run measured here reaches it.

  **A cycle row is a band and not an attribution**, and the printed report
  says so above the table. Inside one window the orchestrator waits on the
  previous agent, verifies the report it hands over and frames the next
  prompt, and no transcript field marks where any of those ends. Cycle 1 is
  the one row without that window, because the run's own start is a boundary
  a script can take and the framing goes to the head row instead. Splitting
  the acts apart needs a person to label them, which is why it is not what
  this does.

  **Where no spawn is found, the count and the transcript path are printed
  and no table is.** An empty cycle table reads as *this run spawned
  nothing* — and a run that did spawn reads exactly the same way the moment a
  harness stops writing a spawn as an `Agent` block. That is the failure
  shape a wrong family row had for four releases, and it is repaired the same
  way here rather than being discovered the same way twice. (#145)

- `skills/verify/SKILL.md` states the boundary where a session measuring a
  segment reads it, beside the split it already prescribed for a resumed
  agent. That one splits at the user lines the coordinator wrote; an
  orchestrator's boundary is not a user line, and nothing said what it was.
  The paragraph says **spawn cycle** rather than *cycle*, because the review
  chain owns that word for the mark's own unit. (#145)

### Changed

- **Nothing in a reading taken without the new mode moves**, value for value.
  The exclusion of the delegated interval is an argument the plain path does
  not pass, so `--json` and the printed report answer exactly what they
  answered before — the fourth release in a row where a meter change had to
  be weighed against every reading already published. `--json` gains a
  `spawns` key carrying the cycle rows, and a `delegated_s` of 0.0 whose
  meaning is *nothing was removed from the numbers beside it*, never *this
  run delegated nothing*; the `Agent` row of the family table is where that
  second question is answered. (#145)

<!-- specs/1788912166-red-for-following-the-documents-green-for-ignoring-one -->
<!-- specs/1788912166-red-for-following-the-documents-green-for-ignoring-one -->

### Fixed

- **A draft pull request was failed for doing exactly what a document told it
  to do.** `skills/code-review/orchestration.md` opens the draft pull request
  at the end of the build, before round 1, because a reviewer needs a pull
  request to review. So the first thing that happened after the draft opened
  was `chain-check` running against a `rounds/` directory that is empty by
  design — and the arm counting round records failed it. That window was
  documented as *the window's expected state, not a failure to chase*, which
  is a check teaching people to route around it.

  The `Pass` arm a hundred lines down the same walk had been draft-aware since
  the draft state was first read, and its own message says *"Open it as a
  draft while the rounds run"*. The record-count arm now reads the same value:
  on a draft the missing record is printed and the run exits 0, and the notice
  names `ready_for_review` as what re-arms the check. Nothing that can reach
  `main` is exempt — pressing *Ready for review* re-runs the workflow and the
  arm applies.

  **`unknown` stays strict**, and that is the fix's whole safety property.
  `pull_request_state` has three answers, not two: no payload, a payload that
  will not parse, one naming no pull request, and one whose `draft` is a
  string all land on `unknown`, which is judged as ready. A parametrised case
  pins all four, because a harness that stopped writing the flag would
  otherwise turn this fix into a way past the round-record requirement itself.

- **A documented deletion cost 153 written sentences, so nobody was ever going
  to write them.** `survivor-check` reports every place still carrying wording
  a range removed, and a branch that DELETES a shipped section leaves every
  sentence of it standing in the durable copies that are supposed to survive a
  deletion. Measured on one release's own range: **153 places at similarity
  1.60–1.62**, every one correct as a report and not one of them a defect. The
  escape was one row per survivor, which at that size is not an escape — the
  branch turns the step off instead, which is the outcome the escape exists to
  prevent.

  `seal/specs/<work-item-id>/survivors.md` now takes a second row shape,
  `| Range | Grounds |`, alongside the per-survivor `| Path | Quote | Grounds |`.
  The first cell tells them apart, and a path can never be read as a range
  because the dots need a non-space word on both sides. The spec is resolved
  rather than compared as text, because CI spells the range
  `origin/<base>...HEAD` and a person spells it as two commits — those are one
  range.

  **The row is anchored on the range and on the work item it lives in, and the
  second anchor is why the first is not enough.** `origin/<base>...HEAD` is not
  a range, it is a relation, and it resolves to whatever range the checkout it
  is read on is over. Every work item's `survivors.md` in the tree is handed to
  every run, and one lives until the release that ships it, so a single merged
  row in that spelling excused every later branch cut from the same base and
  turned the step off for the rest of the release — the outcome the escape
  exists to prevent, arriving through the escape. A declaration now holds only
  over a range that touches its own work item's directory, which a work item's
  own range always does.

  Both anchors fail loudly. A spec that no longer resolves prints under
  `unresolved`, one refused for belonging to another work item prints under
  `not yours` with that work item named, and neither refuses the run — a
  deleted release branch in an old declaration cannot turn every later check
  into a refusal. Grounds are not optional, and every excused survivor is
  still printed with them: what this removes is the cost of writing 153 rows,
  never the cost of reading 153 lines.

### Added

- **The `Broad gate` cell is read now, and until this release nothing read
  it.** Every round record carries the row and `grep -n broad` over the
  checker matched no line at all, so the one full-suite run this whole design
  turns on could be skipped, or spent before the round it was meant to seal,
  and no gate in the repository had an opinion about either.

  At a **ready** pull request `chain-check` reads the cell on the last round
  record, and it tells four states apart. `not yet` — or no row at all — is
  the run that never happened. A SHA the record's own `Target SHA` descends
  from is the run spent before the round it was meant to seal, and the refusal
  names both commits; that is the more expensive of the two, because the cell
  claims a run happened. A cell with no SHA-shaped word in it names no run and
  fails too: above the cutoff `round_record.py new` writes the row on every
  record and `close --broad-gate` is the only thing that changes the value, so
  such a cell is a choice — and left as a notice, writing `skipped` was a
  shorter way past the arm than deleting the row. Below the cutoff it is still
  reported rather than failed, because records written before it hold free
  text.

  Equal is not premature — `git merge-base --is-ancestor X X` succeeds — so
  the resolved commits are compared before any ancestry question. The passing
  condition is asked directly, *the gate ran at the reviewed commit or after
  it*, rather than as the complement of *premature*: written the other way it
  admitted a gate commit on an unrelated line of history in silence. That case
  is reported now, and a gate SHA this repository cannot see makes no claim at
  all, which is the ordinary state after a squash.

  **A draft is excused it**, for the reason the rounds are still running: the
  broad gate runs once, after they settle.

  **It is bounded by a cutoff, and that is not optional.** Every round record
  ever written defaults to `not yet`, so an arm reading the cell without one
  would be red on every work item in the tree and every one in flight. The
  cutoff is keyed on a work item's id the way the seven before it are, and the
  reasoning is the one they share: a check whose first production act is red
  on history nobody can fix is a check people learn to skip.

### Changed

- **`Broad gate`'s label and its `not yet` sentinel moved** from the script
  that writes the row to the one that now reads it, and the writer imports
  both. Two copies drift silently in the direction that matters — rename the
  row in the writer alone and it keeps writing a row the reader no longer
  finds, which the new arm reads as *no run was named*.

<!-- specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is -->
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
  five printed figures do.** Both rules were computed over every transcript
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

<!-- specs/1788936260-a-case-pins-what-it-actually-measures -->
<!-- specs/1788936260-a-case-pins-what-it-actually-measures -->

### Added

- **`arm-check` asks *would any case notice if this were wrong* of a whole
  module, one branch at a time.** A module's branches were counted by hand
  once, and #262's own table says 33 where
  `hooks/review-history-guard.py` now has 31 — the file changed twice after
  the count was taken. The new checker derives the list from the module's own
  syntax tree instead, makes each branch wrong, runs a command you name, and
  reports the branches nothing notices.

  **There are two ways to be wrong and the answers differ by a lot.**
  Inverting a test asks whether a case would notice it running backwards;
  removing the branch asks whether one would notice it not being there.
  Measured 2026-09-09 on `hooks/review-history-guard.py`, against
  `tests/test_chain_hooks.py`: **12 of 32 branches survive removal, and none
  of the 29 that inversion can be asked of survives it.** A branch counts
  watched when either is noticed. The report prints both rows, says which one
  #262's table of nine compares with — every sentence in that table is about
  taking something out, so a single merged number invites exactly the wrong
  comparison — and names every branch it asked one operator and not the
  other, which is why the two denominators differ: for a handler with one
  type left, inverting it and removing it are the same edit, so it is asked
  once.

  **The walk refuses a syntax it does not recognise instead of skipping it.**
  A checker whose own enumeration goes short prints a shorter count that still
  reads like a total, which is the defect it replaces one level up. So every
  one of this interpreter's 122 syntax-tree constructors is classified — a
  branch-carrying shape, or a non-branch with the grounds written beside it —
  and a Python release that adds one turns a test red rather than quietly
  narrowing the walk.

  **A branch nothing notices is not automatically a defect**, and the report
  says so where it prints them: a branch that cannot be reached, or one whose
  removal changes no behaviour, belongs in that list. It is report-only —
  exit 0 either way.

  **The wait for one command is bounded and the run survives a failed one.**
  `--timeout` defaults to 900 seconds and 0 removes the bound; a negative is
  refused. A command that does not return in time, and one that cannot be
  started at all, is recorded as a branch nothing measured rather than as a
  verdict — so a virtual environment that stops being buildable partway
  through costs one branch instead of the whole run. **It bounds the wait and
  not the work**: only the command's own process is killed, so a command that
  spawns something — a wrapper script running the suite one process down —
  leaves that running. Each branch asks two questions, so a branch can take
  twice the bound.

  **The total says which rule narrowed it.** `assert` and `for`/`else` are not
  counted, by #262's rule rather than because they hold no test, and the
  report names them where it prints the total. A run narrowed with `--only`
  says what it was narrowed out of, so a number pasted into a record does not
  read as the module's.

  Run it as `arm-check <module>` to list the branches, or with
  `--tests "<command>"` to get the verdict. `skills/verify/SKILL.md` §2
  carries the details.

### Fixed

- **A test that pinned a paragraph's wording let three rearrangements of its
  claim through.** `skills/verify/SKILL.md` explains why a command-time share
  can read above 100% — concurrent calls, ordinarily from batching rather than
  from a background command — and the test guarding that paragraph asserted
  four short phrases. Measured one edit at a time: swapping the two causes,
  inverting the measured direction, and putting the old wording back at the
  start of a sentence all **passed**. Each of the three is exactly the
  regression the test was written to stop.

  Every regression it was written against is a *rearrangement of true words*,
  and no substring assertion sees a rearrangement. The two load-bearing
  clauses are now asserted whole and the negative assertion is
  case-insensitive. Verified over five edits, one at a time, with the file
  restored and hash-compared after each: all five now fail, and the three
  above used to pass.

  **Where a paragraph carries a ranking (*this is the ordinary cause, that the
  rarer one*) or a direction (*it came from A and not from B*), the assertion
  has to carry the ranking or the direction.**

## 0.9.4 — 2026-09-08

<!-- specs/1788846800-an-exited-session-reads-as-live-for-five-minutes -->
<!-- specs/1788846800-an-exited-session-reads-as-live-for-five-minutes -->

### Fixed

- **Ending a session made the tree look busy for the next five minutes.** The
  worktree guard has one last check for a session it cannot see as a process —
  a VS Code extension panel, say, which writes this project's files without
  running anything called `claude`. It looked for a recently written session
  file and, finding one, reported someone at work. A session that has just
  *closed* leaves exactly the same trace, and nothing told the two apart, so
  for five minutes after every session in the project ended the guard refused
  branch switches and pushed the work into a worktree nobody needed. The guard
  already knew better one step earlier: sessions leave a note recording which
  process owns them, and that note had already been checked and correctly
  thrown away as belonging to a session that was gone. The recently written
  file then put it straight back. Those notes are now believed on both paths.
  The extension-panel case is unaffected — a live one still owns its note —
  and a session that cannot be checked at all still counts as working, so
  nothing new is ever waved through.

- **Batching commands into one call cost a confirmation the previous release
  had removed.** Since 0.9.1 the first worktree a session creates takes one
  confirmation and the rest take none — but only for a command that creates a
  worktree and does nothing else. Adding a pipe, or a `cd` in front, brought
  the confirmation back, which meant the repository's own instruction to batch
  independent commands into one call was what triggered it. On the 0.9.2
  release run that cost two stops out of five worktrees created. The guard now
  stays quiet for these instead of asking again: it has already had its answer
  about the worktree, and the rest of the command line is judged by your own
  permission settings, exactly as it would be if the guard were not installed.
  Nothing new is permitted — a `sudo` in the command is still judged by the
  rule you wrote for `sudo` — and the first worktree of a session is still a
  question.

### Changed

- The argument for why the guard stays quiet rather than asking again now sits
  with the code that acts on it, instead of only beside one of the two places
  that call it — the one a reader following the other path would never open.

<!-- specs/1788904490-every-published-reading-carries-three-wrong-rows -->
<!-- specs/1788904490-every-published-reading-carries-three-wrong-rows -->

### Fixed

- **A test run this repository actually makes was charged to the row that
  names nothing, and a file write was charged to `test` in the same reading.**
  The meter decided a command was a test run by looking for five names —
  `pytest`, `jest`, `vitest`, `go test`, `cargo test`, `mvn test` — and a
  project that ships `bin/test` matches none of them. Every run of it landed
  in `other`, the row nobody reads because it is the row everything falls
  into. The family now knows a script named `test` invoked by path
  (`./bin/test`, `scripts/test.sh`) and the runners a language's own
  convention names (`make test`, `npm test`, `tox`, `rspec`, `dotnet test` and
  their siblings), so a repository that has said what its test command is in
  the filesystem is read correctly without configuring anything. Measured over
  180 transcripts: **157 calls whose first word is this repository's own
  runner went from 0 charged to `test` to all 157.**

  **The other direction was larger.** A command's whitespace is flattened
  before the family is taken, so a `cat > file <<'EOF' … EOF` that writes a
  document arrives as one line with the whole document in it — and any runner
  named inside it took the call. The classifier now stops at the heredoc
  operator, which answers it for every family at once instead of one word at a
  time: **644 calls the old family charged to `test` are not test runs**, and
  `lint/type` and `build` lose the same kind of false positive. A `<<`
  followed by a lowercase unquoted word is left alone, because in a real
  command line that is more often a quoted comparison than a heredoc and
  cutting there would charge a real run to `other`.

  **What the table still cannot name, it now says out loud.** A runner called
  `bin/check` or `./run-suite` is a name nobody outside that repository can
  guess, and the failure was silent: an empty `test` row reads exactly like a
  run with no tests in it. When `other` leads the table by time, the report
  now says that the largest family names nothing and prints the slowest
  command charged there — the exact string a family would have to learn. It is
  absent when a named family leads. (#200)

- **A round that wrote a full report read as 62 output tokens.** A streamed
  assistant message reaches the transcript as several rows sharing one
  `message.id`, and its `output_tokens` grows across them — the last row
  carries the completed count. The totals kept the first row, so the `output`
  figure was the sum of however much of each message had been written when its
  first row landed. Measured over the same 180 transcripts: 9,098 of 13,425
  messages are split, and the reported total was 4,976,637 against a real
  8,683,844. **The error is not a scale factor**, which is why no reader could
  correct for it — two segments taken the same day were out by 3.2× and 556×,
  with nothing in the printed report saying which.

  Each field is now summed at the **largest** count its message reached. Not
  the last row, though last and largest agree on every one of those 13,425
  messages and no rows arrive out of order: `output_tokens` grows within a
  message, so the largest is the completed count under any row order, where
  last-row-wins is only right under one the format does not promise. The dedup
  itself was right and stays — a message written as one row per content block
  repeats its usage on each, and per-row summing would multiply a run's
  headline number.

  `load`'s per-turn tuple carried a third element, that message's
  `output_tokens`, that **nothing in the file read**. It is removed rather than
  repaired, because what sat there was the same first partial count: a wrong
  number waiting for its first reader, which is exactly how this defect was
  written. The input-side fields it does read are fixed when the request is
  made and repeat unchanged on every row, which is why that reader was never
  affected. (#202)

- **A third the meter could not compute was charged 0, and the line below took
  that 0 for a baseline.** The context line prints when the last third of a
  run's input counts exceeds the first third by half, and any positive number
  clears a threshold of zero. So a transcript whose first third overflowed
  printed `0 → 10 input tokens; later calls cost more than the same call would
  have earlier` — the input had collapsed by 307 orders of magnitude and the
  line said it grew. With the uncomputable third **last** the line was
  suppressed instead, so which direction the reader was told depended on which
  third overflowed. The threshold now requires a first third above zero, the
  same shape as the positive-span guard two functions up.

  A second shape, one function earlier: the filter deciding which turns enter
  the mean was a truthiness test on a signed number, so it **dropped a zero
  and kept a negative**. Six turns whose first three carry minus ten input
  tokens gave a growth of `[-10, 0, 10]` and printed the line off a baseline
  no harness can mean. Zero goes on being dropped and that is not a
  regression: the counter answers 0 both for a field a harness never wrote and
  for one it wrote as 0, so the file cannot tell a turn that spent nothing
  from a turn nobody measured, and a mean is the wrong place to guess. (#193)

### Changed

- **Readings taken before this release and readings taken after it are not
  comparable, and nothing in either says so.** Every per-segment reading this
  repository has published carries all three defects above. The transcripts
  still exist, so any of them can be retaken; whether they are re-derived or
  simply marked is `questions.md` Q1 on this work item, and the marking is
  posted to the open flow-measurement log.

## 0.9.3 — 2026-09-08

<!-- specs/1788890000-the-survivor-step-runs-on-a-range-no-fix-pass-wrote -->
- **The survivor check no longer runs on a release pull request, and says so
  rather than being silently skipped.** The check reports every place still
  carrying wording a range removed, and its unit is a **fix pass's range** —
  the floor it ships with was calibrated over 77 of them. A pull request into
  `main` carries the union of every work item the release holds, which is a
  range no fix pass ever writes: one item's removed wording is scored against
  four other items' prose, and each of those items was already checked at its
  own pull request. The release that shipped the check found this the only way
  it could be found, by failing its own release pull request with 72 places
  reported, none of them a survivor of the range that removed the wording. So
  the step now passes on a base of `main` and prints why, in the shape the two
  steps above it already use — a job-level skip reads as *did not run*, and
  that is the state where the next reader deletes a guard nobody can explain.
  (#180)

<!-- specs/1788873600-the-baseline-is-the-moving-pull-request-base -->
- **Squashing one work item turned every sibling branch red, and the message
  was right about what it measured.** `unverified-check --baseline REF` refuses
  when a work item's `overview.md` was present at the baseline and is gone on
  the branch — an honest arm, because deleting the file was otherwise cheaper
  and quieter than deleting one row from it. But `REF` is the branch a pull
  request merges into, and that branch moves: the moment one work item squashes
  into a release branch, every sibling branch cut before that squash has the
  squashed item's `overview.md` at the base and never had it at all. So each
  sibling was told that rows had left the record when nothing had left and the
  base had moved. On the release that found this, three of four branches paid a
  release-branch merge, a re-run broad gate, a re-pushed pull request and a
  documentation conflict each, and the cost grows with roughly the square of
  the work items a release carries.

  **The baseline is now the fork point.** `REF` is resolved once, to
  `git merge-base REF HEAD`, and every read of the base uses that commit: a row
  present where this branch forked and absent now was removed by this branch,
  which is the only claim the tool makes, and a row that arrived on the base
  afterwards is not this branch's business. Rebasing the stale branch was never
  the way out — every round record names its branch's commits by `Target SHA`
  and every rider carries a `Verified … at <sha>` stamp, and a rebase orphans
  both.

  The repair is applied where the ref is resolved rather than at the arm that
  reported it, because the row-count arm reads the base revision too, through
  `git show REF:<path>`: a base that gains a row in this branch's own overview
  after the fork reported rows the branch never had. Two arms of one refusal
  reading two revisions is the duplicated-reader split this module has closed
  four times, so there is one resolution point and one revision in the report.

  A report names the revision it compared against in the shortest form that is
  true: the ref alone where the merge base is the ref's own commit, and
  `the merge-base of <ref> and HEAD (<short>)` where the base has moved past
  the fork. A `REF` that shares no history with `HEAD` is exit 2 beside the
  `REF` that does not resolve, because a comparison against nothing is not a
  comparison. `docs/release-checklist.md` step 0 carried the workaround and no
  longer needs to; the never-rebase rule that was written inside it stays, as
  the standing rule it always was. (#272)

<!-- specs/1788873610-every-copy-out-of-raw-meets-the-hider-question -->
- **`round_record.py` reads a record back through the shared reader before it
  writes it, and that is the guard's completeness argument rather than a
  list.** #169's guard shipped with an enumeration presented as a two-axis
  grid — the copies the generator makes, crossed with the two passes
  `readable` blanks by — and closed with *a fourth copy would add a row …
  neither exists*. **A fourth copy existed.**
  `round_record.py#inherited_rows` reads every earlier `round-K.md` and takes
  cells out of its raw verdict rows into the new record, and no hider
  question was asked of it. Two copy paths the grid also did not name are
  safe, and the distinction is what the argument was missing: `terminal_value`
  and `close`'s fix-table cells read the comment-and-fence-blanked text, so no
  hider survives them, while the four unsafe ones read the raw file.
  **The row axis had been chosen by listing the copies somebody could see** —
  the third enumeration on that branch and the third to come up one member
  short. What replaces it is a property about the DESTINATION: every copy
  lands in one artefact, so a record read back before it is written answers
  for every copy path at once, including one added next year. One function in
  the module now opens a file for writing, and the argument is a test that
  walks the module's own syntax tree for every writer — a grid can go one row
  short and stay green, and a new writer turns that case red.
  **What it closes that no question asked of a source could.** A comment
  balanced in the report and half in the record: a copied row and a copied
  block are slices of the report, so a comment the report itself balances
  arrives in the record as half of one. Measured before the change — a report
  whose `Grounds` cell opens a comment and closes it on the line below is
  accepted, the generator **exits 0**, the record is written, and
  `## Executed probes`, `## Inherited coordinates` and `## Deferred` each
  resolve to zero occurrences through the shared reader while standing in the
  bytes, with nothing in the run saying a word. That shape had been recorded
  as needing *balance across the slice*, a question the report-wide guard
  could not ask because a copied block may legitimately carry a whole
  comment; asked at the destination it needs no knowledge of which slice took
  the half. And a value that passed through no text at all: `--ran-by` and
  `--broad-gate` are checked for a pipe and a newline because either breaks
  the row they are written into, and an HTML comment opener breaks every
  reader below the row.
  **A comment that opens inside a fenced block and closes outside it is now
  refused by a message naming the comment.** It used to be refused as *a
  fenced block in the report is never closed*, about a report whose every
  fence closes — the comment's span blanks the block's own closing fence one
  pass earlier, so the fence question is asked of a text whose closer is
  already gone. The reviewer was sent to look for something that is not
  there, which is the defect the same chain's round 2 had already fixed once
  for the other order of the two questions. Telling the two apart is the
  fence question asked of the raw text as well, and both texts that are asked
  — the report and the round paragraph — get their own sentence, because a
  reviewer told *the report* looks in a different file from one told *the
  round paragraph*. Every refusal now names the line the hider opens on,
  found by asking the reader's own pass of each prefix rather than by a
  second reading of where a marker sits.
  **The order of the two questions is now written once.** An unterminated
  comment blanks the closing fence of every block below it, so the comment
  must be asked first or the refusal names the wrong hider — a rule that is a
  property of the reader's pass order and not of any one text, and that had
  been written out once per text, twice, with a third text due.
  **What is left, named rather than assumed**: a hider in a text read for
  named sections can make the generator read LESS than the text holds — a
  verdict row whose coordinate is not inherited, a `New units` entry a depth
  walk does not see, a fix row reported as never written. All three are
  refused loudly today and none of them writes a hider into a record, and
  each refusal talks about cell arithmetic rather than about a comment.
  Closing it takes a question scoped to the section each text is read for,
  because a whole-text question there refuses a file this repository already
  has. It is recorded at the coordinate with that measurement. (#182)

<!-- specs/1788873620-two-in-range-values-make-one-that-is-not -->
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

<!-- specs/1788873630-the-orchestrator-sections-leave-the-reviewers-payload -->
- **More than half of the review skill was addressed to the orchestrator, and
  a reviewer read all of it at every spawn (issue #265).** The five sections
  `skills/code-review/SKILL.md` prefixed `Orchestrator:` were 24,948
  characters, 53% of the file, and a `warden` spawn received them before its
  first tool call. A reviewer acts on none of them: it does not decide whether
  a run ends, does not resume an implementer, does not open or mark a pull
  request, and does not post. **They now live in
  `skills/code-review/orchestration.md`**, which the skill names in a pointer
  where its intro ends, so a session orchestrating a review run meets the
  path before it reads any of the reviewer's material.

  **The seam is the author's, not this change's.** The five sections were one
  contiguous block — lines 236 to 653 — and every heading in that run carries
  the prefix while nothing outside it does. The 418 removed lines are
  byte-identical to the file that now holds them, and the three ledger rows
  that were anchored on those headings came back from `--reverify` with the
  hashes they had before the move.

  The headings keep the `Orchestrator:` prefix, so every reference names the
  section it always named and only the file changed.

- **Three of `writing-style`'s four per-document sections are not a
  reviewer's, and they left the reviewer's payload too.** 「PR 본문에만」,
  「다른 팀에 답할 때」 and 「사용자와의 대화에만」 moved to
  `skills/writing-style/outside-the-review.md`; 「리뷰 코멘트에만」 stayed,
  because that one is the only writing a reviewer does. `writing-style` is
  still in both `warden`'s and `smith`'s `skills:` list — the file moved, not
  the list.

  **No style check was built, and that is the decision rather than the
  omission.** Moving the whole skill out of preload would trade a guarantee
  for a saving and pay for it with an instruction, and #180 is seven measured
  instances of a rule written down and then re-broken. Whether a style rule
  can be checked mechanically is still open.

- **What a `warden` spawn reads goes from 108,399 bytes to 78,109**, measured
  with `wc -c` over the three files its `skills:` list names plus its own
  definition.

  **This is occupancy, not speed.** Prompt caching flattens the repeat price
  within a session, so there is no per-spawn token saving to claim and no
  wall-clock reading behind any of these figures — the meter this repository
  publishes is wrong until #200 and #202 land. What the numbers say is that
  the characters occupied the context window on every spawn whether they came
  from cache or not, and that a round killed and re-run paid the full write
  again.

- **Both enumerations of what the split would cost were taken by grep, and
  both were short.** Recorded because the enumeration is the release this
  ships in.

  The check that *no reference crosses the seam* greped the literal
  `Orchestrator:`, which matches the five `##` headings and none of the seven
  `###` subsections beneath them. Re-taken by construction over every heading
  in the block, four live references appear that the grep could not see —
  `agents/smith.md` and `skills/implement/SKILL.md` name one subsection,
  `tests/test_a_record_precedes_the_fixes_it_commissions.py` names another,
  and `docs/review-handoff-protocol.md` names a `##` one twice.

  *Eleven test modules pin the path* is eleven by path and **21** in fact: ten
  more name the file as the Python tuple `("skills", "code-review",
  "SKILL.md")`, which no path grep reaches. Six of the eleven needed no change
  at all, five modules the estimate never named broke, and
  `tests/test_docs_line_wrap.py` is the one that could not have been caught by
  running anything — it reads a fixed list of paths, so 418 lines of
  wrap-covered prose leaving a listed file lose their guard with nothing going
  red.

<!-- specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks -->
- **A fix repaired the coordinate a finding named and the same claim stayed
  standing somewhere else, seven times, and now a check looks.**
  `survivor-check --range <a>..<b>` takes the range a fix pass wrote and
  reports every place in the tree that still carries wording the range
  removed, naming the path, the standing text and the corrected sentence it
  matched. It runs at the fix pass, in the smith's verify step, and on every
  pull request. `agent-contract` §12 has said *do not fix the coordinate*
  since 0.7.0 and reaches every agent at startup; #229 measured the same class
  in another repository, over a documentation work item whose findings per
  round ran 13 → 8 → 5 → 6 and never converged, with 3 of its 4 rounds
  repeating an earlier finding in a different file. So this release ships the
  check rather than an eighth sentence. (#180)

  **It was built against two events in this repository's history and is seen
  failing on both.** One commit reworded a sentence in `agents/warden.md` and
  left its pin behind in a test module that then sat red through two review
  rounds and two broad gates, because no reviewer may run the broad gate
  (#269). Another corrected a docstring and left the identical claim in two
  ledger rows, one of them the shared file a reader meets first (#267). A
  literal grep finds neither: the first is one sentence split across two
  adjacent string literals, so no line holds it, and the second is a
  paraphrase whose longest identical run is three words.

  What a survivor scores is **the number of independent phrases it shares that
  occur nowhere else**, so the threshold means the same thing in a twenty-file
  repository and a thousand-file one, and it is calibrated over 77 real
  ranges rather than chosen. Two kinds of carrier are excluded with a written
  reason instead of a list: a work item's round records, which quote a
  finding's wording by design, and struck-through text, which is this
  repository's own mark for a claim it no longer makes.

  **A survivor a person judges legitimate is answered, not switched off.** A
  row in `seal/specs/<work-item-id>/survivors.md` names the path, a quoted
  substring of the standing text and the grounds; the quote is the anchor, so
  the exemption stops holding the moment that text changes, and an excused
  survivor is still printed with its grounds. There is no value meaning
  *check nothing*.

## 0.9.2 — 2026-09-08

<!-- specs/1788844127-the-reviewers-report-reaches-the-record-retyped -->
- **The reviewer's report reached the record retyped, and now it reaches it as
  a file (issue #228).** `round_record.py new` took `--report <path>`, and the
  reviewer's report was not a path: the warden returns it as its final message
  and the orchestrator is told not to open the agent transcript, so the report
  existed in a transcript nobody may read and in chat text, and the
  orchestrator typed it into a file to have something to pass. Four rounds of
  one work item in another repository, four retypings; 0.9.0's own #190 · #207
  run retyped rounds 2 and 3 by hand. A retyped verdict row carries retyped
  coordinates, re-review inheritance carries the paraphrase into the next
  round, and `Fixes checked by` then names a round whose report is not the
  report the reviewer wrote.

  **The warden writes its report to
  `seal/specs/<work-item-id>/rounds/round-<n>-report.md` and returns that
  path**, and **`round_record.py new` reads that path when `--report` is
  absent**, derived from `--item` and `--round` — the same pair `round-N.md`
  itself is derived from, so the reviewer and the generator cannot spell it
  differently from each other. The flag stays and it still wins: a round whose
  report predates the convention, and a round that ran more than one reviewer,
  both need it. Where neither the flag nor the file is there, the run refuses
  and the message names the path AND the convention that fills it — a derived
  path with no sentence beside it reads as a mistyped argument, which is the
  one thing it cannot be.

  **The fixer side already had this shape**, `rounds/round-<n>-fixes.md`, so
  this is the missing half of a convention rather than a new one.

- **The record and the report are told apart, in the three documents that used
  to carry only the prohibition.** *The reviewer writes no round record* and
  *the reviewer writes nothing under the work item* had become one sentence,
  which is why the missing half above read as forbidden rather than as absent.
  `agents/warden.md` now says the record is `round_record.py new`'s, written
  after the orchestrator verifies the findings, and the report is the
  reviewer's own artifact — the thing the contract's §6 already calls its
  final output, in a different medium and with no more authority. It is still
  uncommitted, still unverified, and still inert until the orchestrator acts
  on it.

  `skills/agent-contract/SKILL.md` is unchanged. §6 says an exception *"is one
  agent's, and it is named in that agent's definition — never here"*, so the
  permission is written in `agents/warden.md` beside the rule it excepts —
  the clone rule, which is what actually forbade the write and is a section
  above the one that looked like it did.

- **A record is selected by name, never by directory membership
  (`docs/review-handoff-protocol.md` §Layout).** `rounds/` holds three files
  per round beside the record — the report, the round paragraph, the fix
  table — and the layout diagram read as an inventory of the directory. Three
  readers in this repository took membership for record-ness. Two raised
  `TypeError` on sorting two `None`s rather than failing an assertion; the
  third counted fifty-three non-records into a corpus of records and said
  nothing at all, and it is fixed here. The
  report itself stays implementation, like the parent path: the protocol
  requires a record, and a conforming tool whose reviewer writes `round-N.md`
  directly needs none of the three.

<!-- specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible -->
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
  the half a person acts on first and no test would say so. Every piece it
  builds is now read whole — six of them, counted from the expression the
  builder returns rather than from a reading of it — and each was seen red on
  its own deletion before the case was committed. The two mutations that still
  pass are named in the case itself, because what survived a measurement is a
  fact and "nothing else can be pinned" is not.
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
  from the wider sentence would go looking for history to rewrite. Both
  documents that state the rule now agree — a third names the ticket rather
  than the check, and describes what the check used to do, so it is left as
  the record of that moment it is.

<!-- specs/1788844300-the-guards-cases-cannot-observe-what-they-guard -->
<!-- specs/1788844300-the-guards-cases-cannot-observe-what-they-guard -->

### Fixed

- **An ordinary `gh` command piped into `jq` could have stopped a session's
  Bash call.** The same reminder decides which parts of a command line are `gh`
  commands by splitting on `|` and reading each piece with `shlex`. A pipe
  inside a quoted string — `gh pr view 123 --json comments | jq '.comments[] |
  .body'`, which is the reminder's own example — leaves a piece whose quoting
  is unbalanced, and `shlex` raises on it. One arm absorbs that, and no case
  watched it: deleting the arm left this module and every other module that
  touches the hook green, while the hook itself began exiting 1 with
  `ValueError: No closing quotation` on that command — out of a `PostToolUse`
  hook and into the session's Bash call, which is the one thing this hook is
  written never to do. It has a case now. The arm was found by applying the
  same enumeration to the two functions of the file the first pass had not
  walked, which is what a review round is for.
- **So could a command as ordinary as one ending in a newline.** The same
  splitter breaks on `\n` as well as on `|`, so any multi-line Bash command
  leaves a trailing piece with no tokens in it at all. Two index guards keep
  the reminder from reading a first word off such a piece, and no case watched
  either: deleting one left the module green while the hook exited 1 with
  `IndexError: list index out of range` on `gh pr view 1 --json comments` with
  a trailing newline and on `echo hi;`. `FOO=bar` gets there by the other
  route — it is one token, which the environment-assignment prefix arm
  consumes, so the index runs off the end just the same. All of it is covered
  now, together with the quoting arm above, by **one parametrized case rather
  than four** — they share a single input class, a piece the reminder cannot
  reduce to a first word — and the case closed a fourth decision as a
  by-product. What is still unwatched in that function misfiles a reminder
  rather than stopping anything, and went to a ticket, because writing a case
  for each closes today's list and not the class (#209, #210).
- **The pre-merge reminder's reader had two failure arms nothing watched, and
  either one would have stopped a session's Bash call.** `reader()` loads the
  shared reader by relative path and answers `None` where it cannot, so a copy
  of the plugin without `skills/` leaves the reminder printing rather than
  raising — that is the whole reason it returns `None` instead of raising. Two
  of its arms were pinned by cases and two were not: a `.py` reader that does
  not parse, and a `.py` reader that parses and imports something this
  interpreter does not have. Deleting either arm left the whole module green,
  so nothing would have noticed the arm going away. Both have a case now, and
  each was seen red on its own arm with the other left green (#209).
  The second of them was named by no ticket and no ledger row. It turned up
  because the arms were enumerated out of the function's own source instead of
  read off the page: the except tuple has three members where every prose
  reading of it had counted two, which makes four reachable arms rather than
  three. The evidence ledger's row said three, and now says four.
  A fifth arm, `spec.loader is None`, gets a sentence rather than a case. No
  file path constructs it — a directory, a `.txt`, an extensionless file and an
  empty string all make `spec_from_file_location` answer `None` outright, while
  a `.py`, a `.pyc`, a `.so`, a missing `.py` and even a directory *named*
  `x.py` all come back with a real loader. It is defence in depth, and saying so
  is the honest close.
- **The case guarding what a closing word can hide behind was a list of two
  literals, so a third hiding place would have arrived unguarded and silent.**
  The reminder decides a round record is closed by reading it the way the
  shared reader does, which blanks fenced blocks and HTML comment bodies — a
  closing word inside either is not a closing note. The case covering that was
  parametrized over two hand-written entries with a comment saying a third
  reader pass would want a third entry, and nothing made it want one: adding a
  third pass and running the module left everything green, while a closing word
  inside an inline code span silently began reading as hidden. The
  parametrization is now compared against the passes the reader actually
  composes, read out of its own source, so a pass added later fails that case
  instead of passing quietly (#210). The direction was never dangerous — a
  further pass only makes the reminder fire more often — but the silence was.
  What that comparison can see is passes the reader calls **by name**. A pass
  written instead as a regular-expression substitution on the text — the shape
  a text-level blanker is naturally written in, and the shape the ticket itself
  used as its example — is invisible to it, and left the comparison agreeing
  while the reminder's answer flipped. That shape is now refused outright with
  a message saying what to do about it, rather than passing unnoticed.
  The case also goes red when a reader pass is RENAMED, and its message used to
  offer only the repair for a pass that was added — adding a key, which for a
  rename leaves an extra key and the case still red. It now names both causes
  and the repair each one takes.
- **A work item with no round records at all could have started reading as one
  whose rows were never drained.** `is_closed` answers *closed* when there are
  no records, which is what keeps the reminder quiet for the state most work
  items are in, and no case called it that way: mutating that answer to
  *not closed* left every case green. It has a case now. The arm is unreachable
  from the hook itself, which asks only when records exist, but it is reachable
  in one line of code — and where an arm can be reached directly, a case is the
  honest close rather than a sentence.

<!-- specs/1788844400-a-body-naming-two-issues-claims-one -->
- **A pull request body naming two issues claims one, and nothing said so
  (issue #167).** PR #162's body wrote a closing keyword followed by two
  numbers in one sentence. At the 0.8.0 release the first was closed and the
  second stayed open, and somebody closed it by hand afterwards.

  Nothing malfunctioned. A closing keyword claims the one number that follows
  it — GitHub reads it that way, and `close_issues_on_release.py` says so in a
  comment two lines above its own regex. The answer was written down in the
  one file whose author needs it least at the moment the prose is written: the
  session writing a pull request body is not reading the release closer.

  **So the repair is a check that reports, not a wider regex.** Widening
  `CLOSING` would make this repository close issues GitHub does not, and the
  two would then disagree about what a body means — worse than the loss it
  repairs.

  `.github/scripts/issue_claims_check.py` runs first in the `hygiene`
  workflow, on every pull request. It prints every issue number the body
  claims, every one it merely mentions, and a warning for any sentence that
  claims one number and names another beside it. **It never fails a pull
  request**: a check that goes red on prose stops a release for a false
  positive, and one measured occurrence does not buy that. Its only non-zero
  exit is a step handed no body at all, which is a misconfigured workflow
  rather than a body.

  **What a sentence is, since the whole check turns on it.** A segment ends at
  `.!?;` before whitespace, at a blank line, or at the start of a new markdown
  block — and **not** at a single newline, because every body here is
  hard-wrapped and the defect arrives split across two lines. Fenced blocks
  and code spans are blanked character for character, so a body quoting the
  failing shape as an example reports nothing, and the warning can still quote
  the sentence as the author wrote it. `e.g.` ends a segment too, which can
  only split two numbers apart: the check under-reports rather than inventing
  a warning.

  `docs/issues-and-milestones.md` gains the rule in prose, beside the section
  that already says a missing `Closes #N` costs an issue that stays open
  forever.

## 0.9.1 — 2026-09-08

<!-- specs/1788789329-a-git-call-that-fails-reads-as-no-remote -->
- **A git call that failed used to read as a repository with no remote, and
  in `seal import` that switched off the refusal keeping another project's
  records out (issue #111).** `git()` in `skills/implement/scripts/seal.py`
  answered `""` for every failure — an `OSError`, a timeout, a non-zero exit —
  and four of its five call sites read that `""` as a fact about the
  repository. The sharpest of them decided whether the zip in hand came from
  somewhere else: an empty answer short-circuited the whole condition, so a
  git that timed out merged another project's records with no word about it.
  Nothing is destroyed — `seal import` never overwrites — but two projects'
  work items land in one root keyed by work-item id, with nothing afterwards
  to tell them apart, which is the outcome the refusal exists to prevent.

  **The unanswerable question now refuses**, which is the direction
  `gitlinks_under_root`, `porcelain` and `indexed` in the same file already
  take. The message carries git's own words, because *run it again* and *this
  machine will never answer* are the two things a person does next and only
  git's text tells them apart.

  **The escape is `--allow-unreadable-remote`, a flag of its own.** Typing
  `--allow-other-repo` is saying *I have read both URLs and they are one
  repository under two spellings*; someone whose git could not answer has read
  neither and is saying something else. Routing both past one flag would merge
  the two facts again at the only place a user acts on the distinction.

  **The manifest leaves out what git could not read**, rather than freezing
  `""` into the zip for the receiving machine to read as a fact. `remote` now
  has three states — a URL, `""` for a repository with no `origin`, and absent
  for a question that went unanswered — and a zip recording no remote refuses
  on arrival for the same reason. `head` loses its empty state entirely: `git
  rev-parse HEAD` prints a SHA whenever it succeeds, so present means a SHA
  was read. The format number does not move, because no field was renamed or
  repurposed and format 1's only reader of the two already went through
  `manifest.get`.

  **`git_asked` is one helper where there were three.** `porcelain`, `tracked`
  and `gitlinks_under_root` had each grown the same *(value, why)* shape for
  themselves; it is promoted so a caller needing the distinction does not
  write a fourth. `git()` is that helper with the distinction thrown away,
  which is the right reading for a caller with nothing to do with `why` — and
  after this change it has exactly one call site left, `other_worktrees`,
  where a failure means an advisory note does not print. Its docstring now
  says that silence is by design.

  Its `answered` parameter exists for one measured fact: `git config --get`
  exits 1 when the key is not set, so for that command alone a non-zero code
  is an answer. Measured 2026-09-07 — an unset `remote.origin.url` gives
  `(1, '', '')` and a `.git/config` git cannot parse gives `(128, '', 'fatal:
  bad config line 9 …')`. `--default ""` would have removed the special case
  and wants git 2.18, which nothing else here needs, so an old git would have
  started refusing a path that works today.

  **The ticket said four call sites were left; there were five.** It did not
  count the second `git()` inside the refusal message, which asked git again
  for the URL it had just read and printed whatever that call answered — so a
  failure between the two put a blank where the message promises this clone's
  URL. That is this ticket's own failure appearing inside the message
  reporting it. The value compared is now the value printed.

  **The receiving guard reads the manifest's `remote` for its TYPE, not its
  presence.** Review round 1 measured `null`, `42`, `[]`, `{}` and `true` all
  importing at exit 0 with both guards silent — and `null` is what any JSON
  writer produces from the `None` this change introduced, so the very state
  the export uses to say *I could not look* arrived at the guard as a key that
  was present.

  **The refusal names the machine that can fix it.** One closing line used to
  cover two failures with two different next steps. When this clone's git went
  silent, running the import again may succeed; when the ZIP is the silent
  side, the bytes say the same thing on every run there is and the export has
  to happen again on the other machine — so telling that person to re-run sent
  them into a loop that cannot end. When both sides are silent the zip
  decides, because no re-run here clears it whatever this clone's git answers
  next.

  **The export says which field it had to leave out.** It used to write a zip
  that would be refused on arrival and print nothing about it, which left the
  diagnosis on the importing machine while the one that could clear the
  failure — by running the export again — was told it had succeeded. Only the
  `remote` line carries the note about the other machine's flag, because only
  a missing `remote` is refused there. (#111)

- **Two checks of this repository's own round records stopped crashing on the
  files the review chain writes beside a record.** Both asked git for
  `seal/specs/*/rounds/round-*.md`, and git's pathspec has no way to say *and
  then a number*, so the glob also picked up `round-N-report.md`,
  `round-N-asked.md` and `round-N-fixes.md`. Ordering the result asked for a
  round number those files do not have, and two of them in one work item ended
  the check with a `TypeError` instead of a verdict — so a run that committed
  a reviewer's report beside its record turned two checks off and reported it
  as a crash. `chain_check.py` itself already drops those files on the same
  test; the two readers that did not now do. (#111)

<!-- specs/1788789330-the-update-notice-names-the-expensive-move -->
- **The update notice and the update procedure now name `/reload-plugins`,
  and say exactly how far the measurement behind it reaches (issue #134).**
  The session-start notice closed with *"Either way, restart to load it"* and
  the skill closed the same way. Both named the move that ends the session you
  are in, and neither named the cheaper one this repository had already
  measured and written down.

  **What a reload was measured to do, and nothing more.** Run 6 of
  `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` is the
  only positive case: a sentinel in the version cache came back PRESENT after
  a `/reload-plugins`, and ABSENT in run 5 without one. So a preloaded skill
  body handed to a spawned agent is re-read at a reload, and that is the whole
  of what was established.

  **Three things are stated as unmeasured rather than left to silence**, which
  is the ticket's second acceptance condition. The experiment touched neither
  hooks nor agent definitions, and — the part the ticket itself assumed — its
  sentinel sat in the *running* version's own cache directory, so it shows a
  re-read of the copy already in force and nothing about a session picking up
  a newly installed one. A user reading this notice is in exactly that second
  case. `skills/update/SKILL.md` §5 carries the run that would settle it: run
  6's own method, with a sentinel in a hook and in an `agents/*.md` instead of
  in a skill body.

  Saying *not measured* rather than *not needed* is the point of the
  distinction. A user told the reload is insufficient stops using it; a user
  told it covers everything gets a half-loaded plugin with no way to tell.

  **Every sentence that names the reload says which copy it re-reads.** Without
  that qualifier the notice recommends, as the cheap way to get the release
  that just arrived, a move whose only measured effect is on the version the
  user already has — and the module's own docstring said so thirty lines up.
  The qualifier now sits inside the claim's own sentence in both languages,
  including the two README command-table rows and the two by-hand code
  comments, which are as much an instruction as the paragraph above them.

  **The gate table stopped calling the banner one line.** `README.md`'s
  version-check row said the hook *shows one line*; it has shown four since
  before this work item, and this work item is what made the notice longer.
  The row now says it shows a short notice naming `/specseal:update` and the
  two moves that load a release — a description of what the notice says rather
  than a count of how it renders, so there is no number left to go stale. The
  Korean edition never carried the count and is unchanged.

  **Fifteen sentences moved, enumerated by grep rather than from the ticket's
  list** — which was three lines short and named neither of the Korean
  README's three. Two of the fifteen are code comments inside fenced blocks
  (`# then restart`, `# 그다음 재시작`), which the wrap test skips by design
  and which a reader copying the block copies with it.

<!-- specs/1788789985-round-record-dies-on-python-3-9 -->
- **`round_record.py` says which interpreter it needs, at entry, instead of
  dying partway through with an interpreter traceback (issue #226).** On a
  machine whose `python3` is 3.9 it died at `zip(..., strict=True)` with
  `TypeError: zip() takes no keyword arguments` — and it died there, which is
  to say after argument parsing, path resolution and the report read had all
  succeeded. So the failure read as a bug in the report, and the message named
  neither the version needed nor the flag. macOS still ships 3.9 as
  `/usr/bin/python3`, so that is the default interpreter on a common platform,
  and a repository pinning a newer one does not help because the script is
  invoked directly rather than through it. Reported from another repository on
  0.8.3.

  Fifteen lines after the imports now refuse an interpreter below the floor
  with a sentence naming the floor, the version found and the interpreter it
  was found at, and saying that nothing was read and nothing was written.
  Exit 2, which already meant *nothing was written*, and the docstring's
  exit-code line says so now rather than being quietly widened.

  **The four `strict=True` sites stay, and that is the ticket's other
  suggestion refused on grounds rather than on taste.** `CONTRIBUTING.md`
  names 3.12 as the supported floor, so dropping them would buy a few more
  lines before the next 3.10+ construct, at the price of the invariant the
  comment above the first one states: both of the reader's passes keep indices
  intact, so the two reads are the same file line for line, and a length that
  differed would truncate the hidden set — which is that check reporting clean
  because it read less.

  **The guard runs before `chain = load(CHAIN, ...)`, and the placement is
  load-bearing.** That assignment reads and executes a second file at import,
  before `main()` is ever called, and it succeeds on 3.9 — so a guard written
  in `main()`, which is where one naturally goes, would still let the operator
  watch exactly the progress the ticket is about. A mutation that moved it
  there left every end-to-end case green and was caught by one case reading
  the module's own AST.

  **The floor is not imported from `.github/scripts/run_tests.py`, and the
  reason is the argument rather than the convenience.** A read that can fail
  gives the guard a second way to die on the one machine that has no other way
  of being told what is wrong; and a fallback-safe read still has to name a
  floor in its `except` branch, so the second spelling survives the import
  anyway. The number is pinned by a test instead, which is the mechanism this
  repository already uses for the same number in five other places. That pin
  ties the repository's two floor authorities together for the first time:
  `test_release_hygiene.py` reads `ruff.toml`, the runner's own suite reads
  `run_tests.py`, and nothing read both.

  **The class was enumerated by construction and five members were deferred,
  each with an answerer.** Twenty-five entry points ship; six carry a
  construct newer than the floor. `.github/scripts/gather_changelog.py`,
  `.github/scripts/fold_ledger.py`, `skills/implement/scripts/seal.py` and
  `skills/verify/scripts/session_cost.py` use `datetime.UTC` (3.11) and
  `hooks/root-migrate.py` uses `zip(strict=)` — three of them named after a
  literal `python3 ` in the release checklist, one invoked by the harness, and
  one that ends a run report. A new case re-runs that enumeration on every
  suite run, so a seventh cannot arrive as a traceback on a stranger's
  machine.

  The scan's own spelling was wrong twice and the record says so, because it
  is the same failure both times — an instance the pattern could not reach.
  `zip\([^)]*strict=` hid the site in `round_record.py#inherited_rows`, where
  an inner call closes a parenthesis before the keyword is reached; and
  `datetime\.UTC` hid `session_cost.py`, which spells the module
  `import datetime as dt`. Review round 1 found the second by re-deriving the
  class from the AST rather than from the table, which is what an enumeration
  is for.

<!-- specs/1788817289-local-mode-from-first-setup-to-the-gate -->
- **A repository in local mode met a review chain that refused its root and a
  check that reported its declaration missing.** `round_record.py` derived the
  repository from the work item, through a `git rev-parse --show-toplevel` run
  from inside the item — and a local-mode item sits under the common git
  directory, where git declines that question outright (`fatal: this operation
  must be run in a work tree`). So every call needed `--root "$PWD"`, and the
  first one without it was told the item is nowhere. Git is asked which trees
  belong to the clone now, and the caller's tree is the answer where it belongs
  to that clone — compared by common git directory rather than by the paths
  `git worktree list` prints, because for a repository built with
  `--separate-git-dir`, and for a bare clone, those paths are the git directory
  itself and the caller's own tree is not among them. A root that is not a work
  tree is refused rather than named, so the failure lands on the command that
  can name it instead of on whatever runs next.
  Then `chain-check` printed *Add `seal/specs/<work-item>/routing.md`
  to declare* while the declaration sat at
  `<git-common-dir>/seal/specs/<id>/routing.md` — a path local mode does not
  use, and a file the operator already had. It says which root it searched
  now: a local-mode repository is told where its root is and that nothing
  under it is committed, and a shared-mode one is still told to write the
  file, with the prefix and the branch it searched for named. The verdict does
  not move — reading an untracked declaration would make the local run assert
  something CI can never reproduce — so what is fixed is that a false *no
  declaration* is no longer indistinguishable from a real one. (#225)

- **The mode nobody was asked about is now a state something names.** Creating
  `seal/` is what opts a repository in, and whether it lands in the tree or
  under the git directory decides whether every clone carries that
  repository's review records. The preset block `install.sh` copies into
  `~/.claude/CLAUDE.md` — which loads in every project on the machine,
  including one that has never seen SpecSeal — told a session to write
  `seal/specs/<id>/routing.md` before the first edit, and that write creates
  the root. The question lived in a skill the session had no reason to load,
  and nothing afterwards noticed: a root somebody chose and a root that
  appeared this way were byte-identical. Two halves close it. The routing rule
  names the condition **before** it names the write, and the bootstrap now
  records the answer it collects with `seal mode`. And a new gate,
  `mode-gate`, names a root whose `seal/config.md` carries no `Mode` row — two
  prompts per session per repository and no more: one deny carrying the three
  ways on as options, then the plain confirmation that approving gets past,
  then silence for the rest of the session, and nothing at all once the row
  exists. In local mode the repository is the clone, so one root shared by
  several work trees is one question rather than one per tree. It judges the
  repository the SESSION sits in rather than one a `-C` names, because this is
  a fact about a workspace and not a verdict about a change. (#151)

- **On upgrade, every repository that opted in before this release meets that
  gate.** The `Mode` row is written by `seal mode` and, from this release, by
  the bootstrap that creates the root. Nothing back-fills it and nothing writes
  one at session start, so a repository that has had `seal/` for months has no
  row — and its next session is denied on its first Bash call and asked on its
  second. Running `seal mode` once in each such repository records the mode
  from where the folder already is, moves nothing, and ends the prompting
  before it starts. (#151)

<!-- specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id -->
- **A round record's finding id is now a bare integer, and a record that
  numbers findings any other way is refused with the format named and the row
  quoted (issue #227).** A reviewer numbered eight findings `R2-1` … `R2-8` —
  the round in the id, so a finding stays unambiguous when three rounds are
  read side by side. The generator read the first digit run anywhere in the
  cell, so all eight collapsed toward `2`, and what came back was *the fix
  table has two rows for finding 2* about a table holding one `R2-1` and one
  `R2-2`. The first read is that the table is malformed, not that the ids
  are, and with eight rows and no coordinate the pair had to be found by
  hand. Both tables now read the cell through one pattern, and a genuine
  duplicate quotes both rows.

  **The refusal was chosen over accepting a prefix, and the corpus is why.**
  Every committed record was run through both rules first: of 130 that parse,
  82 pass under either, 46 already refuse today, and 2 pass today only by
  miscounting — `r3 🟡 2` keys as finding **3**, out of the `3` in `r3`, and
  `🟢 round 2's finding (🟡 4)` keys as **2** where the cell names 4. So the
  rule takes away two wrong answers and no right one. The round is already in
  the record's own file name, which is what a prefixed id was reaching for.

  **The format is now stated where reviewers pick numbers**, not only at the
  point of refusal — the ticket's own last line. The reviewer chooses the
  numbering and the fix pass copies it, so the refusal used to surface at the
  orchestrator, one hop from either agent that could have avoided it.

  **And the refusal now arrives.** A `#` cell of punctuation ending in a
  non-digit used to send the pattern exponential — 11.4 s to refuse 28
  characters, and each further character doubled it — so `close` and `new`
  produced nothing and never returned. That is worse than the confusing
  message the ticket opened for, on the tool that gates every record. The
  pattern reads one marker character per repetition instead of a run of them,
  which accepts and keys exactly the same set: checked over every `#` cell in
  every committed record and over 4368 constructed shapes, with no
  disagreement. A 100 000-character cell now refuses in three milliseconds.

- **`Contract changes` no longer reports `no call site found` for a unit
  pytest itself reaches (issue #211).** A collected test function is called by
  the runner and never by name, so the only `test_thing(` in the tree is its
  own `def` line and the reach came back empty — the row said *this unit is
  dead* about a case that runs on every CI leg. It reads `pytest only` now,
  which is the value that already existed for a unit reached only from
  `tests/`.

  **The class was enumerated by running the derivation, not by reading it.**
  Over every top-level def under `tests/`: 1892 of 1947 `test_*` defs read
  `no call site found`, and so did 8 of 42 fixtures — the member the ticket
  had left in its own *Not verified* section. A fixture is injected by
  parameter name and a `conftest` hook is dispatched by the plugin manager,
  so neither is ever written as `name(` either.

  **It is those three shapes and not everything under `tests/`.** One helper
  there reads `no call site found` correctly, because it is passed by name as
  a value and never called, and a wider rule would say the runner covers a
  unit nothing covers — the same false sentence pointing the other way. One
  limit is recorded rather than closed: the hook arm reads `conftest.py`
  alone, where pytest also dispatches hooks from collected test modules.

  **Which file a def sits in decides two different things, and the first
  version of this asked only one of them.** Collection is two rules: which
  file becomes a test module and which def inside it is a case. A `test_*` def
  in `tests/helpers.py` satisfies the second and not the first, so pytest
  never runs it — and it was reading `pytest only`, which is the false
  sentence above pointing back again. It reads `no call site found` now. And a
  `conftest.py` is the opposite case: pytest loads it by name and documents
  the repository root placement first, so a fixture or a hook in a root
  `conftest.py` was reading `no call site found` — the reported defect, left
  standing at the commonest placement of all. Both now read what they should,
  and the boundary was re-derived by running the rule over every top-level def
  in the tree rather than by reading it.

  **A conftest is loaded by name, but the directory decides whether pytest
  loads it at all.** The first repair accepted the name from anywhere, which
  put the false sentence back: a `conftest.py` in a directory nothing is
  collected under — a vendored tree, an examples directory, `src/` in a
  repository whose tests live under `tests/` — is imported by nobody, so its
  fixtures are injected into nothing and the row was saying the runner covers
  them. The rule now asks whether a file pytest collects sits at or below the
  conftest's own directory, which is the question pytest itself asks, and it
  asks it inside `tests/` as well as outside.

- **A rider comment is now checked wherever this repository plants one.** The
  list of directories the rider checks walk left out `tests/`, so four riders
  were held to nothing at all — two carrying a measurement, one with no
  verification stamp in any form, and one whose own branch record said the
  stamp had been checked when nothing had checked it. Two of the four could
  not be given a stamp naming a commit, because the commits their measurements
  were taken at were discarded when their branches squashed, so a stamp may
  now name the content it was read against instead.

- **`Contract changes` now sees a unit that gains or loses a returnable
  value, and the shape it still cannot see is written down (issue #194).** The
  derivation compared parameters and return arities, so a unit returning the
  same shape with a meaning it could not return before changed neither and the
  row read `none` — on the row that exists for the largest regression class
  #57 measured. The measured instance returned 0 for a mean it cannot compute,
  and the one call site interpreting that 0 was never revisited: it takes the
  charged 0 as a baseline and reports growth on a run whose input collapsed.
  The contract now carries the set of returnable constant literals, keyed by
  type as well as value — Python hashes `0` and `False` into one key, and
  those are two different things to return.

  **A real instance the old rule missed, found by construction:** between
  v0.8.0 and v0.8.3, `chain_check.py#read_record` began returning an explicit
  `None` with signature and arity unchanged. The old contract read it as
  unchanged.

  **The hole is the other half of the deliverable, not a gap left over.** A
  changed input→value mapping — a unit that keeps returning exactly the values
  it already returned and changes which inputs reach which one — is invisible
  to a literal-set comparison by construction. `docs/review-chain-spec.md` now
  says so, names the measured instance, and says the residual is the
  reviewer's. Documentation alone had been refused as an answer, because it
  moves the work to a person; the check ships and the paragraph states where
  it stops, so a later session widening it is removing a stated limit rather
  than closing a gap.

<!-- specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session -->
- **The worktree guard asks once per session instead of once per worktree
  (issue #237).** It answered creation with `ask` at every site that reached
  it, so no path through it cost zero prompts and the cost grew with the number
  of worktrees. Measured on the 0.9.1 release run: six work items on six
  branches needed six `git worktree add` calls, and the guard held the run at
  all six. An unattended run reaches the first and stops there.

  **`[worktree-ok]` could not fix that and `has_token`'s docstring says why.**
  The token is written into the command by whoever issues it, so the model can
  write it on the first attempt; reading it as consent turns the guard off with
  nobody asked. What separates the first creation from the sixth needs no
  token: the harness only runs a `git worktree add` that was permitted, so a
  `PostToolUse` observation of one that actually **ran** is written after the
  answer rather than before the question, which is the one thing a command text
  cannot forge.

  `hooks/worktree_consent.py` writes that record — an empty file at
  `<git-common-dir>/specseal-worktree-consent/<session-id>` — on both entry
  points, and the guard reads it above every row of its creation ladder,
  because each of them asks something a person has already answered. One
  invariant changes: *creating a worktree always takes one confirmation*
  becomes *the first creation of a session takes one*.

  **A third directory, not a value in the choice marker beside it.** That
  marker is written by `PreToolUse` before the answer and means *the question
  was put*, so one shared file would let the guard read its own question back
  as consent. They also fail in opposite directions — an unwritable choice
  marker counts as **already asked**, an unwritable consent record counts as
  **no consent** — and one file cannot fail two ways.

  **Keyed to the clone, with no expiry.** The record stands for *this session
  may split this clone into worktrees*, so it lives under the common git
  directory and a linked worktree of the same clone shares it. A session id is
  already scoped to a session, so a time bound on top of it could only produce
  one new outcome: a session outliving the bound is asked a second time, which
  is the failure being removed. A failed `git worktree add` records too — the
  record is about the approval, and the retry after a failure is the worst
  moment to put the question again.

  **The allow is bounded, and the bound is about each segment rather than only
  about the compound.** `permissionDecision: "allow"` covers the whole tool
  call, so the guard speaks only for a command that is worktree creation and
  nothing else; a compound gets `ask` about the rest of the command line, never
  a deny about the worktree, and a command the lexer gave up on gets `ask` too.
  So does a creation carrying an expansion or a redirection — `$( )`,
  backticks, `>`, `>>`, `<`, `2>`, `<(…)`, a subshell, a heredoc — and one
  behind a wrapper, `sudo git worktree add …` or `env VAR=… git worktree add
  …`, because a user's own `permissions.deny` must not be spoken over by a hook
  reasoning about worktrees.

  The command word has to be the word `git` and not a file whose name ends
  that way. The test compared basenames, so `./git`, `bin/git`,
  `/tmp/evil/git`, `~/git` and `*/git worktree add …` were all vouched for —
  and that allow covers the whole tool call, so one approved creation would
  have let a session run any executable on the machine by giving it a filename
  of `git`. `/usr/bin/git worktree add …` now costs one prompt; a wrong deny
  spends a prompt, a wrong allow signs for a binary nobody identified.

  **A creation anywhere in the command is judged before it runs.** The guard
  classified the first segment it could read while the writer records for a
  creation anywhere, so a `git switch` written in front of a creation took the
  decision and the creation was never judged — it ran, and the session held
  consent from that point. The switch ladder keeps every verdict it had, and
  its two silent exits now fall through to the creation.

  So does the branch of a choice site that lets the command through. Two of
  the three concurrency rows kept above the creation deny only **once** per
  session per direction and ask on every attempt after, so the second `git
  switch feature/x && git worktree add ../wt f` in a session was answered
  *Approve — switch branches in this shared tree* — and approving it created
  the worktree with the creation question never put. The deny keeps its
  precedence; only the ask yields.
  On the `Agent`/`isolation: "worktree"` path the guard goes silent rather than
  allowing, because that call is a creation *plus* an agent with a prompt and
  the record is about the first half.

  What does not change: a session with no record still asks at every site, the
  single-stream row still denies and steers to `git switch`, and the switch
  direction never reads the record. (#237)

<!-- specs/1788824000-a-rider-stamp-names-a-commit-the-squash-discards -->
- **A rider stamp no longer names a commit the release's own merge rule
  destroys.** `# RIDER:` comments carry a `Verified … at <sha>` line so whoever
  opens one can see how stale it is. A fix pass works on a feature branch, so
  the only commits it has to name are that branch's — and a feature branch
  **squashes** into its release branch, which writes one new commit and keeps
  none of the originals. The stamp planted by #226's fix pass stopped
  resolving the moment #226 merged, and
  `tests/test_a_rider_reaches_its_file.py::test_every_rider_stamp_names_a_commit_this_branch_can_reach`
  turned the release branch red — on the merge rather than on the branch that
  wrote it, so the person who has to repair it is never the person who caused
  it. The claim was re-measured on the squash commit that carries the same
  state and the stamp names that. The class this belongs to — a stamp naming a
  position in a repository whose rules rewrite positions at every boundary — is
  #239. (#239)

<!-- specs/1788826000-a-stamp-names-content-not-a-commit -->
<!-- specs/1788826000-a-stamp-names-content-not-a-commit -->

### Fixed

- **A rider comment's verification stamp names the content it was checked
  against, not a commit.** Every `# RIDER:` in the tree carried a
  `Verified <date> at <sha>` line, and a feature branch squashes into its
  release branch — which keeps none of the branch's own commits, so the check
  failed on the release branch with nobody who caused it looking, and every
  pull request into that branch failed until somebody re-pointed it by hand.
  A stamp now reads `Verified <date> against <anchor>@<hash>`, using the same
  anchors the evidence ledger uses, and the check makes no git call at all: a
  squash, a rebase and a shallow clone are invisible to it.
  A drifted rider names the unit that changed and says to re-read the comment,
  which is what a rider is for. `.github/scripts/rider_check.py` checks them
  and `--reverify` re-stamps them — rewriting the hash wherever it moved, and
  the date only beside a hash that moved, because a stamp whose content has
  not changed records a reading nobody repeated. `--reverify --only` takes a
  file rather than a rider, and the drift message now says so.
- **A `## RIDER:` heading in a markdown file no longer breaks the build.** `#`
  opens a comment in Python, YAML and shell, and in markdown it opens a
  heading — so a heading naming the marker was read as a rider carrying no
  stamp, and the check exited 2 on a line nobody wrote as a rider. Markdown's
  rider form is the HTML comment, and that is now the only form read there.
  Every other thing this check gives up loses an alarm; this was the one place
  it invented one.
- **`--only` no longer reports success for a run that ignored it.** A path no
  rider carries printed `0 restamped · 0 refused` at exit 0, so a typo in the
  path read as *nothing needed doing* — and exit 0 is the answer a script
  reads. It is now refused by name. `--only` without `--reverify`, and beside
  `--migrate`, were ignored the same way and read the whole tree; both are
  refused before anything is read.
- **Three riders were held by nothing.** The scanned roots covered four
  directories and riders live in six, so the one in
  `.github/scripts/fold_ledger.py` and two under `tests/` were checked by no
  case at all — and one of those had never carried a stamp in any form.
- **A round record's `Target SHA` stays as it is, and `templates/sdd-round.md`
  now says why.** It records a moment rather than pointing at live content, a
  reviewed tree has no anchor to write, and the record check already falls
  back to `refs/remotes/pull/<N>/head` — the copy of GitHub's pull-request
  refs that CI fetches — which a squash does not touch.

## 0.9.0 — 2026-09-07

<!-- specs/1788735085-a-loaded-file-naming-a-real-version-is-a-timer -->
- **A loaded file may no longer name a version at or above the running one,
  so a document naming a release that has not shipped goes red on the commit
  that writes it (issue #179).** The check read one number — the version in
  `plugin.json` — so a version written *ahead* of the release was green every
  day until the day it shipped, and red on that release's own preparation
  commit, hours in, after the broad gate had already run.
  `docs/issues-and-milestones.md` carried `0.9.0` that way for three releases,
  and the branch that found it had just written two more of the same shape.
  The comparison is read rather than the equality: at or above the running
  version is a timer and is refused, below it is history and is kept.

  **The half that is kept is what decided the design.** The obvious wider
  rule — refuse every version this repository has ever shipped, read from the
  tags or the changelog — refuses `docs/issues-and-milestones.md`'s own
  sentence saying that *the branch `release/v0.3.0` shipped as 0.2.0*, which
  is the reader's only way to tell which release an issue went out in. A rule
  that cannot state that fact is refusing history rather than catching a
  timer, so it was not taken.

  **The comparison is numeric, and that is not a detail.** `0.10.0` is above
  `0.8.3` and every comparison of the two as text says otherwise — and
  `0.10.0` is the exact version the issue names as the one the next author
  writes. A mutation run that swapped the numeric comparison for a textual
  one is what put a case behind it.

  **Three exemptions, each argued where it is declared, and the illustrative
  one asserts its own precondition.** The value the repository already tells
  authors to write (`1.2.3`) is allowed in every loaded file, because the
  point of an illustrative number is that the next author writes it somewhere
  this list cannot know the name of. `docs/experiments/` joins the
  records-of-a-moment list as a path prefix rather than as three more file
  names: those records are dated by their own file names and rewriting the
  version an experiment measured on falsifies the record, which is true of
  every file that directory will ever hold. A version belonging to another
  product — bash's, in a comment about its glob behaviour — is pinned to the
  file that names it, so the token cannot walk through anywhere else.

  The illustrative exemption carries a case of its own asserting that the
  value is neither the running version nor one `CHANGELOG.md` records as
  shipped. On the day this repository ships that number, a bare string in an
  allow-list would wave through exactly the line the check exists to catch,
  and it would do so in silence.

  **The failure message is where the reason now lives**, which is what the
  issue asked for: it names the file, the line and the token, says why such a
  line is a timer, and tells the next author what to write instead and which
  paragraph explains why. `docs/issues-and-milestones.md`'s milestone example
  now asks "what is in 1.2.3" and points at that paragraph. (#179)

- **The comment on `git ls-files`' quoting arguments credits `-z` with what
  it alone does, and so do the two records that repeated it (issue #98).**
  Three places said `-z` alone turns git's escaping of non-ASCII paths off
  and `core.quotePath=false` does not. Re-measured on git 2.50.1 (Apple
  Git-155) over four quoting variants and a fifth for control characters:
  either argument turns that escaping off by itself, so the sentence was
  false, and the same comment contradicted itself three lines further down.

  What `-z` does that the config does not is two things. It turns off the
  escaping of control characters as well — under `core.quotePath=false` alone
  a name holding a newline still comes back quoted — and it separates on NUL,
  the one byte a filename cannot hold. The split below the call is on NUL, so
  dropping `-z` returns the whole listing as a single entry.

  **Nothing in the call changed.** The instruction the comment gives — if one
  of the two is ever pruned, prune `core.quotePath=false` — was right all
  along; only the grounds under it were wrong, which is why no test could
  have caught this and why it travelled from a round record into a ledger row
  and a comment unremarked. The ledger row whose own clause stated the false
  sentence is corrected in `seal/ledger.md` itself, and the two rows anchored
  on the unit the comment lives in were re-read and re-verified.

  Folded in with it: a fixture docstring said two documents carry the only
  mention of one template, where each carries the only mention of one. The
  conclusion it drew was right; the reason given for it was true of one
  document. (#98)

<!-- specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row -->
- **The round record now carries the reviewer's paste-ready fix, and a `|`
  inside a cell no longer truncates the row (#187, #189).** The review skill
  requires a paste-ready fix for every 🔴 and every 🟡 and spends four
  paragraphs on what makes one paste-ready, and `round_record.py new` copied
  the report's four tables and dropped everything else — so not one of those
  blocks reached the file the fix pass is told to open instead of the report.
  Measured: a 162-line report carried three executed snippets, its record came
  out at 80 lines with none of them, and the fix pass rebuilt all three from a
  description and got its first reproduction wrong. The same loss then
  recurred five times on the next branch, whose orchestrator worked around it
  by posting each report as a pull-request comment — durable, and not a file
  any clone contains. **The record gains `## Paste-ready fixes`**, extracted
  by the mechanism the probes table has used since #161: every fenced block
  under the heading, copied whole, and nothing else of the section, so no
  prose nobody parses enters a file the pull-request check reads. A report
  that carries no fence under the heading is still a record — the section
  reads `no paste-ready fix in the report`, which says what was observed
  rather than that none was needed, and beside an open row in the verdict
  table that sentence is the gap written down. A verifying round that opens
  nothing writes no fix, which is why refusing there would stop an unattended
  run over a report that is correct.

  **And a `|` the reviewer wrote inside a cell reaches the record as text.**
  It used to make the row carry more cells than the header declares; every
  renderer drops the surplus, so the text from that character on was invisible
  in the rendered record while surviving in the raw file, and the checker read
  the shifted index. The two compounded: with the fenced blocks going nowhere,
  a table cell was the only durable home for a fix, and a fix is where a pipe
  comes from. Rows are now re-serialised with their pipes escaped rather than
  copied verbatim — in every table the record copies and in the fix table the
  implementer hands over. **A `|` inside a backtick code span is read as
  text**, which is the reviewer's own markup saying so, and that reading is
  taken only when it lands on exactly the header's width; otherwise the plain
  reading is capped at that width and a bare pipe past the last column stays
  in the last cell. A `|` inside an HTML comment is never a break in any
  reading — the row's width is counted on the comment-stripped report and the
  copy is rebuilt from the raw one, and where those two texts disagreed about
  a character the record lost a column at exactly header width, with the
  location standing in the verdict cell the checker reads. The obvious
  repair — fold the surplus into the last column, since the last column is
  the free-text one — was ruled out by measurement over this repository's own
  committed records: of 4128 body rows, eight are over-wide, all eight have
  their pipe inside a code span, one has it in a probes command where folding
  would move half the command into `Result`, and one has it in the Finding
  column where folding shifts that same verdict cell. Nothing here asks a
  person anything. **One report shape that produced a record before is now
  refused**: a fence opener hidden inside an HTML comment under the new
  heading, which would otherwise write a record carrying an open fence and
  blank every section below it.

  **The reviewer is told where the fix goes**, which is the half that keeps
  the section from arriving empty every round: the agent's report contract
  shows the heading beside the three table headings and no longer says the
  generator reads nothing else of the report, and the findings format says the
  fenced block is the only place a fix survives the session — a Grounds cell
  is one line, and this is what used to truncate it.

  **The pre-merge reminder no longer reads a narrated word as a closing
  note.** It stayed quiet once some round record said the rows were drained,
  and it decided that by matching `closed` against the record's raw text.
  Putting the reviewer's code into every record made that reachable
  everywhere, and this repository's own fixes carry the word. The record is
  now read through the same reader every other check uses, so a closing word
  counts only where a reader would read it — **not inside a fenced block and
  not inside an HTML comment.** The second half is the one that was already
  costing something: over this repository's 127 committed round records the
  repair changes the verdict on three, all three because their only closing
  word stands inside an HTML comment the round wrote to narrate itself — two
  of them in the record's header comment, the third in a note beside the field
  table saying the loop is *not closed by one more small fix* — and all three
  still have unresolved rows the reminder should have
  been naming. (#187, #189)

<!-- specs/1788761915-a-record-states-what-nothing-reads -->
- **`evidence-check` now reads what a record says about the tree, and refuses
  a record of a work item that has not shipped when it names a unit nothing
  outside the records carries (issue #190).** A ledger row is a claim about
  the tree that something reads; a `spec.md`, a `plan.md`, an `overview.md`,
  a round record or a phase record states the same kind of thing and nothing
  read it. One work item closed that class three times in three rounds and it
  came back each time, because every closing grepped for the carriers instead
  of building a reader.

  **The boundary is a file the release already removes.** A work item whose
  `seal/ledger/<id>.md` fragment still exists has not shipped, and the fold
  deletes that fragment at the release — so *this record is still the file
  the next segment opens* needs no state of its own. The 129 occurrences in
  work items that have shipped are history and are never opened: a plan from
  0.4.0 proposing a helper that was built under another name is a correct
  record of what was decided then, and a check that refuses history is a
  different mistake.

  **A backticked name is read as a claim only when it carries an
  underscore**, and that narrowing was forced by measuring. Of the 55 distinct
  names in this repository's records that appear nowhere else, the 19 without
  an underscore are a shell command, six stdlib names, an errno, an
  environment variable, a lint code, a probe value, five words of ordinary
  prose in backticks, and three verdict words a checker used to emit — not one
  a claim about a unit, where all 36 compound names are. Without it the first
  record mentioning `str.rpartition` would be asked to mark it as absent,
  which is noise attached to a name that is real.

  **The escape hatch is the marker reviewers already write.** A line carrying
  `NAME NOT IN TREE` is not read at all, in either of the marker's two
  meanings: a name a paste-ready fix is proposing, and a name a record is
  deliberately calling gone. It exempts the line and not the name, so the same
  name still has to exist everywhere else it is claimed — and the exemption
  stays with the person who knows the name is absent instead of becoming a
  list inside the checker that whoever is annoyed by a refusal can widen.

  **A `path#unit@hash` a record wrote down is resolved by the ledger's own
  reader**, so a stamp in a record and a row in a ledger cannot drift apart
  into two rules. Two things deliberately do not carry across: a verdict
  table's `Location` column is `path:line` by design, so a record is never
  told to run the coordinate migrator, and drift in a record reports rather
  than fails — a live work item's branch is editing the very units its records
  stamp, and a check that is always red gets ignored. An `EXTERNAL`
  coordinate is exit 0 in a record exactly as it is in a ledger, so a
  migration repository does not fail for the state its parity config exists
  to allow.

  **A quotation is not a claim.** A fenced region and an HTML comment are not
  read: `## Paste-ready fixes` is code the tree does not have yet, which is
  what a paste-ready fix is, and marking one up would change the fix somebody
  pastes. Each runs to its own end — a comment to its `-->`, so a template's
  two-line comment is an aside on both lines, and a fence to a close carrying
  the marker that opened it, so a `~~~` quoted inside a ```-block does not end
  the quotation. A fence the record never closes is read as a malformed record
  rather than as a quotation of everything left: its lines are read as claims,
  because an author's missing backticks must not be the thing that makes the
  rest of a record pass in silence.

  **A directory the walk cannot list is `UNREADABLE` and exit 2**, the way an
  unreadable file already was. `os.walk` swallows one, so a work item whose
  records folder could not be listed contributed nothing and the run said
  nothing; the same held one directory up, where an unlistable `seal/ledger/`
  read as a repository with no live work item and took the whole arm quiet. A
  directory that is ABSENT is still an empty answer — a repository that has
  not started is not a broken one.

  **The run says how many work items it did not read.** A work item that has
  not written its ledger fragment yet is skipped, and `0 names read` with exit
  0 used to say the same thing for *every record is clean* and *no record was
  opened*. The summary now opens with `N work items read · M unread`.

  One hole is known and left: an untracked or `.gitignore`d file still counts
  as part of the tree, so a scratch note holding a name can silence a refusal
  locally. Closing it means asking git what it carries, and this checker calls
  git for nothing outside `--migrate`. CI reads a clean checkout, where the
  file is not there, so CI is the stricter reader. (#190)

- **`round_record.py new` says what bound the next round is under, as it
  writes the record (issue #207).** The review chain bounds a run one step
  earlier than the cap: after a record whose floor row reads `no`, at most one
  later record may close on a fix, and the record that reads its fixes ends
  the run whatever it finds. That was enforced only at the broad gate — after
  every round of the run had already been spawned — so a session deciding
  whether to spawn again had nothing but the cap, which is a number a prompt
  can carry and is wrong. One work item ran three rounds past the bound with
  both documents open, wrote *"round N of a cap of five"* into every spawn
  prompt it sent, and reverted 37.9 minutes of agent time.

  `new` already opens the previous record to set its `Fixes checked by`, and
  the floor row is a row of the same table, so the answer costs a read it was
  already paying for. It prints nothing where no earlier record met the floor
  — including round 1, because a sentence invented for a state that has none
  is worse than silence — `one reopening remains` where none has closed on a
  fix since, and `this record ends the run` where one has, carrying the same
  four-cell exit the refusal at the gate names.

  **It reads both of the walks the gate runs, because a quiet run is bounded
  by only one of them.** Floor `no`, then two rounds that neither reopened the
  run nor closed on a fix: nothing has closed on a fix, and the gate still
  refuses the third record. Reading one walk printed `one reopening remains`
  at round 2 and invited exactly the round that would be refused. It is also
  silent for a work item old enough that the gate grandfathers it, guarded
  separately for each walk, because a work item can be past one cutoff and not
  the other — one bound really enforced, the other only noticed.

  **And it runs each walk from every record whose floor row reads `no`.** The
  gate reads that row on every record, so a second one starts walks of its
  own. Only the count walk needs more than one starting point: the reopening
  walk never stops, so a later start's findings are all inside an earlier
  one's, while the count walk does stop — and an earlier walk that had already
  stopped hid a later floor record's walk entirely. Reading the earliest alone
  printed `one reopening remains` at a round the gate returned an error for,
  which is the same defect one floor record over.

  The floor record it names is the **earliest** whose row reads `no`, except
  in the count branch, where it is the record the firing walk started from —
  the only record the count beside it is true of. Keyed to the latest it would
  restart at every record it stops at and bound nothing, which is the failure
  the count itself was rebuilt for. (#207)

- **A coordinate the records arm printed used the platform's separator, so
  the same file read two ways.** The ledger arm's rows carry `/` because they
  were read from a file; the records arm builds every path it prints out of
  `os.walk` and `os.path.join`, so on Windows a refusal named
  `seal\specs\…\rounds\round-2.md` where a ledger row naming the same file
  said `seal/specs/…`. A coordinate is written with `/` everywhere else in
  this repository, and it is a thing a person copies and opens.

  The five printers inside `check_records` now go through one helper rather
  than five replacements, so a sixth built path added later is normalised or
  does not print. The split is **who spelled it**: a `--ledger` pattern comes
  back exactly as the operator typed it, which is the rule the display helper
  exists for and is unchanged.

  **The Windows leg of CI had been red on this since the commit that added
  the arm — through three review rounds and two fix passes.** Every round and
  every broad gate ran on macOS, where the normalisation is a no-op, so
  nothing local could see it. The case passes `ntpath` to the helper rather
  than skipping off Windows, which is how a POSIX machine removes the
  guarantee instead of resting on it. (#190)

## 0.8.3 — 2026-09-06

<!-- specs/1788686494-the-printed-ledger-name-collapses-through-relpath -->
- **The evidence check printed the name of a file it had not read.** Where a
  `--ledger` pattern crosses a symlink before a `..` — `--ledger
  'x/lnk/../ledger.md'`, with `x/lnk` pointing at `y` — the checker opened the
  file the pattern actually names and printed a header naming a different one.
  `os.path.relpath` folds `..` the way `normpath` does, by rewriting the
  string rather than by asking the filesystem, so it answered `x/ledger.md`:
  a real file, usually holding different rows. The exit code and the rows
  were right; the name a person reads and then goes and opens was wrong.

  A ledger path rendered for a person now goes through one helper that drops
  the root's own leading segments and touches nothing else about the
  spelling. Where a path is not under the root, it prints in full — longer
  than before, and naming the file that was read. That covers a local-mode
  root seen from a linked worktree, where the ledger genuinely sits outside
  the tree.

  **The issue named four places and there were five.** The fifth is the
  `--ledger narrowed this run` notice, which lists the ledgers a narrowed run
  did not read; it was missed because its variable is spelled differently
  from the other four. So the class was closed by following where a ledger
  path can reach rather than by searching for a name, and a test now
  recomputes that reach against the source on every run and refuses the old
  call anywhere in it. A sixth place added later is caught by that test as
  long as the ledger path gets there by one of the ordinary ways a value
  moves — assigned straight across, aliased, unpacked from a tuple, looped
  over, or handed to another function in this file.
  It is a guard against the edit somebody actually makes, not a proof that
  no such place can exist.

  What deliberately did not change: the suggestion list a broken row prints
  when its code looks to have moved. Those are scanned source files rather
  than ledgers, they are built downward from the repository root so they
  carry no `..` to fold, and they are normalised on purpose so they can be
  compared against the path a row spells. (#163)

<!-- specs/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback -->
- **A virtualenv the operator has made read-only ended `bin/test` in a
  traceback printed underneath a refusal it had already given.** The ignore
  that keeps `.venv` out of `git status` is written from a `finally` in
  `ensure`, which is what makes it an exit-level guarantee rather than a list
  of remembered paths — and it is also what puts the write on the two exits
  whose entire product is a sentence. `write_text` was unguarded, so on a
  `.venv` this process cannot write to, the floor refusal reached stderr and a
  `PermissionError` followed it. The write is guarded now and says what it
  could not do: it names the ignore, the reason, and that the virtualenv stays
  visible to `git status` until that write can succeed or the reader removes
  the directory. **The remedy names no cause on purpose**, because the guard
  catches four of them — no permission, a read-only filesystem, a full disk,
  and the path already being a directory — and an earlier wording said *make
  it writable*, which is wrong advice on two. Which one it was is carried by
  the reason. The refusals above it keep their wording and their exit codes,
  and the runner does not try to win the argument — a read-only `.venv` is
  the operator's. **The class is closed by construction rather than by a list**:
  `hide_from_git` holds the only write this module makes to the working tree
  itself, and everything else that lands there is a builder subprocess's,
  whose failure is already a return code the caller reads. The module
  docstring says so, and says the guard belongs to the module rather than to
  the function, because the class is one write only for as long as nobody adds
  a second. **A `chmod 555` fixture is not a guarantee, and asserting only *no
  traceback* would have hidden that**: root bypasses the permission bits and
  Windows ignores every bit but read-only, so on two of the three platforms CI
  runs the write succeeds and a case asserting absence would pass for the
  wrong reason. One case builds the real fixture and is skipped where `chmod`
  does not stop a write, with the reason written into the skip so it travels
  into pytest's own report; a second makes the write itself refuse, so the
  wording is pinned everywhere. Neither can pass on a write that succeeded.
  (#177)

- **A ledger row whose guarantee a change makes conditional gains the
  condition; it is not removed.** Two rows were in that position and both are
  repaired in place, because a row is removed when a change takes away the
  code it cites and this one took nothing away. The virtualenv row's claim —
  invisible to git on every exit of `ensure` — was never about the write
  landing, and on the one path where it does not land the row had been false
  before this change as well, in the worse way: the write raised through the
  `finally` and replaced the refusal with a traceback. So what was wrong was
  an unstated precondition rather than the mechanism, and the mechanism is
  exactly what the guard was written to keep. The new claims went into the
  work item's own fragment, which is where the fragment rule puts them.

- **A case that reads three named constants catches a rename and cannot see a
  fourth constant added beside them.** `docs/review-chain-spec.md` names the
  five values that can stand in the reach half of a `Contract changes` entry,
  and the case holding the document to them read `PYTEST`, `PYTEST_ONLY` and
  `NO_SITE` out of `round_record.py` by name. That is three ways of catching
  an edit to a value that exists and no way at all of catching one being
  added — the drift the paragraph exists against, where the document goes
  stale and the suite stays green. The set is now **derived** from
  `call_sites`' own `return` statements, so a value the function gains has to
  reach the document before the suite is green again. Measured rather than
  argued: with a sixth value added to the function, the derived case exits 1
  naming it and the named case passes. **Both are kept**, because neither
  covers the other, and **which half each one holds was measured, after a
  first attempt asserted it and got it wrong.** The sentence saying which of
  the five values is a unit name is read by the older case alone, so removing
  it from the document reddens that one and leaves the derived one green; a
  value added to the function is seen by the derived one alone. A rename and a
  reword redden both, because the derived case checks the same three constants
  by name before it starts. The wrong version claimed the rename for the older
  case alone, and it stood in the comment a maintainer would read while
  deciding to delete one of the two — which would have deleted the case
  holding the half nothing else holds.

  **What a `return` hands back is not the same as what appears inside it**,
  and the first derivation confused the two. It collected every string
  anywhere in a `return`, so a comparison operand, a keyword argument, half of
  an f-string and a dictionary key all arrived as reach values; the case then
  went red naming a word the function cannot produce, and told the reader to
  add it to a shipped document. It now asks what each kind of expression can
  hand to the caller, and the refusal names both directions — add the word, or
  fix the derivation — because two steps still deliberately over-reach. What
  the derivation cannot see is recorded beside it and split into under-reach
  and over-reach: five shapes hand a value back across a statement or a call
  and read as nothing, six more are one branch away, and two are read though
  the function may never hand them back.

  **Reading what a function returns means stopping where that function
  stops.** The same confusion survived one level up: the walk that collected
  the returns descended into nested scopes, so a helper written inside the
  function under review handed over a word that function never returns — and
  the refusal then sent the reader to the part that had never seen the node.
  The walk now stops at anything that opens another function scope. Two node
  types do, because only a function body may hold a `return`; a class or a
  lambda is reached through one of those two rather than past it, so listing
  either would add a member no test could ever justify.

  **The derivation reads the generator's text as an argument, and that is
  what makes it testable at all**: today the function under review names a
  constant in every return and writes no literal into one, so against the
  real module the branch that reads a literal is unreachable and a mutation
  deleting it survives — which is what the mutation loop found, in the very
  case written to close a list that would go stale. Ten mutations over the
  derivation's branches and eight over the walk around it, one at a time,
  each now killed by a named case. (#177)

<!-- specs/1788700685-two-value-shaped-odd-rows-end-the-report -->
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

## 0.8.2 — 2026-09-06

<!-- specs/1788613827-a-runs-report-carries-one-comparison-table -->
- **A run's report carries one comparison table, and the row nobody can
  produce by hand comes out of one command.** #161's run summed `usage` over
  its transcript and its subagents with a script written for that occasion,
  and a number summed one way this run and another way the next is worthless
  to compare against. `skills/verify/SKILL.md` §*Measure the segment, and
  feed the flow log* now states the run-level table: nine rows — rounds, wall
  clock, commits by kind, findings by severity, findings by `Location`, the
  records' share of the diff, model turns with the three token columns,
  segments per kind, and the broad gate — each with the cell saying where its
  number is taken from. Three sentences ship with it, each pinned by a case:
  the tokens are counted rather than estimated and counted the same way every
  time, naming the command and all three `usage` fields; a comparison against
  a run whose transcript covered only part of its branch says so in the prose
  rather than as a column, because a column would make it a field and there
  is no reader for one; and the table carries **no verdict** — what a row
  meant on one branch goes in the comment beside it. The rows name no issue
  number and no milestone, so the section still ships to repositories that
  have neither. It is **not a third destination**: the table joins the
  segment readings in the rolling log the section already names. Two rows
  say what they mean rather than leaving it to each run: a **record** is
  anything under `seal/` — the work item's documents, the ledger and its
  fragments alike — which is the review chain's own definition and what both
  the `Location` buckets and the share row count by, and the **broad gate**
  row asks whether the gate ran and at what SHA, which is what the cell it
  reads actually carries. And the section says which file of a project
  directory is a run's main transcript, because `--latest` takes the newest
  file anywhere beneath it and on a run with segments that is usually a
  segment. (#170)
- **`session_cost.py` prints the token line, over the whole run rather than
  the transcript it was handed.** The script already opened exactly those
  files and already read `usage` — it threw away everything but
  `input_tokens` and `cache_read_input_tokens`, and it read one file where a
  run has several. It now sums `output_tokens`,
  `cache_creation_input_tokens` and `cache_read_input_tokens` over the given
  transcript **and** every `*.jsonl` under the `<session-id>/subagents/`
  directory beside it, always and behind no flag, and reports the same under
  `--json` as a `tokens` object. A message's usage counts once however many
  rows it is split across, which is the trap the existing `context_growth`
  dedup already exists for. **Two turn counters, on purpose**: a turn here is
  an assistant message carrying `usage`, where `tools_per_turn`'s denominator
  is a message carrying a tool call — the per-segment bars in
  `docs/review-handoff-protocol.md` are calibrated against that ratio, and
  widening it would move a published threshold with nothing saying it had
  moved, and the printed report names each count's own scope so the two
  cannot be divided into each other. **No way this degrades ends the report**
  — an unopenable transcript is skipped, an unparseable line dropped, a field
  a harness stops writing contributes zero, and a value that is not a number
  counts as none. Almost every one of those makes the totals smaller; the one
  that goes the other way is a split message whose rows carry no usable key,
  counted once per row instead of once. So the line prints both counts: the
  transcripts it opened, which the same report's `Agent` call count is the
  cross-check for at 18 against 17 on a real run, and the turns, which is
  where a doubled run would show. Seen red first: each of the four new
  behaviours against the old script, and the guard for a transcript that
  cannot be opened pinned by a case calling `token_totals` directly, after
  mutation testing showed a directory fixture never reaching it. Prompt
  budget: zero. (#170)
- **A transcript that only read and thought reports what it spent.** The
  token line was summed after the no-tool-calls guard, so a transcript
  carrying `usage` and no paired tool call exited 1 with an empty stdout —
  and that transcript is a segment, which is exactly what the table's
  per-kind token row is summed over. It now prints the token block and says
  why there are no time lines. A transcript with neither still exits as it
  did. (#170)
- **The two documents that carry the table point at its owner instead of
  copying its rows.** `docs/review-handoff-protocol.md` §*After the run — the
  per-segment bars* says the bars judge a segment against its kind and the
  table judges a run against the last run measured — a reader who met only
  the bars had no way to know the second instrument existed — and names the
  owning section by file and heading. `skills/commit-pr-convention/SKILL.md`
  §*Pull request bodies* states the chain section's shape for a work item
  routed through the review chain: the comparison table first, then what the
  rounds found, so a reader who stops after the first screen still has the
  numbers. PR #162 wrote that section as prose and PR #168 as a table, which
  is the whole of what a fixed set of rows buys. Both refuse the rows
  themselves, and the refusal in
  `tests/test_the_chain_section_has_one_shape.py` is itself held to the
  owner's current wording — a row renamed in `skills/verify/SKILL.md` turns
  `test_the_pinned_rows_are_the_owners_own` red rather than leaving a green
  case guarding a string nobody would paste. Eleven mutations over the two
  paragraphs, nine of them because the first red proved only that the
  paragraph was absent: a case red because its subject does not exist has not
  been seen red for its own reason. (#170)

<!-- specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite -->
- **`bin/test` runs this repository's suite from an environment it builds
  once.** The command `CONTRIBUTING.md` named resolved and installed its
  dependency on every call — 55–58 seconds each, paid on all seventeen test
  calls of one measured segment (#133) — so the gap was never a missing
  command, it was a command that is cheap only the first time you forgive it.
  `bin/test` and `bin/test.cmd` join the five `bin/` pairs already there over
  `.github/scripts/run_tests.py`: a virtualenv at `.venv` built on the first
  call and reused after, arguments passed straight through, the repository root
  resolved from the script's own path so it works from any directory or
  worktree, and the interpreter it used printed every time. Measured on one
  machine: **5.24 s cold, then 0.60 s** — and the claim is not that the first
  call is cheap but that it is the only one. **Every failure is a sentence
  rather than a traceback**, which is what a command that writes to the working
  tree owes: no `uv` and no 3.12-or-newer interpreter names both and says which
  to install, a build step that exits non-zero names the directory to remove, a
  build that leaves no pytest behind stops instead of rebuilding forever, and a
  copy of `bin/` with no runner beside it says so — on both platforms, in the
  same words. The file has to parse and run under Python 3.9 to print the first
  of those, so nothing in it is newer than the floor it refuses. **The
  virtualenv is invisible to git on every path that can produce one**, and that
  is a guarantee about exits rather than a list of paths: `uv venv` writes
  `.venv/.gitignore` and `python -m venv` writes none, so the runner writes it
  itself, from the one function that reaches a virtualenv at all, on every way
  out of it. A list was tried first and went short twice — it named a build
  that succeeded, then a build that failed partway and a `.venv` merely
  adopted, and review still found two more: the one adopted `.venv` the floor
  **refuses**, which is also the one least likely to carry an ignore of its own
  because every version that refusal rejects predates the 3.13 where `python -m
  venv` began writing one, and a directory an earlier run left on a machine
  where neither builder can now finish. **The floor is asked of an adopted
  environment too**:
  the version both builders record in `pyvenv.cfg` is read rather than run, and
  a `.venv` below the floor is refused with a sentence naming what to remove. A
  directory that says nothing about its version is kept — refusing on silence
  turns one unknown into a suite nobody can run. No `-n auto`, because
  `pytest-xdist` is CI's install and a freshly built environment has pytest and
  nothing else. (#156)
- **A session finds the runner instead of being handed it, or guessing.**
  `CONTRIBUTING.md` §*Running the checks* names `bin/test` first and shows the
  narrow `bin/test tests/<file> -q` a segment types, with the sentence saying
  the full five-minute run is the orchestrator's, once, after the review rounds
  settle. The `uvx` form stays as a labelled **no-write** fallback — for a
  reader who does not want a `.venv` in their tree — carrying the 55–58 seconds
  that demoted it, because a fallback named without its cost gets promoted back
  by the next reader. The floor sentence now names `FLOOR` in the runner, so
  the document's 3.12 and the code's are traceable to each other rather than
  two numbers that happen to agree today. `docs/review-handoff-protocol.md`
  §*The handoff before round 1* takes a fifth requirement: **a runner the
  repository ships is found, not typed into every prompt**, with the old
  requirement kept intact for a repository that ships none. What bought it:
  four build segments of one work item read repeats of **17 s, 2 s, 0 s and
  0 s**, and the only difference between them was whether the orchestrator had
  remembered to type the runner into the spawn prompt — a requirement met by
  hand, once per prompt, is met until somebody forgets. `agents/smith.md` is
  the carrier that closes that, because it reaches a segment at startup with
  nobody typing anything, and it names the protocol's section rather than
  restating the rule. (#156)
- **A round record's `Contract changes` row now has its vocabulary written
  down.** `docs/review-chain-spec.md` §*The fix surface* defined the reach half
  as the call sites of a changed unit and named none of the five values the
  generator actually writes there — the enclosing unit, the file's basename,
  and the three words `round_record.py` substitutes: `pytest` when any caller
  sits under `tests/`, `pytest only` when those are the whole reach, and `no
  call site found` when there is none. Reading a correct cell as a mistake cost
  a review round of this very work item. The three words are read out of the
  generator's own constants by the case that pins them, so the document cannot
  drift from the code. (#156)

<!-- specs/1788661274-the-roll-names-the-next-version-by-guessing -->
- **A release rolls the measurement log only where a new version has actually
  shipped, and the log is named after the version it rolled from.** The old
  arithmetic guessed the next number — `0.8.1` became `0.9.0` — and at the
  0.8.1 release that guess closed #166, which had been opened at the 0.8.0
  release and held the measurements 0.8.1 had just been written with, then
  opened #172 under the identical title. Two issues with one name, one of
  them closed, and the readings carried across by hand. The roll now reads
  the open log's title for the version it says it rolled from and compares
  that with the version in the checked-out tree: equal means this push
  shipped nothing new — a re-run of the job, or a merge that moved no
  version — and the run closes nothing, opens nothing, and exits 0 saying so.
  `docs/branch-and-release.md` is why the title states a fact instead of a
  prediction: whether the next number is a minor or a patch is known at the
  end and not at the cut, so at the moment the roll runs the just-shipped
  version is the one thing certain and the next one is the one thing nobody
  can name. `next_version` is deleted with the guess it made. **Both
  outcomes leave the job green**, so each prints a line — `rolled:` names the
  issue closed and the title opened, `nothing due:` names the log and the
  version — and a reader of the release log tells them apart without opening
  the tracker. **A title the script cannot read as its own is due rather than
  silent**, and that direction is chosen rather than incidental: read as
  *not due*, an unreadable title stops the log forever with the workflow
  green, which is the failure being fixed one step over; read as *due*, it
  costs at most one roll that was not owed. **Its own means the whole title
  from the first character** — the `chore: ` prefix and the marker, then a
  version — so a title carrying those words somewhere inside it, like
  `docs: explain flow measurement — after 0.8.2`, names no version this roll
  will act on. The comment posted on the log being closed now says what
  replaces it and quotes the successor's title, where it used to promise a
  log for the version the release ships next — the prediction this change
  removes. (#155)
- **What a log's title means now, and what the older ones mean.** A rolling
  log is titled `chore: flow measurement — after 0.8.2`, and the version in
  it is the one the log rolled from: that log opened at the 0.8.2 release,
  holds what was measured since, and is closed by whatever ships next. A
  title written before this change names the version the log was **predicted
  to be for**, which is how a 0.8.1 release came to close a log titled for
  0.9.0. Those are **not rewritten** — a retitle falsifies every comment that
  cites them — and the marker the roll now writes appears in none of them, so
  each of them reads as a title stating no version at all, which is always
  due. The first release after this change rolls the last old-convention log
  and the convention retires itself. `docs/issues-and-milestones.md` carries
  the format, the condition and both meanings; `skills/verify/SKILL.md` gains
  the boundary it was missing, since a rolling log now opens at a release,
  accumulates until the next version ships, and is discarded by the release
  that ships it — where the skill used to describe it as one version's,
  ending when that version shipped, which points a reader at an end that has
  already passed. (#155)

<!-- specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading -->
- **A fenced block in a reviewer's report must close, and its span must not
  cross a line `round_record.py new` reads the report by.** A fence that
  crosses one hid a whole section from every later reading, and each reading
  had its own wrong answer for the absence: the record got the empty template
  for `## Executed probes` and `## Deferred`, `nothing to drain` for a
  Deferred section the reviewer had in fact written, and exit 0 both times.
  Where the section was required the message blamed the reviewer for a
  section they had written — `the report has no ## Verdicts section`. The
  refusal now names the heading the fence swallowed and says what to do about
  it, so the writer is told what to fix rather than that something is wrong.
  **#169 called the late-closed fence *the one member of the class left
  open*, and it was not.** Decomposing on one boolean over one span — a fence
  has a closer or it has not, and where it has one the span either crosses a
  line the generator reads by or it does not — gives seven members, of which
  two silently lost a whole table rather than the one #169 named, and three
  more were caught only by the message that blames the reviewer. The issue's
  proposed fix, a membership test against a tuple of section constants inside
  `fenced_after`, reaches neither of the two: a fence that takes
  `## Executed probes` leaves the report with no probes section, so `build`
  never calls `fenced_after` at all and no guard living in that function
  could see the shape. **The guard therefore lives over the whole report and
  keys on the span rather than on the name**, and it derives the lines a
  fence may not cross from `REPORT_TABLES`' headings and `TERMINAL_LINES` —
  the module's own statement of what it reads, which nothing in the module
  read before this. A section added later is guarded, and gets a case, by
  being added there; no second list exists to go stale, which is what the
  membership test would have been by the next section. **What is refused is a
  report losing a section, never a fence mentioning one.** A reviewer of this
  generator pastes record-shaped blocks, headings and all, and a rule reading
  the mention would stop the tool on its own review rounds — so the guard
  asks whether the heading still stands outside the fence. A `#` at column 0
  is a Markdown heading and a Python comment both, and only the fence tells
  them apart, which is why nothing in the guard reads the `#` character.
  **That seven-member count is a count of one partition and not of the ways a
  report loses a section silently, and reading it as the second cost three
  more refusals.** The partition was taken against the headings and the
  terminal lines, in the one text the report-wide check reads, for the one
  input it reads. Applied to what it had not been: the generator reads the
  report a second time, verbatim, when it copies a fenced block — so an
  opener inside an HTML comment is invisible to the check and an opener to
  the copy, and the record went out with two sections unreadable at exit 0.
  It reads the table ROWS under a standing heading, not the heading alone —
  so a fence taking the rows left `## Deferred` in place and the record read
  `nothing to drain` beside a row the reviewer wrote. And it reads a second
  input, the round paragraph, which is spliced above every section a reader
  looks up and had never passed through the guard at all — an open fence
  there blanked the record from `## Verdicts` down, and the record was
  written before the failure. All three are refused now, each with a message
  naming what the fence took and what to do about it. The row rule keeps the
  same limit as the heading rule: a fence quoting rows beside a table that
  still stands is copied as it always was, which is what lets a reviewer of
  this generator paste record-shaped blocks into a report it will accept.
  **A fence is not the only hider, and that list of three was one short.**
  Every text reaches the generator through `readable`, which blanks in two
  passes and runs `strip_comments` first — so an HTML comment opened and
  never closed blanks every line below it exactly as an open fence does, one
  pass earlier, where no fence question can see it. The missing member was
  created by the fix for the round paragraph above: that guard asked the
  fence question of the comment-stripped text while the paragraph is spliced
  into the record verbatim, so an unterminated comment wrote the record and
  left four of its five sections unreadable to every downstream reader. Both
  the report and the round paragraph now ask both questions, the comment's
  first — an open comment blanks the closing fence of every block below it,
  so the other order names a fence that is closed in the text as written. On
  the report the same question replaces a message that sent the writer to add
  a `Needs a fix:` line they had in fact written. **What is left is one cell,
  named rather than assumed**: a comment that is balanced in the report and
  half in the record, because a copied row and a copied block are both slices
  of it. Refusing that takes a question about balance across a slice rather
  than about a hider that never closes, since a copied block may legitimately
  carry a whole comment — so it is recorded at the coordinate with what it
  costs, a straddle in a verdict row losing three whole sections. (#169)

## 0.8.1 — 2026-09-05

<!-- specs/1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records -->
- **A review round's record is generated from the two agents' reports rather
  than written by the orchestrator, one cell at a time.** Issue #161 counted
  the branch before this one (#153 + #150): fifteen rounds and 22 h 47 min for
  two features' worth of review. From its 70 commits, with gaps over two hours
  cut to two, **12.8 h of its 18.8 active hours sat in front of record commits
  and 3.6 h in front of fix commits**; 33 of its 65 findings were located in a
  record rather than in code, and 50 of the 61 findings after round 1 sat in a
  file the preceding fix pass had written. The loop that reviewed the tool's
  own paperwork had a gain at or above one, and that is why this release
  exists.
  `skills/code-review/scripts/round_record.py` writes `rounds/round-N.md`.
  `new` takes the warden's report and the round paragraph of the spawn prompt
  and derives every field row from something nobody typed into a cell:
  `Target SHA` from a ref that has to resolve, `PR` from `gh` or `not yet
  opened`, `Fixes checked by` and the two surface rows at their landing
  values, `Needs a fix` and `Loses a record or crashes` from what stands after
  the colon in the report's two lines, the verdict, probe and deferred tables
  copied row for row, `Inherited coordinates` from every earlier record's
  `Location` cells. It sets round N-1's `Fixes checked by` to `round-N` — the
  reach-back the orchestrator forgot five times on the last branch — ticks
  `Pass` when no verdict is open, and runs `chain_check --worktree` before it
  returns, told the pull request is a draft unless `gh` says otherwise.
  `close` takes the smith's fix table and the fix range, applies the verdicts,
  and measures `Contract changes` and `New units` from an AST comparison of
  the range's two ends — every changed signature with the enclosing unit of
  each call site, every added top-level unit with its depth. **A unit at
  depth 2 is refused at the keyboard, before any cell is written**: a `fixed`
  finding whose `Location` sits inside a unit an earlier record's `New units`
  names, in a file the range adds a unit to. The refusal names the unit, the
  finding, the record whose row names the parent, and the exit the rule
  already gives. What the orchestrator still writes by hand is one thing, the
  round paragraph of the spawn prompt, which `new` copies in verbatim.
  Every cell writer takes a structured value: a pipe or a newline anywhere,
  or a comma inside a surface name, is refused before anything touches the
  disk, and there is no `--grounds` or `--note` flag for a session to hide
  prose in. Nothing here commits; the commit is the orchestrator's, made from
  a record it has read. When every verdict closes without a fix word —
  `answered`, `withdrawn`, `not a defect`, `deferred <home>` — both
  subcommands land the record on `no fixes to check` and a bare `none`, from
  one spelling of the derivation, because a round that commissioned no fixes
  will never have any and *not yet written* is false the moment it is
  written. That is the capped run's last record, and the check accepts it.
  Seen red first: every refusal at a named fixture, the two-record reach-back
  read back, the depth-2 refusal on a fixture whose earlier record names the
  parent; 29, 47 and 6 mutations over the three phases' units, none surviving
  a second pass. Prompt budget: zero. The AST comparison reads Python; a file
  it cannot parse, or another language, is read by a diff-line heuristic and
  the cell's trailing comment names the files read that way. (#161)
- **`chain_check.py --worktree` reads the records as the working tree holds
  them, so a check run before the record commit judges the cell it is about.**
  Three 🔴 of the last branch reached CI because the check read `git show
  HEAD:<rel>` and a record edited on disk was invisible to it until committed.
  Under the flag `read_record` opens the file on disk, `changed` includes
  uncommitted and untracked paths so a record just written is judged and its
  `Target SHA` held to the branch, and the first line of the output says the
  working tree was read. **Local only**: CI keeps reading `HEAD`, because a
  working tree that differs from HEAD is what CI never sees and the more
  permissive direction is the wrong one there. Seen red in both directions
  before the flag existed — an uncommitted edit that breaks a record, and one
  that repairs it, each visible only with the flag. Failure direction: at the
  pull request nothing changes; locally it blocks more, on the record about
  to be committed, which is where a refusal costs a correction rather than a
  round. Prompt budget: zero. The path is rebuilt from `/`-split parts with
  `os.path.join`, as the rest of the checker does, and no case ran on Windows.
  (#161)
- **The floor's reopening exception is bounded to one, and a run that would
  reopen twice ends `capped`.** A verifying round that opens something is a
  finding round, its fixes need a reader, and that reader may open something
  again; every record the floor's count stopped at was itself a record that
  met the floor, so the count restarted there and nothing bounded the chain.
  #161 measured fifteen rounds through that door, with the exception used by
  every verifying round of the branch.
  `stopping_floor` now makes a second walk over the same later records, and it
  never stops: it counts every later record whose verdicts closed on a fix,
  wherever it sits, and refuses the second, naming it by file and the floor
  record it follows. The message carries the exit in one spelling
  (`CAPPED_EXIT`): every finding still open becomes an issue, its verdict
  reads `deferred #N`, the record's `Fixes checked by` reads `no fixes to
  check`, and the pull request says `chain: capped`. Keyed to `REOPEN_FROM`,
  whose value is the id of the work item that added the rule — the seventh
  cutoff of the shape `STRICT_FROM` … `ORDER_FROM` carry — so earlier work
  items print and nothing red is inherited. `docs/review-chain-spec.md`
  §*The reopening — one, and then the run is capped* owns the rule; the
  skill, the template, the protocol and the warden link to it in one sentence
  each, where four of them used to state the unbounded version.
  **The vocabulary the exit needs.** `deferred <home>` joins `CLOSED_WORDS`
  and not `FIX_WORDS`: `deferred #170` and `deferred seal/follow-up.md` close
  a finding on the issue or the file it went to and produced no code, so `no
  fixes to check` beside them is the truth and a last record whose every
  verdict reads that way may tick `Pass`. A bare `deferred` — the word with
  nothing after it, or only a separator — stays OPEN and comes back as
  `deferred (no home)`, the direction every verdict the checker cannot read
  takes: it says something was left and not where. `templates/config.md`'s
  list of strings no language row governs carries the word.
  Seen red: each refusal at a named fixture before the walk existed, the
  cutoff at the boundary second, the capped run's legal end, the bare word
  through a ready pull request; the well-written two-record run kept green,
  and this repository's own records pass under the new arm. Nine mutations
  over the walk and the vocabulary, nine killed. **Failure direction: blocks
  more.** A run that reopens twice is refused where it used to pass. What it
  lets through, stated rather than left to be found: a defect the second
  reopening would have found ships as an issue rather than as a round — the
  trade `questions.md` Q2 chose with the alternative on the table, since
  removing the exception entirely would have shipped round 7's floor bug and
  three Windows defects of the last branch as issues too. Prompt budget:
  zero. The walk reads records through the same reader as every other check,
  with no platform-dependent path in it. (#161)
- **Nine rules bind a review run, each stated by one carrier and linked from
  the others, so a run's rounds come from the code rather than from the
  tool's own fixes and records.** Where each one lives, with what it
  measures:
  1. A finding whose `Location` is a record (`seal/specs/**`,
     `seal/ledger/**`, `seal/ledger.md`) is a correction and not a round —
     what `chain_check` or `evidence_check` refuses is corrected in the
     closing commit, what they do not read is prose, and `Needs a fix` does
     not count it. Owner `docs/review-chain-spec.md` §*The last round
     verifies*, with the count: 33 of 65 findings located in records, records
     55 % of the diff.
  2. A fix pass may not add mechanism — a rule, a checker, a template
     section, a walk. A finding closable only by one is an issue and the
     verdict is `deferred #N`; the depth rule already refuses the second
     level, this is the first. Owner `skills/code-review/SKILL.md` §*A fix
     pass adds the unit that pins it*, with round 4 of the last branch as the
     measurement: a rule, a reader and two cases built to close one 🟡, at
     the cost of round 5's 🔴, issue #159 and half of round 6.
  3. 🟡 means *a defect the release would ship* — the tool does something
     wrong or tells a person something wrong. ⬜ is new beside it: a sentence
     that reads badly while the behaviour and the fact stay right, fixed in
     passing or not at all, never counted by `Needs a fix`. Half of the last
     branch's 53 🟡 were true sentences about prose. Owner the skill's
     §*Findings format*; `agents/warden.md` §Report puts the one question per
     finding.
  4. The reopening is one and the run ends `capped` — the entry above.
  5. A fix pass owes code and a test. It writes no `phases/phase-N.md` and no
     `plan.md` row; the fix table in its hand-back is its record and
     `round_record.py close` writes the rest. Owner `agents/smith.md`.
  6. The draft pull request opens at the end of the build, before round 1, so
     the platform legs run beside the chain; three Windows-only defects
     arrived after round 12 on the last branch. Owner the skill's
     §*Orchestrator: the pull request opens before round 1, and a phase is
     re-run*; `docs/flow.md`'s order inside a ticket carries the step.
  7. A session that has compacted hands the next round to a fresh one, and
     the generated record is the handoff. Owner the same skill section.
  8. A moratorium on new parsed fields in `round-N.md` and new rows the
     ledger must carry, until the next minor release. This work adds a
     subcommand and a verdict word and no field. Owner the spec's §*What the
     record carries*.
  9. A hand-back's verification claim is a claim: before the orchestrator
     spawns the next phase it runs the closed phase's suite and the lint of
     its changed files itself and reads the output; the broad gate still runs
     once, after the rounds settle. Owner the same skill section as 6;
     `docs/review-handoff-protocol.md` gains §*After a phase — the hand-back's
     claim is re-run*.
  `tests/test_the_rules_have_one_owner.py` holds the same table as pins: the
  owner states each rule, every link names its owner, and a walk over `docs
  skills agents templates` holds the count rule's phrase to the owner and its
  links. Every changed sentence was seen red with the sentence stashed — 40
  mutations over the three owner files and 24 over the five linking carriers,
  none surviving. Every sentence that said the orchestrator writes a record
  cell now names the generator; the three that are about the reviewed-HEAD
  mark, which the orchestrator does write, were left true. (#161)
- **The warden's report carries the record's three tables in the record's own
  column headers, and a fix pass hands over a fix table.** `agents/warden.md`
  §Report asks for `## Verdicts`, `## Executed probes` and `## Deferred`
  beneath the findings prose, with `| # | Finding | Location | Verdict |
  Grounds |`, `| What was run | Result |` and `| Finding | Where it went | Who
  answers it |` — the generator's parser and the warden's headers are one
  constant, pinned across both files, so a finding that is not a row of the
  verdict table reaches no record and no orchestrator prose sits in a parsed
  cell. The two terminal lines are unchanged. `agents/smith.md` and
  `skills/implement/SKILL.md` §5 give the fix pass `## Fixes` with `| # |
  Verdict | Commit or grounds |`, one row per open finding — `fixed` with the
  commit, `answered` with the grounds, `deferred <home>` with the issue or
  the file — and `round_record.py close` applies it; the depth of a unit the
  pass added is measured by `close` from the diff rather than declared in the
  hand-back. `templates/sdd-round.md` says the record is generated by `new`
  and closed by `close`, keeps its comments as documentation of fields a
  generated record does not copy, and offers `deferred <home>` in the verdict
  vocabulary; `templates/sdd-phase.md`'s `Ran by` comment names the
  `--ran-by` value the generator writes. The reports themselves are saved to
  the session's scratch directory and not committed: the generated record is
  their durable form, and a second file per round would be one more file the
  checker had to learn to ignore. (#161)

## 0.8.0 — 2026-09-05

<!-- specs/1788472135-the-run-outlives-its-last-finding -->
- **A review run now has a floor as well as a ceiling, and a fix pass now
  has a bound on what it may create.** Three rounds, and five while a 🔴 is
  open, was a ceiling with nothing under it, so it got spent like a budget:
  #81 ran seven rounds and the last three found nothing that leaves the root
  and nothing that crashes. `docs/review-chain-spec.md` and
  `skills/code-review/SKILL.md` now state the floor — **stop when a round
  finds nothing that leaves the root and nothing that crashes** — and say
  where the rest of what that round found goes, which is deferred with a
  named answerer or an issue. The reviewer answers it in a line of its own
  the way it already answers `Needs a fix`, `agents/warden.md` carries that
  line in both the passage that explains it and the report format a reviewer
  copies from, and `round-N.md` gains a row of the same name:
  `| Loses a record or crashes | no |`, or `yes — <what>`. It is a second
  terminal condition rather than the first one reworded, and the two come
  apart — a round can need a fix and still stop the run — so the three files
  that called `Needs a fix` *the* answer the run ends on now call it one of
  two. **The verifying round is what the floor leaves standing**: a record
  that met the floor may be followed by one more, the round that reads the
  diff of the fixes that closed it, and a second one is the run carrying on
  past its own stopping rule.
  **The rounds the floor removes are the rounds that were reading what each
  fix pass created, which is why the second half ships in the same release.**
  Measured across four rounds of #82, three consecutive rounds found their
  finding inside the previous round's fixes, every time in the unit the fix
  added rather than in the fix itself — by construction the fix ships
  reviewed and the unit it added ships unreviewed, in one commit. The bound
  is **a fix pass may add a unit; that unit's fix may not**, stated in
  `skills/code-review/SKILL.md` and `agents/smith.md`, and `round-N.md`'s
  existing `New units` row now carries the depth of each entry —
  `unit (depth 1)`, entries separated by `;`. The depth goes per entry rather
  than in a row of its own because one fix pass can answer a finding in old
  code and a finding inside an earlier unit in the same breath, and one
  number for the round would be false of one of them. **Where a refused unit
  goes is written in the same sections as the rule**, one phase ahead of the
  check that refuses it, so no session meets *this unit may not exist* with
  nowhere to put it.
  **`chain_check.py` reads both rows at the pull request rather than leaving
  them for whoever is awake.** A missing floor row fails; an empty cell, a
  word that is neither answer, and `yes` with nothing after it fail on any
  record; and a `no` followed by two or more later round records fails,
  naming the exit. A `New units` entry with no depth fails, one at depth 2 or
  above fails with the two places the unit goes instead named in the message,
  and one carrying two units under a single `(depth N)` — the comma spelling
  the row used before the depth existed — fails as well. `none`, with or
  without a reason, stays an answer to `New units` as it was, and a trailing
  `;` on it no longer turns it into something else.
  **`Needs a fix` stops being a row nothing reads**, which is what keeps the
  bound above from refusing the one sequence the documents require. A
  verifying round that opens something is a finding round, so its own fixes
  need a reader, and that reader is a third record; the count therefore stops
  at the first later record whose `Needs a fix` says the run reopened. The
  row takes the floor's `no` / `yes — <what>` vocabulary and the same cutoff,
  and it is grandfathered whole rather than only when absent — it carried
  free text for three releases with nothing reading it, so a value written
  earlier was held to no vocabulary.
  **`docs/review-handoff-protocol.md` moves to draft 1.0**, with the floor
  row, the depth and the separator in `New units`, the depth's own adoption
  cutoff, and a section for the floor and what may follow a stopped round.
  **Older work items are not made red.** Both rules are keyed to the id of
  the work item that wrote them, the way `STRICT_FROM` and `SURFACE_FROM`
  already are: a record whose work item began before the cutoff prints
  instead of failing, because a merged record has no honest repair and a run
  that went past its floor can only be repaired by a round nobody can spawn
  now. A row that is present and malformed is refused at any age, since
  formatting is always the author's.
  **What no check can see, recorded rather than parsed away:** a depth
  declared wrong — `(depth 1)` on a unit that is really second-level. The
  rule is a declaration, and the verifying round reading the `New units`
  surface is what looks at it. `templates/config.md`'s list of what a
  `Record language` row does not govern grows by the new field name, the
  `depth` marker and the floor's `no` and `yes`, so a repository writing its
  records in another language is told which words stay English. (#110, #117)

<!-- specs/1788486395-the-roll-opens-the-next-log-with-no-body -->
- **A measurement that only meant something across versions was being written
  to the issue the next release deletes.** Two issues collect the same shape
  of comment — the rolling `flow-measurement` log, which
  `.github/scripts/roll_flow_measurement_issue.py` closes and replaces every
  time a release reaches `main`, and a durable ledger that is kept across
  versions — and `skills/verify/SKILL.md`'s "Measure the segment, and feed the
  flow log" named only the first. So a rate held against a previous version's
  baseline went where it would be discarded, which happened on 2026-09-04 and
  is what #136 opened for. The section now says which reading goes to which: a
  segment's own numbers to the rolling log, readings that span versions to the
  durable one. **A repository declares its durable log with a `flow-baseline`
  label** — the same lookup shape as the rolling one, a label rather than a
  number, and the same exactly-one-open invariant. A repository that never
  creates it is unaffected, because an absent label is the no-op it already
  was.
  **Zero open used to be one fact and is now two.** A repository that never
  measured and one whose log stopped both read zero, and only the second is a
  broken invariant. `gh issue list --label flow-measurement --state all` tells
  them apart for one call. A session that finds the second **names it and
  opens nothing**: two sessions finishing segments at the same moment would
  both read zero and both create, and the next release then fails on two or
  more, which is the same invariant broken from the other side.
  **Every rolling log used to be born empty.** The roll passed `--body ""`, so
  a new log said nothing about what it was for and carried no path back to the
  one it replaced. It now opens carrying the issue it rolls from, the version
  it closes on, and the durable ledger — found by the `flow-baseline` label
  rather than hardcoded, and left out of the sentence entirely where a
  repository has none.
  **The same create asks for this repository's index label and its `log:`
  milestone, and neither can fail a release.** A milestone is repository state
  that gets renamed and deleted, and `gh issue create` fails the whole call on
  a name it cannot resolve, while the invariant this script protects is the
  one-open rule that no milestone touches. The create is attempted with both,
  then with the label alone, then with neither, and each fallback writes into
  the body of the issue it opens what the attempt above it could not set — the
  body, because that is the artifact a person opens and a workflow log is not.
  A failed attempt re-reads the open-issue list before retrying, so a create
  that reported failure after it had actually landed ends the ladder instead
  of opening a second issue.
  **This repository's own durable log (`#51`) carries the new label**, so the
  0.9.0 log opens pointing at it without anything further being done by hand.
  (#136)

<!-- specs/1788491830-a-segments-record-says-what-it-cost -->
- **A segment's record said what it was asked, what it found and which commit
  it read, and never what ran it.** Every segment of two work items was
  metered this week and posted to the flow log, and not one of those readings
  can be attributed afterwards — they all ran on the same model, and that fact
  lived only in a session transcript. `templates/sdd-phase.md` and
  `templates/sdd-round.md` now carry a `| Ran by |` row, and
  `docs/review-handoff-protocol.md` (draft 1.1) carries it in the field table
  with its `Required` column answered.
  **The row names the agent AND the model**, joined by the word `on` —
  `specseal:smith on <model>`. Either half alone answers neither question the
  numbers raise: an agent without a model cannot be compared against another
  run of the same agent, and a model without an agent cannot be told apart
  from the orchestrating session's own turns. The joining `on` is a word
  rather than a punctuation mark on purpose, because a separator inside a code
  span splits the cell carrying it and that has bitten these records twice.
  **It is the spawning session's row, never the segment's own.** An agent is
  told what it is, so a value it writes about itself is the value it was told,
  and the model is a spawn-time argument the orchestrator chose —
  `agents/*.md` pins none. It is the reach-back `Fixes checked by` and the
  fix-surface rows already make. `skills/code-review/SKILL.md` and
  `skills/verify/SKILL.md` both say so, because they are read by different
  sessions at different moments.
  **`unknown — <why>` is an answer and a bare `unknown` is not**, in the shape
  `nobody — <why>` already has. A session spawning through another harness may
  genuinely have no name for a model, and a vocabulary offering only the
  confident answer gets the confident answer written whether or not it is
  true.
  **`chain_check.py` reads the row**, so it is enforceable rather than true
  only while somebody is awake. An absent row fails for work items begun on or
  after `RUNNER_FROM` and prints for older ones — the fourth cutoff of the
  shape `STRICT_FROM`, `SURFACE_FROM` and `FLOOR_FROM` already carry, because
  a merged record has no honest repair: nobody can recover what ran a segment
  whose session is over. A row that is present and unreadable is refused at
  any age, the split the fix-surface rows already make.
  (#137)

<!-- specs/1788501054-a-check-reports-clean-while-something-is-missing -->
- **A ledger check scoped to one work item's fragment reported clean while the
  shared ledger went stale underneath it.** `evidence-check --ledger
  '<fragment>'` reads that fragment and nothing else, and the narrowing was
  adopted for a correct reason: it is what keeps `--reverify` off a row whose
  claim is false and belongs to somebody else. Carried into READING, it
  blinds. One work item's three review rounds and two fix passes all ran the
  scoped form and all reported ok; the unscoped read at the pull request found
  **fifteen drifted rows and one broken claim**, every one in a file the
  branch had touched, and one of them a claim the branch itself had made
  false.
  **`docs/review-handoff-protocol.md` (draft 1.2) gains a fourth handoff
  requirement**: a command with more than one form names the form, and says
  what the other one is for. Naming the form alone is not enough — a reader
  who does not know what the write's narrowing buys deletes it, and
  `--reverify` then re-stamps the false claim.
  `skills/code-review/SKILL.md` carries the two forms as a table, with the
  repair that looks obvious refused by name.
  **And the tool announces its own narrowing**, because guidance binds only a
  session that reads it and the session this trap was sprung on narrowed the
  command on its own initiative. A `--ledger` run now opens with the ledgers
  it did not read, named one per line, and how to read them. It prints before
  anything is opened — so a glob with a typo in it no longer reports `no
  evidence ledgers found`, which is the sentence a repository with no ledger
  at all gets — and a run that narrowed to exactly what the defaults would
  have opened says nothing. Nothing in a skipped ledger is read: the line is a
  report on what was skipped, not a second pass over it.
  **Two names for one file are one ledger**, matched by inode rather than by a
  spelling of the path, so a case variant on a case-insensitive filesystem, a
  hard link and a symlink all count as read. Comparing paths put a platform
  inside the answer — `os.path.normcase` folds case on Windows alone — and
  `--ledger SEAL/ledger.md` then read the ledger and listed it as unread.
  A file the run cannot identify falls back to its path rather than to a
  shared blank: an inode of 0 is not an identity (Python's own contract says
  so, and CPython's Windows `stat` leaves both fields 0 when it cannot open a
  file), and taken at face value it gave every such file ONE identity — so a
  ledger that was read swallowed every ledger that was not, and the run said
  nothing. Over-reporting is the declared direction here, and silence was its
  reverse. (#153)
- **A round record written after the fixes it commissioned looked exactly like
  one written before them.** `templates/sdd-round.md` says a record is written
  right after the round posts and nothing observed it; measured twice in one
  release, four minutes and two minutes late, and both times the reviewer's
  drafted replacement text lived only in a report and the next segment rebuilt
  it from scratch. A late record leaves no trace, because by then its verdict
  cells read `fixed at <sha>` — which is what a correct record looks like
  after its own update pass.
  **`chain_check.py` refuses a record whose ADDING commit descends from a
  commit its own verdicts name as the fix**, for work items begun on or after
  its `ORDER_FROM` — the fifth cutoff of the shape `STRICT_FROM`,
  `SURFACE_FROM`, `FLOOR_FROM`, `NEEDS_FROM` and `RUNNER_FROM` carry. It is
  the adding commit and never the last one: a correct record IS updated after
  its fixes land, so refusing on the last commit would fail every well-written
  record. Read on every record, like the four rows before it, because the last
  record is the one least likely to be late.
  **Three things it does not refuse**, each of which would otherwise fail an
  honest record: a verdict closing with `answered`, `withdrawn` or `not a
  defect`, which produces no code; a fix commit that is an ancestor of the
  record's own `Target SHA`, which the round already reviewed and therefore
  did not commission — that one is red on the second record of every well-run
  chain without it; and a record with no adding commit in `<baseline>..HEAD`,
  which arrived before the base and about which nothing is claimed.
  **Where a record was deleted and re-added, the LATER add is what counts.**
  That is the only shape producing more than one add, and it is the one that
  makes a late record look early: a stub committed on time, removed, and the
  real record written after the fixes. The version anybody reads was authored
  at the last add.
  **The reach is the commit a verdict cell carries, and that is a bound rather
  than a choice.** Measured across this repository's own records: 235 cells
  close with a fix word, 215 name a commit and 20 do not, and `| fixed |` is
  house style rather than malformed. So a record written entirely that way is
  invisible to the refusal however late it was committed.
  `templates/sdd-round.md` now asks for the commit beside the word, with the
  reason, rather than a sixth refusal being added for a spelling twenty
  existing cells already use — the reach grows as records land and nothing red
  is inherited.
  **The ordering rule made a record's fix surface start out empty, and
  `chain_check.py` now requires the second step.** Because the record is
  committed before its fixes exist, `Contract changes` and `New units` both
  begin at `none — the fixes are not yet written`, and until this landed
  nothing required anyone to come back and fill them — a record that never
  did read exactly like one whose fixes added nothing, and a verifying round
  opening it saw no finding surface at all. A row still saying *not yet
  written* on a record whose `Fixes checked by` names a later round is now
  refused: that round opened the fixes, so they exist, and the cell
  contradicts its own file two rows down. While `Fixes checked by` still says
  `nobody`, the value is the truth and nothing refuses it. Behind the same
  cutoff, so records of earlier work items print.
  This is the one place in the checker whose direction for a value it cannot
  read is **allow** rather than refuse. A rule about which English sentences
  mean *not yet* would be a rule about English, so the phrase is a constant
  the template prints and the checker matches at the START of the reason.
  **What escapes is wider than a rewording**, and three spellings carry the
  template's words unchanged: a dash outside the separator set, a doubled
  space inside the phrase, and any clause in front of it. Only the first is
  punctuation, so widening the separator set would close one of the three and
  leave the claim false about the other two — the limit is written down
  instead, with all three spelled out and a case running them.
  **And the arm keys on `Fixes checked by`**, so it reaches the session that
  filled that cell and stopped, never the one that filled nothing. `nobody`
  beside a pending row prints rather than fails, because that is the state the
  ordering rule requires; `no fixes to check` beside one prints too, and there
  the pair is not merely unrefused but wrong — a round that commissioned no
  fixes will never have any. That is the terminal record of every run, and
  whether it should be refused is a question for the repository owner.
  **The floor's count now stops at a record that wrote fixes, not only at
  one that reopened.** The walk read `Needs a fix`, which is the reviewer's
  answer to *what did I open*; the bound needs *were fixes written that owe a
  reader*, and the two come apart when the orchestrator fixes a 🟡 the
  reviewer said could be answered with grounds — because it ships, as a
  false count in a ledger fragment does. The row then reads `no` over fixes
  that exist, and the run had no terminal record any exit accepted: the
  reader after the `no` was a second uncounted record, and stopping at the
  `no` was refused both ways. Measured on this work item's own seventh
  round. The verdict column already carried the fact — it is what refuses
  `no fixes to check` beside `fixed` — and the walk reads it there now.
  ALLOW, one record wider in one sequence, and the cheaper mistake: the
  other way to satisfy the old walk was rewriting `fixed` to `answered`
  over fixes that exist. Three quiet rounds are still refused, because
  `answered` writes nothing.
  **What a rebase does to it is stated rather than left to be found.** The
  adding commit is read on the branch, and a rebase replays a branch's commits
  in order, so a passing record cannot be turned failing. What a rebase
  changes is the SHA a verdict cell names, which then resolves to nothing and
  makes no claim — so a rebase can turn a **failing** record passing, and that
  is the safe direction of the two.
  `docs/review-chain-spec.md` carries the subsection, and
  `skills/code-review/SKILL.md` carries the habit that clears it: commission
  the fix pass from the committed record rather than from the reviewer's
  report, which is a message in a session that ends. (#150)
- **Whether a record can be made to carry the artifact it says it verified is
  answered rather than assumed, and the answer is no.** A round record's
  executed-probes row read *"the round's proposed fixes … green, then red in
  every case"* and the record contained none of that code, so the implementer
  wrote its own replacement for the second time in one release. Writing the
  record first is necessary and not sufficient.
  `docs/review-chain-spec.md` names the three checks somebody would write and
  why each fails — a keyword match over free prose is an enumeration over an
  unbounded domain, requiring a fenced block on every record refuses the
  ordinary case, and the content cannot be in a diff at the moment the record
  is written. What remains is a declaration in `templates/sdd-round.md`: a
  probe row whose subject was a **proposed replacement** carries the
  replacement itself, in a fenced block, never a sentence about it. A command
  is reproducible from its own text; a patch is not. (#150)

## 0.7.0 — 2026-09-03

<!-- specs/1788445862-a-phase-hands-the-next-one-a-record -->
- **A build phase now leaves the same committed, per-segment record a review
  round already does, and both records now say what they were asked to do
  as well as what they found.** What a phase discovered used to reach the
  next phase only if the orchestrator retyped it into the next spawn prompt,
  and it went missing without a trace when it didn't: phase 4 of an earlier
  work item moved a rule out of `agents/smith.md` into an interim home, and
  phase 5 removed that interim home before the rule had actually reached
  anywhere else, deleting it from the repository with nothing recording that
  it had gone missing (#107, #121). New `templates/sdd-phase.md` mirrors
  `templates/sdd-round.md`'s shape for the build side: a field table
  carrying only `Phase` and `Commit` — a phase has no `Target SHA` to
  squash away and no `Pass` checkbox to answer — then `## What this phase
  was asked`, `## What this phase found`, and `## What this phase removes`
  (a table naming what left the tree and where it must land; `none` is a
  valid row, a blank table is not). `templates/sdd-plan.md`, `agents/smith.md`
  and `skills/implement/SKILL.md` are wired to it, so a spawned session
  writes `seal/specs/<work-item-id>/phases/phase-N.md` at each phase's close
  without having to be told twice.
  **Separately, neither a round record nor a phase record said what it was
  *asked* to do, only what it found.** #81's round 1 was the cheapest round
  measured — 7.6 minutes, 29 tool calls, one 🔴 and four 🟡 — because its
  spawn prompt named eight specific things to try to break, in order; that
  fact was recoverable only from a transcript. `templates/sdd-round.md`
  gains `## What this round was asked`, between the field table and the
  verdicts, and `skills/code-review/SKILL.md` instructs the orchestrator to
  copy the round-specific spawn content into it right after posting (#119).
  **Enforcement is a template blank plus a skill instruction, not a gate.**
  A `chain_check.py` refusal for a missing section was considered and set
  aside: it would need a red test, a stated failure direction, a prompt
  budget and a platform-honesty case for a mechanism that has shipped zero
  records yet to measure a cutoff against, and is revisitable once real
  phase records exist to learn from.
  **Two follow-on questions from #119 — naming which plugin version or
  commit ran a segment, and a `CONTRIBUTING.md` paragraph on the
  plugin-copy-in-force confusion — are explicitly out of scope here** and
  recorded as deferred, per the issue's own scoping, rather than silently
  dropped. (#121, #119)

<!-- specs/1788449488-measure-what-flow-finds -->
- **Measuring a smith or warden segment and logging what it found is now
  automatic, in every repository this plugin installs into, instead of a
  message a person had to remember to retype.** Issue #109: the instruction
  used to live only in one operator's own memory file, naming a fixed issue
  number that went stale twice. `skills/verify/SKILL.md` gains "Measure the
  segment, and feed the flow log" — after every segment, find this
  repository's open `flow-measurement`-labelled issue
  (`gh issue list --label flow-measurement --state open`) and post
  `session_cost.py`'s numbers to it; where no such issue is open (nearly
  every installed repository, today), the step is a no-op — nothing is
  measured, nothing is posted, nothing asks. A new
  `.github/scripts/roll_flow_measurement_issue.py`, wired into
  `close-issues-on-release.yml`, closes the current log and opens the next
  one — titled with the release's version bumped to the next minor — every
  time a release reaches `main`, so the log keeps growing without anyone
  opening the next issue by hand. This repository's own log (`#89`) is
  labelled as part of this change, so `0.8.0`'s issue opens on this
  repository's own next release without further action.
  **The rollover script retries once before treating "no issue open" as the
  invariant broken**, not on "more than one open": a search-index lag right
  after a label write can only ever undercount what is actually open, never
  overcount, so only a zero reading gets a second look. Found while building
  the label bootstrap in this same branch — `gh issue list` returned empty
  immediately after `gh issue edit --add-label`, while `gh issue view` in
  the same breath showed the label already applied.
  **Filed separately, out of this branch's scope: `agents/smith.md`'s
  mutation-testing instruction says to clear `tests/__pycache__` between
  mutations, and that is not the only cache a mutated module can leave
  behind** — a script loaded from `.github/scripts/` by path, the way this
  branch's own new tests load the file under test, caches its bytecode under
  `.github/scripts/__pycache__` instead, and a stale copy there survived one
  mutation's restore long enough to fail an unrelated later test run.
  `docs/flow.md`'s "While the flow runs" section — the instruction this work
  replaces — is deleted, and the two boxes it names as done (`#121 + #119`,
  `#109` itself) are ticked. (#109)

## 0.6.0 — 2026-09-03

<!-- specs/1788433011-every-spawn-prompt-is-retyped-from-memory -->
<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The rules every agent works under now live in one file the agent already
  has, instead of being retyped into each spawn prompt from memory.** Half of
  every prompt was identical to the last one, so a rule that failed to be
  recalled went missing with nothing recording that it had. It had already
  happened twice: one rule arrived at round 2 of a seven-round chain and
  round 1 ran without it, and another arrived at round 3 after two rounds had
  each rediscovered it. The new `agent-contract` skill is that file — sixteen
  numbered sections holding what is true of `smith`, `warden`, `scribe` and
  whichever agent is added next: how an exit code is read, what an agent must
  not run, what a spawn prompt may narrow and may not widen, which labels a
  report keeps apart, what reaching an agent in prose is worth, what an agent
  must not write, how a probe is named and how it drives git, that edits go
  through the `Edit` tool, how reads and runs are batched, what language the
  records are written in, where a `seal/…` path resolves, and the four method
  lessons the review chain paid for. **It arrives with nothing typed**: each
  agent's definition lists it under `skills:`, so it is injected at startup,
  before the agent's first tool call, and no agent resolves a path. A section
  number is never reused and never re-ordered, so a prompt can say *§3 is
  narrowed this round* and a round record still means the same thing when
  someone opens it six months later.
  **One thing you will see that is not an agent's behaviour.**
  `agent-contract` appears in the skill listing, because that listing is how
  the harness injects it. It is not a procedure to invoke: its frontmatter
  carries `user-invocable: false` and its description says it is injected
  into agents rather than run.
  **Each agent definition keeps only what is its own.** `agents/warden.md`
  keeps where it works — a `git clone --no-local` at the target SHA, with a
  `uv` venv because `pytest` is not installed for the system interpreter —
  its report format, the verifying round's re-derivation, and the records it
  must not write. `agents/smith.md` keeps the specification set, the design
  gate, the routing declaration, vertical slices, mutation-testing what it
  added, its hand-back and the 3+ Fix Rule. `agents/scribe.md` keeps
  resolving the original checkout, an absence carrying its search, and facts
  with coordinates and no verdicts. What each had been duplicating is gone
  from all three, and a definition that carries a section's own sentences
  again fails the suite rather than passing unnoticed.
  **`docs/review-handoff-protocol.md` stops being the interim home**, which
  it had named itself since it was written, and moves to draft 0.9. The
  section that carried those rules is a pointer at the contract and the
  definitions, and what stands in its place is the one rule that was always
  the document's own: a prompt carries what is specific to the round and
  nothing else.
  **The orchestrator is bound by the same contract**, and the two skills it
  reads — `implement` and `code-review` — say so. It never opens
  `agents/*.md`, so a contract reaching only the agents would have missed the
  party whose forgetting started this: the headline failure was an
  orchestrator breaking a rule it had put into every prompt it sent.
  `user-invocable: false` permits that load and does not oblige it, which is
  why the obligation is written where the orchestrator reads. (#107)

## 0.5.0 — 2026-09-03

<!-- specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in -->
- **A repository that must not carry the plugin's files in its tree can
  opt in: local mode keeps the whole root under the git directory.** The
  root lives at one of two places and the hooks read whichever exists, in
  order: `<repo>/seal/`, which is committed and is shared mode, then
  `seal/` under the common git directory (`git rev-parse --git-common-dir`),
  which is local mode — shared by every linked worktree of the clone, never
  a commit candidate, and needing no `.gitignore` line. There is no config
  key. Every hook that opens a file under the root resolves it the same
  way — the commit gate's declaration and the path its stop text tells you
  to write, the implementer notice, the review-history guard, the evidence
  advisor, the ledger migration and `evidence-check`'s defaults when the
  plugin's own copy runs (the copy `evidence-ci` vendors into `tools/`
  reads `<repo>/seal/` as before) — and the one sentence a session needs is
  in the `implement` skill and at the top of both agents: every `seal/…`
  path means `<repo>/seal/` where it exists and
  `$(git rev-parse --git-common-dir)/seal/` otherwise. What local mode
  gives up, stated in the README and in the root's own README: the
  pull-request checks read committed files, so CI cannot run them there,
  and a new machine or a re-clone starts empty. Switching is a move and a
  commit, documented under *Shared or local* in the README; export and
  import arrive with #81.
  **Nothing here writes to your tree without being asked. What arrives
  unasked, on its own line: first setup asks one more question, once —
  shared or local, shared first — in the batch the `implement` skill
  already asks, and a repository with `seal/` at either place is never
  asked.** Shared creates `<repo>/seal/` in the tree, which the routing
  commit carries, and writes the pull-request checks to
  `.github/workflows/hygiene.yml` from the new `templates/hygiene.yml`
  only when that file is absent — it clones the plugin at the release
  installed at setup and runs the chain check and the unverified-rows
  check. Local creates the root under the common git directory, installs
  nothing and touches nothing in the tree. The session-start migration is
  unchanged — a repository on the 0.3.x layout committed the plugin's files
  and is moved into `<repo>/seal/` — except that a repository whose root is
  already at either place is marked as moved, so a local-mode repository
  that later checks out a branch still carrying `.specseal/` is not moved
  into the tree it chose to keep clean.

<!-- specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill -->
- **A repository can say what language its pull requests are written in,
  and the skill reads that instead of requiring English of everyone.** The
  new `seal/config.md` holds one markdown table in the shape `parity.md`
  already uses, and its first row is `Pull request language`. Where that row
  names a language, `commit-pr-convention` writes the commit subject, the
  commit body, the pull request title and the pull request body in it — all
  four, because a squash makes them one text. **No file and no row both mean
  English**, so a repository that says nothing behaves exactly as it did
  before, and nothing is created for it: the file is written by a repository
  that wants a non-default, from the new `templates/config.md`. The root is
  resolved the two-place way, `<repo>/seal/` then
  `$(git rev-parse --git-common-dir)/seal/`, so local mode carries a config
  too.
  **Three things the row deliberately does not reach**, stated in the skill
  and again in the template, because the person writing the config reads the
  second and never the first: the prefix vocabulary is not translated
  (`feat:` stays `feat:` — it is scanned in a log and parsed by tooling);
  branch names stay ASCII, since a branch name is typed into a shell and
  pasted into a URL; and the response language, what the session says to
  you, remains a person's own setting, because two people in one repository
  can want different answers there and the same one here.
  The translated body is now named for **its own** language rather than the
  body's — `pr.<lang>.md`, so an English repository keeps `pr.ko.md` and a
  Korean one keeps `pr.en.md`. Nothing in this repository is renamed: the
  name was under-specified rather than wrong.
  Nothing in `hooks/` reads the file, and that is a decision rather than an
  omission: judging what language a commit message is in means being wrong
  about names, identifiers and quoted English, and a gate that guesses stops
  a correct commit. The mechanism is the skill's text, as it already is for
  the prefix vocabulary.

<!-- specs/1788395377-the-release-guard-globs-one-place -->
- **The release guard looked in one place for a file two work items kept in
  another (issue #96).** `fold_ledger.py` refuses a release while any work
  item still has an open row in `evidence-todo.md` — a fact a reviewer
  verified that never reached the ledger — and it finds those files with
  `seal/specs/*/evidence-todo.md`. Two work items kept theirs one directory
  deeper, under `rounds/`, so the guard was blind to two of five. Nothing
  was hidden: both carried a `drained` line. What was gone is the meaning of
  the guard's silence for those two, and the next open row written there
  would have passed a release without a word. The four misplaced files move
  to the level `docs/review-handoff-protocol.md` names, where every other
  work item already keeps them, and a test pins the layout rather than the
  glob — the glob is one line and the layout is written by hand once per
  work item, so the layout is the half that drifts. Found by asking what the
  guard's glob actually reaches, during another work item's review round.

  **And the rule is now said where a session meets it.** The reminder
  `hooks/review-history-guard.py` prints after a review is posted names the
  two todo files at the work item's own level, spelled from the same base as
  the round record beside them, and `docs/review-chain-spec.md` says the same.
  The `code-review` skill says why: `round-N` is the only member of the set
  that is plural and unbounded, so it is the only one that gets a directory.
  The protocol already said where the files go, and the sentence a session
  actually reads at the moment it creates them did not.

<!-- specs/1788398967-local-modes-records-never-leave-the-clone -->
- **Local mode's records can be carried to another machine, and taking one
  in never overwrites what is already there.** Two new commands,
  `seal export` and `seal import`, on the Bash tool's PATH while the plugin
  is enabled. Local mode keeps the ledger and the work-item records under the
  common git directory, so a new machine or a re-clone starts with nothing —
  that is the mode's whole trade-off, and it now reads as *take a copy*
  rather than *lose it*.
  `seal export` writes the root, and only the root, to
  `seal-<repo>-<date>.zip` beside the clone, with a manifest naming the
  remote URL and the HEAD SHA at export. **The smith mark, the worktree
  choices, the review and parity marks, every lease and the export's own
  state sit beside the root**, so none of them travels: the export walks the
  root and nothing else, which is why the design requires the root to be its
  own directory. A symbolic link inside it is skipped and named rather than
  followed — the one way out of that structure.
  The zip lands beside the clone rather than in it, because the ordinary
  place to run the command is the repository root and an untracked zip there
  is one `git add -A` from committing the records local mode exists to keep
  out of the tree. `--output` overrides it and says so when the path is
  inside the tree.
  **`seal import` never overwrites and never asks.** A file that is not there
  is added; one that is there with the same bytes is left alone, so
  re-importing the same zip writes nothing at all; one that is there with
  different bytes gets the incoming copy beside it as
  `<name>.incoming<ext>` — `ledger/<id>.incoming.md` next to
  `ledger/<id>.md` — and the collision is listed. Which of a pair is right is
  a reading rather than a merge, and no answer the command could pick would
  avoid sometimes throwing work away. It names `evidence-check .` as the next
  step instead of running it and reporting a pass nobody read.
  It refuses, writing nothing, for a zip from another repository (with
  `--allow-other-repo` where the two are one repository under two spellings —
  ssh at one machine and https at another compare equal), for a member that
  would land outside the root, and where both roots already exist.
  `--into shared` or `--into local` creates the named mode's root, which is
  the second way to switch modes.
  **In shared mode `seal export` writes no zip.** The records are committed,
  so every clone and CI already have them, and a zip would be a second copy
  that nothing keeps current. It prints the path and the `mv` that switches
  to local mode, and exits 1 — so `seal export && cp seal-*.zip …` does not
  copy nothing and report success.
  Once per release, `seal export --check` prints one line — how many work
  items changed since the last export — and uploads nothing anywhere. Where
  the copy goes is the user's business. It counts work items only, so a
  change confined to `follow-up.md` reports 0; the line's wording is fixed by
  the design, and widening it is recorded as an open question rather than
  taken silently.
- **One claim was corrected by measuring it, and the correction is why the
  import is stricter than it was designed to be.** This work was planned
  around "`extractall` is the classic path-traversal sink". On the CPython
  the plugin ships on that is false: it already strips `..` and a leading `/`
  from a member's name, and writes a symbolic-link entry as an ordinary file.
  What actually disqualifies it is that it **overwrites**, and that it writes
  through a symbolic link in the destination. That second one is a real
  escape, the import's own writer had it too, and it is now refused before
  anything is written. The member-name validation was kept regardless: a
  defence that holds only while a standard-library sanitiser keeps its
  current shape is not one this plugin can claim.
- **Review then measured the same claim one level down and found it still too
  narrow.** The check that closed the escape walked every directory above a
  member and stopped short of the member itself, so a symbolic link named for
  the record was never looked at. A broken one reads as absent, so the file
  was treated as new and written straight through the link, outside the root,
  at exit 0 with nothing printed. The check now covers the leaf, and three
  documents that called the directory case the only way out say what was
  measured instead.
- **Review then found the same escape one name over, and it is closed at two
  levels.** A collision does not write to the member's name — it falls back to
  `<name>.incoming<ext>`, and the check that refuses links had never seen the
  fallback names. A broken link there read as absent, so the copy was written
  straight through it, outside the root, at exit 0 and printed as an ordinary
  collision. The sender of the zip chooses whether the collision happens at
  all, by sending bytes that differ. Every candidate name is now read as a
  link rather than as a file, and the write itself opens with a flag the
  kernel refuses to follow a link through — so a name that becomes a link
  after it was checked is refused too.
- **An import now refuses a zip that declares more than a root of records
  holds, and a zip whose data does not match its own checksums.** Each member is read whole, and the zip arrives from another
  machine, so its declared sizes are the sender's choice: a 408 KB file
  declaring 400 MB in one member wrote 419 MB and took as much memory, in
  0.2 s. A member is capped at 32 MB and an archive at 512 MB, and the total
  is summed before the manifest is parsed — that read is unbounded too, so a
  400 MB `manifest.json` used to take 400 MB of memory on its way to being
  rejected. A bad checksum was the other way in: a zip whose central directory
  is well formed and whose data is corrupt used to write the records before
  the corrupt one and then die on a traceback, which is a partial import from
  a zip that chose to be one.
- **Two smaller corrections.** A clone holding both roots is now refused
  however the import is asked, including with no `--into` flag — the case the
  specification and both READMEs describe was the one spelling that still
  wrote. And a repository with no commit yet records an empty SHA in the
  manifest rather than the four letters `HEAD`, which is what `git rev-parse`
  prints on its way to exiting 128.
- **The third round opened the half the first two never had, and found the
  same shape there.** Both earlier rounds read the import. `seal export`
  writes its zip to a temporary name first, so a failed write leaves no half
  archive — and that name is `seal-<repo>-<date>.zip.partial`, beside the
  clone, which anyone can predict. A symbolic link planted there took the
  manifest and every record outside the clone at exit 0, while the command
  printed `wrote <path>` for a path that was the link. The temporary name is
  now opened with the same flag the import writes with, and the zip's own name
  is read as a link rather than as a file — a check whose docstring claimed
  the import shared it, which is why the import's fix never visited it.
- **A zip can no longer end an import in a traceback.** Three ways in: a
  member the build cannot decompress, an encrypted member, and a corrupt
  manifest — the last one because the manifest was read before the data was
  checked. The checks now run in one order, largest question first: how many
  members, how many bytes, what the names are, whether the data reads, and
  only then what the manifest says. A member count is bounded too, because
  both size bounds count bytes and a zip of 300,000 empty members wrote
  300,002 files into the root at exit 0.
- **And a name that has to be a directory for the zip and is a file is
  refused before anything is written.** `os.makedirs` raised on it mid-write,
  leaving the records before it on disk. The sender corrupts nothing to reach
  it — two members named that way is enough — and the root's own contents
  raise it from the other side.
- **The fourth round found no way out of the root, and one thing the fix
  before it had broken.** Refusing to write through something at the export's
  temporary name also removed it — a link, a file somebody left, or a
  concurrent export's archive still being written, which loses that export the
  zip it was about to rename. The cleanup that removes a half-written archive
  is for a name this command created, and it now runs only for one.
- **A zip can no longer end an import in a traceback for a reason the
  filesystem gave, either.** The check for a name the zip needs as a directory
  asked whether it was a file, and a named pipe is not a file — it walked past
  and met the same crash. And nothing at all guarded the write loop: a
  directory in the root that cannot be written into, or a full disk, left a
  partial copy and a traceback. Both stop with a line of their own now, and
  the second says what is true — this command overwrites nothing, so running
  it again finishes the copy.
- **A zip from a later version of this format is told so.** The name checks
  ran first, and a later format is exactly what moves the names they read, so
  a zip declaring format 2 was answered as a malformed zip rather than as a
  build too old. The format field exists for no other day.
- **Two messages stopped sending people to the wrong place.** A clash inside
  the zip told a person to rename a file that was not on their machine, and
  the Korean README described that clash as always coming from their own clone.
- **The last round found no way out and no crash the change had caused, and
  one the change had walked past.** A manifest is another machine's file, and
  this build checked that it was an object and that its version number was one
  it reads — every other field was trusted to be the kind of thing it looked
  like. A manifest naming a commit but no time raised at the closing line,
  *after* every record was written: the person saw a Python traceback and exit
  1 for a copy that had succeeded, and exit 1 reads as nothing happened. Those
  fields are read as text or as absent now.
- **And a name that means the manifest to one check meant a record to
  another.** `manifest.json/` was exempt from the name rules as the manifest
  and outside the size bound as not-the-manifest, so it could declare any size
  at all. Both spellings answer to both checks now.
- **Three sentences and a table row that described something else.** Both
  READMEs said the import writes nothing when it stops, and the round before
  had added a stop that writes. The refusal for a zip from a later version of
  this format was in no document a person is pointed at. And the ledger row
  saying which bounds are read before the manifest was wrong a second time, in
  the same place.

<!-- specs/1788411058-the-mode-is-two-shell-lines-in-a-readme -->
- **Switching between shared and local mode is a command now, and a
  repository can say which mode it wants before the folder moves.** It was
  two shell lines in `README.md`'s *Shared or local* section — correct, and
  unfindable — and a repository arriving from the 0.3.x layout landed in
  shared without ever being asked, which put the people most likely to want
  local mode in the place least likely to tell them it was still available.
  `seal mode` prints where the root is, what `seal/config.md`'s new `Mode`
  row says it should be, and whether the two agree. `seal mode local` and
  `seal mode shared` switch; `seal mode --apply` switches to what an edited
  row says; `seal mode --check` writes nothing and exits non-zero on a
  disagreement, which the pull-request checks now run so the row cannot
  quietly become a document that lies.
  **The row is what the repository wants and the folder's location is what
  it has.** Nothing at runtime reads the row — every hook still resolves the
  root by looking for `<repo>/seal/` and then `<git-common-dir>/seal/` — so a
  gate can never be sent looking in a place with no folder. It has no default
  either: an absent row is filled in from where the folder actually is, which
  is an observation rather than an assumption, and is the state of every
  repository that has a `config.md` today.
  **Beyond the two shell lines it does what a `mv` cannot.** It refuses when
  the other mode's root already exists, refuses when the index carries a
  change under `seal/` or the workflow path, carries
  `.github/workflows/hygiene.yml` in and out, and writes the row so the file
  and the folder agree afterwards. It stages; you commit.
  **Carrying the workflow file is the part that is easy to mistake for
  tidiness.** Measured in a repository with no `seal/`: the two checks it
  runs fail in opposite directions — one goes red on every pull request
  forever for a repository that did the right thing, and the other goes green
  having examined nothing. Left behind, a switch to local turns the build red at the first of them.
  **The two directions do not cost the same, and the command says so before
  it acts.** Going to local takes the records out of the tree and every other
  clone loses them at the next pull, which is what `seal export` and `seal
  import` are for. Going to shared is the one to be sure about: the commit,
  not the move, is the point of no return, and until it lands
  `git reset -- :/seal :/.github/workflows/hygiene.yml` and then `seal mode
  local` walk the whole thing back.
  The rename runs first and every step after it is idempotent, so a stopped
  run — or a person who already ran the README's `mv` by hand — is finished
  by running the command again rather than refused. (#104)

<!-- specs/1788420760-a-language-row-that-governs-four-things -->
<!-- seal/specs/1788420760-a-language-row-that-governs-four-things/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A repository can say what language this plugin writes in, and it is two
  answers rather than one.** The row that shipped as `Pull request language`
  governed four things — the commit subject and body, the pull request title
  and body — and everything else this plugin wrote stayed English whatever it
  said. So a team working in Korean got Korean pull requests and English
  specifications, which is a pull-request setting wearing a language
  setting's name. It is now `Commit and pull request language`, which is what
  it always governed, and it takes the review report posted to a pull request
  with it. A second row, `Record language`, governs the prose in the
  work-item records: the specification, the plan, the memo, the questions,
  the changelog fragment, the round records' cells, and a ledger row's claim
  and grounds.
  **The two are independent.** Setting one does not carry the other, because
  an absent row's default is what every repository had before that row
  existed, and a row inheriting another's value is not that. Three
  combinations, which are the three people want: everything English, the
  commits and pull requests in the team's language with the documents in
  English, and both.
  **Prose follows the rows and structure does not.** What stays English in
  every repository, whatever either row says: the commit prefix vocabulary,
  branch names, all code, and every string a checker reads literally — a
  round record's field names, its verdict vocabulary and its `Pass` checkbox,
  the `<!-- -->` markers, a `drained` line, and a ledger anchor's
  `path#unit@hash`. A translated field name is not a translation; it is a
  checker that stops reading. (#106)

<!-- specs/1788420761-the-settings-live-in-a-file-nobody-opens -->
<!-- seal/specs/1788420761-the-settings-live-in-a-file-nobody-opens/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`/specseal:config` shows what this repository decided for itself, and
  changes any of it.** Three rows live in `seal/config.md` — the language the
  commits and pull requests are written in, the language the records are
  written in, and which of the two places the root lives at — and until now
  the only way to see any of them was to open a file nobody has a reason to
  open. First setup asks its questions once and never again; this is how to
  ask them later.
  It shows rows that are absent as well as present, with the default and
  where it comes from, because a row a repository never set is the most
  likely one somebody wants to change. For the mode it runs `seal mode` and
  reports what that says — the folder, the row, and whether they agree —
  rather than reading the row itself, since a second reader is a second
  answer.
  **A change is routed to whatever owns that row.** A language row is only a
  row and is edited in place. The mode row moves a directory, stages a
  commit, and installs or removes the pull-request workflow, so the skill
  runs `seal mode` and reports that list rather than saying *done*. Before
  switching to shared it says what cannot be undone: the commit, not the
  move, is the point of no return. (#105)

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
  the once-per-repository marker is `~/.claude/specseal/root-migrated`. To move by hand instead, run the sequence in the README's *Coming up from
  0.3.x*: it creates `seal/specs`, then does one `git mv` per entry of
  `.specseal/` and per work item, removes the two emptied directories, and
  ends with `evidence-check --reverify .`, which re-points each row citing a
  moved file. Every gate, checker and release
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
