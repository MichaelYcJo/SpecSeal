# 1790076050-the-release-tail-is-three-acts-no-document-names — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | docs/386-the-release-tail-ends-at-the-tag |

Answered 2026-09-22 by the repository owner, before the first edit.

## Why this way

The owner pressed `automation` for the whole 0.13.1 run. This work item is
#386, #417 and #450 taken as one branch: three acts that happen after the tag
and are written down in no document — publishing the release note, telling the
plugin directory, and the `size: now` label the sizing rule specifies and the
tracker has never had. All three are read by whoever cuts the next release, so
they change the checklist and the tracker's own document rather than any code,
and the SDD ladder's top rung applies because what a release does after its tag
is a rule.
