- **The orchestrator's acts are a table now, and a case holds it from both
  sides.** Every act addressed to the session that spawns agents sits under an
  `Orchestrator:` heading in one of the two orchestration files, and there was
  no list of them — so nobody could say which of them still had to be
  remembered. `skills/implement/orchestration.md` §*Orchestrator: which of
  these acts runs itself* is that list, one row per act against what delivers
  it, and `tests/test_every_orchestrator_act_names_its_delivery.py` fails when
  an act has no row, when a row names a heading no file carries, when a row
  names a command or a check with no file behind it, and when a row reading
  `still a sentence` carries no grounds. The cell answers one question — when
  the orchestrator forgets this act, what notices — and the reading it
  produced corrects the ticket: of the twenty acts, eight are already delivered
  by a check and five by a command, and five are still a sentence. Those five
  are what a next work item picks from. The table has twenty rows rather than
  the nineteen the frame counted, because the section holding it is itself a
  marked heading.
- **`session-cost --post` is the flow-log posting, as a command.**
  `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* wrote
  the procedure out in full — which label to look up, how to tell a repository
  that never made the log from one whose log somebody closed, which of the two
  logs a reading belongs to — and nothing typed it. The mode resolves the
  label, implements every state the prose enumerates, and posts the reading
  with what a person says about it. It refuses without `--says`, because the
  numbers are the script's and the judgment is not; it opens no issue in any
  state; and `--label` reaches the durable cross-version log with the same
  code. A repository that never created the label, and a machine with no `gh`
  on it, both post nothing and fail nothing — that is the ordinary case, and a
  command red there is one people stop running. The command does not make
  anybody run it, and both the skill and the table say so rather than reading
  closed. (#330)
