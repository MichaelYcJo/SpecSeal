### Added

- A work item that commits in more than one repository can keep one
  contract in a pact (#647, steps A and B). The pact is `seal/pact.md` in
  one of the repositories, begun from `templates/pact.md`, and every
  repository of the work item is a signatory, that one included. A sentence
  belongs in the pact when another repository's code would be wrong if it
  changed. `docs/the-pact.md` is the policy.

- The routing step covers every repository the work item commits in. The
  question is asked once, the work-item id is minted once and names the
  directory in every repository, and a declaration goes into each
  repository that already has a `seal/` root. A repository without one is
  named in the handback and left alone, because writing into it would opt
  it in.

- Two `seal/config.md` rows, `Pact` and `Pact notify`, name the pact a
  signatory signs and what it asks to be told about a change to it;
  `Pact notify` decides which of its changes are recorded as pact changes,
  below. A row that will not parse is refused in a sentence rather than read
  as absent.
  `/specseal:config` now shows all ten rows the template ships, including
  `Reference specs`, which it had been leaving out.

- A signatory cites a clause it was built against as
  `pact:<name>/"<heading path>"@<hash>`, in a spec's Grounding or in a ledger
  row's `Clause` cell. Its own `evidence-check` reads past the anchor, so a
  version in a clause heading is never reported as an old-format coordinate.

- `pact-check`, run at the pact's repository, reads every signatory the pact
  lists, found through `~/.claude/specseal/pact-paths.md` or a sibling
  checkout with nothing guessed, and grades every anchor: `SUPERSEDED`
  where the signatory was built against an older clause, `NOT TAKEN` naming
  the branch holding a change the pact has not taken, `UNMATCHED` and
  `BROKEN`. It runs locally only.

### Changed

- At a signatory's pull request, `chain-check` prints the pact it names, the
  notify value and how many pact anchors the declared work item cites, and
  in the pact's repository how many signatories the pact lists. None of it
  moves the exit status, because a pull request there can read one
  repository and `pact-check` is where the reconciliation runs.
