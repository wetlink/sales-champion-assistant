# 销冠助手：企业调研与建联策略 / sales-champion-assistant

中文 | [English](README.en.md)

`sales-champion-assistant` 是一个面向 ToB 销售、BD 和客户经营的智能体工作流包。输入企业名称后，它会围绕公开信息整理企业画像、客户评级、招聘薪资信号、关键人线索、资本与政府关系、产业链位置、资源匹配路径和沟通建议。

这个项目原名 `company-intel-report`。开源展示名调整为「销冠助手：企业调研与建联策略」，更贴近日常使用场景。

仓库提供：

- 一份自包含的 Codex/OpenClaw 风格 Skill（prompts、schema、资源池样例都打包在 `references/` 内）。
- 两阶段中文提示词：Researcher 先产出结构化情报，Writer 再生成报告。
- 一份 JSON Schema，用作开发期结构参考。
- 一份资源池样例，用于把企业线索转成可执行的建联路径。
- 一个校验脚本，用来检查 Skill 包结构和内容口径。

## 适合场景

- 销售或 BD 准备拜访前，快速了解目标企业。
- 客户经营需要判断企业规模、成长性、风险和切入口。
- 招商、产业服务、生态合作团队需要整理客户背景和资源匹配方式。
- 团队希望把"查企业 + 写报告 + 给建联打法"沉淀为可复用流程。

## 输出内容

完整报告结构：

- 综合评级：`★★★（高潜领军者）/★★☆（中坚力量）/★☆☆（稳健/高危）`，由"行业双维主导判定表"得出（行业增长+行业地位双维主导，严重性熔断最优先），并写明判定依据。
- GTM 客群 Fact Check：员工数、客户分层、来源平台（第三方估算显式标注 `⚠️第三方估算（平台名）`）和置信度。
- 【PART 1: 星标评级评估】敏感性扫描、严重性检查、五维星级评估——行业增长（政策锚点 + 行业增速 vs GDP 数字对比）、行业地位（资质与梯队定位）、区域地位（"地头蛇"信号）、财务和资本（注册资本/融资轮次/研发占比）、管理层画像（先进因子 F1-F7 命中计数 + 类型标签）。
- 【PART 2: 深度背景调查】业务概览、发展历程、财务与股东、创始人与团队、数字化实践（SaaS/ERP 使用必查）、招聘与薪资信号，含跨来源矛盾核查。
- 【PART 3-8】权力地图与人物画像、资本背景与政府关系、上下游产业链、社会足迹与战略焦虑、资源匹配建联策略、高管沟通方式建议。
- 综合说明：销售视角结论、矛盾核查汇总、信息缺口、免责说明。

## 目录

```text
.
├── README.md
├── README.en.md
├── LICENSE
├── scripts/
│   └── validate_skill_package.py
└── skill/
    └── sales-champion-assistant/        ← 自包含 Skill 包
        ├── SKILL.md
        └── references/
            ├── prompts/company_intel_prompts_zh.md
            ├── schema/company_intel_report.schema.json
            └── config/resource_catalog.example.json
```

## 快速检查

项目本身不依赖第三方 Python 包。建议使用 Python 3.10 或更高版本。

```bash
python3 scripts/validate_skill_package.py
```

通过后会看到：

```text
[ok] sales-champion-assistant skill package validated
```

这个校验会检查：

- `SKILL.md` 的 frontmatter 名称。
- Skill 中引用的 prompt、schema 和配置文件是否真实存在于包内。
- Prompt 是否保留关键流程标记（判定表、先进因子、数字化实践、检索可靠性等）。
- Schema 与 Prompt 内嵌 JSON 模板的关键字段是否一致。
- 资源池样例是否包含政府关系、客户池、资本网络、校友/协会、招聘入口和合规字段。

## Skill 安装

Skill 包是自包含目录，直接复制即可：

```bash
mkdir -p ~/.codex/skills
cp -R skill/sales-champion-assistant ~/.codex/skills/
```

Claude Code 等支持 symlink 的运行时也可以直接链接：

```bash
ln -s "$(pwd)/skill/sales-champion-assistant" ~/.claude/skills/sales-champion-assistant
```

安装后，智能体在遇到"查一下这家公司""做一份客户建联报告""给我一个 BD 拜访策略""整理某公司的客户画像"等需求时，会按 `SKILL.md` 调用这套流程。

## 资源池配置

`skill/sales-champion-assistant/references/config/resource_catalog.example.json` 是一个示例资源池，包含：

- 政府关系入口。
- 链主客户和行业客户池。
- 资本网络。
- 校友和商协会。
- 招聘入口。
- 合规边界。

实际使用时，请把样例中的 `your_team_name`、`客户A`、`客户B` 等替换成团队自己的资源。报告中的"资源匹配建联策略"会依赖这份资源池，资源越清楚，建议越能落地。

## 使用口径

销冠助手只使用公开可核验信息。无法确认的内容写"未公开"；推断内容需要标注依据；招聘岗位和薪资不能编造；第三方平台估算必须标注来源平台。遇到浏览器、搜索、招聘平台反爬或页面超时，按"检索可靠性 Playbook"降级并记录信息缺口，避免用空泛判断补齐。

这个项目适合做销售准备和客户研究。正式商务决策、投资判断或法律判断，请以原始公告、合同、监管文件和专业意见为准。

## License

MIT
