# Survivors — a unit the extractor cannot bound is refused

`survivor-check --range origin/release/v0.21.0...HEAD` names each place that
still carries wording this item's range removed. Each row below was read at
the branch's head, and its grounds say why the standing text stays.

| Path | Quote | Grounds |
|---|---|---|
| `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` | `seal/releases/0.16.0.md#"### 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated">"H1 · every split"@098baf93` | #867's `Re-read · H1` row, a reading dated 2026-10-08 at the hashes it held then. Its family's newest reading is this item's own `Re-read · H1` row in `seal/ledger/1791384159-a-unit-the-extractor-cannot-bound-is-refused.md`, at the rewritten units' hashes, and `--strict` reads the family OK; re-stamping an older reading would rewrite what #867 recorded |
