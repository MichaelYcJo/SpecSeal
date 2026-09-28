- **The worktree guard judges a branch switch written after a worktree
  creation in the same command (issue #620).** `git worktree add ../x -b x &&
  git switch y` used to be judged as a creation alone, so with consent it was
  silent, and the switch ran even when another Claude session was actively
  working in the tree. A command that switches and creates now gets the switch
  direction's verdict whichever of the two is written first, with the creation
  judged inside it. The two orders give the same decision and the same reason
  in every tree state, and the combined verdict is never weaker than either
  part alone. A switch into the worktree the same command creates (`cd ../x &&
  git switch y`) is judged against the session's own tree, because the new
  one does not exist yet when the guard runs; `git -C ../x switch y` avoids
  that stop.
- **The routing answer is read only from an entry marked `isSidechain:
  false`, and two guard messages say only what was counted (issue #624).** A
  transcript entry whose `isSidechain` is true, missing, or not a boolean is
  no longer read as the person's `automation` answer. The `[worktree-ok]`
  prompt now says no other session *can be shown to be working* in the tree,
  which is also true where only idle sessions were found. The uncommitted-
  changes prompt opens with *Single-stream tree* only where the tree was
  counted as single-stream; reached through `[shared-tree-ok]`, it says the
  token carried the user's answer. Both in English and Korean.
- **The worktree guard's specification states what it enforces as classes,
  not counts (issue #243).** It said exactly five spellings of `git` get an
  allow and that everything else asks. Measured with consent present, every
  spelling the shell reduces to the word `git` gets the allow and everything
  else leaves the guard silent; none asks. It also gave the no-hole property
  of the creation check as three figures from a probe nobody can re-run. Both
  paragraphs now name the committed cases that hold them, and the heredoc
  known limit, measured as closed, is removed.
- **The uncommitted-changes prompt reads the tree being switched, not the
  session's directory.** `git -C <repo> switch` or `cd <repo> && git switch`
  into a dirty repository from elsewhere gave no prompt, and a switch into a
  clean clone from a dirty session tree asked about the wrong tree's changes.
  Found in review; it predates this release. The force-staged check behind the
  prompt runs from the tree's root, so a switch through a subdirectory still
  names an ignored path that was force-staged.
- **Every command the worktree guard prints for a person to run names the tree
  it is about.** Where the shell is outside the judged tree, the switch
  steers, the worktree option and the `git restore` hints carry `git -C
  <tree>`; inside it the text is unchanged. The `git restore` hints always
  carry `-C <root>`, because their paths are root-relative, and followed from
  another repository they would have unstaged or overwritten that repository's
  files. Two printed commands still act on the shell's tree, and a repository
  path with a space breaks the printed `worktree add` line; both are #643.
