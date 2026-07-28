# Sales Champion Assistant / sales-champion-assistant

[中文](README.md) | English

`sales-champion-assistant` is an agent workflow package for B2B sales, business development, and account operations. Given a company name, it turns public information into a company profile, customer rating, hiring and salary signals, key-person leads, capital and government ties, supply-chain position, resource-matching paths, and outreach suggestions.

The project was formerly named `company-intel-report`. The public-facing name is now "Sales Champion Assistant: Company Research And Outreach Strategy" to better match daily sales workflows.

This repository provides:

- A self-contained Codex/OpenClaw-style Skill (prompts, schema, and the sample resource catalog are bundled under `references/`).
- A two-stage Chinese prompt workflow: Researcher creates structured intelligence, Writer turns it into a report.
- A JSON Schema for development-time structure reference.
- A sample resource catalog that maps company leads to actionable outreach paths.
- A validation script for checking the Skill package structure and content contracts.

## Use Cases

- Help sales or BD teams prepare before a customer meeting.
- Evaluate company scale, growth, risk, and possible entry points for account operations.
- Support investment promotion, industry services, and ecosystem partnerships with reusable company background research.
- Turn "research a company, write a report, propose outreach moves" into a reusable workflow.

## Output

A full report includes:

- Overall rating — `★★★ / ★★☆ / ★☆☆` with a standardized label, decided by an industry-first decision table (industry growth + industry position dominate; a severity veto locks the rating at the lowest tier), with the decision trace spelled out.
- GTM customer-segment fact check, including employee count, segment, source platform (third-party estimates are explicitly flagged), and confidence.
- PART 1 star-rating review: sensitivity scan, severity veto check, and five-dimensional scoring — industry growth (policy anchor plus growth-vs-GDP numbers), industry position (credentials and tier), regional position ("local champion" signals), finance and capital (registered capital, funding rounds, R&D ratio), and management profile (numbered advanced factors F1-F7 with hit count and a type label).
- PART 2 deep background review: business overview, history, finance and shareholders, founder and team, digital practice (SaaS/ERP adoption is a mandatory check), hiring and salary signals, plus cross-source contradiction checks.
- PART 3-8: power map, capital and government ties, supply chain, public footprint and strategic concerns, resource-matching outreach strategy, and executive communication suggestions.
- A closing summary with a sales-perspective conclusion, contradiction recap, information gaps, and a disclaimer.

## Repository Layout

```text
.
├── README.md
├── README.en.md
├── LICENSE
├── scripts/
│   └── validate_skill_package.py
└── skill/
    └── sales-champion-assistant/        <- self-contained Skill package
        ├── SKILL.md
        └── references/
            ├── prompts/company_intel_prompts_zh.md
            ├── schema/company_intel_report.schema.json
            └── config/resource_catalog.example.json
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

The Skill package is a self-contained directory — just copy it:

```bash
mkdir -p ~/.codex/skills
cp -R skill/sales-champion-assistant ~/.codex/skills/
```

Runtimes that support symlinks (such as Claude Code) can link it directly:

```bash
ln -s "$(pwd)/skill/sales-champion-assistant" ~/.claude/skills/sales-champion-assistant
```

## Usage Policy

Sales Champion Assistant only uses publicly verifiable information. Unknown items should be marked as "not public"; inferences need evidence; job and salary data must not be fabricated; third-party estimates must name the source platform. If search, browser access, or recruiting platforms fail, follow the retrieval-reliability playbook: degrade gracefully and record the information gap instead of filling it with generic claims.

This project is intended for sales preparation and customer research. For formal business, investment, or legal decisions, rely on original notices, contracts, regulatory filings, and professional advice.

## License

MIT
