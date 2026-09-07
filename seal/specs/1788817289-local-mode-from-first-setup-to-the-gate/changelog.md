- **A repository in local mode met a review chain that refused its root and a
  check that reported its declaration missing.** `round_record.py` derived the
  repository from the work item, through a `git rev-parse --show-toplevel` run
  from inside the item — and a local-mode item sits under the common git
  directory, where git declines that question outright (`fatal: this operation
  must be run in a work tree`). So every call needed `--root "$PWD"`, and the
  first one without it was told the item is nowhere. Git is asked which trees
  belong to the clone now, and the caller's tree is the answer where it is one
  of them. Then `chain-check` printed *Add `seal/specs/<work-item>/routing.md`
  to declare* while the declaration sat at
  `<git-common-dir>/seal/specs/<id>/routing.md` — a path local mode does not
  use, and a file the operator already had. It says which root it searched
  now: a local-mode repository is told where its root is and that nothing
  under it is committed, and a shared-mode one is still told to write the
  file, with the prefix and the branch it searched for named. The verdict does
  not move — reading an untracked declaration would make the local run assert
  something CI can never reproduce — so what is fixed is that a false *no
  declaration* is no longer indistinguishable from a real one. (#225)

- **The mode nobody was asked about is now a state something names.** Creating
  `seal/` is what opts a repository in, and whether it lands in the tree or
  under the git directory decides whether every clone carries that
  repository's review records. The preset block `install.sh` copies into
  `~/.claude/CLAUDE.md` — which loads in every project on the machine,
  including one that has never seen SpecSeal — told a session to write
  `seal/specs/<id>/routing.md` before the first edit, and that write creates
  the root. The question lived in a skill the session had no reason to load,
  and nothing afterwards noticed: a root somebody chose and a root that
  appeared this way were byte-identical. Two halves close it. The routing rule
  names the condition **before** it names the write, and the bootstrap now
  records the answer it collects with `seal mode`. And a new gate,
  `mode-gate`, names a root whose `seal/config.md` carries no `Mode` row — one
  deny per session per repository with the three ways on as options, then the
  plain confirmation, and nothing at all once the row exists. It judges the
  repository the SESSION sits in rather than one a `-C` names, because this is
  a fact about a workspace and not a verdict about a change. (#151)
