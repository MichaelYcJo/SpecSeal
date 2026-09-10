# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `26f5277` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build `plan.md`'s row 4, the last one, and hand to the review chain. Write
`overview.md` — which closes the one failing case at the phase's start,
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` — with two
`Not verified` rows: the full suite, lint and typecheck answered by **the
sealer** rather than the orchestrator, since this is the work item that gives
that run an owner, and `payload-meter --agent sealer`, unrunnable until #292
merges. Its `## Where spec and implementation diverged` owes two rows the
orchestrator caused rather than the build: `spec.md` S7 and `plan.md`'s
phase-3 Verified-by both name things that do not exist on this branch.

Write `changelog.md` in the shape of
`seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/changelog.md`
— one `- **bold lead.**` entry per user-visible change, each ending with the
issue number: the fourth agent, the `broad-gate` command and the row a
repository has to write, `round_record.py seal`, and the rule now naming its
owner; with the stamp in the first or second entry as what a person sees, and
the ASCII twin named for a console that cannot draw blocks.

Take phase 3's three carried rows. **One:** rename
`test_the_section_says_the_full_run_is_the_orchestrators`, which asserts the <!-- NAME NOT IN TREE: the name as the task named it; this phase is the rename -->
opposite of its own name — and because `seal/ledger.md`'s R4 cites that
coordinate, the rename REMOVES the anchor rather than drifting it, so the row
loses the coordinate there and the claim is written into this work item's own
fragment. **Two:** the rows phase 2 drifted, plus whatever phase 3's edits
drifted, re-verified with the scoped WRITE form and then read unscoped to 0
broken. **Three:** two edits to `docs/flow.md` — #30's box ticked in 0.10.0,
and a row for #330 added to 0.10.1, written from the issue rather than copied.

Then the modules the branch touched plus four named ones,
`survivor-check --range 6f09a3f..<head>` with what it reports corrected or
exempted, `phases/phase-4.md`, the Status cell, and `overview.md` closed.

Mid-phase the coordinator added five items for a phase 5, to be carried here
and not acted on: the ambiguity of *after the rounds settle*, the capped run's
missing path to a seal — to be MEASURED here rather than believed — the word
`seal` claimed by two agent definitions at once, the rule that one seal is
final, and the rule that every reference to an instance of it names whose.

## What this phase found

**`docs/flow.md:86` orders this release *#292's meter · #30 · #84 · then
#120*, so the meter is FIRST and not fourth — which corrects phase 3's
record.** That record read the bullet list's order, where the sequence is
stated in a block quote above it, under a paragraph headed *the order has one
constraint that is not the list's order*. Nothing phase 3 built depended on
it, and the consequence lands here rather than there: the two coordinates the
frame verified against, `tests/test_a_section_marked_for_one_role_reaches_
only_that_role.py` and `payload-meter`, are #292's and are absent because that
pull request (#329) is open. Under the list's order they would have been late;
under the real order they were never going to exist yet. `overview.md` records
both as divergences the frame caused.

**A capped run has no path to a sealed pull request, and it was measured
rather than read.** A probe built the state and ran the chain end to end:

| What was asked | What it answered |
|---|---|
| `Needs a fix` after `close` applied a fix table closing the finding `deferred #999` | `yes — 🔴 1` — unchanged, because the field is the reviewer's and `close` rewrites nothing |
| the `Pass` box | `- [x] Pass` — checked, because `deferred <home>` is a closing word and no verdict is open |
| the verdict row | `\| 🔴 1 \| … \| deferred #999 \| #999 \|` |
| `round_record.py seal` | exit 2 — *round-1.md's `Needs a fix` reads `yes — 🔴 1`, and the broad gate runs after the rounds settle … no cell was written* |
| `chain_check.py`, judged ready | exit 1 — *`Broad gate` is `not yet` on the last round record, and this is a ready pull request* |

So every step of the coordinator's chain holds, and the two rules contradict
each other: `docs/review-chain-spec.md` says a capped run labels its pull
request `chain: capped` and opens it ready, and nothing can write the cell that
a ready pull request requires. **It bites only where the capped round found
something** — a capped round that opens nothing leaves `Needs a fix: no` and
seals normally — which is exactly the case the cap exists for. The repair is
`seal`'s condition rather than the documents: `Needs a fix: yes` should refuse
only while a finding is still OPEN in the verdict table, which is what `Pass`
already answers one row down. **Phase 5's**, with a case seen red first and the
widened condition stated in the docstring beside the three refusals. The probe
was deleted, as §7 requires.

**The base commit's ledger is clean, which is what made an unscoped re-stamp
the honest form here.** The handoff prescribes the scoped WRITE,
`--ledger '<fragment>' --reverify`, so a blanket run cannot re-stamp a row
somebody else has to judge. All eighteen drifted rows were in `seal/ledger.md`,
which that form cannot reach. Measured instead of assumed: `evidence-check` in
a worktree at `release/v0.10.0` reads **1055 ok · 0 drifted · 0 broken**, so
there was no pre-existing drift for a blanket run to take. Every one of the
eighteen was re-read against this branch's own diff for that anchor, given a
note saying what moved and whether the claim holds, and dated 2026-09-10; the
fragment was stamped by the scoped form first, and the unscoped READ afterwards
is **1089 ok · 0 drifted · 0 broken · 0 old-format**, exit 0.

**Two of the eighteen were false rather than merely drifted, and re-stamping
alone would have preserved them.** R4 and R5 both still said the full run was
the orchestrator's — the sentence #30 removed from the two documents they
cite. A re-stamp recomputes a hash and reads nothing, so a row whose CLAIM
went stale passes it silently. Both claims were corrected in place. This is
the argument against re-pointing R4's removed coordinate at the new name as
well: it would have carried a false claim onto a coordinate that resolves.

**The rename is this repository's first worked instance of *a removed anchor
is not re-pointed*.** The rule is in `CLAUDE.md` and `templates/ledger.md` and
had no example. R4 lost the coordinate, the new claim is S1 of the fragment,
and the case's docstring now says why the old name stood — phase 3 deferred
the rename on purpose so the ledger row it forces would be repaired beside it.
Two lines of `phases/phase-3.md` name the old case, which `evidence_check`'s
records arm refuses; both carry `NAME NOT IN TREE` rather than being corrected,
because what phase 3 read was that name.

**`survivor-check` exits 0 on the phase range and finds four more over the
branch, so the phase range is not the range CI reads.** `6f09a3f..HEAD`
reported four places and `origin/release/v0.10.0...HEAD` — the pull-request
check's spelling — reports four different ones. Anything that runs only the
phase range hands a pull request four reports nobody has judged.

**Two of the phase range's four were live and were corrected, not exempted.**
`chain_check.py`'s gate docstring and the inline comment below it both
enumerated the writers of the `Broad gate` cell and stopped at one — *`close
--broad-gate` is the only thing that changes the value* — which #30 made false.
Phase 3 saw them and left them, reading the sentence as reasoning that survives
`seal` joining `close`. The word is *only*, and the conclusion it carries, *so
a cell this arm cannot parse there is a cell somebody chose*, rests on the
enumeration being complete; phase 3 had already corrected the same sentence in
the docstring of the case that pins that arm, which left the pin naming two
writers and the code naming one. The other seven are records of what was true
when they were written, or descriptions of the cell's VALUE FORMAT — a wording
the correction kept verbatim — and each is exempted with a quote and grounds.

**An exemption row's Path cell must hold the path and nothing else.** The
`CHANGELOG.md` row was first written `` `CHANGELOG.md` (0.9.5's entry) `` and
was not matched, while two rows beside it with bare backticked paths were. A
line number is accepted — phase 3's `README.md:71` row carries one — so what
the reader refuses is trailing prose, silently, by reporting the place as still
standing. The tell is an exemption that changes nothing.

## Five items carried to phase 5

Four of the five are one subject — what the word `seal` means and who owns
each instance of it — and they are listed together because splitting them is
how the fourth went missing in the first place. Items 3, 4 and 5 will likely
be one commit touching one case module. Item 2 is separate and stands alone.



**1. *After the rounds settle* is prose over a condition a machine already
reads.** A work item has build phases with their own progression and a review
chain with its own rounds, so *the rounds* does not say which. The condition is
exact and it is a row: **the last round record's `Needs a fix` reads `no`**,
which is the first thing `round_record.py seal` refuses on — so the mechanism
is right and only the words are vague. The phrase stands in `agents/warden.md`,
`skills/verify/SKILL.md` twice, and `skills/code-review/orchestration.md`, with
`agents/smith.md` carrying its own spelling. Name the row instead of the moment
in each, and in `agents/sealer.md` too, since a sealer spawned early is the
failure that row prevents.

**2. The capped run, above.** The repair is `seal`'s condition.

**3. The word `seal` is claimed by two agent definitions, and one of them is
wrong.** `agents/warden.md:22` opens *You keep the seal: what a mark records is
that your review happened*, and `agents/sealer.md:21` opens *You take the
seal.* What the warden keeps is `<git-dir>/specseal-reviewed`, the mark that a
review happened; what the sealer takes is the broad gate's stamp, that a tree
was green at a SHA. One word, two referents, in two files a reader opens
together. The fix is the warden's sentence — it should name the **review
mark** — keeping the rest of the paragraph's meaning (a record and not a
barrier, the commit gate waivable without one, the record worth whatever is put
behind it) and adding one clause saying the seal is a different mark and a
different agent's. Renaming the sealer is not on the table: the product's name
is built on the noun and the whole stamp design rests on it.

Two facts measured here rather than left as the handover's prose.
**No test pins the phrase**: `grep -rn "keep the seal\|keeps the seal"` over
`tests/`, `docs/`, `skills/`, `agents/`, `templates/` and both READMEs returns
exactly one line, `agents/warden.md:22` itself, at `26f5277`. And
**`README.md:594` is a third referent, and it needs the same treatment**: *what
exists is the instruction, the warden's audit of the seal, and the `round-N.md`
field that makes a repeat visible* — that seal is the smith's `verify` proof
block, which is neither the review mark nor the broad gate's stamp, and the
sentence sits three bullets from one describing the `Broad gate` cell. A reader
of that bullet list now meets the word twice in one screen meaning two
different things. It is one more sentence in the same pass.

**4. Nothing says which seal is the final one, and that is the rule item 3
was missing.** The owner stated it: *every agent seals what it verified, and
the one seal over the whole project is the sealer's.* So the word is not
overloaded by having many instances — a smith's proof block is that smith's
seal over its own slice, and it is legitimate — what was missing is that one
of them is final and nothing anywhere says so. **Two properties already make
the final one distinguishable and the paragraph should name those rather than
invent new ones.** Scope: every other seal covers what that agent touched, and
the sealer's covers a tree nobody is still editing. Form: every other seal is
text, and the sealer's is the only one drawn as a picture — which is why #30
prints the disc on success alone, so seeing the drawing means the last one was
earned.

Where it goes follows this repository's own rule, the one
`tests/test_the_rules_have_one_owner.py` holds: one carrier states a rule and
every other links to it by name. `skills/verify/SKILL.md` owns the concept —
it holds the Seal Test and the seal block — so it states this, and
`agents/sealer.md` and `agents/warden.md` each carry one sentence naming it as
the owner. That is also where item 3 points: the warden's opening stops calling
its review mark a seal, and its link sentence is what says which seal is which.

**It belongs in that module's `RULES` table, and the judgment is asked for
here rather than assumed.** The table's entries are `(owner file, the sentence
the owner states, {other carrier: the link phrase it must carry})`, and this
rule has exactly that shape — one owner and two carriers whose sentences must
stay links rather than becoming restatements, which is the drift the table
exists to catch. A row is mechanism, so it needs a case seen red; phase 5 is
implementation rather than a fix pass, so it may add one.

**5. A bare *the seal* is ambiguous the moment more than one exists, so every
reference to an INSTANCE names whose.** The line: the concept and its formats
stay bare — `Seal Test`, `seal block`, `SpecSeal`, `counterfeit seal` are all
fine as they stand — and an instance never is. *The smith's seal*, *the
sealer's seal*, *the review mark* each say whose. `README.md:594`'s *the
warden's audit of the seal* is the shape to look for: it names an auditor and
leaves the audited seal anonymous, and the answer there is the smith's. The
failure arrived from the party writing the rule down — the orchestrator said
*the seal is in three places* while specifying this.

**The home exists and it is not a new module.**
`tests/test_one_word_one_meaning.py` was built for this class, and its
docstring says why the shape is what it is: *each word gets ONE meaning and
every coordinate is brought to it — a case per word, asserting the pinned
phrasing AND the absence of the loose one … A document can gain the corrected
sentence and keep the old one two paragraphs down, which is how two answers
ship at once.* It pins five words today; `seal` is the sixth. Two things to
get right: **the absence assertion has to exclude the concept's own terms**, or
it goes red on every file that mentions the Seal Test, and a case there is
mechanism, so it is phase-5 implementation with a red seen first.

No sixth use of the word was found.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md`'s R4 coordinate on the renamed case, and with it the fourth ground of that row | S1 of `seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md`, which carries the claim under the new name. R4's Notes says the coordinate left and where it went, so the shorter grounds list does not read as an oversight |
| The case name `test_the_section_says_the_full_run_is_the_orchestrators` | `..._the_sealers`, in the same file with the same body. Its docstring keeps the reason the old name stood, and the two lines of `phases/phase-3.md` that name it carry `NAME NOT IN TREE` |
| `chain_check.py`'s two claims that `close --broad-gate` is the only thing that changes the `Broad gate` cell | the same two comments, now naming `seal` beside it. Nothing else held that enumeration: the two printed messages were corrected in phase 3, and the docstring of the case that pins the arm names both writers already |
| The stale owner in `seal/ledger.md`'s R4 and R5 claims — *the full suite is the orchestrator's* | the same two claims, saying the sealer's. The documents they cite were re-pointed in phase 3; the ledger's copies were not, and a re-stamp would have carried them |
