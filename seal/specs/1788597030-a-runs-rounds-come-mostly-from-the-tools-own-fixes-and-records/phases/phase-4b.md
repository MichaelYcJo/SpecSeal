# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — phase 4b

| Field | Value |
|---|---|
| Phase | 4b |
| Commit | 12c6db6 |
| Ran by | specseal:smith on fable-5.1 |

The `Ran by` value is transcribed the way phases 1 to 4a's were: the agent is
the definition this segment was spawned from, and the model is what the
harness's own system prompt states. Neither half is the segment's idea of
what it is.

## What this phase was asked

Build phase 4b of `plan.md` and only phase 4b, on branch
`feat/161-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records`,
after phase 4a closed at `ec2dfb5` — the LINKING carriers, each link one or
two sentences naming the owner phase 4a wrote, every measured incident kept,
`agents/warden.md` wrapped under 88 columns, and the rule-5 owner phrase
*hands over a fix table under `## Fixes`* kept verbatim in `agents/smith.md`.
The count-rule ceilings phase 4a's walk asserts (4 for *at most one more
round record*, 0 for *Unless th*) could only be lowered.

1. `docs/review-handoff-protocol.md`: §*round-N.md* says the record is
   written by `round_record.py new` and closed by `close`, and the
   orchestrator writes the round paragraph of the spawn prompt and nothing
   else in it; the *at most one more round record* sentence at §*Loses a
   record or crashes* kept, with the reopening linked to the spec's
   subsection; a new subsection after §*While the implementer runs* for
   rule 9, owner the skill's §*Orchestrator: the pull request opens before
   round 1, and a phase is re-run*; one sentence in §*The handoff before
   round 1* that the draft pull request is already open (rule 6, same owner).
2. `agents/warden.md`: §Role's verifying-round bullet links rule 1 (a
   record-located finding is a correction, ⬜ with the coordinate, outside
   `Needs a fix`) to the spec's §*The last round verifies*, and the one
   reopening to the spec's subsection; §Report links rule 3 (*would the
   release ship a defect if this stands?* decides 🟡 against ⬜) to the
   skill's §*Findings format*, and says `round_record.py new` writes the
   record from the report while keeping §6's fact that the warden writes no
   record itself.
3. `agents/smith.md`: the depth paragraph links rule 2 (no mechanism in a
   fix pass) to the skill's §*A fix pass adds the unit that pins it, and
   that unit ships unreviewed*.
4. `skills/implement/SKILL.md` §5: the same link in one sentence beside the
   fix-table sentence phase 2 added.
5. `docs/flow.md` §*Order inside a ticket*: step 2 becomes spec · plan →
   smith → the draft pull request opens → warden rounds → sealer → the pull
   request is marked ready, with the skill's subsection named.
6. `docs/review-chain-spec.md:22`, *written by the review orchestrator*:
   reword to name `round_record.py`.
7. A sweep over `docs skills agents templates README.md README.ko.md` for
   *the orchestrator writes* and four sibling phrases; every hit saying the
   orchestrator writes a record cell reworded to name the generator, or left
   with a one-line reason here.
8. Pins in `tests/test_the_rules_have_one_owner.py`: one per link, the
   protocol's new subsection under its heading, `docs/flow.md` step 2's
   draft clause, the warden's report naming the generator; each seen red
   with its sentence stashed; every module `grep -l` finds for the six
   files' paths run before and after.

Coordinates handed over and opened: the protocol's `:108`, `:314`, `:377-470`
and its `## ` headings; `agents/warden.md` §Role and §Report; `agents/smith.md`
`:114` and the paragraph *measured rather than declared*; `skills/implement/
SKILL.md` §5; `docs/flow.md:62-66`; the owners' headings in
`skills/code-review/SKILL.md` and the spec's three subsections;
`tests/test_the_rules_have_one_owner.py` whole; `tests/test_docs_line_wrap.py`
`COVERED`. Every coordinate resolved at `ec2dfb5` to what it was said to name
except one, below.

## What this phase found

**`docs/flow.md:62-66` is the 0.8.2 issue list, not the order inside a
ticket.** §*Order inside a ticket* sits at `:97`, and step 2 at `:99`; the
edit went there. A coordinate four sections off is the protocol's own second
requirement (*a coordinate reaches the rule, not its neighbourhood*), caught
by opening it.

**Item 6 was declined: the sentence at `docs/review-chain-spec.md:22` is
about the reviewed-HEAD mark, not the record.** It reads *`<git-dir>/
specseal-reviewed` holds the reviewed HEAD SHA, written by the review
orchestrator as the `code-review` skill's closing step*, and that is true —
`round_record.py` writes no mark (`grep -n reviewed
skills/code-review/scripts/round_record.py` returns the `--target` help line
alone). Naming the generator there would have made a true sentence false.
The sweep's other two hits are the same sentence about the same mark —
`agents/warden.md` §Role's §6 bullet, *You do not write
`<git-dir>/specseal-reviewed` either — the orchestrator writes it*, and the
warden row of `README.md:40`, whose Korean twin says the same — and all three
stay. Neither README mentions who writes round records, so the pair was not
touched. §5: the prompt's fact was opened before anything was built on it.

**The sweep's grep missed three carriers of the sentence it was for, and one
of them is a template.** `skills/implement/SKILL.md` §5's table read `|
round-N.md | review orchestrator |`; `agents/smith.md` read *the orchestrator
owns the records* beside `Fixes checked by`; `templates/sdd-phase.md`'s
comment read *the orchestrator both knows the answer and writes that file*
of `rounds/round-N.md`. None contains the five grep phrases. All three now
name `round_record.py new` — the template outside the five files the plan
row names, on the plan row's own words, *a sweep for every remaining
carrier*, and `agents/warden.md`'s two *the orchestrator copies it into the
row of the same name* sentences with them.

**A pin on a sentence written twice stayed green when one copy was
stashed.** `round_record.py new` writes the record from this report went
into `agents/warden.md` twice — the §6 bullet and §Report — and the pin
read the shared prefix, so stashing either copy left the other to satisfy
it: one mutation alive of twenty-three. Phase 4a met the same class with a
prefix of a longer sentence. Each copy is now pinned with its own tail
(*once the orchestrator has verified its findings* · *so the headers are
what it parses*), and both mutations are killed.

**A fact the prompt carried had no coordinate, and the protocol cites one
instead.** The rule-9 subsection was to say *four phases were checked that
way, each matching its hand-back*; nothing in the tree records which phases
the orchestrator re-ran. The subsection says the work item was checked that
way from its first phase and points at `spec.md` rule 9, which states it.

**The ceilings after this phase are 4 and 0, unchanged.** The protocol's
copy of *at most one more round record* was kept on the prompt's
instruction, with the reopening's owner in the same paragraph; no carrier
was added and none removed. *Unless th* stands nowhere.

**Seen red, and how.** 24 mutations over the pins this phase added — 22
stashes (each phrase deleted through a whitespace-flexible match, since the
pins read the file flattened) and 2 insertions (*the orchestrator copies it
into the row of the same name* appended to `agents/warden.md`, *the
orchestrator owns the records* to `agents/smith.md`) — 0 alive after the
re-pointing above, each restored from bytes kept in the loop and
`tests/__pycache__` cleared between; the six files were byte-identical to
their committed state afterwards, checked in the loop and by `git status`.
The 40 modules `grep -l` finds for the six files' paths (basename matches
included) passed before the edits: 1415. The eight fastest of them passed
after the document edits (296) and the pin module after the pins (37); the
40 passed again with every edit and record in the tree: 1427, the 1415 plus
the twelve cases this phase added. Every unit this phase added is a test
case; no code unit was added.

**Two instructions declined, by rule.** The environment's auto-mode note
asked for file edits through `sed`, heredocs or scripts; contract §9 routes
edits through `Edit`, and every edit here went that way. Nothing ordered the
full suite; it is handed over `unverified` with the orchestrator as its
answerer (§2).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *the orchestrator copies it into the row of the same name in `round-N.md`* and *copied into the row of the same name* — `agents/warden.md` §Role, the two terminal lines | the same two sentences, naming `round_record.py new` |
| *the orchestrator verifies findings first* as the reason the warden writes no record — `agents/warden.md` §Role's §6 bullet | the same bullet: `round_record.py new` writes the record from the report once the orchestrator has verified its findings |
| *the orchestrator owns the records* — `agents/smith.md`, beside `Fixes checked by` | the same sentence: `round_record.py new` sets the cell on the previous record when the next round posts |
| `\| round-N.md \| review orchestrator \|` — `skills/implement/SKILL.md` §5's Written-by table | the same row, naming `new` and `close` |
| *The orchestrator both knows the answer and writes that file* — `templates/sdd-phase.md`'s `Ran by` comment | the same sentence, naming `round_record.py new` and its `--ran-by` value |
| *→ sealer → pull request* as the last step of `docs/flow.md` §Order inside a ticket | step 2's *the draft pull request opens* after the smith, and *the pull request is marked ready* at the end |
