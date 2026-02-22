#!/usr/bin/env python3
"""
Create a scoped context document scaffold for Codex projects.

Examples:
  python scripts/create_specialized_context.py --domain codex-config
  python scripts/create_specialized_context.py --domain backend --output BACKEND-INSTRUCTIONS.md --marker pyproject.toml
  python scripts/create_specialized_context.py --domain frontend --route ui-build="Build UI workflows" --force
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _title_case(domain: str) -> str:
    return domain.replace("-", " ").strip().title()


def _default_output(domain: str) -> str:
    return f"{domain.upper()}-INSTRUCTIONS.md"


def _parse_route(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ValueError(
            f"Invalid --route value '{raw}'. Expected format: skill-name=purpose."
        )
    skill, purpose = raw.split("=", 1)
    skill = skill.strip()
    purpose = purpose.strip()
    if not skill or not purpose:
        raise ValueError(
            f"Invalid --route value '{raw}'. Both skill and purpose are required."
        )
    return skill, purpose


def _render_markers(markers: list[str]) -> str:
    if not markers:
        markers = ["AGENTS.md", "skills/", "config.toml", "config.template.toml"]
    lines = []
    for marker in markers:
        lines.append(f"- `{marker}`")
    return "\n".join(lines)


def _render_routes(routes: list[tuple[str, str]]) -> str:
    lines = ["| Task | Preferred Skill |", "|---|---|"]
    if not routes:
        lines.append(
            "| [Describe domain task here] | `[choose-skill]` |"
        )
    else:
        for skill, purpose in routes:
            lines.append(f"| {purpose} | `{skill}` |")
    return "\n".join(lines)


def build_content(
    domain: str,
    title: str | None,
    markers: list[str],
    routes: list[tuple[str, str]],
) -> str:
    heading = title.strip() if title else _title_case(domain)
    marker_block = _render_markers(markers)
    route_block = _render_routes(routes)

    return f"""# {heading} - Specialized Context

## Scope

Apply this context only when the target repository matches these markers:
{marker_block}

Outside this scope, do not apply these routing rules unless explicitly requested by the user.

## Delegation-First Execution

- If a suitable skill-specific agent exists, dispatch it first.
- Keep parent context minimal: pass only required files, constraints, and expected output.
- Fall back to direct execution only when delegation is blocked or no suitable skill exists.

## Parallelization Playbook

1. Decompose work into independent subtasks.
2. Run read-heavy subtasks in parallel by default.
3. Partition write-heavy subtasks by non-overlapping file ownership.
4. Complete one integration and validation pass before final output.

## Skill Routing

{route_block}

## Validation

1. Validate changed skills with `quick_validate.py`.
2. Audit changed skill roots with `codex-skill-optimizer`.
3. Re-run checks after fixes and ensure no remaining errors.
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a specialized Codex context scaffold."
    )
    parser.add_argument("--domain", required=True, help="Domain slug, for example codex-config.")
    parser.add_argument("--output", help="Output path. Default: <DOMAIN>-INSTRUCTIONS.md")
    parser.add_argument("--title", help="Optional title override for the context heading.")
    parser.add_argument(
        "--marker",
        action="append",
        default=[],
        help="Scope marker path/pattern. Repeatable.",
    )
    parser.add_argument(
        "--route",
        action="append",
        default=[],
        help="Routing entry in skill=purpose format. Repeatable.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    args = parser.parse_args()

    domain = args.domain.strip().lower()
    if not domain:
        raise SystemExit("Domain cannot be empty.")

    output = Path(args.output or _default_output(domain))
    if output.exists() and not args.force:
        raise SystemExit(
            f"Refusing to overwrite existing file: {output}. Use --force to overwrite."
        )

    routes: list[tuple[str, str]] = []
    for raw in args.route:
        routes.append(_parse_route(raw))

    content = build_content(
        domain=domain,
        title=args.title,
        markers=args.marker,
        routes=routes,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"[OK] Wrote context scaffold to: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
