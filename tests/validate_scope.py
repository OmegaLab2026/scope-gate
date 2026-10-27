#!/usr/bin/env python3
"""Validate the public structure and frozen scope contract of this repository."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADINGS = ["Goal", "Inputs / Outputs", "Must do", "Won't do", "Acceptance"]
REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "docs/demo.gif",
    "docs/build_demo.py",
    "examples/SCOPE.md",
    "skills/scope-gate/SKILL.md",
    "skills/scope-gate/agents/openai.yaml",
    "tests/routing-cases.json",
]


class ValidationError(ValueError):
    """Raised when a repository invariant is not satisfied."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path}") from exc


def validate_frontmatter(skill_text: str) -> None:
    lines = skill_text.splitlines()
    if not lines or lines[0] != "---":
        raise ValidationError("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError("SKILL.md frontmatter is not closed") from exc

    frontmatter = "\n".join(lines[1:end])
    if not re.search(r"^name:\s*scope-gate\s*$", frontmatter, re.MULTILINE):
        raise ValidationError("SKILL.md frontmatter must name scope-gate")
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 40:
        raise ValidationError("SKILL.md needs a meaningful description")


def scope_headings(scope_text: str) -> list[str]:
    return re.findall(r"^##\s+(.+?)\s*$", scope_text, re.MULTILINE)


def validate_scope_text(scope_text: str) -> None:
    if scope_headings(scope_text) != HEADINGS:
        raise ValidationError(
            "scope headings must be exactly and only: " + ", ".join(HEADINGS)
        )

    required_metadata = [
        r"^- Version:\s*V\d+\.\d+\s*$",
        r"^- First created:\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*$",
        r"^- Updated:\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*$",
    ]
    for pattern in required_metadata:
        if not re.search(pattern, scope_text, re.MULTILINE):
            raise ValidationError(f"scope metadata does not match: {pattern}")

    if re.search(r"\bTODO\b|\[TODO", scope_text, re.IGNORECASE):
        raise ValidationError("scope example contains an unfinished placeholder")


def validate_openai_yaml(path: Path) -> None:
    text = read_text(path)
    expected = [
        'display_name: "Scope Gate"',
        'short_description: "Five-field delivery scope before implementation"',
        'default_prompt: "Use $scope-gate to scope this request before implementation."',
    ]
    for line in expected:
        if line not in text:
            raise ValidationError(f"agents/openai.yaml missing: {line}")


def validate_routing_cases(path: Path) -> None:
    try:
        cases = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ValidationError("routing-cases.json is not valid JSON") from exc

    for group in ("should_invoke", "should_not_invoke"):
        entries = cases.get(group)
        if not isinstance(entries, list) or len(entries) < 3:
            raise ValidationError(f"{group} must contain at least three cases")
        for entry in entries:
            if not isinstance(entry, dict) or not entry.get("prompt") or not entry.get("reason"):
                raise ValidationError(f"{group} entries need prompt and reason")


def validate_demo(path: Path) -> None:
    try:
        header = path.read_bytes()[:6]
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path}") from exc
    if header not in (b"GIF87a", b"GIF89a"):
        raise ValidationError("docs/demo.gif is not a GIF")
    if path.stat().st_size < 10_000:
        raise ValidationError("docs/demo.gif is suspiciously small")


def validate_repository(repo_root: Path) -> None:
    for relative_path in REQUIRED_FILES:
        if not (repo_root / relative_path).is_file():
            raise ValidationError(f"missing required file: {relative_path}")

    skill_text = read_text(repo_root / "skills/scope-gate/SKILL.md")
    validate_frontmatter(skill_text)
    for phrase in (
        "Brief analysis",
        "**Options**",
        "**Recommendation:**",
        "ADRs, technical designs, ticket breakdowns, estimates",
        "`SCOPE.md`",
        "`V1.1`",
        "`V2.0`",
    ):
        if phrase not in skill_text:
            raise ValidationError(f"SKILL.md is missing contract phrase: {phrase}")

    validate_scope_text(read_text(repo_root / "examples/SCOPE.md"))
    validate_openai_yaml(repo_root / "skills/scope-gate/agents/openai.yaml")
    validate_routing_cases(repo_root / "tests/routing-cases.json")
    validate_demo(repo_root / "docs/demo.gif")

    for readme_name in ("README.md", "README.zh-CN.md"):
        readme = read_text(repo_root / readme_name)
        for target in (
            "docs/demo.gif",
            "examples/SCOPE.md",
            "LICENSE",
            "skills/scope-gate/SKILL.md",
        ):
            if target not in readme:
                raise ValidationError(f"{readme_name} does not link {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    root = args.repo_root.resolve()
    try:
        validate_repository(root)
    except ValidationError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: scope-gate structure is valid at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
