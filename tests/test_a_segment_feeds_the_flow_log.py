"""Issue #109 part 1: the instruction "measure every smith/warden segment and
log what it found" used to live only in a person's message
(`~/.claude/projects/.../memory/measure-every-segment-to-89.md`), retyped
every session and naming a hardcoded issue number that goes stale the moment
that issue closes. It moves into `skills/verify/SKILL.md`, between
`## Seal block` and `## Counterfeits (stop on sight)`, so a session does it
because the skill says so, and the destination becomes a
`flow-measurement`-labelled GitHub issue instead of a number.

This module pins three things a session reading that section needs: both
commands are named (`session_cost.py` and the `gh issue list --label
flow-measurement --state open` lookup), and the no-op case is stated
explicitly — most installed repositories never create the label, so the
common case is that this section does nothing, and the section has to say so
rather than leave a reader to infer it from silence.

`skills/verify/SKILL.md` carries no HTML comments anywhere in the file
(checked directly, not assumed) — so unlike
`tests/test_a_phase_hands_the_next_one_a_record.py`'s template pins, this
module does not need a comment-stripping reader; a plain substring check
already means "outside any comment", matching
`tests/test_review_axes.py`'s style for the same reason (the source here is
skill prose, not a template with placeholders).

Issue #136 adds a second destination and a second zero. Two issues collect
measurements in the same shape and one of them is deleted at every release, so
the section now says which reading goes to which — a segment's own numbers to
the rolling `flow-measurement` log, a reading that only means something across
versions to the durable `flow-baseline` one — and separates a repository that
never measured from one whose log stopped. The cases below pin both labels,
the rule that separates them, the `--state all` lookup that tells the two
zeroes apart, and the refusal that keeps a session from repairing the second.

They also pin what the section may NOT say. This file ships to repositories
that have neither this repository's `measurement` index label nor its
`log: measurement` milestone nor its durable issue number, so those three are
`.github/scripts/`'s to name and not the skill's —
`tests/test_the_release_check_watches_what_ships.py` is what classifies that
directory as staying home.

Issue #170 adds a second reading to the same section, one level up. Everything
above it measures one segment; a run is every segment plus the rounds and the
commits between them, and no segment's numbers say what the run cost. So the
section now states the run-level comparison table — its rows, what each row is
taken from, and the three sentences that keep it comparable: the tokens are
counted rather than estimated and counted the same way every time, a run whose
transcript covered only part of its branch says so in the prose rather than in
a column, and the table itself carries no verdict. The cases below pin each of
those, and one of them is structural rather than textual — every row of the
table must name a source, because a row nobody can reproduce is a row the next
run fills in by feel.
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, "skills", "verify", "SKILL.md")

SECTION_HEADING = "## Measure the segment, and feed the flow log"


def read():
    with open(SKILL, encoding="utf-8") as f:
        return f.read()


def section_body():
    """Whitespace-collapsed, so a substring check does not break every time
    the prose re-wraps at a different column — the wording is what these
    tests pin, not which line a hyphen happens to fall on."""
    text = read()
    start = text.index(SECTION_HEADING)
    rest = text[start + len(SECTION_HEADING) :]
    next_heading = rest.index("\n## ")
    return " ".join(rest[:next_heading].split())


def section_text():
    """The section with its lines intact. `section_body` collapses whitespace,
    which is right for prose and wrong for a table whose rows are lines."""
    text = read()
    start = text.index(SECTION_HEADING)
    rest = text[start + len(SECTION_HEADING) :]
    return rest[: rest.index("\n## ")]


RUN_TABLE_HEADER = "| Row | Taken from |"

RUN_TABLE_ROWS = (
    "Rounds",
    "Wall clock",
    "Commits, by kind",
    "Findings by severity",
    "Findings by `Location`",
    "Records' share of the diff",
    "Model turns",
    "Segments",
    "Broad gate",
)


def run_table_rows():
    """The run-level table's data rows, as `[row label, source]` pairs."""
    lines = section_text().splitlines()
    assert RUN_TABLE_HEADER in lines, (
        "the section carries no run-level table — `" + RUN_TABLE_HEADER + "` "
        "is the header row every case below reads"
    )
    rows = []
    for line in lines[lines.index(RUN_TABLE_HEADER) + 2 :]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def test_skill_has_no_html_comments_at_all():
    """The premise the rest of this module leans on: with zero `<!--` in the
    whole file, a plain substring match already means "outside any HTML
    comment" — there is no comment for the section to hide inside."""
    assert "<!--" not in read(), (
        "skills/verify/SKILL.md now has HTML comments — this module's plain "
        "substring checks no longer prove the section sits outside them; "
        "switch to a comment-stripping reader like "
        "tests/test_a_phase_hands_the_next_one_a_record.py does"
    )


def test_the_section_exists_between_seal_block_and_counterfeits():
    text = read()
    seal_idx = text.index("## Seal block")
    section_idx = text.index(SECTION_HEADING)
    counterfeits_idx = text.index("## Counterfeits (stop on sight)")
    assert seal_idx < section_idx < counterfeits_idx, (
        "the flow-log section must sit between `## Seal block` and "
        "`## Counterfeits (stop on sight)` — that is the placement `plan.md` "
        "fixed for phase 1"
    )


def test_the_section_names_the_measure_step():
    body = section_body()
    assert "session_cost.py" in body, (
        "the section never names `session_cost.py` — a session reading it "
        "has no command to run against the segment's transcript"
    )


def test_the_section_names_the_lookup_command():
    body = section_body()
    assert "gh issue list --label flow-measurement --state open" in body, (
        "the section never names the exact lookup command — a session would "
        "have to guess how to find the destination issue rather than being "
        "told"
    )


def test_the_section_names_the_post_command():
    body = section_body()
    assert "gh issue comment" in body and "--body-file" in body, (
        "the section never names how to post the measurement — "
        "`gh issue comment <n> --body-file <file>`"
    )


def test_the_section_states_an_absent_label_is_a_no_op():
    body = section_body()
    assert "no-op" in body, (
        "the section must say explicitly that an absent "
        "`flow-measurement` issue makes this a no-op — silence here reads "
        "as an unhandled case, not as 'nothing to do', and most installed "
        "repositories will hit exactly this branch"
    )
    for phrase in ("nothing is posted", "nothing fails", "nothing asks"):
        assert phrase in body, f"the no-op sentence lost `{phrase}`"


def test_the_section_says_it_happens_without_asking():
    body = section_body()
    assert "never" in body and "question" in body, (
        "the section must say the post happens without asking — otherwise a "
        "session reading it may treat the destination issue as something "
        "requiring approval, reintroducing the prompt #109 exists to remove"
    )


def test_the_section_names_the_durable_logs_label():
    body = section_body()
    assert "flow-baseline" in body, (
        "the section never names `flow-baseline`, so a reading that only "
        "means something across versions has nowhere to go but the rolling "
        "log — which is deleted when the version ships. That happened on "
        "2026-09-04 and is what #136 opened for"
    )


def test_the_section_says_what_separates_the_two_logs():
    """Naming both labels is not the same as saying which gets what. A session
    with two destinations and no rule picks by feel, which is the state before
    this section named either of them."""
    body = section_body()
    assert "span versions" in body, (
        "the section names the two logs but never says what separates them — "
        "a reading that spans versions is the one that must not go to the "
        "log that is discarded"
    )
    assert "discarded" in body, (
        "the section must say the rolling log is discarded at the release; "
        "that is the whole reason the durable one exists, and without it the "
        "split reads as an arbitrary filing convention"
    )


def test_the_section_separates_the_two_zeroes():
    body = section_body()
    assert "gh issue list --label flow-measurement --state all" in body, (
        "the section must name the `--state all` lookup. A repository that "
        "never measured and one whose log stopped both read zero open, and "
        "the first is a no-op while the second is a broken invariant — one "
        "call tells them apart"
    )


def test_a_session_names_the_stopped_log_rather_than_opening_one():
    """The obvious next step — if none is open, open one — is what breaks the
    invariant the release-time roll depends on."""
    body = section_body()
    assert "not a session's act" in body, (
        "the section must refuse outright: a session that finds the label "
        "with a history and nothing open names it and opens nothing"
    )
    assert "two or more" in body, (
        "the refusal must carry its reason — two sessions finishing segments "
        "at the same moment both read zero and both create, and the next "
        "release then fails on two or more. Without the reason the refusal "
        "reads as caution and the next reader talks themselves out of it"
    )


def test_the_sections_opening_sentence_names_no_single_destination():
    """#136's own body quotes this sentence as the defect, and adding a
    paragraph below it does not repair it. The opening is imperative and
    complete, so a session that skims the heading and the first sentence does
    the pre-#136 thing with the rest of the section unread."""
    body = section_body()
    opening = body.split("**")[0]
    assert "flow-measurement" not in opening, (
        "the section still opens by telling a session to post to the "
        "`flow-measurement` log. Whichever label the first sentence names is "
        "the destination a skimming reader uses, and naming one of two is "
        "the instruction #136 exists to correct"
    )
    assert "two" in opening, (
        "the opening must say there is more than one log. A reader who goes "
        "no further has to at least know a choice is being made for them"
    )


def test_the_durable_log_gets_the_same_two_zeroes():
    """The section gives both labels the same exactly-one-open invariant and
    then hands only one of them the `--state all` split. A durable ledger
    somebody closed by hand then reads exactly like a repository that never
    measured, which is #136's own failure recurring one label over."""
    body = section_body()
    assert "somebody closed the durable ledger" in body, (
        "the section never says what a `flow-baseline` label with a history "
        "and nothing open means, so the one reading that survives it -- the "
        "cross-version one -- is silently dropped"
    )
    assert "is the first of those and nothing more" not in body, (
        "the sentence folding `flow-baseline`'s zero into the harmless case "
        "is back. It is the fold that makes a closed durable ledger "
        "indistinguishable from a repository that never had one"
    )


def test_the_shipped_skill_names_no_repository_specific_tracker_state():
    """This skill ships. `flow-measurement` and `flow-baseline` are the
    plugin's vocabulary and belong here; the `measurement` index label, the
    `log: measurement` milestone and the durable issue's number are this
    repository's own and belong in `.github/scripts/`, which
    `tests/test_the_release_check_watches_what_ships.py` classifies as staying
    home."""
    text = read()
    assert "log: measurement" not in text, (
        "the shipped skill names this repository's own milestone — an "
        "installed repository has no such milestone and cannot act on it"
    )
    assert "#51" not in text, (
        "the shipped skill hardcodes this repository's durable issue number. "
        "A number is what #109 removed from the rolling log's lookup for the "
        "same reason: it goes stale, and it means nothing anywhere else"
    )
    assert "`measurement`" not in section_body(), (
        "the section names the bare `measurement` index label, which exists "
        "in this repository only. The two labels a shipped skill may name are "
        "`flow-measurement` and `flow-baseline`"
    )


def test_the_section_states_the_run_level_table():
    assert RUN_TABLE_HEADER in section_text(), (
        "the section says what one segment's reading is and where it goes, "
        "and never says what a whole run's report carries. Without the table "
        "each run invents its own shape and two runs cannot be read side by "
        "side"
    )


def test_the_run_level_table_carries_every_row():
    labels = [row[0] for row in run_table_rows()]
    for expected in RUN_TABLE_ROWS:
        assert any(expected in label for label in labels), (
            f"the run-level table has no `{expected}` row. The rows are the "
            "whole point of stating the table: a run that drops one is a run "
            "the next comparison cannot line up against"
        )


def test_every_row_of_the_run_level_table_names_its_source():
    """Structural rather than textual. A row with no source is a number the
    next run produces by feel, which is exactly what one stated shape is for."""
    for row in run_table_rows():
        assert len(row) == 2 and row[1], (
            f"the run-level table's `{row[0]}` row names no source. Every row "
            "must say where its number is taken from, or the next run guesses"
        )


def test_the_token_row_names_the_command_that_prints_it():
    token_rows = [row for row in run_table_rows() if "Model turns" in row[0]]
    assert token_rows, "the run-level table lost its token row"
    assert "session_cost.py" in token_rows[0][1], (
        "the token row does not name `session_cost.py`. It is the one row "
        "nobody can produce by hand, and a run that sums `usage` with a "
        "script written for the occasion produces a number the next run "
        "cannot be compared against"
    )


def test_the_tokens_are_counted_rather_than_estimated():
    body = section_body()
    assert "counted, not estimated" in body, (
        "the section must say the tokens are counted, not estimated — an "
        "estimate in the token row makes every comparison against it wrong "
        "by an unknown amount"
    )
    for field in (
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    ):
        assert field in body, (
            f"the counting rule never names `{field}`, so 'the same way every "
            "time' is not something a reader can check"
        )


def test_partial_coverage_is_stated_in_the_prose_and_not_as_a_column():
    """`questions.md` assumption 6: a column would make it a parsed field, and
    the number still has to be qualified where a person reads it."""
    body = section_body()
    assert "only part of its branch" in body, (
        "the section never says what to do when a run's transcript covered "
        "only part of its branch. The number is then smaller than the run, "
        "and a comparison against a whole one reads as an improvement"
    )
    assert "rather than as a column" in body, (
        "the partial-coverage note must be stated as prose beside the table "
        "rather than as a column of it"
    )
    labels = [row[0].lower() for row in run_table_rows()]
    assert not any("coverage" in label for label in labels), (
        "coverage became a column of the run-level table. Assumption 6 keeps "
        "it in the prose: a column is a field, and this one is a caveat"
    )


def test_the_table_carries_no_verdict():
    body = section_body()
    assert "carries no verdict" in body, (
        "the section must say the table carries no verdict — #170's own "
        "*Not this*. A table that judges is one the next run argues with "
        "before it can compare anything"
    )
    assert "never in a column" in body, (
        "the section must send what a row meant on one branch to the comment "
        "beside the table rather than into a column of it"
    )


def test_the_table_is_the_runs_reading_where_the_rest_is_one_segments():
    """The two readings live in one section, so the section has to say which
    level each is taken at — otherwise the table reads as a fourth thing to
    measure per segment."""
    body = section_body()
    assert "measures one segment" in body, (
        "the section never says that everything above the table is one "
        "segment's reading, so a reader cannot tell what level the table is "
        "taken at"
    )
    assert "this run beside the last run measured" in body, (
        "the section never says the table holds two runs side by side. One "
        "run's numbers alone are a record, not a comparison"
    )


def test_the_table_is_not_a_third_destination():
    body = section_body()
    assert "not a third destination" in body, (
        "the section names two logs and then adds a table without saying "
        "where it goes. It goes to the rolling log the section already "
        "names — a reader left to guess invents a third place"
    )


def labelled(fragment):
    """The one run-level row whose label carries `fragment`, as [label, source]."""
    rows = [row for row in run_table_rows() if fragment in row[0]]
    assert len(rows) == 1, (
        f"expected exactly one run-level row labelled {fragment!r}, found "
        f"{len(rows)}. A row renamed has to bring its case with it"
    )
    return rows[0]


def test_the_location_buckets_are_the_repositorys_own_definition_of_a_record():
    """Round 1's finding 3. The row split `ledger` from `record` and the share
    row counted only `seal/specs/**`, where the review chain's own definition
    puts a work item's documents, the ledger and its fragments in ONE bucket:
    a finding in any of them is about the run's paperwork rather than about
    the tool. Two definitions of one word made the same run's share row read
    45 % as the row was written and 48 % under the policy — and a table exists
    to be comparable, which two fillings of one row destroy.

    A ticket is a request and a ratified document outranks it, so the buckets
    follow the policy. `overview.md` §*Where spec and implementation diverged*
    quotes both sides."""
    label, source = labelled("Findings by `Location`")
    assert "ledger" not in label, (
        "the `Location` row still lists `ledger` as a bucket of its own. The "
        "ledger and its fragments are records, so a finding in one lands in "
        "two buckets and the column no longer adds up"
    )
    assert "`seal/`" in source, (
        "the `Location` row names four buckets and nowhere says what a record "
        "is, which is the whole of what the two fillings disagreed about"
    )
    share_source = labelled("Records' share")[1]
    assert "seal/specs" not in share_source, (
        "the share row counts `seal/specs/**` alone, so a branch that wrote "
        "ledger rows reads as having written less paperwork than it did"
    )


def test_the_broad_gate_row_asks_for_what_the_cell_actually_carries():
    """Round 1's finding 4. The row asked for `how many times, at what SHA`
    from a cell that holds one entry — `round_record.py` replaces it rather
    than appending — so a run that ran the gate twice had nowhere in the
    record to say so and the row was filled from memory or left blank."""
    label, source = labelled("Broad gate")
    assert "how many times" not in label, (
        "the `Broad gate` row asks for a count. The cell it names carries at "
        "most one SHA, so the count comes from somewhere the next run cannot "
        "check"
    )
    assert "not yet" in source, (
        "the row names the cell without saying what it holds, which is the "
        "reason the count went unnoticed in the first place"
    )


def test_the_section_says_which_transcript_is_the_runs_own():
    """Round 1's finding 7. The token row is taken over *the run's main
    transcript* and nothing said which file that is. `--latest` walks the
    whole project directory and takes the newest file, which on a run that
    spawned segments is a segment — measured, on this very work item: it
    landed on a subagent transcript and the token line read `1 transcript`
    for a run with several."""
    body = section_body()
    assert "sitting directly under the project directory" in body, (
        "the section asks for the run's main transcript and never says where "
        "one is, so the reader takes whatever `--latest` hands them"
    )
    assert "lands on a segment" in body, (
        "the section never says `--latest` can land on a segment, which is "
        "the ordinary case on a run that spawned any"
    )
