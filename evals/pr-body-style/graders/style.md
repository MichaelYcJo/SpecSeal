---
type: llm
criteria: |
  The PR body must (1) describe what CHANGES for users/operators, not list
  files ("auth_service.py에 함수 추가" style file-by-file listing fails),
  (2) call out the DB migration as a separate operational item, (3) use plain
  Korean prose in complete sentences without colloquial endings (~네요/~예요),
  (4) explain WHY where a choice needs justification. Fail if it is a
  file-by-file changelog or omits the migration callout.
---
PR body follows the writing-style skill's norms.
