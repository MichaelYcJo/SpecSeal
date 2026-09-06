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
  segment readings in the rolling log the section already names. Two rows
  say what they mean rather than leaving it to each run: a **record** is
  anything under `seal/` — the work item's documents, the ledger and its
  fragments alike — which is the review chain's own definition and what both
  the `Location` buckets and the share row count by, and the **broad gate**
  row asks whether the gate ran and at what SHA, which is what the cell it
  reads actually carries. And the section says which file of a project
  directory is a run's main transcript, because `--latest` takes the newest
  file anywhere beneath it and on a run with segments that is usually a
  segment. (#170)
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
  moved, and the printed report names each count's own scope so the two
  cannot be divided into each other. **No way this degrades ends the report**
  — an unopenable transcript is skipped, an unparseable line dropped, a field
  a harness stops writing contributes zero, and a value that is not a number
  counts as none. Almost every one of those makes the totals smaller; the one
  that goes the other way is a split message whose rows carry no usable key,
  counted once per row instead of once. So the line prints both counts: the
  transcripts it opened, which the same report's `Agent` call count is the
  cross-check for at 18 against 17 on a real run, and the turns, which is
  where a doubled run would show. Seen red first: each of the four new
  behaviours against the old script, and the guard for a transcript that
  cannot be opened pinned by a case calling `token_totals` directly, after
  mutation testing showed a directory fixture never reaching it. Prompt
  budget: zero. (#170)
- **A transcript that only read and thought reports what it spent.** The
  token line was summed after the no-tool-calls guard, so a transcript
  carrying `usage` and no paired tool call exited 1 with an empty stdout —
  and that transcript is a segment, which is exactly what the table's
  per-kind token row is summed over. It now prints the token block and says
  why there are no time lines. A transcript with neither still exits as it
  did. (#170)
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
