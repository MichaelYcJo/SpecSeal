# 1789296100-the-seal-and-ci-read-one-ledger-differently — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `<filled with this phase's commit>` |
| Ran by | unknown — the spawn prompt named no model, and the value is the spawning session's to fill |

## What this phase was asked

Five documents stop describing one reader: `skills/evidence-check/SKILL.md`
(the Run block, the `--strict` flag row, the `DRIFTED` verdict row),
`README.md` and `README.ko.md`'s ledger paragraph, `CONTRIBUTING.md`'s check
list, and the `ledger` job's comment in `.github/workflows/test.yml`, which
argued leniency without naming the reader that disagrees. Phase 1's structural
case goes green.

## What this phase found

**Q3, measured, and the step needs no edit.** The `ledger` job's shell body was
run verbatim over a drifted fixture rather than read. The step exits 0, and the
log ends:

```
exit 1 is the lenient reading. `broad-gate` runs this same check with `--strict`, where drift is exit 2, and this tree would come back NOT SEALED.
::warning::evidence ledger reports drift — re-verify the rows above
```

The two read as one message and in the right order — the sentence first, the
warning naming the rows above it. Only the comment was edited, which is what
the default said, and the reading is now a run.

**S5 was shown red once per document, not once.** The case had been red against
all five since phase 1. That is one red for a five-file rule, so after the
edits `broad-gate` was replaced with a bare `the gate` in one file at a time
and the case re-run: **all five went red individually and the tree restored
byte-for-byte each time.** A rule that five files satisfy is worth exactly as
much as its ability to name the one that stops.

**The per-block rule earned itself twice.** `README.md:43` and `README.ko.md:41`
name `broad-gate` in the sealer's row of the agent table, a hundred lines from
anything about drift, so a file-level check would have passed both READMEs
before this phase began — and the per-file mutation above would then have shown
them green with the ledger paragraph gutted.

**Two existing cases caught this phase, and one of them was already red.**

| Case | What it caught |
|---|---|
| `tests/test_one_word_one_meaning.py::test_no_instructing_document_leaves_an_instance_anonymous` | the first `README.md` wording said *refuses the branch at the seal*, leaving the instance anonymous — `CLAUDE.md` §*a thing more than one party can have is named with whose*. Reworded to name the sealer, and `README.ko.md` was reworded the same way rather than being left as the one language that did not say whose |
| `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview` | **red on this branch from the framer's own commit `17164d7`**, which wrote `spec.md` with no `overview.md` beside it. `plan.md` puts the memo in phase 4, which would have left an existing case red across every review round of this work item. The memo is opened here instead |

The second is a finding about the frame, not about this phase, and it is
recorded in `overview.md` §*Where spec and implementation diverged* rather than
being routed back to the framer.

**`bin/evidence-check`'s header was left alone**, which `plan.md` permitted an
edit to. The wrapper already shows `evidence-check . --strict` as a form a
reader can type, and the fact about who passes that flag now arrives in the
output of every run that needs it. Editing the POSIX header and not the `.cmd`
sibling is the surviving wording `survivor-check` reports; editing both
duplicates a sentence the script already prints. Recorded in `overview.md`
§*Not done*.

**Run at this phase's close:**
`bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py tests/test_a_narrowed_ledger_read_says_what_it_skipped.py tests/test_chain_hooks_hardening.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py -q`
— **121 passed**. The first run of that set was 2 failed, 119 passed, and both
failures are the row pair above.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `ledger` job's comment as the only statement that drift is tolerated, with no reader named beside it | the same comment, which now names `broad-gate` and the `--strict` grading, and `skills/evidence-check/SKILL.md` §*Which reader graded your tree*, which holds all three readers in one table |
