### Fixed

- The worktree guard now asks about a `git checkout` that git resolves by a
  message search, a merge-base shorthand, or a branch guessed from a remote
  not named `origin` (#790). Before, it looked a checkout's name up with a
  suffix that a message search reads as part of its pattern, so `git checkout
  ':/fix typo'` detached HEAD over a dirty or shared tree without a word; it
  could not read `git checkout main...topic` at all; and it guessed a
  remote-only branch from `origin` alone. The guard now asks git the way
  `git checkout` resolves a name: the name resolved and peeled to a commit,
  `<a>...<b>` where it has exactly one merge base, and a remote-tracking
  branch of any remote. The old lookup is still asked first, so nothing the
  guard asked about before goes quiet. It still reads no `checkout.guess` or
  `checkout.defaultRemote`, so a few commands git refuses, such as a guessed
  name under `--detach` or one two remotes hold, are asked too;
  `docs/worktree-guard-spec.md` §*Known limits* lists them.
- The worktree guard no longer reads a consent token written inside a
  here-document body (#780). A `[shared-tree-ok]` that a command only carried
  as text in a body let a switch through where the guard could not tell who
  else was working in the tree, and a `[worktree-ok]` there turned the
  single-stream worktree refusal into a confirmation. A token now counts only
  where the command as written and the command with its bodies taken out both
  carry it, the rule the commit gate's waiver has followed since #773. Every
  documented form still works: a trailing `# [shared-tree-ok]`, a bare word,
  or a token inside `( … )`, with or without a here-document elsewhere in the
  command.
