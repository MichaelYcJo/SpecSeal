---
name: implement
description: |
  Spec-driven implementation methodology: document layout (docs/ + seal/), policy-first
  judgment, evidence feedback, and review incorporation.
  Use when: implementing a feature, starting a ticket — including deciding how to
  start one, incorporating review feedback, or when a repo needs its document
  layout bootstrapped.
  NOT for: reviewing someone else's code (use `code-review`), or explaining how
  something already works. The line is whether the question names a work item to
  be built: "how should I approach TICKET-4" is this skill, "how does the review
  chain work" is not.
---

# implement — spec-driven implementation

Methodology for implementing against written specs, leaving durable evidence,
and closing the loop with review. Loaded by the `smith` agent; usable directly.

**`skills/agent-contract/SKILL.md` binds this session too, and only if you
load it.** A session driving the work directly reads this skill and never
`agents/*.md`, so the contract every agent it spawns receives at startup
reaches it by being opened rather than by arriving — `user-invocable: false`
permits the load and does not oblige it. #107's headline failure is an
orchestrator breaking a rule it had put into every prompt it sent.

## The orchestrator's half is a file of its own

**If you are orchestrating a work item rather than building it, read
`skills/implement/orchestration.md` before the first edit.** The three
sections this file used to carry for the session that spawns agents are
there, verbatim and under an `Orchestrator:` prefix: how the `seal/` root is
created the first time a repository opts in, how parity mode is set up, and
how the routing question — three axes, one question, one declaration — is
asked and written into `routing.md` before anything is built.

**An implementer never opens it**, and that is why it is a path rather than
an entry in a `skills:` list. Asking a person and writing `routing.md` are
acts `agents/smith.md` leaves to the session that spawned it, so 14,949
characters of procedure reached every `smith` spawn with no act of its own to
apply them to (#292). `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`
is what keeps a marked section out of a preloaded file.

Everything else in this file is the implementer's, and the orchestrator reads
it too: a work item is judged against the same precedence and the same file
set as the code it builds.

## The language the records are written in

**Read `Record language` in `config.md` before writing any of the documents
below**, the same way `commit-pr-convention` reads its own row before a commit
or a pull request. The root is resolved the way every path in this skill is.

```markdown
| Item | Value |
|---|---|
| Record language | Korean |
```

It governs the **prose** in `spec.md`, `plan.md`, `overview.md`,
`questions.md`, `changelog.md`, the cell contents of `rounds/round-N.md` and
`phases/phase-N.md` and the text beneath their tables, and the claim and
grounds of a ledger row.

**Every way of not naming one lands on English** — no file, no such row, an
empty value, a file that cannot be read. A config nobody can read must not
stop the work.

**It is independent of `Commit and pull request language`.** Setting one does
not carry the other, and the two surfaces have different audiences: a pull
request is read by whoever opens it, and a record is read by whoever comes
back to the decision six months later.

**What stays English whatever it says**, because these are read literally
rather than by a person: every field name, section heading and vocabulary
word the checkers match, listed in `templates/config.md` under *What no row
governs* — that list is derived from the checkers' own constants, so it
cannot drift from them; `<!-- specs/<work-item-id> -->` and the other
markers; a `drained` line and a ✅; a ledger anchor's `path#unit@hash`; and
all code — identifiers, comments, docstrings, file names, test function
names. A translated field name is not a translation, it is a checker that
stops reading.

## Document layout — two roots, three lifetimes

Every artifact this skill produces goes to one of two roots, and the second is
laid out by **lifetime**, not by who wrote it:

| Root | Lifetime | Test | Authority |
|---|---|---|---|
| `docs/` | Permanent, cumulative | Must still be true in 6 months | **Norms, ratified by humans.** Read when the repository has them; **never created here** — a project's documentation convention is its own |
| `seal/specs/<work-item-id>/` | One work item | Its role ends when this work ships (SDD, overview, round records) | The contract this work executes against. A human approves `plan.md`, which is why this is a repository document and not tool state |
| `seal/`, everything above `specs/` | Permanent | Everything this plugin maintains | Written and read by machines: the ledger, the migration config, the follow-up list |

The axis is lifetime and authority, **not audience** — humans and AI read all
three. (Labeling policies "for humans" would push sessions away from reading
them, and policy outranks everything else when a repository has it.)

`seal/` lives at one of two places, and its presence at either is what tells
the gates this repository runs the workflow. **Every `seal/…` path in this
plugin's skills and agents means `<repo>/seal/` where that directory exists,
and `$(git rev-parse --git-common-dir)/seal/` otherwise.** The first is
shared mode: committed, because gitignored files do not follow worktrees or
other machines. The second is local mode: under the common git directory, so
every linked worktree of the clone shares it, and never a commit candidate.
A repository with both is shared, and nothing else — no config key — is
read. What sits directly under it is permanent; what sits under
`seal/specs/` lives as long as its work item:

```
seal/
├── README.md         the export rules, for sessions that never load this skill
├── ledger.md         spec clause ↔ code coordinates, as they stood before
│                     work items wrote fragments
├── ledger/
│   └── <work-item-id>.md   one work item's rows, no header — folded into
│                           ledger.md by the release that ships the work item
├── parity.md         migration config, only when declared
├── follow-up.md      schedulable items in a repository with no tracker
└── specs/<work-item-id>/
    ├── routing.md    the routing answer, written before the first edit
    ├── spec.md · plan.md · questions.md · overview.md
    ├── rounds/
    │   └── round-N.md    one review round — closed at merge and kept
    └── tests-todo.md · evidence-todo.md
```

The review round records live beside the work item they are about, with the
routing declaration and the rest of the SDD set. They used to sit under the
plugin's own directory, keyed by a pull request number that does not exist
while the rounds that would fill it are running.
No correct session could create that directory, and none ever did
(`docs/review-handoff-protocol.md` carries the whole reasoning). A work
item's directory exists from its first commit, because routing is written
into it before the first edit.

**Nothing else follows them, because there is nothing else.** A round record
carries the SHA it reviewed, so it never asserts a present state and can live
beside the contract. Progress does the same thing one file up, in `plan.md`'s
Status column, where a closed phase carries the commit that closed it — the
same past-state trick, for the same reason.

**Judgment precedence is policy > SDD > code where policy exists, and
SDD > code where it does not.** Most repositories are the second kind. Do not
manufacture the first by writing policy documents nobody asked for: the SDD set
is the root of judgment, and a policy document is a thing a human decides to
keep.

## Procedure

### 1. Read the spec before the code

Judgment precedence: **policy (`docs/`) > SDD (`seal/specs/`) > the ticket >
existing code** — and, where the repository declares a migration config, the
original sits between the ticket and the existing code, because policy being
silent is what makes the original decide (see `legacy-parity`).

A spec that contradicts policy gets fixed, not followed. **A ticket is a
request, not an authority**: it says what someone wants, which is why it ranks
above the code as it happens to be, and why it ranks below the documents that
were ratified. A ticket asking for something policy forbids is a question for a
person, not an instruction — write it into `questions.md` rather than building
it or dropping it.

- Policy documents delegate to each other. "This document doesn't answer it"
  is not a policy gap until sibling documents in the same domain are checked.
- Read `seal/follow-up.md` before starting. It holds items
  whose answer exists but which waited on prerequisite work — **this work may
  be that prerequisite.** If so, include the item in this change and delete its
  row; what remains in that file is the definition of remaining scope.
- Verify clause numbers a ticket cites. Tickets are written before (or drift
  from) the documents they cite; a missing clause means writing it is part of
  this work, with a freshly allocated number.
- A spawn prompt's facts arrive under `docs/review-handoff-protocol.md`'s
  handoff before round 1: coordinates rather than prose, each fact labelled
  executed, read, or unverified. A fact with no coordinate and no label is an
  assertion nobody has opened — open it before building on it, however
  confident the prompt that carried it. An aggregate (a count, a total) is
  not a coordinate: the number can be checked while the claim it stands for
  cannot, and one such fact reached five documents before a review round
  found it false.

**Collect what needs a person before the first edit, and ask it in one batch.**
Read the spec chain looking for the questions as well as the answers, and put
every one of them in front of the user at the start: a decision only they can
make, an approval, a credential, a permission the session does not have.

The cost of a question is not its difficulty, it is when it arrives. Asked
before the work starts, it costs a reply. Asked at minute thirty, it stops
everything until someone is at the keyboard — and the longer a session is
meant to run unattended, the more of it a late question wastes. Asking one at
a time is the same failure spread out: three interruptions cost three waits.

Two things sharpen the list:

- **A question you can answer is not a question.** Read the documents and the
  code first. What survives that is the batch.
- **Assume, in writing, whatever would not change what you build.** State the
  assumption in `questions.md` and continue. Only where different answers mean
  different code does the work actually have to wait.

Something a session cannot do for itself belongs on the same list — widening
its own permissions, for one, which the harness blocks by design. Better
found in the first minute than at the commit.

**A question in this batch names its answers, and every answer continues.**
"Should I release this?" and "should the warden review it?" both have a `no`
that leads nowhere — the session that answers it is holding finished work with
no destination, which is a gate wearing the shape of a question. A yes/no is
the tell. Ask which of two named paths instead, and say what each one does.

**A waiver is one command's, and it is the implementer's.** `[no-review]`
still works and is unchanged: it waives **one command**, where a
`routing.md` declaration routes **a work item** — the file the session
that spawned you wrote before the first edit
(`skills/implement/orchestration.md`), which keeps the review arm of the
commit gate silent for every commit of a declared branch, for either review
answer. Coupling them would ask for the same answer twice and stop a
session for not repeating itself. Where no declaration is in force — no
file, a branch it does not name, or a file that will not parse — the gate
behaves exactly as it did before, which is to ask. For a change that
belongs to no work item at all, the token is still the way past, and it
goes in FRONT of the command, quotes included:
`: '[no-review]'; git commit …` (and `[no-parity]` too where a migration
config is declared). After `git commit` a bare word is a pathspec and git
rejects the whole command.

**Once the batch is answered, the session runs to the pull request.** What
surfaces after it is written down rather than raised: a decision only a person
can make goes to `questions.md`, a finding you neither fixed nor answered to
`seal/follow-up.md` with an answerer named — a deferral to nobody is how
"someone will look at it" becomes nobody did (`verify` §The answerer has to
exist) — and what was deliberately left goes to the overview's Not done
section. Each is named in the PR body, because a leftover nobody can find was
not handed over.

The test for whether something is a question or a row: would a different
answer change what you build *now*? If it would not, raising it spends a
person's attention on something that was never blocking, and the session that
waits for the reply spends more.

### 2. Implement, and feed evidence back where you verified it

When you open code or run something to settle a judgment, record the outcome on
the row it belongs to and put **the date you read it** in the Checked column.
Only rows in this work's scope — full-ledger audits verify what is already
correct and return nothing.

A coordinate is `path#major@hash` — the enclosing unit, a function or class for
code and a heading path for a document — with an optional `>minor` narrowing it
to the statement a claim is about. It carries no line number and no commit, so
nothing in it goes stale for a reason unrelated to the claim. Cite the unit and
leave the minor level off unless whole-unit hashing has been measured to drift
rows on unrelated edits. Re-verifying is re-reading and running
`evidence-check --reverify`.

**Rows a work item adds go in its own fragment**, `seal/ledger/<work-item-id>.md`,
not appended to `seal/ledger.md`. Two branches cannot collide there, because
no two work items share an id, and the checker reads the whole
`seal/ledger/*.md` glob. The fragment lives until the release that ships
the work item, whose preparation step folds it into `seal/ledger.md` and
removes it; a row is a content anchor, so the move changes nothing the
checker measures.

**Draft as you go, write in one pass.** The recording is cheap and the round
trip is not: one session made twenty-six separate edits to its ledger and
policy documents, seventy-eight seconds of command time that cost about three
and a half minutes of waiting. Keep the rows as you settle them and write
them to the file when the work item closes, or at a phase boundary — not one
edit per row.

This record is the input for the reviewer and the next ticket. Unrecorded
verification gets redone by every session that follows — the single largest
avoidable cost in multi-session work.

**Commit at the smallest step that stands on its own.** What an intermediate
commit costs is a property of the repository rather than a fact about
committing, and two things can drive that cost to nothing:

- feature branches **squash** into their base, so every commit the branch
  wrote stops existing at the merge and none is left for anyone to read;
- a `routing.md` declaration is in force, which silences the review arm of the
  commit gate for either answer (`skills/implement/orchestration.md`).

Read both off the repository before leaning on them. One that merges without
squashing keeps every commit in its history, and one with no declaration meets
the review question at each commit. **A declaration does not silence the
parity arm**: the two opt-ins are independent, so where a migration config is
declared a code-touching commit still meets that one. The wake/quiet table in
`skills/implement/orchestration.md` says what wakes and quiets each arm, and
it is the only place that says it.

What committing *buys* is a separate matter, and that one holds everywhere. A
review round records the commit it read, so work still sitting in the working
tree is not visible to the reviewer at all — there is no spelling for *and
also the four files that were not committed yet*.

*Commit as you go* alone does not settle the cadence. One session was told
exactly that and did it, eight commits across two rounds, and still had five
modified files in the working tree when an unrelated command reached the
worktree guard. That window has a price wherever this plugin is installed: the
guard asks whether the changes should ride along to the other branch, and
*commit them here first* — the answer that is usually right — is not one of
the two buttons. Nothing had said how early early is.

The two cadences in this section govern different acts. *Draft as you go*
batches the **write** into the ledger file, so rows land in one edit at a
phase boundary instead of one edit each; this rule is about the **commit**. A
phase boundary is where they meet: write the rows you have been keeping, and
let that write ride the commit that closes the phase. Pairing each row with
the one slice it describes is not on offer, because those slices are already
several commits behind and buying the pairing costs one write per row, which
the rule above refuses. What must not happen is a run of commits reaching the
reviewer with the ledger still empty, because by the paragraph above the
reviewer sees only what was committed.

**Commit freely; a ledger row names no commit for a merge to orphan.** This
used to be the one place the cadence had to be steered around, and it is not a
place any more: a row records an anchor and a hash of what that anchor holds,
so there is no commit in it that a squash or a rebase could invalidate.

**An edit must be able to fail.** Prefer the `Edit` tool: a pattern that does
not match is an error you see immediately. When the environment routes edits
through the shell instead — `sed -i`, a heredoc, a short script — a
substitution whose pattern misses does nothing, says nothing, and exits zero.
The miss surfaces at the next check, and the cost is another edit and another
run of whatever you had already run. Measured on one work item here: no `Edit`
calls, 128 shell edits across 47 files, 2.7 edits per file, and a column
insertion that silently did not happen because the indentation did not match.

So assert the landing. Every shell substitution states what it expected to
match and fails loudly when it did not:

```python
assert old in text, f"pattern did not match: {old[:60]}"
```

This is `verify`'s second condition — *a check that cannot fail is a
counterfeit seal* — applied one step earlier. An edit that cannot fail is an
unverified edit, and reporting it as made is the same claim as reporting a
`read` as passing.

### 3. The SDD file set

**When a work item is required** — the same threshold the Design Gate uses,
because they are the same judgment. Drawing no line is how the set quietly
stops being written; this repo's own history has two features that shipped
without one and nothing noticed.

| Work | What to write |
|---|---|
| It **alters observable behaviour** — a gate's verdict, a hook's output, a skill's or agent's instructions, a public API, text a person reads and acts on. Or it changes a value someone waits on or is limited by — a timeout, a retry count, a rate, a size cap — and NAMING that value is what puts it on this rung | `spec.md` and `plan.md` **before** implementing — approval of `plan.md` IS the gate — then the closing memo |
| It alters none of that and is more than one line — a refactor, a performance pass, a formatting sweep, a test that pins what already holds. These four are DEFAULTS, not a closed list: a performance pass that moves a timeout a person waits on belongs on the rung above, and the value's name is what moves it | the closing memo. A one-line scope confirmation replaces the plan |
| A typo, a config value, a one-line fix | nothing |

**Behaviour, not file count, and the difference runs both ways.** The top rung
used to read *6+ files, a new module, or an architectural choice*, and two of
those three conditions measured size.

- **One file, and it qualifies.** A change to an agent's persona is two files
  of wording, and wording is what a session reads and acts on. Measured here:
  `warden-persona-accuracy` opened as exactly that, wrote no `spec.md`, and
  finished at eight files with five of them arriving in review rounds 2 and 3.
  Under the behaviour test it needed a plan at file one.
- **Many files, and it does not.** Copying test repositories instead of
  running `git init` for each touched more files than that and altered nothing
  anyone can observe — no verdict, no output, no instruction. The suite runs
  faster and says the same things.

The count also never said **when** it was taken (issue #35). The gate it
guards — plan approval — exists only before the first edit, so the number had
to be the estimate; nothing said so, and nothing said what to do when the
estimate was passed. Seven branches were measured for that issue and two
missed the rung by growing past it after the gate had already gone by. A test
with no number has no moment at which the number is taken, so the question
stops being answerable and stops needing an answer.

What it costs: *does this alter observable behaviour* is a judgment where
*six files* was a count, and two people can disagree about a borderline case.
That is the trade — a judgment that is about the right thing beats a
measurement of the wrong one, and the list in the rung is what keeps the
judgment from being free-form. The way out of a default is to NAME the value a
person waits on or is limited by, which a reader can open and check. *I judged
it observable* is not something anyone can check, and it is not a way out.

`questions.md` is not on that ladder: it starts with the batch collected
before the first edit (step 1) and gains a row whenever a decision only a
human can make appears later, at any size. A late one still gets written — the
batch is what keeps it from being the only way they arrive.

A work item's directory is `seal/specs/<unix-epoch-seconds>-<slug>/` (e.g.
`seal/specs/1784780439-center-list-sort/`), bootstrapped from `templates/`. The
timestamp prefix keeps directories in creation order and collision-free
without a registry — take it from `date +%s` when creating the directory.

| File | Starts from | Holds | When |
|---|---|---|---|
| `spec.md` | `templates/sdd-spec.md` | WHAT — scope, mandatory user scenarios & acceptance, grounding clauses | before implementing |
| `plan.md` | `templates/sdd-plan.md` | HOW — phases as vertical slices, alternatives with failure scenarios; this is the Design Gate's artifact | before implementing (gated work) |
| `questions.md` | `templates/sdd-questions.md` | decisions only a human can make — extracted so nothing ships on a silent assumption | one batch before the first edit, then as they arise |
| `overview.md` | `templates/sdd-overview.md` | the closing memo — one line of purpose, then what the diff cannot show (below) | opened at the first divergence, unverified item, or fed-back clause; closed when implementation ends |
| `phases/phase-N.md` | `templates/sdd-phase.md` | what this phase was asked, what building it found, what it removed from the tree — never the commit or the one-line delivery description `plan.md`'s Status/Delivers cells already own | written when the phase closes |

The middle column is not decoration. A template that no shipped document
names is a template a session cannot find: it reads *bootstrapped from
`templates/`*, cannot tell which file that means, and writes one from
scratch. Two of the original four — before `phases/phase-N.md` joined the
table — were in exactly that state.

**What goes into `phases/phase-N.md`'s `## What this phase was asked`
section is the phase-specific content of the spawn or task that started
it** — never the boilerplate the contract, this skill, and `agents/smith.md`
already carry, which every phase gets told by definition and none of them
need repeated in their own record. Copy it in when the phase closes: what
the spawn prompt or task description said this phase, specifically, had to
build.

**`plan.md`'s Phases table is the task list, and there is no other.** Each
phase carries a **Verified by** column, so it cannot be called done the way a
checkbox can be ticked, and a **Status** column that is empty or holds the
commit that closed the phase.

The objection that sent task lists elsewhere is real and it is about form
rather than location: mutable progress inside the contract asserts a state
that is not true, which is the failure this plugin's ledger exists to prevent.
A commit is not mutable progress. It asserts a **past** state that someone can
open — the same trick that lets a round record sit beside the contract — so a
tick and the word `done` are refused where a hash is not. Both of those can be
typed without anything having happened.

What this gives up, stated rather than left to be found: the finer structure
`feature-planner` produces — per-task dependencies, what can run in parallel —
does not fit in a phase row and is not kept anywhere between sessions. Phases
are already ordered and already vertical slices, so what is lost is the
parallel marker, and the judgment is that a list nobody ever wrote had no
structure to lose. It had a home under the plugin's own root for three
releases, no code ever read it, and it was never once created.

### 4. The closing memo — only what the diff cannot show

`seal/specs/<work-item>/overview.md` is not a summary of the work. `git diff --stat`
already holds the file list and the diff holds the detail; re-deriving them at
the end costs a re-read of your own change and lands further from the truth
than the command would.

Four things go in it, and after the session closes three of them are nowhere
else. Write each **when it happens** — a call made at minute ten is invisible
by minute ninety, and reconstruction is the expensive way to get a worse
answer.

1. Why this work exists and what the result changes — **one line**, not a walk
   through the diff. Where the change alters nothing observable no `spec.md`
is written, so this is
   the only place the purpose stays in the repository.
2. Where spec and implementation diverged — both sides quoted, which side won,
   and the grounds, at the moment you decide it. "The document probably said
   so" is not grounds; quote it.
3. What was not verified — with **who has to answer it**, at the moment you
   decide not to run something.
4. What was fed back into the spec — clauses this work added, marked as
   *inferred during implementation* so planners know they may overturn them.

A memo whose last three sections are empty is correct and four lines long.

**`## Not verified` is read by a machine, so it has one shape** — a
`| Item | Who must answer |` table, or the line `none — <why>`. Any other
spelling of the heading or the header row fails the check rather than reporting
zero, because zero reads as "everything has been closed".

An item is closed by marking it, never by deleting it:

```
| ✅ how the gates render in a TUI | seen on screen, session of 2026-08-25 |
```

An unmarked row counts open, so the silent direction is always "still open",
and a bare check mark with nothing after it is refused the same way a ticked
checkbox is. Deleting the row — or the whole file — fails the next pull
request (`unverified-check --baseline origin/<base>`), which is what keeps "I
verified it" and "I tidied it away" from being the same edit.

What that check reads is the **number** of rows, not their text. So the second
cell saying what closed the item is a convention it cannot enforce: swapping
one row for another keeps the count and passes. Leaving the original answerer
in place beside a check mark is how a closing goes out unproven, and only a
reader catches it.

Never record something as passing that you did not run. Findings from reading
and findings from execution are labeled separately.

### 5. Incorporate review — read the round records first

A session fixing review feedback starts at `seal/specs/<work-item-id>/`,
**not** at the inline comments. Two of its files are owned by the implementer:

| File | Written by | Acted on by |
|---|---|---|
| `round-N.md` | `round_record.py new`, run by the review orchestrator; `close` applies the fix table | next review round |
| `tests-todo.md` | review orchestrator | **implementer** — plant each test in the file the row names |
| `evidence-todo.md` | review orchestrator | **implementer** — merge each fact into `seal/ledger/<work-item-id>.md` |

Inline comments may not contain these lists at all. Fixing only the comments
ships the code change and silently drops the tests and the evidence.

A finding is a claim too, and it arrives from someone who did not write the
code. Open the coordinate and judge it yourself: fix what holds, and where it
does not, answer it in `round-N.md` with the grounds — the policy clause, the
original's behavior, the constraint that makes the state unreachable. What is
not allowed is the third path, changing the code to quiet a finding you do not
believe. A review the implementer cannot argue with is not a review, it is a
handoff of judgment.
Probes already run by a previous round (listed in `round-N.md`) are not
rebuilt — only re-checked for whether the finding is now fixed.

**A fix pass hands over a fix table and writes no phase record.** The table
sits under `## Fixes` as `| # | Verdict | Commit or grounds |`, one row per
OPEN finding of the round it answers: `fixed` with the commit, `answered` with
the grounds, `deferred <home>` with the issue or file it went to — a finding
the reviewer closed in the report takes no row, and `close` refuses one. The pass
writes no `phases/phase-N.md` and no `plan.md` row — `round_record.py close`
applies the table to `rounds/round-N.md` and measures the fix surface from
the range of fix commits, so the round record is the pass's record. The
build's phases keep theirs. Nor does a fix pass add mechanism — a rule, a
checker, a template section, a walk — and a finding closable only by one is
`deferred #N` to an issue; `skills/code-review/orchestration.md` §*A fix
pass adds the unit that pins it, and that unit ships unreviewed* owns that
rule.

### 6. Close before merge — drain the rows, keep the records

Before the PR merges, every unresolved (⬜) row must move out:

| Remaining item | Destination |
|---|---|
| Doable within this PR | Do it now — merging is the last moment anyone is looking |
| Waiting on prerequisite work | `seal/follow-up.md` |
| Needs a decision | The policy document's open-questions section |

Then say so in the round record: what went where, or `nothing to drain`. The
records themselves stay. It used to be deleted here, and deletion was buying
one thing worth keeping — a deadline that forced the draining — while costing
more than it bought: rows left for durable homes because the directory was
about to disappear, and those homes are outside what the next reviewer reads.
A deferral that leaves the round records leaves the inheritance range with
it, and comes back as a finding next round.

A finding deferred mid-change is a row in `round-N.md`'s Deferred field as
well, naming where it went. That field is the one-line version of this table,
in the file the next round already opens.

## Proof block

End the response with this block whenever the skill was applied. Its values
cannot be filled without actually opening the documents — that is the point.
Never invent them; write `none — <reason>` for anything not actually read.

```
📋 implement applied
· spec:     <policy/SDD files and clauses actually read>
· evidence: <ledger rows added or updated, with the file they went in>
· verified: <what was executed vs. what was only read>
```

When the skill matched but did not apply, say so explicitly with the reason —
silence is indistinguishable from failure to trigger.
