---
name: codex-skill-optimizer
description: "Audit and optimize Codex skill folders (`*/SKILL.md`) for trigger quality, context efficiency, and modern AGENTS/Codex conventions. Use when creating new skills, migrating legacy skills, reviewing many skills, or before committing skill updates."
---

# Codex Skill Optimizer

## Overview

Use this skill to run deterministic checks across Codex skills and apply safe automatic fixes, then provide a prioritized manual optimization plan for anything that should not be auto-edited.

## Workflow

1. Inventory target skills under the requested root path.
2. Run `scripts/audit_codex_skills.py` to generate an audit report.
3. Classify findings:
- `error`: must fix before merge.
- `warning`: should fix for quality and maintainability.
- `info`: optional improvements.
4. If requested, run safe autofixes with `--apply`.
5. Re-run audit to confirm improvements and detect remaining manual work.
6. For each remaining issue, propose exact file-level edits and rationale.

## Commands

Run audit only:

```bash
python scripts/audit_codex_skills.py --root skills
```

Audit and apply safe fixes:

```bash
python scripts/audit_codex_skills.py --root skills --apply
```

Audit including hidden/system skills:

```bash
python scripts/audit_codex_skills.py --root skills --include-system
```

Emit JSON for tooling/CI:

```bash
python scripts/audit_codex_skills.py --root skills --format json
```

Fail CI on warnings:

```bash
python scripts/audit_codex_skills.py --root skills --fail-on warning
```

## Auto-Fix Policy

`--apply` only performs conservative transforms:
- Replace legacy project-doc filenames with `AGENTS.md`.
- Normalize legacy absolute rule/memory paths to `$CODEX_HOME/...`.
- Normalize trailing whitespace and file ending newline.

Do not auto-refactor structure, reorder sections, or rewrite large text blocks without explicit user request.

## Manual Optimization Checklist

Use `references/skill-quality-checklist.md` for manual improvements that require judgment:
- trigger description quality,
- progressive disclosure and token budget,
- deterministic workflow clarity,
- project-specific hardcoding removal,
- anti-pattern cleanup.

## Output Requirements

When reporting results:
1. List findings by severity and file path.
2. Show what was auto-fixed vs what remains manual.
3. Provide a minimal patch plan for remaining issues.
4. Include exact commands used.
