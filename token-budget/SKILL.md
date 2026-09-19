---
name: token-budget
description: Token 预算与节约纪律：定量管理 token 成本。当需要分配里程碑预算、阶段结算记账、控制记忆/注入预算、复盘紧凑输出、统计缓存命中率时触发。关键词：token预算、token记账、token结算、预算分配、紧凑输出、缓存命中率。
metadata:
  author: software-workflow
  version: "2.0"
---

# Token Budget — Token 预算与节约纪律

token 是真实成本：**先定量、再执行、后结算、以实测为准。**

## 触发场景
- 里程碑/阶段开工分配预算（研究/开发分账）
- 阶段结束结算实际消耗
- 注入上下文/恢复记忆需控预算
- 复盘输出紧凑化；统计缓存命中率

## 核心数值（默认，PM 可调）
| 项 | 预算 |
|---|---|
| 恢复记忆 | ≤1000 token |
| 知识注入 | ≤800 token |
| R9 复盘输出 | ≤300 token 摘要 |
| skill 常驻 SKILL.md | ≤1500 token |
| skill 单 references | ≤3000 token |
| 单任务 skill 总消耗 | ≤10000 token |

## 工作流程
1. **开工分配**：里程碑五字段（目标/验收基线/禁区/环境事实/token 预算），PM 拍板。
2. **执行期纪律**：延迟加载（只读入口+当前目标+直接引用）；长文沉文件；禁禁区。
3. **阶段结算（必跑）**：`node tools/token-ledger.mjs <workspace> --out ledger-<日期>.json` → 取 `input+output` 对比预算 → 秒级时间戳记录 → 缓存命中率入看板。超额不阻断但必记录。
4. **复盘紧凑化**：要点+文件:行号+一句话结论，长文沉文件。

## 边界纪律
- 预算是参考值，实际以实测账本为准；超额记录即可。
- 记账是阶段门禁必做项；预算分配是 PM 职责。
- 工具化（tokenMeter/compaction/看板）在插件阶段；当前纪律+文件先行。
