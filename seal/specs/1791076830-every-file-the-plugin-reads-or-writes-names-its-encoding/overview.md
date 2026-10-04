# every file the plugin reads or writes names its encoding (#741) — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/{spec,plan,questions}.md (K1–K4, D1–D8, S1–S10); CONTRIBUTING.md §House rules; hooks/console.py module docstring; tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED and its liveness half; tests/conftest.py#git_listing, #on_disk, #decline_if_shrunken
· evidence: seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md — written in phase 3
· verified: executed — the new module, the phase-1 covering modules, M2 and M4; read — W1's handler per hook site

## Why this work exists

A file read or written in the locale's encoding breaks only on the Windows leg, so nothing held a branch to naming it until that leg went red after review; now the suite names every such call on every leg.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What the unfixed pre-commit does under an ASCII console (M4) | Spec D6: *under an ASCII stderr the pre-commit hook should die with `UnicodeEncodeError` … the person reads a traceback in place of the refusal.* Measured 2026-10-04 at `1ecb019f`, the S5 refusal with `PYTHONIOENCODING=ascii PYTHONUTF8=0`: exit 1, no traceback, the whole refusal printed with every `—` and `…` spelled `—` / `…`, the waiver it tells the reader to type included. Python keeps `backslashreplace` on stderr whatever `PYTHONIOENCODING` names | S8 planted, asserting the refusal arrives byte for byte as `gate.refusal` builds it and carries no `\u20` escape; red against the unfixed hook, green with the call | Spec S8's Then is *stderr carries the refusal*, which the unfixed hook does not do. M4's question as worded (does it die?) answers no, and the failure direction is milder than D6 says: the commit was refused before and after, and only the legibility of the refusal changes |
| `codecs.open` and `os.fdopen` argument positions | Spec K1: `codecs.open` takes `encoding` as *the 4th positional argument* like `open`; `os.fdopen` is *as `open`, positions shifted by the fd* | The walker uses each signature: `codecs.open(filename, mode, encoding)` is 3rd; `os.fdopen(fd, mode, buffering, encoding)` puts the fd in `open`'s file slot, so its positions are `open`'s | The signatures (`codecs.open`, `os.fdopen` → `open(fd, *args)`); spec silent on why it chose otherwise. No such call is in the tree |
| A `*` positional splat | Spec K2 names a `**` splat | The walker counts a `*` splat as unproven too | K2's own principle: *shapes the walker cannot prove … count as unnamed*. A `*args` can carry the encoding's position. None in the tree |
| How a `.github/scripts/` site is named | Spec, Data & interfaces: product edits *add `encoding="utf-8"` … to existing calls* | `text=True` is replaced by `encoding="utf-8"` at all 14 sites | `encoding=` alone puts `subprocess` in text mode, so the pair says the same thing twice; `tests/conftest.py#git_listing` already spells it this way |
| `read_mark` exists twice | Spec D7 names `hooks/commit-review-gate.py#read_mark` | Fixed as named; `hooks/gate.py#read_mark` already reads `encoding="utf-8", errors="replace"` | Read at `1ecb019f`. The gate's copy is the shape the old one now matches |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite over this branch | the sealer, at its one broad run |
| The fixes on a real cp1252 interpreter | the pull request's `windows-latest` CI leg |
| `hooks/git/post-commit.py` writes its notice to stdout, which keeps `strict` errors under `PYTHONIOENCODING=ascii`, so before this work a non-ASCII notice there should have raised rather than degraded. Read, not executed: the call now reconfigures stdout first, and no case builds the notice's triggering state under an ASCII console | warden, round 1 |

## Not done

Nothing yet.

## Fed back into the spec

none
