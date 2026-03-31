# Research: Claude Code Default Behaviors

Date: 2026-02-26 (based on v2.1.58)

## Sources

- [Anthropic Best Practices](https://code.claude.com/docs/en/best-practices)
- [HumanLayer - Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — v2.1.58, 225+ files
- [arxiv 2602.15228 - System Prompts in Code Generation](https://arxiv.org/abs/2602.15228)
- [arxiv 2509.14744 - Agentic Coding Manifests](https://arxiv.org/abs/2509.14744)
- [Arize - CLAUDE.md Optimization](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)

---

## 1. Anthropic Official CLAUDE.md Guidelines

### Include
- Bash commands Claude can't guess
- Code style rules that **differ from defaults**
- Test runner, build commands
- Project-specific architecture decisions
- Environment quirks, non-intuitive behaviors

### Exclude
- Things discoverable by reading the code
- Language conventions Claude already knows
- Detailed API docs (use links instead)
- Frequently changing information
- Self-evident practices like "write clean code"

### Key Quotes
> "If Claude already does something correctly without the instruction, delete it or convert it to a hook."
> "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

---

## 2. Claude Code System Prompt Deep Analysis

Source: [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) v2.1.58

The system prompt is not a single block but a **modular architecture of 225+ conditional files**:
- Agent Prompts: 29
- Data References: 26
- System Prompts: 50+
- System Reminders: 40+
- Tool Descriptions: 50+ (Bash alone has 47 fragments)

### 2.1 Code Quality (5 independent fragments)

| Fragment | Exact Wording (verbatim) |
|---|---|
| **Avoid over-engineering** | "Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused." |
| **No unnecessary additions** | "Don't add features, refactor code, or make 'improvements' beyond what was asked. Don't add docstrings, comments, or type annotations to code you didn't change." |
| **No unnecessary error handling** | "Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries." |
| **No premature abstractions** | "Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. Three similar lines of code is better than a premature abstraction." |
| **No compatibility hacks** | "If you are certain that something is unused, you can delete it completely." |

→ **Conclusion**: KISS, YAGNI, and "scope discipline" are already distributed across 5 fragments. No need to repeat them in detail in CLAUDE.md.

### 2.2 File Operations

| Behavior | Built-in Wording |
|---|---|
| Read before Edit | "Do not propose changes to code you haven't read. Read it first." |
| Minimize file creation | "Do not create files unless they're absolutely necessary. Generally prefer editing an existing file." |
| No README auto-creation | "NEVER proactively create documentation files (*.md) or README files." |
| Software engineering context | "When given an unclear or generic instruction, consider it in the context of software engineering tasks." |

### 2.3 Git Workflow (8+ fragments, most detailed area)

| Behavior | Built-in Wording |
|---|---|
| Commit only when asked | "Only create commits when requested by the user. If unclear, ask first." |
| NEVER update git config | Explicit prohibition |
| No destructive ops | "NEVER run destructive git commands (push --force, reset --hard, checkout .) unless the user explicitly requests" |
| Never skip hooks | "NEVER skip hooks (--no-verify, --no-gpg-sign, etc)" + "If a hook fails, investigate and fix the underlying issue." |
| Prefer new commits | "ALWAYS create NEW commits rather than amending" |
| Specific files staging | "prefer adding specific files by name rather than 'git add -A'" |
| No force push to main | "NEVER run force push to main/master, warn the user" |
| Co-Authored-By | Conditional variable (`COMMIT_CO_AUTHORED_BY_CLAUDE_CODE`), included/excluded based on settings |
| PR creation | Uses gh CLI, HEREDOC format, detailed workflow included |

→ **Conclusion**: Git safety rules are the most detailed area in the system prompt. "Feature branches", "don't skip hooks" etc. are completely unnecessary in CLAUDE.md. Only "No Co-Authored-By" has override value.

### 2.4 Security

| Behavior | Built-in Wording |
|---|---|
| OWASP Top 10 prevention | "Be careful not to introduce security vulnerabilities such as command injection, XSS, SQL injection" |
| Immediate fix | "If you notice that you wrote insecure code, immediately fix it" |
| Secrets prevention | "Do not commit files that likely contain secrets (.env, credentials.json, etc)" |
| Security review | `/security-review` slash command built-in (2610 tokens) |

### 2.5 Communication Style

| Behavior | Built-in Wording |
|---|---|
| Conciseness | "Your responses should be short and concise." |
| No filler | "Avoid using filler words, repetition, or restating what the user has already said." |
| No emoji | "Only use emojis if the user explicitly requests it." |
| Code references | "Include the pattern file_path:line_number" |
| No time estimates | "Avoid giving time estimates or predictions" |
| Hide inner monologue | "Avoid sharing your thinking or inner monologue in your output" |

### 2.6 Tool Usage

| Behavior | Built-in Wording |
|---|---|
| Dedicated tools first | "Do NOT use Bash to run commands when a relevant dedicated tool is provided" (Read > cat, Edit > sed, Grep > grep, Glob > find) |
| Parallel calls | "Make all independent tool calls in parallel" |
| Alternatives when blocked | "Do not attempt to brute force. Consider alternative approaches." |
| Confirm risky actions | "Check with the user before proceeding" for destructive/irreversible actions |

### 2.7 Agents/Memory (built-in)

| Behavior | Description |
|---|---|
| Task tool | Agent spawn guidelines built-in (294 tks) |
| Explore agent | Code exploration specialist subagent (516 tks) |
| Plan mode | Plan mode transition logic (633 tks) |
| Agent memory | Domain-specific memory update guide (337 tks) |
| Session memory | Session memory template + update instructions (756 tks) |
| Learning mode | Educational interaction mode (1042 tks) |

→ **Conclusion**: Basic agent behaviors are built-in. Orchestrator/Worker **separation rules** are NOT, so they have override value.

---

## 3. What Requires Override (not covered by defaults)

| Behavior | Default | Required Override | Rationale |
|---|---|---|---|
| Korean response | English | `ALWAYS respond in Korean` | Not in system prompt |
| Use uv | Tends toward pip/poetry | `prefer uv` | Not in system prompt |
| Use pnpm | Tends toward npm | `prefer pnpm` | Not in system prompt |
| Auto-format with ruff | Manual | PostToolUse hook | Enforced via hook |
| Stop after 3 failures | Suggests alternatives but no threshold | 3+ Fix Rule | Specific "3 attempts" threshold needed |
| Verify before completion | Tends to claim "should work" | Verification Gate | IDENTIFY→RUN→READ→VERIFY process |
| Remove Co-Authored-By | Conditionally included (default ON) | `No Co-Authored-By` | Variable override |
| Agent role separation | No distinction | Orchestrator/Worker pattern | Not in system prompt |
| Two-stage review | None | Two-Stage Review | Not in system prompt |
| Auto-trigger skills | None | Auto-trigger rules | Custom workflow |
| Persistence | Can abandon with TODOs | Start = Finish | Not in system prompt |

---

## 4. Gray Area: Knows but Inconsistently Applies

| Item | System Prompt Coverage | Recommendation |
|---|---|---|
| SOLID | None (no explicit SRP, OCP, etc.) | Keep as 1-line reminder |
| DRY | Indirectly: "three similar lines > abstraction" | Reinforce with specific threshold in rules/ |
| KISS | Strongly covered by 5 fragments | 1-line reminder sufficient |
| Scope discipline | Covered: "only make directly requested changes" | Reinforce in rules/ |
| No leftover TODOs | None | "Start = Finish" override needed |
| Root cause analysis | "consider alternatives" level only | Detail in rules/ |

---

## 5. Key Paper Findings

### arxiv 2602.15228
- "Increasing instruction specificity does not monotonically increase accuracy"
- "Few-shot examples can degrade performance in large models"
- Java is more sensitive to system prompt variations than Python

### HumanLayer Analysis
- **"As instruction count increases, compliance rate for ALL instructions decreases uniformly"**
- System prompt already contains ~50 instructions
- CLAUDE.md recommended to stay under 150-200 total instructions
- HumanLayer's own CLAUDE.md is under 60 lines
- "Never send an LLM to do a linter's job" — use formatters/linters for code style

### Arize Research
- CLAUDE.md optimization improved SWE Bench by +10.87% (single repo)
- Key insight: repo-specific instructions are more effective than generic ones

---

## 6. Community Reports (GitHub Issues)

- [#668](https://github.com/anthropics/claude-code/issues/668) — Bug where Claude ignores CLAUDE.md instructions
- [#7777](https://github.com/anthropics/claude-code/issues/7777) — Claude ignores agent/CLAUDE.md instructions
- Common cause: CLAUDE.md is too long, causing instructions to get "buried"

---

## 7. Conclusion: CLAUDE.md Writing Principles

### Include Criteria (include if any match)
1. **Does it change default behavior?** (e.g., Korean, uv, No Co-Authored-By)
2. **Is it a specific threshold/criterion?** (e.g., "stop after 3 failures")
3. **Is it a unique workflow?** (e.g., Two-Stage Review, Orchestrator/Worker)

### Exclude Criteria (exclude if any match)
1. **Already in system prompt?** — Check against 225+ fragments
2. **Default language/framework convention?** (e.g., snake_case, camelCase)
3. **Explanation or directive?** (explanation = harmful, directive = helpful)
4. **Can a linter/formatter/hook handle it?** (e.g., ruff → hook)

### Ideal Size
- CLAUDE.md: **under 60 lines** (HumanLayer benchmark)
- Total instructions: **under 100** (system ~50 + CLAUDE.md ~50)
- Detailed rules: separate into `rules/` directory (loaded only when needed)

### Common Mistakes: Duplicating System Prompts
| Often written in CLAUDE.md | Already built-in because |
|---|---|
| "Read before edit" | Edit tool fails without Read + dedicated fragment |
| "Don't over-engineer" | 5 independent fragments already cover this |
| "Use feature branches" | Included in Git safety protocol |
| "Don't skip hooks" | "NEVER skip hooks" explicit prohibition |
| "Prefer dedicated tools" | 13 tool usage policy fragments |
| "Be concise" | 2 tone and style fragments |
| "Don't create unnecessary files" | Minimize file creation fragment |
| "Security best practices" | OWASP Top 10 prevention fragment |
| "No emoji" | Explicit prohibition |
| "Git safety" | 8+ fragments, most detailed area |
