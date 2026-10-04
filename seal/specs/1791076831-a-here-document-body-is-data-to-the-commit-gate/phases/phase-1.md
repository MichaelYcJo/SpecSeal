# 1791076831-a-here-document-body-is-data-to-the-commit-gate — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | f7b40db8 |
| Ran by | unknown — the spawn prompt did not name it; the orchestrator fills it |

## What this phase was asked

The reader says what each body is. `hooks/cmdline.py` gains a per-body record
(text, quoted, terminated) from `_heredoc_split`'s one pass, and
`drop_heredoc_bodies` and `heredoc_bodies` become views over it with identical
output. Quoting follows R2a, so a `$` in the delimiter word is never quoted. No
gate behaviour changes yet. Before anything is built, see #739's three
refusals red at `101f9bd0`, so the cause is executed and not only read.
`hooks/cmdline_base.py` is never edited.

## What this phase found

**#739's three refusals, executed at the base.** The hooks at `101f9bd0` and at
the frame's head `636ebdb5` are the same bytes (`git diff --stat 101f9bd0
636ebdb5` touches only this directory). A probe drove `commit-review-gate.py`
as a subprocess from an opted-in, undeclared session directory, beside a
declared repository for the third row. All three came back `deny` with the
unplaceable-construct text: row 1 (`python3 - <<'EOF'` appending to a file),
row 2 (`cat > pr.md <<'EOF'` then `gh pr edit` and `gh pr ready`), and row 3
(`python3 - "$F" <<'EOF' && git -C <declared> add f && git -C <declared> commit
-m x`). A body that names the commit only inside single quotes, or only in a
`#` line, was already silent: the shell reading needs the commit in command
position, or inside a double-quoted backtick. So every case in phase 2 carries
one of those two spellings, or it would pass before the fix.

**The record carries two fields more than the spec names.** `heredocs` returns
`Heredoc(text, quoted, terminated, delimiter, dashed)`. R2d needs to know which
opener owns which body, and a count alone can coincide while two openers are
misread in opposite directions. With the delimiter and the dash, phase 2 can
compare each opener's word on the line with the body it claims.

**`_heredoc_word` keeps its signature.** It has a second caller,
`_heredoc_end`, so the quoting is read from the raw span the split pass already
holds (`_quoted_delimiter`), not from a changed return value.

**The two old views are byte-identical.** A probe loaded `101f9bd0`'s
`hooks/cmdline.py` beside the worktree's and compared both views over every
string constant in `tests/*.py` (24,304 strings, 465 holding `<<`), each
string also after `drop_comments` and in three heredoc variants. It found 0
differences.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
