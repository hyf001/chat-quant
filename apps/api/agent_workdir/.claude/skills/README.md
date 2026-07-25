# Chat-Quant Agent Skills

Place Claude Agent SDK project skills in this directory.

Expected layout:

```text
apps/api/agent_workdir/.claude/skills/
  stock_query/
    SKILL.md
  charting/
    SKILL.md
  strategy_authoring/
    SKILL.md
  backtest/
    SKILL.md
  risk_disclaimer/
    SKILL.md
```

M2 copies this directory into each isolated SDK session working directory at
`<AGENT_WORKDIR_ROOT>/<chat_session_id>/.claude/skills` before calling
`claude_agent_sdk.query()`. The SDK then discovers and loads skills using its
native project-scope logic from `cwd/.claude/skills`.
