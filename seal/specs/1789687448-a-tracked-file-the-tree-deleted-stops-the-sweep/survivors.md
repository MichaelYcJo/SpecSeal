# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — survivors

<!-- Places `survivor-check` reports as still carrying wording this range
removed, which are correct reports and not defects. The quote is the anchor:
the exemption stops holding the moment that text changes. -->

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_payload_meter_says_what_it_measured.py` | `skills: [alpha, beta]` | The range rewrote `test_the_scan_covers_something`, whose two `assert … in files` lines became a `COVERED` tuple and a declining helper. The shared phrases the check found are `files assert skills` and `skill md in`, which fall across the seam between an assertion and the path `skills/implement/SKILL.md` on one side, and across a YAML flow-form frontmatter fixture on the other. The standing line is about a meter reading `skills: [a, b]` as a list; it is not a copy of any sentence this work removed, and nothing about it would become false if the rewritten case were reverted |
