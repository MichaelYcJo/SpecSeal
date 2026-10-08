## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 🟡 1 | fixed | 8645d9ea (the command's closing and docstring, the A1 pin, the changelog), 2f48cd68 (the box and its pin): a portal listing picks up each new version without a resubmission and goes live by its publish setting, which by default waits for somebody to select Publish |
| 🟡 2 | fixed | 8645d9ea: `claude.ai` leaves `ALLOWED_DOMAINS` for `ALLOWED_UNDER_PATHS`, allowed bare or under `/directory`; `test_the_product_host_is_allowed_bare_and_under_the_directory_only` refuses a share link, an address and a subdomain |
| 🟡 3 | fixed | 2f48cd68: the box heading reads *The marketplace files and the directory's page have been read*, and §6's opening says the second box reads what a script can and names the page that answers the rest; both pinned in the A5 box case |
| 🟡 4 | fixed | 2f48cd68: the fold's record line says a marketplace file pins a commit of each outside plugin's source repository, and the fixed-name paragraph says a marketplace file keys its entry on the name; pinned in the A8 cases |
| 🟡 5 | fixed | 2f48cd68: *one of the two once went twenty-eight days*; pinned in the A5 box case |
| ⬜ 6 | fixed | 8645d9ea: a `--root` with no readable manifest is `parser.error`, exit 2 with one line; `test_a_root_with_no_manifest_is_a_malformed_argument` |
| ⬜ 7 | fixed | 2f48cd68: `spec.md` (twice) and `questions.md` say *Anthropic's mail domain* and *the directory team's address* |
| ⬜ 8 | fixed | 2f48cd68: the bullet says a curated catalog and a nightly mirror (official README read 2026-10-08), and the third-reader sentence says *branch or tag* (`claude.com/docs/plugins/submit`, fetched 2026-10-08); the bullet pinned in the A7 case, the sentence left unpinned as A8 states. fb256f54 corrects the docstring's copy of the same claim, which `survivor-check` found |
