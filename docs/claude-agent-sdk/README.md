# Claude Agent SDK Documentation

Fetched from: https://code.claude.com/docs/llms.txt
Fetched at: 2026-07-26T06:00:55.619561Z
Page count: 30

## Pages

- [How the agent loop works](agent-loop.md) - Understand the message lifecycle, tool execution, context window, and architecture that power your SDK agents.
- [Use Claude Code features in the SDK](claude-code-features.md) - Load project instructions, skills, hooks, and other Claude Code features into your SDK agents.
- [Track cost and usage](cost-tracking.md) - Learn how to track token usage, estimate costs, and configure prompt caching with the Claude Agent SDK.
- [Give Claude custom tools](custom-tools.md) - Define custom tools with the Claude Agent SDK's in-process MCP server so Claude can call your functions, hit your APIs, and perform domain-specific operations.
- [Rewind file changes with checkpointing](file-checkpointing.md) - Track file changes during agent sessions and restore files to any previous state
- [Intercept and control agent behavior with hooks](hooks.md) - Intercept and customize agent behavior at key execution points with hooks
- [Hosting the Agent SDK](hosting.md) - Deploy the Agent SDK in production: subprocess architecture, session persistence, scaling, observability, and multi-tenant isolation for Docker, Kubernetes, and sandbox providers.
- [Connect to external tools with MCP](mcp.md) - Configure MCP servers to extend your agent with external tools. Covers transport types, tool search for large tool sets, authentication, and error handling.
- [Migrate to Claude Agent SDK](migration-guide.md) - Guide for migrating the Claude Code TypeScript and Python SDKs to the Claude Agent SDK
- [Modifying system prompts](modifying-system-prompts.md) - Choose between the `claude_code` preset and a custom system prompt, and customize behavior with CLAUDE.md, output styles, append, or a fully custom prompt.
- [Observability with OpenTelemetry](observability.md) - Export traces, metrics, and events from the Agent SDK to your observability backend using OpenTelemetry.
- [Agent SDK overview](overview.md) - Build production AI agents with Claude Code as a library
- [Configure permissions](permissions.md) - Control how your agent uses tools with permission modes, hooks, and declarative allow/deny rules.
- [Plugins in the SDK](plugins.md) - Load custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers through the Agent SDK
- [Agent SDK reference - Python](python.md) - Complete API reference for the Python Agent SDK, including all functions, types, and classes.
- [Quickstart](quickstart.md) - Get started with the Python or TypeScript Agent SDK to build AI agents that work autonomously
- [Securely deploying AI agents](secure-deployment.md) - A guide to securing Claude Code and Agent SDK deployments with isolation, credential management, and network controls
- [Persist sessions to external storage](session-storage.md) - Mirror session transcripts to S3, Redis, or your own backend so any host can resume them.
- [Work with sessions](sessions.md) - How sessions persist agent conversation history, and when to use continue, resume, and fork to return to a prior run.
- [Agent Skills in the SDK](skills.md) - Extend Claude with specialized capabilities using Agent Skills in the Claude Agent SDK
- [Slash Commands in the SDK](slash-commands.md) - Learn how to use slash commands to control Claude Code sessions through the SDK
- [Stream responses in real-time](streaming-output.md) - Get real-time responses from the Agent SDK as text and tool calls stream in
- [Streaming Input](streaming-vs-single-mode.md) - Understanding the two input modes for Claude Agent SDK and when to use each
- [Get structured output from agents](structured-outputs.md) - Return validated JSON from agent workflows using JSON Schema, Zod, or Pydantic. Get type-safe, structured data after multi-turn tool use.
- [Subagents in the SDK](subagents.md) - Define and invoke subagents to isolate context, run tasks in parallel, and apply specialized instructions in your Claude Agent SDK applications.
- [Todo Lists](todo-tracking.md) - Track and display todos using the Claude Agent SDK for organized task management
- [Scale to many tools with tool search](tool-search.md) - Scale your agent to thousands of tools by discovering and loading only what's needed, on demand.
- [Agent SDK reference - TypeScript](typescript.md) - Complete API reference for the TypeScript Agent SDK, including all functions, types, and interfaces.
- [TypeScript SDK V2 session API (removed)](typescript-v2-preview.md) - Reference for the removed V2 TypeScript Agent SDK session API, with session-based send/stream patterns for multi-turn conversations.
- [Handle approvals and user input](user-input.md) - Surface Claude's approval requests and clarifying questions to users, then return their decisions to the SDK.
