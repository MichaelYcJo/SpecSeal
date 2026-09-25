# Survivors — a ledger row that will not parse is counted

`survivor-check --range 0abfb371..HEAD`, run at `b94697c3` after the build's
three phases, reported four places. The removed wording came from two places.
One is the rider-stamp row this branch removed from `seal/ledger.md`, whose
claim had been false since #239. The other is `seal/follow-up.md`'s #299 row,
which this work item closes. None of the four places is a claim the range
corrected.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/spec.md` | `tests/test_a_rider_reaches_its_file.py#"STAMP = re.compile(r"Verified …")"@05033bb1` | the frame's table of the live instances, quoting the coordinate as it stood when the framer measured it; a record of what was found, not a claim about the tree |
| `.github/scripts/rider_check.py` | r"Verified (?P<date>\d{4}-\d{2}-\d{2}) at (?P<sha>[0-9a-f]{7,40})\b" | `OLD_STAMP`, the pre-#239 stamp form the checker keeps so it can name a stamp that still uses it; it shares the regex with the removed row's quoted line and states nothing that row claimed |
| `seal/releases/0.12.1.md` | a row names content and never a position | another row's own note on `survivors.md`; it shares only this house phrase with the removed follow-up row |
| `seal/follow-up.md` | **No coordinate is repeated in this row, on purpose**: the rule above sends anything tied to one to a `# RIDER:` | another follow-up row's own note; it shares only the phrasing about riders with the removed #299 row |
