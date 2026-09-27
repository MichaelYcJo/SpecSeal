# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d66b9f8 |
| Ran by | unknown — the spawn prompt named no agent or model for this record; the orchestrator may fill this row |

## What this phase was asked

#624. `isSidechain` refused unless it is literally `false`, with copies 7–10.
The switch ladder's tracked-changes row given a lead conditioned on what was
measured, with copies 11–12. The `[worktree-ok]` row's opening reworded to
*can be shown to be working*, with copies 13–14. Cases S7–S9 in both
languages: S7 red with `is True` restored, S8 red at the base, S9 red with the
old wording. The paste-ready code for #624.1 and #624.3 from round 2 of work
item 1790381327.

## What this phase found

**The frame holds.** Both paste-ready fixes landed as written. #624.2 had no
paste-ready code, and `spec.md` decision 6's shape was enough: the lead is
*Single-stream tree* where nothing idle was counted and detection was
reliable, and *[shared-tree-ok] carries the user's answer to switch in this
shared tree* in the other two states that reach the row. The listing, the
phantom note and the verdict are the same bytes in all three.

**Single stream is `not idle and reliable`, and M8 is why both halves are
there.** A lead chosen from `reliable` alone printed *Single-stream tree* for
the only-idle state, and S8 caught it.

**Seen red.** S7, S8 and both S9 cases were run before any hook was edited,
and all four failed: S7 read `"true"`, `1`, `None` and an absent field as
consent under `is True`, S8's idle row opened *Single-stream tree* and named
no token, and S9's two cases found the old sentence.

**S7 gained a `False` row that the paste-ready version lacked.** Without it,
a reader that refused every entry would pass the widened case. It is also
what separates M5 from M6 below.

**Mutations**, from the committed bytes at `41b1bf9`, restored from a copy,
run over the three narrow modules and `tests/test_worktree_guard_signals.py`:

| Mutation | Red |
|---|---|
| M5 — `is True` restored | S7 alone |
| M6 — every entry refused | S7 and the eleven routing-answer cases that read a real answer |
| M7 — the row-3 lead always *Single-stream tree* | S8 alone |
| M8 — single stream judged from `reliable` alone | S8 alone |
| M9 — the old English `[worktree-ok]` sentence | both S9 cases |
| M10 — the old Korean `[worktree-ok]` sentence | both S9 cases |
| M11 — the Korean token lead replaced by the old lead | S8 alone |

**Copies the sweep found beyond the list.** None in code or policy.
`seal/specs/1790381327-…/overview.md` says *a result marked `isSidechain:
true` is refused*, which was true of that work item when it closed. It is a
record of the past and is left alone. `seal/releases/0.15.5.md` A1 is copy 9,
which phase 4 corrects with the other ledger rows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `isSidechain … is True` and its comment | `is not False`, with the comment the paste-ready fix carried |
| *No other Claude session is working in this tree, but* (both languages) | *No other Claude session can be shown to be working in this tree, but* (both languages) |
| *not marked `isSidechain: true`* in `docs/worktree-guard-spec.md` §*What exactly is read* | *carrying `isSidechain: false`*, same place |
