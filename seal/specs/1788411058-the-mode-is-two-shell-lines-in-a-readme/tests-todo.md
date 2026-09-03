# 1788411058-the-mode-is-two-shell-lines-in-a-readme — tests to plant

<!-- Rows a review round asked for and the implementation commit did not
carry. Drained when every row is planted or answered; the release guard reads
this file's sibling, `evidence-todo.md`, and the review-history guard names
both. -->

| Test | Why it is not here already | Who plants it |
|---|---|---|
| `.gitignore` holding `seal/`, `seal mode shared` run from a subdirectory: take the `git add -f :/seal` the output prescribes, run it **from that subdirectory**, and assert the root enters the index | Round 5 measured all three recovery commands working and found two of them pinned by nothing: reverting `seal.py:2000` to `git add {root}` and `seal.py:1970`'s `:/` both left 76 cases green. The case round 4 planted ignores `.github/` only, so the root's `git add` never fails and its prescription never prints. Behaviour is correct; the guard against a regression is missing | the next commit that opens `tests/test_the_mode_is_a_row_and_a_command.py` |
| The same shape for `git rm -r --cached :/seal`, which needs a tracked root rather than an ignored one | same round, same measurement | the same |

drained: no
