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
