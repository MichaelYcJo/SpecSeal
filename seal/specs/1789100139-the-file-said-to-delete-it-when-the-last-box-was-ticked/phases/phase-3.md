# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — phase 3

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `2206a0c` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

Repair the live citations that would name a file which does not exist:
`tests/test_release_hygiene.py`'s exemption entry, its docstring clause and
its fixture path; `tests/test_a_corrected_sentence_survives_elsewhere.py`'s
comment; both `skills/code-review/scripts/survivor_check.py` docstring
citations; `skills/verify/scripts/broad_gate.py`'s. And Q3 (c): both editions
of the 0.4.0 design record lose the clause naming the file, the rest of the
sentence standing. Each touched module run on its own, exit code read.

## What this phase found

**Q5, measured rather than assumed.** The question was whether removing
`"docs/flow.md"` from `RECORDS_OF_A_MOMENT` leaves any loaded file that still
needs the entry. Recomputing the check over every tracked loaded file with
that one entry dropped and every other exemption in place returns **seven
offending lines, all seven in `docs/flow.md`**:

    docs/flow.md:43 names 0.11.0    docs/flow.md:77 names 0.11.0
    docs/flow.md:67 names 0.11.1    docs/flow.md:78 names 0.11.0
    docs/flow.md:76 names 0.11.1    docs/flow.md:102 names 0.11.0 (twice)

No other loaded file needs it. The entry is removed, and the default in
`questions.md` — *remove the entry, repoint the two fixtures* — holds.

**What the measurement changed is WHEN the entry comes out, and that is a
divergence from `plan.md`.** Phase 3 was to remove it; it is removed in phase
4's commit instead, with the file. The seven lines above are the reason: with
the file still tracked, a commit that drops the entry and keeps the file
leaves `test_no_loaded_file_names_a_version_at_or_above_the_running_one` red.
A commit that does not stand on its own is what `skills/implement/SKILL.md`
§2 tells this session not to write, so the two halves of one atomic change
ride together. The docstring clause and the fixture, which are independent of
the file's existence, are in this phase's commit.

**There is one fixture usage, not two.** `spec.md` §Data & interfaces and the
handoff both name *two cases* using the path as a fixture —
`test_a_record_of_a_moment_keeps_every_version_it_names` and *the `timers_in`
assertion around line 574*. Those are the same site: line 574 is the first
assertion inside that case. `grep -n '"docs/flow.md"'` over the module returns
three lines and no more — the entry, the docstring, and that one fixture. It
is repointed at `docs/one-root-by-lifetime.md`, which is an exact-path entry
that still exists, so the case keeps testing both shapes it claims to test.

**Q4's two repairs are not the same repair, and the second is the one with
content.** `survivor_check.py`'s first citation attributes a design decision
to a row in the deleted file; it now attributes it to the moment the decision
was made — *the shape was written down when #180 was scheduled* — and keeps
the sentence itself, which was already quoted inline. The second citation
pointed at a section for the list of durable copies a deletion leaves behind,
and a pointer to a deleted section is worth nothing, so it **states the
list**: the design records under `seal/specs/`, `CHANGELOG.md` and the
tickets themselves. `tests/test_a_corrected_sentence_survives_elsewhere.py`'s
comment carried the same pointer and took the same repair, because it is the
same claim one file over — which is §12's enumeration, not two coincidences.

**`broad_gate.py`'s citation needed nothing said, only a path dropped.** It
reads *#103's class made out of the fix for it*, and #103 is an issue that
still exists and still describes its own class. An issue number is the
durable coordinate here; the file was only ever where somebody had written
the number down.

**S6 caught three lines this work item wrote itself.** After the six repairs,
`git grep "flow\.md"` outside `CHANGELOG.md`, `seal/ledger.md` and
`seal/specs/` still returned four hits: the exemption entry, and three
sentences from phases 1 and 2 explaining where the section came from — one in
`skills/implement/orchestration.md`'s intro and two in
`tests/test_the_rules_have_one_owner.py`. Each was a correct sentence about
history and each named a path that will not resolve. They name the issue and
describe the file instead (*the shared checklist that was deleted for being
written by every branch*), which is the same rule the owner's Q3 call states
from the other side: the changelog is where a removal is recorded, so no
other file carries a marker for it.

**Both editions of the 0.4.0 record moved together**, which `CONTRIBUTING.md`
requires and which the clause's own wrapping made non-trivial: the English
sentence spanned two lines and the Korean three, so both paragraphs were
re-wrapped rather than having a clause cut out of them. No version number was
added to either, which is what (b) would have cost and the reason (b) was
declined.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tests/test_release_hygiene.py`'s docstring clause *`docs/flow.md` is a list headed by the version it tracks* | Nowhere. It argued an exemption that phase 4 removes; the two exemptions that remain keep their arguments |
| `survivor_check.py`'s pointer to §*A shipped version's section is deleted, not kept* for the durable copies | Stated inline instead, in both carriers: the design records under `seal/specs/`, `CHANGELOG.md` and the tickets |
| `survivor_check.py`'s attribution of #180's shape to a row in the deleted file | Attributed to #180's scheduling instead; the quoted sentence was already inline and is unchanged |
| `broad_gate.py`'s `docs/flow.md` before *#103's class* | Nowhere — #103 is the coordinate and it still resolves |
| The clause *`docs/flow.md` is the checklist that tracks them until the last one merges* from `docs/one-root-by-lifetime.md` §*Order* and its Korean edition | Nowhere. Q3 (c): the rest of the sentence stands and the removal is recorded in the changelog fragment, not by a marker left in the record |
