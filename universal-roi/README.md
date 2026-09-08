# Universal ROI — Decide Before You Commit

**A decision-grade AI skill that turns any idea into a clear, evidence-backed ROI case: what you could gain, what it will really cost, what could break, and the smallest next move worth making.**

[简体中文完整说明](README.zh-CN.md) · [What it does](#what-it-does) · [Use it](#use-it) · [How it thinks](#how-it-thinks) · [License](#license)

Most ROI calculators ask one question: **“What is the return?”**

Universal ROI asks the questions that decide whether a return is real:

> What happens if we do nothing? Who actually benefits? What will this consume in cash, hours, attention, and alternatives? Which assumption can kill the plan? What does success, failure, and a safe exit look like?

It is built for people who want a decision, not a seductive spreadsheet.

## What it does

Give the skill an idea, objective, constraints, and any data you have. It can research the facts that matter, keep evidence separate from assumptions, and return a practical decision report.

It covers:

- **Real upside** — revenue, savings, time, assets, skills, optionality, and other outcomes, with the recipient and timing made explicit.
- **The full bill** — setup, operations, maintenance, rework, taxes, fees, cash lock-up, exit costs, time, attention, stress, and opportunity cost.
- **Three defensible futures** — best reasonable, base, and worst reasonable scenarios with the conditions behind each; never a made-up “guaranteed result.”
- **Hidden dependencies** — demand, conversion, capacity, data, permissions, vendors, contracts, adoption, reversibility, and the first signals of failure.
- **A decision path** — act, run a small experiment, gather decisive evidence, or stop; with checkpoints, a budget, and exit criteria.
- **Reproducible numbers** — an included Python calculator reports incremental cash ROI, NPV, payback, period-end funding gap, opportunity-cost-adjusted metrics, and probability-weighted results when the probabilities are genuinely defensible.

## Use it

Place this folder in a Codex skills directory, or point Codex at `SKILL.md`. Then ask naturally:

```text
Use $universal-roi to assess this:

I want to build an AI side business. I can spend 8 hours a week and ¥5,000,
and I want revenue within six months. Research demand and real costs. Show me
what I could gain, best/base/worst outcomes, hidden conditions, and the
lowest-cost validation plan.
```

You can use it for an AI agent, startup, purchase, course, career move, relocation, process change, or personal decision. It adapts the measurement to the decision instead of pretending every part of life has a price tag.

### Optional calculator

The calculator has no third-party dependencies:

```bash
python3 scripts/roi_calculator.py /absolute/path/input.json --output /absolute/path/result.json
```

See [`references/calculation.md`](references/calculation.md) for the input schema, formulas, and a synthetic example. It calculates supplied numbers; it does not invent evidence, validate a market, or turn uncertain assumptions into facts.

## How it thinks

```text
Idea + goals + constraints + data
               ↓
Compare against the real alternative: do nothing / another option / a small test
               ↓
Research the assumptions that can change the decision
               ↓
Model incremental benefits, full costs, timing, and constraints
               ↓
Stress-test best reasonable / base / worst reasonable outcomes
               ↓
Make a conditional decision and design the cheapest decisive experiment
```

The skill follows several hard rules:

1. **No fake precision.** Unknown values stay unknown; estimates carry ranges and sources.
2. **No double counting.** Cash returns, monetized non-cash effects, and non-monetizable values are kept separate.
3. **No optimism disguised as a base case.** A scenario includes the conditions required to achieve it.
4. **No ROI without a baseline.** Every result is incremental relative to a credible alternative.
5. **No action by default.** The analysis proposes a path; purchases, messages, trades, and external changes still require the user’s authorization.

## Repository map

```text
universal-roi/
├── SKILL.md                         # Core instructions for the AI/agent
├── agents/openai.yaml               # Codex interface metadata
├── references/
│   ├── calculation.md                # Metrics, formulas, JSON schema, examples
│   ├── decision-checks.md            # Hidden-condition checklists by decision type
│   └── report-template.md            # Decision-report structure
└── scripts/
    └── roi_calculator.py             # Dependency-free reproducible calculator
```

## Who this is for

Founders deciding whether to build. Operators deciding whether to automate. Individuals deciding whether to buy, learn, switch, or wait. Anyone who has been given a confident answer but still does not know what it really costs.

## Contributing

Issues and pull requests are welcome. The most useful contributions are concrete:

- Better checklists for a specific decision type
- Corrections to calculation logic or edge cases
- Evidence-quality improvements and source guidance
- Real, anonymized examples that show where the framework needs to be sharper

Please avoid adding rules that only fit one anecdote. A good contribution makes a future decision more honest, more reproducible, or easier to act on.

## License

[MIT](LICENSE) © 2026 Henry

---

## 简体中文

# Universal ROI —— 在承诺投入之前，先把账算明白

**这是一个用于 AI / Agent 的决策级 ROI Skill：把任何想法转成可查证的收益、真实代价、风险情景和最低成本行动方案。**

普通 ROI 计算器只问“回报是多少”。Universal ROI 会继续追问真正决定成败的问题：不做会怎样？谁真正获益？它会消耗多少现金、时间、注意力与机会？哪项假设一旦失效，整个计划就不成立？成功、失败和退出分别是什么样？

它适用于 AI Agent、创业、副业、购买设备、学习技能、换工作、搬家、流程优化，以及任何“到底值不值得做”的选择。

### 它会交付什么

- 可兑现的收益：收入、节省支出、时间、技能、资产、选择权及其他价值
- 完整成本账：启动、运营、维护、返工、税费、资金占用、退出、精力和机会成本
- 最好合理 / 基准 / 最坏合理三种情景，以及每种情景必须成立的条件
- 被忽略的前提：需求、转化、能力、数据、权限、供应商、采用率、可逆性等
- 明确建议：现在行动、先小试、补关键证据后决定，还是暂不做
- 能复算的财务结果：现金 ROI、NPV、回本期、资金缺口，以及适用时的概率加权结果

### 一句话调用示例

```text
用 $universal-roi 评估：我想用 AI 做一个副业，每周能投入 8 小时，预算 5000 元，希望 6 个月内产生收入。请联网查证需求和成本，分析能得到什么、最好和最坏结果、隐藏条件，并给出最低成本的验证步骤。
```

完整方法与使用方式见上方英文说明及 [`SKILL.md`](SKILL.md)。
