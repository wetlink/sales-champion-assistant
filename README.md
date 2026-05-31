# 销冠助手：企业调研与建联策略 / sales-champion-assistant

`sales-champion-assistant` 是一个面向 ToB 销售、BD 和客户经营的智能体工作流包。输入企业名称后，它会围绕公开信息整理企业画像、客户评级、招聘薪资信号、关键人线索、资本与政府关系、产业链位置、资源匹配路径和沟通建议。

`sales-champion-assistant` is an agent workflow package for B2B sales, business development, and account operations. Given a company name, it turns public information into a company profile, customer rating, hiring and salary signals, key-person leads, capital and government ties, supply-chain position, resource-matching paths, and outreach suggestions.

这个项目原名 `company-intel-report`。开源展示名调整为「销冠助手：企业调研与建联策略」，更贴近日常使用场景。

The project was formerly named `company-intel-report`. The public-facing name is now "Sales Champion Assistant: Company Research And Outreach Strategy" to better match daily sales workflows.

仓库提供：

This repository provides:

- 一份 Codex/OpenClaw 风格的 Skill。
- A Codex/OpenClaw-style Skill.
- 两阶段中文提示词：Researcher 先产出结构化情报，Writer 再生成报告。
- A two-stage Chinese prompt workflow: Researcher creates structured intelligence, Writer turns it into a report.
- 一份 JSON Schema，用来约束结构化情报字段。
- A JSON Schema for validating the structured intelligence fields.
- 一份资源池样例，用于把企业线索转成可执行的建联路径。
- A sample resource catalog that maps company leads to actionable outreach paths.
- 一个轻量校验脚本，用来检查 Skill 打包结构。
- A lightweight validation script for checking the Skill package structure.

## 适合场景 / Use Cases

- 销售或 BD 准备拜访前，快速了解目标企业。
- Help sales or BD teams prepare before a customer meeting.
- 客户经营需要判断企业规模、成长性、风险和切入口。
- Evaluate company scale, growth, risk, and possible entry points for account operations.
- 招商、产业服务、生态合作团队需要整理客户背景和资源匹配方式。
- Support investment promotion, industry services, and ecosystem partnerships with reusable company background research.
- 团队希望把“查企业 + 写报告 + 给建联打法”沉淀为可复用流程。
- Turn "research a company, write a report, propose outreach moves" into a reusable workflow.

## 输出内容 / Output

完整报告包含：

A full report includes:

- 企业信息与星标评级。
- Company information and star rating.
- GTM 客群 Fact Check，包括员工数、客户分层、来源和置信度。
- GTM customer-segment fact check, including employee count, segment, source, and confidence.
- 敏感性扫描与严重性检查。
- Sensitivity and severity review.
- 五维星级评估：行业增长、行业地位、区域地位、财务和资本、管理层画像。
- Five-dimensional scoring: industry growth, industry position, regional position, finance and capital, and management profile.
- 招聘信息与薪资水平分析。
- Hiring and salary analysis.
- 权力地图与人物画像。
- Power map and key-person profiles.
- 资本背景与政府关系。
- Capital background and government ties.
- 上下游产业链。
- Upstream and downstream supply-chain view.
- 社会足迹与战略焦虑。
- Public footprint and strategic concerns.
- 资源匹配建联策略。
- Resource-matching outreach strategy.
- 高管沟通方式建议。
- Executive communication suggestions.

## 目录 / Repository Layout

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

## 快速检查 / Quick Check

项目本身不依赖第三方 Python 包。建议使用 Python 3.10 或更高版本。

The project itself does not require third-party Python packages. Python 3.10 or newer is recommended.

```bash
python3 scripts/validate_skill_package.py
```

通过后会看到：

Expected output:

```text
[ok] sales-champion-assistant skill package validated
```

这个校验会检查：

The validator checks:

- `SKILL.md` 的 frontmatter 名称。
- Skill 中引用的 prompt、schema 和配置文件是否能被打包。
- JSON Schema 是否要求 `enterprise_info`。
- Prompt 是否保留关键流程标记。
- 资源池样例是否包含政府关系、客户池、资本网络、校友/协会、招聘入口和合规字段。

## Skill 安装 / Skill Installation

Skill 分发包已放在：

The distributable Skill package is located at:

```text
skill/sales-champion-assistant/sales-champion-assistant.zip
```

如果你的运行时支持本地 Skill 目录，推荐先生成带引用文件的打包目录：

If your runtime supports local Skill directories, first generate a staged package with references:

```bash
python3 scripts/validate_skill_package.py --keep-staging
```

然后复制生成的 Skill 包：

Then copy the generated Skill package:

```bash
mkdir -p ~/.codex/skills
cp -R .skill-package-staging/sales-champion-assistant ~/.codex/skills/
```

安装后，智能体在遇到“查一下这家公司”“做一份客户建联报告”“给我一个 BD 拜访策略”“整理某公司的客户画像”等需求时，可以按 `SKILL.md` 调用这套流程。校验脚本会把 `prompts/`、`schema/` 和 `config/` 放入 Skill 包的 `references/` 目录，便于运行时读取。

After installation, an agent can follow `SKILL.md` when asked to research a company, create an account outreach report, draft a BD visit strategy, or build a customer profile. The validator packages `prompts/`, `schema/`, and `config/` into the Skill `references/` directory.

## 资源池配置 / Resource Catalog

`config/resource_catalog.example.json` 是一个示例资源池，包含：

`config/resource_catalog.example.json` is a sample resource catalog containing:

- 政府关系入口。
- 链主客户和行业客户池。
- 资本网络。
- 校友和商协会。
- 招聘入口。
- 合规边界。

实际使用时，请把样例中的 `your_team_name`、`客户A`、`客户B` 等替换成团队自己的资源。报告中的“资源匹配建联策略”会依赖这份资源池，资源越清楚，建议越能落地。

In real use, replace placeholders such as `your_team_name`, `客户A`, and `客户B` with your own team resources. The "resource-matching outreach strategy" depends on this catalog; clearer resources produce more actionable suggestions.

## 使用口径 / Usage Policy

销冠助手只使用公开可核验信息。无法确认的内容写“未公开”；推断内容需要标注依据；招聘岗位和薪资不能编造。遇到浏览器、搜索、招聘平台反爬或页面超时，报告应记录信息缺口，避免用空泛判断补齐。

Sales Champion Assistant only uses publicly verifiable information. Unknown items should be marked as "not public"; inferences need evidence; job and salary data must not be fabricated. If search, browser access, or recruiting platforms fail, record the information gap instead of filling it with generic claims.

这个项目适合做销售准备和客户研究。正式商务决策、投资判断或法律判断，请以原始公告、合同、监管文件和专业意见为准。

This project is intended for sales preparation and customer research. For formal business, investment, or legal decisions, rely on original notices, contracts, regulatory filings, and professional advice.

## License

MIT
