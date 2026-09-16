<!-- seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The routing question moves to the framer, gains the answer people most
  often want to give, and is checked at the pull request.** Three issues were
  one question seen from three sides: who asks it (#419), what shape it takes
  (#88), and what checks that the answer was honoured (#399). Built apart, the
  same question would have been edited three times and the last built against a
  moving target — which had already happened once, when #399's first framing
  keyed a check on a path floor and two phases were thrown away.

  - **The question is now two questions in one `AskUserQuestion` call**, which
    is still one wait. Question 1 offers `automation` — every party runs and
    nothing stops to ask again — `per axis`, and `no work item`. Question 2 is
    four checkboxes, meaningful only under `per axis`. The answer given most
    often is one click where it used to be three ticks.
  - **The exit names what it turns off rather than where it ends.** The rule
    came from a measured instance: the owner read `straight to the PR` as *call
    no agents at all*, where in the tree that answer turns off `warden` alone.
    So each box now states its UNCHECKED meaning — *this session writes the
    code*, *nothing reviews this code before the pull request*, *the branch is
    handed back, committed and unpushed* — because that is the half a label
    cannot say. The `Review` row's value is unchanged: 16 committed
    declarations carry it, and renaming it would send the commit gate back to
    asking on every one.
  - **`routing.md` records whether the run was allowed to stop and ask**, in a
    new `Automation` row, and **which answer was pressed**, in `Answer
    pressed`. Without the second, a pressed preset and four boxes ticked by
    hand are the same bytes. Both are optional and both read as *never asked*
    when absent, so all 84 declarations already committed parse unchanged.
  - **The session that spawns the work asks it, and the framer asks nobody
    anything.** `agents/framer.md`'s acts become *gather, judge, plan*: what
    the repository can answer, the framer answers, with the grounds where a
    reviewer can open them, and `questions.md` becomes the residue — every row
    owing a reason the tree could not answer it. What it does **not** do is put
    a question to a person: **no agent this plugin spawns has
    `AskUserQuestion`**, so a framer told to ask would be told to call a tool
    it does not have, and a framer told to write `routing.md` would write an
    answer nobody gave. A framer that arrives to a missing declaration reports
    it. A case sweeps every `agents/*.md` and refuses any line naming that tool
    outside the sentence that says no agent has it.
  - **`agents/smith.md` puts down three acts three other documents already gave
    to somebody else** — the design gate, the routing batch and the `routing.md`
    write. It also loses the sentence telling it that a missing frame proves
    none was owed; that inference is not sound, and where `routing.md` declares
    a framer and no `spec.md` is there, `smith` now stops and says so.
  - **The framer leaves a mark in the tree**, one line at the foot of
    `spec.md`, because the existing framer mark lives in the git dir and a git
    dir does not travel to CI.
  - **A work item that declares a framer and draws no frame is refused at the
    pull request.** `chain_check.py` compares the declaration against the
    frame — nothing is re-judged and nothing is counted. What the arm cannot
    see is written in the module beside it, in seven items, because the day
    somebody reads a green run as evidence that a framer ran, that list is the
    only thing standing between the reading and them.
  - **The broad gate gets a home where no round record exists.** A work item
    declaring `straight to the PR` still owes the one full-suite run — that
    answer turns off the reviewer, not the sealer — and the cell had nowhere to
    live. It now lives in `seal/specs/<work-item-id>/broad-gate.md`, written by
    the same subcommand and read by the same reader.
  - **Two arms grandfather work begun before the rule existed**, each on the
    mechanism the broad-gate arm already used, and each measured first: 10 of
    the 11 work items declaring a framer carry no mark, and not one of the 16
    declaring `straight to the PR` carries a seal file.

- **A check over agent definitions refuses an instruction no agent can carry
  out.** No agent this plugin spawns has `AskUserQuestion`, so a definition
  telling one to collect what a person must answer is an instruction nothing
  performs. Two cases hold it: one refuses any `agents/*.md` line naming that
  tool outside the sentence saying no agent has it, and one refuses collecting
  *in one batch* where the surrounding words are about a person answering.
  **Batching reads is a different thing and is not refused** — that is what
  `agent-contract` §10 asks every agent for, and the check decides by what the
  sentence claims rather than by the phrase it uses.

- **Personal instructions: re-run `install.sh` after updating.** The routing
  paragraph in the `<!-- specseal:start -->` block changed with the question,
  and an installed copy follows only when the installer runs again. Until then
  a session reading the old block asks the three-checkbox question while every
  document in the repository describes the new one.

  What the installer cannot reach is anything OUTSIDE those markers. A personal
  `CLAUDE.md` that restates the routing question in its own words — a Korean
  table of the three checkboxes, say — is the owner's own text, and the
  installer never touches it. That half is theirs to update.
