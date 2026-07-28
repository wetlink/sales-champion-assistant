#!/usr/bin/env python3
"""Validate the self-contained sales-champion-assistant skill package in place."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKILL_DIR_NAME = "sales-champion-assistant"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9_./-]+")

# 私有校準樣本中的真實企業名清單（不入庫）：一行一個名稱片段，
# 任何一個出現在倉庫文本文件中即視為洩漏。
BLOCKLIST_FILE = ".sample-blocklist.txt"

TEXT_SUFFIXES = {".md", ".json", ".txt", ".yaml", ".yml"}


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
    return parser.parse_args()


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
        "阶段一：Researcher",
        "阶段二：Writer",
        "{{company_name}}",
        "{{resource_catalog_json}}",
        "enterprise_info",
        "严重性检查",
        "招聘信息",
        "薪资水平",
        # 行業雙維主導評級體系
        "判定表",
        "高潜领军者",
        "中坚力量",
        "rating_logic",
        # 五維論據深度要求
        "十五五",
        "先进因子",
        "数字化实践",
        "⚠️第三方估算",
        "矛盾核查",
        # 融合報告骨架與檢索規範
        "PART 1",
        "PART 2",
        "检索可靠性",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        raise ValidationError(
            "Prompt file is missing required markers: " + ", ".join(missing)
        )


def validate_schema(package_dir: Path) -> None:
    schema_path = package_dir / "references/schema/company_intel_report.schema.json"
    load_json(schema_path)
    text = schema_path.read_text(encoding="utf-8")
    required_fields = [
        "rating_logic",
        "advanced_factors",
        "policy_anchor",
        "growth_vs_gdp",
        "background_check",
        "digital_practice",
        "contradiction_checks",
        "source_platform",
    ]
    missing = [field for field in required_fields if f'"{field}"' not in text]
    if missing:
        raise ValidationError(
            "Schema is missing required fields: " + ", ".join(missing)
        )

    # 提示詞內嵌 JSON 模板與 schema 是雙份定義，關鍵字段必須兩處同在。
    prompt_text = (
        package_dir / "references/prompts/company_intel_prompts_zh.md"
    ).read_text(encoding="utf-8")
    drift = [field for field in required_fields if f'"{field}"' not in prompt_text]
    if drift:
        raise ValidationError(
            "Prompt embedded JSON template lacks schema fields: " + ", ".join(drift)
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


def validate_no_real_samples(source_root: Path) -> None:
    blocklist_path = source_root / BLOCKLIST_FILE
    if not blocklist_path.is_file():
        print(f"[skip] no {BLOCKLIST_FILE}; sample-leak check not run")
        return
    blocklist = [
        line.strip()
        for line in blocklist_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    hits: list[str] = []
    for path in sorted(source_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts or ".skill-package-staging" in path.parts:
            continue
        if path == blocklist_path:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in blocklist:
            if name in text:
                hits.append(f"{path.relative_to(source_root)}: {name}")
    if hits:
        raise ValidationError(
            "Real sample company data must not enter the repo: " + "; ".join(hits)
        )


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    package_dir = source_root / "skill" / SKILL_DIR_NAME

    try:
        if not package_dir.is_dir():
            raise ValidationError(f"Skill package dir not found: {package_dir}")
        validate_frontmatter(package_dir)
        validate_references(package_dir)
        validate_prompt(package_dir)
        validate_schema(package_dir)
        validate_resource_catalog(package_dir)
        validate_no_real_samples(source_root)

        print("[ok] sales-champion-assistant skill package validated")
        return 0
    except ValidationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
