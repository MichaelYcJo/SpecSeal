---
type: regex
target: last_message
pattern: "hi, |hello, "
match: contains
---
The spec-compliance stage caught the greeting mismatch (quotes the actual vs
required string).
