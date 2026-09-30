# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show, each part written when it happened. -->

## Why this work exists

The commit gate, the mode and broad gates and the rider check each decided by
a rule of their own, or by none, whether a row quoted in a fence or parked in
an HTML comment is a row; they now read one walk, held line by line to a
CommonMark parser, so a hidden row stops answering and no row the base read is
lost.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The uncertainty table is wider than the frame's minimum | `spec.md` §*What is not modelled*: "a construct start indented one to three spaces", "a line at up to three spaces beginning `<` …", "lines of a block quote, and lines indented four spaces or more". The code also leaves unclaimed a construct-looking line behind a list marker or `>` at any indentation, a line behind any container marker, a blank line after an indented or marked line, and a fence whose first closer carries a no-break space after its run | The wider table | `spec.md`: "It may never narrow what it calls uncertain without that", and widening the uncertain set is the other direction. Each addition was found by the property going red on a generated document the frame's minimum called exact (phase 2's record); `- ```` hides the item's indented lines, which the minimum claimed live |
| S15 for a copied hook reader | `spec.md` S15: "when it loads, then it exits with a sentence naming the file" | `hooks/config.py` (and `hooks/routing.py`, phase 4) raise one `ImportError` carrying that sentence; `seal.py` exits 2 with it through `HOOK_PURPOSES` | Both are modules other code imports, not scripts. A gate that raises at load is skipped for that call and said at the end of the turn (`hooks/dispatch.py`, #28, merged from #660 during phase 2); a script that loads either by path catches the error (`chain_check.py`) or names the file before it imports (`seal.py#HOOK_PURPOSES`), and an exit from inside an import would take that choice from it |

## Not verified

| Item | Who must answer |
|---|---|
| The oracle and the property on the Windows and Linux legs | CI's test matrix at the pull request |
| The full suite, lint and typecheck over the finished branch | the sealer, once the review rounds settle |
| Q7's corpus time on the slowest CI leg, Windows; it was measured on macOS alone | CI's Windows leg at the pull request, whose log times the module |
| A no-break space after a closing fence run: the shared delimiter rule (`unverified_check.py#fence_closes`, and `hooks/blocks.py#fence_closes` in step with it) reads it as a closer with `str.strip`, and CommonMark does not. The walk claims nothing below such an opener, so no reader here gives a third answer, but every other reader of the shared rule still reads it that way | the orchestrator, who decides whether it is filed against the shared rule |

## Not done

- `docs/the-broad-gate.md` §*A fenced example in a config file is not a config
  row* was not given a sentence on comments. It is a ratified policy, and the
  frame cites it as grounds rather than as a document this work edits; the
  rule and the new refusal are stated in `templates/config.md`, which the
  policy's readers are sent to.
- The CONTRIBUTING.md gate lines are drafted in each phase record, for the
  pull request body, and not written into `CONTRIBUTING.md`: that section
  asks each change to carry them, not to add them to it.

## Fed back into the spec

- *Inferred during implementation:* the uncertainty table in `spec.md`
  §*What is not modelled* is a minimum the build widened in four places
  (`phases/phase-2.md`); a planner may narrow any of them only with the
  context in the property's alphabet and the property green.
