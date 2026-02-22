# Codex Documentation References

References below were verified on 2026-02-22.

## Official OpenAI Codex docs

- Overview: https://developers.openai.com/codex
- Quickstart: https://developers.openai.com/codex/quickstart
- Customization concepts: https://developers.openai.com/codex/concepts/customization
- Multi-agents concepts: https://developers.openai.com/codex/concepts/multi-agents
- CLI features: https://developers.openai.com/codex/cli/features#running-in-interactive-mode
- Config basics: https://developers.openai.com/codex/config-basic
- Advanced config: https://developers.openai.com/codex/config-advanced
- Config reference: https://developers.openai.com/codex/config-reference
- Sample config: https://developers.openai.com/codex/config-sample
- Rules: https://developers.openai.com/codex/guides/rules
- AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Skills: https://developers.openai.com/codex/skills
- Custom prompts: https://developers.openai.com/codex/custom-prompts
- Cloud tasks: https://developers.openai.com/codex/cloud
- Running on Windows: https://developers.openai.com/codex/windows

## Open source repository (upstream)

- Codex CLI repository: https://github.com/openai/codex
- Repository AGENTS.md: https://raw.githubusercontent.com/openai/codex/main/AGENTS.md
- Configuration schema (source of keys/defaults): https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json
- Config docs bridge in repo (now points to docs site): https://raw.githubusercontent.com/openai/codex/main/docs/config.md
- Orchestrator base prompt template: https://github.com/openai/codex/blob/main/codex-rs/core/templates/agents/orchestrator.md
- Default collaboration mode template: https://github.com/openai/codex/blob/main/codex-rs/core/templates/collaboration_mode/default.md
- Plan collaboration mode template: https://github.com/openai/codex/blob/main/codex-rs/core/templates/collaboration_mode/plan.md

## Decision handoff provenance

- Multi-agent orchestration model: https://developers.openai.com/codex/concepts/multi-agents
- AGENTS.md routing and instruction boundaries: https://developers.openai.com/codex/guides/agents-md
- Skill metadata and implicit invocation policy: https://developers.openai.com/codex/skills
- Practical handoff behavior is synthesized from the official multi-agent/skills docs plus upstream prompt templates; there is no single page titled "decision handoff".

## Local docs included in this repository

- `AGENTS.md`
- `UE-INSTRUCTIONS.md`
- `config.template.toml`
