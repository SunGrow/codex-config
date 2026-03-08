# Research Instructions

## Scope

Apply this context to technical research, API verification, recommendations, and mixed-domain fact-finding that requires stable sourcing.

Use `researcher` for focused research. Use `research-director` when the request needs decomposition, parallel child research, or synthesis across multiple subtopics. For Unreal-specific research, prefer `ue-researcher` or `ue-research-director`.

## Source Priorities

1. Primary source code, specifications, and official schemas
2. Official documentation, API references, and release notes
3. Maintainer-authored examples and official sample repositories
4. High-quality community references that can be cross-checked
5. Articles, tutorials, and forum posts used only as secondary evidence

Higher-priority sources override lower-priority sources on conflicts.

## Research Process

1. Check the local project first so recommendations fit the existing codebase.
2. Define the exact question and split broad requests into focused sub-questions.
3. Verify unstable claims against primary sources whenever possible.
4. Record version, release, or date context whenever it matters.
5. Mark uncertainty explicitly instead of guessing.

## Mixed-Domain Routing

- Use `ue-researcher` for Unreal Engine APIs, plugins, Blueprint behavior, or UE architecture.
- Use `researcher` for general libraries, languages, frameworks, tooling, or platform APIs.
- Use `research-director` or `ue-research-director` when a request mixes both and needs synthesis.

## Output Format

Every substantial research result should use this structure:

```md
## Research Brief: <topic>

### Summary
### Verified APIs and Patterns
### Recommended Approach
### Risks and Open Questions
### Sources
```

Use clear confidence markers such as `Verified`, `Likely`, and `Uncertain` when needed.

## Recommendations And Risk

- Prefer built-in or officially supported solutions over custom patterns.
- Call out dependencies, module/package requirements, thread or runtime constraints, and migration/version risk.
- Do not present recommendations that would cost the user significant time or money without current verification.

## Durable Learnings

- Child researchers must not write shared memory during execution.
- Reusable discoveries should be returned in a `Reusable Learnings` section.
- Persist only stable, versioned knowledge into `docs/` or `memories/`.
