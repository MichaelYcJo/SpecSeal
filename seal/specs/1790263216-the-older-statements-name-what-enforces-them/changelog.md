- **Every folded statement under `docs/` names what enforces it, and the
  fold's shape binds all of them (issue #565).** 115 statements folded before
  the shape existed carried no line saying what reads them, and review had
  already found one of them false. Each now ends in one `Enforced by:` line.
  103 name what reads the rule: the case that plants the violating input,
  the pin on a text a session acts on, or the workflow CI runs. Twelve say `nothing — <why>`, and the reason says which
  kind of rule it is: a person's or a session's act (7), a record rather than
  a rule (2), or a rule no case reads yet (3). `grep -rn 'Enforced by:
  nothing' docs/` lists all twelve. The 26 that did not open with a bold rule
  sentence now do. This repository's `Fold shape from` row is `0`, so the
  suite's real-tree case holds every statement, and a later edit that drops
  a line or renames a function one names fails it. The Korean edition of the
  one-root design carries the English targets byte for byte, and the editions
  test now compares each paired statement's line. One statement was false
  against the code: `docs/branch-and-release.md` said a rider's stamp names a
  commit. It is now corrected, along with the same sentence in both editions
  of the one-root design.
