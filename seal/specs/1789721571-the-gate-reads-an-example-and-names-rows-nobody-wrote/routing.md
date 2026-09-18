# 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/429-430-the-gate-reads-an-example-and-names-rows-nobody-wrote |

Answered 2026-09-18 by MichaelYcJo, before the first edit.

## Why this way

Two findings from round 3 of #415, both about `seal/config.md` — one about
which table is read out of it, one about what the refusal says when a row in
it will not parse. Neither was fixed on that branch because the run was
capped.

#429 is a verdict: `hooks/config.py#config_rows` starts at the first
`| Item | Value |` header in the file and a code fence is invisible to it in
both directions, so an example table written above the live one is the table
every reader gets — the broad command, the mode, every row. `seal/config.md`
is a markdown file whose own header comment points at a template full of
example tables, so the shape that breaks it is the shape a person is invited
to write.

#430 is text a person reads and acts on: the refusal for an unparseable
`Broad gate` line ends by saying every row written below it is lost, without
ever asking whether anything is below it. This repository's own config ends
with that row, and so does the table `templates/config.md` ships, so the file
somebody is likeliest to be holding the first time they type a bare pipe is
the file the sentence is false about.

A gate's verdict and a refusal a person debugs from both sit on the ladder's
top rung, so the frame is drawn by a party that does not then build to it.
They are one work item because they are one file's reader and that reader's
one refusal, found by one round, and splitting them would have two branches
editing `hooks/config.py` and its cases at the same time.
