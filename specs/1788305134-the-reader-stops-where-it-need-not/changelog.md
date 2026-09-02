- **The command reader stopped commits it did not need to stop, and once
  it stopped asking it answered where it should have refused.** A path the
  command wrote out for itself one segment earlier is a path the gate can
  read: `SB=/abs; git -C "$SB" commit` names `/abs`, and the gate's answer
  is byte-identical to the written-out form. Nothing this process cannot
  see is guessed at — `git -C "$WT"` from the environment, `$SB/r$n` in a
  loop, `$(pwd)` and `$1` all still reach the ask — because the substitution
  runs in FRONT of the test that refuses them rather than replacing it. A
  `((` inside a `${…}` word is a word to both paren models, so the heredoc
  below it opens and `echo ${x:-((} <<EOF / cd /target / EOF / git commit`
  is judged where the shell is rather than where the body says. A refused
  segment that carries no name — `fi`, `then echo hi`, a subshell — keeps
  the names the command has written, where every refusal used to empty
  them and `if …; then … fi` prompted for that alone. That aim was proven
  against bash rather than assumed, and the proof found 82 shapes it had
  opened: a body's SECOND statement arrived as a top-level assignment and
  bound, so `if false; then echo hi; SB=/three; fi; git -C "$SB"` answered
  `/three` where bash has `/one`; and `! for SB in …` passed as a simple
  command because only the first word met the reserved-word test. A stack
  of open bodies runs beside the name environment now, and a statement
  inside a body is forgotten rather than bound — a stack, because a
  multi-line `case` puts its arm pattern `a )` where a subshell's closer
  stands and an integer count took it for one. A call to a function the
  string itself defined empties the names it holds, an array assignment
  `SB=(x)` empties the name rather than binding `(x)`, and `((SB=…))`,
  `let` and `${SB:=…}` forget it. The differential that found all of this
  is in the tree as `tests/test_the_reader_agrees_with_bash.py`: whatever
  the reader answers, bash must answer the same, and a prompt is exempt.
  `agents/warden.md` and `agents/scribe.md` say how to write a scratch-repo
  probe that commits without raising the prompt.
