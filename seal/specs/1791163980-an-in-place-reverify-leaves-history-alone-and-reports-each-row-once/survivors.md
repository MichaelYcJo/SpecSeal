# Survivors — an in-place `--reverify` leaves history alone and reports each row once

This range moved the tree of
`test_a_coordinate_left_and_then_read_unchanged_records_nothing` into a helper
that two cases share, so its docstring's description of the tree moved with
it and was reworded. The places below share words with the sentences that
moved, and each is true as it stands.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check-2.md` | A walk can leave a coordinate and a later walk read it unchanged. | the 0.18.2 item's second verifying pass, quoting the case it proposed in its paste-ready fix; a record of that pass, and the tree it describes is the one `left_then_unchanged` now builds |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check-2.md` | Two walks find the quoted hash gone and leave X1, the third reads it unchanged, and the file ends where X1's hash says. | the same paste-ready fix; the walks it describes are still what that tree does, and `left_then_unchanged`'s docstring says the same in its own words |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | The line the fix prints for a claim tie reads `N places, none holding the recorded content — left`. | the verifying pass over #808's fix, describing the line at `1c3178a1` that #810 then corrected; a record of what that tree printed |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | --reverify at 1c3178a1: src/service.py#handler>"y = x"  2 places, none holding the recorded content — left | the same pass's executed output at `1c3178a1`, quoted as run; true of that commit |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | `2 places, none holding the recorded content — left`, BROKEN part | p1 is a two-place coordinate no place holds, which is not a tie, and its wording is unchanged by #810: `2 places, none holding the recorded content` is still true there |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | a claim whose minor content two or more places hold is named | the pass's verdict row for the finding #810 fixed, stating the defect as it stood at `1c3178a1` |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | 3 places, none holding the recorded content — left" in out, out | a removed line in the pass's paste-ready diff, which #810 applied; a diff shows the old line by construction |
