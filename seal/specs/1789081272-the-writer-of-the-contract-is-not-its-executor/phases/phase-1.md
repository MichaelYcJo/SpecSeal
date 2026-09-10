# 1789081272-the-writer-of-the-contract-is-not-its-executor — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `51ff098` — the phase is `77e0ae5` (the definition), `57bc82e` (these records) and `51ff098` (the survivor correction) |
| Ran by | smith on Opus 5 (1M context) |

## What this phase was asked

`agents/framer.md`, the fifth agent definition, and its entry in
`tests/test_docs_line_wrap.py`'s `COVERED`.

Shape it on `agents/sealer.md` — the newest definition and the only one
written after §6 stopped carving exceptions, so its `## The one write, and
why it is yours` is the grant form to copy. Name the three writes (`spec.md`,
`plan.md`, `questions.md`, each from its `templates/` file) as the whole
permission, and carve no exception anywhere.

The content came from #84 and its six comments: what the framer is, why it
exists (the anchor, never speed — the one measurable clause came in at 1.30
tools per turn against a 1.27 baseline), what it reads against what the smith
reads, that it opens questions without owning their answers, that a phase
prompt is a pointer at a `plan.md` row rather than a page of its own, that
its phase is the one interactive one, that the SDD ladder decides when it
runs, and that its report names the path and the count of the questions it
opened rather than their text (Q2).

Two bounds were given as constraints. `agents/framer.md` must not assign the
broad gate and specifically must not carry `spawned for exactly that`, which
is the marker `tests/test_broad_gate_rule.py:286` counts against §2's word
`One`. And it may cite a contract section by number and say what it means for
the framer, but may carry no 15-word run of any section body.

Two items arrived labelled unverified, with this phase named as the answerer:
whether `tests/test_one_word_one_meaning.py`'s `SEAL_SWEPT` and
`tests/test_the_seal_is_taken_once_by_the_sealer.py`'s `DEFINITIONS` need the
new file. Also asked: say whether row 1 holds before building to it.

The `skills:` list was given as `agent-contract`, `implement`,
`feature-planner`, `confidence-check`, `writing-style`, with the two utility
skills leaving `agents/smith.md` in phase 2 so that phase is a move rather
than a copy. That instruction is where this phase diverged, below.

## What this phase found

**Row 1 holds. The `skills:` list given with it does not, and that is
measured rather than argued.** Written with all five entries, the tree comes
back red on two cases nothing in the plan accounts for:

- `test_every_shipped_skill_is_named_in_both_readmes` — *README.md's agents
  table never names `confidence-check` as preloaded by any agent.* The case
  builds the preloaded set from the union of every `agents/*.md` frontmatter
  and requires each member to appear in a `| **` row of both README editions.
- `test_the_readme_group_counts_are_derived_too` — *README.md's skills row
  does not say `The Seven the agents follow`, and the `preloaded` group holds
  7.* The counts move 5/11 to 7/9, both editions' skills row goes stale, and
  9 has no entry in that case's own `spellings` table, so the repair is two
  README editions plus a constant in a test.

None of that is in phase 1's delivery, in phase 2's row, or in `spec.md`
§Scope item 8, which enumerates the documents that describe the agent set as
four and names neither README.

So the list was built as `agent-contract`, `implement`, `writing-style` — the
three `agents/smith.md` carries — and the two utility skills are named as
**callable in prose**, with a sentence saying why they stay off the list. Two
things say that is the right form rather than a workaround. S4 asks only that
they be *named as callable in `agents/framer.md` and in no other
`agents/*.md`*, and `agents/smith.md` names them today in exactly that
way — in prose, not in its frontmatter, which is what makes S4's new case red
against the smith as it stands. And a preloaded body is paid for on every
spawn (#292); `test_the_sealer_preloads_the_contract_and_nothing_else` is
that argument already written into a case, for the agent whose procedure is
one command.

**Phase 2 is still a move, not a copy.** What moves is the design-gate
paragraph naming the two skills, out of `agents/smith.md` and into the
framer's own words — which are already there. Phase 2 also owns the third
axis of this, untouched here: both skills' frontmatter carries a `smith is
driving` stand-down clause that
`tests/test_the_design_gate_belongs_to_the_smith` pins, and that clause names
the wrong agent once the gate is the framer's.

**Both unverified items are answered, and they answer differently.**

- `SEAL_SWEPT` needs the file, and it is now in it. The list's own membership
  test is *files that instruct somebody*, and a definition is one. Shown
  load-bearing rather than assumed: with a bare `the seal` planted in
  `agents/framer.md`, the sweep is red with the entry (naming the file and
  quoting the sentence) and green without it.
- `DEFINITIONS` does not need it, and adding it would be wrong. Its three
  cases require `the full suite is the sealer's, once, after the rounds
  settle` and the coverage-probe sentence, and both are applications of §2 to
  an agent that runs checks. The framer runs none — not a module, not a
  probe, not the suite — so there is nothing for either sentence to be about,
  and §2's silence rule already covers it: an agent runs none of the three
  unless its own file hands them over.

**The margin under the moved-rule window is wide.** The longest run
`agents/framer.md` shares with any contract section is 8 words, against §5
and §4. `WINDOW` is 15 and `LONGEST_KEPT_APPLICATION` — the maximum
`test_the_window_sits_between_what_was_measured` asserts on — is 10, so the
new file does not narrow the margin the case exists to watch.

**A red case is open on this branch and it is not phase 1's.**
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` fails
because this work item has a `spec.md` and a `plan.md` and no `overview.md`.
The base has no such directory at all, so the sealer would call it `new`: it
arrived with `d146944`, the frame's own commit, and every phase from 1 to 5
sits on it while `plan.md` gives the memo to phase 6. `overview.md` is opened
in this phase's second commit instead, which is what `skills/implement/
SKILL.md` §4 asks anyway — the memo opens at the first divergence, and this
phase has one.

**The survivor check found a repeated comment, and the answer was to stop
repeating it differently.** Over `d870992..57bc82e` it reported five places
still carrying *Wrapped from its first line, so it goes in at birth* — four
other `COVERED` entries and a `seal/ledger.md` row. Every report was correct
and none was a defect: that sentence is a per-entry idiom in `COVERED`, one
copy per file that arrived already wrapped, and pluralising the sealer's copy
to cover two files is what turned the four singular copies into survivors of
a removal. So the sealer's entry keeps its own singular comment with only the
false half corrected — it is no longer *the one* unswept `agents/*.md` file —
and `framer.md` takes a comment of its own. The range then reports nothing
standing, and no `survivors.md` was needed. An exemption file with no rows is
refused outright, which is the right refusal: five written rows would have
been the escape rather than the fix.

**Any edit to `COVERED` drifts a ledger row, and this one did.**
`tests/test_docs_line_wrap.py#COVERED@5409898a` anchors the claim that the
eleven modules pinning the review skill's path are not the modules its split
breaks. Re-read rather than re-pointed: a list entry and two comments move
neither the eleven modules nor the wrap-coverage loss that goes silent when
material leaves a listed file. Hash now `f06c858f`, `Checked` at the day it
was read, and `evidence-check` back to 1100 ok · 0 drifted.

**One process slip, since a hand-back that hides it teaches nothing.** The
mutation script restored `tests/test_one_word_one_meaning.py` with
`git checkout --`, which is the restore-from-HEAD failure `agents/smith.md`
§Boundaries warns about by name; it discarded the `SEAL_SWEPT` entry, which
was re-applied. `agents/framer.md` was restored from a scratchpad copy and
verified byte-identical, which is what the rule asks for.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_docs_line_wrap.py`'s claim that `agents/sealer.md` is *the one `agents/*.md` file with no sweep behind it* | the same comment, now plural and naming `framer.md` as arriving on the sealer's terms — the claim stopped being true the moment a second unswept definition landed |
