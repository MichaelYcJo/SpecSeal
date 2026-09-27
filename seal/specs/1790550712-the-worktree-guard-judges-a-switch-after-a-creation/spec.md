# Feature Specification: the worktree guard judges a switch written after a creation (#620, #624, #243)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Milestone 48 (`release: 0.15.6`), item A. One verdict change (#620), three
reason sentences and one reader condition (#624), and three wrong counts in
the enforcement document (#243). All three live in `hooks/worktree-guard.py`,
`hooks/worktree_consent.py` and `docs/worktree-guard-spec.md`.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §*Creation consent* — *What does not change*: "The switch direction reads neither: a creation the user agreed to, or a run the user said should not stop, says nothing about taking another session's branch out from under it." | #620 is a breach of this clause. With consent present, `git worktree add ../x -b x && git switch y` is silent over an ACTIVE tree, because the switch is never judged. The fix enforces the clause; it adds no rule. |
| `docs/worktree-guard-spec.md` §A *Branch switch* matrix | What a switch gets in each tree state. After this work a switch gets it wherever it is written in the command. |
| `docs/worktree-guard-spec.md` §*Creation consent*, the table under *So the creation is judged between the ladder's two halves* | The precedence between a switch and a creation on one command line, already ratified for switch-then-create. This work applies the same table to create-then-switch rather than writing a second one. |
| `docs/worktree-guard-spec.md` §*Why the allow is bounded* and §*Unknowns resolve conservatively* | The strictness order below: `allow` speaks for the whole call and bypasses the user's own permission settings, `silent` hands the call to them, `ask` puts it to a person, `deny` stops it. A wrong deny costs a prompt and a wrong allow can break another session's tree. |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | A `cd` to a directory that holds no repository falls back to the session's own tree. This decides how `git worktree add ../x && cd ../x && git switch y` is judged (below). |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Every new case seen red; the PR body states the failure direction and the prompt budget (see `plan.md`). |
| `skills/agent-contract/SKILL.md` §5, §12, §14, §15 | §5: a count in the document must come from something a reader can run. §12: the walk defect and each corrected sentence are fixed as a class, and the plan lists every copy. §14: every changed reason is pinned in the same commit. §15: every new case is shown red first. |

## Decisions the tickets left open, and what the tree answered

1. **"Stricter" across the guard's four outcomes is `deny` > `ask` > `silent` > `allow`.**
   The grounds are the §*Why the allow is bounded* clause in the table above.
   `silent` ranks above `allow` because silence leaves the harness's own
   permission flow in force, while `allow` overrides it. A command that
   carries a switch can never reach `allow`: `only_creates_a_worktree` requires
   every segment to be a `git worktree add` (`hooks/worktree-guard.py#only_creates_a_worktree`),
   and a switch segment fails that. So in practice the combined verdict is
   drawn from `deny`, `ask` and `silent`.

2. **The stricter answer is produced by the ladder that already produces it,
   not by a new comparison.** A command that carries both a switch and a
   creation is judged by the switch ladder, with the creation hooked in at the
   two places the switch-then-create shape already uses (`choose`'s
   `before_ask`, and the `judge_creation` call between rows 2 and 3). That
   holds whichever segment is written first. Read against each tree state,
   this ladder's verdict is never weaker than either direction's own verdict.
   The list below is `read`, and scenario S3 is the case that measures it:

   | Tree state | Switch alone | Creation alone (compound) | The shared ladder |
   |---|---|---|---|
   | ACTIVE | deny | ask (no consent) · silent (consent) | deny |
   | only IDLE, first attempt | deny (choice) | deny (choice) · silent | deny, the switch's text |
   | only IDLE, later attempts | ask | deny (choice, own budget) then ask · silent | the creation's verdict, or the switch's ask where the creation is silent |
   | detection unusable | as IDLE | as IDLE | as IDLE |
   | single stream, dirty | ask | deny · silent | the creation's deny, or the dirty-tree ask where the creation is silent |
   | single stream, clean | silent | deny · silent | the creation's deny, or silent |
   | the creation's own repository differs (`git -C`) | per the switch's tree | per its own tree | same rows, each judged against its own tree |

3. **Which reason text reaches the person when both fire at the same level.**
   This is the precedence the ratified table already sets, and it has a reason
   at each level:
   - **Two denies:** the switch's text. The ACTIVE row comes first and then the
     choice rows. A deny stops the whole command line, so the creation is
     stopped with it and is judged on the next attempt.
   - **Two asks:** the creation's text. Approving an `ask` runs every segment,
     so the text must name the creation. Otherwise the consent record is
     minted for a question nobody put, which is the property
     `docs/worktree-guard-spec.md` §*The property, measured rather than the
     shapes* states. What is lost is the dirty-tree fact (*the changes follow
     you*) when the creation also asks. That loss already exists for
     switch-then-create, and this work neither creates it nor removes it.
   - **Different levels:** the stricter verdict's own text, always.

4. **Order-independence is the property the new case pins.** For every tree
   state, consent state and attempt, `git worktree add ../wt f && git switch
   feature/x` and `git switch feature/x && git worktree add ../wt f` get the
   same decision and the same reason. That checks the fix against the whole
   class: once the order cannot change the answer, the reviewed switch-first
   behaviour covers the create-first shape too.

5. **A `cd` into the worktree the same command creates is judged against the
   session's own tree.** In `git worktree add ../x && cd ../x && git switch y`,
   `../x` holds no repository when `PreToolUse` runs, so `judgeable` falls back
   to the session's directory (§*Which tree*). This errs toward a stop: the
   person meets the tree's switch verdict for a switch that actually happens
   in the new worktree. `git -C ../x switch y` in the same place has a `-C`
   that names no repository, so it keeps §*Which tree*'s silence and the
   creation's own verdict stands. The document's *Known limits* gains this
   line, and it names `-C` as the spelling that avoids the stop. A special
   case that reads the creation's path argument would be new mechanism, and
   the milestone adds none.

6. **The `[shared-tree-ok]` dirty-tree row names what was measured.** Row 3 of
   the switch ladder is reached in three states: single stream (nothing idle,
   detection reliable), and, under `[shared-tree-ok]`, only-IDLE and
   detection-unusable. Its opening *Single-stream tree* / *이 트리는 단건
   작업이라* is true in the first state only. In the other two the lead says
   the token carried the person's answer. Only the first sentence changes. The
   list of changes, the phantom note and the verdict do not.

7. **The `[worktree-ok]` sentence takes #624's wording in both reliable
   states.** *No other Claude session can be shown to be working in this
   tree, but* / *이 트리에서 작업 중임이 확인되는 다른 Claude 세션은 없지만*.
   It is true both with nobody counted and with only idle sessions counted,
   so one sentence serves both and the condition stays `if reliable`.

8. **`isSidechain` is refused unless it is literally `false`.** The module
   refuses every other unmeasured shape the same way (`_routing_preset` on an
   absent `multiSelect`). Round 2 of work item 1790381327 measured 136 of 136
   linked results and 11016 of 11016 user entries carrying `false` (its
   report, *Executed probes*). That is a count taken by another party,
   carried here as that party's finding.

9. **A count in `docs/worktree-guard-spec.md` is stated only where a committed
   case reproduces it.** #243's three counts all came from probes whose shapes
   are not in the tree. Round 3 of work item 1788817291 said so: *the 21 shapes
   and the fifth tree state are not in the tree … nothing a reader can run
   reproduces 230, 64, or the 1260*. So the document states each boundary as a
   class and cites the case that enforces it. It does not trade one
   unreproducible number for another. #243 and that round's paste-ready text
   propose 690, which is the arithmetic repair of 230 against shapes nobody
   holds, and it is not adopted as a figure for that reason. Where a count
   survives, it is the count the committed case walks, and the case is named
   beside it.

## Scope

**In:**

- #620: the walk in `main` classifies a switch written after a creation. A
  command carrying both goes to the switch ladder, whichever comes first
  (decisions 2 to 5).
- #624.1: `hooks/worktree_consent.py#automation_answered` refuses an entry
  whose `isSidechain` is not literally `false` (decision 8).
- #624.2: the switch ladder's row 3 opening, both languages (decision 6).
- #624.3: the `[worktree-ok]` row's opening, both languages (decision 7).
- #243: the three counts in `docs/worktree-guard-spec.md` (decision 9),
  re-derived by running the shapes. This covers the command-word class, the
  `ask`/`silent` split, and the writer-record sweep paragraph.
- Every other copy of each corrected sentence, listed in `plan.md`
  §*Enumerated copies*. That includes test docstrings and ledger rows, and
  one miscount of the same family found while framing: a test docstring says
  *"was true of two of them"* where the fix it describes established one.
- `docs/worktree-guard-spec.md` §*Known limits*. It gains decision 5's line.
  Its heredoc line is re-measured and removed if `_judgment_text` now drops
  heredoc bodies, as that function's own docstring says it does.
- The work item's changelog fragment and ledger fragment, and the re-reading
  of every existing ledger row whose anchor this work edits.

**Out, each with its reason:**

- **A switch after a switch in a different tree** (`git switch a && git -C
  ../other switch b`), and **a second creation in a different clone**. Both
  come from #620's cause, but closing them needs the ladder judged once per
  tree, which is a refactor of `main` into a per-tree function. The milestone
  adds no mechanism. `questions.md` Q1 records the default, and the
  orchestrator files the issue.
- **#21** (the dirty-tree prompt recommends an answer it does not offer).
  This work edits row 3's first sentence only. #21 asks to restructure that
  row into a choice site, which is a verdict-shape change and a separate
  decision.
- **#20** (the guard's answer rides on every command). Nothing here touches
  how a retry token carries an answer.
- **#24** (the switch arm has never been judged against a live concurrent
  session). This work adds headless cases through a patched
  `sessions_in_tree` and does not close the live-session question.
- **#22 and #301** (the commit gate's repository identification). Commit gate
  only. No file here is touched.
- **The rest of `docs/worktree-guard-spec.md`**. Only the sections named
  above were read against the code. The document was not audited as a whole.
- **CHANGELOG entries of released versions.** They describe what shipped. The
  correction ships in this work item's own fragment.
- **README.md and README.ko.md.** Their worktree-guard rows were read. They
  describe the switch direction's verdicts without an order of segments and
  say nothing about the three counts or the two sentences, so they stay true
  and are not edited.

## User scenarios & acceptance *(mandatory)*

`decide` is `tests/test_the_guard_asks_once_per_session.py#decide`, which
patches `sessions_in_tree`. "Consent" means the record (`grant`) unless the
row names the routing answer.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the ticket's shape | Given a consent record and an ACTIVE session in the tree · When `git worktree add ../wt -b x && git switch feature/x` · Then `deny`, with the switch ladder's ACTIVE text. It was silent before | new case, seen red at the base |
| S1b the routing answer too | Given the `automation` answer in the transcript, no record, ACTIVE · When the same command · Then `deny` | new case, seen red at the base |
| S2 order does not decide | Given each of the five tree states × {no consent, record} × attempts 1–3, one session id per cell · When the create-first and the switch-first spelling are each run (separate ids) · Then both get the same decision and the same reason | new case, seen red at the base (the create-first spelling is silent or asks where the switch-first one denies) |
| S3 never weaker than either direction | Given the same grid at attempt 1 · When the combined command, the switch alone and the creation-as-compound alone are each run in a fresh session · Then rank(combined) ≥ max(rank(switch), rank(creation)) with `deny`>`ask`>`silent`>`allow`, and the combined command never answers `allow` | new case, seen red at the base |
| S4 nothing moves without a switch | Given each tree state × consent · When `git worktree add ../wt f`, `git worktree add ../wt f && cd ../wt`, and `git status && git worktree add ../wt f` · Then each verdict equals the base's | new case, or the builder's executed before/after table in `phases/phase-1.md` |
| S5 the writer-record property holds with create-first shapes | Given `test_the_guard_is_never_silent_where_the_writer_records`, extended with at least `git worktree add ../wt f && git switch feature/x` and its `;` and `checkout` forms · Then 0 holes | the extended case |
| S6 the `-C` and `cd` spellings | Given ACTIVE in the session's tree · When `git worktree add ../x -b x && git -C ../x switch y` · Then the creation's own verdict (as at the base). When `… && cd ../x && git switch y` · Then `deny` (decision 5, the conservative fallback) | new case, with both asserted |
| S7 sidechain | Given a linked routing result · When `isSidechain` is `True`, `"true"`, `1`, `None`, or absent · Then not consent. When it is `False` · Then consent | `test_a_sidechain_entry_is_not_consent` widened (round 2 report's paste-ready version), seen red with `is True` restored |
| S8 row 3 names what was measured | Given a dirty tree · When `git switch other  # [shared-tree-ok]` with sessions `([], IDLE, True)` and then `([], [], False)` · Then the reason does not open *Single-stream tree* / *이 트리는 단건 작업이라*, and it names `[shared-tree-ok]`. With `([], [], True)` and no token it still opens *Single-stream tree*. Both languages | new case, seen red at the base |
| S9 `[worktree-ok]` names what was measured | Given `git worktree add ../wt f  # [worktree-ok]` · When sessions are `([], [], True)` and `([], IDLE, True)` · Then both reasons carry *No other Claude session can be shown to be working in this tree, but* (Korean twin with `SPECSEAL_LANG=ko`). When `([], [], False)` · Then neither sentence appears | `test_the_two_reworded_reasons_are_pinned_in_both_languages` and `test_the_token_rows_count_sentence_is_said_only_where_a_count_was_taken`, moved to the new wording and given the idle row; seen red with the old wording |
| S10 the command-word class is stated as a class | Given the paragraph at `docs/worktree-guard-spec.md` §*Creation consent*, *The boundary the code implements* · Then it names the class (any spelling the lexer reduces to the word `git`) and no count of spellings. It splits the refused shapes into those that get `ask` and those that leave the guard silent, as a committed case measures them | a committed case pinning at least one member of each group (`allow` · `ask` · silent), shown red by moving one shape to the wrong group; the paragraph cites it on an `Enforced by:` line |
| S11 the sweep paragraph cites what reproduces it | Given *The property, measured rather than the shapes* · Then every number in it is one the named committed case walks, or the paragraph carries no number | read against the case; `seal/releases/0.9.1.md`'s two rows corrected in place |
| S12 every copy moved | Given `plan.md` §*Enumerated copies* · Then each listed copy says the new thing, and a `git grep` for each old phrase finds only records of the past (round records, released changelog, the phase records of earlier work items) | the grep, run by the builder and repeated by the reviewer |

## Data & interfaces

No payload, schema or file-format change. The consent reader's accepted shape
narrows (S7). `respond`'s output keeps its shape. What changes is which reason
text a person reads in the cases S1 to S3, S6, S8 and S9 name.

Ledger coordinates this work cites or drifts are listed in `plan.md`
§*Ledger rows this work re-reads*.

## Open questions → questions.md

One row a person may overturn (Q1, whose default is already applied), three
measurements the build takes, and one the work settles.

Framed 2026-09-28 by framer, before the build.
