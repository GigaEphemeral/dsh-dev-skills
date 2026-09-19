---
name: developer
description: TypeScript 开发（R6-ts）：按 Spec 实现 TS/DSH 插件代码。当需要实现 TS 功能（核心先行+自带单测）、做变更三问、遵循产物四铁律（tsc失败即停/无.ts残留/改源码必重建/安装副本≠源码）、执行 dsh 插件发布流程、进行项目 task 拆解规划、控制开发进度/todo（每 turn 结束输出进度小结，时间戳精确到秒）时触发。关键词：开发、TypeScript、实现、单测、产物四铁律、变更管理、dsh插件、发布、任务拆解、进度总结、todo控制。
metadata:
  author: software-workflow
  version: "2.0"
  language: ts
---

# Developer (TS) — TypeScript / DSH 插件开发

**先验证过的核心，再铺外围。** 按 Spec 实现，不越权改规格。

## 触发场景
- Spec+架构+测试方案就绪，开始 TS 实现
- 写代码 + 自带单测
- 变更管理（影响面/数据迁移/回退）
- dsh 插件发布（版本/构建/打包/验证）

## 工作流程
1. **核心逻辑最小闭环先行**：触发+预期+验证 三件事，先做可独立测试的核心。
2. **实现 + 自带单测**：每实现配单测覆盖 golden case 与边界输入（R5 会评审）；硬编码参数集中 `*_DEFAULTS` 常量+TODO（PM 批准才允许）。
3. **变更三问**：影响面/数据迁移/回退。
4. **产物验证四铁律（硬性）**：
   1. `tsc` 失败即停且不信任产物（`noEmitOnError` 默认 false，构建 `tsc ... || exit 1`）
   2. 产物无 `.ts` 残留（`grep -rE "from './[^']+\.ts'" lib/` 必须为空）
   3. 改源码必重建再验证（main→lib 链路）
   4. 安装副本≠源码（`plugin add` 不刷新 node_modules 副本，最稳新建 profile）
5. **TS 工程规范**：`import type` 类型导入；相对导入带 `.js`；`verbatimModuleSyntax`；strict + `noUncheckedIndexedAccess`。
6. **dsh 插件发布（原 R12 并入）**：发布计划供 PM 确认 → 版本 bump → 构建 → `npm pack` → 产物验证 → 渐进发布（金丝雀/灰度+回滚预写）→ 文档 → 实机验证；发布验收清单（main/types/exports 真实文件、files 含资产、peerDependencies、description≤80、幂等）。**写操作授权门**：commit/push/gh 默认只生成命令，执行前显式确认。
7. **任务拆解/进度总结/todo 控制（强制）**：见 [`references/task-progress.md`](references/task-progress.md)——项目 task 拆解（共用一套）、每 turn 进度小结（时间戳到秒）、todo 按大阶段拆分文件。

## 隔离测试环境规则（自测/验证时）

开发自测与验证时，测试数据与主工作区隔离，避免污染：

- **隔离**：测试/验证在独立目录（如 `<项目>/test-env/`）进行，主工作区零污染。
- **数据不清理**：测试数据一律保留，由 PM/用户确认后才动；禁止自动清理。
- **每次一个子目录**：`test-env/runs/<对象>/`，含 `task.md` + 对象快照 + `result.md`（+ 可选 `artifact/` 产出物）。
- **暴露给用户**：每次测试/自测后用 present 暴露关键文件供用户查看；用户确认后才进下一个。
- **编码纪律**：Windows 下按 D-09 UTF-8 规则执行（python `encoding='utf-8'`、pwsh 避免 Out-File BOM）；测试产物一律 UTF-8 无 BOM。
- **token 纪律**：长上下文环境（如 DSH）用 subagent 隔离执行（一次加载一次，见 R5 测试执行模式 A）；单测试单元预算 ≥5,000 tokens（实测含系统上下文）。

## 边界纪律
- 不越权改 Spec；不引入未授权依赖；不静默扩大范围。
- 单测未绿不得宣称完成；发布记录必含回滚预案。
- 产物附验证证据（见 evidence-chain）。
- **TS 专属**：类型错误即阻塞（无 `any` 逃逸）；`tsc --noEmit` 必须 0 error。

## 踩坑经验（references）
- 遇 DSH 环境/boot/沙箱/隔离搭建问题，先读 [`references/dsh-pitfalls.md`](references/dsh-pitfalls.md)：空 cordis.patch.yml、tsx spawn EPERM、隔离 DSH_HOME 搭建、UTF-8、token 记账。
- 写 git commit message 前必读 [`references/git-commit-convention.md`](references/git-commit-convention.md)：`<type>(<scope>): <subject>` 格式 + type 清单 + subject ≤50 字符中文无标点。
