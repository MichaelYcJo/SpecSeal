- **More than half of the review skill was addressed to the orchestrator, and
  a reviewer read all of it at every spawn (issue #265).** The five sections
  `skills/code-review/SKILL.md` prefixed `Orchestrator:` were 24,947
  characters, 53% of the file, and a `warden` spawn received them before its
  first tool call. A reviewer acts on none of them: it does not decide whether
  a run ends, does not resume an implementer, does not open or mark a pull
  request, and does not post. **They now live in
  `skills/code-review/orchestration.md`**, which the skill names in a pointer
  where its intro ends, so a session orchestrating a review run meets the
  path before it reads any of the reviewer's material.

  **The seam is the author's, not this change's.** The five sections were one
  contiguous block — lines 236 to 653 — and every heading in that run carries
  the prefix while nothing outside it does. The 418 removed lines are
  byte-identical to the file that now holds them, and the three ledger rows
  that were anchored on those headings came back from `--reverify` with the
  hashes they had before the move.

  The headings keep the `Orchestrator:` prefix, so every reference names the
  section it always named and only the file changed.

- **Three of `writing-style`'s four per-document sections are not a
  reviewer's, and they left the reviewer's payload too.** 「PR 본문에만」,
  「다른 팀에 답할 때」 and 「사용자와의 대화에만」 moved to
  `skills/writing-style/outside-the-review.md`; 「리뷰 코멘트에만」 stayed,
  because that one is the only writing a reviewer does. `writing-style` is
  still in both `warden`'s and `smith`'s `skills:` list — the file moved, not
  the list.

  **No style check was built, and that is the decision rather than the
  omission.** Moving the whole skill out of preload would trade a guarantee
  for a saving and pay for it with an instruction, and #180 is seven measured
  instances of a rule written down and then re-broken. Whether a style rule
  can be checked mechanically is still open.

- **What a `warden` spawn reads goes from 108,399 bytes to 78,109**, measured
  with `wc -c` over the three files its `skills:` list names plus its own
  definition.

  **This is occupancy, not speed.** Prompt caching flattens the repeat price
  within a session, so there is no per-spawn token saving to claim and no
  wall-clock reading behind any of these figures — the meter this repository
  publishes is wrong until #200 and #202 land. What the numbers say is that
  the characters occupied the context window on every spawn whether they came
  from cache or not, and that a round killed and re-run paid the full write
  again.

- **Both enumerations of what the split would cost were taken by grep, and
  both were short.** Recorded because the enumeration is the release this
  ships in.

  The check that *no reference crosses the seam* greped the literal
  `Orchestrator:`, which matches the five `##` headings and none of the seven
  `###` subsections beneath them. Re-taken by construction over every heading
  in the block, four live references appear that the grep could not see —
  `agents/smith.md` and `skills/implement/SKILL.md` name one subsection,
  `tests/test_a_record_precedes_the_fixes_it_commissions.py` names another,
  and `docs/review-handoff-protocol.md` names a `##` one twice.

  *Eleven test modules pin the path* is eleven by path and **21** in fact: ten
  more name the file as the Python tuple `("skills", "code-review",
  "SKILL.md")`, which no path grep reaches. Six of the eleven needed no change
  at all, five modules the estimate never named broke, and
  `tests/test_docs_line_wrap.py` is the one that could not have been caught by
  running anything — it reads a fixed list of paths, so 418 lines of
  wrap-covered prose leaving a listed file lose their guard with nothing going
  red.
