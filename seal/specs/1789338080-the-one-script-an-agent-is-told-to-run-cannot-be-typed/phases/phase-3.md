# 1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 432af98 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Write the class pin and see it red against all nine documents and both
unwrapped scripts. Then respell the two typed command forms in
`skills/code-review/orchestration.md` as `round-record`, add one locator to
each of the nine documents, and classify `chain_check.py` with its reason.
Q1 is answered **General**: the pin enumerates `skills/*/scripts/*.py` and
every `.md` under `agents/`, `skills/` and `templates/` rather than naming
`round_record.py` in the assertion. Q4 is decided by the edit itself.

## What this phase found

**Q4 is answered, and the plan's single-sentence assumption held for all nine
— but not at the first mention in three of them.** The locator sits at or
beside the first mention in six documents. In `agents/warden.md`,
`skills/implement/SKILL.md` and `templates/sdd-phase.md` it had to move to the
sentence *after*, because `tests/test_the_rules_have_one_owner.py` pins the
exact phrase each of those files uses to name the generator —
`GENERATOR_NAMED`, five carriers, one literal string each — and the first
drafts inserted a parenthetical into the middle of three of them. Splitting a
pinned phrase to satisfy a new pin is quieting one check with another, so the
phrases were restored whole and the locators moved one sentence down. No
constant of that module was touched.

<!-- Corrected in round 1's fix pass (🟡 4). *One sentence down* was true of
`skills/implement/SKILL.md` and `templates/sdd-phase.md` and NOT of
`agents/warden.md`, where it was 48 lines and two further mentions later — in
the file three of the incident's four segments were reading, which is the one
document where the distance costs most. The pinned substring ends before the
word *in*, so a clause appended after `round-N.md` leaves it whole; the
locator now sits at the first mention, at line 138. This paragraph is left as
it was written and corrected here rather than rewritten, because a record
says what was true when it was written. -->

**Round 1 also measured what this paragraph did not say.** The reviewer read
`GENERATOR_NAMED`'s substring for `agents/warden.md` closely enough to find
that it ends before *in* — which the build had not, and which is why the build
concluded the locator could not go at the first mention at all.

**The pin went red twice, as the plan asked, and the second red was cheap.**
Against the tree as it stood: ten failures, one per document for all nine plus
`chain_check.py` unclassified, each naming its own coordinate. By mutation
after green: the locator deleted from `templates/sdd-round.md` failed on that
document alone.

**The classification-defence case was driven red against a real document, not
only a fixture.** `chain_check.py --worktree` planted at
`skills/code-review/SKILL.md:48` failed naming the file, the line and both
repairs; the plant was reverted and the file is byte for byte as it was.

**The two readers the whole pin rests on were mutated, one at a time.**
`command_forms` made to match nothing turned
`test_a_planted_invocation_turns_the_classification_red` red. `reachable` made
to answer yes to everything turned both
`test_a_document_with_no_locator_is_caught` and
`test_a_locator_inside_a_longer_word_does_not_count` red — which is the pair
that matters, because a `reachable` answering yes would make every one of the
nine document cases pass vacuously. Both mutations were restored from a byte
copy kept before the mutation, never from HEAD, and `tests/__pycache__` was
cleared between them.

**A detector for *invoked* rather than *described* has one sound tell in
prose, and it is a flag.** A subcommand cannot be told from the sentence
around it — *`round_record.py new` writes the record* names a subcommand and
is a description — so `command_forms` reads the script name followed by
whitespace and a dash. That is the same operationalisation the frame measured
`chain_check.py` with, so the classification and the check that defends it
rest on one definition rather than two.

**The phase-boundary run caught two consequences the plan did not anticipate,
and both were repairs owed to this branch.** Beyond the three pinned phrases
above: `agents/smith.md`'s `# RIDER:` stamp drifted, because the locator
landed inside `## Phases` and the stamp anchors on that whole section. The
rider's subject — the `: '[no-review]'; git commit …` waiver example — is byte
for byte unchanged and 138 lines above the edit, so it was re-stamped with
`rider_check.py --reverify --only agents/smith.md` rather than repaired.

**Eleven ledger rows across seven anchors drifted for the same reason, and
re-stamping them is the only reading that leaves the ledger true.** The
anchors are whole sections — one of them, `skills/code-review/orchestration.md#"# code-review — the orchestrator's half"`,
spans lines 1–552, which is the file. There is nowhere in that file an edit
could have gone without drifting it. Each of the eleven claims was re-read
against its section and holds; none is about a command's spelling or about
where a locator sits. `evidence-check --reverify` then moved eleven hashes and
nothing else — the `Checked` dates did not move, which is recorded in
`overview.md` as a finding about the tool rather than about these rows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `round_record.py close …` and `round_record.py new …` as the typed forms in `skills/code-review/orchestration.md` | Nowhere — they are respellings of the same two commands, not a rule leaving the tree. `round_record.py` is still named in seven other places in that file, all descriptive |
