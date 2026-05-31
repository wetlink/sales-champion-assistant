#!/usr/bin/env python3
"""Validate the packaged sales-champion-assistant skill."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path


SKILL_DIR_NAME = "sales-champion-assistant"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9_./-]+")


class ValidationError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Validate the sales-champion-assistant skill package."
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=default_root,
        help="sales-champion-assistant source root.",
    )
    parser.add_argument(
        "--keep-staging",
        action="store_true",
        help="Keep the temporary staged skill package for inspection.",
    )
    return parser.parse_args()


def require_file(path: Path) -> None:
    if not path.is_file():
        raise ValidationError(f"Required file not found: {path}")


def copy_package(source_root: Path, staging_root: Path) -> Path:
    sources = {
        "SKILL.md": source_root / "skill" / SKILL_DIR_NAME / "SKILL.md",
        "references/prompts/company_intel_prompts_zh.md": source_root
        / "prompts"
        / "company_intel_prompts_zh.md",
        "references/config/resource_catalog.example.json": source_root
        / "config"
        / "resource_catalog.example.json",
    }
    for src in sources.values():
        require_file(src)

    package_dir = staging_root / SKILL_DIR_NAME
    for rel_path, src in sources.items():
        dst = package_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return package_dir


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, str], str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValidationError("SKILL.md must start with YAML frontmatter.")

    try:
        _, frontmatter_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValidationError("SKILL.md frontmatter is not closed.") from exc

    data: dict[str, str] = {}
    for line in frontmatter_text.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValidationError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")

    unexpected = sorted(set(data) - {"name", "description"})
    if unexpected:
        raise ValidationError(
            "Only name and description are allowed in frontmatter; "
            f"found: {', '.join(unexpected)}"
        )
    if set(data) != {"name", "description"}:
        raise ValidationError("Frontmatter must contain name and description.")
    return data, body


def validate_frontmatter(package_dir: Path) -> None:
    data, _ = parse_frontmatter(package_dir / "SKILL.md")
    name = data["name"]
    if not NAME_RE.fullmatch(name):
        raise ValidationError(
            f"Skill name '{name}' must be hyphen-case lowercase letters/digits."
        )
    if name != package_dir.name:
        raise ValidationError(
            f"Skill name '{name}' must match folder name '{package_dir.name}'."
        )
    if len(data["description"]) < 20:
        raise ValidationError("Skill description is too short to trigger reliably.")


def validate_references(package_dir: Path) -> None:
    _, body = parse_frontmatter(package_dir / "SKILL.md")
    refs = sorted(set(REFERENCE_RE.findall(body)))
    if not refs:
        raise ValidationError("SKILL.md should reference bundled resources.")
    missing = [ref for ref in refs if not (package_dir / ref).is_file()]
    if missing:
        raise ValidationError(
            "Missing bundled references: " + ", ".join(missing)
        )


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as f:
            value = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"Expected top-level object in {path}")
    return value


def validate_prompt(package_dir: Path) -> None:
    prompt_path = package_dir / "references/prompts/company_intel_prompts_zh.md"
    text = prompt_path.read_text(encoding="utf-8")
    required_markers = [
        "新增企业信息评估模块",
        "阶段一：Researcher",
        "阶段二：Writer",
        "{{company_name}}",
        "{{resource_catalog_json}}",
        "enterprise_info",
        "严重性检查",
        "招聘信息",
        "薪资水平",
        "evidence 至少",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        raise ValidationError(
            "Prompt file is missing required markers: " + ", ".join(missing)
        )


def validate_resource_catalog(package_dir: Path) -> None:
    catalog = load_json(package_dir / "references/config/resource_catalog.example.json")
    required_keys = {
        "government_gr",
        "lighthouse_clients",
        "capital_network",
        "alumni_association",
        "recruiting_entry",
        "compliance",
    }
    missing = sorted(required_keys - set(catalog))
    if missing:
        raise ValidationError(
            "Resource catalog missing required keys: " + ", ".join(missing)
        )


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()

    try:
        with tempfile.TemporaryDirectory(prefix="company-intel-skill.") as tmp:
            package_dir = copy_package(source_root, Path(tmp))
            validate_frontmatter(package_dir)
            validate_references(package_dir)
            validate_prompt(package_dir)
            validate_resource_catalog(package_dir)

            if args.keep_staging:
                kept_parent = source_root / ".skill-package-staging"
                kept_dir = kept_parent / package_dir.name
                if kept_parent.exists():
                    shutil.rmtree(kept_parent)
                kept_parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(package_dir, kept_dir)
                print(f"[ok] kept staged package: {kept_dir}")

        print("[ok] sales-champion-assistant skill package validated")
        return 0
    except ValidationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
