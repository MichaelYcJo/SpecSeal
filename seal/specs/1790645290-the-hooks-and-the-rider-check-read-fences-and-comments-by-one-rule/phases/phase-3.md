# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — phase 3

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 11f393d8 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 3, the config reader on the walk. `config_rows`,
`refusal`, `unfenced` and `fence_map` read through it, with the fence-only
reading on uncertain lines, so `seal.py#table_span` and `broad_gate.py` follow
without a walk of their own. `broad_gate.py` tells a `Broad gate` line hidden in
a comment from one in a fence, in a new sentence documented in
`templates/config.md` and pinned; `#fence_left_open` and `seal.py#write_row`'s
guard name only a fence the walk sees. `seal.py#HOOK_PURPOSES` and the
copied-alone cases gain the new module. Property half 1 for this reader. C1 to
C14, each marked red failing against `3911a8cf`'s `hooks/config.py`; S6, S7,
S8, S15; S14's corpus measurement. The spawn named work item D (#660) as
landing in `hooks/dispatch.py` meanwhile, to be merged in hunk by hunk.

## What this phase found

- **D landed first, and merged clean** (`e235453a`). Its only interaction is
  a reason, not a hunk: `hooks/dispatch.py` now catches a `SystemExit` at a
  gate's load as well and says the failure at the end of the turn (#28). The
  grounds this branch gave for raising rather than exiting when `blocks.py` is
  missing were rewritten to match, in `hooks/config.py`, the copied-alone
  module's comment and the overview's second divergence row.
- **`hooks/config.py#hidden_lines` is the reading, and `fence_map` its shape
  for the callers.** It returns `{index: "fence" or "comment"}` and the
  opener to name; `fence_map` and `unfenced` keep their names and return
  shapes, so `config_rows`, `refusal` and `seal.py#table_span` changed by
  nothing but what they are shown. Half 1 is `Walk.hidden(base)` with
  `blocks.fence_only` as the base, written once in the walk.
- **Which unclosed fence is named.** The walk's own unclosed openers, and the
  old reading's opener where the walk is not sure of that line. A fence line
  inside a closed comment is therefore never named (S8, C2), and a fence left
  open BELOW such a comment is named even though the old reading would name
  the quoted one above it: `test_the_fence_named_is_the_one_that_hides_the_row`
  holds that, added when the mutation dropping the walk's openers stayed
  green.
- **`broad-gate`'s sentence (Q5's last part):** "written inside an HTML
  comment", the line quoted, "The row is not absent and it is not in a code
  fence: it is commented out, and there is no command to seal over", then
  "If it is the command to seal over, take the row out of the comment and into
  the `| Item | Value |` table", ending "Nothing ran." It follows the fence
  sentence, so a file with the row in both a fence and a comment gets the
  fence sentence, as it did. `templates/config.md` §*What is refused, and what
  stays allowed* gained a paragraph stating the comment rule and the sentence,
  and a case pins both.
- **Seen red against `3911a8cf`** by putting that commit's `hooks/config.py`,
  `broad_gate.py` and `seal.py` in place: exactly the rows the frame marks
  red failed (C2, C5, C6, C7, C8, the commented-row case, S8, S6 on the
  bytes, both S7 shapes), and every row it marks *pins* passed (C1, C3, C4,
  C9a, C9b, C12, C13, C14). The template case failed with the template from
  `3911a8cf`.
- **Mutation, one unit at a time:** uncertain lines given no base reading (4
  red, the property's half 1 among them), the walk ignored (7), the old
  opener always named (1), the walk's openers not named (1 after the case
  above was added), `fenced_row_at` taking either kind (2), no commented
  branch in `missing_row` (2).
- **S14, measured (Q3's config third, answered (a)).** Every tracked `.md`,
  519 files, through `config_rows` and `refusal` at `3911a8cf` and at HEAD: 4
  have config rows, 0 differ.
- **Ledger rows this phase drifts** (`hooks/config.py#fence_map`, `#unfenced`,
  `#refusal`; `broad_gate.py#missing_row`, `#fenced_row`; `templates/config.md`
  headings; the runner and `CONTRIBUTING.md` rows phase 1 drifted) are listed
  by `evidence-check`, and are re-read where they live in one pass once phases
  4 and 5 have drifted theirs.
- **Gate lines, drafted for `CONTRIBUTING.md` §*What a change to a gate must
  carry*.** Seen red: above. Failure direction: the mode gate and `broad-gate`
  read FEWER rows in one family (a row inside a comment that closes), which is
  *nothing is declared*, this module's own direction, and more in one shape (a
  table under a closed comment that quotes a fence line), which a renderer
  shows. `broad-gate` refuses where it used to run a commented-out command.
  Prompt budget: no new question; `mode-gate` asks only where the `Mode` row
  stood inside a closed comment, which is *nobody declared*, inside its budget
  of two per session per repository. Platform: string processing only; CRLF is
  C7; macOS only here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/config.py#fence_map`'s own fence walk | `hooks/blocks.py#fence_only` (the same rule, as the base reading) and `#walk`, through `hooks/config.py#hidden_lines` |
| `broad_gate.py#fenced_row_at` taking the complement of `unfenced` | `broad_gate.py#hidden_row_at`, asking the reader which kind hid a line |
