# 1skillCode — 软件开发工作流 Skill 资产包

## 项目总体目标

**固化并优化软件开发的工作流**——把「需求 → 架构 → 测试方案 → 研发 → 测试回归 → 质量管理 → 项目经验总结（→ skill 优化）」这一全链路沉淀为可复用、可检索、可持续进化的方法论 skill 资产，并在后续阶段组合为 agent persona（阶段二）与专业团队插件（阶段三）。

## 项目结构

```
1skillCode/
├── README.md                     # 本文件：总体目标 / 结构 / skill 列表 / 状态
├── dsh-test-plan.md              # DSH 开发测试方案（本体/插件/skill/预设四类）
├── gates/                        # 横切：门禁纪律（S0-S5 退出标准检查）
├── evidence-chain/               # 横切：证据链纪律（无证据=未完成）
├── token-budget/                 # 横切：Token 预算纪律（定量/记账/紧凑输出）
├── R1-brainstormer/              # 需求发散（追问式扩充边界 + 联网竞品调研）
├── R2-spec-owner/                # 需求收敛（可验收指标 + 边界输入）
├── R3-pm/                        # 产品经理决策（四段决策 / YAGNI / 魔法值判定）
├── R4-ts-architect/              # TS 架构师（模块/类型/供应链门禁/架构文档）
├── R5-ts-test-designer/          # TS 测试方案（vitest/golden case/分层）
├── R6-ts-developer/              # TS 开发（产物四铁律/发布/踩坑经验）
├── R7-qa/                        # 测试回归（报告闭环/日志排查/发布合规）
├── R8-reviewer/                  # 代码审核（双轴/分级/阶段末状态化）
├── R9-recapper/                  # 复盘+知识提炼（九段证据链/知识分层/紧凑输出）
├── R10-budget-auditor/           # Token 预算审计（结算/注入预算//compact 适配）
├── test-env/                     # 隔离测试环境（运行时数据，不进版本库）
└── tools/
    ├── keyword-gate.py           # 关键词监测/限制门禁脚本
    └── README.md                 # keyword-gate 使用说明
```

每个 skill 一个目录：`<name>/SKILL.md`（frontmatter + 触发场景 + 工作流程 + 边界纪律 + token 预算 ≤1,500 常驻），踩坑经验放 `<name>/references/`。

## Skill 列表

### 横切纪律三件套（无语言绑定）
| skill | 目录 |
|---|---|
| 门禁纪律 | `gates/` |
| 证据链纪律 | `evidence-chain/` |
| Token 预算纪律 | `token-budget/` |

### 流程角色（无语言绑定）
| 角色 | 目录 | 一句话 |
|---|---|---|
| R1 需求发散 | `R1-brainstormer/` | 帮用户**扩充需求边界**（追问式）+ 主动建议联网竞品调研 |
| R2 需求收敛 | `R2-spec-owner/` | 形容词→可验收指标；边界输入写死 |
| R3 产品经理 | `R3-pm/` | 决策四段；退出标准；YAGNI；魔法值判定 |
| R7 测试回归 | `R7-qa/` | 无证据未完成；报告闭环；日志排查 |
| R8 代码审核 | `R8-reviewer/` | 双轴审查；分级清单；阶段末状态化 |
| R9 复盘+知识 | `R9-recapper/` | 九段证据链；知识分层；紧凑输出 |
| R10 预算审计 | `R10-budget-auditor/` | 结算记账；注入预算；/compact 适配 |

### 按语言的专门专家（本轮 TS，前缀 `ts-`）
| 角色 | 目录 | 专门化点 |
|---|---|---|
| R4 架构师（TS） | `R4-ts-architect/` | TS 模块划分/类型设计/依赖/供应链门禁；严格约束+文档结构 |
| R5 测试方案（TS） | `R5-ts-test-designer/` | TS 测试栈（vitest/type testing）；golden case；分层 |
| R6 开发（TS） | `R6-ts-developer/` | TS/DSH 插件开发；产物四铁律；发布；踩坑经验 |

> 后续语言扩展：新增 `R4-py-architect/`、`R5-py-test-designer/`、`R6-py-developer/` 等，遵循同模板。

## 状态

- [x] 目录骨架 + 本 README
- [x] gates / evidence-chain / token-budget（横切三件套）
- [x] R1-R3 / R7-R10（流程角色，R1 按新要求重写）
- [x] R4-ts / R5-ts / R6-ts（语言专门专家，TS 版）
- [x] tools/keyword-gate.py（关键词监测限制，已 PASS）
- [x] token 预算自检：13/13 skill 常驻 ≤1,500 tokens（最高 R1 920）
- [x] [DSH 开发测试方案](dsh-test-plan.md)（本体/插件/skill/预设四类；模式 A subagent 隔离）
- [ ] 每个 skill 真实小任务试跑验收（阶段一门禁，按 dsh-test-plan 执行）
