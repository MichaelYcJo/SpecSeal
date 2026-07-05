---
type: regex
target: {source: file, path: "messy.py"}
pattern: "x = 1"
match: contains
---
The PostToolUse lint hook reformatted the file (probe: do plugin hooks fire
inside eval runs at all?).
