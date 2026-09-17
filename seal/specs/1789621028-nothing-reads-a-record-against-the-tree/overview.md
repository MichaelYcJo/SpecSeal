# 1789621028-nothing-reads-a-record-against-the-tree — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     <filled at close>
· evidence: <filled at close>
· verified: <filled at close>

## Why this work exists

A round record is written once and the tree keeps moving; nothing read one
against the other. This work pins a fix range in the record where a generator
writes it and a checker reads it, and closes the two instances of the class
that live inside that generator and the case that guards it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Phase 1's acceptance assumes a green baseline for `tests/test_chain_hooks_hardening.py` | `plan.md` Phases row 1: "`bin/test tests/test_chain_hooks_hardening.py` exit 0 untouched". Executed at `5adaffef`, the frame's own commit: **exit 1**, `test_every_spec_directory_that_reached_the_ladder_has_an_overview` naming `1789621028-nothing-reads-a-record-against-the-tree` | Open `overview.md` before phase 1 and take the baseline from there | The frame wrote `spec.md` and `plan.md`, which is what puts a directory on the ladder, and that case demands the memo the builder owns. The plan's claim was true of the tree the framer read and false of the tree the framer left. Nothing is worked around: the memo was due at the first divergence and this is it |

## Not verified

| Item | Who must answer |
|---|---|
| <filled as they arise> | <who or what can answer it> |

## Not done

<filled at close>

## Fed back into the spec

<filled at close>
