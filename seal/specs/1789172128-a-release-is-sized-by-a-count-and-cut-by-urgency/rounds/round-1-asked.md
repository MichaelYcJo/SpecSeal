# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `5ce162e` — every measurement below was taken there |
| Review at | HEAD of the branch, which adds only this paragraph on top of the target |
| Base | `origin/release/v0.11.1` = `7e17f5e` |
| Draft pull request | #364, opened before this round |
| Ran by | specseal:warden on Opus 5 |

## Scope

Issue #361 — a release's size stops being a count and becomes a criterion, and
a label records the answer so the next release is cut without re-reading every
open issue body. Six commits, `6de3f54` through `5ce162e`, on the frame commit
`3b9651b` and the routing commit `bbb6727`.

One document edited (`docs/issues-and-milestones.md`, +62 lines), one new test
module, three ledger files touched, and this work item's records.

## Facts, with labels

**Executed by the orchestrating session** at `5ce162e`, exit codes read
directly with no pipe:

- Nine modules, one per call — `test_a_release_is_sized_by_a_criterion` 7,
  `test_docs_line_wrap` 23, `test_release_hygiene` 32,
  `test_one_word_one_meaning` 13, `test_no_real_identifiers` 2,
  `test_a_row_points_by_content` 102, `test_the_set_a_work_item_always_has` 16,
  `test_a_record_states_what_the_tree_has` 58,
  `test_a_question_says_who_can_answer_it` 6 → **exit 0 each**.
- **The new module seen red, by reverting the document rather than by
  reasoning.** `docs/issues-and-milestones.md` restored to `7e17f5e` → **5
  failed, 2 passed, exit 1**; the five are `test_the_rule_states_the_criterion_and_not_the_count`,
  `test_the_count_survives_as_a_ceiling_in_the_wording_the_cap_already_uses`,
  `test_the_two_releases_are_cited_without_a_version_number`,
  `test_the_rule_says_what_it_does_not_change`,
  `test_the_label_is_two_states_and_nothing_reads_it`. Restored → 7 passed,
  exit 0, `git status --porcelain` empty. **The two that stayed green measure
  the tree rather than the sentence** — the sweep and its can-fail control —
  and the builder reports mutating each of those separately. Re-derive that.
- `uvx ruff check` and `uvx ruff format --check` on the new module → exit 0 each.
- `timers_in` re-run over the whole `LOADED` set at the running version →
  **no offenders**.
- `bin/evidence-check .` → **exit 1 on the records arm only**; the ledger arm
  reads 1144 ok · 0 drifted · 0 broken.

**Executed by the builder**, its own numbers, in `overview.md` and the phase
records: the full narrow set above plus `survivor-check` over
`7e17f5e..HEAD` with `survivors.md` (exit 0, every survivor excused),
`unverified-check` on the memo (exit 0, 4 open), and one deleted `test_tmp_*`
probe. Re-derive rather than inherit — in particular the survivor exemptions
and the claim that each of the sweep's two units was mutated.

**Read, and it is why the evidence carries no version numbers** —
`tests/test_release_hygiene.py`'s `timers_in` refuses every version-shaped
token at or above the running version in the `LOADED` set, `LOADED` includes
`docs`, and the running version is read from `.claude-plugin/plugin.json`.
Both releases the rule cites sit at or above it.

**Read, and it is the defect that was filed rather than fixed** — `v0.11.0` is
tagged, `origin/main` is its release merge, and `CHANGELOG.md` carries its
heading, while `plugin.json` still names it as running. So the refused number
is one the repository has shipped. **#363** holds it.

**Read** — the document's two internal references resolve. The bolded lead-in
it cites for keeping a version illustrative exists and says exactly that, and
names the same check.

**Unverified** — the broad gate. It is the `sealer`'s, after this chain settles.

## Four answers a person gave, which are not yours to reopen

**Q1 — (c).** The two releases are cited as prose with no numbers, and the
checker's off-by-one is #363. Judge whether the prose does that, not whether
numbering would have been better. **A finding that proposes editing
`tests/test_release_hygiene.py` is out of scope by the owner's answer.**

**Q2 — (b), the prefix form.** The owner chose the shape, not the string. The
builder chose `size: now` and took `chain: capped` as the precedent rather than
`merged: X.Y.Z`. Judge the reasoning; the spelling is finally settled when the
owner creates the label, so a better spelling is a note and not a defect.

**Q3 — (a).** The label is created and applied by the owner after this merges.
**This work item writes nothing to the tracker**, and a finding that it should
have is out of scope.

**Q4 — (a).** Release milestone descriptions are out of scope.

## Three divergences the builder declared — judge each, do not inherit

- **The paragraph does not say *nothing automated reads either*.** It says
  nothing *schedules* from either, because §*One thing reads a milestone, and it
  can stop a release* has said the opposite since #359. The narrower clause is
  the true one. `spec.md` expected the wider wording.
- **No exception is written for the label**, against `spec.md`'s expectation.
  The argument: the prefix makes `size:` a topic — sizing, which every release
  has — so §*A label answers what it is about* is not broken and only the value
  is spent. `flow-measurement` stays the one label that is not a topic at all.
- **Two ledger rows drifted where the frame found one.** `seal/ledger.md`'s G5
  and S4 both cite the label section; both were re-read, dated and re-anchored.

## Two things the builder flagged for a second reading

- **`#351`'s `changelog.md:22` quotes the sentence this branch replaces**, and
  both fragments gather into the same released section. Excused in
  `survivors.md` on the ground that its own claim is still true. The builder
  names the alternative reading itself — that a released section should not
  quote a sentence the same section replaces — and it is also a
  `## Not verified` row. This is the judgment most worth a reviewer.
- **The records arm's drift**: this work item's `spec.md:159` quotes the section
  the branch then edits. Inherent to a spec that grounds itself in the code it
  changes, a warning rather than a failure — the ledger job exits only at 2 or
  above. Whether the quote should be re-stamped was left to this round on
  purpose.

## Where a claim flips on how it is measured

**The sweep's absence check cannot be a plain `git grep`.**
`git grep -n "three or four is the size"` exits 1 against the *unedited*
document, because the line wrapped between `three` and `or four` — so the
obvious spelling of that check passes for the wrong reason. The case reads
through a whitespace-flattening reader instead. Check that the reader is
actually flattening, and that the sweep would catch the sentence reappearing
with a different wrap.

## The commands, in the form to use

`bin/test`, narrow, one module at a time. `ruff` is not installed here — `uvx
ruff check` / `uvx ruff format --check`. Read exit codes directly, never
through a pipe (`cmd > /tmp/x 2>&1; echo $?`); this shell is `zsh`.
`evidence_check.py .` **unscoped for reading** — the `--ledger` narrowing is
for a `--reverify` write and blinds a read.
`bin/survivor-check --range 7e17f5e..HEAD --exempt <this item>/survivors.md`.

**Do not run the broad gate.** No `bin/broad-gate`, no full suite, no
repository-wide `ruff`.

## The two lines the run ends on

Answer each in a line of its own — `Needs a fix: no`, or `yes` and what does;
and `Loses a record or crashes: no`, or `yes` and what does. A 🟡 answered with
grounds is `no`, and a finding located under `seal/specs/` is a correction that
does not count.
