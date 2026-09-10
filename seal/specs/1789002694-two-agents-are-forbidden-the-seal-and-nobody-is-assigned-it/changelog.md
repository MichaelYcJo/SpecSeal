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
  run was taken against, the suite's own counts, the exit code your `Broad
  gate` row came back with, the evidence ledger as `N ok · 0 broken`, the
  chain check, and how many review rounds the work item ran. **It never says
  a linter was clean**, because the row is one shell line and nothing in it
  says which part is a linter — a seal that asserted one over a row with none
  in it would be the counterfeit the `verify` skill exists to refuse. The disc is computed from a counted-stitch chart rather than
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
  refuses before writing anything when a finding is still open in the last
  record's verdict table, or when the run was taken before the round it would
  seal. `close --broad-gate` still works for the one pass where fixes and the
  gate land together. (#30)
- **A review run that ends at its cap can now be sealed, and could not
  before.** The review chain is bounded — three rounds, five while a red
  finding is open — and a run that reaches the bound closes what is left by
  deferring it, to an issue or to the follow-up list. That produced a state
  with no way out: the record's `Pass` box came out checked, because deferring
  a finding closes it, while the reviewer's own `Needs a fix` line still read
  `yes` from when the round was running, and nothing rewrites what the
  reviewer wrote. The seal refused on that line, so the cell recording the
  broad run could not be written, and the pull-request check then failed the
  branch for a missing cell nothing was able to write. Two rules of the
  workflow contradicted each other, over exactly the case the cap exists for.
  **The seal now asks the verdict table instead of the reviewer's line**: a
  record with nothing still open has ended its run, however the round felt
  while it was running. The other two refusals are unchanged, and the message
  a person sees when a finding really is open now says which of the two rows
  was read. (#30)
- **"After the rounds settle" now names the row a machine already reads.** A
  work item has build phases with a progression of their own and a review
  chain with its own rounds, so the phrase named neither and every reader had
  to guess which. The condition is the last round record's `Pass` box, checked
  — nothing in its verdict table still open — and the `verify` skill states it
  with the reason the box is the row rather than `Needs a fix`. The two agent
  definitions that act on it, the sealer's own definition and the review
  orchestration skill each name the row and point at that section. The proof
  block's `broad gate` line asks for the same thing. (#30)
- **One word named three different things, and now every reference says
  whose.** `seal` meant the mark recording that a review happened, the stamp
  the broad gate prints, and a smith's own proof block — the first two in the
  two agent definitions a reader opens side by side. The rule that resolves it
  is not fewer seals: **every agent seals what it verified, and the one seal
  over the whole project is the sealer's.** The `verify` skill states that and
  names the two things that already tell the final one apart — it covers a
  tree nobody is still editing, and it is the only seal that is drawn, which
  is why the picture prints on success alone. The warden's definition now
  names what it actually keeps, the review mark, and the rule that a document
  naming a thing more than one party can have says whose is written down in
  the `writing-style` skill, so the next such word does not need its own
  conversation. (#30)
- **The rule now names its owner everywhere it is stated.** It stood in nine
  places saying the run was the orchestrator's, or saying only who was
  forbidden it: two agent definitions, `CONTRIBUTING.md`, the review-chain
  specification, the handoff protocol, the review orchestration skill, the
  `verify` skill, the round-record template, and the suite runner —
  both the `bin/test` wrapper and the module it runs, which are one command
  and were two owners until round 1 found the second. All of them now say
  the sealer's and name the definition that assigns it.
  Two more places were not documents at all but the failure messages the
  chain check prints at a refused pull request — the one place a person
  actually reads the instruction — and both now say to spawn the sealer
  instead of telling the reader to take the run by hand. Both agent
  definitions also gained the distinction the rule needed: **asking whether
  anything already covers a case is a coverage probe, not a seal.** Run it,
  and report it as a probe. (#30)
