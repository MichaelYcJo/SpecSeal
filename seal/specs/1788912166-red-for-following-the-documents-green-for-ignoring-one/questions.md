# Questions: red for following the documents, green for ignoring one

The routing batch was answered before the first edit: `smith` implements, the
chain reviews, the pull request opens. What follows are assumptions taken
under that answer, and one question that is the owner's.

| # | Assumption | Why it does not wait |
|---|---|---|
| 1 | The whole-range row in `survivors.md` is a table row like the per-survivor ones, with the range in the first cell and the grounds in the second | It is a format inside a file only this check reads. Changing it later costs one parser and one case |
| 2 | The eighth cutoff is named for what it gates rather than for its position, and it is set to this work item's own id | The seven before it are named that way. Setting it to this id means the first work item it applies to is the next one opened, which is the shippable direction `chain_check.py:127` argues for |
| 3 | `Broad gate`'s existing free-text values are read leniently: `not yet` is matched exactly, anything containing a SHA-shaped token is a run, and anything else is reported rather than failed | No code validates the cell today, so records in the tree may hold anything. Failing on an unparseable cell would be the retroactive red the cutoff exists to avoid |

## Q4 — should the `Broad gate` cell be validated where it is written?

**The owner's.** Nothing validates it today, and after this work something
reads it. Two answers:

- **Validate at write.** `round_record.py` refuses a `--broad-gate` value that
  is neither `not yet` nor a SHA and a base. The cell then means one thing
  everywhere, and the reader needs no lenient path.
- **Leave it free text and read leniently**, which is assumption 3. A session
  can write what it knows, and a cell nobody can parse is reported rather
  than fatal.

It does not block: assumption 3 is the reading either answer permits, and
validation would be additive. It is recorded because a cell that something
now depends on has stopped being decoration, and that is a change worth
somebody noticing.

## Not asked, because a document already answers it

Whether `orchestration.md` should move the pull request after round 1. A
reviewer needs a pull request to review, the round record has a `PR` cell to
fill, and the check is the thing that is wrong. `spec.md` §Scope records it as
out.
