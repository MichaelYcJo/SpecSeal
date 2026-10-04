# 1791090072-the-three-wave-one-items-read-each-other-after-the-squash — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show, each part written when it happened. -->

📋 implement applied
· spec:     docs/the-evidence-ledger.md §*A released row is read again in the branch's fragment*; docs/the-record-layout.md §*A change writes fragments, never a shared file*; CONTRIBUTING.md §*What a contribution is not asked for* and §*House rules*; routing.md
· evidence: seal/ledger/1791090072-the-three-wave-one-items-read-each-other-after-the-squash.md, three `Re-read ·` rows
· verified: `evidence-check --strict .` 0 drifted and 0 broken, the three named test modules green, `fold_ledger.py --check` naming only the four unfolded fragments (executed); each claim against the merged code (read)

## Scope confirmation

Re-read the three released claims whose units #756, #757 and #758 edited in each other, into this chore's own fragment, and change no code.

## Why this work exists

After the three wave-one items of 0.18.1 squashed, no reading recorded what `fake_venv`, `VERSIONS_OF_ANOTHER_PRODUCT` and `templates/config.md` hold, so `evidence-check --strict` read 10 rows DRIFTED. Each claim holds against the merged code, and the strict reading is clean again.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the re-read is written | 0.18.0's integration chore (#742) re-stamped the siblings' fragment rows in place / this chore wrote one `Re-read ·` row per released root into its own fragment, with `--reverify --into` narrowed by `--ledger` to the three drifted release files | its own fragment | #742 repaired citation hashes, where `docs/the-evidence-ledger.md` says "re-stamp that fragment's row in place". Here the fragment rows cite released rows correctly and only their code coordinate is stale. A row of the same family dated the same day joins the union ("readings that tie on that date are a union"), so the siblings' rows stay as their authors wrote and dated them, and none of them is made to claim a reading its work item did not take |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the whole repository | the sealer, in its one broad run before the pull request is marked ready |

## Not done

No `changelog.md`. Nothing a user runs changes, and no document asks a chore for one; #742, the same shape at 0.18.0, wrote none.

## Fed back into the spec

None.
