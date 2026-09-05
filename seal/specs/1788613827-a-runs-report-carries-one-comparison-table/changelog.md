- **A run's report carries one comparison table, and the row nobody can
  produce by hand comes out of one command.** #161's run summed `usage` over
  its transcript and its subagents with a script written for that occasion,
  and a number summed one way this run and another way the next is worthless
  to compare against. `skills/verify/SKILL.md` §*Measure the segment, and
  feed the flow log* now states the run-level table: nine rows — rounds, wall
  clock, commits by kind, findings by severity, findings by `Location`, the
  records' share of the diff, model turns with the three token columns,
  segments per kind, and the broad gate — each with the cell saying where its
  number is taken from. Three sentences ship with it, each pinned by a case:
  the tokens are counted rather than estimated and counted the same way every
  time, naming the command and all three `usage` fields; a comparison against
  a run whose transcript covered only part of its branch says so in the prose
  rather than as a column, because a column would make it a field and there
  is no reader for one; and the table carries **no verdict** — what a row
  meant on one branch goes in the comment beside it. The rows name no issue
  number and no milestone, so the section still ships to repositories that
  have neither. It is **not a third destination**: the table joins the
  segment readings in the rolling log the section already names. (#170)
- **`session_cost.py` prints the token line, over the whole run rather than
  the transcript it was handed.** The script already opened exactly those
  files and already read `usage` — it threw away everything but
  `input_tokens` and `cache_read_input_tokens`, and it read one file where a
  run has several. It now sums `output_tokens`,
  `cache_creation_input_tokens` and `cache_read_input_tokens` over the given
  transcript **and** every `*.jsonl` under the `<session-id>/subagents/`
  directory beside it, always and behind no flag, and reports the same under
  `--json` as a `tokens` object. A message's usage counts once however many
  rows it is split across, which is the trap the existing `context_growth`
  dedup already exists for. **Two turn counters, on purpose**: a turn here is
  an assistant message carrying `usage`, where `tools_per_turn`'s denominator
  is a message carrying a tool call — the per-segment bars in
  `docs/review-handoff-protocol.md` are calibrated against that ratio, and
  widening it would move a published threshold with nothing saying it had
  moved. The script's own docstrings carry both halves. **Every way this
  degrades prints a smaller number rather than raising** — an unopenable
  transcript skipped, an unparseable line dropped, a field a harness stops
  writing contributing zero — so the line also says how many transcripts it
  covered, and that count is what a reader holds it against; the same
  report's `Agent` call count is the cross-check, measured at 18 against 17
  on a real run. Seen red first: each of the four new behaviours against the
  old script, and the guard for a transcript that cannot be opened pinned by
  a case calling `token_totals` directly, after mutation testing showed a
  directory fixture never reaching it. Prompt budget: zero. (#170)
- **The two documents that carry the table point at its owner instead of
  copying its rows.** `docs/review-handoff-protocol.md` §*After the run — the
  per-segment bars* says the bars judge a segment against its kind and the
  table judges a run against the last run measured — a reader who met only
  the bars had no way to know the second instrument existed — and names the
  owning section by file and heading. `skills/commit-pr-convention/SKILL.md`
  §*Pull request bodies* states the chain section's shape for a work item
  routed through the review chain: the comparison table first, then what the
  rounds found, so a reader who stops after the first screen still has the
  numbers. PR #162 wrote that section as prose and PR #168 as a table, which
  is the whole of what a fixed set of rows buys. Both refuse the rows
  themselves, and the refusal in
  `tests/test_the_chain_section_has_one_shape.py` is itself held to the
  owner's current wording — a row renamed in `skills/verify/SKILL.md` turns
  `test_the_pinned_rows_are_the_owners_own` red rather than leaving a green
  case guarding a string nobody would paste. Eleven mutations over the two
  paragraphs, nine of them because the first red proved only that the
  paragraph was absent: a case red because its subject does not exist has not
  been seen red for its own reason. (#170)
