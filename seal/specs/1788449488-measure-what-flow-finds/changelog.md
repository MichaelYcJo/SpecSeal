- **Measuring a smith or warden segment and logging what it found is now
  automatic, in every repository this plugin installs into, instead of a
  message a person had to remember to retype.** Issue #109: the instruction
  used to live only in one operator's own memory file, naming a fixed issue
  number that went stale twice. `skills/verify/SKILL.md` gains "Measure the
  segment, and feed the flow log" — after every segment, find this
  repository's open `flow-measurement`-labelled issue
  (`gh issue list --label flow-measurement --state open`) and post
  `session_cost.py`'s numbers to it; where no such issue is open (nearly
  every installed repository, today), the step is a no-op — nothing is
  measured, nothing is posted, nothing asks. A new
  `.github/scripts/roll_flow_measurement_issue.py`, wired into
  `close-issues-on-release.yml`, closes the current log and opens the next
  one — titled with the release's version bumped to the next minor — every
  time a release reaches `main`, so the log keeps growing without anyone
  opening the next issue by hand. This repository's own log (`#89`) is
  labelled as part of this change, so `0.8.0`'s issue opens on this
  repository's own next release without further action.
  **The rollover script retries once before treating "no issue open" as the
  invariant broken**, not on "more than one open": a search-index lag right
  after a label write can only ever undercount what is actually open, never
  overcount, so only a zero reading gets a second look. Found while building
  the label bootstrap in this same branch — `gh issue list` returned empty
  immediately after `gh issue edit --add-label`, while `gh issue view` in
  the same breath showed the label already applied.
  **Filed separately, out of this branch's scope: `agents/smith.md`'s
  mutation-testing instruction says to clear `tests/__pycache__` between
  mutations, and that is not the only cache a mutated module can leave
  behind** — a script loaded from `.github/scripts/` by path, the way this
  branch's own new tests load the file under test, caches its bytecode under
  `.github/scripts/__pycache__` instead, and a stale copy there survived one
  mutation's restore long enough to fail an unrelated later test run.
  `docs/flow.md`'s "While the flow runs" section — the instruction this work
  replaces — is deleted, and the two boxes it names as done (`#121 + #119`,
  `#109` itself) are ticked. (#109)
