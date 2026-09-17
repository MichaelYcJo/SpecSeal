<!-- seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **Three checks this release wrote were passing while the thing each is named
  for was free to be wrong.** Each was found by the round that ended its own
  work item's run and deferred because that run had spent its one reopening,
  not because anyone judged it unworthy. They are repaired together because
  they are one shape, and each is now red under the mutation its own issue had
  already measured green.

  - **The two `&` cells of `templates/config.md` now have to say WHICH shell
    does which** (#413). The case found both shell names in each cell and
    nothing tied a name to a consequence, so `/bin/sh` and `cmd.exe` could be
    exchanged in either cell with all eighteen cases green — and the document a
    person reads before writing the `Broad gate` row would then state one
    platform's semantics as the other's. Both swaps are red now. What the case
    still cannot see is written beside it: it pins that the document
    ATTRIBUTES each behaviour to a shell, never that the behaviour is that
    shell's, which stays unmeasured on `cmd.exe`.

  - **A phrase joining either sweep of `tests/test_one_word_one_meaning.py` is
    checked for seam safety again** (#418). The case said it asserted over the
    whole phrase set; three of the set's four sources were hand-copied
    literals, so a phrase added to a sweep was covered by nothing. The phrases
    are module constants the sweeps and the seam case both read — one
    definition, read twice, which is not the derivation the issue refuses — and
    the members `flat` folds are pinned as a list, so a `.py` member joining a
    sweep turns the case red and names it. **The count the closure rested on
    was wrong in three documents**: five members are `.py`, not four. The case
    pins the list rather than a number beside it.

  - **The guard over agent definitions stops matching inside longer words, and
    finds an instruction by what it claims rather than by one spelling**
    (#422). `\bperson` fired on `persona`, which `agents/smith.md` already
    writes, and `\buser` on `users`; both ends of every stem are anchored now.
    Anchoring the back is not free — it would also stop `questions` and
    `asked` — so the stems split into the ones that carry their inflections and
    the ones anchored bare, where the plural names a population rather than the
    party at the keyboard. The `user` stem stays, against the issue's own
    patch: dropping it would let *collect in one batch what the user answers*
    pass in silence. And the finder no longer looks for one substring, so
    `in **one batch**` — `CLAUDE.md`'s own wording — `in a single batch` and
    `as a single batch` all reach the window that judges them. All three
    passed at exit 0 before. Nothing in the tree had to be reworded for either
    half.

  - **The guard is one function, and the case calls the same one.** The
    patterns were first hoisted to module level so a case could open them —
    and that was still the defect, one layer down: no agent definition
    contains a batch phrase at all, so the sweep's loop body never ran and the
    composition inside it could be changed five ways with the module green.
    The sweep is now `batch_instructions(body)`, and the case that holds the
    guard runs that same function over text it writes. All five mutations are
    red.

  - **The marker set matches the one the repository already had.** Emphasis
    was stripped as `*` alone, which left out the marker these files use most:
    backticks outnumber asterisks in four of the five definitions. It strips
    `*`, `_` and backticks now — the same three `chain_check.py`'s normaliser
    of the same name strips — and `into` joined the preposition set. Stripping
    `_` cannot change what is found; it costs only the underscores in a file
    name the refusal prints.

  - **What the back anchor cost is recorded as a loss, not asserted as
    correctness.** It also stopped `asker`, `answerer` and `questioner`, each
    of which names the party this guard looks for — `agent-contract` §4 writes
    `answerer` for exactly that party. Widening the stems is still refused with
    grounds; the three words now sit in their own block saying so.

- **Two Grounds cells of a shipped round record stop rendering an empty first
  clause** (#414's remainder). `rounds/round-2.md` of work item
  `1789445605-…` read `fixed at 6233b769 — . `; the cause was removed earlier
  in this release and eleven cells were left behind, nine repaired by hand at
  the time. These are the last two. Only the rendering is repaired — a round
  record holds what was true when it was written.

- **The wrap module's documented widths are re-derived rather than remembered.**
  `tests/test_docs_line_wrap.py` documented `agents/smith.md` at 148 columns
  where it measures 109, and `skills/implement/SKILL.md` at 99 where it
  measures 90 — a hand-written measurement in the one module whose subject is
  measured widths. Nobody had reported the second one.
