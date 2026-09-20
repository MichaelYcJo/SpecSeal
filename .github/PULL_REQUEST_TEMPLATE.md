<!-- BASE BRANCH — the one thing to check before anything below.

Base this on the open `release/vX.Y.Z` branch, not on `main`. It is the only
branch beginning `release/` in the dropdown to the left of this box, and
`main` is what GitHub offers by default.

A pull request into `main` is a release here. If yours touches what the plugin
ships, CI refuses it for leaving `.claude-plugin/plugin.json` alone; if it does
not, nothing catches the wrong base at all. Either way the base is the cause,
not the version — change the base rather than that file.
Already opened against `main`? The Edit button beside the title changes the
base without closing anything.

The rest is in CONTRIBUTING.md, "Opening a pull request", including what a
contribution is NOT asked for: no work item under seal/specs/, no review
round record, no ledger row, no changelog fragment, and no version bump. -->

## What changes

<!-- One or two sentences on what is different afterwards. Not which files
moved — the diff lists those already. -->

## How it was verified

<!-- The command you ran and what it said. `bin/test tests/<file> -q` on the
module you touched is enough; CI runs the rest on three platforms. Say which
things you read rather than ran. -->

<!-- CHANGING A GATE? Anything under hooks/ or .github/workflows/ carries a
higher bar, because a gate decides whether somebody else's commit proceeds.
Add: the test seen failing before the fix, which way the change leans
(refusing more, or letting more through), whether it puts a new question in
front of a person, and the platforms you could not test. CONTRIBUTING.md,
"What a change to a gate must carry", is the whole of it. -->
