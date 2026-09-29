# 1790655302-every-reader-ends-a-line-where-gfm-does — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. -->

📋 implement applied
· spec:     being written as the phases close
· evidence: being written as the phases close
· verified: being written as the phases close

## Why this work exists

A reader that split markdown or record text with `str.splitlines` read lines
no renderer shows below one of eight characters; after this, every reader
outside work item F's files ends a line where GFM, `ast` and git do.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The count of F's `hooks/config.py` sites | *The class, enumerated*: "`hooks/config.py` (3)" · `ast` finds two calls, `#config_rows` and `#refusal`; `#unfenced` names `text.splitlines()` in its docstring and makes no call | code; the class case lists what `ast` finds | F's file either way, exempted by path. The third was a docstring mention, which the spec's own M3 says it does not list |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over this branch | the sealer, once the review rounds settle |

## Not done

Being written as the phases close.

## Fed back into the spec

none
