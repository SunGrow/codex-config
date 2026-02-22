#!/usr/bin/env python3
"""
Audit and optionally apply safe fixes to Codex skill folders.

Usage examples:
  python scripts/audit_codex_skills.py --root skills
  python scripts/audit_codex_skills.py --root skills --apply
  python scripts/audit_codex_skills.py --root skills --format json --fail-on warning
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class Finding:
    severity: str
    check: str
    path: str
    message: str
    line: int | None = None


@dataclass
class SkillResult:
    skill: str
    skill_file: str
    findings: list[Finding]
    applied_fixes: list[str]


LEGACY_PATH_REPLACEMENTS: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"C:\\Users\\[^\\]+\\.codex\\agent-rules\\"),
        "$CODEX_HOME/agent-rules/",
        "normalize-agent-rules-path",
    ),
    (
        re.compile(r"C:\\Users\\[^\\]+\\.codex\\agent-memory\\"),
        "$CODEX_HOME/agent-memory/",
        "normalize-agent-memory-path",
    ),
    (
        re.compile(r"/Users/[^/]+/.codex/agent-rules/"),
        "$CODEX_HOME/agent-rules/",
        "normalize-agent-rules-path",
    ),
    (
        re.compile(r"/Users/[^/]+/.codex/agent-memory/"),
        "$CODEX_HOME/agent-memory/",
        "normalize-agent-memory-path",
    ),
]


def discover_skill_dirs(root: Path, include_system: bool) -> list[Path]:
    skills: list[Path] = []
    for skill_md in root.rglob("SKILL.md"):
        rel_parts = skill_md.relative_to(root).parts
        if not include_system and any(part.startswith(".") for part in rel_parts):
            continue
        skills.append(skill_md.parent)
    return sorted(set(skills))


def parse_frontmatter(content: str) -> tuple[dict[str, str], list[str], str | None]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", content, re.DOTALL)
    if not match:
        return {}, [], None

    raw = match.group(1)
    keys: list[str] = []
    values: dict[str, str] = {}

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        keys.append(key)
        values[key] = val

    body = content[match.end() :]
    return values, keys, body


def _normalize_newlines(content: str) -> tuple[str, str]:
    newline = "\r\n" if "\r\n" in content else "\n"
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    return normalized, newline


def apply_safe_fixes(content: str) -> tuple[str, list[str]]:
    normalized, newline = _normalize_newlines(content)
    fixed = normalized
    changes: list[str] = []

    if "CLAUDE.md" in fixed:
        fixed = fixed.replace("CLAUDE.md", "AGENTS.md")
        changes.append("replace-claude-md")

    for pattern, replacement, tag in LEGACY_PATH_REPLACEMENTS:
        updated = pattern.sub(replacement, fixed)
        if updated != fixed:
            fixed = updated
            changes.append(tag)

    trimmed_lines = [line.rstrip() for line in fixed.split("\n")]
    fixed = "\n".join(trimmed_lines)
    if fixed != normalized:
        changes.append("trim-trailing-whitespace")

    fixed = fixed.strip("\n") + "\n"
    fixed = fixed.replace("\n", newline)
    return fixed, sorted(set(changes))


def _check_numbered_list_gaps(content: str, rel_path: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()
    idx = 0
    while idx < len(lines):
        if not re.match(r"^\s*\d+\.\s+\S", lines[idx]):
            idx += 1
            continue

        start = idx
        block_nums: list[tuple[int, int]] = []
        while idx < len(lines) and re.match(r"^\s*\d+\.\s+\S", lines[idx]):
            num = int(re.match(r"^\s*(\d+)\.", lines[idx]).group(1))
            block_nums.append((num, idx + 1))
            idx += 1

        nums = [n for n, _ in block_nums]
        if all(n == 1 for n in nums):
            continue

        for i in range(1, len(block_nums)):
            prev_num, _ = block_nums[i - 1]
            cur_num, cur_line = block_nums[i]
            if cur_num != prev_num + 1:
                findings.append(
                    Finding(
                        severity="warning",
                        check="numbered-list-gap",
                        path=rel_path,
                        line=cur_line,
                        message=(
                            f"Numbered list gap detected near line {cur_line} "
                            f"(expected {prev_num + 1}, found {cur_num})."
                        ),
                    )
                )
                break

        if idx == start:
            idx += 1
    return findings


def audit_skill(skill_dir: Path, root: Path, apply: bool) -> SkillResult:
    skill_file = skill_dir / "SKILL.md"
    rel_file = str(skill_file.relative_to(root))
    content = skill_file.read_text(encoding="utf-8")
    applied_fixes: list[str] = []

    if apply:
        fixed, changes = apply_safe_fixes(content)
        if changes:
            skill_file.write_text(fixed, encoding="utf-8")
            content = fixed
            applied_fixes = changes

    findings: list[Finding] = []
    fm_values, fm_keys, body = parse_frontmatter(content)

    if body is None:
        findings.append(
            Finding(
                severity="error",
                check="frontmatter-missing",
                path=rel_file,
                message="Missing or invalid YAML frontmatter block.",
            )
        )
        return SkillResult(skill=skill_dir.name, skill_file=rel_file, findings=findings, applied_fixes=applied_fixes)

    required = {"name", "description"}
    missing = sorted(required - set(fm_keys))
    if missing:
        findings.append(
            Finding(
                severity="error",
                check="frontmatter-required-fields",
                path=rel_file,
                message=f"Missing required frontmatter fields: {', '.join(missing)}.",
            )
        )

    extra = sorted(set(fm_keys) - required)
    if extra:
        findings.append(
            Finding(
                severity="warning",
                check="frontmatter-extra-fields",
                path=rel_file,
                message=f"Unexpected frontmatter fields: {', '.join(extra)}.",
            )
        )

    description = fm_values.get("description", "").strip()
    if not description or "TODO" in description.upper():
        findings.append(
            Finding(
                severity="error",
                check="description-todo",
                path=rel_file,
                message="Description is empty or contains TODO placeholder.",
            )
        )
    else:
        if len(description) < 40:
            findings.append(
                Finding(
                    severity="warning",
                    check="description-short",
                    path=rel_file,
                    message=f"Description may be too short for reliable triggering ({len(description)} chars).",
                )
            )
        if len(description) > 260:
            findings.append(
                Finding(
                    severity="warning",
                    check="description-long",
                    path=rel_file,
                    message=f"Description may be too long/noisy for triggering ({len(description)} chars).",
                )
            )

    line_count = len(content.splitlines())
    if line_count > 500:
        findings.append(
            Finding(
                severity="error",
                check="skill-body-too-long",
                path=rel_file,
                message=f"Skill is very large ({line_count} lines). Split into references/scripts.",
            )
        )
    elif line_count > 300:
        findings.append(
            Finding(
                severity="warning",
                check="skill-body-large",
                path=rel_file,
                message=f"Skill is large ({line_count} lines). Consider progressive disclosure.",
            )
        )

    legacy_checks: list[tuple[str, str, str]] = [
        ("warning", "legacy-claude-reference", r"\bCLAUDE\.md\b"),
        ("warning", "legacy-migration-path", r"migrated-from-claude"),
        ("warning", "hardcoded-user-path", r"C:\\Users\\"),
        ("warning", "hardcoded-user-path", r"/Users/"),
        ("warning", "memory-bloat-section", r"Persistent Agent Memory"),
        ("warning", "memory-bloat-section", r"Update your agent memory"),
    ]
    for severity, check, pattern in legacy_checks:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if match:
            line = content[: match.start()].count("\n") + 1
            findings.append(
                Finding(
                    severity=severity,
                    check=check,
                    path=rel_file,
                    line=line,
                    message=f"Found pattern '{pattern}' that may indicate legacy or high-token content.",
                )
            )

    findings.extend(_check_numbered_list_gaps(content, rel_file))

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        findings.append(
            Finding(
                severity="warning",
                check="openai-yaml-missing",
                path=rel_file,
                message="Missing agents/openai.yaml metadata file.",
            )
        )
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        short_desc_match = re.search(r'^\s*short_description:\s*"(.*)"\s*$', yaml_text, flags=re.MULTILINE)
        if short_desc_match:
            short_desc = short_desc_match.group(1)
            if not (25 <= len(short_desc) <= 64):
                findings.append(
                    Finding(
                        severity="warning",
                        check="openai-short-description-length",
                        path=str(openai_yaml.relative_to(root)),
                        message=(
                            "short_description should be 25-64 chars for UI conventions "
                            f"(found {len(short_desc)})."
                        ),
                    )
                )
        else:
            findings.append(
                Finding(
                    severity="warning",
                    check="openai-short-description-missing",
                    path=str(openai_yaml.relative_to(root)),
                    message='agents/openai.yaml missing "short_description".',
                )
            )

    return SkillResult(skill=skill_dir.name, skill_file=rel_file, findings=findings, applied_fixes=applied_fixes)


def summarize(results: Iterable[SkillResult]) -> tuple[int, int, int]:
    errors = 0
    warnings = 0
    infos = 0
    for result in results:
        for finding in result.findings:
            if finding.severity == "error":
                errors += 1
            elif finding.severity == "warning":
                warnings += 1
            else:
                infos += 1
    return errors, warnings, infos


def print_markdown(results: list[SkillResult], root: Path, apply: bool) -> None:
    errors, warnings, infos = summarize(results)
    print(f"# Codex Skill Audit (`{root}`)")
    print()
    print(f"- Skills scanned: {len(results)}")
    print(f"- Errors: {errors}")
    print(f"- Warnings: {warnings}")
    print(f"- Infos: {infos}")
    print()

    if apply:
        fixed = [(r.skill_file, r.applied_fixes) for r in results if r.applied_fixes]
        print(f"- Files auto-fixed: {len(fixed)}")
        if fixed:
            for path, changes in fixed:
                print(f"  - `{path}`: {', '.join(changes)}")
        print()

    for result in results:
        if not result.findings and not result.applied_fixes:
            continue
        print(f"## {result.skill}")
        if result.applied_fixes:
            print(f"- Auto-fixes: {', '.join(result.applied_fixes)}")
        if not result.findings:
            print("- No remaining findings.")
            print()
            continue
        for finding in result.findings:
            loc = f":{finding.line}" if finding.line else ""
            print(
                f"- `{finding.severity.upper()}` `{finding.check}` "
                f"`{finding.path}{loc}`: {finding.message}"
            )
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and optimize Codex skill files.")
    parser.add_argument("--root", default="skills", help="Root folder that contains skill directories.")
    parser.add_argument("--include-system", action="store_true", help="Include hidden/system skill folders.")
    parser.add_argument("--apply", action="store_true", help="Apply safe automatic fixes.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format.")
    parser.add_argument(
        "--fail-on",
        choices=["error", "warning"],
        default="error",
        help="Exit non-zero on this severity or higher.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Root path is not a directory: {root}")
        return 2

    skill_dirs = discover_skill_dirs(root, include_system=args.include_system)
    results = [audit_skill(skill_dir, root=root, apply=args.apply) for skill_dir in skill_dirs]
    errors, warnings, _ = summarize(results)

    if args.format == "json":
        payload = {
            "root": str(root),
            "skills_scanned": len(results),
            "errors": errors,
            "warnings": warnings,
            "results": [
                {
                    "skill": r.skill,
                    "skill_file": r.skill_file,
                    "applied_fixes": r.applied_fixes,
                    "findings": [asdict(f) for f in r.findings],
                }
                for r in results
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print_markdown(results, root, args.apply)

    if args.fail_on == "warning" and (errors > 0 or warnings > 0):
        return 1
    if args.fail_on == "error" and errors > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
