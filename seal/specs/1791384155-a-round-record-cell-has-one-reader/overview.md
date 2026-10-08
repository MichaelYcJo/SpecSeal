# 1791384155-a-round-record-cell-has-one-reader — overview

## Why this work exists

Five judgments about a round record were each read by two to four scripts
that disagreed about the same cell; each now has one reader in
`chain_check.py`, so the gate, the generator, the broad gate's panel and the
release seal cannot give one cell two meanings.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The plan was written before #860, #837, #869 and #867 landed | `plan.md` §*Seams* names them as landing first / every phase was built on the release branch as merged at ad447367 | the tree as it is | the orchestrator's spawn: "Build each phase on the tree as it now is … record every divergence from the plan in `overview.md`" |
| The home reader is three functions, not two | J2: "a function deferred_home beside `verdict_of`, and issue_of over its answer" / `deferred_parts` returns the home and the note, `deferred_home` is its first half, `issue_of` reads the home | three | J2 also says the fix table takes "the home, with everything after the cut going to the note"; a second cut inside `fix_table` would be the copy this work removes |
| The layer the home's text loses | J2: "with the same two layers taken off (`EMPHASIS`, a trailing stop)" / `HOME_MARKS` (backticks, asterisks, an edge underscore) | `HOME_MARKS` | `EMPHASIS` removes every underscore, so `tests/test_x.py` read as `tests/testx.py`, which round 2 of #666 had fixed on the panel; the word itself is still matched through `EMPHASIS` by `verdict_of` |
| S4's Grounds cell | S4: "the Grounds cell `#854 — the run is capped; <reviewer's grounds>`" with a third cell `why` / `#854 — the run is capped — why; executed` | the third cell kept | the fix table's third cell is the fix pass's reasoning, which #391 part 1 made the generator keep; the spec's expected value dropped it silently |
| A bare `deferred` beside a home in the third cell | spec silent / the third cell is read as if the word stood before it | through `deferred_parts` | it used to write the whole third cell into the Verdict cell, the shape S4 removes for the other arm |
| The release seal's S10 fixture | spec silent / `**deferred** #13, #14` became two cells | changed | `#13, #14` is not a home `issue_of` reads as an issue, and keeping the case's three issues needs one per cell |
| `landings`' flag | J3 names only `depth_two` as the wide reader's caller / `landings` reached `path_forms` through it with `paths_only=True` | `landings` calls `path_forms` directly | the flag chose between two readers, and one of them left |
| A comment in `evidence_check.py` | spec silent / it named one of the five patterns as a second reader of the same shape | reworded | §12: the sentence was false once the pattern left |
| The suite's pull request | spec silent; J4 says the population with no payload and no `gh` that answers now exits 1 / the suite is that population (logged out, #510), 176 cases failed | a stub `gh` in `tests/conftest.py` answers draft for every case, `gh_answers` picks another | the generator assumed draft for the suite before; a case about ready or unknown now says so, and no case reaches a live `gh` for the question |
| How `gh` is run | J4: "the exact call `pull_request_is_ready` makes today" / the path `shutil.which` found, not the bare name | the found path | a `gh.cmd` on Windows is found by `which` and not by a process call naming `gh` |
| `--sealing`'s reach | J4: "the `Broad gate` arm of the last record" / also the direct `broad-gate.md` home | both homes | the gate writes the cell into whichever home `seal` uses, and the draft payload excused both before |
| The environment-leak case (W2) | a failure to re-pin / the judgment's source | the source | under `--sealing` the leaked payload fails nothing; the kept output still shows which pull request judged the fixture |
| The panel's ASCII | spec silent / the home is ASCII-encoded in `rounds_rows`, not in the reader | in the panel | the letter twin maps only the owner's characters; the gate and the release seal want the home as written |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at this branch's head | the sealer, after the review rounds settle |

## Not done

- The release branch carries 33 drifted ledger rows on four coordinates no
  phase of this work edits — `agents/warden.md#"## Report"` (8),
  `templates/config.md#"# Repository config"` (14),
  `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` (10)
  and `skills/verify/scripts/payload_meter.py#heading_starts` (1) — measured
  on an archive of `origin/release/v0.21.0`. Nobody on this branch read their
  claims, so no row here re-reads them, and `evidence-check --strict` exits 2
  on this branch for them alone.

## Fed back into the spec

- *Inferred during implementation:* a deferral's home loses `HOME_MARKS`, not
  `EMPHASIS`, and a bare `deferred` reads its home from the third cell
  through the same grammar.
