# Survivors — the Windows test leg is measured and cut

`survivor-check --range a9d7b0e5...HEAD` reported two places still carrying
wording phase 4b removed from
`test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing`, whose own move
under a spaced directory went to `a_sealed_run`. Both stand, for the reason
in each row.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | The parent first, so the move is a rename on every platform. | `test_a_run_with_no_session_says_so_and_names_the_hand_command` still moves its fixture under a spaced directory with `shutil.move`, and the comment explains that move there; 4b removed only the pipe case's copy of the move, so the sentence is true where it stands |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | it `shutil.move` falls back to a copy and an `rmtree`, which Windows | the same comment's second line, beside the same move |
| `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/spec.md` | with a `.test_durations` file produced by the Windows leg's own | the framer's interface clause says how the committed file was produced, which is what happened: run 37458654434's `--store-durations` artifact, downloaded with `gh run download` (`phases/phase-3.md`). The round 1 fix rewrote CONTRIBUTING's refresh recipe, not that history, and `spec.md` is not the smith's to edit |
