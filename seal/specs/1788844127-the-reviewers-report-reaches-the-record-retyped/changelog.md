- **The reviewer's report reached the record retyped, and now it reaches it as
  a file (issue #228).** `round_record.py new` took `--report <path>`, and the
  reviewer's report was not a path: the warden returns it as its final message
  and the orchestrator is told not to open the agent transcript, so the report
  existed in a transcript nobody may read and in chat text, and the
  orchestrator typed it into a file to have something to pass. Four rounds of
  one work item in another repository, four retypings; 0.9.0's own #190 · #207
  run retyped rounds 2 and 3 by hand. A retyped verdict row carries retyped
  coordinates, re-review inheritance carries the paraphrase into the next
  round, and `Fixes checked by` then names a round whose report is not the
  report the reviewer wrote.

  **The warden writes its report to
  `seal/specs/<work-item-id>/rounds/round-<n>-report.md` and returns that
  path**, and **`round_record.py new` reads that path when `--report` is
  absent**, derived from `--item` and `--round` — the same pair `round-N.md`
  itself is derived from, so the reviewer and the generator cannot spell it
  differently from each other. The flag stays and it still wins: a round whose
  report predates the convention, and a round that ran more than one reviewer,
  both need it. Where neither the flag nor the file is there, the run refuses
  and the message names the path AND the convention that fills it — a derived
  path with no sentence beside it reads as a mistyped argument, which is the
  one thing it cannot be.

  **The fixer side already had this shape**, `rounds/round-<n>-fixes.md`, so
  this is the missing half of a convention rather than a new one.

- **The record and the report are told apart, in the three documents that used
  to carry only the prohibition.** *The reviewer writes no round record* and
  *the reviewer writes nothing under the work item* had become one sentence,
  which is why the missing half above read as forbidden rather than as absent.
  `agents/warden.md` now says the record is `round_record.py new`'s, written
  after the orchestrator verifies the findings, and the report is the
  reviewer's own artifact — the thing the contract's §6 already calls its
  final output, in a different medium and with no more authority. It is still
  uncommitted, still unverified, and still inert until the orchestrator acts
  on it.

  `skills/agent-contract/SKILL.md` is unchanged. §6 says an exception *"is one
  agent's, and it is named in that agent's definition — never here"*, so the
  permission is written in `agents/warden.md` beside the rule it excepts —
  the clone rule, which is what actually forbade the write and is a section
  above the one that looked like it did.

- **A record is selected by name, never by directory membership
  (`docs/review-handoff-protocol.md` §Layout).** `rounds/` holds three files
  per round beside the record — the report, the round paragraph, the fix
  table — and the layout diagram read as an inventory of the directory. Two
  readers in this repository took membership for record-ness and each raised
  `TypeError` on sorting two `None`s rather than failing an assertion. The
  report itself stays implementation, like the parent path: the protocol
  requires a record, and a conforming tool whose reviewer writes `round-N.md`
  directly needs none of the three.
