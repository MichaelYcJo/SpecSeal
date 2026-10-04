### Fixed

- The worktree guard's policy now names the words that make it ask, the
  same words the guard reads (#750). The sentence in
  `docs/worktree-guard-spec.md` §*Which tree* counted a checkout naming a
  branch before `--` as a switch, although git restores the file there and
  the guard does not ask. It named `checkout -b` and left out a bare `-B`,
  which the guard counts. And it left open whether `switch -- x` counts,
  which it does. The guard's behaviour is unchanged. A test now pins the
  sentence, and three new rows bind the guard's reading to each word the
  old sentence got wrong, so the two cannot drift apart on them. The case
  that checks every generated shape against the policy's rule also had a
  half that could never fail; it now fails when the guard stops subtracting
  what each view's own segments already hold.
