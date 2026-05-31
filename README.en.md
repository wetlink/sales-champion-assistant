# Sales Champion Assistant / sales-champion-assistant

[中文](README.md) | English

`sales-champion-assistant` is an agent workflow package for B2B sales, business development, and account operations. Given a company name, it turns public information into a company profile, customer rating, hiring and salary signals, key-person leads, capital and government ties, supply-chain position, resource-matching paths, and outreach suggestions.

The project was formerly named `company-intel-report`. The public-facing name is now "Sales Champion Assistant: Company Research And Outreach Strategy" to better match daily sales workflows.

This repository provides:

- A Codex/OpenClaw-style Skill.
- A two-stage Chinese prompt workflow: Researcher creates structured intelligence, Writer turns it into a report.
- A JSON Schema for validating structured intelligence.
- A sample resource catalog that maps company leads to actionable outreach paths.
- A lightweight validation script for checking the Skill package structure.

## Use Cases

- Help sales or BD teams prepare before a customer meeting.
- Evaluate company scale, growth, risk, and possible entry points for account operations.
- Support investment promotion, industry services, and ecosystem partnerships with reusable company background research.
- Turn "research a company, write a report, propose outreach moves" into a reusable workflow.

## Output

A full report includes:

- Company information and star rating.
- GTM customer-segment fact check, including employee count, segment, source, and confidence.
- Sensitivity and severity review.
- Five-dimensional scoring: industry growth, industry position, regional position, finance and capital, and management profile.
- Hiring and salary analysis.
- Power map and key-person profiles.
- Capital background and government ties.
- Upstream and downstream supply-chain view.
- Public footprint and strategic concerns.
- Resource-matching outreach strategy.
- Executive communication suggestions.

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── config/
│   └── resource_catalog.example.json
├── prompts/
│   └── company_intel_prompts_zh.md
├── schema/
│   └── company_intel_report.schema.json
├── scripts/
│   └── validate_skill_package.py
└── skill/
    └── sales-champion-assistant/
        ├── SKILL.md
        └── sales-champion-assistant.zip
```

## Quick Check

```bash
python3 scripts/validate_skill_package.py
```

Expected output:

```text
[ok] sales-champion-assistant skill package validated
```

## Skill Installation

The distributable Skill package is located at:

```text
skill/sales-champion-assistant/sales-champion-assistant.zip
```

If your runtime supports local Skill directories, first generate a staged package with references:

```bash
python3 scripts/validate_skill_package.py --keep-staging
```

Then copy the generated Skill package:

```bash
mkdir -p ~/.codex/skills
cp -R .skill-package-staging/sales-champion-assistant ~/.codex/skills/
```

## Usage Policy

Sales Champion Assistant only uses publicly verifiable information. Unknown items should be marked as "not public"; inferences need evidence; job and salary data must not be fabricated. If search, browser access, or recruiting platforms fail, record the information gap instead of filling it with generic claims.

This project is intended for sales preparation and customer research. For formal business, investment, or legal decisions, rely on original notices, contracts, regulatory filings, and professional advice.

## License

MIT
