# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | af54c461 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 5: retire the scale from `seal_stamp.py`, `broad_gate.py`,
`hooks/sealer-stamp.py` and `docs/the-broad-gate.md` as `spec.md` Scope 5
lists — the eight names and `check_scale`, `build()` with no argument,
`compose(rows, disc)` and `stamp(rows, shape, disc)`, `admitted` over two
rungs with the owner's one-per-`Stop` rule whole, `read_values` ignoring a
`scale`, `--scale` off both commands, the gate writing no `scale` — and make
a malformed chart a refusal at the gate's `load` (Scope 6). Before the first
edit, capture what the stamp drew at 5623d728 over `SAMPLE_ROWS`, in both
forms, for a byte-for-byte case. Cases S13 and S14; the parametrised scale
cases collapsed and the five scale-only cases retired (Q-W3); the
`read_values` tolerance pair.

## What this phase found

**Q-W3, the capture.** Taken before the first edit to `seal_stamp.py`, by a
scratch script loading `git show 5623d728:skills/verify/scripts/seal_stamp.py`
beside its `seal-mark.txt` and hashing, SHA-256 cut to sixteen hex digits:
`stamp(SAMPLE_ROWS, 0.9, False)` (block form), the same with `shape=True`
(the twin), `stamp(SAMPLE_ROWS, None)` (no disc), and `fitted` over two
blocks labelled `first` and `second` at the default budget, at twice one
block's size plus 10 (both with their disc) and at 50 (the first alone, no
disc). Both forms were taken, as the default answer said; hashes rather
than whole drawings, because the block form is several kilobytes of colour
codes and a sixteen-digit hash fails on any byte. The same script over the
retired module gave the same six hashes, and
`test_the_stamp_draws_byte_for_byte_what_it_drew_at_the_default_scale` pins
them. It is green at 5623d728 in substance and red there only because the
old call spelling differs, so it was seen red by mutation instead: `GAP = 3`
made 4 turned it red.

**`admitted` is simpler than a ladder with one rung.** With one rung the
second pass of the old `admitted` — try each block at a higher rung the
others leave room for — could only ever retry the drawing it already had,
because every scale drew the same disc. It went; the first pass is the rule
whole: as many of the oldest blocks as fit with their disc, and the first
alone with no disc where none fits. The six hashes, including the three
`fitted` ones, are the evidence nothing moved.

**Q-W3, the cases.** Collapsed to one case each: the twin/block width case
(five scales → with and without the disc), the hash-seed case (three
scales → the one disc), the lighting case and the 28-cell case (three
scales each → one). Retired: the NaN refusal, the floor-and-ceiling
refusal, `test_a_file_at_a_scale_the_band_refuses_is_left_pending`,
`test_the_default_scale_is_ninety_percent_with_its_reason_beside_it` and
`test_both_commands_draw_at_the_default_scale_when_given_none`. Replaced
by: the byte-for-byte case; `test_no_scale_is_left_to_ask_for` (no `SCALE`
name and no `check_scale` in the module, `--scale` refused by both
commands' parsers, neither help naming a scale);
`test_the_stamp_says_why_it_has_no_scale_and_neither_command_offers_one`
(the retirement comment); the tolerance pair,
`test_a_values_file_draws_whatever_scale_it_carries` (no key, 0.9, 0.5, a
word, null) and `test_a_file_an_older_gate_wrote_with_its_scale_is_drawn_by_the_hook`.
`test_the_ladder_steps_down_in_order_and_ends_with_no_disc` keeps its name,
which `docs/the-broad-gate.md` cites, over the two rungs; its scale-only
assertions (a file at 1.0 or 0.75 drawn at its own rung) went with the
scale.

**`load` refuses with the gate's prefix.** The refusal reads `broad-gate:
<path> will not load, so nothing ran: <the sibling's sentence>`, so
`CHART_MALFORMED`'s sentence reaches the person whole, with its own path,
after a line that says which file would not load and that nothing ran. A
sibling raising with no sentence is named by its type. `main` loads the
stamp before it parses arguments, so the refusal precedes the redirect, the
check and the worktree; S14's case asserts no kept output and one worktree
for both `broad-gate` and `broad-gate --preflight`.

**One sentence of `docs/the-broad-gate.md` gained the window.** The
unchecked paragraph that already lists where the hook is silent now names
the hook older than #853, which refuses a file without a `scale` and leaves
it pending until the plugin updates, before the sentence saying every
`SEALED` line names `seal-stamp --from`.

Shown red: at 5623d728's stamp, gate and hook, thirteen of the fourteen
new and re-aimed cases failed; the one that passed is the tolerance case's
`0.9` parameter, which the old reader drew too. Mutation: the disc always
drawn, the no-disc fallback dropped or drawn with the disc, the budget
check skipping rather than stopping, the blocks drawn without their disc,
`load` catching too little or naming no type, the hook's block carrying a
`scale`, and the gate writing `"scale": 0.9` were each red through
`bin/mutation-check`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `SCALE_FLOOR`, `SCALE_CEILING`, `DEFAULT_SCALE`, `SCALE_LADDER`, `SCALE_REFUSED`, `SCALE_NOT_A_NUMBER`, `SCALE_TOO_LARGE`, `check_scale` | none: the disc has one size; the comment where they stood says so |
| `--scale` on `seal-stamp` and `broad-gate`, `drawn_from`'s and `signal`'s scale argument, the values file's `scale` field | none; a file that carries one draws, the key read as nothing |
| `admitted`'s second pass over higher rungs | `admitted`'s one pass: with the disc, or the first alone without |
| the five scale-only cases and the scale parameters | the byte-for-byte case, the retirement cases and the tolerance pair |
| a traceback as the gate's answer to a malformed chart | `load`'s `Refused`, exit 2 |
