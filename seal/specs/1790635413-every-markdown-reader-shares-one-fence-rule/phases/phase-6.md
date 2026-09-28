# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 6feed792 |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the segment does not source that value from itself |

## What this phase was asked

`plan.md` phase 6: `hooks/config.py` — the one table generator hides lines
inside a closed HTML comment as well as fenced lines; an unclosed comment
hides nothing. `broad_gate.py` names a `Broad gate` row that stands only
inside a comment. `docs/the-broad-gate.md` §*A fenced example in a config
file is not a config row* gains the comment sentence, and its `Enforced by:`
line names S17's case. Verified by S13–S17, with
`tests/test_the_mode_question_is_asked_once.py` and
`tests/test_the_seal_is_taken_once_by_the_sealer.py` as the neighbouring
modules. Q1 is this phase's to measure and Q3 its to decide.

## What this phase found

- **The generator is a new function, `table_lines`, and `unfenced` stays
  fence-only.** `broad_gate.py#fenced_row_at` takes the complement of
  `unfenced` to find a fenced row. Had `unfenced` started hiding comments, a
  commented row would have been called fenced, which is the #429
  wrong-cause shape the plan names. So `unfenced` keeps its meaning and its
  one outside caller is untouched, and `config_rows`, `refusal` and
  `seal.py#table_span` read `table_lines`, which reads `unfenced` and drops
  what `commented` hides. `seal.py`'s alias moved from `unfenced` to
  `table_lines`.
- **What "a comment that closes" means had to be made exact, and the oracle
  decided it.** The oracle the frame chose is `comment_scan` over
  `blank_fences`, which reports only the state each line BEGINS in. So a line
  is hidden when it begins inside a comment and its run of such lines
  returns to a line that begins outside, or the file ends outside one. The
  one shape where that differs from "the comment containing this line
  closes somewhere" is a comment closed and a new one opened on the same
  line that never closes: nothing in that run is hidden. That is the
  direction toward reading, and the parity table pins it as shape 10.
- **Q1 measured: no shipped shape changes reading.** `seal.py`'s
  `NEW_CONFIG` header comment is the one closed comment among the five
  shapes the question names, and it hides two prose lines above the table.
  `config_rows` and `refusal` answer the same before and after for all five.
  The probe was deleted after the run.
- **Q3 decided:** `commented_row_at`, a sibling of `fenced_row_at`, and an
  arm of `missing_row` after the fence arm. Its sentence is pinned (§14).
- **Two mutations survived the first cases, and two cases were added.**
  `refusal` reading `unfenced` survived S13, because a well-formed commented
  row followed by `-->` ends the walk the same way either way. A commented
  malformed pipe-line is the shape that reaches `refused`, and it kills the
  mutation. `commented_row_at` ignoring `names_this_row` survived S17's
  fixtures, which held only the `Broad gate` line in the comment; one now
  holds a `Mode` row above it.
- **`templates/config.md` gained a paragraph** in §*What is refused, and
  what stays allowed*, because the new refusal points there for the rule.
  It avoids writing a literal comment opener: that template is itself a
  file the comment scan reads.
- **What a gate change must carry** (`CONTRIBUTING.md`): the cases above
  were seen red against `eb06ec3f`. The direction is fewer rows, and only
  where a closed comment hides them. The prompt budget does not grow:
  `mode-gate` asks only where the `Mode` row stood inside a closed comment,
  which is *nobody declared*. The platform-shaped input is line endings,
  and S13 carries the CRLF shape.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal.py`'s `unfenced` alias | `table_lines`, the alias `table_span` reads through |
