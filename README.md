# claude_preset

Research-backed, minimal Claude Code preset. **81% fewer always-loaded tokens** than typical presets.

[한국어](./README.ko.md)

## Why

Based on [arxiv 2602.11988](https://arxiv.org/abs/2602.11988):
- Context files can **decrease** task success by ~2%
- Reasoning cost increases 20-23% with redundant instructions
- Claude already knows SOLID, DRY, "read before edit", etc.
- **Only include what changes Claude's default behavior**

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| CLAUDE.md | 1 | Always-loaded (~350 tokens). Language, tooling, safety rules |
| Rules | 4 | Contextual loading. Engineering, safety, workflow, orchestration |
| Skills | 10 | 0-token when idle. Auto-trigger on keywords |
| Commands | 20 | Slash commands for specific tasks |
| Agents | 8 | Specialized worker templates |

### Always-Loaded (CLAUDE.md, ~350 tokens)

Only rules that **change Claude's default behavior**:
- Korean language response
- `uv`/`pnpm` preference
- Engineering defaults reminder (SOLID, DRY, KISS — single line)
- 3+ Fix Rule (stop after 3 failed attempts)
- Verification Gate (no completion claims without evidence)
- Two-Stage Review (spec compliance → code quality)
- Orchestrator/Worker agent pattern
- Skill auto-trigger rules

### Rules (contextual loading, 0-token when idle)

| File | Purpose |
|------|---------|
| `safety.md` | 3+ Fix Rule details, Verification Gate details, security checklist |
| `quality.md` | SOLID/DRY/KISS details, implementation completeness, scope discipline |
| `orchestration.md` | Orchestrator/Worker role separation, agent templates, model selection |
| `workflow.md` | Two-Stage Review details, PDCA, parallel planning, Git workflow |

### Skills (auto-trigger)

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/confidence-check` | implement, create, build | Pre-implementation assessment |
| `/verify` | done, complete, PR | Post-completion verification |
| `/build-fix` | build errors | Systematic error resolution |
| `/checkpoint` | refactor, delete, migrate | Safety checkpoint |
| `/debug` | test failures | Systematic debugging |
| `/code-review` | review request | Structured code review |
| `/learn` | problem solved | Capture insights |
| `/feature-planner` | new feature (>3 files) | Implementation planning |
| `/gap-analysis` | design vs implementation | Spec comparison |
| `/audit` | commit, PR | Project rule validation |

### Commands

| Category | Commands |
|----------|----------|
| Analysis | `/debug`, `/code-review`, `/code-smell` |
| Architecture | `/architecture`, `/api-design`, `/db-design` |
| Quality | `/testing`, `/refactoring`, `/clean-code` |
| Security | `/security-audit`, `/auth` |
| Framework | `/nextjs`, `/fastapi`, `/react-best-practices` |
| Infra | `/docker`, `/cicd`, `/monitoring` |
| Other | `/naming`, `/error-handling`, `/python-best-practices` |

### Agents

| Agent | Role |
|-------|------|
| `backend-architect` | API, DB, server design |
| `frontend-architect` | UI/UX, component architecture |
| `system-architect` | System-level architecture |
| `security-engineer` | Security review |
| `quality-engineer` | Testing, QA |
| `python-expert` | Python-specific expertise |
| `performance-engineer` | Performance optimization |
| `technical-writer` | Documentation |

## Install

```bash
git clone https://github.com/USERNAME/claude_preset.git
cd claude_preset
bash install.sh
```

The installer will:
1. Back up your existing `~/.claude/` configuration
2. Install CLAUDE.md, rules, skills, commands, agents
3. Merge hooks into your `settings.json` (preserves existing settings)

## Uninstall

```bash
bash uninstall.sh
```

Backs up current config and offers to restore your previous configuration.

## Philosophy

> "Does Claude already do this by default?"

Every line in CLAUDE.md passes this test. If Claude already knows it (snake_case for Python, "use feature branches"), it's not included. Only behavioral overrides that change Claude's defaults are kept.

Principles Claude "knows but doesn't always apply" (SOLID, DRY, etc.) are kept as a single-line reminder in CLAUDE.md, with detailed rules loaded contextually from the `rules/` directory. **Strip the explanations, keep only the directives.**

### Include / Exclude Criteria

| Include (any match) | Exclude (any match) |
|---|---|
| Directives that change default behavior | Already built into the system prompt |
| Specific thresholds/criteria | Default language/framework conventions |
| Unique workflows | "Explanatory" directives (harmful) |
| | Things linters/formatters can handle |

Research: [RESEARCH.md](./RESEARCH.md) | [한국어](./RESEARCH.ko.md)

## Structure

```
claude_preset/
├── CLAUDE.md              # Core config auto-loaded every session (~350 tokens)
├── rules/                 # Behavioral rules, contextually auto-loaded (0-token when idle)
│   ├── safety.md          #   Bug fix limits, completion verification, security rules
│   ├── quality.md         #   Code quality principles (SOLID, DRY, etc.), scope management
│   ├── orchestration.md   #   Agent role separation, templates, model selection criteria
│   └── workflow.md        #   Review process, PDCA cycle, Git workflow
├── skills/                # Auto-triggered skills on keyword detection (0-token when idle)
│   ├── confidence-check/  #   Pre-implementation confidence assessment (implement/create/build)
│   ├── verify/            #   Post-completion verification gate (done/complete/PR)
│   ├── build-fix/         #   Systematic build error resolution
│   ├── checkpoint/        #   Safety checkpoint before risky operations
│   ├── debug/             #   Systematic debugging (4-phase process)
│   ├── code-review/       #   Severity-based code review
│   ├── learn/             #   Capture problem-solving insights
│   ├── feature-planner/   #   Feature implementation planning (>3 files)
│   ├── gap-analysis/      #   Design vs implementation comparison
│   └── audit/             #   Project rule validation
├── commands/              # Slash commands for specific expert tasks (20)
│   ├── debug.md           #   Analysis: debugging, code review, code smell
│   ├── architecture.md    #   Design: architecture, API, DB
│   ├── testing.md         #   Quality: testing, refactoring, clean code
│   ├── security-audit.md  #   Security: security audit, auth
│   ├── nextjs.md          #   Framework: Next.js, FastAPI, React
│   └── ...                #   Infra: Docker, CI/CD, monitoring, etc.
├── agents/                # Specialized agents spawned via Task tool (8)
│   ├── backend-architect.md    # API/DB/server design specialist
│   ├── frontend-architect.md   # UI/UX/component design specialist
│   ├── system-architect.md     # System architecture specialist
│   ├── security-engineer.md    # Security review specialist
│   ├── quality-engineer.md     # Testing/QA specialist
│   ├── python-expert.md        # Python development specialist
│   ├── performance-engineer.md # Performance optimization specialist
│   └── technical-writer.md     # Technical documentation specialist
├── scripts/               # Automation scripts run by hooks
├── templates/             # Config templates (settings.json, etc.)
├── install.sh             # Install (backup + optional @import file cleanup)
└── uninstall.sh           # Uninstall (backup + previous config restore)
```

## Usage Examples

### Skills (auto-trigger — no manual invocation needed)

```
> Build a login feature

# Claude detects "build" keyword → /confidence-check auto-runs
Confidence: 85%
✅ No duplicate exists
✅ Architecture compliant (Next.js App Router)
⚠️ Official docs — NextAuth v5 breaking changes unverified
✅ Working reference found
Recommendation: Review NextAuth v5 migration guide before proceeding
```

```
> All done, create a PR

# Claude detects "done" + "PR" → /verify auto-runs
Verification: PASS
Command: pnpm test && pnpm build
Evidence: Tests 23 passed, 0 failed. Build exit 0.
```

### Slash Commands (manual invocation)

```
> /code-review src/auth/

## Review: src/auth/

**Critical** (1)
- src/auth/session.ts:42 — JWT secret hardcoded → use env var

**Important** (2)
- src/auth/login.ts:18 — missing rate limiting → add express-rate-limit
- src/auth/middleware.ts:7 — no token expiry check → verify exp claim

**Good**: Clean separation of auth logic from routes
**Verdict**: Request Changes
```

```
> /architecture Design a notification system

## Architecture: Notification System

**Requirements**: Real-time notifications, email/push/in-app, per-user settings

**Options**:
1. Polling — Simple, low real-time capability / server load
2. WebSocket — Real-time, bidirectional / complex connection management
3. SSE + Queue — Real-time, unidirectional / additional infra required

**Recommendation**: SSE + Redis Queue
```

```
> /debug 3 tests are failing, find the cause

Bug: UserService.getProfile() returns null for OAuth users
Root cause: OAuth users have no `password` field → findOne query
  implicitly filters by password existence
Fix: Changed query to findOne({ id }) without password condition
Verification: 3 tests now passing
```

### Agents (auto-spawned for complex tasks)

```
> Review the payment system security

# Claude detects security + review → spawns security-engineer agent

## Security Review: Payment System

**Critical** (2)
- src/payment/charge.ts:34 — SQL injection via orderId
- src/payment/webhook.ts:12 — Stripe signature not verified

**High** (1)
- src/payment/refund.ts:8 — No negative amount validation

**Recommendations**: Add Stripe webhook signature verification,
  apply parameterized queries, add amount range validation
```


## License

MIT
