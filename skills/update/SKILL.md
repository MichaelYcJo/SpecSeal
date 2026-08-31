---
name: update
description: Update the plugin to the newest release and say what changed — runs both commands in the right order, then names the entries you are getting.
disable-model-invocation: true
---

# /specseal:update — take the release, and see what is in it

Two commands in a fixed order, and one thing neither of them does: tell you
what you are getting. Running them by hand answers "you are now on <version>",
which is a number, not a reason to restart.

## Procedure

**1. Record what is running.** Read the `version` from
`$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json`. This is the version this
session actually loaded, which is the one the user is comparing against.

**2. Refresh the marketplace, then install.**

```bash
claude plugin marketplace update specseal
claude plugin update specseal@specseal
```

Both, in that order. The first pulls the marketplace clone; the second
installs from it. Running only the second reports *already at the latest
version* against whatever the clone last knew — the failure is silent and
looks like success.

If the second command reports it is already current, say so and stop. There is
nothing to restart for.

**3. Name what changed.** Read `CHANGELOG.md` from the refreshed marketplace
clone — `~/.claude/plugins/marketplaces/specseal/CHANGELOG.md` — and summarize
every entry between the old version and the new one, oldest first. Lead each
with what it changes for the user, not with the release number.

Two kinds deserve to be called out on their own line, because a user who skips
them gets surprised later:

- **behavior that changes without being asked for** — a new gate, a gate that
  fires where it did not, anything that writes to their tree
- **anything they have to do** — a path that moved, a setting that was renamed,
  a compatibility fallback with an expiry

**4. Take the preset block if it moved.** The markers decide what is safe here.
Everything between `<!-- specseal:start -->` and `<!-- specseal:end -->` is
preset-owned and everything outside it is the user's, so replacing the region
cannot touch a line they wrote. `install.sh` relies on that boundary and so
does `preset-setup`, which replaces an older block without asking and diffs
only the remainder.

`claude plugin update` installs agents, skills, and hooks and never opens
`CLAUDE.md`, so without this step a release changes a rule while the
always-loaded file keeps stating the old one. Measured on this repository: the
block changed in two of thirteen releases, and the first went four releases
before anyone noticed.

```bash
diff <(sed -n '/specseal:start/,/specseal:end/p' ~/.claude/plugins/marketplaces/specseal/CLAUDE.md) \
     <(sed -n '/specseal:start/,/specseal:end/p' ~/.claude/CLAUDE.md)
```

Compare the scope that holds the block — `./CLAUDE.md` instead when the project
owns it.

| Result | What happens |
|---|---|
| No difference | nothing is said; the block is current |
| The block differs | back up to `CLAUDE.md.bak`, replace the marker region, and name the rules that arrived. No question is asked, because the markers already say those bytes were never the user's |
| No block on the machine | they never installed the preset. Say so and stop — writing one in is an install, and an update is what was asked for |

One case still needs a person. If a rule that just arrived also appears in the
user's own text outside the markers, the file now states it twice, and the copy
to remove is theirs. Name the overlap and point at `/specseal:preset-setup`,
which classifies it and proposes the deletion through an approved diff.

**5. Say that a restart is needed, and why it is safe to finish first.** The
running session keeps the version it started with: the old directory stays in
the plugin cache and `$CLAUDE_PLUGIN_ROOT` still resolves to it. Nothing is
half-updated and nothing breaks mid-session — the new version simply is not
loaded until Claude Code restarts.

## What this does not do

**It does not restart anything.** Ending a session is the user's call and
their unfinished work is in it.

**It does not delete anything the user wrote.** The preset block is replaced
inside its markers, which is the whole of what the plugin owns. An overlap with
their own text outside the markers is reported, never resolved — that deletion
goes through `preset-setup`'s approved diff.

**It does not decide the update is wanted.** If a release changes behavior the
user relies on, the summary in step 3 is where they find that out — which is
why the summary comes with the update rather than after it.

## Output

```
Updated: <old> → <new>            (or: already on <version>, nothing to do)

What you are getting:
- <what changes for the user> (<version>)
- ...

Needs action:                     (omit when there is none)
- <what moved, what to set, what expires when>

Restart Claude Code to load it. This session keeps running <old> until then —
the old version stays in the cache, so nothing is half-applied.
```
