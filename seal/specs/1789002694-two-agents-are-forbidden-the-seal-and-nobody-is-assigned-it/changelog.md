<!-- seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A fourth agent, `sealer`, takes the one broad run that two agents were
  forbidden and nobody was assigned.** The rule that the full suite runs once,
  after the review rounds settle, has been in this plugin since the beginning,
  and it named who must not run it without ever naming who must: `smith` and
  `warden` are both refused it by the contract's §2, and the act fell to
  whoever happened to be orchestrating. The sealer's whole procedure is one
  command. It reads nothing of the work item — not the specification, not the
  code — runs the checks in order, reads the full output, reports it under the
  three labels, and writes one cell. It judges nothing: a failing check comes
  back with its own lines and no cause and no suggested fix. Its only
  preloaded skill is `agent-contract`, which makes it the smallest payload of
  the four agents at 20 KB, against `smith`'s 99 KB. (#30)
- **A green run prints a seal, and the numbers you need are printed beside
  it.** On success `broad-gate` draws a wax seal — a lily on a disc inside a
  twisted rope — with a panel of readings next to it: the tree and the base the
  run was taken against, the suite's own counts, the linter, the evidence
  ledger as `N ok · 0 broken`, the chain check, and how many review rounds the
  work item ran. The disc is computed from a counted-stitch chart rather than
  drawn as text, so it cannot come out lopsided, and it is emitted with colour
  only where a colour changes. **Where the terminal cannot draw half-blocks —
  a Windows console on a legacy codepage, or any pipe, which is what an agent
  reads through — the same disc prints as letters** at the same width and
  height, so nothing is lost and nothing arrives as question marks. `--shape`
  asks for the letters anywhere, and `bin/seal-stamp` draws one so you can see
  it. **A failing run prints no picture at all** — the words `NOT SEALED`, the
  tree and base, and each failing check with its first lines. (#30)
- **`broad-gate` is a command, where the broad run used to be a command
  assembled from memory each time.** It runs your repository's own broad
  command first, then the four checks every opted-in repository carries —
  the evidence ledger, the unverified-row tally, the review-chain check and
  the survivor check — reading each exit code directly and keeping each
  output in a file. **When a test fails it re-runs only the failing files at
  the base commit**, in a scratch worktree it removes afterwards, and labels
  each failure `new` or `failing on base too`, so a failure that predates the
  work is named as one rather than chased. **Your broad command comes from a
  new `Broad gate` row in `seal/config.md`**, one shell command line, and its
  absence is a refusal rather than a default: `broad-gate` names the row to
  write and exits without running anything. A default would seal a repository
  that runs something else, which is exactly the counterfeit the `verify`
  skill exists to refuse. Put your suite runner first in the row — that is
  what the base comparison re-runs. (#30)
- **`round_record.py seal` writes the broad gate's cell, and it exists because
  `close` could not write it twice.** The cell recording the run has always
  been set by `close --broad-gate`, which also applies a round's fix table —
  and once that table has been applied, `close` correctly refuses to take it
  again, because a second pass would overwrite verdicts the reviewer had
  closed. That left one real situation with no route through it: CI found
  three failures after the gate had already run, the gate had to be re-taken
  at a later commit, and the only way to write the new value was to hand
  `close` a fix table with a header and no rows — which nobody would think to
  do. `seal` is that path with a name. It takes no fix table, reads no verdict
  row, changes the last record's `Broad gate` cell and nothing else, and
  refuses before writing anything when the rounds have not settled, when a
  finding is still open, or when the run was taken before the round it would
  seal. `close --broad-gate` still works for the one pass where fixes and the
  gate land together. (#30)
- **The rule now names its owner everywhere it is stated.** It stood in nine
  places saying the run was the orchestrator's, or saying only who was
  forbidden it: two agent definitions, `CONTRIBUTING.md`, the review-chain
  specification, the handoff protocol, the review orchestration skill, the
  `verify` skill, the round-record template and the runner's own comment.
  All of them now say the sealer's and name the definition that assigns it.
  Two of the places were not documents at all but the failure messages the
  chain check prints at a refused pull request — the one place a person
  actually reads the instruction — and both now say to spawn the sealer
  instead of telling the reader to take the run by hand. Both agent
  definitions also gained the distinction the rule needed: **asking whether
  anything already covers a case is a coverage probe, not a seal.** Run it,
  and report it as a probe. (#30)
