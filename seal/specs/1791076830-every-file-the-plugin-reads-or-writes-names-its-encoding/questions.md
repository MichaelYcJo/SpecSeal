# every file the plugin reads or writes names its encoding (#741) — questions for the planner

<!-- seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/questions.md
     The run is unattended (routing.md: Automation yes, Answer pressed
     automation), and the owner answered once, for all of milestone 53. So no
     row here waits on a person. Each row a person would decide is decided by
     this frame, with the answer written in and the grounds in spec.md, and a
     person may overturn it by opening what the frame opened. -->

**Judgments the ticket left open that the tree answered.** They are listed so
nobody reopens them. Each one's grounds are in `spec.md`.

- **How the check is delivered.** A test module, as every hygiene check on
  the plugin's own source already is; `bin/` is the users' surface (D1).
- **Whether ruff's `PLW1514` is turned on beside it.** No: preview-only, blind
  to most of the class by the ticket's account, and a second instrument that
  disagrees (D1, plan.md A1, A2).
- **The corpus.** Every tracked `.py`, which equals the issue's four roots
  today and covers a fifth on arrival (D2, K4).
- **The allowlist's shape.** Keyed by unit (`path#qualname`), with grounds,
  and a liveness half, copied from `tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED` (D4).
- **What counts as naming.** Any `encoding` but `None`; the repair written is
  `encoding="utf-8"` (K1, D3).
- **Whether the 9 empty-marker `open(path, "w").close()` sites are fixed or
  listed.** Fixed (D3, plan.md A8).
- **Whether `hooks/dispatch.py`'s inline loop is rewritten to call
  `console.to_utf8()`.** No; classified, because three behavioural cases
  already hold it (D5).
- **Whether the entry-point half reaches `.github/scripts/`.** No. #741 says
  *hook entry point*, and `seal/follow-up.md` already holds that widening as
  the repository owner's question. This work leaves the row as it is.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Is the entry-point half an AST order assertion or a behavioural case per entry point? | a person: decided by frame | **AST: the `__main__` block's first statement is `console.to_utf8()`.** Uniform over 22 files, red by deleting or moving the call. The call's own working is held by the existing behavioural cases. **Behavioural per entry point.** Each hook returns silently on undecodable stdin and silently when nothing applies, so a uniform case is green without the call; it needs each hook's own triggering state, 21 fixtures | AST (D5) | decided by frame 2026-10-04 |
| Q2 | Does a read converted to UTF-8 inside a hook keep strict errors? | a person: decided by frame | **Not where it would newly raise.** A raise in a hook reaches `dispatch.py`'s `except Exception`, which is an allow, so a hook read either sits in a handler catching `ValueError` or adds `errors="replace"`. **Strict everywhere.** Uniform, but a non-UTF-8 byte in a mark or lease file on a cp1252 machine, harmless today, becomes a silent allow | Not where it would newly raise; strict outside `hooks/` (D7) | decided by frame 2026-10-04 |
| Q3 | Are product and test sites fixed in one phase or two? | a person: decided by frame | **Two.** The product edits, where Q2's failure direction matters, reach review apart from 302 mechanical test edits. **One.** Fewer commits, and the product edits hide in the bulk | Two (plan.md A9) | decided by frame 2026-10-04 |
| M1 | How many sites does the smith's walker name, against the census's 29 product and 302 test? | a measurement | The census matched subprocess calls by function name and flagged `os.fdopen` loosely (four false positives it then read away). The walker resolves imports, so its count may differ by a few. Nothing built changes; the walker's count is the one of record | The walker's count, stated in `phases/phase-1.md` and `phase-2.md` | ⬜ product half measured 2026-10-04: 29, equal to the census — `phases/phase-1.md`; the test half is phase 2's |
| M2 | Does ruff `PLW1514` (preview) miss `Path.read_text` / `write_text` called on a variable, as the ticket says? | a measurement | One `uvx ruff check --preview --select PLW1514` over a two-line file. A1 is rejected on two other grounds either way, so the answer changes nothing built; it decides only whether the module docstring may repeat the ticket's sentence as measured | The docstring cites it as the ticket's account until measured | ✅ measured 2026-10-04 on ruff 0.16.10: `p.read_text()` and `p.write_text(s)` pass, `Path("x").read_text()` is reported; the docstring states it as measured — `phases/phase-1.md` |
| M3 | Which released ledger rows do the phase 1 and phase 2 edits drift? | a measurement | `bin/evidence-check .` after phase 2. The upper bound, read off the anchors, is every released row whose unit encloses an edited call; the census's product files carry 136 distinct released anchors between them, most on units no edit touches | Phase 3 writes a `Re-read ·` row for each row the tool names, after reading it | ⬜ |
| M4 | Does the unfixed `hooks/git/pre-commit.py`, refusing a commit under `PYTHONIOENCODING=ascii`, die with `UnicodeEncodeError`? | a measurement | Read, not executed: `hooks/gate.py:182` puts U+2026 in the refusal's waiver. **Yes:** S8 is planted, red against the unfixed hook. **No** (the refusal text that path prints is ASCII): S8 cannot be seen red and is not planted, and S7 alone holds the three git hooks | Measure in phase 1 before planting S8 | ✅ measured 2026-10-04: no traceback; the refusal arrives with `\u2014` / `\u2026` escapes, so S8 is planted as *the refusal arrives as written*, red against the unfixed hook — `phases/phase-1.md` |
| W1 | For each of the 15 hook sites, does the surrounding handler already catch `ValueError`, or does it need `errors="replace"`? | the work | Read at `4d2afd1e`: the two JSON reads in `hooks/worktree-guard.py` catch `Exception`; `hooks/commit-review-gate.py#read_mark` catches `OSError` only. The 9 `open(..., "w").close()` markers and the writes cannot raise on encoding. `hooks/version-check.py`'s `plugin.json` read is the other one to open | D7 per site | ✅ read 2026-10-04: only `read_mark` needed `errors="replace"`; `version-check.py#running` catches `ValueError` — `phases/phase-1.md` |
| W2 | Does any test site deliberately exercise the locale default, so naming UTF-8 would defeat it? | the work | None was seen in the census's file list. A test of locale behaviour would spell it with a subprocess and an `LC_ALL`, not an unnamed call; if one is found, it is classified in `ALLOWED` with that as grounds | Fix; classify only on grounds | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
