# Survivors — every family no re-read can clear is named, and `--into` refuses a stale date

The builder ran `survivor-check --range e1e54c71..HEAD` over the whole build
before the hand-back. It reported one place, this item's own frame. The
frame quotes the sentence the range removed, and names it as the sentence the
work replaces. None of the six removed sentences survives as a claim anywhere
else. Round 1's fix range, `1640bf9a..HEAD`, reported one more place in the
same frame, the second row below.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/spec.md` | A row corrected by two rows is not a re-read's to clear | this item's frame naming, in its Grounding, the sentence ⬜ 11 replaces; the frame records what was approved, and the quote is what the work changes from |
| `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/spec.md` | W2 (killed at any step) | this item's frame quoting #756's W9 in its Grounding, with round 1's change to it stated in the same row; `survivor-check --range 1640bf9a..HEAD` matched its *killed at any step* to F1's old *at any step* wording, which round 1 corrected, and the frame records what was approved and what changed |
