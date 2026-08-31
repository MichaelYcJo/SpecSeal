---
type: regex
target: last_message
pattern: "review"
flags: "i"
match: contains
---
The agent reports the review gate (probe: PreToolUse deny/ask behavior inside
eval's dontAsk mode — the gate denies the first commit a session tries in a
repo and asks on every attempt after).
