# Questions — a git call that fails reads as no remote

<!-- Decisions only a human can make. The batch below was collected before the
first edit; anything that arrives later is added as a row rather than raised. -->

## Answered before the first edit

| # | Question | Answer | Who answered |
|---|---|---|---|
| Q1 | Should `seal import` refuse or warn when the remote is unreadable? | **Refuse**, and the escape is a flag of its own rather than `--allow-other-repo`. The grounds are in `spec.md` §*The judgment the owner made* | the repository owner, in the routing batch, 2026-09-07 |
| Q2 | How is this work routed — implementation, review, destination? | `smith` builds; through the review chain; open the pull request into `release/v0.9.1`. Recorded in `routing.md` at `77005f8` | the repository owner, same batch |

## Assumptions taken in writing, because a different answer would not change the code

| # | Assumption | Why it does not block |
|---|---|---|
| A1 | The flag is named `--allow-unreadable-remote` | The owner left the name to this session; `spec.md` argues it against two alternatives. A rename is one string and one line of each README, so waiting on it would cost more than changing it |
| A2 | An absent `remote` in an incoming manifest refuses, the same as an unreadable one here | The ticket's own sentence — *a field that could not be read should be absent rather than empty, so the receiving machine can tell* — has no purpose unless the receiving machine acts on it, and the only act available is the refusal Q1 chose |
| A3 | `head` becomes present-or-absent with no empty state | `git rev-parse HEAD` prints a SHA when it succeeds, so there is no third thing a present-and-empty `head` could mean. The one existing reader already treats absent and empty alike |
| A4 | The format number stays `1` | No field was renamed or repurposed, and format 1's readers already go through `manifest.get`. Moving it would refuse every zip an older build wrote, for a change older builds tolerate |

## Open

None. Nothing surfaced during the work that a person had to settle.
