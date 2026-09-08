- **A rider stamp no longer names a commit the release's own merge rule
  destroys.** `# RIDER:` comments carry a `Verified … at <sha>` line so whoever
  opens one can see how stale it is. A fix pass works on a feature branch, so
  the only commits it has to name are that branch's — and a feature branch
  **squashes** into its release branch, which writes one new commit and keeps
  none of the originals. The stamp planted by #226's fix pass stopped
  resolving the moment #226 merged, and
  `tests/test_a_rider_reaches_its_file.py::test_every_rider_stamp_names_a_commit_this_branch_can_reach`
  turned the release branch red — on the merge rather than on the branch that
  wrote it, so the person who has to repair it is never the person who caused
  it. The claim was re-measured on the squash commit that carries the same
  state and the stamp names that. The class this belongs to — a stamp naming a
  position in a repository whose rules rewrite positions at every boundary — is
  #239. (#239)
