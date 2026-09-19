# TS 测试经验（references · R5-ts-test-designer）

> 固化来源：本项目 DSH 测试方案（`1skillCode/dsh-test-plan.md`）实际执行中的经验（2026-09-18~19）。

## 1. Skill 测试模式 A：subagent 隔离（一次加载一次）
- **问题**：DSH 的 `skill` 工具把 SKILL.md 一次性注入上下文，**注入后无卸载机制**；同一上下文反复加载 = 重复 token + 互相污染。
- **解法**：每个测试单元独立上下文——fork subagent，只注入被测 SKILL.md 一次，执行任务后销毁；主会话零污染。可并行多个 skill 测试。
- **验收**：结构化返回（PASS/FAIL + 验收项逐条 + 问题清单 + token 估算）。

## 2. token 预算：估算 vs 实测
- **问题**：单单元预算 3,000 实测不够——subagent 的系统上下文也计入。
- **实测**：R1 ≈10,000（注入 6-7k + 执行 3.5-4k）；R4-ts ≈6,600；R6-ts ≈3,000。
- **处置**：单单元预算设 5,000-10,000（按任务复杂度）；测试串行省 token。

## 3. keyword-gate 脚本 BOM 坑（Windows）
- **症状**：pwsh `Out-File` 写 JSON 带 BOM，python `json.load` 报 `Unexpected UTF-8 BOM`。
- **处置**：pwsh 写文件避免默认 BOM，或 python 读 `encoding='utf-8-sig'`；测试产物一律 UTF-8 无 BOM（D-09）。

## 4. 验收口径要"可测"
- R1（追问式发散）验收 A1-A6 每条都是可判断的（是否覆盖五方向/是否标⚠️/是否分轮），实测有效。
- 设计验收项时：**每条必须是"满足/不满足 + 一句话证据"可判**，不写模糊标准（如"质量好"）。

## 5. 测试环境规则（D-10）
- 隔离环境 `1skillCode/test-env/`：数据不清理、由用户确认；每次试跑 `runs/<skill>/`（task+snapshot+result+artifact）；自测 `selfcheck/`；测试后 present 暴露给用户。
